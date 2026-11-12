import { useEffect, type ReactNode } from 'react';
import { useSplash } from '../shared/useSplash';

declare global {
  interface Window {
    Oefenpad?: {
      verf?: (element: Element) => void;
      verfAlles?: () => void;
      ensureThemeToggle?: () => void;
    };
  }
}

interface GameShellProps {
  /** API segment; also the CSS scope class .game--<game>. */
  game: string;
  title: string;
  tagline?: string;
  /** Splash title. Omit for games that open straight onto the board. */
  splash?: string;
  onSettings?: () => void;
  children: ReactNode;
  overlays?: ReactNode;
}

/**
 * The chrome every game carries: the .vel column, the site bar, the
 * game heading with its back and settings buttons, and the footer.
 * The class names are the contract with oefenpad.css and the scoped
 * per-game sheets, so they stay Dutch.
 */
export function GameShell({
  game,
  title,
  tagline,
  splash,
  onSettings,
  children,
  overlays,
}: GameShellProps) {
  const splashState = useSplash();

  useEffect(() => {
    // oefenpad.js runs before React renders, so it cannot find .balk .rechts
    // on its own here. Ask it to inject the theme button once we have one.
    window.Oefenpad?.ensureThemeToggle?.();
    window.Oefenpad?.verfAlles?.();
  }, []);

  return (
    <div className={`game--${game}`}>
      {splash === undefined ? null : (
        <div
          className={
            'splash-screen'
            + (splashState.fading ? ' fade-out' : '')
            + (splashState.hidden ? ' hidden' : '')
          }
          onClick={splashState.dismiss}
        >
          <img className="splash-logo" src="/assets/logo/logo_128px.png" alt="Oefenpad" />
          <div className="splash-title">{splash}</div>
        </div>
      )}

      <div className="vel">
        <nav className="balk">
          <a className="merk" href="/index.html">
            <img src="/assets/logo/logo_128px.png" alt="" />
            <span>Oefenpad</span>
          </a>
          <a className="link" href="/index.html">Oefeningen</a>
          <a className="link" href="/Account/Inloggen">Inloggen</a>
          <a className="link" href="/Account/Registreren">Registreren</a>
          <div className="rechts" />
        </nav>

        <div className="spel-kop">
          <h1>{title}</h1>
          <div className="stand">
            {tagline === undefined ? null : <p className="tagline">{tagline}</p>}
            <a className="btn-icon" href="/index.html" aria-label="Terug naar Oefenpad">←</a>
            {onSettings === undefined ? null : (
              <button
                type="button"
                className="btn-icon"
                onClick={onSettings}
                aria-label="Instellingen"
                title="Instellingen"
              >
                ⚙️
              </button>
            )}
          </div>
        </div>

        {children}

        <footer className="voet">
          <div className="links">
            Woorden uit <em>Quick Wins in Dutch</em>
          </div>
          <div className="rechts">
            <a href="/voorwaarden.html">Voorwaarden</a>
            <a href="/privacy.html">Privacy</a>
          </div>
        </footer>
      </div>

      {overlays}
    </div>
  );
}
