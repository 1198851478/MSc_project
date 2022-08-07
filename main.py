import sys
import time as timing

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtOpenGL
from qtwidgets import Toggle

from model import *
from objects import _UPDATE_INTERVAL_

width = 800
height = 600
aspect = width/height

_OBSERVATION_DISTANCE_ = 6.0

# parameters in new window
_ENERGY_LOSS_MINI_ = 0.0
_ENERGY_LOSS_RANGE_ = 0.5
_ENERGY_LOSS_INIT_ = 0.2

_AMBIENT_LIGHT_MINI_ = 0.0
_AMBIENT_LIGHT_RANGE_ = 1.0
_AMBIENT_LIGHT_INIT_ = 0.5

_BOWL_radius_MINI_ = 1.0
_BOWL_radius_RANGE_ = 0.6
_BOWL_radius_INIT_ = 1.0

# parameters in main window
_BALL_radius_MINI_ = 0.1
_BALL_radius_RANGE_ = 0.5
_BALL_radius_INIT_ = 0.2

_ROBOT_SPEED_Y_MINI_ = -10.0
_ROBOT_SPEED_Y_RANGE_ = -_ROBOT_SPEED_Y_MINI_ * 2
_ROBOT_SPEED_X_MINI_ = -10.0
_ROBOT_SPEED_X_RANGE_ = -_ROBOT_SPEED_X_MINI_ * 2

class SimpleViewer(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.offset_z = 1.0

        self.angle1 = 0.5 * pi
        self.angle2 = 0.25 * pi
        
        # Direction of light
        self.direction = [1.0, 2.0, 1.0, 1.0]

        # Intensity of light
        self.intensity = [0.7, 0.7, 0.7, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [_AMBIENT_LIGHT_INIT_, _AMBIENT_LIGHT_INIT_, _AMBIENT_LIGHT_INIT_, 1.0]

        # The surface type(Flat or Smooth)
        self.surface = GL_SMOOTH

        # physics model
        self.model = model()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        # background color
        glClearColor( 0.7, 0.7, 1.0, 0.0 )

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Set light model
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)

        # Enable light number 0
        glEnable(GL_LIGHT0)

        # Set position and intensity of light
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)

        # Setup the material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    def resizeGL(self, width, height):
        self.original_width = width
        self.original_height = height
        aspect = width/height
        glViewport( 0, 0, width, height )

        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()

        gluPerspective( 45.0, aspect, 0.1, 15.0 )

        self.observation_x = _OBSERVATION_DISTANCE_ * cos(self.angle1) * cos(self.angle2)
        self.observation_y = _OBSERVATION_DISTANCE_ * sin(self.angle1) * cos(self.angle2)
        self.observation_z = _OBSERVATION_DISTANCE_ * sin(self.angle2)

        gluLookAt( self.observation_x, self.observation_y, self.observation_z + self.offset_z, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0 )

        # glPointSize(5.0)
        # glLineWidth(5.0)

    def paintGL(self):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        
        # Set shade model
        glShadeModel(self.surface)

        # Physics model
        self.model.Physics_analysis()

        # update the position of the light
        self.update_light_position()

        # draw objects
        self.model.draw()

    def setRotX(self, val):
        self.angle1 = 2 * pi * val/100
        self.resizeGL(self.original_width, self.original_height)

    def setRotY(self, val):
        self.angle2 = 0.5 * pi * val/100
        self.resizeGL(self.original_width, self.original_height)

    # change light type
    def update_light(self, Ambient_light, light_switch, spot_switch):
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [Ambient_light,Ambient_light, Ambient_light])
        if light_switch:
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)
        if spot_switch:
            self.direction[3] = 0.0
        else:
            self.direction[3] = 1.0
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)

    # change light position
    def update_light_position(self):
        self.direction[1] -= self.model.ground.speed_x * _UPDATE_INTERVAL_/1000
        self.direction[0] -= self.model.ground.speed_y * _UPDATE_INTERVAL_/1000
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)

