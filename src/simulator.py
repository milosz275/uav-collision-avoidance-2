from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem
from src.aircraft import Aircraft
from src.settings import Settings
from src.aircraft_item import AircraftItem

class Simulator(QMainWindow):
    """A"""
    def __init__(self):
        super().__init__()

        self.resolution = Settings.resolution
        self.refresh_rate = Settings.refresh_rate

        self.setWindowTitle("Flight Simulator")
        self.setGeometry(100, 100, *self.resolution)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.planes = [
            Aircraft(position=[100, 200], speed=2, course=45),
            Aircraft(position=[700, 200], speed=2, course=135)
        ]

        self.is_finished : bool = False

        self.gui_timer = QTimer(self)
        self.simulation_timer = QTimer(self)
        self.gui_timer.timeout.connect(self.render_scene)
        self.simulation_timer.timeout.connect(self.update_simulation)
        self.gui_timer.start(1000 // self.refresh_rate)
        self.simulation_timer.start(50)

        self.show()
        # self.showFullScreen()
        

    def update_simulation(self):
        """A"""
        for plane in self.planes:
            plane.update_position()

        self.is_finished = self.check_collision()
        if self.is_finished:
            return
        self.is_finished = self.check_offscreen()
        if self.is_finished:
            return
        self.avoid_collisions()

    def avoid_collisions(self):
        return

    def stop_simulation(self):
        self.gui_timer.stop()
        self.simulation_timer.stop()

    def check_collision(self):
        """A"""
        for i in range(len(self.planes) - 1):
            for j in range(i + 1, len(self.planes)):
                distance = ((self.planes[i].position[0] - self.planes[j].position[0]) ** 2 +
                            (self.planes[i].position[1] - self.planes[j].position[1]) ** 2) ** 0.5
                if distance < 10:
                    self.stop_simulation()
                    print("Collision occurred! Simulation stopped.")
                    return True
        return False

    def check_offscreen(self):
        """A"""
        for plane in self.planes:
            if not (0 <= plane.position[0] <= self.resolution[0] and 0 <= plane.position[1] <= self.resolution[1]):
                self.stop_simulation()
                print("Plane got off the main window! Simulation stopped.")
                return True
        return False

    def render_scene(self):
        """Render the scene with planes as circles, bounding box, and ruler marks."""
        self.scene.clear()

        bounding_box = QGraphicsRectItem(10, 10, self.resolution[0], self.resolution[1])
        self.scene.addItem(bounding_box)

        for x in range(100, self.resolution[0], 100):
            ruler_mark = QGraphicsLineItem(x, 0, x, 10)
            self.scene.addItem(ruler_mark)
            text_item = QGraphicsSimpleTextItem(str(x))
            text_item.setPos(x - 5, 15)
            self.scene.addItem(text_item)

        for y in range(100, self.resolution[1], 100):
            ruler_mark = QGraphicsLineItem(0, y, 10, y)
            self.scene.addItem(ruler_mark)
            text_item = QGraphicsSimpleTextItem(str(y))
            text_item.setPos(15, y - 5)
            self.scene.addItem(text_item)

        for plane in self.planes:
            circle_size = 10
            circle = AircraftItem(plane.position, circle_size, plane)
            self.scene.addItem(circle)

        self.view.setScene(self.scene)
        self.view.setSceneRect(0, 0, *self.resolution)