import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from 'react';
import { api, ApiError } from '../../api';
import { GameShell } from '../../site/GameShell';
import { ResumeNote } from '../../shared/ResumeNote';
import { WordImage } from '../../shared/WordImage';
import { formatTime } from '../../shared/format';
import { sfx } from '../../shared/sound';
import { spawnConfetti, type ConfettiOptions } from '../../shared/confetti';
import { useGameData } from '../../shared/useGameData';
import { useLocalStorage } from '../../shared/useLocalStorage';
import { useTimer } from '../../shared/useTimer';
import { paintCanvas, sizeCanvas } from './canvas';
import {
  ERROR_MS,
  HINT_MS,
  SETTINGS_KEY,
  STATS_KEY,
  TRANSLATE_LANGUAGES,
  cellKey,
  cellSizeFor,
  cellsInLine,
  fontSizeFor,
  foundCells,
  foundIndexOf,
  isStraightLine,
  placementFrom,
  viewOf,
  type Cell,
  type MovePayload,
  type PlacementMap,
  type WordSearchResume,
  type WordSearchSettings,
  type WordSearchStats,
  type WordSearchView,
} from './model';

/* =================================================================
   Woordzoeker — find the hidden Dutch words in the grid.

   The server generates the grid, places the words and judges every
   selection; the browser never receives the placement list. It
   keeps only the cells of the words the player has already been
   shown — found ones and hinted ones — for painting and the word
   strike-through. The class names mirror the old page, which
   wordsearch.css is scoped to.
   ================================================================= */

const DEFAULT_DIFFICULTY = 'beginner';
const DEFAULT_CATEGORY = 'animals';
const DEFAULT_SOUND = true;
const DENIED_MS = 350;

const HINT_STYLE = { display: 'flex', gap: 10, justifyContent: 'center', marginTop: 14 };
const CATEGORY_STYLE = { maxWidth: 520 };
const CATEGORY_SUBTITLE_STYLE = { fontSize: 13, color: 'var(--grijs)', marginBottom: 8 };
const SOFT_NOTE_STYLE = { color: 'var(--grijs)', fontSize: 14 };
const CONFIRM_BUTTON_STYLE = {
  background: 'var(--papier)',
  color: 'var(--inkt)',
  boxShadow: 'inset 0 0 0 2px var(--inkt)',
  border: 'none',
  borderRadius: 0,
  padding: '10px 18px',
  cursor: 'pointer',
  fontWeight: 600,
};

/** The celebration burst — the old page's palette and timing. */
const CONFETTI: ConfettiOptions = {
  colors: ['#FF6B6B', '#FFD93D', '#6BCB77', '#4D96FF', '#FF8C42', '#C084FC', '#F472B6'],
  count: 80,
  duration: [2, 4],
  delay: [0, 0.8],
  top: [-25, -5],
  removeAfter: 5000,
};

interface Selection {
  start: Cell;
  end: Cell;
}

