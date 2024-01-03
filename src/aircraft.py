from PySide6.QtCore import QPointF
from PySide6.QtGui import QVector2D
from typing import List
from math import cos, sin, radians, dist
from copy import copy

class Aircraft:
    """Aircraft"""
    aircraft_id: int
    yaw_angle : float
    pitch_angle : float
    roll_angle : float
    set_speed : float
    speed : float
    course : float
    position : QPointF
    distance_covered : float
    size : float = 40.0
    max_course_change : float = 1.5
    speedstep : float = 0.05
    safezone_size : float = 1000.0
    safezone_occupied: bool
    path: List[QPointF]
    path_append_iterator : float

    def __init__(self, aircraft_id, position, yaw_angle, speed) -> None:
        """Initializes the aircraft"""
        self.aircraft_id = aircraft_id
        self.yaw_angle = yaw_angle
        self.pitch_angle = 0.0
        self.roll_angle = 0.0
        self.speed = speed
        self.set_speed = speed
        self.course = self.yaw_angle
        self.position = position
        self.distance_covered = 0.0
        self.safezone_occupied = False # todo: change to int
        self.path = []
        self.path_append_iterator = 0.0

    def update_course(self) -> None:
        """Applies gradual change to yaw angle respecting set course"""
        # todo: replace with algorithm
        abs_course = self.course
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
    
    def update_speed(self) -> None:
        """A"""
        if self.set_speed == self.speed:
            return
        elif self.set_speed > self.speed:
            if self.set_speed - self.speed <= self.speedstep:
                self.speed = self.set_speed
            else:
                self.speed += self.speedstep
        else: # deceleration
            if self.speed - self.set_speed <= self.speedstep:
                self.speed = self.set_speed
            else:
                self.speed -= self.speedstep
        return

    def update_position(self) -> None:
        """Updates position of the aircraft, applies smooth course adjustment"""
        self.update_speed()
        self.update_course()

        # todo: change to matrix
        previous_position : QPointF = copy(self.position)
        speed_vector = self.get_speed_vector()
        self.position.setX(self.position.x() + speed_vector.x())
        self.position.setY(self.position.y() + speed_vector.y())
        
        # distance covered
        distance = dist(previous_position.toTuple(), self.position.toTuple())
        self.distance_covered += distance
        
        # path
        self.path_append_iterator += distance
        if self.path_append_iterator >= 3.5:
            self.path.append(copy(self.position))
            self.path_append_iterator = 0
        return

    def get_speed_vector(self) -> QVector2D:
        """Returns speed vector of the aircraft"""
        return QVector2D(self.speed * cos(radians(self.yaw_angle)), self.speed * sin(radians(self.yaw_angle)))
