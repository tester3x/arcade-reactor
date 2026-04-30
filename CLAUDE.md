# Arcade Reactor — Project Context

This file is auto-loaded by Claude Code at session start. Keep it
tight and current. When something changes (architecture, phase plan,
design decisions), update this file in the same session.

## The user

**Mike.** IT Manager (oil/gas, North Dakota). Direct, no fluff.
Comfortable with PowerShell, git, Windows. Long-session worker.

**Communication preferences:**
- Be direct. No over-apologizing.
- Explicit file paths and commands.
- Tell him when you can't do something.
- Push back when he's wrong, with receipts.
- Don't cave to vague scope requests — ask clarifying questions.
- "Kicking ass" or similar = he's happy. Bug reports come with
  screenshots and context — trust them.

## The project

**Arcade Reactor** — static HTML/JS/CSS retro arcade site at
**arcadereactor.com**, hosted on GitHub Pages. Repo:
`tester3x/arcade-reactor`. Local: `C:\dev\arcade-reactor`.

Pure HTML/CSS/JS. No frameworks, no build step. Each game is one
self-contained HTML file under `games/`.

**Deploy flow:** GitHub Pages serves from `main`. Historically Mike
developed on the feature branch `claude/arcade-reactor-handoff-mwRLq`
and merged to main. In practice Phases 11.5–11.7 landed directly on
`main`, which left the feature branch behind and caused a merge
conflict when we tried to land the art pass. **Going forward, work
on whichever branch Mike hands you — but before editing, always
verify the branch is ancestor-of-main with `git merge-base --is-ancestor`
and rebase/merge main in first if not.** Otherwise your commit will
conflict on the way back.

## Games

- **`games/space-rocks.html`** — Asteroids clone. Shipped, stable.
- **`games/web-reactor.html`** — Tempest-like lane shooter. Shipped, stable.
- **`games/bunker.html`** — Active development. **This is where all
  current work happens.** Becoming "Escape" — a top-down stealth/
  combat game (see below).

## Shared patterns (every game uses these)

- 48px fixed top bar with back link, title, score area
- 900×650 logical canvas, scaled to viewport
- Input merge: keyboard + virtual thumbstick(s) + Gamepad API every
  frame into one input vector
- Standard gamepad mapping. Axes[0]=LX, Axes[1]=LY, Axes[2]=RX,
  Axes[3]=RY. Btn 0=A/fire, Btn 1=B, Btn 7=RT, Btn 9=Start.
  Touch UI auto-hides when the gamepad has recent input and re-shows
  the moment the screen is tapped (most-recent-input wins, 12.1).
- Pause: Esc/P/gamepad Start
- Bunker has a second stick (aim) and a NADE button positioned
  inside the aim-zone — see "bunker.html architecture" below. Other
  games (space-rocks, web-reactor) still use the single-stick layout.

# Bunker → Escape

The vision: Mike is turning `bunker.html` into a game called
**Escape**. Top-down stealth/combat with multiple rooms per level,
guards to evade or fight, keys to find, exit to reach, timer
ticking down. Multi-level progression with escalating threats.

## Reference: Mike's polished snake game

Mike has a separate, ambitious React Native snake game at
`C:\dev\SnakeGame` (not in this repo). Read its source before
making big design moves on Escape — it shows Mike's design bar.

Key takeaways:
- **Mike builds in layers of systems, not single mechanics.** Snake
  has enemy variety + spawn cadence + pickup ecosystem + risk/
  reward + hidden bonuses + timer pressure + theme cycling, all
  interacting. "One mechanic" reads as a tech demo to him.
- **Complexity unlocks over time.** Enemies appear at different
  levels (batbug L1, spidey L3, frankenstein L4, ghost L5). Themes
  cycle every 3 levels. Apply same staggered-introduction pattern
  to Escape: don't put every guard type and pickup in level 1.
- **Polish matters.** Spawn animations, attract mode, screen
  cycling, 3-letter arcade names. Skip these for prototypes but
  remember they're the bar.