# a new window for monitor
class Monitor_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monitor')
        self.resize(500, 250)

        self.initGUI()

        self.render_time = -1
        self.render_time_count = 0

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)

        informations = QtWidgets.QGridLayout()

        informations.addWidget(QtWidgets.QLabel("Ball Speed:"), 0, 0)
        self.ball_speed_label = QtWidgets.QLabel("NA")
        informations.addWidget(self.ball_speed_label, 0, 1)

        informations.addWidget(QtWidgets.QLabel("Ball Center:"), 1, 0)
        self.ball_center_label = QtWidgets.QLabel("NA")
        informations.addWidget(self.ball_center_label, 1, 1)

        informations.addWidget(QtWidgets.QLabel("Observation Point:"), 2, 0)
        self.observation_point_label = QtWidgets.QLabel("NA")
        informations.addWidget(self.observation_point_label, 2, 1)

        informations.addWidget(QtWidgets.QLabel("Render Time(ms):"), 3, 0)
        self.render_time_label = QtWidgets.QLabel("NA")
        informations.addWidget(self.render_time_label, 3, 1)

        gui_layout.addLayout(informations)

    def update_information(self, model):
        self.ball_speed_label.setText("x: "+ "%.1f" % model.ball_speed[0] + \
            " y: "+ "%.1f" % model.ball_speed[1]+ " z: "+ "%.1f" % model.ball_speed[2])
        self.ball_center_label.setText("x: "+ "%.1f" % model.ball.draw_center[0] + \
            " y: "+ "%.1f" % model.ball.draw_center[1]+ " z: "+ "%.1f" % model.ball.draw_center[2])

        Observation_point = Cartesian2Spherical(model.ball.Observation_point)
        Observation_point[1] = Observation_point[1]*180/pi
        Observation_point[2] = Observation_point[2]*180/pi
        self.observation_point_label.setText("r: "+ "%.1f" % Observation_point[0] + \
            " theta: "+ "%.1f" % Observation_point[1]+ " phi: "+ "%.1f" % Observation_point[2])

        self.render_time_label.setText("%.2f" % self.render_time)

