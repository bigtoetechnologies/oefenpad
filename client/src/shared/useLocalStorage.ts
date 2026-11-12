import { useCallback, useState } from 'react';

/**
 * A value kept in localStorage under the same keys the old pages used,
 * so settings and best scores survive the move to React.
 */
export function useLocalStorage<T>(
  key: string,
  initial: T,
): [T, (value: T | ((current: T) => T)) => void] {
  const [value, setValue] = useState<T>(() => {
    try {
      const raw = window.localStorage.getItem(key);
      return raw === null ? initial : (JSON.parse(raw) as T);
    } catch {
      return initial;
    }
  });

  const update = useCallback(
    (next: T | ((current: T) => T)) => {
      setValue((current) => {
        const resolved = typeof next === 'function'
          ? (next as (current: T) => T)(current)
          : next;
        try {
          window.localStorage.setItem(key, JSON.stringify(resolved));
        } catch {
          /* private mode; the value still works for this session */
        }
        return resolved;
      });
    },
    [key],
  );

  return [value, update];
}
