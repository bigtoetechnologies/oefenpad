import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { api, ApiError, fill } from '../../api';
import { GameShell } from '../../site/GameShell';
import { Overlay } from '../../shared/Overlay';
import { ResumeNote } from '../../shared/ResumeNote';
import { WordImage } from '../../shared/WordImage';
import { ZoomPop, type ZoomContent, type ZoomPopRef } from '../../shared/ZoomPop';
import { formatTime } from '../../shared/format';
import { sfx } from '../../shared/sound';
import { spawnConfetti, type ConfettiOptions } from '../../shared/confetti';
import { useGameData } from '../../shared/useGameData';
import { useLocalStorage } from '../../shared/useLocalStorage';
import { useTimer } from '../../shared/useTimer';

/* =================================================================
   Koppelen — match each Dutch word to the right picture.

   The server deals the board and keeps the pairing table: a card's
   face arrives only once it is turned, so nothing here can read an
   answer off the page. The class names mirror the old page, which
   matching.css is scoped to.
   ================================================================= */

interface CategoryView {
  id: string;
  name: string;
  icon: string;
}

/* In a text round (a card-family category without pictures) the right-hand
   panel holds English meanings: side 'image', face kind 'meaning', no picture. */
interface CardFace {
  kind: 'word' | 'image' | 'meaning';
  word: string;
  imageUrl: string | null;
}

interface MatchingCard {
  index: number;
  side: 'word' | 'image';
  matched: boolean;
  faceUp: boolean;
  /** Present only while the card is face up or matched. */
  face: CardFace | null;
}

interface MatchingView {
  category: CategoryView;
  /** Dutch word against English meaning; no pictures in this round. */
  text?: boolean;
  pairs: number;
  moves: number;
  pairsLeft: number;
  cards: MatchingCard[];
}

interface MatchingSettings {
  soundEffects: boolean;
  showLabels: boolean;
}

interface MatchingStats {
  gamesWon: number;
  bestTime: number | null;
}

const SETTINGS_KEY = 'oefenpad-koppelen-settings';
const STATS_KEY = 'oefenpad-koppelen-stats';

const DEFAULT_PAIRS = 6;
const MAX_COLUMNS = 3;
const SMALL_TEXT_AT = 9;
/** Past this length a text card (a phrase or an English meaning) drops to its smallest size. */
const LONG_TEXT_AT = 24;
const WRONG_SHAKE_MS = 350;
const DENY_SHAKE_MS = 400;

const CELEBRATION_STYLE = { borderTop: '6px solid var(--kobalt)' };
const CATEGORY_STYLE = { maxWidth: 520 };
const CATEGORY_SUBTITLE_STYLE = { fontSize: 13, color: 'var(--grijs)', marginBottom: 8 };
const CONFIRM_STYLE = { maxWidth: 340, textAlign: 'center' as const };
const CONFIRM_TEXT_STYLE = { color: 'var(--grijs)', fontSize: 14 };
const CONFIRM_BUTTONS_STYLE = { display: 'flex', gap: 10, justifyContent: 'center', marginTop: 14 };

/** The celebration burst — same palette and timing as the old page. */
const CONFETTI: ConfettiOptions = {
  colors: ['#FFB300', '#009688', '#E57373', '#64B5F6', '#81C784', '#BA68C8'],
  count: 80,
  duration: [2, 4],
  delay: [0, 0.6],
  clear: false,
  removeAfter: 4600,
};