# a new window for property
class Property_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Property')
        self.resize(500, 300)

        self.initGUI()

        self.reload_parameters_flag = False

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)

        self.check_position_correction = QtWidgets.QCheckBox("Position Correction")
        gui_layout.addWidget(self.check_position_correction)

        parameters = QtWidgets.QGridLayout()
        # set the rate of energy loss
        parameters.addWidget(QtWidgets.QLabel("Energy Loss:"), 0, 0)
        self.Energy_Loss = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Energy_Loss.setValue(int((_ENERGY_LOSS_INIT_-_ENERGY_LOSS_MINI_)/_ENERGY_LOSS_RANGE_*100))
        self.Energy_Loss.valueChanged.connect(self.update_label)
        parameters.addWidget(self.Energy_Loss, 0, 1)
        self.energy_label = QtWidgets.QLabel("NA")    # the label shows the value of the slider
        parameters.addWidget(self.energy_label, 0, 2)

        # set the radius of the bowl
        parameters.addWidget(QtWidgets.QLabel("Bowl radius:"), 1, 0)
        self.Bowl_radius = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Bowl_radius.setValue(int((_BOWL_radius_INIT_-_BOWL_radius_MINI_)/_BOWL_radius_RANGE_*100))
        self.Bowl_radius.valueChanged.connect(self.update_label)
        parameters.addWidget(self.Bowl_radius, 1, 1)
        self.bowl_label = QtWidgets.QLabel("NA")    # the label shows the value of the slider
        parameters.addWidget(self.bowl_label, 1, 2)

        # set Ambient Light
        parameters.addWidget(QtWidgets.QLabel("Ambient Light:"), 2, 0)
        self.Ambient_Light = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Ambient_Light.setValue(int((_AMBIENT_LIGHT_INIT_-_AMBIENT_LIGHT_MINI_)/_AMBIENT_LIGHT_RANGE_*100))
        self.Ambient_Light.valueChanged.connect(self.update_label)
        parameters.addWidget(self.Ambient_Light, 2, 1)
        self.Ambient_label = QtWidgets.QLabel("NA")    # the label shows the value of the slider
        parameters.addWidget(self.Ambient_label, 2, 2)
        gui_layout.addLayout(parameters)

        # set light
        light_layout = QtWidgets.QGridLayout()
        self.light_switch = Toggle()
        self.light_switch.setChecked(True)
        self.light_switch.stateChanged.connect(self.update_label)
        light_layout.addWidget(self.light_switch, 0, 0)
        Switch_label = QtWidgets.QLabel("Light Switch")
        light_layout.addWidget(Switch_label, 0, 1)
        self.Spot_switch = Toggle()
        self.Spot_switch.setChecked(True)
        self.Spot_switch.stateChanged.connect(self.update_label)
        light_layout.addWidget(self.Spot_switch, 0, 2)
        self.Parallel_label = QtWidgets.QLabel("Parallel Light")
        self.Parallel_label.setStyleSheet("color: blue;")
        light_layout.addWidget(self.Parallel_label, 0, 3)
        gui_layout.addLayout(light_layout)

        # update the value of the sliders
        self.update_label()

    # update labels based on sliders value
    def update_label(self):
        self.energy_label.setText("%.1f" % (self.Energy_Loss.value()*_ENERGY_LOSS_RANGE_/100 + _ENERGY_LOSS_MINI_))
        self.bowl_label.setText("%.1f" % (self.Bowl_radius.value()*_BOWL_radius_RANGE_/100 + _BOWL_radius_MINI_))
        self.Ambient_label.setText("%.1f" % (self.Ambient_Light.value()*_AMBIENT_LIGHT_RANGE_/100 + _AMBIENT_LIGHT_MINI_))
        if self.Spot_switch.isChecked():
            self.Parallel_label.setText("Spot Light")
            self.Parallel_label.setStyleSheet("color: green;")
        else:
            self.Parallel_label.setText("Parallel Light")
            self.Parallel_label.setStyleSheet("color: blue;")
        # self.Damping_label.setText("%.1f" % (self.Slider_Damping.value()*_DAMPING_MESS_RANGE_/100 + _DAMPING_MESS_MINI_))
        self.reload_parameters_flag = True

    # reset all settings in property window
    def reset_para(self):
        # reset para
        self.check_position_correction.setChecked(False)
        self.Energy_Loss.setValue(int((_ENERGY_LOSS_INIT_-_ENERGY_LOSS_MINI_)/_ENERGY_LOSS_RANGE_*100))
        self.Bowl_radius.setValue(int((_BOWL_radius_INIT_-_BOWL_radius_MINI_)/_BOWL_radius_RANGE_*100))
        self.Ambient_Light.setValue(int((_AMBIENT_LIGHT_INIT_-_AMBIENT_LIGHT_MINI_)/_AMBIENT_LIGHT_RANGE_*100))
        self.light_switch.setChecked(True)
        self.Spot_switch.setChecked(True)
        # run all settings
        self.update_label()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class
        
        self.resize(500, 600)
        self.setWindowTitle('Simulation')

        # show the property
        self.property_win = Property_Window()

         # show the monitor
        self.monitor_win = Monitor_Window()

        # set up the display

        self.glWidget = SimpleViewer(self)
        
        self.initGUI()
        
        timer = QtCore.QTimer(self)
        timer.setInterval(_UPDATE_INTERVAL_)   # period, in milliseconds
        timer.timeout.connect(self.Update_GUI)
        timer.start()
    
    def Update_GUI(self):
        time_start = timing.time()
        if self.property_win.reload_parameters_flag:
            self.update_parameters()
            self.glWidget.update_light(float(self.property_win.Ambient_label.text()), self.property_win.light_switch._handle_position == 1.0,\
                self.property_win.Spot_switch._handle_position == 0.0)
        self.glWidget.updateGL()
        self.monitor_win.update_information(self.glWidget.model)

        # record time
        time_end = timing.time()

        if self.monitor_win.render_time_count > 20:
            self.monitor_win.render_time_count = 0
            self.monitor_win.render_time = (time_end-time_start) * 1000

        self.monitor_win.render_time_count += 1

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)

        new_win_layout = QtWidgets.QGridLayout()
        # the button for property
        show_property = QtWidgets.QPushButton("Property")
        show_property.clicked.connect(self.property_win.show)
        new_win_layout.addWidget(show_property, 0, 0)

        # the button for monitor
        show_monitor = QtWidgets.QPushButton("Monitor")
        show_monitor.clicked.connect(self.monitor_win.show)
        new_win_layout.addWidget(show_monitor, 0, 1)

        gui_layout.addLayout(new_win_layout)

        gui_layout.addWidget(self.glWidget)

        # sliders x, y
        self.SliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.SliderX.setValue(25)
        self.SliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))
        gui_layout.addWidget(self.SliderX)

        self.SliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.SliderY.setValue(50)
        self.SliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))
        gui_layout.addWidget(self.SliderY)

        # parameters form
        # the radius of the ball
        parameters = QtWidgets.QGridLayout()
        parameters.addWidget(QtWidgets.QLabel("Ball radius:"), 0, 0)
        self.Slider_radius = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_radius.setValue(int((_BALL_radius_INIT_-_BALL_radius_MINI_)/_BALL_radius_RANGE_*100))
        self.Slider_radius.valueChanged.connect(self.update_parameters)
        parameters.addWidget(self.Slider_radius, 0, 1)
        self.radius_text = QtWidgets.QLabel("NA")
        parameters.addWidget(self.radius_text, 0, 2)

        # the speed in x axis of the robot
        parameters.addWidget(QtWidgets.QLabel("Robot Speed(x):"), 1, 0)
        self.Slider_xspeed = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_xspeed.setValue(50)
        self.Slider_xspeed.valueChanged.connect(self.update_parameters)
        parameters.addWidget(self.Slider_xspeed, 1, 1)
        self.Speedx_text = QtWidgets.QLabel("NA")
        parameters.addWidget(self.Speedx_text, 1, 2)

        # the speed in y axis of the robot
        parameters.addWidget(QtWidgets.QLabel("Robot Speed(y):"), 2, 0)
        self.Slider_yspeed = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_yspeed.setValue(50)
        self.Slider_yspeed.valueChanged.connect(self.update_parameters)
        parameters.addWidget(self.Slider_yspeed, 2, 1)
        self.Speedy_text = QtWidgets.QLabel("NA")
        parameters.addWidget(self.Speedy_text, 2, 2)

        gui_layout.addLayout(parameters)

        # reset bottom:
        self.reset_botton = QtWidgets.QPushButton("Reset")
        self.reset_botton.clicked.connect(self.reset)
        gui_layout.addWidget(self.reset_botton)

        # run parameters
        self.update_parameters()

    # update all settings based on current configuration
    def update_parameters(self):
        parameters = {}
        # main window
        self.radius_text.setText("%.1f" % (self.Slider_radius.value()*_BALL_radius_RANGE_/100 + _BALL_radius_MINI_))
        self.Speedx_text.setText("%.1f" % (self.Slider_xspeed.value()*_ROBOT_SPEED_X_RANGE_/100 + _ROBOT_SPEED_X_MINI_))
        self.Speedy_text.setText("%.1f" % (self.Slider_yspeed.value()*_ROBOT_SPEED_Y_RANGE_/100 + _ROBOT_SPEED_Y_MINI_))
        parameters["ball radius"] = float(self.radius_text.text())
        parameters["bowl radius"] = float(self.property_win.bowl_label.text())
        parameters["speed x"] = float(self.Speedx_text.text())
        parameters["speed y"] = float(self.Speedy_text.text())

        # property window
        parameters["energy loss"] = float(self.property_win.energy_label.text())
        # parameters["damping"] = float(self.property_win.Damping_label.text())
        parameters["position correction"] = self.property_win.check_position_correction.isChecked()
        
        self.glWidget.model.update_parameters(parameters)
        self.property_win.reload_parameters_flag = False

    # reset all settings
    def reset(self):
        # reset property window settings
        self.property_win.reset_para()
        self.glWidget.model.reset()
        self.glWidget.direction = [1.0, 2.0, 1.0, 1.0]

        # set main window parameters
        self.Slider_radius.setValue(int((_BALL_radius_INIT_-_BALL_radius_MINI_)/_BALL_radius_RANGE_*100))
        self.Slider_xspeed.setValue(50)
        self.Slider_yspeed.setValue(50)
        self.SliderX.setValue(25)
        self.SliderY.setValue(50)

        # run all initial settings
        self.update_parameters()

        self.property_win.reload_parameters_flag = True

if __name__ == '__main__':

    # create the QApplication
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