export function WordSearchGame() {
  const { texts, options, error } = useGameData('wordsearch');

  useEffect(() => {
    if (texts?.['page-title']) document.title = texts['page-title'];
  }, [texts]);

  const [storedSettings, saveSettings] = useLocalStorage<WordSearchSettings>(SETTINGS_KEY, {
    soundEffects: DEFAULT_SOUND,
    difficulty: DEFAULT_DIFFICULTY,
    category: DEFAULT_CATEGORY,
    translateTo: '',
  });
  // The old page filled in missing keys on load rather than trusting the
  // stored object as a whole.
  const settings: WordSearchSettings = {
    soundEffects: storedSettings.soundEffects !== false,
    difficulty: typeof storedSettings.difficulty === 'string' ? storedSettings.difficulty : DEFAULT_DIFFICULTY,
    category: typeof storedSettings.category === 'string' ? storedSettings.category : DEFAULT_CATEGORY,
    translateTo: typeof storedSettings.translateTo === 'string' ? storedSettings.translateTo : '',
  };
  const [, saveStats] = useLocalStorage<WordSearchStats>(STATS_KEY, {
    wins: 0,
    streak: 0,
    bestStreak: 0,
  });

  const [difficulty, setDifficulty] = useState(settings.difficulty);
  const [category, setCategory] = useState(settings.category);
  const [view, setView] = useState<WordSearchView | null>(null);
  const [roundId, setRoundId] = useState<string | null>(null);
  /* Mirrors roundId for the async paths: a move that resolves after the round
     was replaced must be able to tell, and state is stale inside that closure. */
  const roundIdRef = useRef<string | null>(null);
  const rememberRound = useCallback((id: string | null) => {
    roundIdRef.current = id;
    setRoundId(id);
  }, []);
  const [dealing, setDealing] = useState(false);
  const [roundError, setRoundError] = useState<string | null>(null);
  const [resumed, setResumed] = useState<string | null>(null);
  const [expired, setExpired] = useState(false);
  const [placements, setPlacements] = useState<PlacementMap>({});

  const [selection, setSelection] = useState<Selection | null>(null);
  const [dragging, setDragging] = useState(false);
  const [wrongCells, setWrongCells] = useState<Set<string>>(new Set());
  const [hint, setHint] = useState<{ index: number; cells: Cell[] } | null>(null);
  const [celebrating, setCelebrating] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [aboutOpen, setAboutOpen] = useState(false);
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [confirmRestart, setConfirmRestart] = useState(false);
  const [pendingTranslate, setPendingTranslate] = useState<string | null>(null);
  const [revealed, setRevealed] = useState<Set<number>>(new Set());
  const [denied, setDenied] = useState<string | null>(null);

  const [cellSize, setCellSize] = useState(() => cellSizeFor(16, window.innerWidth));
  const [timing, setTiming] = useState(false);
  const seconds = useTimer(timing, roundId);

  const gridRef = useRef<HTMLDivElement>(null);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  // True while a selection is posted; the grid must not take a new tap then.
  const submitting = useRef(false);
  const pointerStart = useRef<Cell | null>(null);
  const hintTimer = useRef<number | null>(null);
  const errorTimer = useRef<number | null>(null);
  const deniedTimer = useRef<number | null>(null);
  const timers = useRef<number[]>([]);
  const confetti = useRef<HTMLDivElement>(null);
  const started = useRef(false);
  const categoryTimer = useRef<number | null>(null);

  useEffect(() => () => {
    timers.current.forEach((id) => window.clearTimeout(id));
    timers.current = [];
    if (hintTimer.current !== null) window.clearTimeout(hintTimer.current);
    if (errorTimer.current !== null) window.clearTimeout(errorTimer.current);
    if (deniedTimer.current !== null) window.clearTimeout(deniedTimer.current);
  }, []);

  const levels = options?.levels ?? [];
  const categories = options?.categories ?? [];

  const t = (key: string, fallback = key) => texts?.[key] ?? fallback;

  /* ---------- rounds ---------- */

  const deal = useCallback(
    async (wantedCategory: string, wantedDifficulty: string, wantedTranslate: string) => {
      // From here the old round is gone, so a move still in flight for it must
      // not repaint the board when it lands.
      roundIdRef.current = null;
      setDealing(true);
      setRoundError(null);
      setResumed(null);
      setExpired(false);
      setPlacements({});
      setSelection(null);
      setDragging(false);
      setWrongCells(new Set());
      setHint(null);
      setRevealed(new Set());
      setDenied(null);
      setCelebrating(false);
      setTiming(false);
      if (hintTimer.current !== null) window.clearTimeout(hintTimer.current);
      hintTimer.current = null;
      if (errorTimer.current !== null) window.clearTimeout(errorTimer.current);
      errorTimer.current = null;
      if (deniedTimer.current !== null) window.clearTimeout(deniedTimer.current);
      deniedTimer.current = null;
      canvasRef.current?.getContext('2d')?.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

      const body: Record<string, string> = {
        category: wantedCategory,
        difficulty: wantedDifficulty,
      };
      if (wantedTranslate) body.translateTo = wantedTranslate;

      try {
        const round = await api.start<WordSearchView>('wordsearch', body);
        rememberRound(round.roundId);
        setView(round.view);
        setTiming(!round.view.done);
      } catch (cause) {
        rememberRound(null);
        setView(null);
        setRoundError(cause instanceof ApiError ? cause.message : t('error', 'De oefening is even niet bereikbaar.'));
      } finally {
        setDealing(false);
      }
    },
    // t only reads the loaded texts, which do not change after load.
    [rememberRound, t],
  );

  const rememberSettings = useCallback(
    (next: Partial<WordSearchSettings>) => {
      saveSettings({ ...settings, ...next });
    },
    [saveSettings, settings],
  );

  /* The wanted settings are passed down rather than read back off `settings`:
     `rememberSettings` only schedules a state update, so a deal in the same
     tick would still send the previous translation. */
  const newRound = useCallback(
    (
      wantedCategory = category,
      wantedDifficulty = difficulty,
      wantedTranslate = settings.translateTo,
    ) => {
      setCategory(wantedCategory);
      setDifficulty(wantedDifficulty);
      rememberSettings({
        category: wantedCategory,
        difficulty: wantedDifficulty,
        translateTo: wantedTranslate,
      });
      void deal(wantedCategory, wantedDifficulty, wantedTranslate);
    },
    [category, difficulty, settings.translateTo, deal, rememberSettings],
  );

  // A first visit opens the category picker once the splash has gone, as the
  // old page did. The marker keeps it from opening on every reload.
  useEffect(() => {
    if (!options) return;
    const seen = 'oefenpad-woordzoeker-visited';
    try {
      if (window.localStorage.getItem(seen) === '1') return;
      window.localStorage.setItem(seen, '1');
    } catch {
      return;
    }
    const timer = window.setTimeout(() => setCategoryOpen(true), 2600);
    categoryTimer.current = timer;
    return () => {
      window.clearTimeout(timer);
      if (categoryTimer.current === timer) categoryTimer.current = null;
    };
  }, [options]);

  // The first round waits for the options. A saved round wins: the player
  // left this board mid-puzzle and should get it back, not a new one.
  useEffect(() => {
    if (started.current || !options) return;
    started.current = true;

    void (async () => {
      const saved = await api.saved<WordSearchView, WordSearchResume>('wordsearch').catch(() => null);
      if (saved !== null) {
        // A returning player does not need the first-visit picker over the board.
        if (categoryTimer.current !== null) {
          window.clearTimeout(categoryTimer.current);
          categoryTimer.current = null;
        }
        setCategoryOpen(false);
        rememberRound(saved.roundId);
        setView(saved.view);
        setPlacements(saved.resume?.placements ?? {});
        setDifficulty(saved.view.difficulty);
        setCategory(saved.view.category.id);
        setTiming(!saved.view.done);
        setResumed(t('resumed', 'We gaan verder waar je gebleven was.'));
        return;
      }

      if (!options.categories.some((entry) => entry.id === category)) {
        const first = options.categories[0];
        if (!first) return;
        newRound(first.id, difficulty);
        return;
      }
      void deal(category, difficulty, settings.translateTo);
    })();
  }, [options, category, difficulty, settings.translateTo, deal, newRound, t]);

  /* ---------- found state ---------- */

  const size = view?.size ?? 10;
  const words = view?.words ?? [];
  const found = view?.found ?? [];
  const foundCount = found.filter(Boolean).length;

  /** word index -> endpoint pair, for the outlines on the canvas. */
  const foundLines = useMemo(() => {
    const lines: Array<[Cell, Cell]> = [];
    words.forEach((_word, index) => {
      if (!found[index]) return;
      const line = placements[index];
      if (!line || line.length === 0) return;
      lines.push([line[0], line[line.length - 1]]);
    });
    return lines;
  }, [words, found, placements]);

  const foundSet = useMemo(() => foundCells(placements, found), [placements, found]);

  const hintSet = useMemo(() => {
    const cells = new Set<string>();
    if (hint) for (const cell of hint.cells) cells.add(cellKey(cell.r, cell.c));
    return cells;
  }, [hint]);

  const selectionCells = useMemo(() => {
    if (!selection) return [];
    return cellsInLine(selection.start, selection.end, size);
  }, [selection, size]);

  const selectionSet = useMemo(() => {
    const cells = new Set<string>();
    for (const cell of selectionCells) cells.add(cellKey(cell.r, cell.c));
    return cells;
  }, [selectionCells]);

  /* ---------- canvas ---------- */

  const repaint = useCallback(() => {
    paintCanvas(canvasRef.current, gridRef.current, {
      cells: gridRef.current ? [...gridRef.current.children] : [],
      size,
      found: foundLines,
      drag: null,
    });
  }, [foundLines, size]);

  // Cell size follows the grid size and the window, as the old page's
  // renderGrid() did.
  useEffect(() => {
    const measure = () => setCellSize(cellSizeFor(size, window.innerWidth));
    measure();
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, [size]);

  // The canvas is the grid wrapper's size, so it must be re-laid-out
  // whenever the grid changes shape, then repainted.
  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper) return;
    sizeCanvas(canvasRef.current!, wrapper);
    repaint();
  }, [repaint, cellSize, size, view]);

  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper) return;
    const observer = new ResizeObserver(() => {
      sizeCanvas(canvasRef.current!, wrapper);
      repaint();
    });
    observer.observe(wrapper);
    return () => observer.disconnect();
  }, [repaint, view]);

  /* ---------- selection ---------- */

  const clearSelection = useCallback(() => {
    setSelection(null);
    setDragging(false);
    setWrongCells(new Set());
    pointerStart.current = null;
  }, []);

  const flashDenied = useCallback(() => {
    if (deniedTimer.current !== null) window.clearTimeout(deniedTimer.current);
    setDenied(t('status-denied', 'Kies eerst een lijn.'));
    deniedTimer.current = window.setTimeout(() => setDenied(null), DENIED_MS);
  }, [t]);

  const submit = useCallback(
    async (start: Cell, end: Cell) => {
      const cells = cellsInLine(start, end, size);
      if (!roundId || cells.length === 0) {
        clearSelection();
        return;
      }

      setSelection({ start, end });
      setWrongCells(new Set());

      // The selection stays on screen while the move is in flight, and
      // `dragging` is false by then, so a tap during that window would be read
      // as the second tap of a line the player never drew.
      submitting.current = true;

      let shown: boolean;
      try {
        // A found selection answers `{ view, foundIndex }`, a wrong one the
        // bare view; api.move wraps either in its own envelope.
        const answer = await api.move<MovePayload>('wordsearch', roundId, {
          action: 'select',
          r1: start.r,
          c1: start.c,
          r2: end.r,
          c2: end.c,
        });
        // The settings panel can deal a new round while this is in flight.
        // Repainting with the old round's view would put back a grid the
        // player has already replaced.
        if (roundIdRef.current !== roundId) return;

        const payload = answer.view;
        const next = viewOf(payload);
        const index = foundIndexOf(payload);
        setView(next);
        setSelection(null);
        setDragging(false);
        pointerStart.current = null;

        shown = index >= 0;
        if (shown) {
          const line = placementFrom(start.r, start.c, end.r, end.c, next.size);
          setPlacements((current) => ({ ...current, [index]: line }));
          if (hint && hint.index === index) setHint(null);
          sfx.correct(settings.soundEffects);
          if (next.done) {
            setTiming(false);
            saveStats((current) => {
              const streak = current.streak + 1;
              return {
                wins: current.wins + 1,
                streak,
                bestStreak: Math.max(current.bestStreak, streak),
              };
            });
            setCelebrating(true);
            spawnConfetti(confetti.current, CONFETTI);
            sfx.fanfare(settings.soundEffects);
          } else {
            setTiming(true);
          }
        }
      } catch (cause) {
        clearSelection();
        setTiming(false);
        if (cause instanceof ApiError && cause.status === 410) setExpired(true);
        setRoundError(cause instanceof ApiError ? cause.message : t('error', 'De oefening is even niet bereikbaar.'));
        return;
      } finally {
        submitting.current = false;
      }

      if (!shown) {
        // Wrong: the old page flashed .cell.error over the selection.
        const keys = new Set<string>();
        for (const cell of cells) keys.add(cellKey(cell.r, cell.c));
        setWrongCells(keys);
        if (errorTimer.current !== null) window.clearTimeout(errorTimer.current);
        errorTimer.current = window.setTimeout(() => {
          setWrongCells(new Set());
          setSelection(null);
          errorTimer.current = null;
        }, ERROR_MS);
      }
    },
    [clearSelection, hint, roundId, saveStats, settings.soundEffects, size, t],
  );

  const cellFromPointer = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>): Cell | null => {
      const grid = gridRef.current;
      if (!grid) return null;
      const box = grid.getBoundingClientRect();
      const step = box.width / size;
      const c = Math.floor((event.clientX - box.left) / step);
      const r = Math.floor((event.clientY - box.top) / step);
      if (r < 0 || r >= size || c < 0 || c >= size) return null;
      return { r, c };
    },
    [size],
  );

  const onPointerDown = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (dealing || submitting.current || !view || view.done) return;
    const cell = cellFromPointer(event);
    if (!cell) return;
    event.preventDefault();
    gridRef.current?.setPointerCapture(event.pointerId);

    if (errorTimer.current !== null) {
      window.clearTimeout(errorTimer.current);
      errorTimer.current = null;
    }
    setWrongCells(new Set());

    if (selection && !dragging) {
      // Second tap: the first cell was already chosen.
      if (selection.start.r === cell.r && selection.start.c === cell.c) {
        clearSelection();
        return;
      }
      const start = selection.start;
      if (isStraightLine(start, cell)) {
        void submit(start, cell);
      } else {
        setSelection({ start: cell, end: cell });
        pointerStart.current = cell;
        flashDenied();
      }
      return;
    }

    pointerStart.current = cell;
    setDragging(true);
    setSelection({ start: cell, end: cell });
  };

  const onPointerMove = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (!dragging || submitting.current) return;
    const cell = cellFromPointer(event);
    if (!cell) return;
    const start = pointerStart.current;
    if (!start) return;
    if (cell.r === start.r && cell.c === start.c) return;
    if (!isStraightLine(start, cell)) return;
    setSelection({ start, end: cell });
  };

  const onPointerUp = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (!dragging) return;
    const start = pointerStart.current;
    const cell = cellFromPointer(event);
    setDragging(false);

    if (!start || !cell) {
      clearSelection();
      return;
    }
    if (start.r === cell.r && start.c === cell.c) {
      // A tap leaves the first cell marked; the next tap completes it.
      setSelection({ start, end: start });
      pointerStart.current = null;
      return;
    }
    if (!isStraightLine(start, cell)) {
      flashDenied();
      clearSelection();
      return;
    }
    pointerStart.current = null;
    void submit(start, cell);
  };

  const onPointerCancel = () => clearSelection();

  /* ---------- hints ---------- */

  const useHint = async () => {
    if (!roundId || !view || view.hintsLeft <= 0 || hint || view.done) return;
    try {
      const answer = await api.move<MovePayload>('wordsearch', roundId, { action: 'hint' });
      const payload = answer.view;
      setView(viewOf(payload));
      const hint = payload?.hint;
      if (!hint) return;
      setHint({ index: hint.index, cells: hint.cells });
      setRevealed((current) => new Set(current).add(hint.index));
      if (hintTimer.current !== null) window.clearTimeout(hintTimer.current);
      hintTimer.current = window.setTimeout(() => {
        setHint(null);
        hintTimer.current = null;
      }, HINT_MS);
    } catch (cause) {
      if (cause instanceof ApiError && cause.status === 410) setExpired(true);
      setRoundError(cause instanceof ApiError ? cause.message : t('error', 'De oefening is even niet bereikbaar.'));
    }
  };

  /* ---------- settings ---------- */

  const changeTranslation = (value: string) => {
    if (value === settings.translateTo) return;
    if (foundCount > 0) {
      // The word pool changes with the translation, so the puzzle restarts.
      // Hold the wanted value until the restart is confirmed: without it the
      // player loses their progress and the puzzle comes back untranslated.
      setPendingTranslate(value);
      setConfirmRestart(true);
      return;
    }
    newRound(category, difficulty, value);
  };

  const confirmTranslation = () => {
    setConfirmRestart(false);
    if (pendingTranslate === null) return;
    newRound(category, difficulty, pendingTranslate);
    setPendingTranslate(null);
  };

  const cancelTranslation = () => {
    setConfirmRestart(false);
    setPendingTranslate(null);
  };

  const pickCategory = (id: string) => {
    setCategoryOpen(false);
    newRound(id);
  };

  const pickRandomCategory = () => {
    if (categories.length === 0) return;
    const pick = categories[Math.floor(Math.random() * categories.length)];
    setCategoryOpen(false);
    newRound(pick.id);
  };

  const toggleRevealed = (index: number) => {
    setRevealed((current) => {
      const next = new Set(current);
      if (next.has(index)) next.delete(index);
      else next.add(index);
      return next;
    });
  };

  /** The old page disabled a level whose words the category cannot fill. */
  const canFill = (levelSize: number | null): boolean => {
    if (levelSize === null) return categories.length > 0;
    // Worst case is the longest fill: insane asks for many words.
    const entry = categories.find((item) => item.id === category);
    if (!entry) return true;
    const needed = levelSize >= 20 ? 16 : levelSize >= 16 ? 10 : levelSize >= 12 ? 8 : 6;
    return entry.count >= needed;
  };

  /* ---------- shells ---------- */

  if (error) {
    return (
      <GameShell game="wordsearch" title={t('ws-title', 'Woordzoeker')}>
        <main className="app-container">
          <p className="hint" role="alert">{error}</p>
        </main>
      </GameShell>
    );
  }

  if (!texts || !options) {
    return (
      <GameShell game="wordsearch" title={t('ws-title', 'Woordzoeker')}>
        <main className="app-container">
          <p className="hint">Even laden…</p>
        </main>
      </GameShell>
    );
  }

  const hintsLeft = view?.hintsLeft ?? 0;

  const overlays = (
    <>
      <div
        className={`celebration-overlay${celebrating ? '' : ' hidden'}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="celebrationOverlayTitle"
      >
        <div className="confetti-container" ref={confetti} />
        <div className="celebration-card">
          <div className="trophy">
            <img src="/assets/logo/logo_128px.png" alt="Oefenpad" className="trophy-logo" />
          </div>
          <h2 id="celebrationOverlayTitle">{t('cele-title')}</h2>
          <p style={SOFT_NOTE_STYLE}>{t('cele-msg')}</p>
          <p style={SOFT_NOTE_STYLE}>
            {t('time-label')} <span id="celeTime">{formatTime(seconds)}</span>
          </p>
          <button type="button" onClick={() => setCelebrating(false)}>{t('btn-close')}</button>
          <button
            type="button"
            onClick={() => {
              setCelebrating(false);
              setCategoryOpen(true);
            }}
          >
            {t('btn-new')}
          </button>
        </div>
      </div>

      <div
        className={`settings-overlay${settingsOpen ? '' : ' hidden'}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="settingsOverlayTitle"
      >
        <div className="settings-modal">
          <h2 id="settingsOverlayTitle">{t('settings-title')}</h2>
          <div className="settings-row">
            <span className="settings-label">{t('sound-effects')}</span>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={settings.soundEffects}
                onChange={(event) => rememberSettings({ soundEffects: event.target.checked })}
              />
              <span className="toggle-slider" />
            </label>
          </div>
          <div className="settings-row">
            <label className="settings-label" htmlFor="settingTranslateTo">
              {t('translate-label')}
            </label>
            <select
              id="settingTranslateTo"
              className="settings-select"
              value={settings.translateTo}
              onChange={(event) => changeTranslation(event.target.value)}
            >
              <option value="">{t('translate-off')}</option>
              {TRANSLATE_LANGUAGES.filter((language) => language.code !== 'nl').map((language) => (
                <option key={language.code} value={language.code} lang={language.code}>
                  {language.name}
                </option>
              ))}
            </select>
          </div>
          <p className="settings-note">{t('translate-hint')}</p>
          <button type="button" className="settings-close-btn" onClick={() => setSettingsOpen(false)}>
            {t('close')}
          </button>
        </div>
      </div>

      <div
        className={`settings-overlay${categoryOpen ? '' : ' hidden'}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="categoryOverlayTitle"
      >
        <div className="settings-modal" style={CATEGORY_STYLE}>
          <h2 id="categoryOverlayTitle">{t('cat-title')}</h2>
          <p style={CATEGORY_SUBTITLE_STYLE}>{t('cat-subtitle')}</p>
          <div className="category-grid">
            {categories.map((entry) => (
              <button
                key={entry.id}
                type="button"
                className={`cat-btn${entry.id === category ? ' active' : ''}`}
                aria-pressed={entry.id === category}
                onClick={() => pickCategory(entry.id)}
              >
                {entry.icon}
                <span>{entry.name}</span>
              </button>
            ))}
            <button type="button" className="cat-btn random-btn" onClick={pickRandomCategory}>
              🎲<span>{t('random-cat')}</span>
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
        </div>
      </div>

      <div
        className={`settings-overlay${aboutOpen ? '' : ' hidden'}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="aboutOverlayTitle"
      >
        <div className="settings-modal" style={{ textAlign: 'center' }}>
          <h2 id="aboutOverlayTitle">{t('about')}</h2>
          <img
            src="/assets/logo/logo_128px.png"
            alt="Oefenpad"
            style={{ width: 100, margin: '16px auto', display: 'block' }}
          />
          <div style={{ fontSize: 22, fontWeight: 700, color: 'var(--inkt)' }}>{t('ws-title')}</div>
          <p style={{ color: 'var(--grijs)', fontSize: 13, marginTop: 16, lineHeight: 1.6 }}>
            {t('about-text')}
          </p>
          <button
            type="button"
            className="settings-close-btn"
            style={{ marginTop: 14 }}
            onClick={() => setAboutOpen(false)}
          >
            {t('close')}
          </button>
        </div>
      </div>

      <div
        className={`settings-overlay${confirmRestart ? '' : ' hidden'}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="langConfirmOverlayTitle"
      >
        <div className="settings-modal" style={{ maxWidth: 340, textAlign: 'center' }}>
          <h2 id="langConfirmOverlayTitle">Instelling wijzigen?</h2>
          <p style={SOFT_NOTE_STYLE}>
            De puzzel begint opnieuw. Je huidige voortgang gaat verloren.
          </p>
          <div style={HINT_STYLE}>
            <button type="button" style={CONFIRM_BUTTON_STYLE} onClick={cancelTranslation}>
              {t('cancel')}
            </button>
            <button
              type="button"
              style={{
                background: 'var(--oranje)',
                color: 'var(--papier)',
                border: 'none',
                borderRadius: 0,
                padding: '10px 18px',
                cursor: 'pointer',
                fontWeight: 600,
              }}
              onClick={confirmTranslation}
            >
              Opnieuw beginnen
            </button>
          </div>
        </div>
      </div>
    </>
  );

  return (
    <GameShell
      game="wordsearch"
      title={t('ws-title', 'Woordzoeker')}
      splash={t('splash-alt', t('ws-title', 'Woordzoeker'))}
      onSettings={() => setSettingsOpen(true)}
      overlays={overlays}
    >
      <main className="app-container">
        <ResumeNote text={resumed} onDone={() => setResumed(null)} />
        <div className="difficulty-bar" role="group" aria-label="Niveau">
          {levels.map((level) => (
            <button
              key={level.id}
              type="button"
              className={`diff-btn${level.id === (view?.difficulty ?? difficulty) ? ' active' : ''}`}
              aria-pressed={level.id === (view?.difficulty ?? difficulty)}
              disabled={!canFill(level.size)}
              onClick={() => newRound(category, level.id)}
            >
              {level.name}
            </button>
          ))}
        </div>

        <div className="status-row" aria-live="polite" aria-atomic="false">
          <span>
            {t('found-label')} <span id="foundCount">{foundCount}</span> /{' '}
            <span id="totalCount">{words.length}</span>
          </span>
          <span id="timerDisplay">⏱ {formatTime(seconds)}</span>
          <span>
            {t('hints-label')} <span id="hintsLeft">{hintsLeft}</span>
          </span>
          {denied === null ? null : <span role="status">{denied}</span>}
        </div>

        {view === null ? null : (
          <div className="game-layout">
            <div className="grid-panel">
              <div className="grid-wrapper" ref={wrapperRef}>
                <canvas id="selectionCanvas" ref={canvasRef} />
                <div
                  className="grid"
                  id="grid"
                  ref={gridRef}
                  role="grid"
                  aria-label={`Woordrooster ${size} bij ${size}`}
                  style={{
                    gridTemplateColumns: `repeat(${size}, ${cellSize}px)`,
                    gridTemplateRows: `repeat(${size}, ${cellSize}px)`,
                  }}
                  onPointerDown={onPointerDown}
                  onPointerMove={onPointerMove}
                  onPointerUp={onPointerUp}
                  onPointerCancel={onPointerCancel}
                  onContextMenu={(event) => {
                    event.preventDefault();
                    if (selection) clearSelection();
                  }}
                >
                  {view.grid.map((row, r) => row.map((letter, c) => {
                    const key = cellKey(r, c);
                    const isFound = foundSet.has(key);
                    const isStart = selection !== null
                      && selection.start.r === r
                      && selection.start.c === c;
                    const classes = ['cell'];
                    if (isFound) classes.push('found');
                    if (selectionSet.has(key) && !isFound) classes.push(dragging ? 'selecting' : 'selected');
                    if (wrongCells.has(key) && !isFound) classes.push('error');
                    if (hintSet.has(key)) classes.push('hint');
                    if (isStart) classes.push('start-marker');

                    return (
                      <div
                        key={key}
                        className={classes.join(' ')}
                        role="gridcell"
                        aria-label={`Rij ${r + 1}, kolom ${c + 1}, ${letter}`}
                        style={{
                          width: cellSize,
                          height: cellSize,
                          fontSize: fontSizeFor(cellSize),
                        }}
                      >
                        {letter}
                      </div>
                    );
                  }))}
                </div>
              </div>
            </div>

            <div className="word-list-panel" id="wordListPanel">
              <h3>{t('words-title')}</h3>
              <ul className="word-list" id="wordList">
                {words.map((word) => {
                  const isFound = found[word.index] === true;
                  const hasTranslation = Boolean(word.translation);
                  const classes = [];
                  if (isFound) classes.push('found');
                  if (hasTranslation) classes.push('has-translation');
                  if (revealed.has(word.index)) classes.push('revealed');

                  return (
                    <li
                      key={word.index}
                      className={classes.join(' ') || undefined}
                      onClick={() => {
                        if (hasTranslation) toggleRevealed(word.index);
                      }}
                    >
                      {word.imageUrl ? (
                        <WordImage className="word-thumb" src={word.imageUrl} />
                      ) : null}
                      <span className="word-text">{word.text}</span>
                      {hasTranslation ? (
                        <span className="word-translation" lang={settings.translateTo}>
                          {word.translation}
                        </span>
                      ) : null}
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        )}

        {roundError === null ? null : (
          <p className="hint" role="alert">
            {roundError}{' '}
            {expired ? (
              <button type="button" className="ctrl-btn" onClick={() => newRound()}>
                {t('btn-new')}
              </button>
            ) : null}
          </p>
        )}

        <div className="controls-bar">
          <button
            type="button"
            className="ctrl-btn"
            id="btnHint"
            onClick={() => void useHint()}
            disabled={dealing || view === null || view.done || hintsLeft <= 0 || hint !== null}
          >
            {t('btn-hint')} (<span id="hintCount">{hintsLeft}</span>)
          </button>
          <button
            type="button"
            className="ctrl-btn primary"
            onClick={() => {
              setAboutOpen(false);
              setCategoryOpen(true);
            }}
            disabled={dealing}
          >
            {t('btn-new')}
          </button>
        </div>
      </main>
    </GameShell>
  );
}
