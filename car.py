import pygame
import math
from config import *

# ── States ─────────────────────────────────────────────────────────────────────
MOVING    = "moving"     # following entry waypoints toward slot
PARKED    = "parked"     # stationary in slot, park timer counting
DEPARTING = "departing"  # timer expired; lot will set up exit when aisle is clear
EXITING   = "exiting"    # following exit waypoints out of lot
EXITED    = "exited"     # off-screen, safe to remove

_PALETTE = [
    (220, 80,  80 ),
    (80,  130, 225),
    (80,  195, 110),
    (220, 175, 55 ),
    (170, 80,  220),
    (220, 135, 55 ),
    (55,  205, 210),
    (220, 95,  170),
]


class Car:
    _counter = 0

    def __init__(self, slot_index):
        Car._counter += 1
        self.id          = Car._counter
        self.slot_index  = slot_index
        self.color       = _PALETTE[(self.id - 1) % len(_PALETTE)]
        self.path_type   = "left"   # "left" or "right" aisle

        self.state        = MOVING
        self.waypoints    = []
        self.wp_idx       = 0

        self.x = float(ROAD_ENTRY_LX)
        self.y = float(ROAD_SPAWN_Y)

        self.park_timer    = 0.0
        self.park_duration = 0.0

        self._dx = 0.0
        self._dy = -1.0   # initially facing up

    # ── Path builders ───────────────────────────────────────────────────────────
    def set_entry_path(self, slot):
        # Cars spawn on the vertical road on the LEFT, drive UP to the entry gate,
        # then turn RIGHT into the lot's internal horizontal road, then UP the aisle.
        self.x = float(ROAD_ENTRY_LX)
        self.y = float(ROAD_SPAWN_Y)

        if slot.col < 2:    # left aisle
            self.path_type = "left"
            self.waypoints = [
                (ROAD_ENTRY_LX,    ENTRY_GATE_Y),       # drive UP to entry gate
                (AISLE0_ENTRY_LX,  ENTRY_GATE_Y),       # turn RIGHT to left aisle entry lane
                (AISLE0_ENTRY_LX,  slot.cy),            # drive UP left entry lane
                (slot.cx,          slot.cy),            # turn into slot
            ]
        else:               # right aisle
            self.path_type = "right"
            self.waypoints = [
                (ROAD_ENTRY_LX,    ENTRY_GATE_Y),       # drive UP to entry gate
                (AISLE1_ENTRY_LX,  ENTRY_GATE_Y),       # turn RIGHT across internal road
                (AISLE1_ENTRY_LX,  slot.cy),            # drive UP right entry lane
                (slot.cx,          slot.cy),            # turn into slot
            ]
        self.wp_idx = 0

    def set_exit_path(self, slot):
        # Cars back out to exit lane, drive DOWN to internal road level,
        # turn LEFT (westward) through the exit gate, then DOWN the vertical road.
        if slot.col < 2:    # left aisle
            self.waypoints = [
                (AISLE0_EXIT_LX,  slot.cy),             # pull back to left exit lane
                (AISLE0_EXIT_LX,  EXIT_GATE_Y),         # drive DOWN to internal road level
                (ROAD_EXIT_LX,    EXIT_GATE_Y),         # turn LEFT through exit gate
                (ROAD_EXIT_LX,    ROAD_OFFSCREEN_Y),    # drive DOWN off screen
            ]
        else:               # right aisle
            self.waypoints = [
                (AISLE1_EXIT_LX,  slot.cy),             # pull back to right exit lane
                (AISLE1_EXIT_LX,  EXIT_GATE_Y),         # drive DOWN right exit lane
                (ROAD_EXIT_LX,    EXIT_GATE_Y),         # cross internal road west, exit gate
                (ROAD_EXIT_LX,    ROAD_OFFSCREEN_Y),    # drive DOWN off screen
            ]
        self.wp_idx = 0

    # ── Update ──────────────────────────────────────────────────────────────────
    def update(self, dt):
        if self.state == PARKED:
            self.park_timer += dt
            if self.park_timer >= self.park_duration:
                self.state = DEPARTING
            return

        if self.state not in (MOVING, EXITING):
            return

        if self.wp_idx >= len(self.waypoints):
            self.state = PARKED if self.state == MOVING else EXITED
            return

        tx, ty = self.waypoints[self.wp_idx]
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)

        if dist < 1.5:
            self.x, self.y = float(tx), float(ty)
            self.wp_idx += 1
        else:
            step  = CAR_SPEED * dt
            ratio = step / dist
            self.x += dx * ratio
            self.y += dy * ratio
            self._dx = dx / dist
            self._dy = dy / dist

    # ── Draw ────────────────────────────────────────────────────────────────────
    def draw(self, surf, font):
        if self.state == EXITED:
            return

        # Build top-down car surface; front = top of the surface
        car_surf = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
        pygame.draw.rect(car_surf, self.color, (0, 0, CAR_W, CAR_H), border_radius=6)
        # Windshield
        pygame.draw.rect(car_surf, (200, 225, 255, 200),
                         (4, 5, CAR_W - 8, 16), border_radius=3)
        # Rear window
        pygame.draw.rect(car_surf, (180, 210, 245, 150),
                         (4, CAR_H - 20, CAR_W - 8, 13), border_radius=3)
        # Wheels
        wc = (25, 25, 25)
        for wx, wy in [(0, 7), (CAR_W - 5, 7), (0, CAR_H - 20), (CAR_W - 5, CAR_H - 20)]:
            pygame.draw.rect(car_surf, wc, (wx, wy, 5, 13))
        # ID label
        lbl = font.render(str(self.id), True, BLACK)
        car_surf.blit(lbl, (CAR_W // 2 - lbl.get_width()  // 2,
                             CAR_H // 2 - lbl.get_height() // 2))

        # Rotate to match current movement direction
        angle_deg = math.degrees(math.atan2(-self._dy, self._dx))
        rotated   = pygame.transform.rotate(car_surf, angle_deg - 90)
        rect      = rotated.get_rect(center=(int(self.x), int(self.y)))
        surf.blit(rotated, rect)
