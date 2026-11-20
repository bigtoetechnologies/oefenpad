# Voorzetselpaden art — session notes (18 Nov 2026)

Working note for the next session: everything needed to start producing images.
It lives here rather than under Docs/ because that tree is HTML only; this folder
already carries a Markdown README.

## 1. The problem

- Repo `C:\repos\oefenpad`. 1,015 cards over 8 band pages. **163 images** in
  `assets/verb-propositions/incoming`, **91 promoted** in `assets/voorzetselpaden`.
  ~850 cards still need art.
- House style (`Docs/voorzetselpaden/base-prompt.txt` + 3 references in
  `assets/verb-propositions/referenceimages/style-a/`): flat cobalt `#2B50C8` on pure
  white, thick crisp outlines, solid fills, white faces, no shading/grey/text, 784×1168.
- Owner has relaxed this: **style is negotiable**. Photorealism, line art and two tones
  are acceptable if the brief is met. Hard rule that stands: **no text/letters/numbers**.

## 2. Hardware and runtime

| | |
|---|---|
| GPU | AMD Radeon RX 5700, 8 GB, gfx1010 (RDNA1), Vulkan only — no ROCm, no bf16, no matrix cores |
| CPU / RAM | Ryzen 5 5500, 16 GB |
| Image runtime | stable-diffusion.cpp commit `de298c2` in `F:\sd` (`sd-cli.exe`, `sd-server.exe`) |
| LLM | LM Studio, CLI `C:\Users\antho\.lmstudio\bin\lms.exe` |

Models on disk:

```
F:\models\city96\FLUX.1-dev-gguf\flux1-dev-Q4_K_S.gguf                 6.5 GB
F:\models\city96\FLUX.1-schnell-gguf\flux1-schnell-Q4_K_S.gguf         6.5 GB
F:\models\flux-kontext\flux1-kontext-dev-Q4_K_S.gguf                   6.8 GB
F:\models\chroma\Chroma1-Base-Q4_0.gguf                                5.4 GB
F:\models\unsloth\FLUX.2-klein-4B-GGUF\flux-2-klein-4b-Q4_K_S.gguf     2.5 GB  (unusable: needs flux2 VAE)
F:\models\offgrid-ai\dreamshaper-xl-v2-turbo-GGUF  juggernaut-xl-v9-GGUF
F:\models\offgrid-ai\realvisxl-v5.0-lightning-GGUF    (all Q8_0 SDXL)
F:\models\models\sd35-medium\sd3.5_medium-Q5_K_M.gguf + clip_g.safetensors  (unusable: no VAE)
F:\models\flux\clip_l.safetensors  ae.safetensors  t5xxl-Q4_K_M.gguf   <- FLUX/Kontext text stack
```

## 3. Speed — measured

- Resolution is superlinear. FLUX dev: **234 s/step at 784×1168** (VRAM thrash) versus
  **~30 s/step at 512×763**. 512×763 is the practical working size for FLUX/Kontext.
- `--offload-to-cpu --stream-layers` halves full-res cost: 234 → **106 s/step**
  (still 38 min for 20 steps).
- VAE on GPU needs tiling: `--backend "vae=vulkan0" --vae-tiling --vae-tile-size 64x64`
  cut decode 74 s → 40 s. Untiled it silently falls back to CPU.
- Fixed per-process overhead is **~120–136 s** (graph-cut setup + weight streaming),
  independent of step count. `sd-server.exe` amortises it (~26 s/image for schnell at 512).
- SDXL fits, so it's fast: 8 steps at 784×1168 = **80 s** with VAE tiling.

| model @ 512×763 | steps | wall clock |
|---|---|---|
| FLUX schnell | 4 | 131–137 s |
| FLUX dev | 20 | 545–656 s |
| Kontext + 3 refs | 8 | 1,336 s (154.7 s/step) |

## 4. Model screen (card `bang-voor-hond`)