export function MatchingGame() {
  const { texts, options, error } = useGameData('matching');

  useEffect(() => {
    if (texts?.['page-title']) document.title = texts['page-title'];
  }, [texts]);

  const [settings, saveSettings] = useLocalStorage<MatchingSettings>(SETTINGS_KEY, {
    soundEffects: true,
    showLabels: false,
  });
  const [, saveStats] = useLocalStorage<MatchingStats>(STATS_KEY, {
    gamesWon: 0,
    bestTime: null,
  });

  const [view, setView] = useState<MatchingView | null>(null);
  const [roundId, setRoundId] = useState<string | null>(null);
  const [category, setCategory] = useState<string | null>(null);
  const [pairs, setPairs] = useState(DEFAULT_PAIRS);
  const [dealing, setDealing] = useState(false);
  const [roundError, setRoundError] = useState<string | null>(null);
  const [resumed, setResumed] = useState<string | null>(null);
  const [firstPick, setFirstPick] = useState<number | null>(null);
  const [locked, setLocked] = useState(false);
  const [wrongPair, setWrongPair] = useState<number[]>([]);
  const [deniedCard, setDeniedCard] = useState<number | null>(null);
  const [celebrating, setCelebrating] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [confirming, setConfirming] = useState(false);

  const zoom = useRef<ZoomPopRef>(null);
  const confetti = useRef<HTMLDivElement>(null);
  const pendingAction = useRef<(() => void) | null>(null);
  const timers = useRef<number[]>([]);
  const timerRunning = useRef(false);

  // `timing` starts the clock and `roundId` puts it back to zero.
  const [timing, setTiming] = useState(false);
  const seconds = useTimer(timing, roundId);

  const t = useCallback(
    (key: string) => fill(texts?.[key] ?? key),
    [texts],
  );

  const later = useCallback((action: () => void, ms: number) => {
    timers.current.push(window.setTimeout(action, ms));
  }, []);

  useEffect(() => () => {
    timers.current.forEach((id) => window.clearTimeout(id));
    timers.current = [];
  }, []);

  const categories = options?.categories ?? [];
  const levels = options?.levels ?? [];

  const stopClock = useCallback(() => {
    timerRunning.current = false;
    setTiming(false);
  }, []);

  /* The view alone cannot say whose turn it is: after a miss the server leaves
     both cards of the pair face up until the next flip closes them, so reading
     the first face-up card would make one of those two the turn's first pick
     and the same-side guard would then refuse half the board. Every caller that
     knows the turn state passes it; only a redraw falls back to the view. */
  const applyView = useCallback((next: MatchingView, pick?: number | null) => {
    setView(next);
    if (pick !== undefined) {
      setFirstPick(pick);
      return;
    }
    const open = next.cards.find((card) => card.faceUp && !card.matched);
    setFirstPick(open ? open.index : null);
  }, []);

  /* ---------- rounds ---------- */

  const deal = useCallback(
    async (wantedCategory: string | null, wantedPairs: number) => {
      setDealing(true);
      setRoundError(null);
      setResumed(null);
      setLocked(false);
      setWrongPair([]);
      setDeniedCard(null);
      setFirstPick(null);
      setCelebrating(false);
      zoom.current?.reset();
      stopClock();

      try {
        const round = await api.start<MatchingView>('matching', {
          ...(wantedCategory === null ? {} : { category: wantedCategory }),
          pairs: wantedPairs,
        });
        setRoundId(round.roundId);
        applyView(round.view);
      } catch (cause) {
        setRoundId(null);
        setView(null);
        setRoundError(cause instanceof ApiError ? cause.message : t('error'));
      } finally {
        setDealing(false);
      }
    },
    [applyView, stopClock, t],
  );

  // The first round waits for the options: it opens on the default
  // category and deals exactly once.
  const started = useRef(false);
  useEffect(() => {
    if (started.current || !options) return;
    started.current = true;

    void (async () => {
      const saved = await api.saved<MatchingView>('matching').catch(() => null);
      if (saved !== null) {
        setRoundId(saved.roundId);
        setCategory(saved.view.category.id);
        setPairs(saved.view.pairs);
        applyView(saved.view);
        setResumed(t('resumed'));
        return;
      }

      const entry = options.categories.find((item) => item.count >= DEFAULT_PAIRS)
        ?? options.categories[0];
      if (!entry) return;
      setCategory(entry.id);
      void deal(entry.id, DEFAULT_PAIRS);
    })();
  }, [options, deal, applyView, t]);

  /* ---------- one turn ---------- */

  const finishTurn = useCallback(() => {
    setWrongPair([]);
    setLocked(false);
  }, []);

  const winGame = useCallback(
    () => {
      stopClock();
      saveStats((current) => ({
        gamesWon: current.gamesWon + 1,
        bestTime: current.bestTime === null ? seconds : Math.min(current.bestTime, seconds),
      }));
      setCelebrating(true);
      sfx.fanfare(settings.soundEffects);
      spawnConfetti(confetti.current, CONFETTI);
    },
    [stopClock, saveStats, seconds, settings.soundEffects],
  );

  const flip = useCallback(
    async (card: MatchingCard) => {
      if (!roundId || !view || locked || dealing) return;
      if (card.matched) return;

      const faceUp = card.matched || card.faceUp;

      // A face-up card shows itself large instead of turning again.
      if (faceUp) {
        zoom.current?.open(zoomOf(view, card.index, settings.showLabels));
        return;
      }

      // The two open cards must come from opposite panels; a second card
      // from the same panel is refused with a shake and is not a move.
      if (firstPick !== null) {
        const first = view.cards.find((candidate) => candidate.index === firstPick);
        if (first && first.side === card.side) {
          sfx.wrong(settings.soundEffects);
          setDeniedCard(card.index);
          later(() => setDeniedCard(null), DENY_SHAKE_MS);
          return;
        }
      }

      if (!timerRunning.current) {
        timerRunning.current = true;
        setTiming(true);
      }
      sfx.flip(settings.soundEffects);
      setLocked(true);

      const opened = [firstPick, card.index].filter((index): index is number => index !== null);

      let result;
      try {
        result = await api.move<MatchingView>('matching', roundId, {
          action: 'flip',
          index: card.index,
        });
      } catch (cause) {
        setLocked(false);
        if (cause instanceof ApiError) {
          setRoundError(cause.message);
          if (cause.status === 410) stopClock();
        }
        return;
      }

      if (result.rejection !== null) {
        // sameSide / alreadyOpen: no move counted, no dialog, just redraw.
        setLocked(false);
        applyView(result.view);
        return;
      }

      const next = result.view;
      const won = result.done && next.pairsLeft === 0;

      if (result.correct === true) {
        applyView(next, null);
        sfx.correct(settings.soundEffects);
        zoom.current?.auto(zoomOf(next, card.index, settings.showLabels), () => {
          finishTurn();
          if (won) winGame();
        });
        return;
      }

      if (result.correct === false) {
        // Shake both cards, then let the server's view turn them back and
        // finish the turn after the second card has been popped.
        setWrongPair(opened);
        sfx.wrong(settings.soundEffects);
        later(() => {
          applyView(next, null);
          zoom.current?.auto(zoomOf(next, card.index, settings.showLabels), finishTurn);
        }, WRONG_SHAKE_MS);
        return;
      }

      // First card of the turn: it stays open; keep the board locked until
      // its pop has finished so a second pick cannot race it.
      applyView(next, card.index);
      zoom.current?.auto(zoomOf(next, card.index, settings.showLabels), () => setLocked(false));
    },
    [
      roundId,
      view,
      locked,
      dealing,
      firstPick,
      settings.soundEffects,
      settings.showLabels,
      later,
      applyView,
      finishTurn,
      winGame,
      stopClock,
    ],
  );

  /* ---------- asking before a board is thrown away ---------- */

  const inProgress =
    view !== null &&
    !dealing &&
    !celebrating &&
    view.pairsLeft > 0 &&
    (view.moves > 0 || firstPick !== null);

  const ask = useCallback(
    (action: () => void) => {
      if (inProgress) {
        pendingAction.current = action;
        setConfirming(true);
      } else {
        action();
      }
    },
    [inProgress],
  );

  const answerConfirm = (take: boolean) => {
    const action = pendingAction.current;
    pendingAction.current = null;
    setConfirming(false);
    if (take) action?.();
  };

  const chooseLevel = (size: number) => {
    if (size === pairs) return;
    ask(() => {
      setPairs(size);
      void deal(category, size);
    });
  };

  const chooseCategory = (id: string) => {
    setCategoryOpen(false);
    ask(() => {
      setCategory(id);
      void deal(id, pairs);
    });
  };

  const chooseRandomCategory = () => {
    setCategoryOpen(false);
    if (categories.length === 0) return;
    const next = categories[Math.floor(Math.random() * categories.length)].id;
    ask(() => {
      setCategory(next);
      void deal(next, pairs);
    });
  };

  const newGame = () => ask(() => void deal(category, pairs));

  /* ---------- panel layout ---------- */

  const panels = useMemo(() => {
    const cards = view?.cards ?? [];
    // Capped at three columns so the cards stay large: extra pairs add rows.
    const columns = Math.min(MAX_COLUMNS, Math.max(2, Math.ceil(cards.length / 4)));
    return {
      words: cards.filter((card) => card.side === 'word'),
      pictures: cards.filter((card) => card.side === 'image'),
      style: { gridTemplateColumns: `repeat(${columns}, 1fr)` },
    };
  }, [view]);

  const shownCategory = view?.category
    ?? categories.find((entry) => entry.id === category)
    ?? null;
  const moves = view?.moves ?? 0;
  const pairsLeft = view?.pairsLeft ?? pairs;

  const renderCard = (card: MatchingCard, position: number) => {
    const faceUp = card.matched || card.faceUp;
    const className = [
      'match-card',
      faceUp ? 'flipped' : '',
      card.matched ? 'matched' : '',
      wrongPair.includes(card.index) ? 'wrong' : '',
      deniedCard === card.index ? 'deny' : '',
    ].filter(Boolean).join(' ');

    const word = card.face?.word ?? '';
    let label: string;
    if (!faceUp) {
      label = t('a11y-card-down');
    } else if (card.matched) {
      label = fill(t('a11y-card-matched'), { what: word });
    } else {
      label = fill(t('a11y-card-up'), { what: word });
    }

    return (
      <button
        key={card.index}
        type="button"
        className={className}
        aria-label={fill(label, { i: position })}
        onClick={() => void flip(card)}
      >
        <div className="card-inner">
          <div className="card-back" />
          {faceUp ? (
            <div
              className={[
                'card-face',
                word.length > SMALL_TEXT_AT ? 'small-text' : '',
                card.face?.kind === 'meaning' ? 'meaning-text' : '',
                word.length > LONG_TEXT_AT ? 'long-text' : '',
              ].filter(Boolean).join(' ')}
              aria-hidden="true"
            >
              {card.side === 'image' && card.face?.imageUrl
                ? <WordImage src={card.face.imageUrl} />
                : word}
            </div>
          ) : (
            <div className="card-face" aria-hidden="true" />
          )}
        </div>
      </button>
    );
  };

  /* ---------- render ---------- */

  if (error) {
    return (
      <GameShell game="matching" title="Koppelen">
        <main className="app-container">
          <p className="hint" role="alert">{error}</p>
        </main>
      </GameShell>
    );
  }

  if (!texts || !options) {
    return (
      <GameShell game="matching" title="Koppelen">
        <main className="app-container">
          <p className="hint">Even laden…</p>
        </main>
      </GameShell>
    );
  }

  const overlays = (
    <>
      <Overlay
        open={celebrating}
        className="celebration-card"
        title={t('cele-title')}
        style={CELEBRATION_STYLE}
      >
        <div className="trophy">
          <img src="/assets/logo/logo_128px.png" alt="Oefenpad" className="trophy-logo" />
        </div>
        <p style={CONFIRM_TEXT_STYLE}>{t(view?.text ? 'cele-msg-text' : 'cele-msg')}</p>
        <div className="stats-row">
          <div className="stat">
            <div className="val">{moves}</div>
            <div className="lbl">{t('moves-label')}</div>
          </div>
          <div className="stat">
            <div className="val">{formatTime(seconds)}</div>
            <div className="lbl">{t('time-label')}</div>
          </div>
        </div>
        <button type="button" className="ctrl-btn" onClick={() => setCelebrating(false)}>
          {t('btn-close')}
        </button>
        <button type="button" className="ctrl-btn primary" onClick={newGame}>
          {t('btn-new')}
        </button>
      </Overlay>
      <div className={`confetti-container${celebrating ? '' : ' hidden'}`} ref={confetti} />

      <Overlay open={settingsOpen} title={t('settings-title')}>
        <div className="settings-row">
          <span className="settings-label">{t('sound-effects')}</span>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={settings.soundEffects}
              onChange={(event) => saveSettings({ ...settings, soundEffects: event.target.checked })}
            />
            <span className="toggle-slider" />
          </label>
        </div>
        <div className="settings-row">
          <span className="settings-label">{t('show-labels')}</span>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={settings.showLabels}
              onChange={(event) => saveSettings({ ...settings, showLabels: event.target.checked })}
            />
            <span className="toggle-slider" />
          </label>
        </div>
        <button type="button" className="settings-close-btn" onClick={() => setSettingsOpen(false)}>
          {t('close')}
        </button>
      </Overlay>

      <Overlay open={categoryOpen} title={t('cat-title')} style={CATEGORY_STYLE}>
        <p style={CATEGORY_SUBTITLE_STYLE}>{t('cat-subtitle')}</p>
        <div className="category-grid">
          {categories.map((entry) => (
            <button
              key={entry.id}
              type="button"
              className={`cat-btn${entry.id === category ? ' active' : ''}`}
              aria-pressed={entry.id === category}
              onClick={() => chooseCategory(entry.id)}
            >
              <span>{entry.icon}</span>
              <span>{entry.name}</span>
            </button>
          ))}
          <button type="button" className="cat-btn random-btn" onClick={chooseRandomCategory}>
            <span>🎲</span>
            <span>{t('random-cat')}</span>
          </button>
        </div>
        <button
          type="button"
          className="settings-close-btn"
          style={{ marginTop: 10 }}
          onClick={() => setCategoryOpen(false)}
        >
          {t('close')}
        </button>
      </Overlay>

      <Overlay open={confirming} title={t('confirm-new-title')} style={CONFIRM_STYLE}>
        <p style={CONFIRM_TEXT_STYLE}>{t('confirm-new-msg')}</p>
        <div style={CONFIRM_BUTTONS_STYLE}>
          <button type="button" className="ctrl-btn" onClick={() => answerConfirm(false)}>
            {t('cancel')}
          </button>
          <button type="button" className="ctrl-btn primary" onClick={() => answerConfirm(true)}>
            {t('confirm-ok')}
          </button>
        </div>
      </Overlay>

      <ZoomPop ref={zoom} />
    </>
  );

  return (
    <GameShell
      game="matching"
      title={t('app-title')}
      splash={t('splash-title')}
      onSettings={() => setSettingsOpen(true)}
      overlays={overlays}
    >
      <main className="app-container">
        <div className="difficulty-bar" role="group" aria-label="Niveau">
          {levels.map((level) => {
            const size = level.size ?? Number(level.id);
            return (
              <button
                key={level.id}
                type="button"
                className={`diff-btn${size === pairs ? ' active' : ''}`}
                aria-pressed={size === pairs}
                disabled={!canFill(categories, category, size)}
                onClick={() => chooseLevel(size)}
              >
                {level.name}
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
            <span>{shownCategory?.icon ?? ''}</span>
            <span>{shownCategory?.name ?? ''}</span>
            <span aria-hidden="true">▾</span>
          </button>
          <span className="status-item">{fill(t('pairs-left'), { n: pairsLeft })}</span>
          <span className="status-item">{`🎯 ${moves}`}</span>
          <span className="status-item">{`⏱ ${formatTime(seconds)}`}</span>
        </div>

        <p className="hint">{t(view?.text ? 'hint-text' : 'hint')}</p>

        {roundError === null ? null : (
          <p className="hint" role="alert">
            {roundError}{' '}
            <button type="button" className="status-chip" onClick={newGame}>
              {t('btn-new')}
            </button>
          </p>
        )}

        <ResumeNote text={resumed} onDone={() => setResumed(null)} />

        <div className="match-layout">
          <div className="match-panel words-panel" style={panels.style}>
            {panels.words.map((card, position) => renderCard(card, position + 1))}
          </div>
          <div className="match-panel pics-panel" style={panels.style}>
            {panels.pictures.map((card, position) => renderCard(card, position + 1))}
          </div>
        </div>

        <div className="controls-bar">
          <button type="button" className="ctrl-btn primary" onClick={newGame} disabled={dealing}>
            {t('btn-new')}
          </button>
        </div>
      </main>
    </GameShell>
  );
}

/* ---------- helpers ---------- */

/** Whether the chosen category holds enough pairs for a level. */
function canFill(
  categories: { id: string; count: number }[],
  category: string | null,
  pairs: number,
): boolean {
  const entry = categories.find((candidate) => candidate.id === category);
  return entry !== undefined && entry.count >= pairs;
}

/** What the card shows in the enlarged pop. */
function zoomOf(view: MatchingView, index: number, showLabels: boolean): ZoomContent {
  const face = view.cards.find((card) => card.index === index)?.face;
  if (!face) return { text: '' };
  const word = showLabels ? face.word : undefined;
  if (face.kind === 'image' && face.imageUrl) return { image: face.imageUrl, word };
  return { text: face.word };
}
