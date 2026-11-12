import { useEffect, useState } from 'react';

/**
 * Counts whole seconds while `running`. Pass a value that changes when a
 * new round is dealt to put the clock back to zero.
 */
export function useTimer(running: boolean, roundKey: unknown = null): number {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    setSeconds(0);
  }, [roundKey]);

  useEffect(() => {
    if (!running) return;
    const id = window.setInterval(() => setSeconds((value) => value + 1), 1000);
    return () => window.clearInterval(id);
  }, [running]);

  return seconds;
}
