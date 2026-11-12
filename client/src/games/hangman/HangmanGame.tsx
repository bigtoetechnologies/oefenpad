import { useCallback, useEffect, useRef, useState } from 'react';
import { api, ApiError, fill } from '../../api';
import { GameShell } from '../../site/GameShell';
import { Overlay } from '../../shared/Overlay';
import { ResumeNote } from '../../shared/ResumeNote';
import { WordImage } from '../../shared/WordImage';
import { spawnConfetti } from '../../shared/confetti';
import { formatTime } from '../../shared/format';
import { sfx } from '../../shared/sound';
import { useGameData } from '../../shared/useGameData';
import { useLocalStorage } from '../../shared/useLocalStorage';
import { useTimer } from '../../shared/useTimer';
import { CANVAS_HEIGHT, CANVAS_WIDTH, drawGallows } from './gallows';

const GAME = 'hangman';

const SETTINGS_KEY = 'oefenpad-galgje-settings';
const STATS_KEY = 'oefenpad-galgje-stats';

/** The round view HangmanService.View builds. */
interface HangmanView {
  category: { id: string; name: string; icon: string };
  difficulty: string;
  maxWrong: number;
  wrong: number;
  guessed: string[];
  pattern: Array<{ gap: boolean; text: string | null; revealed: boolean }>;
  wordLength: number;
  hintsLeft: number;
  status: 'playing' | 'won' | 'lost';
  clueImageUrl: string | null;
  translation: string | null;
  answer: string | null;
  imageUrl: string | null;
}

interface Settings {
  soundEffects: boolean;
  translateTo: string;
}

interface Stats {
  wins: number;
  losses: number;
  streak: number;
  bestStreak: number;
}

interface RoundNumber {
  category: string;
  difficulty: string;
  translateTo: string;
}

/** A letter the server or a hint confirmed is in the word. */
interface PositiveLetter {
  roundId: string;
  letter: string;
}

/** A change that needs the player's consent while a round is running. */
interface PendingChange {
  round: RoundNumber;
  after?: () => void;
}

const DEFAULT_SETTINGS: Settings = { soundEffects: true, translateTo: '' };
const DEFAULT_STATS: Stats = { wins: 0, losses: 0, streak: 0, bestStreak: 0 };

/** Dutch only: there is no language switch in this game. */
const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const KEYBOARD_ROWS = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'];

/** The only translation the service offers is English. */
const TRANSLATE_TO = 'en';

const CONFETTI_COLORS = ['#FFB300', '#009688', '#E57373', '#64B5F6', '#81C784', '#BA68C8'];

/** Optional strings the texts endpoint may or may not carry. */
const EXTRA_TEXT: Record<string, string> = {
  'a11y-difficulty': 'Moeilijkheidsgraad',
  'a11y-keyboard': 'Letters',
  'a11y-blank': 'leeg',
  'a11y-space': 'spatie',
  'a11y-key-hit': '{letter}, goed',
  'a11y-key-miss': '{letter}, niet in het woord',
  'btn-try-again': 'Opnieuw proberen',
};

export function HangmanGame() {
  const { texts, options, error } = useGameData(GAME);

  if (error !== null) {
    return (
      <GameShell game={GAME} title="Galgje">
        <main className="app-container">
          <p role="alert" className="laden">
            {error}
          </p>
        </main>
      </GameShell>
    );
  }

  if (texts === null || options === null) {
    return (
      <GameShell game={GAME} title="Galgje">
        <main className="app-container">
          <p className="laden">Even laden…</p>
        </main>
      </GameShell>
    );
  }

  return (
    <HangmanBoard
      texts={texts}
      categories={options.categories.map((category) => ({
        id: category.id,
        name: category.name,
        icon: category.icon,
      }))}
    />
  );
}

interface CategoryChoice {
  id: string;
  name: string;
  icon: string;
}

interface BoardProps {
  texts: Record<string, string>;
  categories: CategoryChoice[];
}