| model | result |
|---|---|
| SDXL DreamShaper v2 Turbo | photograph; ink 15 / white 0 / grey 76 — style impossible |
| FLUX schnell, 4 steps | flat two-tone drawing; style plausible, scene wrong |
| FLUX dev, 20 steps | flat cobalt, **hue exactly 216**; scene wrong, invented props |
| **Kontext + 3 style refs** | **palette pass** (ink 23.7 / white 74.1 / grey 0.1 / hue 216.4), style right, scene ~70 % |
| Kontext, 3 refs, full res | crashed: Vulkan device lost |
| Kontext, 1 ref, max-vram 4 | crashed: ErrorOutOfDeviceMemory |
| SD3.5 Medium | won't load: no VAE in GGUF, both VAE sources gated (401) |
| Chroma1-Base | runs; best *no-style* scene result, but painterly |
| FLUX.2 klein 4B | won't load: diffusion-only, needs flux2 VAE + mistral-small3.2 |
| Pony v6 XL | won't load: "get sd version from file failed" |

Target art measures ink 22 %, white 75.5 %, grey 0 %, hue 216.

## 5. Prompting findings — the important part

1. **The style paragraph was hijacking the frame.** Dropping style words made FLUX go
   photoreal *and* move the camera. Keep framing instructions, drop rendering ones.
2. **`Avoid:` lists and negative prompts are inert.** FLUX runs at `--cfg-scale 1`,
   so negative text is ignored. Prompts must be positive statements only.
3. **Element attribution improves with plain prompts** (dog barking, no invented child).
4. **Relations do not.** Which side of a gate, relative height (waist-high fence), who
   faces whom — failed repeatedly across models and phrasings.
5. **Emotion does not render.** "Scared face" produced calm, smiling, or cartoon.
6. **Seeds do not fix a semantic bias.** Four seeds of "leaning away from a dog" all
   leaned *towards* it.
7. **Kontext edits locally.** Given the liked image + "make him frightened" it changed
   the face only, left the posture.
8. **img2img at 0.6 strength** kept the hunch and made the dog calmer.
9. **Counting / viewpoint hints work**: "exactly four legs", "side view" remove a lot of
   structural errors.

## 6. What worked

- **Kontext + the three style-A references** — the only route that produced house-style
  art. Use for scene cards, accept ~70 % brief compliance, review the rest.
