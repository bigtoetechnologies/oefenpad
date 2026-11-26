import { Fragment, useCallback, useEffect, useRef, useState } from 'react';
import { api, ApiError, type GameLevel, type LevelResults, type Texts } from '../../api';
import { GameShell } from '../../site/GameShell';
import { ResumeNote } from '../../shared/ResumeNote';
import { useGameData } from '../../shared/useGameData';

/* =================================================================
   Scheidbare werkwoorden — text-first.

   Same two steps as Werkwoorden, but most separable verbs have no
   drawing: a card shows the infinitive, how it splits, its perfect
   and one example; the question asks for the English meaning. The
   server owns the round and the option order; the browser sends the
   position of the chosen option and never sees which one is right.
   ================================================================= */

type StepKind = 'discover' | 'choose';

interface SceneImage {
  id: string;
  url: string;
  alt: string;
}

interface DiscoverContent {
  card: {
    image: SceneImage | null;
    verb: string;
    gloss: string;
    split: string | null;
    perfect: string | null;
    example: string | null;
    exampleEn: string | null;
  };
}

interface ChooseContent {
  verb: string;
  example: string | null;
  options: string[];
}

interface Feedback {
  correct: boolean;
  explanation: string;
  correctOption: number | null;
  chosenOption: number | null;
}

interface ViewBase {
  level: string;
  stepIndex: number;
  item: number;
  count: number;
  steps: StepKind[];
  correct: number;
  total: number;
  phase: 'question' | 'feedback';
  feedback?: Feedback;
}

type View =
  | (ViewBase & { kind: 'discover'; content: DiscoverContent })
  | (ViewBase & { kind: 'choose'; content: ChooseContent });

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

const STEPS: { kind: StepKind; label: string }[] = [
  { kind: 'discover', label: 'step-discover' },
  { kind: 'choose', label: 'step-choose' },
];

function Scene({ image, label }: { image: SceneImage; label?: string }) {
  const [missing, setMissing] = useState(false);

  useEffect(() => setMissing(false), [image.url]);

  return (
    <img
      className="beeld"
      src={image.url || undefined}
      alt={label ?? ''}
      style={missing || image.url === '' ? { visibility: 'hidden' } : undefined}
      onError={() => setMissing(true)}
      aria-hidden={label === undefined ? true : undefined}
    />
  );
}

/** The two stations, with the current one in orange. */
function LevelBar({ texts, kind }: { texts: Texts; kind: StepKind | null }) {
  const at = kind === null ? -1 : STEPS.findIndex((step) => step.kind === kind);

  return (
    <ol className="stoppen" aria-label="Stappen">
      {STEPS.map((step, index) => {
        const state = kind === null ? undefined : index < at ? 'geweest' : index === at ? 'nu' : undefined;
        return (
          <li key={step.kind} data-staat={state} aria-current={state === 'nu' ? 'step' : undefined}>
            {texts[step.label]}
          </li>
        );
      })}
    </ol>
  );
}

/**
 * The feedback sheet. On a narrow screen it sits over the bottom of the
 * step, so tell the step how much it covers; otherwise the picture and
 * the question disappear behind it.
 */
