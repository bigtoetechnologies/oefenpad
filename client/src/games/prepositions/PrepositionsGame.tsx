import { useCallback, useEffect, useLayoutEffect, useRef, useState, type CSSProperties } from 'react';
import { api, ApiError, fill, type GameLevel, type LevelResults, type Texts } from '../../api';
import { GameShell } from '../../site/GameShell';
import { ResumeNote } from '../../shared/ResumeNote';
import { useGameData } from '../../shared/useGameData';

/* =================================================================
   Voorzetselpaden, rendered from the server's view.

   A round is a sequence of steps (discover, choose, trueFalse,
   build). The server owns the step machine, the contrast partner and
   the tile order; the client keeps only the view it was handed plus
   the tiles the player has picked for the build step.
   ================================================================= */

type StepKind = 'discover' | 'choose' | 'trueFalse' | 'build';
type Phase = 'question' | 'feedback';

interface SceneImage {
  id: string;
  url: string;
  alt: string;
}

interface DiscoverContent {
  card: {
    image: SceneImage;
    sentence: string;
    focus: string[];
    meaning: string;
    form: string | null;
    notice: string | null;
  };
}

interface ChooseContent {
  sentence: string;
  focus: string[];
  options: SceneImage[];
}

interface TrueFalseContent {
  image: SceneImage;
  sentence: string;
  focus: string[];
}

interface BuildContent {
  frame: string;
  hint: string;
  image: SceneImage;
  tiles: { id: string; text: string }[];
}

type Content = DiscoverContent & ChooseContent & TrueFalseContent & BuildContent;

interface ConceptFeedback {
  question: string;
  answer: boolean | null;
  explanation: string | null;
}

interface Feedback {
  correct: boolean;
  explanation: string;
  correctScene: string | null;
  chosenScene: string | null;
  expected: boolean | null;
  chosen: boolean | null;
  target: string | null;
  concept: ConceptFeedback | null;
}

interface View {
  kind: StepKind;
  level: string;
  stepIndex: number;
  item: number;
  count: number;
  steps: StepKind[];
  correct: number;
  total: number;
  phase: Phase;
  content: Content;
  feedback?: Feedback;
}

interface FinishedView {
  done: true;
  correct: number;
  total: number;
  level: string;
}

interface Score {
  correct: number;
  total: number;
}

const STEP_KEYS: { kind: StepKind; label: string }[] = [
  { kind: 'discover', label: 'step-discover' },
  { kind: 'choose', label: 'step-choose' },
  { kind: 'trueFalse', label: 'step-truefalse' },
  { kind: 'build', label: 'step-build' },
];

/** Words the underline marks: the preposition chunk of the sentence. */
function Sentence({ nl, focus }: { nl: string; focus: string[] }) {
  return (
    <>
      {nl.split(' ').map((word, index) => {
        const bare = word.replace(/[.,!?]+$/, '').toLowerCase();
        const chunk = focus.includes(bare);
        return (
          <span key={index}>
            {index ? ' ' : null}
            {chunk ? <span className="chunk">{word}</span> : word}
          </span>
        );
      })}
    </>
  );
}

/**
 * The drawing: a cobalt block masked by the brush-painted scene. The
 * image itself shows through the --beeld variable, so a hidden picture
 * must also stop painting that variable.
 */
function Scene({ image, label, className }: { image: SceneImage; label?: string; className?: string }) {
  const [missing, setMissing] = useState(false);
  const probe = useRef<HTMLImageElement>(null);

  // The probe has no layout, so it never shows up; it only reports whether
  // the file is there. Cached loads fire before React's onLoad is attached.
  // Re-runs on every new file: the step keeps one Scene instance across its
  // items, so a single 404 would otherwise blank every later drawing too.
  useEffect(() => {
    setMissing(false);
    const element = probe.current;
    if (element && element.complete && element.naturalWidth === 0) setMissing(true);
  }, [image.url]);

  return (
    <div
      className={className === undefined ? 'beeld' : `beeld ${className}`}
      style={
        missing || image.url === ''
          ? { '--beeld': 'none' } as CSSProperties
          : { '--beeld': `url("${image.url}")` } as CSSProperties
      }
      role={label === undefined ? undefined : 'img'}
      aria-label={label}
      aria-hidden={label === undefined ? true : undefined}
    >
      <img
        ref={probe}
        src={image.url}
        alt=""
        style={{ display: 'none' }}
        onError={() => setMissing(true)}
      />
    </div>
  );
}

