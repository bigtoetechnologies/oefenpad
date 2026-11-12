/* =================================================================
   sound.ts — the small WebAudio set the card games share.

   One AudioContext for the page, created lazily and resumed on use
   because browsers keep it suspended until a gesture. Every call
   takes the game's sound setting, so a muted game is a no-op.
   ================================================================= */

let context: AudioContext | null = null;

function audio(): AudioContext | null {
  if (!context) {
    const Ctor = window.AudioContext
      ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Ctor) return null;
    try {
      context = new Ctor();
    } catch {
      return null;
    }
  }
  if (context.state === 'suspended') void context.resume();
  return context;
}

/** One oscillator with an exponential decay. steps: [[hz, offsetSeconds], ...] */
function tone(
  type: OscillatorType,
  steps: Array<[number, number]>,
  peak: number,
  duration: number,
  startAt?: number,
): void {
  const ctx = audio();
  if (!ctx) return;

  const now = startAt ?? ctx.currentTime;
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();

  oscillator.type = type;
  for (const [frequency, offset] of steps) {
    oscillator.frequency.setValueAtTime(frequency, now + offset);
  }
  gain.gain.setValueAtTime(peak, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

  oscillator.connect(gain);
  gain.connect(ctx.destination);
  oscillator.start(now);
  oscillator.stop(now + duration);
}

const NOTES = [523, 659, 784, 1047];

export const sfx = {
  flip(enabled: boolean): void {
    if (enabled) tone('sine', [[420, 0]], 0.08, 0.08);
  },

  correct(enabled: boolean): void {
    if (enabled) tone('sine', [[523, 0], [659, 0.08]], 0.18, 0.25);
  },

  wrong(enabled: boolean): void {
    if (enabled) tone('sawtooth', [[180, 0], [120, 0.12]], 0.12, 0.22);
  },

  fanfare(enabled: boolean): void {
    if (!enabled) return;
    const ctx = audio();
    if (!ctx) return;
    const start = ctx.currentTime;
    NOTES.forEach((note, index) => {
      tone('sine', [[note, 0]], 0.18, 0.4, start + index * 0.14);
    });
  },
};
