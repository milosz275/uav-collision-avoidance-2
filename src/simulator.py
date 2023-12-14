from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem
from src.aircraft import Aircraft
from src.settings import Settings
from math import radians, sin, cos

class Simulator(QMainWindow):
    """Main simulation App"""
    def __init__(self):
        super().__init__()

        self.resolution = Settings.resolution
        self.bounding_box_resolution = [Settings.resolution[0], Settings.resolution[1]]
        self.refresh_rate = Settings.refresh_rate

        self.setWindowTitle("UAV Flight Simulator")
        self.setGeometry(0, 0, self.resolution[0] + 10, self.resolution[1] + 10)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.aircrafts = []
        self.reset_simulation()

        self.iterator : int = 0

        self.gui_timer = QTimer(self)
        self.simulation_timer = QTimer(self)
        self.gui_timer.timeout.connect(self.render_scene)
        self.simulation_timer.timeout.connect(self.update_simulation)
        
        self.start_simulation()

        self.is_finished : bool = False
        self.show()

    def update_simulation(self):
        """Updates simulation looping through aircrafts, checks collisions with another objects and with simulation boundaries"""
        for aircraft in self.aircrafts:
            aircraft.update_position()

        self.is_finished = self.check_collision()
        if self.is_finished:
            return
        
        self.is_finished = self.check_offscreen()
        if self.is_finished:
            return
        
        self.avoid_collisions()

    def avoid_collisions(self):
        """Detects and schedules avoid maneuver for each aircraft"""
        # todo: implement
        return

    def reset_simulation(self):
        """R"""
        for aircraft in self.aircrafts:
            self.aircrafts.remove(aircraft)
        self.aircrafts = [
            Aircraft(0, position=[100, 200], yaw_angle=340, speed=4, course=45),
            Aircraft(1, position=[700, 200], yaw_angle=135, speed=4, course=145)
        ]

    def start_simulation(self):
        """Starts all timers"""
        self.gui_timer.start(1000 // self.refresh_rate) # frame time
        self.simulation_timer.start(30) # simulation speed
    
    def stop_simulation(self):
        """Stops all timers"""
        self.simulation_timer.stop()
        self.gui_timer.stop()

    def check_collision(self):
        """Checks and returns if any of the aircrafts collided with each other"""
        for i in range(len(self.aircrafts) - 1):
            for j in range(i + 1, len(self.aircrafts)):
                distance = ((self.aircrafts[i].position[0] - self.aircrafts[j].position[0]) ** 2 +
                            (self.aircrafts[i].position[1] - self.aircrafts[j].position[1]) ** 2) ** 0.5
                if distance < ((self.aircrafts[i].size + self.aircrafts[j].size) / 2):
                    self.stop_simulation()
                    print("Aircrafts collided. Simulation stopped")
                    return True
        return False

    def check_offscreen(self):
        """Checks and returns if any of the aircrafts collided with simulation boundaries"""
        for aircraft in self.aircrafts:
            if not (0 + aircraft.size / 2 <= aircraft.position[0] <= self.resolution[0] - aircraft.size / 2 and 0 + aircraft.size / 2 <= aircraft.position[1] <= self.resolution[1] - aircraft.size / 2):
                self.stop_simulation()
                print("Aircraft left simulation boundaries. Simulation stopped")
                return True
        return False

    def render_scene(self):
        """Render the scene with aircrafts as circles, bounding box and ruler marks"""
        self.scene.clear()

        bounding_box = QGraphicsRectItem(0, 0, self.bounding_box_resolution[0], self.bounding_box_resolution[1])
        self.scene.addItem(bounding_box)

        for x in range(100, self.resolution[0], 100):
            ruler_mark = QGraphicsLineItem(x, 0, x, 10)
            self.scene.addItem(ruler_mark)
            text_item = QGraphicsSimpleTextItem(str(x))
            text_item.setPos(x - 10, -25)
            self.scene.addItem(text_item)

        for y in range(100, self.resolution[1], 100):
            ruler_mark = QGraphicsLineItem(0, y, 10, y)
            self.scene.addItem(ruler_mark)
            text_item = QGraphicsSimpleTextItem(str(y))
            text_item.setPos(-25, y - 10)
            self.scene.addItem(text_item)

        for aircraft in self.aircrafts:
            circle = QGraphicsEllipseItem(
                aircraft.position[0] - aircraft.size / 2,
                aircraft.position[1] - aircraft.size / 2,
                aircraft.size,
                aircraft.size)
            self.scene.addItem(circle)

            yaw_angle_line = QGraphicsLineItem(
                aircraft.position[0],
                aircraft.position[1],
                aircraft.position[0] + 1000 * cos(radians(aircraft.yaw_angle)),
                aircraft.position[1] + 1000 * sin(radians(aircraft.yaw_angle)))
            self.scene.addItem(yaw_angle_line)

            course_line = QGraphicsLineItem(
                aircraft.position[0],
                aircraft.position[1],
                aircraft.position[0] + 1000 * cos(radians(aircraft.course)),
                aircraft.position[1] + 1000 * sin(radians(aircraft.course)))
            self.scene.addItem(course_line)

        self.view.setScene(self.scene)
        self.view.setSceneRect(0, 0, *self.resolution)

    def keyPressEvent(self, event):
        """Qt method that handles keypress events for steering the first aircraft and simulation state"""
        if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:
                self.close()
        if len(self.aircrafts) >= 1:
            if event.key() == Qt.Key.Key_D:
                self.aircrafts[0].course = 0
            elif event.key() == Qt.Key.Key_S:
                self.aircrafts[0].course = 90
            elif event.key() == Qt.Key.Key_A:
                self.aircrafts[0].course = 180
            elif event.key() == Qt.Key.Key_W:
                self.aircrafts[0].course = 270
        if len(self.aircrafts) >= 2:
            if event.key() == Qt.Key.Key_L:
                self.aircrafts[1].course = 0
            elif event.key() == Qt.Key.Key_K:
                self.aircrafts[1].course = 90
            elif event.key() == Qt.Key.Key_J:
                self.aircrafts[1].course = 180
            elif event.key() == Qt.Key.Key_I:
                self.aircrafts[1].course = 270
        if event.key() == Qt.Key.Key_R:
            self.stop_simulation()
            self.reset_simulation()
            self.start_simulation()

        return super().keyPressEvent(event)
