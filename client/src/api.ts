/* =================================================================
   api.ts — the only way the browser talks to the games backend.

   Each game gets a round, renders the view it was handed, and posts
   actions back. There is no endpoint that returns a word bank, a
   solution or a full data file.
   ================================================================= */

export interface GameCategory {
  id: string;
  name: string;
  icon: string;
  count: number;
}

export interface GameLevel {
  id: string;
  name: string;
  size: number | null;
  subtitle: string | null;
  /** The visitor may not start this level yet. */
  locked: boolean;
  /** Why, when it is locked: an account, the previous level, or a paid plan. */
  lockReason: 'account' | 'progress' | 'premium' | null;
}

export interface GameOptions {
  categories: GameCategory[];
  levels: GameLevel[];
}

export type Texts = Record<string, string>;

export interface Round<View> {
  roundId: string;
  view: View;
}

export interface MoveResult<View> {
  view: View;
  done: boolean;
  correct: boolean | null;
  explanation: string | null;
  correctCount: number | null;
  total: number | null;
  rejection: string | null;
}

/** A round the account saved earlier, plus the little a resume needs to redraw. */
export interface SavedRound<View, Extra = unknown> {
  roundId: string;
  view: View;
  resume: Extra | null;
}

/** A finished level's best score. */
export interface LevelProgress {
  correct: number;
  total: number;
}

export type LevelResults = Record<string, LevelProgress>;

/** A failed call the player can recover from. */
export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const BASE = '/api/games';

const GONE = 'Deze ronde bestaat niet meer. Start een nieuw spel.';
const OFFLINE = 'De oefening is even niet bereikbaar. Probeer het opnieuw.';

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(url, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers ?? {}),
      },
    });
  } catch {
    throw new ApiError(0, OFFLINE);
  }

  if (response.status === 410) throw new ApiError(410, GONE);

  if (!response.ok) {
    let message = OFFLINE;
    try {
      const body = (await response.json()) as { error?: string };
      if (body.error) message = body.error;
    } catch {
      /* the server answered with no JSON; keep the generic message */
    }
    if (response.status === 429) message = 'Te veel vragen achter elkaar. Wacht even.';
    throw new ApiError(response.status, message);
  }

  return (await response.json()) as T;
}

export const api = {
  options(game: string): Promise<GameOptions> {
    return request<GameOptions>(`${BASE}/${game}/options`);
  },

  texts(game: string): Promise<Texts> {
    return request<Texts>(`${BASE}/${game}/texts`);
  },

  start<View>(game: string, body: unknown = {}): Promise<Round<View>> {
    return request<Round<View>>(`${BASE}/${game}/rounds`, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },

  move<View>(game: string, roundId: string, body: unknown): Promise<MoveResult<View>> {
    return request<MoveResult<View>>(`${BASE}/${game}/rounds/${roundId}/moves`, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },

  /**
   * The round the signed-in player left behind, or null when there is none.
   * A guest always gets null, so the game starts fresh the same way.
   */
  async saved<View, Extra = unknown>(game: string): Promise<SavedRound<View, Extra> | null> {
    const answer = await request<{
      saved: boolean;
      roundId?: string;
      view?: View;
      resume?: Extra | null;
    }>(`${BASE}/${game}/saved`);

    if (!answer.saved || answer.roundId === undefined || answer.view === undefined) return null;
    return { roundId: answer.roundId, view: answer.view, resume: answer.resume ?? null };
  },

  /** Finished levels, best score each. Empty for a guest. */
  async progress(game: string): Promise<LevelResults> {
    const answer = await request<{ levels: LevelResults }>(`${BASE}/${game}/progress`);
    return answer.levels;
  },
};

/**
 * Replaces {name} placeholders. The texts endpoint sends finished Dutch
 * sentences, so this only fills the few that take a value.
 */
export function fill(text: string, values: Record<string, string | number> = {}): string {
  return text.replace(/\{(\w+)\}/g, (whole, name: string) =>
    name in values ? String(values[name]) : whole);
}