function FeedbackBlock({
  feedback,
  last,
  texts,
  disabled,
  onNext,
}: {
  feedback: Feedback;
  last: boolean;
  texts: Texts;
  disabled: boolean;
  onNext: () => void;
}) {
  const panel = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = panel.current;
    const vlak = element?.closest<HTMLElement>('.vlak') ?? null;
    if (element === null || vlak === null) return;

    const measure = () => {
      if (getComputedStyle(element).position !== 'fixed') {
        vlak.style.removeProperty('--terug-hoogte');
        return;
      }
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

  return (
    <div ref={panel} className={`terug ${feedback.correct ? 'goed' : 'fout'}`}>
      <div>{feedback.explanation}</div>
      <div className="verder">
        <button type="button" className="knop" disabled={disabled} onClick={onNext}>
          {last ? texts['done'] : texts['next']}
        </button>
      </div>
    </div>
  );
}

function renderStep(
  view: View,
  texts: Texts,
  send: (move: Record<string, unknown>) => Promise<void>,
  sending: boolean,
) {
  const counter = <span className="teller">{`${view.item + 1} / ${view.count}`}</span>;

  if (view.kind === 'discover') {
    const card = view.content.card;
    const last = view.item === view.count - 1;

    return (
      <div className={`vlak${card.image ? '' : ' vlak--tekst'}`}>
        {card.image ? (
          <div className="beeldvak">
            <Scene image={card.image} label={card.image.alt || undefined} />
          </div>
        ) : null}
        <div className="tekst">
          <p className="uitleg">{texts['discover-hint']}</p>
          <p className="zin">{card.verb}</p>
          <p className="betekenis" lang="en">{card.gloss}</p>
          <dl className="vormen" lang="nl">
            {card.split ? (
              <div>
                <dt>{texts['split-label']}</dt>
                <dd>{card.split}</dd>
              </div>
            ) : null}
            {card.perfect ? (
              <div>
                <dt>{texts['perfect-label']}</dt>
                <dd>{card.perfect}</dd>
              </div>
            ) : null}
          </dl>
          {card.example ? (
            <p className="voorbeeld" lang="nl">
              {card.example}
              {card.exampleEn ? <span className="voorbeeld-en" lang="en">{card.exampleEn}</span> : null}
            </p>
          ) : null}
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

  const content = view.content;
  const feedback = view.feedback;
  const last = view.stepIndex === view.steps.length - 1 && view.item === view.count - 1;

  return (
    <div className={`vlak vlak--tekst vlak--keuze${view.phase === 'feedback' ? ' vlak--na' : ''}`}>
      <div className="tekst">
        <p className="uitleg">{texts['question']}</p>
        <p className="zin">{content.verb}</p>
        {content.example ? <p className="voorbeeld" lang="nl">{content.example}</p> : null}
        <div className="opties" role="group" aria-label={texts['gloss-label']}>
          {content.options.map((option, index) => {
            let state = '';
            if (view.phase === 'feedback' && feedback) {
              if (index === feedback.correctOption) state = ' goed';
              else if (index === feedback.chosenOption) state = ' fout';
            }
            return (
              <button
                key={option}
                type="button"
                className={`keuze-knop${state}`}
                lang="en"
                disabled={view.phase === 'feedback' || sending}
                onClick={() => void send({ action: 'choose', option: index })}
              >
                {option}
              </button>
            );
          })}
        </div>
        {feedback === undefined ? null : (
          <FeedbackBlock
            key={`choose-${view.item}`}
            feedback={feedback}
            last={last}
            texts={texts}
            disabled={sending}
            onNext={() => void send({ action: 'next' })}
          />
        )}
      </div>
      <div className="verder">{counter}</div>
    </div>
  );
}

export function SeparableGame() {
  const { texts, options, error } = useGameData('separable');

  useEffect(() => {
    if (texts?.['page-title']) document.title = texts['page-title'];
  }, [texts]);

  const [view, setView] = useState<View | null>(null);
  const [finished, setFinished] = useState<Score | null>(null);
  const [levelId, setLevelId] = useState<string | null>(null);
  const [roundError, setRoundError] = useState<string | null>(null);
  const [resumed, setResumed] = useState<string | null>(null);
  const [progress, setProgress] = useState<LevelResults>({});
  const [starting, setStarting] = useState(false);
  const [sending, setSending] = useState(false);

  const levelRef = useRef<string | null>(null);
  const roundRef = useRef<string | null>(null);
  const sendingRef = useRef(false);

  const rememberLevel = useCallback((id: string | null) => {
    levelRef.current = id;
    setLevelId(id);
  }, []);

  const restoreRound = useCallback((next: View) => setView(next), []);

  const loadProgress = useCallback(async () => {
    try {
      setProgress(await api.progress('separable'));
    } catch {
      // Progress is a convenience; a failed read must not block the sets.
    }
  }, []);

  useEffect(() => {
    void loadProgress();
  }, [loadProgress]);

  const start = useCallback(
    async (wanted: string) => {
      setStarting(true);
      setRoundError(null);
      setFinished(null);
      setView(null);
      rememberLevel(wanted);
      setResumed(null);

      try {
        const round = await api.start<View>('separable', { level: wanted });
        roundRef.current = round.roundId;
        restoreRound(round.view);
      } catch (cause) {
        roundRef.current = null;
        setRoundError(cause instanceof ApiError ? cause.message : 'De oefening is even niet bereikbaar.');
      } finally {
        setStarting(false);
      }
    },
    [rememberLevel, restoreRound],
  );

  const resumedOnce = useRef(false);
  useEffect(() => {
    if (resumedOnce.current || texts === null) return;
    resumedOnce.current = true;

    void (async () => {
      const saved = await api.saved<View>('separable').catch(() => null);
      if (saved === null) return;
      if (levelRef.current !== null) return;

      roundRef.current = saved.roundId;
      rememberLevel(saved.view.level);
      restoreRound(saved.view);
      setResumed(texts['resumed'] ?? null);
    })();
  }, [texts, rememberLevel, restoreRound]);

  const send = useCallback(
    async (move: Record<string, unknown>) => {
      const id = roundRef.current;
      if (id === null || sendingRef.current) return;
      sendingRef.current = true;
      setSending(true);
      setRoundError(null);

      try {
        const result = await api.move<View | FinishedView>('separable', id, move);
        if ('done' in result.view) {
          roundRef.current = null;
          setFinished({ correct: result.view.correct, total: result.view.total });
          setView(null);
          void loadProgress();
          return;
        }
        if (result.rejection !== null) {
          setRoundError(result.rejection);
          return;
        }
        restoreRound(result.view);
      } catch (cause) {
        if (cause instanceof ApiError) {
          if (cause.status === 410) {
            roundRef.current = null;
            setView(null);
          }
          setRoundError(cause.message);
        } else {
          setRoundError('De oefening is even niet bereikbaar.');
        }
      } finally {
        sendingRef.current = false;
        setSending(false);
      }
    },
    [loadProgress, restoreRound],
  );

  const toLevels = useCallback(() => {
    roundRef.current = null;
    setView(null);
    setFinished(null);
    rememberLevel(null);
    setRoundError(null);
  }, [rememberLevel]);

  const restart = useCallback(() => {
    if (levelId !== null) void start(levelId);
  }, [levelId, start]);

  let body;

  if (error !== null || roundError !== null || (texts === null && error === null)) {
    const message = error ?? roundError;
    body = (
      <main className="app-container" aria-live="polite">
        <p className="vraag" tabIndex={-1}>{message ?? 'Even laden…'}</p>
        {levelId === null ? null : (
          <div className="verder">
            <button type="button" className="knop" onClick={restart} disabled={starting}>
              {texts?.['again'] ?? 'Nog een keer'}
            </button>
            <button type="button" className="knop leeg" onClick={toLevels}>
              {texts?.['other-level'] ?? 'Ander niveau'}
            </button>
          </div>
        )}
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
        <LevelBar texts={texts} kind={null} />
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
      </main>
    );
  } else if (view === null) {
    const mainLevels = options.levels.filter((level) => level.band !== 'a0');
    const basisLevels = options.levels.filter((level) => level.band === 'a0');

    const rows = (list: GameLevel[]) => list.map((level, index) => {
      const done = progress[level.id];
      const band = level.band;
      const startsBand = Boolean(band)
        && (index === 0 || list[index - 1].band !== band);

      return (
        <Fragment key={level.id}>
          {startsBand ? <p className="band-kop">{band!.toUpperCase()}</p> : null}
          <button
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
        </Fragment>
      );
    });

    body = (
      <main className="app-container">
        <LevelBar texts={texts} kind={null} />
        <p className="vraag">{texts['choose-level']}</p>
        <p className="uitleg">{texts['choose-level-hint']}</p>
        <div className="niveaus">{rows(mainLevels)}</div>
        {basisLevels.length === 0 ? null : (
          <details className="basis">
            <summary>{texts['basis-title']}</summary>
            <p className="uitleg">{texts['basis-hint']}</p>
            <div className="niveaus">{rows(basisLevels)}</div>
          </details>
        )}
      </main>
    );
  } else {
    const speech = view.phase === 'feedback' && view.feedback
      ? view.feedback.explanation
      : view.kind === 'discover'
        ? `${view.content.card.verb}. ${texts['discover-hint']}`
        : `${texts['question']} ${view.content.verb}`;

    body = (
      <main className="app-container">
        <ResumeNote text={resumed} onDone={() => setResumed(null)} />
        <LevelBar texts={texts} kind={view.kind} />
        <div className="scherm">
          {renderStep(view, texts, send, sending)}
        </div>
        <p className="alleen-lezer" aria-live="polite">{speech}</p>
      </main>
    );
  }

  return (
    <GameShell
      game="separable"
      title={texts?.['title'] ?? ''}
      tagline={texts?.['tagline']}
      splash={texts?.['splash']}
      onBegin={view === null ? undefined : toLevels}
      beginLabel={texts?.['to-levels']}
    >
      {body}
    </GameShell>
  );
}
