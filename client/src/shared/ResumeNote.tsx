/* =================================================================
   hervat.tsx — the quiet line that says a saved round was picked up.

   A resume is a courtesy, not an event: the player left mid-round and is
   put back where they were. It must never look like a warning, so it
   borrows the muted status colour and disappears when they start anew.
   Dutch only, like the rest of the game chrome.
   ================================================================= */

import { useEffect, useState } from 'react';

export function ResumeNote({ text, onDone }: { text: string | null; onDone?: () => void }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (text === null) {
      setVisible(false);
      return;
    }

    setVisible(true);
    const timer = window.setTimeout(() => {
      setVisible(false);
      onDone?.();
    }, 6000);

    return () => window.clearTimeout(timer);
    // onDone is stable in the games that pass it; the text is the trigger.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [text]);

  if (!visible || text === null) return null;
  return (
    <p className="hervat" role="status">
      {text}
    </p>
  );
}
