import { useEffect, useState } from 'react';
import { api, ApiError, type GameOptions, type Texts } from '../api';

export interface GameData {
  texts: Texts | null;
  options: GameOptions | null;
  error: string | null;
}

/**
 * Loads the two small metadata endpoints a game needs before it can
 * start: its Dutch interface strings and the categories/levels it may
 * offer. Neither contains words, answers or puzzles.
 */
export function useGameData(game: string): GameData {
  const [texts, setTexts] = useState<Texts | null>(null);
  const [options, setOptions] = useState<GameOptions | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    setError(null);

    Promise.all([api.texts(game), api.options(game)])
      .then(([loadedTexts, loadedOptions]) => {
        if (!alive) return;
        setTexts(loadedTexts);
        setOptions(loadedOptions);
      })
      .catch((cause: unknown) => {
        if (!alive) return;
        setError(cause instanceof ApiError ? cause.message : 'De oefening is even niet bereikbaar.');
      });

    return () => {
      alive = false;
    };
  }, [game]);

  return { texts, options, error };
}
