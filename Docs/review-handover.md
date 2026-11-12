# Review and hardening handover

What a code review of the uncommitted `server/` and `client/` work found on 10
November 2026, what was fixed, and what was deliberately left. Read this before
touching the games backend or the account flows.

Scope of the review: the working-tree diff plus roughly 13,000 lines of new
untracked code in `client/`, `server/` and `tools/`.

## State as of 10 November 2026

| Check | Result |
|---|---|
| `dotnet build server/Oefenpad.sln -p:SkipClientBuild=true` | 0 warnings, 0 errors |
| `dotnet test server/Oefenpad.Tests` | 39 passed, 0 failed, 0 skipped |
| `npx tsc --noEmit` in `client/` | 0 errors |
| `tools/smoke-games-api.py` | all checks passed |
| `tools/smoke-game-progress.py` | all checks passed |

Build and tests were run twice by separate agents. The smoke suites were run by
the agent that applied the fixes.

Nothing has been committed. The fixes sit in the working tree on top of the
eight unpushed commits.

## What the owner decided this session

These are not derivable from the code and were settled in conversation.

| Decision | Detail |
|---|---|
| Sending a round's answer to the browser is fine | Hangman may ship the answer at round start. Word search may ship the grid plus every word and position. The client may run game logic locally |
| The concern is bulk download only | "We don't want anybody downloading easy files with all the words and the categories in them" |
| No endpoint may expose a whole inventory | The backend must serve only what the current game or scene needs |
| Prepositions gets level gating | A learner must pass each level before the next unlocks. Accepted as a brake on scraping, not a cure |
| The free tier is a content slice | Voorzetselpaden: three levels free, six with an account, the last nine paid. Word search roughly three A0 categories free. No payment system yet |
| Prepositions scene slugs are not a problem | `wachten-op-bus.png` names the answer, but the game is not an exam |
| Finishing a level counts as passing | The gate exists to make a crawler play, not to grade the player |
| A registration may answer the same either way | When the address already has an account, the sign-up page shows the same success message and emails the holder a route instead of disclosing it |

## What was fixed

Twenty-five changes in total: fifteen findings from the review, six more that a
first review pass had raised and the second missed, and four smaller items.

<details>
<summary>The fifteen review findings</summary>

| # | Severity | Finding | Location |
|---|---|---|---|
| 1 | Critical | Host header poisoned password-reset, confirm and delete links | `server/Oefenpad.Services/AccountService.cs:204` |
| 2 | High | Change-email moved login identity before the new address proved itself | `server/Oefenpad.Services/AccountService.cs:117` |
| 3 | High | Auth cookie shipped without Secure behind a TLS-terminating proxy | `server/Oefenpad.WebUI/Program.cs:128` |
| 4 | High | Concurrent moves on one round corrupted its shared mutable state | `server/Oefenpad.Services/Games/RoundStore.cs:14` |
| 5 | High | Action after a finished round threw, returning 500 not 410 | `server/Oefenpad.Services/Games/PrepositionsService.cs:498` |
| 6 | High | After a miss, half the matching board refused every tap | `client/src/games/matching/MatchingGame.tsx:155` |
| 7 | High | Tapping a missed memory card did nothing and unmasked the pair | `client/src/games/memory/MemoryGame.tsx:297` |
| 8 | High | A transient error wiped the board with no way back | `client/src/games/prepositions/PrepositionsGame.tsx:358` |
| 9 | High | Translation choice discarded; restart cost progress and gained nothing | `client/src/games/wordsearch/WordSearchGame.tsx:569` |
| 10 | Medium | Rate limiter keyed on the proxy address, giving one global bucket | `server/Oefenpad.WebUI/Program.cs:252` |
| 11 | Medium | Non-transactional delete could leave an account with no profile | `server/Oefenpad.Services/AccountDeletionService.cs:298` |
| 12 | Medium | False true/false items opened with "Nee." on a correct answer | `server/Oefenpad.Services/Games/PrepositionsService.cs:278` |
| 13 | Medium | Stale build stamp silently published an empty `/spelen` bundle | `server/Oefenpad.WebUI/Oefenpad.WebUI.csproj:60` |
| 14 | Medium | The `/spelen/` games list rendered with no shell styling | `client/src/site/GameList.tsx:166` |
| 15 | Medium | Read-then-insert race on progress rows 500'd on double submit | `server/Oefenpad.Services/Games/GameProgressService.cs:45` |

</details>

<details>
<summary>The six the second pass missed</summary>

These came from an earlier review of the same tree. The second pass renumbered
its findings and did not cover them, so they were applied separately.

