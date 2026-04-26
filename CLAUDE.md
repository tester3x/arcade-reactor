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
  (amber → red, or green in grenade mode). **Status: getting closer
  but not done.** See "Specific things he's asked for" below.

Up next:

- **Phase 12 polish:** Touch UX iteration. Mike's last word on 12.4
  was "getting closer" and "lets call it." `navigator.vibrate(15)`
  did NOT fire on his Android tablet — debug first thing next
  session (see Open issues). Probably more aim-stick tuning to come.
- **Phase 13:** Speed-run bonus rounds every N levels.
- **Phase 14:** Rename. Either rename `bunker.html` →
  `escape.html` (and update home page card) or keep filename and
  swap the in-game title. Mike's call.
- **Phase 15+:** PWA manifest. Capacitor native wrap. App store
  prep. Mobile build may opt into a richer sprite set (more tiles,
  character poses) — decision for later.

## bunker.html architecture (current — Phase 12.4)

Single file, ~3700 lines. `grep -n "function draw\|// =====" games/bunker.html`
is the fastest way to navigate. Key sections by header comment:

- **HTML/CSS** (lines 1–230): topbar, canvas, two virtual thumbsticks
  (move + aim), NADE button overlay inside aim-zone. Topbar shows
  `PHASE N.M` indicator from `BUILD_LABEL` constant — single source.
- **Input merge:** keyboard, two touch thumbsticks (`touch` + `touchAim`),
  Gamepad API → unified vector. `getMoveVector()` produces normalized (vx, vy).
  `setTouchMode(on)` (12.1) is the single toggle for canvas resize +
  `body.gamepad-active`. Most-recent-input wins.
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
  `state.rooms[id].{guards,bullets,grenades,keys,pickups,explosions}`,
  alertness, timer, transition, gameover.
- **`update()`**: freezes during gameover/transition. Handles movement,
  firing (bullets or grenade cook/throw), bullet/grenade physics, guards,
  pickups, damage, doorway transitions. Touch firing (12.4): `touchAimMag`
  >= `AIM_FIRE_THRESHOLD` (0.7) drives both gun-mode autofire and
  grenade cook. NADE tap is a mode-toggle.
- **Draw:** `drawFloor()` (floor + walls + doorway tints + exit door),
  `drawGuards()` (cones + bodies + state icons), `drawPlayer()`,
  `drawFireReadyDot()` (12.4: gun-tip color cue for touch), `drawBullets()`,
  `drawGrenades()`, `drawKeys()`, `drawPickups()`, `drawHUD()`, `drawMinimap()`,
  overlays (gameover, level complete, times up, transition).

**Sprite system (art pass):** Near the top of the DRAW section, a small
`IMG` object + `loadImg()`/`imgReady()`/`drawChar()` preload and render
Kenney sprites. Every sprite-using draw call is gated on `imgReady(key)`
and falls back to the original procedural render — so a missing or
slow-loading image never blocks gameplay.

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
  Watch what specifically still feels awkward when Mike comes back.

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
