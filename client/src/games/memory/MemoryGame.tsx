import { useCallback, useEffect, useReducer, useRef, useState } from 'react';
import { api, ApiError } from '../../api';
import { Overlay } from '../../shared/Overlay';
import { ResumeNote } from '../../shared/ResumeNote';
import { WordImage } from '../../shared/WordImage';
import {
  ZoomPop,
  type ZoomContent,
  type ZoomPopRef,
} from '../../shared/ZoomPop';
import { formatTime } from '../../shared/format';
import { sfx } from '../../shared/sound';
import { spawnConfetti } from '../../shared/confetti';
import { useGameData } from '../../shared/useGameData';
import { useLocalStorage } from '../../shared/useLocalStorage';
import { useTimer } from '../../shared/useTimer';
import { GameShell } from '../../site/GameShell';

/* The round as the server renders it. A card the player has not turned
   carries no face: the deck itself stays on the server. */
interface CardFace {
  kind: 'word' | 'image';
  word?: string;
  imageUrl?: string;
}

interface MemoryCard {
  index: number;
  matched: boolean;
  faceUp: boolean;
  face: CardFace | null;
}

interface MemoryCategory {
  id: string;
  name: string;
  icon: string;
}

interface MemoryView {
  category: MemoryCategory;
  level: string;
  gridSize: number;
  pairs: number;
  moves: number;
  pairsFound: number;
  cards: MemoryCard[];
}

interface MoveResponse {
  view: MemoryView;
  done: boolean;
  correct: boolean | null;
  rejection: string | null;
}

interface MemorySettings {
  soundEffects: boolean;
  showLabels: boolean;
}

/** Best result per board, keyed "6x6": the shape the old page wrote. */
type BestScores = Record<string, { moves: number; seconds: number }>;

const SETTINGS_KEY = 'oefenpad-geheugen-settings';
const BEST_KEY = 'oefenpad-geheugen-best';

const DEFAULT_SETTINGS: MemorySettings = { soundEffects: true, showLabels: true };
const DEFAULT_LEVEL = '6';

const CONFETTI_COLORS = ['#FFB300', '#009688', '#E57373', '#64B5F6', '#81C784', '#BA68C8'];

/** How long a missed pair shakes before the board carries on. */
const MISS_MS = 350;

function pairCount(level: string): number {
  const size = Number(level);
  return Number.isFinite(size) ? (size * size) / 2 : 0;
}

/** A level or category has room when it offers enough pictures for the pairs. */
function hasRoom(available: number | null, needed: number): boolean {
  return available === null || available >= needed;
}

function boardKey(view: MemoryView | null, level: string): string {
  const id = view?.level ?? level;
  return `${id}x${id}`;
}

/**
 * The server's view as the board should show it: a card whose turn is still
 * being played out stays face down — its picture is popping up in the middle
 * — and a card that was already up keeps the face it had, since it did not
 * turn again with this move.
 */
function peel(view: MemoryView, keepBack: ReadonlySet<number>, base: MemoryView = view): MemoryView {
  const back = (index: number) => keepBack.has(index) && !base.cards[index]?.matched;
  return view.cards.every((card) => !back(card.index) || (!card.faceUp && card.face === null))
    ? view
    : {
      ...view,
      cards: view.cards.map((card) => (back(card.index) ? base.cards[card.index] : card)),
    };
}

function zoomContent(card: MemoryCard, showLabels: boolean): ZoomContent {
  const face = card.face;
  if (face === null) return { text: '' };
  if (face.kind === 'word') return { text: face.word ?? '' };
  return {
    image: face.imageUrl ?? undefined,
    word: showLabels ? face.word ?? undefined : undefined,
  };
}

