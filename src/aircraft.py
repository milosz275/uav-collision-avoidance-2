from PyQt6.QtGui import QVector2D
from typing import List
from math import cos, sin, radians
from copy import copy
from src.maths import Maths

class Aircraft:
    """Aircraft"""
    aircraft_id: int
    yaw_angle : float
    pitch_angle : float
    roll_angle : float
    speed : float
    course : float
    position : QVector2D
    distance_covered : float
    size : float = 50.0
    max_course_change : float = 2.5
    safezone_size : float = 350.0
    safezone_occupied: bool
    path: List[QVector2D]

    def __init__(self, aircraft_id, position, yaw_angle, speed, course) -> None:
        """Initializes the aircraft"""
        self.aircraft_id = aircraft_id
        self.yaw_angle = yaw_angle
        self.pitch_angle = 0.0
        self.roll_angle = 0.0
        self.speed = speed
        self.course = course
        self.position = position
        self.distance_covered = 0.0
        self.safezone_occupied = False # todo: change to int
        self.path = []

    def update_course(self, course) -> None:
        """Applies gradual change to yaw angle respecting set course"""
        # todo: replace with algorithm
        abs_course = course
        while abs_course >= 360:
            abs_course -= 360
        while abs_course < 0:
            abs_course += 360
        abs_course %= 360
        
        if (abs_course - self.yaw_angle) < 0:
            abs_course += 360
        new_yaw_angle = self.yaw_angle
        if (abs_course - self.yaw_angle) <= 180:
            if abs_course < (self.yaw_angle + self.max_course_change):
                new_yaw_angle = abs_course
            else:
                new_yaw_angle += self.max_course_change
        else:
            if abs_course < (self.yaw_angle - self.max_course_change):
                new_yaw_angle = abs_course
            else:
                new_yaw_angle -= self.max_course_change
        new_yaw_angle %= 360
        self.yaw_angle = new_yaw_angle
        return

    def update_position(self) -> None:
        """Updates position of the aircraft, applies smooth course adjustment"""
        self.update_course(self.course)

        # todo: change to matrix
        previous_position : QVector2D = copy(self.position)
        self.position[0] += self.speed * cos(radians(self.yaw_angle))
        self.position[1] += self.speed * sin(radians(self.yaw_angle))
        self.distance_covered += Maths.calculate_points_distance(previous_position, self.position)
       
        # path update
        self.path.append(copy(self.position))
        if len(self.path) == 150:
            del self.path[0]

        return
