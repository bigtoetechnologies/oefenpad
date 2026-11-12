import { useCallback, useEffect, useRef, useState } from 'react';

export interface SplashState {
  hidden: boolean;
  fading: boolean;
  dismiss: () => void;
}

/**
 * The splash behaves as it did on the old pages: it fades out after
 * `autoMs`, or as soon as the player taps it, and is removed from the
 * layout once the fade has finished.
 */
export function useSplash(autoMs = 2500, fadeMs = 600): SplashState {
  const [hidden, setHidden] = useState(false);
  const [fading, setFading] = useState(false);
  const leaving = useRef(false);

  const dismiss = useCallback(() => {
    if (leaving.current) return;
    leaving.current = true;
    setFading(true);
    window.setTimeout(() => setHidden(true), fadeMs);
  }, [fadeMs]);

  useEffect(() => {
    const timer = window.setTimeout(dismiss, autoMs);
    return () => window.clearTimeout(timer);
  }, [autoMs, dismiss]);

  return { hidden, fading, dismiss };
}