- **Gate/postman rethink** (owner's idea): "won't enter" expressed by an open gate plus
  distance worked where a backward lean did not.
- **Line art for objects: 6/6 structurally correct** (lemon, chair, church, bicycle,
  fruit, dog) versus pictogram 3/6 and silhouette 4/6. Line art is the noun style.
- **Abstract nouns read as literal scenes** in line art: hunter, explanation, meeting,
  journey, weather — all clear. Failures: calendar full of numbers (appointment),
  ambiguous stamp (permission), person too small (choice).
- **Deterministic normalisation works on flat art**: `F:\sd\pictogram-normalise.py` maps
  every non-white pixel to `#2B50C8` and flips inverted frames when ink > 50 %
  (chair measured 65 % → swapped). One cobalt on white, guaranteed.
- **RealVisXL Lightning for photoreal nouns**: ~1 min each at 1024², 4/6 clean; church
  drew two buildings, lemon came out cut in half.

## 7. Don't retry

- Forcing tone into style afterwards: hard threshold turned a face into a blob,
  saturation mapping gave a washed-out print. Normalisation only works on flat art.
- Prompt-only emotion, prompt-only relative height, prompt-only "no text".
- Kontext at full resolution, or with 3 refs and a big VRAM budget, on this card.
- SD3.5, FLUX.2 klein, Pony with the current downloads.

## 8. Tooling written

| path | what |
|---|---|
| `F:\sd\style-metric.py` | ink/white/grey/hue measurement + pass/fail |
| `F:\sd\pictogram-normalise.py` | force one-cobalt-on-white, fix inverted frames |
| `F:\sd\test-prompts\` | every prompt variant tried (`postman1`–`postman10`, `plain`, `plain2`, `nostyle`, `wordstyles/`, `hardnouns/`, `words/`) |
| `F:\sd\run-baseline-sdxl.bat`, `run-refs-kontext.bat`, `run-refs-klein.bat` | batch runners (klein cannot work) |
| `tools/check-prepositions-art.py` | QA harness: pixel checks + VLM `must`/`avoid` check + HTML sheet. **Untracked, unreviewed.** |
| `F:\outputs\style-test\ words\ wordstyles\ hardnouns\` | all rendered output |

## 9. Verified commands

FLUX schnell, 512×763, 4 steps:

```
sd-cli --diffusion-model F:/models/city96/FLUX.1-schnell-gguf/flux1-schnell-Q4_K_S.gguf \
  --clip_l F:/models/flux/clip_l.safetensors --t5xxl F:/models/flux/t5xxl-Q4_K_M.gguf \
  --vae F:/models/flux/ae.safetensors --fa --max-vram 5 \
  --backend "te=cpu,vae=vulkan0" --vae-tiling --vae-tile-size 64x64 \
  --prompt-file PROMPT.txt --seed 20261118 --steps 4 --cfg-scale 1 \
  --sampling-method euler -W 512 -H 763 -o OUT.png
```

Kontext + the three style references — the house-style route:

```
sd-cli --diffusion-model F:/models/flux-kontext/flux1-kontext-dev-Q4_K_S.gguf \
  --clip_l F:/models/flux/clip_l.safetensors --t5xxl F:/models/flux/t5xxl-Q4_K_M.gguf \
  --vae F:/models/flux/ae.safetensors \
  -r assets/verb-propositions/referenceimages/style-a/zorgen-om-persoon.png \
  -r assets/verb-propositions/referenceimages/style-a/krijgen-van-vriend.png \
  -r assets/verb-propositions/referenceimages/style-a/trots-op-kind.png \
  --fa --max-vram 4 --offload-to-cpu --stream-layers --backend "te=cpu,vae=cpu" \
  --prompt-file PROMPT.txt --seed 20261118 --steps 8 --cfg-scale 1 \
  --sampling-method euler -W 512 -H 763 -o OUT.png
```

RealVisXL Lightning, photoreal nouns at 1024²:

```
sd-cli -m F:/models/offgrid-ai/realvisxl-v5.0-lightning-GGUF/realvisxl-v5.0-lightning-Q8_0.gguf \
  --force-sdxl-vae-conv-scale --fa --max-vram 5 \
  --backend "vae=vulkan0" --vae-tiling --vae-tile-size 64x64 \
  --prompt-file PROMPT.txt --negative-prompt-file NEG.txt --seed 20261118 \
  --steps 6 --cfg-scale 2 --sampling-method euler -W 1024 -H 1024 -o OUT.png
```

QA harness:

```
python tools/check-prepositions-art.py --no-vision --html report.html
python tools/check-prepositions-art.py --limit 10 --html report.html   # + VLM, needs LM Studio
```

## 10. Recipe for starting production

Scene cards (verbs + prepositions), house style:

1. Prompt = plain positive statements: subject, action, relations, framing. No `Avoid:`
   text; style tail of 2–3 lines at most.
2. Kontext + 3 refs, 512×763, 8 steps, fixed seed, 2–4 rolls per card.
3. Contact sheet, pick the roll that satisfies the card's `must`.
4. Review with the harness — pixels first, VLM second.

Noun / vocabulary images:

1. Prefer **sourcing** real photos (Wikimedia Commons, licence recorded) — no artefacts.
2. Otherwise line art: FLUX schnell at 512 — "clean line drawing, colouring book style,
   thick even black outlines on white, single subject, side view".
3. `F:\sd\pictogram-normalise.py` → one cobalt on white; potrace to vector; hand-fix.
4. If photorealism is required: RealVisXL Lightning at 1024, 6 steps, cfg 2, counting
   hints ("exactly four legs"), 3 rolls, keep the best.

Always check: no text/letters/numbers, single subject, whole object in frame, person
large enough to fill most of the frame.

## 11. Open items

- `tools/check-prepositions-art.py` is untracked and unreviewed; its VLM path has never
  run end-to-end (server was loaded, then stopped).
- `git pull` blocked: `~/.ssh/id_ed25519` is passphrase-protected and no ssh-agent runs.
  Start the agent, or pull from a normal terminal.
- Zed has an `lmstudio` provider now (`settings.json`, backups `.bak` / `.bak2`). It needed
  all seven `capabilities` fields: `tools`, `images`, `parallel_tool_calls`,
  `prompt_cache_key`, `chat_completions`, `interleaved_reasoning`, `max_tokens_parameter`.
  The model was not visible afterwards — Zed needs a restart.
- VS Code is not installed; `C:\Users\antho\.continue\config.yaml` is written in advance.
- LM Studio: `lms server start`, model `qwen/qwen3.5-9b`, context 8192 (16 GB RAM caps this
  at roughly 16k before it spills to RAM).
