import { useState } from 'react';

interface WordImageProps {
  src: string;
  alt?: string;
  className?: string;
}

/**
 * A word picture. The image bank is generated from a folder, so an
 * entry can outlive its file; a missing picture hides itself instead
 * of leaving a broken-image icon in the middle of a game.
 */
export function WordImage({ src, alt = '', className }: WordImageProps) {
  const [failed, setFailed] = useState(false);
  if (failed) return null;

  return (
    <img
      src={src}
      alt={alt}
      className={className}
      onError={() => setFailed(true)}
    />
  );
}