export function MemoryGame() {
  const { texts, options, error: dataError } = useGameData('memory');

  const [view, setView] = useState<MemoryView | null>(null);
  const [roundId, setRoundId] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState(DEFAULT_LEVEL);
  const [categoryId, setCategoryId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [roundError, setRoundError] = useState<string | null>(null);
  const [resumed, setResumed] = useState<string | null>(null);
  /** Cards of a missed pair, shaking while the board shows the miss. */
  const [missed, setMissed] = useState<number[]>([]);
  /** Cards of a miss that has been shown; the server keeps them up, the board does not. */
  const [hidden, setHidden] = useState<number[]>([]);
  const hiddenRef = useRef<number[]>([]);
  // pendingFirst is a ref, so the board needs a nudge once it clears.
  const [, bump] = useReducer((value: number) => value + 1, 0);

  const [showSettings, setShowSettings] = useState(false);
  const [showCategories, setShowCategories] = useState(false);
  /** The board the player is waiting to deal, once they confirm the restart. */
  const [pendingDeal, setPendingDeal] = useState<{ level: string; category: string } | null>(null);
  const showConfirm = pendingDeal !== null;
  const [showCelebration, setShowCelebration] = useState(false);

  const [settings, setSettings] = useLocalStorage<MemorySettings>(SETTINGS_KEY, DEFAULT_SETTINGS);
  const [best, setBest] = useLocalStorage<BestScores>(BEST_KEY, {});

  const zoom = useRef<ZoomPopRef>(null);
  const confettiContainer = useRef<HTMLDivElement>(null);
  /** True while a turn is being resolved; further taps are ignored. */
  const locked = useRef(false);
  /**
   * The card popping up in the middle, and the view before it was turned.
   * The board keeps that card down until the pop has finished.
   */
  const pendingFirst = useRef<{ index: number; previous: MemoryView } | null>(null);
  /** The first card of the current turn, kept until the turn resolves. */
  const turnFirst = useRef<{ index: number; previous: MemoryView } | null>(null);

  const won = view !== null && view.pairsFound >= view.pairs;
  const seconds = useTimer(view !== null && view.moves > 0 && !won, roundId);
  /** A deal counts as under way from the first card turned, as on the old page. */
  const inProgress = pendingFirst.current !== null
    || (view !== null && (view.moves > 0 || view.pairsFound > 0 || view.cards.some((card) => card.faceUp)));

  // Kept in refs so the turn and the overlays read the latest values
  // without being rebuilt every render.
  const settingsRef = useRef(settings);
  settingsRef.current = settings;
  const roundIdRef = useRef(roundId);
  roundIdRef.current = roundId;
  const inProgressRef = useRef(inProgress);
  inProgressRef.current = inProgress;
  const viewRef = useRef<MemoryView | null>(view);
  viewRef.current = view;
  /** The board on the table: level id and category id. */
  const choice = useRef({ level: DEFAULT_LEVEL, category: '' });

  const text = (key: string, fallback: string): string => texts?.[key] ?? fallback;

  useEffect(() => {
    document.title = text('page-title', 'Geheugen — Oefenpad');
    // text() reads `texts`; rerun once the strings arrive.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [texts]);

  /* ---------- rounds ---------- */

  const startRound = useCallback(async (nextLevel: string, nextCategory: string) => {
    choice.current = { level: nextLevel, category: nextCategory };
    locked.current = true;
    pendingFirst.current = null;
    turnFirst.current = null;
    setLoading(true);
    setRoundError(null);
    setResumed(null);
    setShowCelebration(false);
    setPendingDeal(null);
    setMissed([]);
    hiddenRef.current = [];
    setHidden([]);
    zoom.current?.reset();

    try {
      const round = await api.start<MemoryView>('memory', {
        category: nextCategory === '' ? 'all' : nextCategory,
        level: nextLevel,
      });
      setRoundId(round.roundId);
      viewRef.current = round.view;
      setView(round.view);
      setSelectedLevel(round.view.level);
      setCategoryId(round.view.category.id);
    } catch (cause) {
      setRoundId(null);
      viewRef.current = null;
      setView(null);
      setRoundError(cause instanceof ApiError ? cause.message : 'De oefening is even niet bereikbaar.');
    } finally {
      setLoading(false);
      locked.current = false;
    }
  }, []);

  // One start, after the categories arrive. The default category is the
  // first with enough pictures for the default board, else the first one.
  const categories = options?.categories;
  const started = useRef(false);
  useEffect(() => {
    if (categories === undefined || started.current) return;
    started.current = true;

    void (async () => {
      const saved = await api.saved<MemoryView>('memory').catch(() => null);
      if (saved !== null) {
        choice.current = { level: saved.view.level, category: saved.view.category.id };
        setRoundId(saved.roundId);
        viewRef.current = saved.view;
        setView(saved.view);
        setSelectedLevel(saved.view.level);
        setCategoryId(saved.view.category.id);
        setLoading(false);
        setResumed(text('resumed', 'We gaan verder waar je gebleven was.'));
        return;
      }

      const roomy = categories.find((category) => hasRoom(category.count, pairCount(DEFAULT_LEVEL)));
      void startRound(DEFAULT_LEVEL, (roomy ?? categories[0])?.id ?? '');
    })();
  }, [categories, startRound]);

  const postMove = useCallback(async (body: Record<string, unknown>): Promise<MoveResponse | null> => {
    const id = roundIdRef.current;
    if (id === null) return null;
    try {
      return await api.move<MemoryView>('memory', id, body);
    } catch (cause) {
      setRoundId(null);
      viewRef.current = null;
      setView(null);
      setShowCelebration(false);
      setRoundError(cause instanceof ApiError ? cause.message : 'De oefening is even niet bereikbaar.');
      return null;
    }
  }, []);

  function celebrate(finalView: MemoryView, elapsed: number) {
    const key = boardKey(finalView, finalView.level);
    setBest((current) => {
      const previous = current[key];
      const better = previous === undefined
        || finalView.moves < previous.moves
        || (finalView.moves === previous.moves && elapsed < previous.seconds);
      return better ? { ...current, [key]: { moves: finalView.moves, seconds: elapsed } } : current;
    });

    setShowCelebration(true);
    spawnConfetti(confettiContainer.current, {
      colors: CONFETTI_COLORS,
      count: 80,
      duration: [2, 4],
      delay: [0, 0.6],
      clear: false,
      removeAfter: 4600,
    });
    sfx.fanfare(settingsRef.current.soundEffects);
  }

  /**
   * One turn. The server adds the turned card to the cards that are up and
   * resolves the pair when there are two. The board never shows the card
   * until the turn is over: it pops up in the middle instead.
   */
  async function flipCard(card: MemoryCard) {
    // The view a tap acts on: the one the server sent last. A rerender may not
    // have landed yet, and a card already showing must grow, not turn again.
    const current = viewRef.current;
    const raw = current?.cards[card.index] ?? card;
    // A missed pair was turned back on screen without telling the round.
    const target = hiddenRef.current.includes(raw.index)
      ? { ...raw, faceUp: false, face: null }
      : raw;
    if (current === null || roundIdRef.current === null || locked.current) return;

    // A card that is already showing grows instead of turning again.
    if (target.matched || target.faceUp) {
      zoom.current?.open(zoomContent(target, settingsRef.current.showLabels));
      return;
    }

    locked.current = true;
    // The mask hides a missed pair the round still holds face up. Drop it for the
    // new turn, but keep it so a move that never lands can put it back: without
    // that, a failed or refused flip snaps both missed cards face up again.
    const wasHidden = hiddenRef.current;
    hiddenRef.current = [];
    setHidden([]);
    sfx.flip(settingsRef.current.soundEffects);

    const first = turnFirst.current;
    const result = await postMove({ action: 'flip', index: target.index });
    if (result === null) {
      pendingFirst.current = null;
      hiddenRef.current = wasHidden;
      setHidden(wasHidden);
      locked.current = false;
      return;
    }
    if (result.rejection !== null) {
      hiddenRef.current = wasHidden;
      setHidden(wasHidden);
      locked.current = false;
      return;
    }

    const { correct, done } = result;
    viewRef.current = result.view;
    setView(result.view);

    // The first card of a turn opens it; the second one ends it.
    if (correct === null) turnFirst.current = { index: target.index, previous: current };
    pendingFirst.current = { index: target.index, previous: current };
    if (correct === false && first !== null) {
      // A miss leaves its pair up until the next card is turned: the board
      // shows the old view while the pop runs, then the server's one.
      pendingFirst.current = { index: first.index, previous: first.previous };
    }

    const turned = result.view.cards[target.index] ?? target;
    const miss = correct === false && first !== null;

    const finish = () => {
      locked.current = false;
      pendingFirst.current = null;
      // A turn is two cards: keep the first card's record until the pair
      // has been judged, not just until its own pop has finished.
      if (correct !== null) turnFirst.current = null;
      // The board moves to the server's view only now, after the pop: until
      // then the card of this turn stays down. pendingFirst is a ref, so ask
      // for a render explicitly.
      bump();
      if (done) celebrate(result.view, seconds);
    };

    zoom.current?.auto(zoomContent(turned, settingsRef.current.showLabels), () => {
      if (miss) {
        // Both cards of the miss shake, then turn back together.
        setMissed([first.index, target.index]);
        sfx.wrong(settingsRef.current.soundEffects);
        window.setTimeout(() => {
          setMissed([]);
          // The server keeps a miss face up until the next turn; the old
          // board turned it back down, so mask those two cards here.
          hiddenRef.current = [first.index, target.index];
          setHidden(hiddenRef.current);
          finish();
        }, MISS_MS);
        return;
      }
      if (correct === true) sfx.correct(settingsRef.current.soundEffects);
      finish();
    });
  }

  /* ---------- controls ---------- */

  /** Deals a board now, or asks first while a deal is under way, as the old page did. */
  const requestDeal = useCallback((level: string, category: string) => {
    setShowCelebration(false);
    if (inProgressRef.current) {
      setPendingDeal({ level, category });
      return;
    }
    void startRound(level, category);
  }, [startRound]);

  function requestNewGame() {
    requestDeal(choice.current.level, choice.current.category);
  }

  /** From the celebration card the finished board does not need confirming. */
  function newGameAfterWin() {
    setShowCelebration(false);
    void startRound(choice.current.level, choice.current.category);
  }

  const chooseCategory = useCallback((id: string) => {
    setShowCategories(false);
    if (id === choice.current.category) return;
    requestDeal(choice.current.level, id);
  }, [requestDeal]);

  const chooseLevel = useCallback((id: string) => {
    if (id === choice.current.level) return;
    requestDeal(id, choice.current.category);
  }, [requestDeal]);

  /* ---------- render ---------- */

  if (dataError !== null) {
    return <p className="hint">{dataError}</p>;
  }
  if (texts === null || options === null) {
    return <p className="hint">Even laden…</p>;
  }

  const pairsNeeded = pairCount(selectedLevel);
  /** Pictures the chosen category offers, or null while it is unknown. */
  const picturesAvailable = view !== null
    ? options.categories.find((category) => category.id === view.category.id)?.count ?? null
    : null;
  const bestScore = best[boardKey(view, selectedLevel)];

  // The server's account of the deal, with the card that is popping up in the
  // middle kept down. A missed pair has just been turned back by hidden, so
  // the board matches the old page even though the round still has it up.
  const serverShown = view === null
    ? null
    : pendingFirst.current === null
      ? view
      : peel(view, new Set([pendingFirst.current.index]), pendingFirst.current.previous);

  const shown = serverShown === null || hidden.length === 0
    ? serverShown
    : {
        ...serverShown,
        cards: serverShown.cards.map((card) =>
          hidden.includes(card.index)
            ? { ...card, faceUp: false, face: null }
            : card),
      };
  const shownCard = (index: number): MemoryCard =>
    shown?.cards[index] ?? { index, matched: false, faceUp: false, face: null };

  const body = (
    <div className="app-container">
      <div className="difficulty-bar" role="group" aria-label="Niveau">
        {options.levels.map((entry) => (
          <button
            key={entry.id}
            type="button"
            className={`diff-btn${entry.id === selectedLevel ? ' active' : ''}`}
            aria-pressed={entry.id === selectedLevel}
            disabled={!hasRoom(picturesAvailable, pairCount(entry.id))}
            onClick={() => chooseLevel(entry.id)}
          >
            {entry.name}
          </button>
        ))}
      </div>

      <div className="status-row" aria-live="polite" aria-atomic="false">
        <button
          type="button"
          className="status-chip"
          onClick={() => setShowCategories(true)}
          title={texts['cat-title']}
        >
          <span>{view?.category.icon ?? '🖼️'}</span>
          <span>{view?.category.name ?? texts['cat-all']}</span> ▾
        </button>
        <span>{texts['moves-label']}</span> <span>{view?.moves ?? 0}</span>
        <span>{texts['pairs-label']}</span> <span>{view?.pairsFound ?? 0}/{view?.pairs ?? pairsNeeded}</span>
        <span>{texts['time-label']}</span> <span>{formatTime(seconds)}</span>
        <span>{texts['best-label']}</span> <span>{bestScore === undefined ? '—' : `${bestScore.moves} 🎯`}</span>
      </div>

      {roundError !== null && (
        <div className="hint" role="alert">
          {roundError}{' '}
          <button
            type="button"
            className="ctrl-btn"
            onClick={() => void startRound(choice.current.level, choice.current.category)}
          >
            {texts['btn-new']}
          </button>
        </div>
      )}

      <ResumeNote text={resumed} onDone={() => setResumed(null)} />

      {shown === null ? (
        loading && <p className="hint">Even laden…</p>
      ) : (
        <div className="memory-grid" style={{ gridTemplateColumns: `repeat(${shown.gridSize}, 1fr)` }}>
          {Array.from({ length: shown.gridSize * shown.gridSize }, (_unused, index) => {
            const card = shownCard(index);
            const faceUp = card.matched || card.faceUp;
            const word = card.face?.word ?? '';
            const label = !faceUp
              ? `Kaart ${card.index + 1}, dicht`
              : card.matched
                ? `Kaart ${card.index + 1}, ${word}, gevonden`
                : `Kaart ${card.index + 1}, ${word}`;
            const classes = [
              'card',
              faceUp ? 'flipped' : '',
              card.matched ? 'matched' : '',
              missed.includes(card.index) ? 'wrong' : '',
            ].filter(Boolean).join(' ');

            return (
              <button
                key={`${roundId}:${card.index}`}
                type="button"
                className={classes}
                data-index={card.index}
                aria-label={label}
                onClick={() => void flipCard(card)}
              >
                <div className="card-inner">
                  <div className="card-back" />
                  <div className="card-face" aria-hidden={!faceUp}>
                    {!faceUp || card.face === null ? null
                      : card.face.kind === 'word'
                        ? <span className="card-word">{card.face.word}</span>
                        : <WordImage src={card.face.imageUrl ?? ''} />}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      )}

      <div className="controls-bar">
        <button type="button" className="ctrl-btn primary" onClick={requestNewGame}>
          {texts['btn-new']}
        </button>
      </div>
    </div>
  );

  const overlays = (
    <>
      <div
        className={`celebration-overlay${showCelebration ? '' : ' hidden'}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="memory-celebration-title"
      >
        <div ref={confettiContainer} className="confetti-container" />
        <div className="celebration-card">
          <div className="trophy">
            <img src="/assets/logo/logo_128px.png" alt="Oefenpad" className="trophy-logo" />
          </div>
          <h2 id="memory-celebration-title">{texts['cele-title']}</h2>
          <p style={{ color: 'var(--grijs)', fontSize: 14 }}>{texts['cele-msg']}</p>
          <div className="stats-row">
            <div className="stat">
              <div className="val">{view?.moves ?? 0}</div>
              <div className="lbl">{texts['moves-label']}</div>
            </div>
            <div className="stat">
              <div className="val">{formatTime(seconds)}</div>
              <div className="lbl">{texts['time-label']}</div>
            </div>
          </div>
          <button
            type="button"
            style={{ marginRight: 8, background: 'var(--raster-zacht)', color: 'var(--inkt)' }}
            onClick={() => setShowCelebration(false)}
          >
            {texts['btn-close']}
          </button>
          <button type="button" onClick={newGameAfterWin}>
            {texts['btn-new']}
          </button>
        </div>
      </div>

      <Overlay open={showSettings} title={texts['settings-title']}>
        <div className="settings-row">
          <span className="settings-label">{texts['sound-effects']}</span>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={settings.soundEffects}
              onChange={(event) => setSettings({ ...settings, soundEffects: event.target.checked })}
            />
            <span className="toggle-slider" />
          </label>
        </div>
        <div className="settings-row">
          <span className="settings-label">{texts['show-labels']}</span>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={settings.showLabels}
              onChange={(event) => setSettings({ ...settings, showLabels: event.target.checked })}
            />
            <span className="toggle-slider" />
          </label>
        </div>
        <button type="button" className="settings-close-btn" onClick={() => setShowSettings(false)}>
          {texts['close']}
        </button>
      </Overlay>

      <Overlay open={showCategories} title={texts['cat-title']} style={{ maxWidth: 520 }}>
        <p style={{ fontSize: 13, color: 'var(--grijs)', marginBottom: 8 }}>{texts['cat-subtitle']}</p>
        <div className="category-grid">
          {options.categories.map((category) => {
            const enough = hasRoom(category.count, pairsNeeded);
            return (
              <button
                key={category.id}
                type="button"
                className={`cat-btn${category.id === categoryId ? ' active' : ''}`}
                disabled={!enough}
                onClick={() => chooseCategory(category.id)}
              >
                <span>{category.icon}</span>
                <span>{enough ? category.name : `${category.name} (${category.count})`}</span>
              </button>
            );
          })}
        </div>
        <button
          type="button"
          className="settings-close-btn"
          style={{ marginTop: 10 }}
          onClick={() => setShowCategories(false)}
        >
          {texts['close']}
        </button>
      </Overlay>

      <Overlay open={showConfirm} style={{ maxWidth: 340, textAlign: 'center' }}>
        <h2>{texts['confirm-new-title']}</h2>
        <p style={{ color: 'var(--grijs)', fontSize: 14 }}>{texts['confirm-new-msg']}</p>
        <div style={{ display: 'flex', gap: 10, justifyContent: 'center', marginTop: 14 }}>
          <button
            type="button"
            style={{
              background: 'var(--raster-zacht)',
              color: 'var(--inkt)',
              border: 'none',
              borderRadius: 0,
              padding: '10px 18px',
              cursor: 'pointer',
              fontWeight: 600,
            }}
            onClick={() => setPendingDeal(null)}
          >
            {texts['cancel']}
          </button>
          <button
            type="button"
            style={{
              background: 'var(--kobalt)',
              color: 'var(--papier)',
              border: 'none',
              borderRadius: 0,
              padding: '10px 18px',
              cursor: 'pointer',
              fontWeight: 600,
            }}
            onClick={() => {
              if (pendingDeal === null) return;
              void startRound(pendingDeal.level, pendingDeal.category);
            }}
          >
            {texts['confirm-ok']}
          </button>
        </div>
      </Overlay>

      <ZoomPop ref={zoom} />
    </>
  );

  return (
    <GameShell
      game="memory"
      title={texts['app-title']}
      splash={texts['splash-title']}
      onSettings={() => setShowSettings(true)}
      overlays={overlays}
    >
      {body}
    </GameShell>
  );
}
