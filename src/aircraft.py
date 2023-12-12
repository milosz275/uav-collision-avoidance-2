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
    max_course_change : float = 5.0
    position : QVector2D = (0, 0)
    size : float = 10.0
    #aircraft_item: AircraftItem

    def __init__(self, id, position, speed, course, size):
        self.id = id
        self.position = position
        self.speed = speed
        self.yaw_angle = course
        self.size = size
        #self.aircraft_item = AircraftItem(position, size, self)

    def set_course(self, course):
        while course >= 360:
            course -= 360
        while course < 0:
            course += 360
        # now, course is only [0, 359]
        if course > self.yaw_angle:
            if (course - self.yaw_angle) <= 180:
                if course < (self.yaw_angle + self.max_course_change):
                    self.yaw_angle += (course - self.yaw_angle)
                else:
                    self.yaw_angle += self.max_course_change
            else:
                if course > (self.yaw_angle - self.max_course_change):
                    self.yaw_angle -= (self.yaw_angle - course)
                else:
                    self.yaw_angle -= self.max_course_change
        elif self.yaw_angle < course:
            return
        else:
            return

        self.yaw_angle = course

    def update_position(self):
        """A"""
        # that needs a fix
        self.position[0] += self.speed * cos(radians(self.yaw_angle))
        self.position[1] += self.speed * sin(radians(self.yaw_angle))
        #self.aircraft_item.set_position(self.position, self.size)
