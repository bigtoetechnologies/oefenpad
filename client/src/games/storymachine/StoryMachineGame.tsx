import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import { api, ApiError, type Texts } from '../../api';
import { GameShell } from '../../site/GameShell';
import { ResumeNote } from '../../shared/ResumeNote';
import { useGameData } from '../../shared/useGameData';
import { settleRow, spinDuration, type StripDirection } from './strips';

/* =================================================================
   Verhaalmachine — the story machine.

   Reels are positional: reel 0 is always WHO, reel 1 always DOES
   WHAT. That is why this is a machine and not a bag of dice, so the
   order the server sends is the order on screen.

   The server draws every tile. A spin only hands back the pictures the
   animation walks past; the tile it lands on is already in the view.
   Held reels never move. The class names mirror the old page, which
   storymachine.css is scoped to.
   ================================================================= */

const GAME = 'storymachine';

/** The service allows two to six reels; the old page opens on three. */
const MIN_REELS = 2;
const MAX_REELS = 6;
const DEFAULT_COUNT = 3;

/** How long the lever stays pulled when a pull cannot do anything. */
const NUDGE_MS = 260;

const REDUCED_MOTION = '(prefers-reduced-motion: reduce)';

type Language = 'nl' | 'en';

interface ReelLabel {
  nl: string;
  en: string;
}

interface Tile {
  id: string;
  /** A picture, drawn the same in every language. Never text. */
  art: string;
  nl: string;
  en: string;
}

interface Reel {
  index: number;
  label: ReelLabel;
  held: boolean;
  tile: Tile;
}

interface StoryView {
  count: number;
  language: Language;
  reels: Reel[];
}

interface SpinStrip {
  index: number;
  /** Fourteen pictures; the last one is the tile that lands. */
  art: string[];
}

/**
 * A spin answers like any other move, except that its view is wrapped one
 * level deeper and carries the strips: `{ view: { view, strips } }`.
 */
interface SpinPayload {
  view: StoryView;
  strips: SpinStrip[];
}

/**
 * The service chooses between two view shapes for the result's `view`: the
 * plain view every other move returns, or the spin's payload. The running
 * server and this source disagree on which one is in force, so both are
 * accepted and told apart by their keys.
 */
function readView(result: unknown): StoryView | null {
  if (typeof result !== 'object' || result === null) return null;
  const outer = result as Partial<StoryView> & Partial<SpinPayload>;
  if (Array.isArray(outer.reels)) return outer as StoryView;
  if (typeof outer.view === 'object' && outer.view !== null) return outer.view;
  return null;
}

function readStrips(result: unknown): SpinStrip[] {
  if (typeof result !== 'object' || result === null) return [];
  const outer = result as Partial<StoryView> & Partial<SpinPayload>;
  return Array.isArray(outer.strips) ? outer.strips : [];
}

/** What one reel shows, and how it moves there. */
interface ReelCell {
  art: string[];
  direction: StripDirection;
  transitionMs: number;
  spinning: boolean;
}

const atRest = (art: string): ReelCell => ({
  art: [art],
  direction: 'up',
  transitionMs: 0,
  spinning: false,
});

function messageFor(cause: unknown): string {
  return cause instanceof ApiError ? cause.message : 'De oefening is even niet bereikbaar.';
}

function prefersReducedMotion(): boolean {
  return window.matchMedia(REDUCED_MOTION).matches;
}

export function StoryMachineGame() {
  const { texts, error } = useGameData(GAME);

  if (error !== null) {
    return (
      <GameShell game={GAME} title="Verhaalmachine">
        <main className="app-container">
          <p role="alert" className="laden">
            {error}
          </p>
        </main>
      </GameShell>
    );
  }

  if (texts === null) {
    return (
      <GameShell game={GAME} title="Verhaalmachine">
        <main className="app-container">
          <p className="laden">Even laden…</p>
        </main>
      </GameShell>
    );
  }

  return <StoryBoard texts={texts} />;
}