export function PrepositionsGame() {
  const { texts, options, error } = useGameData('prepositions');

  useEffect(() => {
    if (texts?.['page-title']) document.title = texts['page-title'];
  }, [texts]);

  const [view, setView] = useState<View | null>(null);
  const [finished, setFinished] = useState<Score | null>(null);
  const [levelId, setLevelId] = useState<string | null>(null);
  /* Mirrors levelId for the resume request, which resolves outside render and
     needs to know whether the player has chosen in the meantime. */
  const levelRef = useRef<string | null>(null);
  const rememberLevel = useCallback((id: string | null) => {
    levelRef.current = id;
    setLevelId(id);
  }, []);
  // Only the setter is read: roundRef carries the live id, and the render
  // decides on levelId so a transient error still offers a way back.
  const [, setRoundId] = useState<string | null>(null);
  const [roundError, setRoundError] = useState<string | null>(null);
  const [resumed, setResumed] = useState<string | null>(null);
  const [progress, setProgress] = useState<LevelResults>({});
  const [starting, setStarting] = useState(false);
  const [sending, setSending] = useState(false);
  const [placed, setPlaced] = useState<string[]>([]);

  // One move at a time: the ref blocks a double tap before React has
  // re-rendered, and it holds the round id so a stale closure cannot
  // post to a round that has already been replaced.
  const sendingRef = useRef(false);
  const roundRef = useRef<string | null>(null);
  // Moves that must land in order: when one is in flight, the next waits
  // here instead of being dropped (a level end posts `next` and `start`).
  const queue = useRef<Promise<void>>(Promise.resolve());
  const timers = useRef<number[]>([]);

  useEffect(() => () => {
    timers.current.forEach((id) => window.clearTimeout(id));
  }, []);

  const later = useCallback((action: () => void, ms: number) => {
    timers.current.push(window.setTimeout(action, ms));
  }, []);

  const t = useCallback(
    (key: string) => fill(texts?.[key] ?? key),
    [texts],
  );

  const focusStep = useCallback(() => {
    const target =
      document.querySelector<HTMLElement>('.game--prepositions .vraag')
      ?? document.querySelector<HTMLElement>('.game--prepositions .niveaus .niveau')
      ?? document.querySelector<HTMLElement>('.game--prepositions .klaar');
    target?.focus({ preventScroll: false });
  }, []);

  /* ---------- rounds ---------- */

  const restoreRound = useCallback((next: View, keepPlaced = false) => {
    setView(next);
    // A checked build row is judged in place, so its tiles stay put; any
    // other move starts the next item with an empty row.
    if (!keepPlaced) setPlaced([]);
    // The build row is only rebuilt when the item changes.
    later(focusStep, 30);
  }, [focusStep, later]);

  const start = useCallback(
    async (wanted: string) => {
      setStarting(true);
      setRoundError(null);
      setFinished(null);
      setView(null);
      setPlaced([]);
      rememberLevel(wanted);
      setResumed(null);

      const run = queue.current.then(async () => {
        try {
          const round = await api.start<View>('prepositions', { level: wanted });
          roundRef.current = round.roundId;
          setRoundId(round.roundId);
          restoreRound(round.view);
        } catch (cause) {
          roundRef.current = null;
          setRoundId(null);
          setRoundError(cause instanceof ApiError ? cause.message : t('error'));
        } finally {
          setStarting(false);
        }
      });
      queue.current = run;
      await run;
    },
    [restoreRound, rememberLevel, t],
  );

  const expire = useCallback(() => {
    roundRef.current = null;
    setRoundId(null);
    setView(null);
    setFinished(null);
    setPlaced([]);
  }, []);

  /* ---------- progress ---------- */

  const loadProgress = useCallback(async () => {
    try {
      setProgress(await api.progress('prepositions'));
    } catch {
      // Progress is a convenience; a failed read must not block the level list.
    }
  }, []);

  useEffect(() => {
    void loadProgress();
  }, [loadProgress]);

  // A round left mid-level is picked up before the level list is shown.
  const resumedOnce = useRef(false);
  useEffect(() => {
    if (resumedOnce.current || texts === null) return;
    resumedOnce.current = true;

    void (async () => {
      const saved = await api.saved<View>('prepositions').catch(() => null);
      if (saved === null) return;
      // The level list is live while this request runs. A player who has
      // already picked a level must not be dragged back into the old round.
      if (levelRef.current !== null) return;

      roundRef.current = saved.roundId;
      setRoundId(saved.roundId);
      rememberLevel(saved.view.level);
      restoreRound(saved.view);
      setResumed(texts['resumed'] ?? null);
    })();
  }, [texts, restoreRound, rememberLevel]);

  const send = useCallback(
    async (move: Record<string, unknown>) => {
      const id = roundRef.current;
      if (id === null || sendingRef.current) return;
      sendingRef.current = true;
      setSending(true);
      setRoundError(null);

      try {
        const result = await api.move<View | FinishedView>('prepositions', id, move);
        if ('done' in result.view) {
          roundRef.current = null;
          setRoundId(null);
          setFinished({ correct: result.view.correct, total: result.view.total });
          setView(null);
          setPlaced([]);
          void loadProgress();
          later(focusStep, 30);
          return;
        }
        if (result.rejection !== null) {
          setRoundError(result.rejection);
          return;
        }
        restoreRound(result.view, move.action === 'build');
      } catch (cause) {
        if (cause instanceof ApiError && cause.status === 410) {
          expire();
          setRoundError(cause.message);
        } else if (cause instanceof ApiError) {
          setRoundError(cause.message);
        } else {
          setRoundError(t('error'));
        }
      } finally {
        sendingRef.current = false;
        setSending(false);
      }
    },
    [restoreRound, expire, focusStep, later, t, loadProgress],
  );

  /* ---------- level list and end screen ---------- */

  const levels: GameLevel[] = options?.levels ?? [];

  const restart = useCallback(() => {
    if (levelId !== null) void start(levelId);
  }, [levelId, start]);

  const toLevels = useCallback(() => {
    roundRef.current = null;
    setRoundId(null);
    setView(null);
    setFinished(null);
    rememberLevel(null);
    setPlaced([]);
    setRoundError(null);
  }, []);

  /* ---------- body ---------- */

  let body;

  if (error !== null || roundError !== null || (texts === null && error === null)) {
    const message = error ?? roundError;
    body = (
      <main className="app-container" aria-live="polite">
        <p className="vraag" tabIndex={-1}>
          {message ?? 'Even laden…'}
        </p>
        {levelId !== null ? (
          <div className="verder">
            <button type="button" className="knop" onClick={restart} disabled={starting}>
              {t('again')}
            </button>
            <button type="button" className="knop leeg" onClick={toLevels}>
              {t('other-level')}
            </button>
          </div>
        ) : null}
      </main>
    );
  } else if (texts === null || options === null) {
    body = (
      <main className="app-container" aria-live="polite">
        <p className="vraag">Even laden…</p>
      </main>
    );
  } else if (finished !== null) {
    body = (
      <main className="app-container">
        <LevelBar texts={texts} active={null} steps={[]} />
        <div className="klaar">
          <div className="score" tabIndex={-1}>{`${finished.correct} / ${finished.total}`}</div>
          <p className="van">{texts['score-word']}</p>
          <button type="button" className="knop" onClick={restart} disabled={starting}>
            {texts['again']}
          </button>
          <button type="button" className="knop leeg" style={{ marginTop: 10 }} onClick={toLevels}>
            {texts['other-level']}
          </button>
        </div>
        <p className="alleen-lezer" aria-live="polite">
          {`${texts['done']}. ${finished.correct} / ${finished.total} ${texts['score-word']}.`}
        </p>
      </main>
    );
  } else if (view === null) {
    body = (
      <main className="app-container">
        <LevelBar texts={texts} active={null} steps={[]} />
        <p className="vraag">{texts['choose-level']}</p>
        <p className="uitleg">{texts['choose-level-hint']}</p>
        <div className="niveaus">
          {levels.map((level, index) => {
            const done = progress[level.id];
            if (level.locked) {
              const reason = level.lockReason === 'premium'
                ? t('locked-premium')
                : level.lockReason === 'progress'
                  ? t('locked-progress')
                  : t('locked-account');
              return (
                <div
                  key={level.id}
                  className="niveau is-dicht"
                  aria-disabled="true"
                >
                  <span className="nr">{index + 1}</span>
                  <span className="wat">
                    {level.name}
                    <span className="onder">{reason}</span>
                  </span>
                  <span className="slot" aria-hidden="true">🔒</span>
                  {level.lockReason === 'account' ? (
                    <a className="dicht-link" href="/Account/Registreren">
                      {t('register')}
                    </a>
                  ) : null}
                </div>
              );
            }
            return (
              <button
                key={level.id}
                type="button"
                className="niveau"
                disabled={starting}
                onClick={() => void start(level.id)}
              >
                <span className="nr">{index + 1}</span>
                <span className="wat">
                  {level.name}
                  <span className="onder">{level.subtitle ?? ''}</span>
                </span>
                {done === undefined ? null : (
                  <span className="gehaald">{`✓ ${done.correct}/${done.total}`}</span>
                )}
              </button>
            );
          })}
        </div>
        <p className="alleen-lezer" aria-live="polite">{texts['choose-level']}</p>
      </main>
    );
  } else {
    body = (
      <main className="app-container">
        <ResumeNote text={resumed} onDone={() => setResumed(null)} />
        <LevelBar texts={texts} active={view} steps={view.steps} />
        <div className="scherm">
          {renderStep(view, texts, placed, setPlaced, send, sending)}
        </div>
        <p className="alleen-lezer" aria-live="polite">
          {view.phase === 'feedback' && view.feedback
            ? feedbackSpeech(view.feedback)
            : spokenSentence(view, texts)}
        </p>
      </main>
    );
  }

  return (
    <GameShell
      game="prepositions"
      title={texts?.['title'] ?? ''}
      tagline={texts?.['tagline']}
    >
      {body}
    </GameShell>
  );
}

