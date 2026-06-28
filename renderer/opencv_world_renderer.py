from dataclasses import dataclass
from typing import Protocol, Tuple

import cv2
import numpy as np

from renderer.scene_graph import SceneGraph, SceneNode
from renderer.render_queue import RenderQueue


@dataclass(frozen=True)
class RenderConfig:
    width: int = 1280
    height: int = 720
    pixels_per_meter: float = 18.0
    boat_screen_y_ratio: float = 0.78
    show_debug_current_zones: bool = True
    river_left_ratio: float = 0.22
    river_right_ratio: float = 0.78

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Renderer dimensions must be positive")
        if not 0.75 <= self.boat_screen_y_ratio <= 0.80:
            raise ValueError("Boat screen ratio must stay between 0.75 and 0.80")
        if self.pixels_per_meter <= 0:
            raise ValueError("pixels_per_meter must be positive")
        if not 0.0 < self.river_left_ratio < self.river_right_ratio < 1.0:
            raise ValueError("river bank ratios must satisfy 0 < left < right < 1")


class BoatLike(Protocol):
    x: float
    y: float


class OpenCVWorldRenderer:
    def __init__(self, config: RenderConfig = RenderConfig()):
        self.config = config

    def world_to_screen(self, world_x: float, world_y: float, boat: BoatLike) -> Tuple[int, int]:
        cx = self.config.width * 0.5
        boat_sy = self.config.height * self.config.boat_screen_y_ratio
        sx = cx + (world_x - boat.x) * self.config.pixels_per_meter
        sy = boat_sy - (world_y - boat.y) * self.config.pixels_per_meter
        return int(round(sx)), int(round(sy))

    def render(self, scene: SceneGraph, boat: BoatLike) -> np.ndarray:
        frame = np.zeros((self.config.height, self.config.width, 3), dtype=np.uint8)
        frame[:] = (126, 92, 42)

        self._draw_river_banks(frame)
        for node in scene.nodes:
            self._draw_node(frame, node, boat)

        self._draw_boat(frame)
        self._draw_hud(frame, scene)
        return frame


    def render_queue(self, queue: RenderQueue, boat: BoatLike) -> np.ndarray:
        frame = np.zeros((self.config.height, self.config.width, 3), dtype=np.uint8)
        frame[:] = (126, 92, 42)

        self._draw_river_banks(frame)
        for command in queue.commands:
            self._draw_command(frame, command, boat)
        self._draw_boat(frame)
        return frame

    def _draw_command(self, frame: np.ndarray, command, boat: BoatLike) -> None:
        if command.kind == "circle":
            x, y = self.world_to_screen(command.world_x, command.world_y, boat)
            cv2.circle(frame, (x, y), max(2, int(command.radius * self.config.pixels_per_meter)), command.color, -1)
        elif command.kind == "line":
            if len(command.points) != 2:
                return
            p1 = self.world_to_screen(command.points[0][0], command.points[0][1], boat)
            p2 = self.world_to_screen(command.points[1][0], command.points[1][1], boat)
            cv2.line(frame, p1, p2, command.color, command.thickness)
        elif command.kind == "rect":
            x, y = self.world_to_screen(command.world_x, command.world_y, boat)
            half_w = max(4, int(command.width * self.config.pixels_per_meter * 0.5))
            half_h = max(4, int(command.height * self.config.pixels_per_meter * 0.5))
            if command.alpha < 1.0:
                overlay = frame.copy()
                cv2.rectangle(overlay, (x - half_w, y - half_h), (x + half_w, y + half_h), command.color, -1)
                cv2.addWeighted(overlay, command.alpha, frame, 1.0 - command.alpha, 0, frame)
                cv2.rectangle(frame, (x - half_w, y - half_h), (x + half_w, y + half_h), command.color, 1)
            else:
                cv2.rectangle(frame, (x - half_w, y - half_h), (x + half_w, y + half_h), command.color, -1)
        elif command.kind == "polygon":
            points = np.array([self.world_to_screen(x, y, boat) for x, y in command.points], dtype=np.int32)
            if len(points) >= 3:
                cv2.fillPoly(frame, [points], command.color)
        elif command.kind == "text":
            if command.layer >= 1000:
                x = int(round(command.world_x * 18))
                y = int(round(command.world_y * 32))
            else:
                x, y = self.world_to_screen(command.world_x, command.world_y, boat)
            cv2.putText(frame, command.text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, command.font_scale, command.color, command.thickness)

    def _draw_river_banks(self, frame: np.ndarray) -> None:
        h, w = self.config.height, self.config.width
        river_left = int(w * self.config.river_left_ratio)
        river_right = int(w * self.config.river_right_ratio)
        cv2.rectangle(frame, (0, 0), (river_left, h), (44, 92, 48), -1)
        cv2.rectangle(frame, (river_right, 0), (w, h), (44, 92, 48), -1)
        cv2.line(frame, (river_left, 0), (river_left, h), (82, 130, 74), 4)
        cv2.line(frame, (river_right, 0), (river_right, h), (82, 130, 74), 4)

    def _draw_node(self, frame: np.ndarray, node: SceneNode, boat: BoatLike) -> None:
        if node.kind == "current_zone" and not self.config.show_debug_current_zones:
            return

        x, y = self.world_to_screen(node.world_x, node.world_y, boat)

        if node.kind == "rock":
            cv2.circle(frame, (x, y), max(2, int(node.radius * self.config.pixels_per_meter)), node.color, -1)
        elif node.kind == "checkpoint":
            half_w = max(4, int(node.width * self.config.pixels_per_meter * 0.5))
            cv2.line(frame, (x - half_w, y), (x + half_w, y), node.color, 3)
            if node.label:
                cv2.putText(frame, node.label, (x - half_w, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, node.color, 2)
        elif node.kind == "current_zone":
            half_w = max(4, int(node.width * self.config.pixels_per_meter * 0.5))
            half_h = max(4, int(node.height * self.config.pixels_per_meter * 0.5))
            overlay = frame.copy()
            cv2.rectangle(overlay, (x - half_w, y - half_h), (x + half_w, y + half_h), node.color, -1)
            cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)
            cv2.rectangle(frame, (x - half_w, y - half_h), (x + half_w, y + half_h), node.color, 1)

    def _draw_boat(self, frame: np.ndarray) -> None:
        w = self.config.width
        y = int(self.config.height * self.config.boat_screen_y_ratio)
        pts = np.array([
            [int(w * 0.50), y - 26],
            [int(w * 0.47), y + 32],
            [int(w * 0.53), y + 32],
        ], dtype=np.int32)
        cv2.fillPoly(frame, [pts], (28, 28, 32))
        cv2.polylines(frame, [pts], True, (225, 225, 225), 2)

    def _draw_hud(self, frame: np.ndarray, scene: SceneGraph) -> None:
        y = 34
        for line in scene.hud_lines[:6]:
            cv2.putText(frame, line, (24, y), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (245, 245, 245), 2)
            y += 32
