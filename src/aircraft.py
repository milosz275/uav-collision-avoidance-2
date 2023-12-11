from PyQt6.QtGui import QVector2D
from math import cos, sin, radians

class Aircraft:
    yaw_angle: float = 0.0
    pitch_angle: float = 0.0
    roll_angle: float = 0.0
    speed: float = 100.0
    position: QVector2D = (0, 0)

    def __init__(self, position, speed, course):
        self.position = position
        self.speed = speed
        self.yaw_angle = course

    def update_position(self):
        """A"""
        self.position[0] += self.speed * cos(radians(self.yaw_angle))
        self.position[1] += self.speed * sin(radians(self.yaw_angle))
