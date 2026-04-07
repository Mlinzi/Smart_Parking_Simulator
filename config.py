SCREEN_W = 1100
SCREEN_H = 720
FPS      = 60
TITLE    = "Smart Parking Simulator"

# ── Colours ─────────────────────────────────────────────────────────────────────
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0  )
GRAY      = (150, 150, 150)
DARK_GRAY = (42,  44,  50 )
GREEN     = (55,  210, 88 )
RED       = (215, 52,  52 )
YELLOW    = (240, 210, 20 )
BLUE      = (52,  128, 228)
ORANGE    = (225, 138, 28 )
ASPHALT   = (66,  68,  74 )
ROAD_COL  = (82,  84,  92 )
CURB_COL  = (122, 118, 105)
MARKING   = (232, 228, 152)
SLOT_FREE = (32,  148, 70 )
SLOT_OCC  = (148, 32,  32 )
PANEL_BG  = (12,  16,  28 )
PANEL_HL  = (0,   208, 148)
PANEL_DIM = (88,  92,  112)
LED_ON_G  = (0,   255, 80 )
LED_ON_R  = (255, 58,  58 )

AISLE_COL    = (55,  57,  64 )
INT_ROAD_COL = (76,  78,  86 )

# ── External road (VERTICAL strip on the LEFT of the lot) ────────────────────────
ROAD_X        = 10     # left edge of vertical road strip
ROAD_W        = 85     # road width  (two lanes side-by-side)

# Lane centres on the vertical road
ROAD_ENTRY_LX = ROAD_X + ROAD_W // 4          # 31  entry lane (cars travel UP)
ROAD_EXIT_LX  = ROAD_X + 3 * ROAD_W // 4      # 73  exit lane  (cars travel DOWN)

# ── Lot ─────────────────────────────────────────────────────────────────────────
LOT_X = ROAD_X + ROAD_W + 10   # 105  (gap of 10 between road and lot)
LOT_Y = 40

SLOT_DEPTH = 110
SLOT_W     = 52
SLOT_GAP   = 5
N_ROWS     = 8
N_COLS     = 4
AISLE_W    = 130
WALL_PAD   = 10

# ── Column X positions ───────────────────────────────────────────────────────────
COL0_X   = LOT_X + WALL_PAD          # 115
AISLE0_X = COL0_X  + SLOT_DEPTH      # 225
COL1_X   = AISLE0_X + AISLE_W        # 355
COL2_X   = COL1_X   + SLOT_DEPTH     # 465
AISLE1_X = COL2_X   + SLOT_DEPTH     # 575
COL3_X   = AISLE1_X + AISLE_W        # 705

LOT_W = COL3_X + SLOT_DEPTH + WALL_PAD - LOT_X   # 720

COL_X = (COL0_X, COL1_X, COL2_X, COL3_X)

# Lane centres inside each aisle
AISLE0_ENTRY_LX = AISLE0_X + AISLE_W // 4          # 257  (entry / UP lane)
AISLE0_EXIT_LX  = AISLE0_X + 3 * AISLE_W // 4      # 322  (exit  / DOWN lane)
AISLE1_ENTRY_LX = AISLE1_X + AISLE_W // 4          # 607
AISLE1_EXIT_LX  = AISLE1_X + 3 * AISLE_W // 4      # 672

# ── Row Y positions ─────────────────────────────────────────────────────────────
SLOT_AREA_TOP    = LOT_Y + 12                        # 52
SLOT_STEP_Y      = SLOT_W + SLOT_GAP                 # 57
SLOT_AREA_H      = N_ROWS * SLOT_STEP_Y - SLOT_GAP   # 451
SLOT_AREA_BOTTOM = SLOT_AREA_TOP + SLOT_AREA_H        # 503

# ── Internal horizontal road (inside lot, bottom of slot area) ───────────────────
INT_ROAD_H      = 100
INT_ROAD_TOP    = SLOT_AREA_BOTTOM + 6                    # 509
INT_ROAD_CY     = INT_ROAD_TOP + INT_ROAD_H // 2          # 559
INT_ROAD_BOTTOM = INT_ROAD_TOP + INT_ROAD_H                # 609

# Lane centres at ¼ road-height from centreline → 50 px apart.
# CAR_W = 38 px, so passing clearance = 50 - 38 = 12 px each side.
INT_ROAD_ENTRY_Y = INT_ROAD_CY - INT_ROAD_H // 4   # 534  (upper / eastward lane)
INT_ROAD_EXIT_Y  = INT_ROAD_CY + INT_ROAD_H // 4   # 584  (lower / westward lane)

LOT_H = INT_ROAD_BOTTOM - LOT_Y + 10  # 559

# ── Gate Y positions (where the vertical road meets the internal horizontal road) ─
ENTRY_GATE_Y = INT_ROAD_ENTRY_Y   # 536  cars enter the lot at this Y
EXIT_GATE_Y  = INT_ROAD_EXIT_Y    # 562  cars exit  the lot at this Y

# ── Spawn / despawn positions on the vertical road ──────────────────────────────
ROAD_SPAWN_Y     = LOT_Y + LOT_H + 60    # 659  cars appear here (below lot)
ROAD_OFFSCREEN_Y = SCREEN_H + 80         # 800  cars disappear here (off bottom)

# ── Cars ─────────────────────────────────────────────────────────────────────────
CAR_W, CAR_H = 38, 58
CAR_SPEED    = 110

# ── Timing ──────────────────────────────────────────────────────────────────────
SPAWN_MIN, SPAWN_MAX = 2.0, 5.0
PARK_MIN,  PARK_MAX  = 8.0, 22.0

# ── Panel ────────────────────────────────────────────────────────────────────────
PANEL_X = LOT_X + LOT_W + 20   # 845
PANEL_Y = LOT_Y
PANEL_W = SCREEN_W - PANEL_X - 12   # 243
PANEL_H = LOT_H