/** The four stations, greyed unless the level reaches them. */
function LevelBar({ texts, active, steps }: { texts: Texts; active: View | null; steps: StepKind[] }) {
  let walked = false;
  const states = STEP_KEYS.map(({ kind }) => {
    if (steps.length > 0 && !steps.includes(kind)) return 'skipped';
    if (active !== null && kind === active.kind) {
      walked = true;
      return 'now';
    }
    if (walked) return 'todo';
    if (active !== null) return 'done';
    return 'todo';
  });

  return (
    <ol className="stoppen" aria-label="Stappen">
      {STEP_KEYS.map(({ kind, label }, index) => (
        <li
          key={kind}
          aria-current={states[index] === 'now' ? 'step' : undefined}
          hidden={states[index] === 'skipped'}
          {...(states[index] === 'done'
            ? { 'data-staat': 'geweest' }
            : states[index] === 'now'
              ? { 'data-staat': 'nu' }
              : {})}
        >
          <span lang="nl">{texts[label] ?? ''}</span>
        </li>
      ))}
    </ol>
  );
}

/** What the screen reader hears before an answer: the Dutch prompt line. */
function spokenSentence(view: View, texts: Texts): string {
  const content = view.content;
  switch (view.kind) {
    case 'discover':
      return content.card.sentence;
    case 'choose':
      return `${texts['which-image']} ${content.sentence}`;
    case 'trueFalse':
      return `${texts['sentence-fits']} ${content.sentence}`;
    case 'build':
      return content.hint;
  }
}

