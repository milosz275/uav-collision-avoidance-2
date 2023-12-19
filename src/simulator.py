from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QKeySequence
from src.maths import Maths
from src.aircraft import Aircraft
from src.settings import Settings
from math import radians, sin, cos, atan2, degrees
from copy import copy

class Simulator(QMainWindow):
    """Main simulation App"""
    def __init__(self) -> None:
        super().__init__()

        self.resolution = Settings.resolution
        self.bounding_box_resolution = [Settings.resolution[0], Settings.resolution[1]]
        self.refresh_rate = Settings.refresh_rate

        self.setWindowTitle("UAV Flight Simulator")
        self.setGeometry(0, 0, self.resolution[0] + 10, self.resolution[1] + 10)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.debug : bool = True
        self.display_info : int = 2 # 0 - not displayed; 1 - displayed top left; 2 - displayed below aircraft
        self.display_course_trajectory : bool = True
        self.display_yaw_trajectory : bool = True
        self.display_safezone : bool = True
        self.display_paths : bool = True
        self.cause_crash_second : bool = False

        self.frame_time : float = 1000 // self.refresh_rate # in miliseconds
        self.simulation_threshold = self.frame_time # in miliseconds
        self.gui_timer = QTimer(self)
        self.simulation_timer = QTimer(self)
        self.gui_timer.timeout.connect(self.render_scene)
        self.simulation_timer.timeout.connect(self.update_simulation)
        self.gui_timer.start(self.frame_time) # frame time
        
        self.frame_counter : int = 0
        self.is_finished : bool = False
        self.aircrafts : list(Aircraft) = []
        self.reset_simulation()
        self.start_simulation()
        self.show()
        return

    def update_simulation(self) -> None:
        """Updates simulation looping through aircrafts, checks collisions with another objects and with simulation boundaries"""
        for aircraft in self.aircrafts:
            aircraft.update_position()

        self.check_safezones()

        self.is_finished = self.check_collision()
        if self.is_finished:
            return
        
        self.is_finished = self.check_offscreen()
        if self.is_finished:
            return
        
        if self.cause_crash_second:
            self.cause_collision()
        return

    def avoid_aircraft_collision(self, aircraft_id : int) -> None:
        """Detects and schedules avoid maneuver for each aircraft"""
        aircraft = self.aircrafts[aircraft_id]
        if not aircraft.aircraft_id == aircraft_id:
            print("Aircraft ids are not the same. Closing...")
            self.close()
        # todo: implement algorithm
        return

    def reset_simulation(self) -> None:
        """Resets drawn paths and resets aircrafts"""
        for aircraft in self.aircrafts:
            aircraft.path.clear()
        self.aircrafts.clear() 
        self.aircrafts = [
            Aircraft(0, position=[100, 200], yaw_angle=340, speed=2, course=45),
            Aircraft(1, position=[700, 200], yaw_angle=135, speed=2, course=145)
        ]
        return

    def start_simulation(self) -> None:
        """Starts all timers"""
        self.is_finished = False
        self.simulation_timer.start(self.simulation_threshold)
        return
    
    def stop_simulation(self) -> None:
        """Stops all timers"""
        self.simulation_timer.stop()
        self.is_finished = True
        return

    def check_safezones(self) -> None:
        """Checks if safezones are entered by another aircrafts"""
        for i in range(len(self.aircrafts) - 1):
            for j in range(i + 1, len(self.aircrafts)):
                distance = Maths.calculate_points_distance(self.aircrafts[i].position, self.aircrafts[j].position)
                if distance <= self.aircrafts[i].safezone_size / 2:
                    if not self.aircrafts[i].safezone_occupied:
                        self.aircrafts[i].safezone_occupied = True
                        self.avoid_aircraft_collision(self.aircrafts[i].aircraft_id)
                        print("Some object entered safezone of Aircraft ", self.aircrafts[i].aircraft_id)
                else:
                    if self.aircrafts[i].safezone_occupied:
                        self.aircrafts[i].safezone_occupied = False
                        print("Some object left safezone of Aircraft ", self.aircrafts[i].aircraft_id)
                if distance <= self.aircrafts[j].safezone_size / 2:
                    if not self.aircrafts[j].safezone_occupied:
                        self.aircrafts[j].safezone_occupied = True
                        self.avoid_aircraft_collision(self.aircrafts[j].aircraft_id)
                        print("Some object entered safezone of Aircraft ", self.aircrafts[j].aircraft_id)
                else:
                    if self.aircrafts[j].safezone_occupied:
                        self.aircrafts[j].safezone_occupied = False
                        print("Some object left safezone of Aircraft ", self.aircrafts[j].aircraft_id)
        return

    def check_collision(self) -> bool:
        """Checks and returns if any of the aircrafts collided with each other"""
        for i in range(len(self.aircrafts) - 1):
            for j in range(i + 1, len(self.aircrafts)):
                distance = Maths.calculate_points_distance(self.aircrafts[i].position, self.aircrafts[j].position)
                if distance <= ((self.aircrafts[i].size + self.aircrafts[j].size) / 2):
                    self.stop_simulation()
                    print("Aircrafts collided. Simulation stopped")
                    return True
        return False

    def check_offscreen(self) -> bool:
        """Checks and returns if any of the aircrafts collided with simulation boundaries"""
        for aircraft in self.aircrafts:
            if not (0 + aircraft.size / 2 <= aircraft.position[0] <= self.resolution[0] - aircraft.size / 2 and 0 + aircraft.size / 2 <= aircraft.position[1] <= self.resolution[1] - aircraft.size / 2):
                self.stop_simulation()
                print("Aircraft left simulation boundaries. Simulation stopped")
                return True
        return False
    
    def cause_collision(self) -> None:
        """Test method allowing to crash second aircraft into the first"""
        if len(self.aircrafts) >= 2:
            aircraft = self.aircrafts[1]
            target_aircraft = self.aircrafts[0]
            delta_x = target_aircraft.position[0] - aircraft.position[0]
            delta_y = target_aircraft.position[1] - aircraft.position[1]
            angle_rad = atan2(delta_y, delta_x)
            angle_deg = degrees(angle_rad)
            angle_deg %= 360
            aircraft.course = angle_deg
            return

    def render_scene(self) -> None:
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

        # path update planning
        append_to_paths : bool = False
        if not self.is_finished:
            self.frame_counter += 1
            if self.frame_counter == 3:
                self.frame_counter = 0
                append_to_paths = True  

        for aircraft in self.aircrafts:
            # aircraft representation
            aircraft_circle = QGraphicsEllipseItem(
                aircraft.position[0] - aircraft.size / 2,
                aircraft.position[1] - aircraft.size / 2,
                aircraft.size,
                aircraft.size)
            if aircraft.safezone_occupied:
                aircraft_circle.setPen(QPen(Qt.GlobalColor.gray))
            self.scene.addItem(aircraft_circle)

            # path update
            if append_to_paths:
                aircraft.path.append(copy(aircraft.position))
                if len(aircraft.path) == 100:
                    del aircraft.path[0]

            if self.debug:
                # info label
                if self.display_info:
                    info_text = f"id: {aircraft.aircraft_id}\nx: {aircraft.position[0]:.2f}\ny: {aircraft.position[1]:.2f}\nspeed: {aircraft.speed}\ndistance: {aircraft.distance_covered:.1f}\ncourse: {aircraft.course:.1f}\nyaw: {aircraft.yaw_angle:.1f}"
                    text_item = QGraphicsSimpleTextItem(info_text)
                    if self.display_info == 1:
                        text_item.setPos(-60 + 100 * (aircraft.aircraft_id + 1), 30)
                    elif self.display_info == 2:
                        text_item.setPos(aircraft.position[0] -100, aircraft.position[1] -100)
                    self.scene.addItem(text_item)

                # travelled path
                if self.display_paths:
                    if len(aircraft.path) > 1:
                        for i in range(len(aircraft.path) - 1):
                            point1 = aircraft.path[i]
                            point2 = aircraft.path[i + 1]
                            path_line = QGraphicsLineItem(point1[0], point1[1], point2[0], point2[1])
                            pen : QPen
                            if aircraft.aircraft_id == 0:
                                pen = QPen(Qt.GlobalColor.magenta)
                            elif aircraft.aircraft_id == 1:
                                pen = QPen(Qt.GlobalColor.blue)
                            else:
                                pen = QPen(Qt.GlobalColor.cyan)
                            pen.setWidth(1)
                            path_line.setPen(pen)
                            self.scene.addItem(path_line)

                # safezone around the aircraft
                if self.display_safezone:
                    aircraft_safezone_circle = QGraphicsEllipseItem(
                        aircraft.position[0] - aircraft.safezone_size / 2,
                        aircraft.position[1] - aircraft.safezone_size / 2,
                        aircraft.safezone_size,
                        aircraft.safezone_size)
                    self.scene.addItem(aircraft_safezone_circle)

                # angles of movement
                if self.display_yaw_trajectory:
                    yaw_angle_line = QGraphicsLineItem(
                        aircraft.position[0],
                        aircraft.position[1],
                        aircraft.position[0] + 1000 * cos(radians(aircraft.yaw_angle)),
                        aircraft.position[1] + 1000 * sin(radians(aircraft.yaw_angle)))
                    yaw_angle_line.setPen(QPen(Qt.GlobalColor.red))
                    self.scene.addItem(yaw_angle_line)
                if self.display_course_trajectory:
                    course_line = QGraphicsLineItem(
                        aircraft.position[0],
                        aircraft.position[1],
                        aircraft.position[0] + 1000 * cos(radians(aircraft.course)),
                        aircraft.position[1] + 1000 * sin(radians(aircraft.course)))
                    if aircraft.course % 45 == 0 and not aircraft.course % 90 == 0:
                        course_line.setPen(QPen(Qt.GlobalColor.green))
                    self.scene.addItem(course_line)

        self.view.setScene(self.scene)
        self.view.setSceneRect(0, 0, *self.resolution)
        return

    def keyPressEvent(self, event) -> None:
        """Qt method that handles keypress events for steering the aircrafts and simulation state"""
        
        if QKeySequence(event.key()).toString() == "`":
            self.debug ^= 1
        
        # ctrl + button
        if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:
                self.close()
        if event.key() == Qt.Key.Key_Escape:
            self.close()

        if not self.debug:
            return super().keyPressEvent(event)
        
        # first aircraft steering
        if len(self.aircrafts) >= 1:
            if event.key() == Qt.Key.Key_D:
                self.aircrafts[0].course = 0
            elif event.key() == Qt.Key.Key_S:
                self.aircrafts[0].course = 90
            elif event.key() == Qt.Key.Key_A:
                self.aircrafts[0].course = 180
            elif event.key() == Qt.Key.Key_W:
                self.aircrafts[0].course = 270
            elif event.key() == Qt.Key.Key_F2:
                if self.aircrafts[0].speed > 1:
                    self.aircrafts[0].speed -= 1
            elif event.key() == Qt.Key.Key_F3:
                self.aircrafts[0].speed += 1
            elif event.key() == Qt.Key.Key_Y:
                course = self.aircrafts[0].course
                course -= self.aircrafts[0].max_course_change * 2
                if course < 0:
                    course += 360
                self.aircrafts[0].course = course
            elif event.key() == Qt.Key.Key_U:
                course = self.aircrafts[0].course
                course += self.aircrafts[0].max_course_change * 2
                if course >= 360:
                    course -= 360
                self.aircrafts[0].course = course
        
        # second aircraft steering
        if len(self.aircrafts) >= 2:
            if event.key() == Qt.Key.Key_L:
                self.aircrafts[1].course = 0
            elif event.key() == Qt.Key.Key_K:
                self.aircrafts[1].course = 90
            elif event.key() == Qt.Key.Key_J:
                self.aircrafts[1].course = 180
            elif event.key() == Qt.Key.Key_I:
                self.aircrafts[1].course = 270
            elif event.key() == Qt.Key.Key_F6:
                if self.aircrafts[1].speed > 1:
                    self.aircrafts[1].speed -= 1
            elif event.key() == Qt.Key.Key_F7:
                self.aircrafts[1].speed += 1
            elif event.key() == Qt.Key.Key_O:
                course = self.aircrafts[1].course
                course -= self.aircrafts[1].max_course_change * 2
                if course < 0:
                    course += 360
                self.aircrafts[1].course = course
            elif event.key() == Qt.Key.Key_P:
                course = self.aircrafts[1].course
                course += self.aircrafts[1].max_course_change * 2
                if course >= 360:
                    course -= 360
                self.aircrafts[1].course = course
        
        # shortcuts for every case
        if event.key() == Qt.Key.Key_R:
            self.stop_simulation()
            self.reset_simulation()
            self.start_simulation()
        elif event.key() == Qt.Key.Key_Slash:
            if self.is_finished:
                self.start_simulation()
            else:
                self.stop_simulation()
        elif event.key() == Qt.Key.Key_1:
            value = self.display_info + 1
            if value > 2:
                value = 0
            self.display_info = value
        elif event.key() == Qt.Key.Key_2:
            self.display_course_trajectory ^= 1
        elif event.key() == Qt.Key.Key_3:
            self.display_yaw_trajectory ^= 1
        elif event.key() == Qt.Key.Key_4:
            self.display_safezone ^= 1
        elif event.key() == Qt.Key.Key_5:
            self.display_paths ^= 1
        elif event.key() == Qt.Key.Key_6:
            self.cause_crash_second ^= 1

        return super().keyPressEvent(event)