| Fix | Location |
|---|---|
| `send` and `spin` recompare the round id after the await; `chooseCount` guards on `spinningRef` | `client/src/games/storymachine/StoryMachineGame.tsx:293,336,358` |
| `/saved` reuses the live round and drops Resume's fresh copy, instead of leaking a slot per resume | `server/Oefenpad.WebUI/Api/GamesApi.cs:59` |
| Beginner `MinOverlapPercent` 30 to 0, which is the only value a one-direction grid can reach | `server/Oefenpad.Services/Games/WordSearchService.cs:22` |
| `submit` discards its response when the round id has moved on | `client/src/games/wordsearch/WordSearchGame.tsx:431` |
| Confetti duration unified on seconds at all four call sites; doc comment corrected | `client/src/shared/confetti.ts:12`, `client/src/games/hangman/HangmanGame.tsx:244` |
| The resume effect returns early when the player has already picked a level | `client/src/games/prepositions/PrepositionsGame.tsx:299` |

The obvious fix for the round leak is wrong. Removing `save.RoundId` before the
resume kills the round the browser is still holding, so a second tab would
return 410 to the first mid-game. `tools/smoke-game-progress.py` catches it.

</details>

<details>
<summary>Four smaller items fixed along the way</summary>

- `client/scripts/scope-css.mjs` silently dropped `:root` token overrides, losing
  Voorzetselpaden's `--ruimte`. It now rewrites them to `.game--<game>`.
- `client/index.html` had no `data-taal`, so both language spans rendered.
- `MemoryService` indexed `Content.Categories` unchecked.
- `GameShell` still had two dead `href="#"` nav links that `index.html` had
  already replaced with Inloggen and Registreren.

</details>

Two shapes are worth knowing because they recur. Several client bugs were a
stale closure surviving an await: the fix is a ref mirroring the state, compared
after the await. Two others were server-side ordering, where a check ran before
the state it depended on was cleared.

## What was deliberately left

| Item | Why | Location |
|---|---|---|
| Login timing oracle | A dummy PBKDF2 verification for unknown addresses was judged not worth the change | — |
| `RoundStore`'s global 4,000-round cap evicts other players' live rounds | Real, but the fix is a per-user cap, which is the scaling work already parked as open item 10 in `CLAUDE.md` | `server/Oefenpad.Services/Games/RoundStore.cs` |

## Corrections to the record

Two things earlier documents state or imply that are wrong.

**bigtoegames is not the reference architecture.** It is vanilla HTML, CSS and
JavaScript with no .NET, no React and no API. It was the source of game
*content* only: the word bank, the image manifest, the Dutch strings and the
game mechanics. `Docs/reuse-bigtoegames.md` describes that correctly. The
backend's reference is TotumTeams, as `Docs/accounts-handover.md:48-61` says.

**The old word bank is not on the public remote.** `bigtoetechnologies/oefenpad`
is public, but its head is `f095325` from 31 October 2026. `src/shared/words.js`
entered at `ef47919`, which is inside the eight unpushed commits. What is public:
`src/storymachine/reels.js`, `Docs/Concept.md`, `Docs/games.md`,
`Docs/suggestions.md` and `Docs/story-machine.md`.

## Architecture findings

### The server follows TotumTeams closely; the client had no reference

TotumTeams is Blazor and MudBlazor with no JavaScript frontend, so `client/` was
written without a model to follow. Matching on the server: the eight-project
split, `Directory.Build.props`, `Result<T>`, `IdentityDbContext` with a context
factory, `AuditableEntry`, `UtcDateTimeConverter`, `*Mappings.ToDto`, the
rate-limit policy style, `SqliteTestBase` and the migrations layout.

| Divergence worth acting on | Evidence |
|---|---|
| Manual DI instead of Scrutor `Scan` | `server/Oefenpad.WebUI/Program.cs:52-57,64-75`; TotumTeams `Program.cs:199` |
| `IGameService` and `GameRegistry` in Services, not Contracts | `server/Oefenpad.Services/Games/GameService.cs:10,206` |
| `ExecuteWithRetryAsync` copied but dead | No `EnableRetryOnFailure`, zero callers. `Docs/accounts-handover.md` calls it a match, which overstates it |
| No Serilog, no `/health`, no `UseExceptionHandler` | TotumTeams has all three |
| No `ValidateOnStart`; Data Protection keys path hard-coded | `server/Oefenpad.WebUI/Program.cs:39`; TotumTeams reads `DataProtection:KeysPath` |
| `RateLimitPolicies` moved from Enums to WebUI | `server/Oefenpad.WebUI/Services/RateLimitPolicies.cs` |

No `.resx`, plain validators, SQLite and a simplified email path are all
justified by scope.

### The games are loosely coupled but the seam is untyped

The six games are not over-coupled. One route set, one registry, one round store
and one save table serve all six, `GamesApi.cs` holds no per-game code, and a
seventh game touches no other game's files.

The real weakness is the opposite. Move bodies arrive as raw `JsonElement`,
views leave as `object`, and each game re-declares its view shape by hand in
React. A server rename compiles clean and fails at runtime. `client/src/api.ts`
was checked field by field against the server DTOs on 10 November 2026 and
matched, with nothing enforcing it.

| Strain | Evidence |
|---|---|
| Level progress built for six games, used by one | `LevelOf` returns null for five of six; only `PrepositionsService.cs:79` overrides it |
| Storymachine does not fit the contract | Never returns `Done`, fakes categories, fakes levels as reel counts | 
| Hand-maintained registries, six places | `Program.cs:64-69`, `GameContent.cs:22`, `App.tsx`, `GameList.tsx`, `main.tsx` |

