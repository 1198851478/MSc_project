import sys

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

_DAMPING_MESS_MINI_ = 4000
_DAMPING_MESS_RANGE_ = 6000

# parameters in main window
_BALL_REDIUS_MINI_ = 0.1
_BALL_REDIUS_RANGE_ = 0.5
_BALL_REDIUS_INIT_ = 0.2

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

        # draw objects
        self.model.draw()

    def setRotX(self, val):
        self.angle1 = 2 * pi * val/100
        self.resizeGL(self.original_width, self.original_height)

    def setRotY(self, val):
        self.angle2 = 0.5 * pi * val/100
        self.resizeGL(self.original_width, self.original_height)

    def update_light(self, Ambient_light, light_switch, spot_switch):
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [Ambient_light,Ambient_light, Ambient_light])
        if light_switch:
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)
        if spot_switch:
            self.direction[2] = 0.0
        else:
            self.direction[2] = 1.0
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)


# a new window for monitor
class Monitor_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Monitor')
        self.resize(400, 230)

        self.initGUI()

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

        gui_layout.addLayout(informations)

    def update_information(self, model):
        self.ball_speed_label.setText("x: "+ "%.1f" % model.ball_speed[0] + \
            " y: "+ "%.1f" % model.ball_speed[1]+ " z: "+ "%.1f" % model.ball_speed[2])
        self.ball_center_label.setText("x: "+ "%.1f" % model.ball.draw_center[0] + \
            " y: "+ "%.1f" % model.ball.draw_center[1]+ " z: "+ "%.1f" % model.ball.draw_center[2])

