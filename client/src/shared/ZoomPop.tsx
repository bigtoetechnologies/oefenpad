import { useImperativeHandle, useRef, useState, forwardRef } from 'react';

export interface ZoomContent {
  /** Picture to show, when the card is a picture. */
  image?: string;
  /** Dutch word under the picture. */
  word?: string;
  /** Plain text card, used for word cards. */
  text?: string;
}

export interface ZoomPopRef {
  /** Enlarges a card, holds it, then shrinks it and calls back. */
  auto(content: ZoomContent, onDone: () => void): void;
  /** Shows a card at normal size until it is dismissed. */
  open(content: ZoomContent): void;
  /** Tears the popup down and drops any pending callback. */
  reset(): void;
}

const HOLD_MS = 1400;
const OUT_MS = 500;

/**
 * The card pop the card games share. A just-flipped card grows to the
 * middle of the screen, holds for a moment, then shrinks back; the
 * callback runs when it has gone, so the board can resolve the turn.
 */
export const ZoomPop = forwardRef<ZoomPopRef>(function ZoomPop(_props, ref) {
  const overlay = useRef<HTMLDivElement>(null);
  const card = useRef<HTMLDivElement>(null);
  const holdTimer = useRef<number | null>(null);
  const outTimer = useRef<number | null>(null);
  const popping = useRef(false);
  const onDone = useRef<(() => void) | null>(null);
  const [visible, setVisible] = useState(false);

  function clearTimers() {
    if (holdTimer.current !== null) window.clearTimeout(holdTimer.current);
    if (outTimer.current !== null) window.clearTimeout(outTimer.current);
    holdTimer.current = null;
    outTimer.current = null;
  }

  function paint(content: ZoomContent) {
    const node = card.current;
    if (!node) return;

    node.className = content.text === undefined ? 'zoom-card' : 'zoom-card zoom-text';
    node.replaceChildren();

    if (content.text !== undefined) {
      node.textContent = content.text;
      return;
    }

    if (content.image) {
      const image = document.createElement('img');
      image.src = content.image;
      image.alt = '';
      node.appendChild(image);
    }

    if (content.word) {
      const word = document.createElement('div');
      word.className = 'zoom-word';
      word.textContent = content.word;
      node.appendChild(word);
    }
  }

  function hide() {
    overlay.current?.classList.add('hidden');
    card.current?.classList.remove('zoom-pop', 'zoom-pop-out');
    setVisible(false);
  }

  function finish() {
    hide();
    popping.current = false;
    const callback = onDone.current;
    onDone.current = null;
    callback?.();
  }

  function popOut() {
    if (!popping.current) return;
    clearTimers();
    card.current?.classList.remove('zoom-pop');
    card.current?.classList.add('zoom-pop-out');
    outTimer.current = window.setTimeout(finish, OUT_MS);
  }

  function reset() {
    clearTimers();
    popping.current = false;
    onDone.current = null;
    hide();
  }

  useImperativeHandle(ref, () => ({
    auto(content, done) {
      reset();
      popping.current = true;
      onDone.current = done;
      paint(content);
      overlay.current?.classList.remove('hidden');
      card.current?.classList.add('zoom-pop');
      setVisible(true);
      holdTimer.current = window.setTimeout(popOut, HOLD_MS);
    },

    open(content) {
      reset();
      paint(content);
      overlay.current?.classList.remove('hidden');
      setVisible(true);
    },

    reset,
  }));

  function dismiss() {
    if (popping.current) popOut();
    else hide();
  }

  return (
    <div
      ref={overlay}
      className={`zoom-overlay${visible ? '' : ' hidden'}`}
      role="dialog"
      aria-modal="true"
      aria-label="Kaart"
      onClick={dismiss}
    >
      <div ref={card} className="zoom-card" />
    </div>
  );
});
