from PySide6.QtGui import QVector2D
from PySide6.QtCore import QPointF

class Maths:
    """Math calculations"""
    @staticmethod
    def sqrt(number : float, exponent : int = 2) -> float:
        """Returns square root of given number"""
        power : float = 1.0 / exponent
        return number ** power

    @staticmethod
    def calculate_relative_distance(first : QPointF, second : QPointF) -> float:
        """Returns distance between two points"""
        return float(Maths.sqrt((first.x() - second.x()) ** 2 + (first.y() - second.y()) ** 2))

    @staticmethod
    def calculate_relative_vector(first : QPointF, second : QPointF) -> QVector2D:
        """Returns distance between two points"""
        return QVector2D(first.x() - second.x(), first.y() - second.y())