# a new window for property
class Property_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Property')
        self.resize(500, 230)

        self.initGUI()

        self.reload_parameters_flag = False
        self.position_correction_flag = False

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)

        self.check_position_correction = QtWidgets.QCheckBox("Position Correction")
        self.check_position_correction.stateChanged.connect(self.set_position_correction)
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

        # set Ambient Light
        parameters.addWidget(QtWidgets.QLabel("Ambient Light:"), 1, 0)
        self.Ambient_Light = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Ambient_Light.setValue(int((_AMBIENT_LIGHT_INIT_-_AMBIENT_LIGHT_MINI_)/_AMBIENT_LIGHT_RANGE_*100))
        self.Ambient_Light.valueChanged.connect(self.update_label)
        parameters.addWidget(self.Ambient_Light, 1, 1)
        self.Ambient_label = QtWidgets.QLabel("NA")    # the label shows the value of the slider
        parameters.addWidget(self.Ambient_label, 1, 2)
        gui_layout.addLayout(parameters)

        # set light
        light_layout = QtWidgets.QGridLayout()
        self.light_switch = Toggle()
        self.light_switch.stateChanged.connect(self.update_label)
        light_layout.addWidget(self.light_switch, 0, 0)
        Switch_label = QtWidgets.QLabel("Light Switch")
        light_layout.addWidget(Switch_label, 0, 1)
        self.Spot_switch = Toggle()
        self.Spot_switch.stateChanged.connect(self.update_label)
        light_layout.addWidget(self.Spot_switch, 0, 2)
        self.Parallel_label = QtWidgets.QLabel("Spot Light")
        self.Parallel_label.setStyleSheet("color: blue;")
        light_layout.addWidget(self.Parallel_label, 0, 3)
        gui_layout.addLayout(light_layout)

        # # set Damping Coefficient
        # parameters.addWidget(QtWidgets.QLabel("Damping Coefficient:"), 3, 0)
        # self.Slider_Damping = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # self.Slider_Damping.valueChanged.connect(self.update_label)
        # parameters.addWidget(self.Slider_Damping, 3, 1)
        # self.Damping_label = QtWidgets.QLabel("NA")    # the label shows the value of the slider
        # parameters.addWidget(self.Damping_label, 3, 2)

        # gui_layout.addLayout(parameters)

        # update the value of the sliders
        self.update_label()

    # update labels based on sliders value
    def update_label(self):
        self.energy_label.setText("%.1f" % (self.Energy_Loss.value()*_ENERGY_LOSS_RANGE_/100 + _ENERGY_LOSS_MINI_))
        self.Ambient_label.setText("%.1f" % (self.Ambient_Light.value()*_AMBIENT_LIGHT_RANGE_/100 + _AMBIENT_LIGHT_MINI_))
        # self.Damping_label.setText("%.1f" % (self.Slider_Damping.value()*_DAMPING_MESS_RANGE_/100 + _DAMPING_MESS_MINI_))
        self.reload_parameters_flag = True

    def set_position_correction(self):
        self.position_correction_flag = self.check_position_correction.isChecked()

    # reset all settings in property window
    def reset_para(self):
        self.check_position_correction.setChecked(False)
        self.Energy_Loss.setValue(int((_ENERGY_LOSS_INIT_-_ENERGY_LOSS_MINI_)/_ENERGY_LOSS_RANGE_*100))
        self.Ambient_Light.setValue(int((_AMBIENT_LIGHT_INIT_-_AMBIENT_LIGHT_MINI_)/_AMBIENT_LIGHT_RANGE_*100))

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
        if self.property_win.reload_parameters_flag:
            self.update_parameters()
            self.glWidget.update_light(float(self.property_win.Ambient_label.text()), self.property_win.light_switch._handle_position == 0,\
                self.property_win.Spot_switch._handle_position == 0)
        self.glWidget.updateGL()
        self.monitor_win.update_information(self.glWidget.model)

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
        # the redius of the ball
        parameters = QtWidgets.QGridLayout()
        parameters.addWidget(QtWidgets.QLabel("Ball Redius:"), 0, 0)
        self.Slider_redius = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_redius.setValue(int((_BALL_REDIUS_INIT_-_BALL_REDIUS_MINI_)/_BALL_REDIUS_RANGE_*100))
        self.Slider_redius.valueChanged.connect(self.update_parameters)
        parameters.addWidget(self.Slider_redius, 0, 1)
        self.redius_text = QtWidgets.QLabel("NA")
        parameters.addWidget(self.redius_text, 0, 2)

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
        self.redius_text.setText("%.1f" % (self.Slider_redius.value()*_BALL_REDIUS_RANGE_/100 + _BALL_REDIUS_MINI_))
        self.Speedx_text.setText("%.1f" % (self.Slider_xspeed.value()*_ROBOT_SPEED_X_RANGE_/100 + _ROBOT_SPEED_X_MINI_))
        self.Speedy_text.setText("%.1f" % (self.Slider_yspeed.value()*_ROBOT_SPEED_Y_RANGE_/100 + _ROBOT_SPEED_Y_MINI_))
        parameters["redius"] = float(self.redius_text.text())
        parameters["speed x"] = float(self.Speedx_text.text())
        parameters["speed y"] = float(self.Speedy_text.text())

        # property window
        parameters["energy loss"] = float(self.property_win.energy_label.text())
        # parameters["damping"] = float(self.property_win.Damping_label.text())
        parameters["position correction"] = self.property_win.position_correction_flag
        
        self.glWidget.model.update_parameters(parameters)
        self.property_win.reload_parameters_flag = False

    # reset all settings
    def reset(self):
        # reset property window settings
        self.property_win.reset_para()
        # reset light
        self.glWidget.update_light(float(self.property_win.Ambient_label.text()))
        # reset physics model parameters
        self.glWidget.model.reset()

        # set main window parameters
        self.Slider_redius.setValue(int((_BALL_REDIUS_INIT_-_BALL_REDIUS_MINI_)/_BALL_REDIUS_RANGE_*100))
        self.Slider_xspeed.setValue(50)
        self.Slider_yspeed.setValue(50)
        self.SliderX.setValue(25)
        self.SliderY.setValue(50)

        # run all initial settings
        self.update_parameters()

if __name__ == '__main__':

    # create the QApplication
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
