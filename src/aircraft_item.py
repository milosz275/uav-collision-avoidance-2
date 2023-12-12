from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsSimpleTextItem
from PyQt6.QtGui import QVector2D

# class AircraftItem(QGraphicsEllipseItem):
#     def __init__(self, position : QVector2D, size, aircraft: Aircraft, parent = None):
#         super().__init__(position[0] - size / 2, position[1] - size / 2, size, size, parent)
#         self.aircraft = aircraft

#         self.info_text_item = QGraphicsSimpleTextItem(self)
#         self.info_text_item.setPos(self.x() + self.rect().width() + 5, self.y())
#         self.update_aircraft_info()

#     def hoverEnterEvent(self, event):
#         self.info_text_item.setVisible(True)

#     def hoverLeaveEvent(self, event):
#         self.info_text_item.setVisible(False)

#     def update_aircraft_info(self):
#         info_text = f"Aircraft ID: {self.aircraft.id}\nPosition: {self.aircraft.position}\nSpeed: {self.aircraft.speed}\nCourse: {self.aircraft.yaw_angle}"
#         self.info_text_item.setText(info_text)

class AircraftItem(QGraphicsEllipseItem):
    def __init__(self, position : QVector2D, size : float, aircraft, parent = None):
        super().__init__(position[0] - size / 2, position[1] - size / 2, size, size, parent)
        self.aircraft = aircraft
        # self.setX(position[0] - size / 3)
        # self.setY(position[1] - size / 3)

        # Create a label for the aircraft information
        self.info_text_item = QGraphicsSimpleTextItem(self)
        self.update_aircraft_info()  
        self.info_text_item.setVisible(True) 

    def hoverEnterEvent(self, event):
        self.info_text_item.setVisible(True)

    def hoverLeaveEvent(self, event):
        self.info_text_item.setVisible(False)

    def set_position(self, position : QVector2D, size : float):
        #self.setPos(position[0] - size / 2, position[1] - size / 2)
        return

    def update_aircraft_info(self):
        info_text = f"Aircraft ID: {self.aircraft.id}\nPosition: ({self.aircraft.position[0]:.2f}, {self.aircraft.position[1]:.2f})\nSpeed: {self.aircraft.speed}\nCourse: {self.aircraft.yaw_angle}"
        self.info_text_item.setText(info_text)
        self.info_text_item.setPos(50, 75 * (self.aircraft.id + 1))