`GameContent.cs:22` hard-codes the six game names. A seventh game's texts are
skipped silently until the name is added.

### The React games have no tests

`client/package.json` has only `dev`, `build`, `preview` and `scope-css`. There
is no Vitest, Jest or Playwright dependency and no test file anywhere under
`client/`. The only automated client check is the TypeScript compile.

BigToe's fake-DOM smoke suites, its dictionary check and its build-time asset
check were all dropped in the move and nothing replaced them.

## Content exposure under the owner's threat model

The "easy files" requirement is met. `words.json`, `wordimages.json`,
`prepositions.json` and `reels.json` are `EmbeddedResource`
(`server/Oefenpad.Resources/Oefenpad.Resources.csproj:15-18`) and unreachable
over HTTP. Only `/assets` and the WebUI `wwwroot` are served. The React bundle
carries no word list, and there are no sourcemaps.

What remains is scripted crawling, one round at a time.

| Exposure | Requests to take the lot | Verdict |
|---|---|---|
| Prepositions `/options` returned every frame phrase in one GET | 1 | Fixed: the subtitle is now the scene count |
| Memory, level 10, category "all": 50 of 148 words and images per call | ~13 | Fix |
| Storymachine: 6 of 72 tiles per round, lever redraws without a new start | ~40 | Fix |
| Word search insane: 65 words per call | ~75 for ~2,500 words | Low priority, owner's call |
| Hangman: one word per call | ~13,000 | Leave |
| `/options` category ids, names and counts | 1 | Leave. Metadata, no words |

These counts are static analysis of the generators, not measured against a
running host. The rate limit is 600 requests per 5 minutes per IP
(`server/Oefenpad.WebUI/Program.cs:153`), which none of the crawls above trip.
`/api/games` still has no `RequireAuthorization`, and it does not need one for
the brake to bite: `GameAccessService` reads progress directly, marking levels
past the free slice as `account`, levels past the account slice as `premium`,
and levels inside a tier that the learner has not reached as `progress`.
Starting one answers 403.

## Work closed after the review

| # | Item | What was done |
|---|---|---|
| 1 | `/options` leaked every preposition frame phrase | `PrepositionsService.Options()` no longer joins the phrases; a level's subtitle is its scene count (`3 beelden`, `1 beeld`). Test: `The_prepositions_options_carry_no_frame_phrases` |
| 2 | Preposition gating and the free-tier slice | `GameAccessService` + `PrepositionAccess` in `server/Oefenpad.Services/Games/`. Three tiers: levels 1–3 free, 4–9 with an account, 10–18 paid (shut, since payment is not built). `GameLevel` carries `locked` / `lockReason`; `/options` annotates and `POST .../rounds` answers 403. The client renders a locked row with a lock glyph, the Dutch reason, and a Registreren link when the reason is `account`. Eight tests in `Games/GameAccessTests.cs` |
| 3 | `easy` word-search overlap | Confirmed unreachable. Twenty generated boards had **0 %** overlap: under `AvoidAdjacent` a shared cell's other-direction neighbours read as touches, so regeneration could never succeed. `MinOverlapPercent` 25 → 0. Round time fell from **152 ms to 8.3 ms**; medium, hard, master and insane were unchanged (274, 487, 481, 19 ms) |
| 4 | Registration disclosed whether an address had an account | `RegistrationService.RegisterAsync` now returns the same success result when the address already has an account and emails the holder instead: a fresh confirmation link when unconfirmed, or a sign-in button plus password-reset link when confirmed (`AccountEmails.AccountBestaatAl`). The success copy is neutral ("Controleer je e-mail…"). Two tests replace the old one |
| 5 | Production `App:BaseUrl` / `App:KnownProxies` | The start-up guard already existed; this session verified it and documented the required values, their failure modes and a sample production invocation in `accounts.md`. `appsettings.json` now carries both keys (empty). Setting the real domain and SMTP provider is a deployment step, not code — it waits on open question 1 (domain) and item 8 (mail provider) |
| 6 | Record the free-tier decision | `Docs/decisions.md` Q4 now states the games' free slice and what remains open; `CLAUDE.md` items 5, 7 and 8 were narrowed to match |

## Work not started

Nothing from the review is left unaddressed. What remains is deployment: a
domain, an SMTP provider and a proxy address. See `CLAUDE.md` open items 1, 8
and 10.

## How to verify

```sh
dotnet build server/Oefenpad.sln -p:SkipClientBuild=true
dotnet test server/Oefenpad.Tests
cd client && npx tsc --noEmit
python3 tools/smoke-games-api.py
python3 tools/smoke-game-progress.py
```

The smoke suites need the server running on 8098. Port 8080 belongs to something
of the owner's; leave it alone.

```sh
ASPNETCORE_ENVIRONMENT=Development dotnet run \
  --project server/Oefenpad.WebUI --urls http://127.0.0.1:8098
```

Stop that server when finished. A previous session left one listening.
