from math import sqrt
from PyQt6.QtGui import QVector2D

class Maths:
    """Math calculations"""
    @staticmethod
    def calculate_points_distance(first : QVector2D, second : QVector2D) -> float:
        """Returns distance between two points"""
        return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)