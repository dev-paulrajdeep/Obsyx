# Obsyx Desktop Hardware Profiles Architecture

Obsyx provides a modular hardware/form-factor profile architecture that specializes compositor graphics parameters, Waybar layouts, and telemetry instruments according to the host system's hardware profile and power constraints.

---

## Available Canonical Profiles

### 1. `laptop` (Mobile & Battery Conservative)
Designed for laptops, portable devices, and battery-sensitive workflows.

- **Compositor Rendering:**
  - **Blur:** Single pass (`passes = 1`, `size = 4`, `vibrancy = 0.15`), substantially reducing GPU compositing overhead on integrated graphics.
  - **Shadows:** Completely disabled to eliminate shadow draw calls.
  - **Refresh Rate:** Variable Frame Rate enabled (`vfr = true`), Variable Refresh Rate disabled (`vrr = 0`).
- **Waybar Configuration:**
  - **Compact Geometry:** Bar height reduced to `32px` with tight margins (`6px` top, `8px` horizontal) to maximize vertical workspace on 13"–16" screens.
  - **Power-Aware Telemetry:** Includes battery and volume monitors while omitting always-polling dedicated GPU query scripts to prevent waking up discrete GPUs while on battery.

### 2. `workstation` (High-Fidelity Desktop)
Designed for desktop workstations, high-refresh multi-monitor setups, and dedicated GPU machines.

- **Compositor Rendering:**
  - **Blur:** High-fidelity multi-pass blur (`passes = 3`, `size = 8`, `vibrancy = 0.35`) delivering deep frosted glass aesthetics.
  - **Shadows:** Ambient drop shadows enabled (`range = 24`, `render_power = 3`).
  - **Refresh Rate:** Variable Refresh Rate enabled (`vrr = 1`) for fluid gameplay and high-Hz monitor sync.
- **Waybar Configuration:**
  - **Spacious Geometry:** Full `40px` height with generous margins (`12px`).
  - **Expanded Instrument Cluster:** Full system monitoring including dedicated GPU utilization (`custom/gpu`), CPU core meters, memory, network, and VPN monitors.

---

## Profile CLI Management (`obsyx profile`)

Profiles are managed directly via the `obsyx profile` subcommand.

### 1. List Available Profiles
```bash
./bin/obsyx profile list
```
Displays all canonical profiles, their feature matrix, and marks the currently active profile (`● ACTIVE`).

Emits JSON with `--json`:
```bash
./bin/obsyx profile list --json
```

### 2. Inspect Profile Details
```bash
./bin/obsyx profile show laptop
./bin/obsyx profile show workstation
```
Displays detailed parameter tuning including blur passes, shadow settings, VRR state, and Waybar height.

### 3. Apply a Profile
```bash
# Apply laptop profile to user dotfiles (~/.config)
./bin/obsyx profile apply laptop

# Dry-run simulation (makes zero filesystem changes)
./bin/obsyx profile apply laptop --dry-run

# Apply to isolated sandbox destination
./bin/obsyx profile apply laptop --dest /tmp/test-config
```

When applied:
1. Deploys Hyprland configuration override to `<dest>/hypr/config/profile.lua` and `<dest>/obsyx/profile.lua`.
2. Deploys specialized Waybar layout and stylesheet overrides to `<dest>/waybar/config.jsonc` and `<dest>/waybar/profile-style.css`.
3. Records active profile metadata into `<dest>/.obsyx_profile`.
4. Automatically triggers live reload (`hyprctl reload` and `pkill -SIGUSR2 waybar`) if running within an active Wayland session.
