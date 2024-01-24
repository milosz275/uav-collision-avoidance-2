from PySide6.QtCore import QPointF
from PySide6.QtGui import QVector2D
from typing import List
from math import cos, sin, radians, dist, asin, degrees, tan
from copy import copy

class Aircraft:
    """Aircraft"""
    aircraft_id: int
    yaw_angle : float # heading angle
    pitch_angle : float # dive angle
    roll_angle : float # bank angle
    set_speed : float
    speed : float
    vertical_speed : float
    course : float
    position : QPointF
    rendered_position : QPointF
    previous_position : QPointF
    distance_covered : float
    size : float
    turn_radius : float
    max_course_change : float
    speedstep : float = 0.05
    safezone_size : float = 1000.0
    safezone_occupied : bool
    is_turning : bool
    is_turning_right : bool
    path: List[QPointF]
    g_acceleration : float = 9.81

    def __init__(self, aircraft_id, position, yaw_angle, speed, size) -> None:
        """Initializes the aircraft"""
        self.aircraft_id = aircraft_id
        self.yaw_angle = yaw_angle
        self.pitch_angle = 0.0
        self.roll_angle = 45.0
        self.speed = speed
        self.vertical_speed = 0.0
        self.set_speed = speed
        self.course = self.yaw_angle
        self.position = position
        self.rendered_position = QPointF(self.position.x(), self.position.y())
        self.size = size
        self.previous_position = copy(position)
        self.distance_covered = 0.0
        self.max_course_change = 0.0
        self.safezone_occupied = False # todo: change to int
        self.is_turning = False
        self.is_turning_right = False
        self.path = []

    # def calculate_turn_radius(self) -> None:
    #     """A"""
    #     self.turn_radius = float((self.g_acceleration * tan(self.roll_angle)) / self.speed)
        

    def calculate_max_course_change(self) -> None:
        """A"""
        self.max_course_change = float((self.g_acceleration * tan(self.roll_angle)) / self.speed)

        # chord_length : float = dist(self.previous_position.toTuple(), self.position.toTuple())
        # if chord_length <= 0 or self.turn_radius <= 0:
        #     self.max_course_change = 0
        #     return
        # height : float = (chord_length ** 2) / (2 * self.turn_radius)
        # ratio = height / chord_length
        # if ratio < -1:
        #     ratio = -1
        # elif ratio > 1:
        #     ratio = 1
        # self.max_course_change = degrees(asin(ratio))

    def update_course(self) -> None:
        """Applies gradual change to yaw angle respecting set course"""
        # todo: replace with algorithm
        abs_course = self.course
        while abs_course >= 360:
            abs_course -= 360
        while abs_course < 0:
            abs_course += 360
        abs_course %= 360
        
        if (abs_course == self.yaw_angle):
            self.is_turning = False
            return
        else:
            self.is_turning = True

        if (abs_course - self.yaw_angle) < 0:
            abs_course += 360
        new_yaw_angle = self.yaw_angle

        # self.calculate_turn_radius()
        self.calculate_max_course_change()

        if (abs_course - self.yaw_angle) <= 180:
            self.is_turning_right = True
            if abs_course < (self.yaw_angle + self.max_course_change):
                new_yaw_angle = abs_course
            else:
                new_yaw_angle += self.max_course_change
        else:
            self.is_turning_right = False
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
        self.previous_position = copy(self.position)
        speed_vector = self.get_speed_vector()
        self.position.setX(self.position.x() + speed_vector.x())
        self.position.setY(self.position.y() + speed_vector.y())
        self.rendered_position.setX(self.position.x() / 10)
        self.rendered_position.setY(self.position.y() / 10)
        
        # distance covered
        distance = dist(self.previous_position.toTuple(), self.position.toTuple())
        self.distance_covered += distance
        
        # path
        self.path.append(copy(self.position))
        return

    def get_speed_vector(self) -> QVector2D:
        """Returns speed vector of the aircraft"""
        return QVector2D(self.speed * cos(radians(self.yaw_angle)), self.speed * sin(radians(self.yaw_angle)))