function HangmanBoard({ texts, categories }: BoardProps) {
  const settingsStore = useLocalStorage<Settings>(SETTINGS_KEY, DEFAULT_SETTINGS);
  const statsStore = useLocalStorage<Stats>(STATS_KEY, DEFAULT_STATS);

  const settings: Settings = {
    ...DEFAULT_SETTINGS,
    ...settingsStore[0],
    translateTo: settingsStore[0]?.translateTo === TRANSLATE_TO ? TRANSLATE_TO : '',
  };

  const [roundId, setRoundId] = useState<string | null>(null);
  const [view, setView] = useState<HangmanView | null>(null);
  const [choice, setChoice] = useState<RoundNumber | null>(null);
  const [pending, setPending] = useState<PendingChange | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [resumed, setResumed] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  /* The view hides which letters are in the word until a guess is judged,
     so the keyboard's colouring is remembered from the verdicts. */
  const [positiveLetters, setPositiveLetters] = useState<PositiveLetter[]>([]);
  const [translationShown, setTranslationShown] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [celebrationOpen, setCelebrationOpen] = useState(false);
  const [loseOpen, setLoseOpen] = useState(false);
  const [lastWon, setLastWon] = useState<{ seconds: number; streak: number } | null>(null);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const confettiRef = useRef<HTMLDivElement>(null);
  const roundIdRef = useRef<string | null>(null);
  const busyRef = useRef(false);

  useEffect(() => {
    document.title = texts['page-title'] ?? 'Galgje';
  }, [texts]);

  const t = useCallback(
    (key: string): string => texts[key] ?? EXTRA_TEXT[key] ?? '',
    [texts],
  );

  /** The finished round's answer, which the view only carries once it is over. */
  const answer = view === null ? '' : view.answer ?? '';

  const playing = view !== null && view.status === 'playing';
  const seconds = useTimer(playing, roundId);
  const secondsRef = useRef(seconds);
  useEffect(() => {
    secondsRef.current = seconds;
  }, [seconds]);

  /* ---------- rounds ---------- */

  const startRound = useCallback(
    async (next: RoundNumber) => {
      if (busyRef.current) return;
      busyRef.current = true;
      setStarting(true);
      setNotice(null);
      setResumed(null);
      setPending(null);
      setCelebrationOpen(false);
      setLoseOpen(false);
      setTranslationShown(false);

      try {
        const round = await api.start<HangmanView>(GAME, {
          category: next.category,
          difficulty: next.difficulty,
          translateTo: next.translateTo,
        });
        roundIdRef.current = round.roundId;
        setRoundId(round.roundId);
        setChoice(next);
        setView(round.view);
        setPositiveLetters([]);
      } catch (cause) {
        setNotice(cause instanceof ApiError ? cause.message : 'De oefening is even niet bereikbaar.');
      } finally {
        busyRef.current = false;
        setStarting(false);
      }
    },
    [],
  );

  /* ---------- finish ---------- */

  const finishRef = useRef<(next: HangmanView) => void>(() => {});

  finishRef.current = (next: HangmanView) => {
    if (next.status === 'won') {
      const streak = (statsStore[0].streak ?? 0) + 1;
      statsStore[1]((current) => ({
        ...current,
        wins: (current.wins ?? 0) + 1,
        streak,
        bestStreak: Math.max(current.bestStreak ?? 0, streak),
      }));
      setLastWon({ seconds: secondsRef.current, streak });
      setCelebrationOpen(true);
      const container = confettiRef.current;
      window.requestAnimationFrame(() => {
        spawnConfetti(container, {
          colors: CONFETTI_COLORS,
          count: 80,
          duration: [2, 4],
          delay: [0, 0.6],
          clear: false,
          removeAfter: 4600,
        });
      });
      sfx.fanfare(settings.soundEffects);
    } else if (next.status === 'lost') {
      statsStore[1]((current) => ({ ...current, losses: (current.losses ?? 0) + 1, streak: 0 }));
      setLoseOpen(true);
    }
  };

  /* ---------- moves ---------- */

  const send = useCallback(
    async (body: { action: 'guess'; letter: string } | { action: 'hint' }) => {
      const id = roundIdRef.current;
      if (id === null || busyRef.current) return;
      busyRef.current = true;

      try {
        const result = await api.move<HangmanView>(GAME, id, body);
        setView(result.view);
        // A hint always reveals a letter that is in the word.
        if (result.correct === false) sfx.wrong(settings.soundEffects);
        else {
          sfx.correct(settings.soundEffects);
          if (body.action === 'guess') {
            setPositiveLetters((current) => [...current, { roundId: id, letter: body.letter }]);
          }
        }
        if (result.done) finishRef.current(result.view);
      } catch (cause) {
        if (cause instanceof ApiError) {
          setNotice(cause.message);
          if (cause.status === 410) {
            roundIdRef.current = null;
            setRoundId(null);
          }
        } else {
          setNotice('De oefening is even niet bereikbaar.');
        }
      } finally {
        busyRef.current = false;
      }
    },
    [settings.soundEffects],
  );

  const overlayOpen = celebrationOpen || loseOpen || settingsOpen || categoryOpen;
  const overlayOpenRef = useRef(overlayOpen);
  overlayOpenRef.current = overlayOpen;

  const guess = useCallback(
    (letter: string) => {
      if (view === null || view.status !== 'playing') return;
      if (view.guessed.includes(letter)) return;
      if (!ALPHABET.includes(letter)) return;
      if (overlayOpen || pending !== null) return;
      void send({ action: 'guess', letter });
    },
    [overlayOpen, pending, send, view],
  );

  const requestHint = useCallback(() => {
    if (view === null || view.status !== 'playing' || view.hintsLeft <= 0) return;
    if (overlayOpen || pending !== null) return;
    void send({ action: 'hint' });
  }, [overlayOpen, pending, send, view]);

  /* ---------- physical keyboard ---------- */

  const guessRef = useRef(guess);
  useEffect(() => {
    guessRef.current = guess;
  }, [guess]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.ctrlKey || event.metaKey || event.altKey) return;
      if (event.key.length !== 1) return;
      const letter = event.key.toUpperCase();
      if (!ALPHABET.includes(letter)) return;
      if (overlayOpenRef.current) return;
      guessRef.current(letter);
    };
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, []);

  /* ---------- canvas ---------- */

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas === null || view === null) return;

    const paint = () => {
      drawGallows(canvas, view.wrong, document.documentElement.classList.contains('dark'));
    };
    paint();
    document.addEventListener('themechange', paint);
    return () => document.removeEventListener('themechange', paint);
  }, [view]);

  /* ---------- leave guard, as the old page had ---------- */

  // Only a game still being played is worth warning about. roundIdRef outlives
  // the round — it is cleared only on a 410 — so a won or lost game would
  // otherwise raise the browser's "changes may not be saved" on the way out.
  const inProgressRef = useRef(false);
  inProgressRef.current = view !== null && view.status === 'playing' && view.guessed.length > 0;

  useEffect(() => {
    const onBeforeUnload = (event: BeforeUnloadEvent) => {
      if (roundIdRef.current === null || !inProgressRef.current) return;
      event.preventDefault();
      event.returnValue = '';
    };
    window.addEventListener('beforeunload', onBeforeUnload);
    return () => window.removeEventListener('beforeunload', onBeforeUnload);
  }, []);

  /* ---------- the first round ---------- */

  const startedRef = useRef(false);
  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;

    void (async () => {
      const saved = await api.saved<HangmanView>(GAME).catch(() => null);
      if (saved !== null) {
        roundIdRef.current = saved.roundId;
        setRoundId(saved.roundId);
        setChoice({
          category: saved.view.category.id,
          difficulty: saved.view.difficulty,
          translateTo: saved.view.translation === null ? '' : TRANSLATE_TO,
        });
        setView(saved.view);
        setPositiveLetters(positiveLettersOf(saved.view));
        setResumed(t('resumed'));
        return;
      }

      const first = categories[0];
      void startRound({
        category: first === undefined ? 'animals' : first.id,
        difficulty: 'medium',
        translateTo: settings.translateTo,
      });
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const positiveLettersOf = (view: HangmanView): PositiveLetter[] =>
    view.guessed
      .filter((letter) => view.pattern.some(
        (item) => item.revealed && item.text !== null && item.text.toUpperCase() === letter,
      ))
      .map((letter) => ({ roundId: roundIdRef.current ?? '', letter }));

  /* ---------- starting something new ---------- */

  const inProgress = view !== null && view.status === 'playing' && view.guessed.length > 0;

  const beginRound = (next: RoundNumber, after?: () => void) => {
    if (inProgress) {
      setPending({ round: next, after });
      return;
    }
    void startRound(next);
    after?.();
  };

  const confirmNewGame = () => {
    if (pending === null) return;
    const { round, after } = pending;
    setPending(null);
    void startRound(round);
    after?.();
  };

  const requestDifficulty = (difficulty: string) => {
    if (choice === null || difficulty === choice.difficulty) return;
    beginRound({ ...choice, difficulty });
  };

  const requestCategory = (categoryId: string) => {
    setCategoryOpen(false);
    if (choice === null) return;
    beginRound({ ...choice, category: categoryId });
  };

  const requestRandomCategory = () => {
    setCategoryOpen(false);
    if (choice === null || categories.length === 0) return;
    const pick = categories[Math.floor(Math.random() * categories.length)];
    beginRound({ ...choice, category: pick.id });
  };

  const updateTranslateTo = (value: string) => {
    const next = value === TRANSLATE_TO ? TRANSLATE_TO : '';
    if (next === settings.translateTo) return;

    settingsStore[1]({ ...settings, translateTo: next });

    if (choice === null) return;

    // Turning translation off keeps the current word: translated words are
    // a subset of all words, so only the hint disappears.
    if (next === '') {
      setTranslationShown(false);
      return;
    }

    beginRound(
      { ...choice, translateTo: next },
      () => {
        setSettingsOpen(false);
      },
    );
  };

  const retryRound = () => {
    const last = choice ?? {
      category: categories[0]?.id ?? 'animals',
      difficulty: 'medium',
      translateTo: settings.translateTo,
    };
    void startRound(last);
  };

  /* ---------- derived content ---------- */

  // The full word is only known once it is over; the keyboard colours a
  // guessed letter from the verdict the server gave it.
  const word = view === null
    ? ''
    : view.pattern.map((item) => item.text ?? '').join('');
  const currentRound = roundId;
  const correctLetters = positiveLetters
    .filter((item) => item.roundId === currentRound)
    .map((item) => item.letter);
  const isCorrectLetter = (letter: string): boolean =>
    correctLetters.includes(letter) || word.includes(letter);
  const translation = view?.translation ?? null;
  // The service only answers with English, whatever was asked for.
  const translationLanguage = translation === null ? undefined : TRANSLATE_TO;

  const spokenWord = view === null
    ? ''
    : view.pattern
        .map((item) => {
          if (item.gap) return t('a11y-space');
          return item.revealed ? item.text ?? '' : t('a11y-blank');
        })
        .join(', ');

  const displayed = view;

  const body = (
    <main className="app-container">
      <div
        className="difficulty-bar"
        role="group"
        aria-label={t('a11y-difficulty')}
      >
        {(['easy', 'medium', 'hard'] as const).map((difficulty) => {
          const active = (choice?.difficulty ?? 'medium') === difficulty;
          return (
            <button
              key={difficulty}
              type="button"
              className={active ? 'diff-btn active' : 'diff-btn'}
              aria-pressed={active}
              onClick={() => requestDifficulty(difficulty)}
            >
              {t(`diff-${difficulty}`)}
            </button>
          );
        })}
      </div>

      <div className="status-row" aria-live="polite" aria-atomic="false">
        <button
          type="button"
          className="status-chip"
          title={t('cat-title')}
          onClick={() => setCategoryOpen(true)}
        >
          <span>{displayed?.category.icon ?? ''}</span>
          <span>{displayed?.category.name ?? ''}</span> ▾
        </button>
        <span className="status-item">
          ❌ {displayed?.wrong ?? 0}/{displayed?.maxWrong ?? 10}
        </span>
        <span className="status-item">⏱ {formatTime(seconds)}</span>
      </div>

      {notice === null ? null : (
        <div className="status-row" role="alert">
          <span>{notice}</span>
          <button type="button" className="status-chip" onClick={retryRound}>
            {t('btn-try-again')}
          </button>
        </div>
      )}

      <ResumeNote text={resumed} onDone={() => setResumed(null)} />

      <div className="game-area">
        <canvas
          id="hangmanCanvas"
          ref={canvasRef}
          width={CANVAS_WIDTH}
          height={CANVAS_HEIGHT}
          aria-hidden="true"
        />
        <div
          id="wordClue"
          className={displayed?.clueImageUrl == null ? 'word-clue hidden' : 'word-clue'}
          aria-hidden="true"
        >
          {displayed?.clueImageUrl == null
            ? null
            : <WordImage key={displayed.clueImageUrl} src={displayed.clueImageUrl} />}
        </div>
        <div
          id="wordTiles"
          className={translation === null ? 'word-tiles' : 'word-tiles has-translation'}
          role="img"
          aria-live="polite"
          aria-label={spokenWord + (translation === null ? '' : `. ${t('translate-aria')}`)}
          tabIndex={translation === null ? undefined : 0}
          title={translation === null ? undefined : t('translate-hint')}
          onClick={() => {
            if (translation === null) return;
            setTranslationShown((shown) => !shown);
          }}
          onKeyDown={(event) => {
            if (event.key !== 'Enter' && event.key !== ' ') return;
            if (translation === null) return;
            event.preventDefault();
            setTranslationShown((shown) => !shown);
          }}
        >
          {displayed === null
            ? null
            : displayed.pattern.map((item, index) => {
                if (item.gap) {
                  return <div key={index} className="word-gap" />;
                }
                return (
                  <div
                    key={index}
                    className={item.revealed ? 'word-tile revealed' : 'word-tile'}
                  >
                    {item.revealed ? item.text : ''}
                  </div>
                );
              })}
        </div>
        <div
          id="wordTranslation"
          className={translation !== null && translationShown ? 'word-translation show' : 'word-translation'}
          aria-live="polite"
          lang={translationLanguage}
        >
          {translation ?? ''}
        </div>
      </div>

      <div className="keyboard" role="group" aria-label={t('a11y-keyboard')}>
        {KEYBOARD_ROWS.map((row) => (
          <div key={row} className="key-row">
            {row.split('').map((letter) => {
              const used = displayed !== null && displayed.guessed.includes(letter);
              const hit = used && isCorrectLetter(letter);
              let className = 'key-btn';
              if (used) className += hit ? ' correct' : ' wrong';
              return (
                <button
                  key={letter}
                  type="button"
                  className={className}
                  disabled={used}
                  aria-label={used
                    ? fill(t(hit ? 'a11y-key-hit' : 'a11y-key-miss'), { letter })
                    : `Letter ${letter}`}
                  onClick={() => guess(letter)}
                >
                  {letter}
                </button>
              );
            })}
          </div>
        ))}
      </div>

      <div className="controls-bar">
        <button
          type="button"
          className="ctrl-btn"
          disabled={!playing || displayed === null || displayed.hintsLeft <= 0}
          onClick={requestHint}
        >
          {t('btn-hint')} ({displayed?.hintsLeft ?? 0})
        </button>
        <button
          type="button"
          className="ctrl-btn primary"
          disabled={starting}
          onClick={() => choice !== null && beginRound(choice)}
        >
          {t('btn-new')}
        </button>
      </div>
    </main>
  );

  const overlays = (
    <>
      <div
        className={celebrationOpen ? 'celebration-overlay' : 'celebration-overlay hidden'}
        id="celebrationOverlay"
        role="dialog"
        aria-modal="true"
        aria-labelledby="celebrationOverlayTitle"
      >
        <div className="celebration-card">
          <div className="trophy">
            <img src="/assets/logo/logo_128px.png" alt="Oefenpad" className="trophy-logo" />
          </div>
          <h2 id="celebrationOverlayTitle">{t('cele-title')}</h2>
          <p style={{ color: 'var(--grijs)', fontSize: '14px' }}>{t('cele-msg')}</p>
          <p style={{ color: 'var(--grijs)', fontSize: '14px' }}>{t('lose-msg')}</p>
          <div id="celeImage" className={view?.imageUrl == null ? 'cele-image hidden' : 'cele-image'}>
            {view?.imageUrl == null
              ? null
              : <WordImage key={view.imageUrl} src={view.imageUrl} />}
          </div>
          <p style={POPUP_WORD_STYLE}>{answer}</p>
          <p
            id="celeTranslation"
            className={translation === null ? 'popup-translation' : 'popup-translation show'}
            lang={translationLanguage}
          >
            {translation ?? ''}
          </p>
          <p style={{ color: 'var(--grijs)', fontSize: '14px' }}>
            {t('time-label')} {formatTime(lastWon?.seconds ?? 0)}
          </p>
          <p style={{ color: 'var(--grijs)', fontSize: '14px' }}>
            {t('streak-label')} {lastWon?.streak ?? 0}
          </p>
          <button type="button" style={SECONDARY_BUTTON_STYLE} onClick={() => setCelebrationOpen(false)}>
            {t('btn-close')}
          </button>
          <button
            type="button"
            onClick={() => {
              setCelebrationOpen(false);
              if (choice !== null) void startRound(choice);
            }}
          >
            {t('btn-new')}
          </button>
        </div>
      </div>

      <div
        className={loseOpen ? 'celebration-overlay' : 'celebration-overlay hidden'}
        id="loseOverlay"
        role="dialog"
        aria-modal="true"
        aria-labelledby="loseOverlayTitle"
      >
        <div className="celebration-card">
          <div className="trophy" style={{ fontSize: '48px' }}>💀</div>
          <h2 id="loseOverlayTitle">{t('lose-title')}</h2>
          <p style={{ color: 'var(--grijs)', fontSize: '14px' }}>{t('lose-msg')}</p>
          <div id="loseImage" className={view?.imageUrl == null ? 'cele-image hidden' : 'cele-image'}>
            {view?.imageUrl == null
              ? null
              : <WordImage key={view.imageUrl} src={view.imageUrl} />}
          </div>
          <p style={POPUP_WORD_STYLE}>{answer}</p>
          <p
            id="loseTranslation"
            className={translation === null ? 'popup-translation' : 'popup-translation show'}
            lang={translationLanguage}
          >
            {translation ?? ''}
          </p>
          <button type="button" style={SECONDARY_BUTTON_STYLE} onClick={() => setLoseOpen(false)}>
            {t('btn-close')}
          </button>
          <button
            type="button"
            onClick={() => {
              setLoseOpen(false);
              if (choice !== null) void startRound(choice);
            }}
          >
            {t('btn-new')}
          </button>
        </div>
      </div>

      <Overlay open={settingsOpen} title={t('settings-title')}>
        <div className="settings-row">
          <span className="settings-label">{t('sound-effects')}</span>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={settings.soundEffects}
              onChange={(event) => settingsStore[1]({ ...settings, soundEffects: event.target.checked })}
            />
            <span className="toggle-slider" />
          </label>
        </div>

        <div className="settings-row">
          <span className="settings-label">{t('translate-label')}</span>
          <select
            className="settings-select"
            value={settings.translateTo}
            onChange={(event) => updateTranslateTo(event.target.value)}
          >
            <option value="">{t('translate-off')}</option>
            <option value={TRANSLATE_TO} lang={TRANSLATE_TO}>English</option>
          </select>
        </div>
        <p className="settings-note">{t('translate-hint')}</p>

        <button type="button" className="settings-close-btn" onClick={() => setSettingsOpen(false)}>
          {t('close')}
        </button>
      </Overlay>

      <Overlay open={categoryOpen} title={t('cat-title')}>
        <p style={{ fontSize: '13px', color: 'var(--grijs)', marginBottom: '8px' }}>
          {t('cat-subtitle')}
        </p>
        <div className="category-grid">
          {categories.map((category) => (
            <button
              key={category.id}
              type="button"
              className={displayed?.category.id === category.id ? 'cat-btn active' : 'cat-btn'}
              onClick={() => requestCategory(category.id)}
            >
              <span>{category.icon}</span>
              <span>{category.name}</span>
            </button>
          ))}
          <button type="button" className="cat-btn random-btn" onClick={requestRandomCategory}>
            <span>🎲</span>
            <span>{t('random-cat')}</span>
          </button>
        </div>
        <button
          type="button"
          className="settings-close-btn"
          style={{ marginTop: '10px' }}
          onClick={() => setCategoryOpen(false)}
        >
          {t('close')}
        </button>
      </Overlay>

      <Overlay
        open={pending !== null}
        title={t('confirm-new-title')}
        style={{ maxWidth: '340px', textAlign: 'center' }}
      >
        <p style={{ color: 'var(--grijs)', fontSize: '14px' }}>{t('confirm-new-msg')}</p>
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '14px' }}>
          <button type="button" style={SECONDARY_BUTTON_STYLE} onClick={() => setPending(null)}>
            {t('cancel')}
          </button>
          <button type="button" style={PRIMARY_BUTTON_STYLE} onClick={confirmNewGame}>
            {t('confirm-ok')}
          </button>
        </div>
      </Overlay>

      <div className="confetti-container" id="confettiContainer" ref={confettiRef} />
    </>
  );

  return (
    <GameShell
      game={GAME}
      title={texts['app-title'] ?? 'Galgje'}
      splash={texts['splash-title'] ?? 'Galgje'}
      onSettings={() => setSettingsOpen(true)}
      overlays={overlays}
    >
      {body}
    </GameShell>
  );
}

const POPUP_WORD_STYLE = {
  fontSize: '26px',
  fontWeight: 800,
  letterSpacing: '3px',
  color: 'var(--kobalt)',
  margin: '8px 0 0',
};

const SECONDARY_BUTTON_STYLE = {
  marginRight: '8px',
  background: 'var(--papier)',
  color: 'var(--inkt)',
  boxShadow: 'inset 0 0 0 2px var(--inkt)',
  border: 'none',
  borderRadius: 0,
  padding: '10px 18px',
  cursor: 'pointer',
  fontWeight: 600,
};

const PRIMARY_BUTTON_STYLE = {
  background: 'var(--oranje)',
  color: 'var(--papier)',
  border: 'none',
  borderRadius: 0,
  padding: '10px 18px',
  cursor: 'pointer',
  fontWeight: 600,
};