function feedbackSpeech(feedback: Feedback): string {
  if (feedback.concept === null) return feedback.explanation;
  return [feedback.explanation, feedback.concept.question, feedback.concept.explanation]
    .filter((part): part is string => part !== null && part !== '')
    .join(' ');
}

function renderStep(
  view: View,
  texts: Texts,
  placed: string[],
  setPlaced: (next: string[]) => void,
  send: (move: Record<string, unknown>) => Promise<void>,
  sending: boolean,
) {
  const counter = (
    <span className="teller">{`${view.item + 1} / ${view.count}`}</span>
  );

  const back = view.phase === 'feedback' && view.feedback ? (
    <FeedbackBlock
      // Stable per item, so answering the concept question does not remount
      // the block and pull focus off the button the player just pressed.
      key={`${view.kind}-${view.item}`}
      feedback={view.feedback}
      last={view.stepIndex === view.steps.length - 1 && view.item === view.count - 1}
      texts={texts}
      disabled={sending}
      onNext={() => void send({ action: 'next' })}
      onConcept={(answer) => void send({ action: 'concept', answer })}
    />
  ) : null;

  switch (view.kind) {
    case 'discover': {
      const card = view.content.card;
      const last = view.item === view.count - 1;
      return (
        <div className="vlak">
          <div className="beeldvak">
            <Scene image={card.image} label={card.image.alt || undefined} />
          </div>
          <div className="tekst">
            <p className="zin">
              <Sentence nl={card.sentence} focus={card.focus} />
            </p>
            <p className="betekenis" lang="en">{card.meaning}</p>
            {card.form === null ? null : (
              <p className="vorm" lang="nl">{card.form}</p>
            )}
            {card.notice === null ? null : (
              <p className="vorm" lang="nl">{card.notice}</p>
            )}
          </div>
          <div className="verder">
            {counter}
            <button
              type="button"
              className="knop"
              disabled={sending}
              onClick={() => void send({ action: 'next' })}
            >
              {last ? texts['start-practice'] : texts['next']}
            </button>
          </div>
        </div>
      );
    }

    case 'choose': {
      const content = view.content;
      const feedback = view.feedback;
      return (
        <div className={`vlak vlak--keuze${view.phase === 'feedback' ? ' vlak--na' : ''}`}>
          <div className="tekst">
            <p className="uitleg">{texts['which-image']}</p>
            <p className="kloptzin">
              <Sentence nl={content.sentence} focus={content.focus} />
            </p>
            {back}
          </div>
          <div className="keuzes">
            {content.options.map((option, index) => {
              let state = '';
              if (view.phase === 'feedback' && feedback) {
                if (option.id === feedback.correctScene) state = ' goed';
                else if (option.id === feedback.chosenScene) state = ' fout';
              }
              return (
                <button
                  key={option.id}
                  type="button"
                  className={`keuze${state}`}
                  data-scene={option.id}
                  aria-label={`Beeld ${index + 1}`}
                  disabled={view.phase === 'feedback' || sending}
                  onClick={() => void send({ action: 'choose', scene: option.id })}
                >
                  <Scene image={option} />
                </button>
              );
            })}
          </div>
          <div className="verder">{counter}</div>
        </div>
      );
    }

    case 'trueFalse': {
      const content = view.content;
      const feedback = view.feedback;
      const truth = feedback?.expected ?? null;
      return (
        <div className={`vlak${view.phase === 'feedback' ? ' vlak--na' : ''}`}>
          <div className="beeldvak">
            <Scene image={content.image} label={content.image.alt || undefined} />
          </div>
          <div className="tekst">
            <p className="uitleg">{texts['sentence-fits']}</p>
            <p className="kloptzin">
              <Sentence nl={content.sentence} focus={content.focus} />
            </p>
            <div className="tweeknoppen">
              {([true, false] as const).map((value) => {
                let state = '';
                if (truth === value) state = ' goed';
                else if (feedback?.chosen === value) state = ' fout';
                return (
                  <button
                    key={String(value)}
                    type="button"
                    className={`keuze-knop${state}`}
                    disabled={view.phase === 'feedback' || sending}
                    onClick={() => void send({ action: 'trueFalse', answer: value })}
                  >
                    {value ? texts['true'] : texts['false']}
                  </button>
                );
              })}
            </div>
            {back}
          </div>
          <div className="verder">{counter}</div>
        </div>
      );
    }

    case 'build': {
      const content = view.content;
      const checked = view.phase === 'feedback';
      const locked = checked || sending;
      const used = new Set(placed);
      const complete = placed.length === content.tiles.length;
      // Checked, the feedback block owns the only way forward.
      const rowState = checked ? (view.feedback?.correct ? 'rij goed' : 'rij fout') : 'rij';
      const return_ = checked
        ? null
        : (
          <button
            type="button"
            className="knop"
            disabled={locked || !complete}
            onClick={() => void send({ action: 'build', tiles: placed })}
          >
            {texts['check']}
          </button>
        );

      return (
        <div className={`vlak${checked ? ' vlak--na' : ''}`}>
          <div className="beeldvak">
            <Scene image={content.image} className="bouwbeeld" label={content.image.alt || undefined} />
          </div>
          <div className="tekst">
            <p className="vraag" tabIndex={-1}>{texts['build-question']}</p>
            <p className="uitleg">{content.hint}</p>
            {placed.length === 0 ? (
              <div className="rij leeg">{texts['build-instruction']}</div>
            ) : (
              <div className={rowState}>
                {placed.map((id, position) => (
                  <button
                    key={id}
                    type="button"
                    className="tegel geplaatst"
                    disabled={locked}
                    onClick={() => setPlaced(placed.filter((_, at) => at !== position))}
                  >
                    {content.tiles.find((tile) => tile.id === id)?.text ?? ''}
                  </button>
                ))}
                <span className="punt">.</span>
              </div>
            )}
            <div className="pool">
              {content.tiles.map((tile) => {
                const taken = used.has(tile.id);
                return (
                  <button
                    key={tile.id}
                    type="button"
                    className={taken || checked ? 'tegel vast' : 'tegel'}
                    disabled={taken || locked}
                    onClick={() => setPlaced([...placed, tile.id])}
                  >
                    {tile.text}
                  </button>
                );
              })}
            </div>
            {back}
          </div>
          <div className="verder">
            {counter}
            {return_}
          </div>
        </div>
      );
    }
  }
}