- **Eventual mobile target.** Snake is React Native. Escape will
  likely get the same treatment via Capacitor wrap once it's fun.
  Build with phone-friendly UX in mind (touch already merged with
  keyboard/gamepad).

## Design decisions locked in

These came out of a long design conversation. Don't relitigate
without explicit reason.

1. **Screen-based rooms (not spatial-with-fog).** Each room is its
   own full-screen instance. Walking onto a doorway tile triggers
   a fade transition to the next room. This is Path B in the
   design conversation — chosen because "if you see the whole map
   from the start, how Escape-y is that?"
2. **Room-bound guards.** Guards stay in their assigned room,
   never cross doorways. Solves the cross-room movement problem
   architecturally rather than via AI.
3. **Hybrid stealth/combat.** Player can shoot guards. Stealth is
   rewarded via a planned **global alertness** system (Phase 9):
   shooting raises alertness, which makes remaining guards more
   suspicious (wider cones, faster patrols).
4. **Adaptive difficulty (deferred).** Future "Adaptive Director"
   phase reads player skill (deaths, time-per-level, times spotted)
   and tunes guard count/speed/vision. NOT a pre-game easy/medium/
   hard picker. Deferred because it needs play data to tune.
5. **Adaptive minimap.** Minimap starts as fog-of-war (rooms reveal
   as visited). Later, the adaptive director also tunes how much
   info it shows (low-skill: keys + guards on map; high-skill:
   layout only).

## Updated phase plan

Built ✓:

- **Phase 1–4:** Player movement, walls, guards, combat, HP, game over.
- **Phase 5:** Screen-based room architecture. Per-room maps, doorways,
  fade transitions, per-room guard/bullet state persistence.
- **Phase 6:** Keys + locked exit + WIN overlay + fog-of-war minimap.
- **Phase 7:** Pickups (health, speed boost) + limited ammo.
- **Phase 8:** Countdown timer + TIME'S UP overlay.
- **Phase 9:** Global alertness system (shooting raises alertness →
  wider cones + faster patrols + shorter investigate cooldowns).
- **Phase 10:** Guard types — sentry, hunter, alarm-raiser.
- **Phase 11:** Multi-level (L1 Bunker, L2 North Wing, L3 Core Reactor).
- **Phase 11.5–11.7:** Cook-and-throw grenades, aim reticle with
  landing/blast preview, cook-hint, guard dodge, grenades lob over walls.
- **Art pass (2026-04-24):** Swapped procedural wall, player, and
  guard rendering for Kenney CC0 Topdown Shooter sprites. Floor stays
  procedural — Kenney has no solid dark-gray floor tile. See
  "Sprites / TD Shooter assets" below.
- **Phase 11.8:** Twin-stick touch — added right-side aim stick, NADE
  button. Aim stick overrides facing same as gamepad right stick.
- **Phase 12.0:** Adaptive director. Per-completion score (time vs 90s
  target / hits taken / spotted count), rolling 3-level average,
  drives guardFraction, visionMult, speedMult, investigateMult, and
  minimap detail tier. Persists to `localStorage['bunker.skill.v1']`.
  Reset: `localStorage.removeItem('bunker.skill.v1'); location.reload()`.
- **Phase 12.1:** Input mode auto-switch — most-recent-input wins.
  Tap screen → touch UI back; press any controller input → touch UI
  hides. `setTouchMode(on)` is the single toggle for canvas resize +
  `body.gamepad-active` class.
- **Phase 12.2:** Post-hit recovery (iframes 60→120, knockback
  150→220, +25% speed during iframes) + touch ergonomics (FIRE
  button autofire-on-hold + aim direction persists 60 frames after
  release).
- **Phase 12.3:** Stick-base finger-anchor dropped. The OS-reported
  contact centroid sits below the visual thumb tip, so the base used
  to "jump down" on first touch. Now base stays put and the initial
  touch dx/dy is its offset from the base center.
- **Phase 12.4:** Touch redesign around aim-stick-as-trigger. Soft
  push (<0.7 mag) = silent peek; hard push (≥0.7) = autofire (gun)
  or cook (grenade). Drop below threshold or release = throw in
  grenade mode. NADE button is now a tap-toggle for weapon mode (not
  hold-to-cook), positioned inside the aim-zone right next to the
  aim stick. FIRE button removed on touch entirely. 15ms haptic at
  the threshold cross + colored dot at the player's gun barrel
  (amber → red, or green in grenade mode).