function StoryBoard({ texts }: { texts: Texts }) {
  const [roundId, setRoundId] = useState<string | null>(null);
  const [view, setView] = useState<StoryView | null>(null);
  const [count, setCount] = useState(DEFAULT_COUNT);
  const [language, setLanguage] = useState<Language>('nl');
  const [cells, setCells] = useState<ReelCell[]>([]);
  const [pulling, setPulling] = useState(false);
  const [busy, setBusy] = useState(false);
  const [turned, setTurned] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [resumed, setResumed] = useState<string | null>(null);

  const roundRef = useRef<string | null>(null);
  const countRef = useRef(DEFAULT_COUNT);
  const languageRef = useRef<Language>('nl');
  const movingRef = useRef(false);
  const spinningRef = useRef(false);
  const timersRef = useRef<number[]>([]);
  /* Set right before the render that puts a new strip in place, and cleared
     once that render has painted, so the strip is seen at its first picture
     before it travels. */
  const rewindRef = useRef(false);

  useEffect(() => {
    document.title = texts['page-title'] ?? 'Verhaalmachine';
  }, [texts]);

  const t = useCallback((key: string): string => texts[key] ?? '', [texts]);

  /** Every timer the animation sets, cleared together when the board goes. */
  const later = useCallback((ms: number, run: () => void) => {
    const timer = window.setTimeout(() => {
      timersRef.current = timersRef.current.filter((item) => item !== timer);
      run();
    }, ms);
    timersRef.current.push(timer);
  }, []);

  const stopTimers = useCallback(() => {
    timersRef.current.forEach((timer) => window.clearTimeout(timer));
    timersRef.current = [];
  }, []);

  useEffect(() => stopTimers, [stopTimers]);

  /* ---------- rounds ---------- */

  const start = useCallback(
    async (nextCount: number, nextLanguage: Language) => {
      if (movingRef.current) return;
      movingRef.current = true;
      setBusy(true);
      setNotice(null);
      setResumed(null);
      spinningRef.current = false;
      stopTimers();
      setPulling(false);
      setTurned(false);
      setView(null);
      setCells([]);

      try {
        const round = await api.start<StoryView>(GAME, {
          count: nextCount,
          language: nextLanguage,
        });
        roundRef.current = round.roundId;
        setRoundId(round.roundId);
        setView(round.view);
        setLanguage(round.view.language);
        languageRef.current = round.view.language;
        setCells(round.view.reels.map((reel) => atRest(reel.tile.art)));
      } catch (cause) {
        roundRef.current = null;
        setRoundId(null);
        setView(null);
        setCells([]);
        setNotice(messageFor(cause));
      } finally {
        movingRef.current = false;
        setBusy(false);
      }

      // The slider fires on every step of a drag, so the steps that arrived
      // while this round was loading were dropped. Catch up on the last one,
      // or the control reads a number the machine is not showing.
      if (countRef.current !== nextCount) {
        void start(countRef.current, languageRef.current);
      }
    },
    [stopTimers],
  );

  const startedRef = useRef(false);
  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;

    void (async () => {
      const saved = await api.saved<StoryView>(GAME).catch(() => null);
      if (saved !== null) {
        roundRef.current = saved.roundId;
        setRoundId(saved.roundId);
        setView(saved.view);
        setCount(saved.view.count);
        countRef.current = saved.view.count;
        setLanguage(saved.view.language);
        languageRef.current = saved.view.language;
        setCells(saved.view.reels.map((reel) => atRest(reel.tile.art)));
        setResumed(t('resumed'));
        return;
      }

      void start(countRef.current, languageRef.current);
    })();
  }, [start, t]);

  /** The server has answered a move; show what it says. */
  const apply = useCallback((next: StoryView) => {
    setView(next);
    setLanguage(next.language);
    languageRef.current = next.language;
    setTurned(false);
  }, []);

  /**
   * Sends one action and resolves to the move result's view, or null when the
   * round is gone or the call failed. An expired round is not restarted here:
   * the player is told, and offered a fresh round.
   */
  const send = useCallback(async (body: unknown): Promise<StoryView | null> => {
    const id = roundRef.current;
    if (id === null) return null;

    try {
      const result = await api.move<unknown>(GAME, id, body);
      // The round can be replaced while this is in flight — a slider step
      // starts a new one. Applying an answer from the round the player has
      // already left would show reels that belong to nothing.
      if (roundRef.current !== id) return null;
      return readView(result.view);
    } catch (cause) {
      setNotice(messageFor(cause));
      if (cause instanceof ApiError && cause.status === 410) {
        roundRef.current = null;
        setRoundId(null);
        setView(null);
        setCells([]);
      }
      return null;
    }
  }, []);

  const toggleHold = (reel: Reel) => {
    if (busy || spinningRef.current || view === null || roundId === null) return;

    const held = !reel.held;
    // The reel answers at once; the server's copy of it follows behind.
    setView({
      ...view,
      reels: view.reels.map((item) => (item.index === reel.index ? { ...item, held } : item)),
    });
    setNotice(null);

    void send({ action: 'hold', index: reel.index, held }).then((next) => {
      if (next !== null) apply(next);
    });
  };

  const chooseLanguage = (next: Language) => {
    if (busy || spinningRef.current || view === null || next === languageRef.current) return;
    setLanguage(next);
    languageRef.current = next;

    void send({ action: 'language', language: next }).then((result) => {
      if (result !== null) apply(result);
    });
  };

  const chooseCount = (next: number) => {
    // A spin owns the reels until it finishes; starting a new round under it
    // leaves the animation driving a board that no longer exists.
    if (spinningRef.current) return;
    if (!Number.isFinite(next) || next === countRef.current) return;
    const clamped = Math.min(MAX_REELS, Math.max(MIN_REELS, Math.round(next)));
    countRef.current = clamped;
    setCount(clamped);
    // A round already loading would swallow this one; `start` catches up with
    // countRef when it finishes.
    if (movingRef.current) return;
    void start(clamped, languageRef.current);
  };

  /* ---------- spinning ---------- */

  /** A spin, with the pictures the animation walks past. */
  const spin = async (): Promise<{ view: StoryView; strips: SpinStrip[] } | null> => {
    const id = roundRef.current;
    if (id === null) return null;

    try {
      const result = await api.move<unknown>(GAME, id, { action: 'spin' });
      // Same as `send`: a spin answered after the round was replaced must not
      // drive the animation of the round that replaced it.
      if (roundRef.current !== id) return null;
      const next = readView(result.view);
      return next === null ? null : { view: next, strips: readStrips(result.view) };
    } catch (cause) {
      setNotice(messageFor(cause));
      if (cause instanceof ApiError && cause.status === 410) {
        roundRef.current = null;
        setRoundId(null);
        setView(null);
        setCells([]);
      }
      return null;
    }
  };

  const pull = useCallback(async () => {
    if (busy || spinningRef.current || view === null || roundId === null) return;

    // Held reels stay where they are; pulling with all of them held does nothing.
    if (!view.reels.some((reel) => !reel.held)) return;

    spinningRef.current = true;
    setPulling(true);
    setTurned(false);
    setNotice(null);

    const spun = await spin();
    if (spun === null) {
      spinningRef.current = false;
      setPulling(false);
      return;
    }

    const landed = spun.view;
    const strips = new Map(spun.strips.map((strip) => [strip.index, strip]));
    const free = landed.reels.filter((reel) => !reel.held && strips.has(reel.index));

    const durationOf = (index: number): number =>
      spinDuration(free.findIndex((reel) => reel.index === index), free.length);

    const finish = () => {
      setCells(landed.reels.map((reel) => atRest(reel.tile.art)));
      apply(landed);
      spinningRef.current = false;
      setPulling(false);
    };

    // Nothing to animate: a held reel, or the visitor asked for less movement.
    if (free.length === 0 || prefersReducedMotion()) {
      finish();
      return;
    }

    rewindRef.current = true;
    setCells(landed.reels.map((reel) => {
      const strip = strips.get(reel.index);
      if (strip === undefined || reel.held || strip.art.length === 0) {
        return atRest(reel.tile.art);
      }
      return {
        art: strip.art,
        // Neighbouring reels turn opposite ways, so the drum reads as one machine.
        direction: reel.index % 2 === 0 ? 'up' : 'down',
        transitionMs: durationOf(reel.index),
        spinning: true,
      };
    }));
    setView(landed);
    setLanguage(landed.language);
    languageRef.current = landed.language;

    const longest = Math.max(...free.map((reel) => durationOf(reel.index)));
    later(longest + 80, finish);
  }, [apply, busy, later, view, roundId]);

  const pullRef = useRef(pull);
  useEffect(() => {
    pullRef.current = pull;
  });

  /* ---------- the lever ---------- */

  const nudgeRef = useRef<number | null>(null);

  /** A pull that cannot do anything still moves the lever, so it never looks dead. */
  const nudgeLever = () => {
    if (nudgeRef.current !== null) window.clearTimeout(nudgeRef.current);
    setPulling(true);
    nudgeRef.current = window.setTimeout(() => {
      nudgeRef.current = null;
      setPulling(false);
    }, NUDGE_MS);
  };

  useEffect(() => () => {
    if (nudgeRef.current !== null) window.clearTimeout(nudgeRef.current);
  }, []);

  /* Space or Enter anywhere on the page pulls the lever, unless the focus is
     on something that already answers to those keys: a button, the slider or
     the language checkbox. */
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== ' ' && event.key !== 'Enter') return;
      if (event.ctrlKey || event.metaKey || event.altKey || event.repeat) return;
      if (event.defaultPrevented) return;

      const target = event.target as HTMLElement | null;
      const focused = document.activeElement;
      if (
        focused !== null && focused !== document.body
        || target !== null && target !== document.body
          && target.closest('button, input, textarea, select, a, [contenteditable="true"]') !== null
      ) {
        return;
      }

      event.preventDefault();
      void pullRef.current();
    };

    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, []);

  /* ---------- render ---------- */

  const reels = view?.reels ?? [];
  const freeReels = reels.filter((reel) => !reel.held);
  const leverBlocked = view === null || busy || freeReels.length === 0;
  const announcement = reels.map((reel) => reel.tile[language]).join(', ');

  let cards: ReactNode = null;
  if (view !== null) {
    cards = (
      <div className="cards" id="cards">
        {reels.map((reel) => {
          const word = turned ? reel.tile[language] : '';
          const label = word === ''
            ? `${reel.label.en} — ${t('turn-for-word')}`
            : `${reel.label.en}: ${word}`;
          return (
            <button
              key={reel.index}
              type="button"
              className={turned ? 'card turned' : 'card'}
              aria-pressed={turned}
              aria-label={label}
              onClick={() => setTurned(!turned)}
            >
              <span className="card-inner">
                <span className="card-face card-back" aria-hidden="true" />
                <span className="card-face card-front">
                  <span className="card-word" lang={language}>{word}</span>
                </span>
              </span>
            </button>
          );
        })}
      </div>
    );
  }

  const body = (
    <main className="app-container">
      <div className="controls">
        <label className="control">
          <span>{t('reels')}</span>
          <input
            type="range"
            id="reel-count"
            min={MIN_REELS}
            max={MAX_REELS}
            step={1}
            value={count}
            onChange={(event) => chooseCount(Number(event.target.value))}
          />
          <output id="reel-count-out" htmlFor="reel-count">{count}</output>
        </label>

        <label className="control control-check">
          <input
            type="checkbox"
            id="lang-nl"
            checked={language === 'nl'}
            onChange={(event) => chooseLanguage(event.target.checked ? 'nl' : 'en')}
          />
          <span>{t('dutch')}</span>
        </label>
      </div>

      <div className="cabinet">
        <div className="window" id="window">
          {reels.map((reel, index) => (
            <ReelStrip
              key={`${roundId ?? ''}-${reel.index}`}
              reel={reel}
              cell={cells[index] ?? atRest(reel.tile.art)}
              rewind={rewindRef}
              label={reel.held ? `${reel.label.en}, ${t('hold-hint')}` : `${reel.label.en} — ${t('hold-hint')}`}
              onToggle={() => toggleHold(reel)}
            />
          ))}
        </div>

        <button
          type="button"
          id="lever"
          className={pulling ? 'lever pulled' : 'lever'}
          aria-label={t('lever-label')}
          aria-disabled={leverBlocked}
          onClick={() => {
            if (leverBlocked) nudgeLever();
            else void pull();
          }}
        >
          <span className="lever-stick" />
          <span className="lever-knob" />
        </button>
      </div>

      {cards}

      <p className="held-hint">{t('held-hint')}</p>

      <ResumeNote text={resumed} onDone={() => setResumed(null)} />

      <p className="sr-only alleen-lezer" id="announce" aria-live="polite">
        {announcement}
      </p>

      {notice !== null && (
        <p className="held-hint" role="alert">
          {notice}
          {roundId === null && (
            <>
              {' '}
              <button
                type="button"
                className="storymachine-new"
                onClick={() => void start(countRef.current, languageRef.current)}
              >
                {t('btn-new') || 'Nieuw spel'}
              </button>
            </>
          )}
        </p>
      )}

      {view === null && notice === null && <p className="laden">Even laden…</p>}
    </main>
  );

  return (
    <GameShell game={GAME} title={t('title') || 'Verhaalmachine'} tagline={t('tagline') || undefined}>
      {body}
    </GameShell>
  );
}

