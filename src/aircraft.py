from PyQt6.QtGui import QVector2D
from math import cos, sin, radians
#from src.aircraft_item import AircraftItem

class Aircraft:
    """Aircraft"""
    id: int
    yaw_angle : float = 0.0
    pitch_angle : float = 0.0
    roll_angle : float = 0.0
    speed : float = 100.0
    course : float = 0.0
    max_course_change : float = 2.5
    position : QVector2D = (0, 0)
    size : float = 10.0

    def __init__(self, id, position, yaw_angle, speed, course, size):
        """Initializes the aircraft"""
        self.id = id
        self.position = position
        self.speed = speed
        self.yaw_angle = yaw_angle
        self.course = course
        self.size = size

    def set_course(self, course):
        """Applies gradual change to yaw angle respecting set course"""
        # todo: replace with algorithm
        abs_course = course
        while abs_course >= 360:
            abs_course -= 360
        while abs_course < 0:
            abs_course += 360
        abs_course %= 360
        multiplier = 1
        if (abs_course - self.yaw_angle) < 0:
            abs_course += 360
            multiplier += 1
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

    def update_position(self):
        """Updates position of the aircraft, applies smooth course adjustment"""
        self.set_course(self.course)

        # todo: change to matrix
        self.position[0] += self.speed * cos(radians(self.yaw_angle))
        self.position[1] += self.speed * sin(radians(self.yaw_angle))
