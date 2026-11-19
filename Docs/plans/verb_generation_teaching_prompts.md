# Verb Generation & Teaching Pipeline — Modular Prompts

Each prompt below is self-contained and designed to be pasted into a fresh context window, targeting a single file or discrete batch so sub-agents stay lean and avoid context bloat.

---

## Phase 1: Irregular Verbs

### Prompt 1.1 — Scope & Schema for Irregular Verbs
```text
Create a single schema/specification file (`irregular_verbs_spec.md` or `.json`) defining how we will store all Dutch irregular verbs and their conjugations for language teaching.
Include:
- Target language levels and which tenses apply to each level.
- Rules for generating up to 4 example sentences per verb across relevant tenses, paying close attention to how Dutch tenses and aspect differ from English (avoiding literal English calques).
- A format for image generation prompts paired with each example sentence (e.g., showing action in progress vs. completed arrival/result).
- A structure suitable for parallel sub-agent batches without context bloat.
Do not generate the full verb list yet—output only the schema and generation rules.
```

### Prompt 1.2 — Generate Irregular Verbs (Batch A)
```text
Using our irregular verbs schema, generate the first batch of high-frequency Dutch irregular verbs (alphabetical slice A–G, or first N verbs as agreed in the schema) into a standalone batch file (`irregular_verbs_batch_01.json` or `.md`).
For each verb, include:
- All relevant conjugations across tenses mapped to CEFR/language levels.
- Up to 4 example sentences in context (accounting for Dutch tense/aspect nuances vs. English).
- A clear image prompt for each example sentence.
Keep output strictly to this batch file so context remains small.
```

### Prompt 1.3 — Generate Irregular Verbs (Remaining Batches)
```text
Continue generating the remaining Dutch irregular verbs following the exact same schema and formatting rules as the previous batch, writing them to the next batch file (`irregular_verbs_batch_02.json` / `batch_03.json`).
Ensure every verb includes all level-appropriate tense conjugations, up to 4 nuanced example sentences, and corresponding image prompts.
```

### Prompt 1.4 — Assemble Single Master Irregular Verbs File
```text
Combine all generated irregular verb batch files into a single master file (`irregular_verbs_master.json` or `.md`).
Verify there are no missing required fields, duplicate entries, or broken formatting, and summarize any edge cases or tense/aspect notes found during consolidation.
```

---

## Phase 2: Regular Verbs (Using Lexicon / Voorzetselpaden Pattern)

### Prompt 2.1 — Define Regular Verb Generation Plan from Lexicon
```text
Create a plan/mapping file (`regular_verbs_plan.md`) for extracting regular Dutch verbs from our lexicon list and structuring them to match the `voorzetselpaden` / verb-preposition pattern.
Specify:
- How regular verbs are filtered/grouped from the lexicon list.
- All tenses included per verb and level mapping.
- How 4 sample sentences and 4 image prompts per verb will be structured consistently with `voorzetselpaden`.
- Batch sizing for parallel sub-agent execution.
```

### Prompt 2.2 — Generate Regular Verbs (Batch 1)
```text
Following `regular_verbs_plan.md` and matching the `voorzetselpaden` structure, generate the first batch of regular Dutch verbs into `regular_verbs_batch_01.json` (or `.md`).
Include full tense conjugations, 4 sample sentences per verb, and an image prompt for each sentence.
```

### Prompt 2.3 — Generate Regular Verbs (Subsequent Batches & Consolidation)
```text
Generate the next batch of regular Dutch verbs from the lexicon list into `regular_verbs_batch_02.json` (or merge completed batches into `regular_verbs_master.json` / `.md`), maintaining strict consistency with the `voorzetselpaden` format, 4 sample sentences per verb, and image prompts.
```

---

## Phase 3: Creative Teaching Formats & Mini-Games

### Prompt 3.1 — Brainstorm & Evaluate Teaching Activities for Verbs
```text
Propose creative ways to teach Dutch regular and irregular verbs beyond standard drills, comparing them against the `voorzetselpaden` approach.
Include concrete mechanics for:
- Adding `"verb"` as a category in Hangman and Word Search formats.
- A Memory game variant pairing verb stems on one side of the board with conjugated forms/tenses on the other.
- 2–3 additional high-engagement formats suited to different tenses and learner levels.
Save the evaluation to `verb_teaching_formats.md`.
```

### Prompt 3.2 — Create Game Data / Content Spec for `"verb"` Category
```text
Using `verb_teaching_formats.md`, create a structured data file (`verb_games_data.json`) supporting:
- Hangman entries under category `"verb"` (with clues/tense hints).
- Word Search word lists/grids under category `"verb"`.
- Memory board pairs mapping verb stems to specific tense conjugations.
Keep schemas clean and easy for the game runner or sub-agents to consume.
```

---

## Phase 4: Separable Verbs (*Scheidbare Werkwoorden*)

### Prompt 4.1 — Define Separable Verbs Schema & Split Strategy
```text
Create `separable_verbs_spec.md` adapting our verb schema for Dutch separable verbs (*scheidbare werkwoorden*).
Account for:
- Prefix separation in main clauses vs. attached forms in subordinate clauses, infinitives with *te*, and past participles (*ge-* placement).
- Level-appropriate tenses, up to 4 example sentences per verb, and image prompts (e.g., visually distinguishing literal/spatial separation vs. completed action).
- A parallel sub-agent batching plan.
```

### Prompt 4.2 — Parallel Batch Generation for Separable Verbs
```text
Following `separable_verbs_spec.md`, generate a batch of Dutch separable verbs (`separable_verbs_batch_01.json` / `.md`) with full conjugations across relevant tenses, 4 example sentences per verb (showing separable behavior accurately), and image prompts.
```

### Prompt 4.3 — Consolidate Separable Verbs Master File
```text
Merge all separable verb batch files into `separable_verbs_master.json` (or `.md`), checking prefix/participle consistency, sentence counts (up to 4 per verb), and image prompt completeness.
```

---

## Execution Tips for Fresh Contexts & Sub-Agents
- **One file per prompt:** Keep each prompt focused on creating or merging one specific file so a fresh session doesn't waste tokens re-reading huge datasets.
- **Parallelize batches, not schemas:** Run schema/spec prompts first (`1.1`, `2.1`, `4.1`), then launch parallel sub-agents across disjoint alphabetical/index ranges for batch files (`batch_01`, `batch_02`, etc.), followed by a single merge step.
- **Autonomous defaults:** Each spec prompt instructs the agent to lock in sensible defaults (e.g., CEFR levels A1–B2, JSON vs. Markdown) and document them in the spec file so execution isn't blocked on questions.