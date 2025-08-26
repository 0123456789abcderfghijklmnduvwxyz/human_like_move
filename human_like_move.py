def human_like_move(
    x: int,
    y: int,
    duration: float,
    fps: int = 240,
    curvature: float = 0.15,
    jitter: float = 0.04,              # fraction of distance
    jitter_px_cap: float = 16.0,       # how many pixels it's allowed to jiggle at maximum i think
    jitter_min_px: float = 0.0,        # e.g., set to 1–2 px to see jitter on short moves
    jitter_decay: float = 1.0,         # was 1.5; 0.0 = constant amplitude
    jitter_cycles=(1.5, 3.0),          # was ~1 cycle; try 1.5–3 for visible wiggle
):
    import math, random, time, pyautogui
    if duration <= 0:
        pyautogui.moveTo(x, y, duration=0)
        return

    start_x, start_y = pyautogui.position()
    dx, dy = x - start_x, y - start_y
    dist = math.hypot(dx, dy)
    if dist < 0.5:
        pyautogui.moveTo(x, y, duration=0)
        return

    dir_x, dir_y = dx / dist, dy / dist
    ortho_x, ortho_y = -dir_y, dir_x

    # Bezier arc (unchanged)
    along = min(max(dist * 0.25, 30.0), 300.0)
    arc = curvature * min(dist * 0.25, 120.0) * random.choice([-1.0, 1.0])
    c1x = start_x + dir_x * along + ortho_x * arc * 0.5
    c1y = start_y + dir_y * along + ortho_y * arc * 0.5
    c2x = x - dir_x * along + ortho_x * arc
    c2y = y - dir_y * along + ortho_y * arc

    def bezier(s: float):
        inv = 1.0 - s
        b0 = inv * inv * inv
        b1 = 3.0 * inv * inv * s
        b2 = 3.0 * inv * s * s
        b3 = s * s * s
        bx = b0 * start_x + b1 * c1x + b2 * c2x + b3 * x
        by = b0 * start_y + b1 * c1y + b2 * c2y + b3 * y
        return bx, by

    def min_jerk(u: float):
        u = max(0.0, min(1.0, u))
        u2 = u * u
        u3 = u2 * u
        u4 = u3 * u
        u5 = u4 * u
        return 10.0 * u3 - 15.0 * u4 + 6.0 * u5

    # Updated wobble
    max_wobble = min(dist * max(jitter, 0.0), jitter_px_cap)
    max_wobble = max(max_wobble, jitter_min_px)
    phase1 = random.uniform(0, 2 * math.pi)
    phase2 = random.uniform(0, 2 * math.pi)
    base_freq = random.uniform(*jitter_cycles)

    fps = int(max(30, min(fps, 480)))
    dt = 1.0 / fps
    start_t = time.perf_counter()
    end_t = start_t + duration
    next_t = start_t

    old_pause = pyautogui.PAUSE
    old_min_dur = getattr(pyautogui, "MINIMUM_DURATION", 0.0)
    old_min_sleep = getattr(pyautogui, "MINIMUM_SLEEP", 0.0)
    pyautogui.PAUSE = 0
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0

    try:
        while True:
            now = time.perf_counter()
            if now >= end_t:
                break

            u = (now - start_t) / duration
            s = min_jerk(u)
            bx, by = bezier(s)

            if max_wobble > 0.0:
                wobble_env = (1.0 - s) ** jitter_decay
                w = (
                    math.sin(2 * math.pi * base_freq * s + phase1)
                    + 0.35 * math.sin(2 * math.pi * base_freq * 2.0 * s + phase2)
                ) * max_wobble * wobble_env
                bx += ortho_x * w
                by += ortho_y * w

            pyautogui.moveTo(bx, by, duration=0)

            next_t += dt
            sleep_for = next_t - time.perf_counter()
            if sleep_for > 0:
                time.sleep(sleep_for)

        now = time.perf_counter()
        if now < end_t:
            time.sleep(end_t - now)
        pyautogui.moveTo(x, y, duration=0)
    finally:
        pyautogui.PAUSE = old_pause
        pyautogui.MINIMUM_DURATION = old_min_dur
        pyautogui.MINIMUM_SLEEP = old_min_sleep