interface ReelStripProps {
  reel: Reel;
  cell: ReelCell;
  /** Set just before a spin renders; cleared once that render has painted. */
  rewind: { current: boolean };
  label: string;
  onToggle: () => void;
}

/**
 * One reel: a window onto a strip of pictures. The strip is moved by whole
 * rows, so its travel follows the reel's own width without measuring a tile.
 * While spinning it is translated; at rest it holds only the landed tile.
 */
function ReelStrip({ reel, cell, rewind, label, onToggle }: ReelStripProps) {
  const stripRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const strip = stripRef.current;
    if (strip === null) return;

    const row = settleRow(cell.art.length, cell.direction);
    const wasRewinding = rewind.current;
    rewind.current = false;

    if (wasRewinding) {
      strip.style.transition = 'none';
      strip.style.transform = 'translateY(0)';
      // Force the browser to accept the reset before it is animated away from.
      void strip.offsetHeight;
    }

    strip.style.transition = cell.transitionMs > 0
      ? `transform ${cell.transitionMs}ms cubic-bezier(.17,.67,.21,1)`
      : 'none';
    strip.style.transform = `translateY(calc(${row} * -100%))`;
  }, [cell, rewind]);

  const classes = [
    'reel',
    reel.held ? 'held' : '',
    cell.spinning ? 'spinning' : '',
  ].filter((name) => name !== '').join(' ');

  return (
    <button
      type="button"
      className={classes}
      aria-pressed={reel.held}
      aria-label={label}
      onClick={onToggle}
    >
      <div className="strip" ref={stripRef}>
        {cell.art.map((art, index) => (
          <div className="tile" key={`${index}-${art}`} aria-hidden="true">
            <span className="tile-art">{art}</span>
          </div>
        ))}
      </div>
    </button>
  );
}
