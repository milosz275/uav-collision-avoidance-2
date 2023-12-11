from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsSimpleTextItem

class AircraftItem(QGraphicsEllipseItem):
    def __init__(self, position, size, aircraft, parent=None):
        super().__init__(position[0] - size / 2, position[1] - size / 2, size, size, parent)
        self.aircraft = aircraft

    def hoverEnterEvent(self, event):
        self.show_aircraft_info()

    def hoverLeaveEvent(self, event):
        self.hide_aircraft_info()

    def show_aircraft_info(self):
        info_text = f"Aircraft ID: {self.aircraft.id}\nPosition: {self.aircraft.position}\nSpeed: {self.aircraft.speed}\nCourse: {self.aircraft.course}"
        text_item = QGraphicsSimpleTextItem(info_text)
        text_item.setPos(self.x() + self.rect().width() + 5, self.y())
        self.scene().addItem(text_item)
        self.info_text_item = text_item

    def hide_aircraft_info(self):
        if hasattr(self, 'info_text_item'):
            self.scene().removeItem(self.info_text_item)
            del self.info_text_item