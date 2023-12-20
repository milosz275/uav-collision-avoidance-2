from math import sqrt
from PyQt6.QtGui import QVector2D
from PyQt6.QtCore import QPoint

class Maths:
    """Math calculations"""
    @staticmethod
    def calculate_relative_distance(first : QPoint, second : QPoint) -> float:
        """Returns distance between two points"""
        distance : float = sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)
        return distance

    @staticmethod
    def calculate_relative_vector(first : QPoint, second : QPoint) -> QVector2D:
        """Returns distance between two points"""
        vector : QVector2D = (first[0] - second[0], first[1] - second[1])
        return vector
