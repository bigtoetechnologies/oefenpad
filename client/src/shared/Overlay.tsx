import { useId, type CSSProperties, type ReactNode } from 'react';

interface OverlayProps {
  open: boolean;
  title?: ReactNode;
  children: ReactNode;
  /** Extra class on .settings-modal, e.g. a wider category picker. */
  className?: string;
  style?: CSSProperties;
}

/**
 * The modal shell the games share: a .settings-overlay holding a
 * .settings-modal. The per-game sheet supplies the look; this only
 * keeps the markup, the dialog role and the hidden state in one place.
 */
export function Overlay({ open, title, children, className, style }: OverlayProps) {
  const titleId = useId();

  return (
    <div
      className={`settings-overlay${open ? '' : ' hidden'}`}
      role="dialog"
      aria-modal="true"
      aria-labelledby={title === undefined ? undefined : titleId}
    >
      <div className={`settings-modal${className ? ` ${className}` : ''}`} style={style}>
        {title === undefined ? null : <h2 id={titleId}>{title}</h2>}
        {children}
      </div>
    </div>
  );
}