- **Phase 12.5:** On-screen pause button in the topbar (Esc/P/Start
  also still work — `syncTouchUi()` polls `state.paused` each frame
  to keep the glyph in sync regardless of input source). Plus
  aim-stick anchor-on-touch — touchdown point becomes the stick's
  origin so first contact reads (0,0) and never accidentally
  snap-fires when the thumb lands off-center. Move stick keeps
  base-center origin (it's not a fire trigger).
- **Phase 12.6:** Ammo budget bumped — start 25→45, max 45→80,
  pickup 15→25. Touch aim was making shootouts unwinnable.
  Stealth pressure stays intact via alertness on fire.
- **Phase 12.7:** Single-key diagonals on keyboard — Q=NW, E=NE,
  Z=SW, C=SE. Combos like W+D still work; magnitude clamped in
  `getMoveVector()` so combo keys don't double-speed.
- **Phase 12.8:** Mouse aim + LMB autofire on desktop. Cursor on
  canvas = gun direction; LMB held = continuous fire (matches
  touch hold-to-fire). Coordinates converted via
  `canvas.getBoundingClientRect()` so it stays correct across
  resizes. RMB context menu disabled on canvas. Cursor set to
  `crosshair`. (Later partially reverted in 12.17 — see below.)
- **Phase 12.9:** Slow body turn experiment for mouse aim. Reverted
  by 12.10 — body still ended at cursor, just delayed. Wrong fix.
- **Phase 12.10:** **Body fully decoupled from aim.** `p.dir` =
  body facing (movement-driven, last-faced when idle). `p.aimDir` =
  aim direction (driven by gamepad RS / touch aim / mouse / movement
  fallback). Bullets and grenades shoot from `p.aimDir`; sprite
  renders at `p.dir`. Added `drawAimLine()` — thin dotted cyan line
  from player toward `p.aimDir` with a small reticle dot at the end,
  hidden on touch (fire-ready dot already cues there) and in grenade
  mode (impact reticle is more informative).
- **Phase 12.11:** (later trimmed in 12.12) Razer Naga side-mouse
  buttons + Digit1-Equal as fire alternates.
- **Phase 12.12:** Trimmed 12.11. Now: `Digit1` = fire (alongside
  Space + LMB at the time), `Digit3` = grenade-mode toggle (mirrors
  G). Other Naga digits unbound — open for future actions.
- **Phase 12.13:** Searchable corpses (Castle Wolfenstein homage).
  New `rs.corpses[]` per room. On guard death, push corpse with
  pre-rolled loot (4-8 ammo + ~18% chance of a grenade). Walk
  within `SEARCH_R` and press Space → loot transfers to player,
  corpse marked looted. Rendered under live elements.
- **Phase 12.13.1:** Hotfix — `SEARCH_R = PLAYER_R + GUARD_R + 6`
  threw a TDZ ReferenceError because `GUARD_R` is declared later
  in the file. Inlined the value (30, then 50 in 12.17). See
  Lessons Learned.
- **Phase 12.14:** Corpse polish. (a) Fix Space-fire bug — the
  consumed flag now latches across frames until Space is released,
  so a held Space after search doesn't sneak a burst out next
  frame. (b) Loot flash duration 30→120 frames with a fade. (c)
  Blood-pool oval offset slightly toward facing direction with
  per-corpse size wobble.
- **Phase 12.15:** `assets/bodyblood.png` decal under each corpse
  (custom art Mike made in Photoshop, 64×64). Wired through the
  IMG/imgReady pipeline so missing/slow asset falls back to the
  procedural oval. **Process gotcha**: code commit and asset commit
  pushed separately diverged on the feature branch — landed as a
  merge commit instead of fast-forward. Next time, rebase the
  feature branch on main before pushing code that depends on a
  separate asset.
- **Phase 12.16:** Dropped the pulsing yellow "search me" ring on
  unlooted corpses. Random rotation + scale (0.85-1.2x) per blood
  splat, stored at death so a row of bodies doesn't read as cloned.
  Body sprite alpha bumped slightly (no ring competing).
- **Phase 12.17:** Three things in one ship.
  - `SEARCH_R` 30→50 — anywhere on the visible blood splat
    triggers Space-search.
  - **Single fire input on keyboard/mouse**: only `Digit1`
    (Razer Naga btn 1). Space and LMB dropped from fire — Space
    is search-only now (kills the search/fire conflict entirely),
    mouse is aim-only. Held Digit1 autofires (continuous mode) to
    match the old held-LMB feel. Gamepad and touch unchanged.
  - **Health backpack**: vials no longer auto-heal on walk-over.
    They go into `p.inv.health` (cap `HEALTH_INV_MAX = 5`); press
    `H` to consume one and +1 HP. Inventory persists across levels
    via `carryPlayer.inv`. HUD shows `+ N [H]` next to the hearts
    when carrying any.

Up next:

- **Phase 12.18 (settings UI):** Mike asked for it explicitly in
  the 12.17 session: "i'd also like to be able to change up my
  forward angle and strife keys" + "did we put in control settings
  yet". MVP scope: gear icon in topbar → modal listing actions
  (forward/back/left/right + 4 diagonals, fire, search, grenade
  toggle, heal, pause) and current bindings. Click an action →
  capture next keypress → save. Persist to localStorage. Reset to
  defaults button. Then refactor every hard-coded
  `keys['KeyW']` / `keys['Digit1']` into a binding lookup.
  Significant change — touches every input handler.
- **Phase 12.19+ (more backpack):** Speed-boost pickup is still
  auto-applied on walk-over (12.17 only converted health). If
  Mike wants symmetric behavior, move it to inventory + a use key
  (V?). Mike's exact words were "pick up all items and put them
  in our back-pack" — health was the main complaint, but he might
  want speed too once he sees how health feels.
- **Touch UX iteration:** Mike's last word on 12.4 was "getting
  closer." Session 2026-04-30 shifted entirely to desktop +
  keyboard + mouse + Naga, so touch tuning didn't get attention.
  Pick back up if/when Mike returns to tablet play.
- **Vibrate-on-android:** Still untested. `navigator.vibrate(15)`
  did NOT fire on Mike's Samsung tablet in 12.4. Debug list in
  Open Issues below — try first thing whenever touch-mode
  development resumes.
- **Phase 13:** Speed-run bonus rounds every N levels.
- **Phase 14:** Rename. Either rename `bunker.html` →
  `escape.html` (and update home page card) or keep filename and
  swap the in-game title. Mike's call.
- **Phase 15+:** PWA manifest. Capacitor native wrap. App store
  prep. Mobile build may opt into a richer sprite set (more tiles,
  character poses) — decision for later.

## bunker.html architecture (current — Phase 12.17)

Single file, ~4200 lines. `grep -n "function draw\|// =====" games/bunker.html`
is the fastest way to navigate. Key sections by header comment:

- **HTML/CSS** (lines 1–260): topbar (with on-screen pause button —
  12.5), canvas, two virtual thumbsticks (move + aim), NADE button
  overlay inside aim-zone. Topbar shows `PHASE N.M` indicator from
  `BUILD_LABEL` constant — single source. Canvas has
  `cursor: crosshair` (12.8).
- **Input merge:** keyboard, two touch thumbsticks (`touch` + `touchAim`),
  Gamepad API, **mouse** (`mouse.x/y/active/fire`, 12.8) → unified
  aim direction `p.aimDir`. Body direction `p.dir` is movement-driven
  only (12.10 decoupling). `getMoveVector()` produces normalized
  (vx, vy). `setTouchMode(on)` (12.1) is the single toggle for canvas
  resize + `body.gamepad-active`. Most-recent-input wins.
  - Fire on keyboard/mouse: **Digit1 only** (12.17). Held = autofire.
    Space is search-only. LMB is aim-only.
  - Search: Space (12.13). Edge-triggered, finds nearest unlooted
    corpse within `SEARCH_R = 50`, transfers loot.
  - Heal: H (12.17). Edge-triggered. Consumes one `p.inv.health`
    charge, +1 HP.
  - Grenade-mode toggle: G or Digit3 (Naga btn 3, 12.12).
- **Adaptive Director (12.0):** Module-level `directorState` recomputed
  in `buildStateFor()` from `currentSkillScore()` (avg of last
  `SKILL_HISTORY_N` completed-level scores from `localStorage`).
  Knobs: `guardFraction` (drops spawns at low skill), `visionMult`,
  `speedMult`, `investigateMult`, `minimapTier`. Reads in
  `makeGuardsForRoom()`, `guardVisionHalfNow()`, `guardPatrolSpeedNow()`,
  `guardInvestigateIntervalNow()`, `drawMinimap()`. `runStats` (transient,
  reset per level) tracks framesElapsed / hits / spotted, used at
  `recordLevelComplete()` to score the run.
- **Level data (`LEVEL_1`, `LEVEL_2`, `LEVEL_3`):** each level has
  `.rooms.{id}` with `map` (18×13 0/1 array), `doorways`, `guardSpawns`
  (with `type`), `keySpawns`, `pickupSpawns`, `exit`, and (start room)
  `playerSpawn`. 50px tile grid. Collision still uses the logical grid,
  not sprite bounds.
- **Helpers:** `currentRoom()`, `currentRoomState()`, `doorwayAt()`,
  `isWallAt()`, `tileToPx()`.
- **Guard AI:** wander patrol (forward-progress watchdog) → alert → chase
  → search → investigate. Grenade dodge behavior added in 11.7.
  Room-bound (no cross-room logic needed).
- **State:** `state.player`, `state.levelIndex`, `state.currentRoomId`,
  `state.rooms[id].{guards,bullets,grenades,keys,pickups,explosions,corpses}`,
  alertness, timer, transition, gameover. **Player has `dir` (body)
  and `aimDir` (aim) now (12.10).** Player carries `inv` (12.17 —
  health charges in the backpack, persists across levels).
- **Corpses (12.13):** `rs.corpses[]` per room. Pre-rolled loot
  (`{ammo, grenade, looted, lootFlash, bloodRot, bloodScale}`).
  Drawn under live elements via `drawCorpses()`.
- **`update()`**: freezes during gameover/transition. Handles movement,
  firing (bullets or grenade cook/throw), bullet/grenade physics, guards,
  pickups, damage, doorway transitions, **search (Space) and heal (H)**.
  Touch firing (12.4): `touchAimMag >= AIM_FIRE_THRESHOLD` (0.7) drives
  gun-mode autofire and grenade cook. Mouse fire path was removed in
  12.17 — fire on desktop = `keys['Digit1']`.
- **Draw:** `drawFloor()`, `drawCorpses()` (12.13, under live elements),
  `drawKeys()`, `drawPickups()`, `drawGuards()`, `drawBullets()`,
  `drawGrenades()`, `drawGrenadeAim()`, `drawAimLine()` (12.10 — desktop
  aim cue), `drawPlayer()`, `drawFireReadyDot()` (12.4 — touch only),
  `drawCookTimer()`, `drawExplosions()`, `drawHUD()`, `drawMinimap()`,
  overlays (gameover, level complete, times up, transition).

**Sprite system (art pass):** Near the top of the DRAW section, a small
`IMG` object + `loadImg()`/`imgReady()`/`drawChar()` preload and render
Kenney sprites. Every sprite-using draw call is gated on `imgReady(key)`
and falls back to the original procedural render — so a missing or
slow-loading image never blocks gameplay. 12.15 added `corpsePool`
keyed to `assets/bodyblood.png` (Mike's custom blood splat).

When adding new room-scoped state (new pickup type, etc.), put it in
`LEVELs[id].rooms[id]` (definition) AND in `state.rooms[id]` (runtime).
Mirror the guards/bullets/keys/pickups pattern.

**When you ship a build:** bump `BUILD_LABEL` (string) — the topbar +
HUD pull from it. Use `N.0` for new phase, `N.x` for refinement.

## Sprites / TD Shooter assets

Located at `assets/TD Shooter/` (601 files). Source: Kenney's Topdown
Shooter pack, **CC0 public domain** — free to use commercially, credit
optional. Per-file categories: `PNG/{Character Name}/`, `PNG/Tiles/`,
`Spritesheet/`, `Tilesheet/`, `Vector/`.

Currently used in `bunker.html`:
- Wall: `PNG/Tiles/tile_70.png` (orange ridged industrial panel)
- Player: `PNG/Survivor 1/survivor1_gun.png`
- Guard sprites by type: `Hitman 1` (patrol), `Soldier 1` (sentry),
  `Robot 1` (hunter), `Zombie 1` (alarm) — all the `_gun.png` variant.

**Gotchas:**
- Kenney topdown sprites face **RIGHT (east)** in source, matching our
  `dir = 0 = east` convention. **No rotation offset.** Don't add +π/2.
- Kenney misspelled "zombie" as `zoimbie` in filenames. Use literally.
- "TD Shooter" folder has a space — URL-encode as `TD%20Shooter` in paths.
- `Thumbs.db` files are in the commit (Windows artifact). Harmless.
- There is **no solid dark-gray floor tile** in the pack. All dark
  grays are wall-interior tiles with white borders that dominate when
  tiled. Floor stays procedural.

## Workflow

**Branch:** Default to whatever branch Mike's session hands you.
Before editing, `git merge-base --is-ancestor origin/main <branch>` —
if it fails, the branch is behind main and needs `git merge main` first,
or cherry-pick onto main instead. Skipping this step causes merge pain
when the work lands on main.

**Per-phase loop:**
1. Read current `bunker.html` (Mike may have made manual edits)
2. Confirm scope + tuning details with Mike before coding
3. Build the phase, syntax-check (`node --check` on extracted JS)
4. Commit + push
5. Mike pulls, tests at `arcadereactor.com/games/bunker.html`
6. If good → he merges to main (or asks Claude to)
7. Update CLAUDE.md if architecture changed

**Syntax check:**
```bash
awk '/<script>/,/<\/script>/' games/bunker.html | grep -v '^<script>\|^</script>' > /tmp/check.js && node --check /tmp/check.js
```

## Lessons learned (don't repeat)

1. **Grid navigation was designed but never shipped.** Previous
   chat's handoff claimed "grid nav for patrol" was current.
   Reality: latest commit was a forward-progress watchdog.
   The grid-nav approach (guards walk cardinal-only, decide at
   tile centers) was a good idea — revisit when tackling guard
   movement properly. With room containment now in place, this is
   a smaller problem.
2. **Don't bolt features onto bug fixes.** Surgical fixes ship
   clean; combo fixes break things.
3. **Validate map data before claiming done.** Waypoint endpoints
   on floor isn't enough — segments between waypoints need to
   clear walls too. Same applies to keys: spawn position must be
   on floor AND not on a doorway tile AND ideally not adjacent to
   the player spawn.
4. **A single open map is a tech demo, not a game.** Mike pushed
   back hard on "one room with a key and a door." Layered systems
   per snake's design bar.
5. **Don't argue past the user's clarifying point.** When Mike
   says "you must be misunderstanding something," he's usually
   right and I'm describing a different model than he's picturing.
6. **Verify sprite orientation by looking at the file, not assuming.**
   Kenney's topdown shooter sprites face RIGHT, not up. I assumed up,
   added +π/2 rotation, and every character walked sideways on first
   ship. Fix was trivial (remove the offset) but avoidable — Read the
   actual PNG once before picking a rotation formula.
7. **Don't trust that a "development branch" is ancestor-of-main
   without checking.** Phases 11.5–11.7 went direct to main and were
   never back-merged to `claude/arcade-reactor-handoff-mwRLq`, so when
   we pushed the art pass to handoff then tried to merge → conflict.
   Fix was a cherry-pick onto main. See Workflow section above for
   the check to do before editing.
8. **Don't write `const X = Y + Z` at module top if Y or Z is
   declared further down.** TDZ — `const`/`let` are hoisted but
   their values aren't. The reference throws a ReferenceError at
   parse-evaluate time and halts the entire script → blank screen.
   Bit me in 12.13 (`SEARCH_R = PLAYER_R + GUARD_R + 6`; GUARD_R
   declared a thousand lines later). `node --check` catches grammar
   but not runtime TDZ, so syntax-pass means nothing here. Fix:
   inline the literal, or move the declaration after its dependencies.
9. **When a code commit depends on Mike's separate asset commit,
   rebase or wait for the asset before pushing.** 12.15 had me
   wire `bodyblood.png` and push the code; meanwhile Mike pushed
   the asset to main. Histories diverged → ended up as a merge
   commit instead of fast-forward. Either: wait for the asset to
   land before pushing the code (and rebase if main moved), or
   coordinate so both go in the same push.
10. **When user says "I have N ways to fire" they mean drop the
    extras.** Don't preserve "all known fire inputs" out of
    over-cautious convenience. 12.11 bound Digit1-Equal as fire
    "covering all the Naga keys"; 12.12 trimmed to Digit1+Digit3;
    12.17 trimmed to Digit1 only when Mike said "i should only
    have 1." Picking ONE is almost always what the user wants;
    map other physical buttons to that one keybind via the
    settings UI (or, today, via Razer Synapse).

## Scope guidance

The previous handoff's "one phase per chat" rule was set by Mike
in a past session. He'll waive it when he's in flow (he did this
chat — built Phase 5, then asked to keep going). Defer to him.

What to actually hold the line on:
- Don't build features beyond the agreed phase scope mid-build.
  ("Oh while you're in there, also add X" → "next phase".)
- Don't redesign architecture mid-phase.
- Bug fixes in the current build are always fair game.

## Open issues / specific asks

**Active (next session):**

- **Settings UI for key remap.** Mike's explicit ask: "i'd also
  like to be able to change up my forward angle and strife keys"
  + "did we put in control settings yet". MVP scope in "Up next"
  → Phase 12.18 above. Significant change — touches every input
  handler that currently reads `keys['KeyW']` etc. Worth doing
  before adding more actions because every new keybind compounds
  the migration cost.
- **Speed-boost pickup is still auto-applied on walk-over.** 12.17
  converted health to inventory but skipped speed. Mike said "pick
  up all items and put them in our back-pack" — speed is the
  obvious follow-up. Suggest V or some other unused key to consume
  one charge.
- **Haptic vibrate didn't fire on Mike's Android tablet (12.4).** Code
  is `if (touchAimFire && !lastTouchAimFire && navigator.vibrate) navigator.vibrate(15)`.
  Possible causes to check:
  - Some Android browsers gate vibrate behind a recent user-gesture
    activation — should be fine inside touch handlers but test
  - Samsung tablets sometimes have a system "Vibration feedback" toggle
    in Sound settings that has to be on for web vibrate to do anything
  - Chrome may silently no-op `navigator.vibrate` on certain devices
    when battery saver is on
  - Console-log inside the threshold-cross block to confirm the call
    is even reached, then add a diag overlay if it is
- **Touch UX still iterating.** 12.4 was "getting closer" not "done."
  The 2026-04-30 session was almost entirely desktop/keyboard/mouse
  + Naga focus, so touch tuning didn't get attention. Pick back up
  if/when Mike returns to tablet play.

**Backlog (long-running):**

- "Trifecta-style" hidden bonuses (consider once core is fun)
- Heading-bar inconsistency on sprite-rendered guards (the procedural
  fallback draws a white direction bar; sprite path doesn't). Mike
  hasn't said it bothers him. Skip unless asked.
- Swap the survivor character sprite if the gun-side reads wrong
  (try `manBlue_gun` or `soldier1_gun` — Mike will say)
- Branch hygiene: `claude/arcade-reactor-handoff-mwRLq` is still
  stuck behind main with an aborted merge ghost in Mike's local
  (we ran `git merge --abort` mid-session 2026-04-26 to clear it).
  Either delete it (`git push origin --delete claude/arcade-reactor-handoff-mwRLq`)
  or fast-forward it to main. Mike's call.
- The `claude/pause-button-stick-input-gcQw2` feature branch from
  the 2026-04-30 session is at parity with main — safe to delete
  whenever convenient.
- Rename `bunker.html` → `escape.html` (Phase 14)

## Session end log

**2026-04-24 (art pass):** Imported Kenney TD Shooter asset pack,
did a minimal art pass on bunker (walls, player, guards → sprites;
floor stays procedural). Shipped to main: commits `ced1203`, `273bd69`,
`d5270b7`. Tablet confirmed working. Parked for the night.

**2026-04-26 (Phases 11.8 → 12.4):** Big session. Branch:
`claude/phase-11-12-cleanup-FLhSi`. Mike merged each phase to main
incrementally with `git merge --ff-only`.
- `7494a9c` — Phase 11 cleanup: dropped dead floor-sprite path +
  unused `rayDistToWall()` helper
- `7689c99` — Phase 11.8: twin-stick touch + NADE button
- `d67032b` — Phase 12.0: adaptive director (skill, knobs, minimap tier)
- `d5cd5c2` — Phase 12.1: input mode auto-switch (touch ↔ gamepad)
- `6ce4a4b` — Phase 12.2: post-hit recovery (iframes 60→120,
  knockback 150→220, +25% iframe speed) + touch fire/aim ergonomics
- `0de08ee` — Phase 12.3: dropped stick finger-anchor (fixed
  "jumps down" on first touch)
- `4fc10c7` — Phase 12.4: aim-stick threshold trigger, NADE inside
  aim-zone, gun-tip color cue, haptic on threshold cross
- During session we cleared an old aborted merge in Mike's local
  (`git merge --abort` on `claude/arcade-reactor-handoff-mwRLq`).
  That branch is still on its old commit on the remote.
- Mike's last word: "we are getting closer. there was no vibrate."
  Vibration debug + further touch tuning is the first task next time.

**2026-04-30 (Phases 12.5 → 12.17):** Long session, all
desktop/keyboard/mouse focused. Mike played from his Windows
PC with a Razer Naga. Branch:
`claude/pause-button-stick-input-gcQw2`. Most phases ff-merged
to main; 12.15 ended up as a merge commit due to asset/code split
push (see Lesson #9). All shipped commits:
- `9b4dfda` — 12.5: on-screen pause button + aim-stick anchor-on-touch
- `ce1203f` — 12.6: ammo budget bump (45/80/25)
- `9042dae` — 12.7: Q/E/Z/C single-key diagonals
- `15518ce` — 12.8: mouse aim + LMB autofire
- `842f64b` — 12.9: slow body turn (reverted in 12.10)
- `ce6f6a7` — 12.10: decouple body from aim + aim line
- `4d98a6b` — 12.11: Naga / side-mouse fire bindings
- `d5e1440` — 12.12: trim to Digit1=fire, Digit3=grenade
- `12ca32c` — 12.13: searchable corpses (ammo + grenade loot)
- `52f2e54` — 12.13.1: hotfix SEARCH_R TDZ blank screen
- `35a0a99` — 12.14: Space-fire latch fix + longer flash + blood pool
- `aa4632e` — 12.15 merge: bodyblood.png decal (Mike's PS asset)
- `308e485` — 12.16: drop search ring + randomize blood splat
- `9c4b385` — 12.17: SEARCH_R 50, single-fire (Digit1 only),
  health backpack + H-to-heal

Big arc of the session: rebuilding the desktop input model from
scratch after Mike pointed out keyboard had no way to aim
independent of movement. Tried mouse-aim (12.8) → tried slow
body turn for "realism" (12.9) → realized that wasn't right →
fully decoupled body from aim with separate `p.aimDir` (12.10).
Then built corpse-loot system (12.13-12.16) hitting on Castle
Wolfenstein. Then trimmed fire inputs from 3 to 1 + introduced
backpack inventory (12.17).

End of session: settings UI for key remap is the explicit next
ask. Mike paused to start a new chat after CLAUDE.md update.