/**
 * The answer block. The concept question sits inside it: it asks about
 * meaning, is never scored, and only exists when the server sent one.
 */
function FeedbackBlock({
  feedback,
  last,
  texts,
  disabled,
  onNext,
  onConcept,
}: {
  feedback: Feedback;
  last: boolean;
  texts: Texts;
  disabled: boolean;
  onNext: () => void;
  onConcept: (answer: boolean) => void;
}) {
  const concept = feedback.concept;
  const answered = concept === null || concept.answer !== null;
  const nextButton = useRef<HTMLButtonElement>(null);
  const panel = useRef<HTMLDivElement>(null);

  // On a narrow screen the panel covers the bottom of the step. Tell the
  // step how much of itself is covered, so the drawing and the sentence
  // move up instead of disappearing behind it. The panel grows when the
  // concept question arrives, hence the observer rather than one
  // measurement.
  useLayoutEffect(() => {
    const element = panel.current;
    const vlak = element?.closest<HTMLElement>('.vlak') ?? null;
    if (element === null || vlak === null) return;

    const measure = () => {
      if (getComputedStyle(element).position !== 'fixed') {
        vlak.style.removeProperty('--terug-hoogte');
        return;
      }
      // offsetHeight ignores the slide-in transform, which a rect would not.
      const top = window.innerHeight - element.offsetHeight;
      const covered = Math.max(0, Math.round(vlak.getBoundingClientRect().bottom - top));
      vlak.style.setProperty('--terug-hoogte', `${covered}px`);
    };
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    window.addEventListener('resize', measure);
    return () => {
      observer.disconnect();
      window.removeEventListener('resize', measure);
      vlak.style.removeProperty('--terug-hoogte');
    };
  }, []);

  // Answering the concept question reveals the only way forward, so hand
  // the keyboard to it rather than leaving focus on a dead button.
  const wanted = concept !== null && concept.answer !== null;
  useEffect(() => {
    if (wanted) nextButton.current?.focus({ preventScroll: true });
  }, [wanted]);

  return (
    <div ref={panel} className={`terug ${feedback.correct ? 'goed' : 'fout'}`}>
      <div>{feedback.explanation}</div>
      {concept === null ? null : (
        <span className="concept">
          {concept.question}
          <div className="concept-rij">
            {([true, false] as const).map((value) => {
              let state = '';
              if (concept.answer !== null) {
                if (concept.answer === value) state = ' goed';
                else state = ' fout';
              }
              return (
                <button
                  key={String(value)}
                  type="button"
                  className={state.trim() === '' ? undefined : state.trim()}
                  disabled={concept.answer !== null || disabled}
                  onClick={() => onConcept(value)}
                >
                  {value ? texts['yes'] : texts['no']}
                </button>
              );
            })}
          </div>
          {concept.explanation === null ? null : (
            <span className="concept">{concept.explanation}</span>
          )}
        </span>
      )}
      {answered ? (
        <div className="verder">
          <button ref={nextButton} type="button" className="knop" disabled={disabled} onClick={onNext}>
            {last ? texts['done'] : texts['next']}
          </button>
        </div>
      ) : null}
    </div>
  );
}
