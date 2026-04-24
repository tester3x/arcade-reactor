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

**Deploy flow:** GitHub Pages serves from `main`. Mike develops on
the feature branch `claude/arcade-reactor-handoff-mwRLq`, pulls
locally to test, then merges to main → Pages redeploys in 1-2 min.

## Games

- **`games/space-rocks.html`** — Asteroids clone. Shipped, stable.
- **`games/web-reactor.html`** — Tempest-like lane shooter. Shipped, stable.
- **`games/bunker.html`** — Active development. **This is where all
  current work happens.** Becoming "Escape" — a top-down stealth/
  combat game (see below).

## Shared patterns (every game uses these)

- 48px fixed top bar with back link, title, score area
- 900×650 logical canvas, scaled to viewport
- Input merge: keyboard + virtual thumbstick + Gamepad API every
  frame into one input vector
- Standard gamepad mapping. Axes[0]=LX, Axes[1]=LY. Btn 0=A/fire,
  Btn 9=Start. `body.gamepad-active` class hides touch controls
  when controller is connected
- Pause: Esc/P/gamepad Start

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

- **Phase 1-4:** Player movement, walls, guards, combat, HP, game
  over (in `bunker.html`).
- **Phase 5 ✓ shipped:** Screen-based room architecture. `LEVEL_1`
  has 3 rooms (A↔B↔C) with per-room maps, doorways, guards.
  Fade transitions on doorway entry. Per-room state persistence
  (guards stay where they were when you re-enter a room).

Up next:

- **Phase 6:** First playable level. Keys (3 scattered across
  rooms), exit door in Room C (locked until all keys collected),
  WIN overlay, basic fog-of-war minimap (top corner).
- **Phase 7:** Pickups (health, speed boost) + limited ammo.
- **Phase 8:** Countdown timer (3 min default, color shift as it
  drops, "TIME'S UP" overlay).
- **Phase 9:** Global alertness system. Shooting raises alertness
  → guards get wider cones + faster patrols + shorter investigate
  cooldowns.
- **Phase 10:** New guard types. Sentry (stationary, wide cone),
  hunter (faster), alarm-raiser (alerts whole level on spot).
- **Phase 11:** Multi-level. Levels 2, 3, 4+ with bigger maps,
  more rooms, more guards.
- **Phase 12:** Adaptive director. Reads player skill, tunes
  difficulty knobs + adaptive minimap detail.
- **Phase 13:** Speed-run bonus rounds every N levels.
- **Phase 14:** Rename. Either rename `bunker.html` →
  `escape.html` (and update home page card) or keep filename and
  swap the in-game title. Mike's call.
- **Phase 15+:** PWA manifest. Capacitor native wrap. App store
  prep.

## bunker.html architecture (current — Phase 5)

Single file, ~1500 lines. Key sections:

- **HTML/CSS** (lines 1-216): topbar, canvas, virtual thumbstick,
  styles. Topbar shows `PHASE N` indicator — bump when phase
  changes.
- **Input merge** (~lines 260-490): keyboard, touch thumbstick,
  Gamepad API → unified `keys{}`, `touch{}`, `pad{}`. `getMoveVector()`
  produces normalized (vx, vy).
- **`LEVEL_1`** (~line 525): the room data. `LEVEL_1.rooms.{A,B,C}`
  each contain: `map` (2D 0/1 array, 18 cols × 13 rows), `doorways`
  (array of `{x,y,toRoom,toX,toY}`), `guardSpawns` (array of
  `{x,y}` in tile coords), and (for start room) `playerSpawn`.
- **Helpers** (~lines 608-655): `currentRoom()` returns the active
  room definition, `currentRoomState()` returns the active runtime
  state (guards + bullets), `doorwayAt(col,row)` checks transition
  triggers, `isWallAt(x,y)` samples the current room's map,
  `tileToPx(tx,ty)` converts tile coords to pixel center.
- **Guard AI** (~lines 660-950): unchanged from Phase 4. Wander
  patrol with forward-progress watchdog, alert→chase→search cycle,
  investigate behavior. Per-guard, no cross-room logic needed
  (rooms isolate guards naturally).
- **State** (~lines 1000-1022): `state.player`, `state.currentRoomId`,
  `state.rooms[id].guards`, `state.rooms[id].bullets`,
  `state.transition` (null or `{t, phase, toRoom, toX, toY}`),
  `state.gameover`, `state.gameoverT`.
- **`update()`** (~line 1068): freezes during gameover and during
  active transition. After movement, checks for doorway tile under
  player → starts transition. Otherwise: firing, bullets, guards,
  player damage. All loops use `currentRoomState()`.
- **Draw** (~line 1195+): `drawFloor()` renders current room's map
  + doorway tints, `drawGuards()` and `drawBullets()` only render
  current room's, `drawTransition()` overlays black fade when
  transitioning, `drawGameOver()` for death.

When adding new room-scoped state (e.g., keys in Phase 6), put it
in `LEVEL_1.rooms[id]` (definition: where keys spawn) AND in
`state.rooms[id]` (runtime: which keys remain). Mirror the
guards/bullets pattern.

## Workflow

**Branch:** `claude/arcade-reactor-handoff-mwRLq` for development.
Mike merges to main when phase is verified.

**Per-phase loop:**
1. Read current `bunker.html` (Mike may have made manual edits)
2. Confirm scope + tuning details with Mike before coding
3. Build the phase, syntax-check (`node --check` on extracted JS)
4. Commit + push to feature branch
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

## Scope guidance

The previous handoff's "one phase per chat" rule was set by Mike
in a past session. He'll waive it when he's in flow (he did this
chat — built Phase 5, then asked to keep going). Defer to him.

What to actually hold the line on:
- Don't build features beyond the agreed phase scope mid-build.
  ("Oh while you're in there, also add X" → "next phase".)
- Don't redesign architecture mid-phase.
- Bug fixes in the current build are always fair game.

## Specific things he's asked for that aren't built yet

- Door sprite (Phase 6+ has a door but visual treatment TBD)
- Adaptive difficulty (Phase 12)
- "Trifecta-style" hidden bonuses (consider once core is fun)
- **Destructible secret walls with caches** (11.8+): blowable
  wall tiles that reveal hidden loot (ammo / bandage / grenade
  pickups) when a grenade detonates adjacent. Needs a new tile
  kind (e.g. `2` = breakable wall) and a cache spawn table per
  level
- Aim assist for grenades (Halo-style magnetism) — floated but
  never built; Mike suggested it'd help him specifically
- Touch-mode grenade button + cook support for the tablet
  (currently gamepad/keyboard only)
- **Tanks** — new game, Atari Combat clone. Top-down, 2 tanks,
  walls. Fits the codebase pattern
- Delta-time movement refactor (pixels/sec instead of px/frame)
  once the FPS counter confirms tablets run below 60
