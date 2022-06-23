import sys

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtOpenGL

from model import *

width = 800
height = 600
aspect = width/height

# error code
_ERROR_ILLEGAL_INPUT_ = -1

# parameters
_ROBOT_MESS_MINI_ = 1.0
_ROBOT_MESS_RANGE_ = 9.0
_SPRING_MESS_MINI_ = 0.1
_SPRING_MESS_RANGE_ = 0.9
_DAMPING_MESS_MINI_ = 0.1
_DAMPING_MESS_RANGE_ = 0.9


def IsNum(str):
    # if str is int
    if str.isdigit():
        return True
    s=str.split('.')
    if len(s)>2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
            return True


class SimpleViewer(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

        # original postion of observation
        self.observation_x = 6.0
        self.observation_y = 0.0
        self.observation_z = 1.0

        self.offset_z = 1.0

        self.angle1 = 0
        self.angle2 = 0
        
        # Direction of light
        self.direction = [1.0, 2.0, 1.0, 1.0]

        # Intensity of light
        self.intensity = [0.7, 0.7, 0.7, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [0.5, 0.5, 0.5, 1.0]

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

        self.observation_x = 6.0 * cos(self.angle1) * cos(self.angle2)
        self.observation_y = 6.0 * sin(self.angle1) * cos(self.angle2)
        self.observation_z = 6.0 * sin(self.angle2)

        gluLookAt( self.observation_x, self.observation_y, self.observation_z + self.offset_z, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0 )

        # glPointSize(5.0)
        # glLineWidth(5.0)

    def paintGL(self):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        
        # Set shade model
        glShadeModel(self.surface)

        # draw objects
        self.model.draw()

    def setRotX(self, val):
        self.angle1 = 2 * pi * val/100
        self.resizeGL(self.original_width, self.original_height)

    def setRotY(self, val):
        self.angle2 = 0.5 * pi * val/100
        self.resizeGL(self.original_width, self.original_height)

# new window for property
class NewWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Property')
        self.resize(400, 230)
        self.new_parameter_flag = False # if true, it means property has changed, reload the property.

        self.initGUI()

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)

        parameters = QtWidgets.QGridLayout()
        # set the mess of the bowl and the robot
        parameters.addWidget(QtWidgets.QLabel("Robot Mess(kg):"), 0, 0)
        self.Slider_mess = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_mess.valueChanged.connect(self.update_label)
        parameters.addWidget(self.Slider_mess, 0, 1)
        self.mess_label = QtWidgets.QLabel("NA")    # the label the show the value of the slider
        parameters.addWidget(self.mess_label, 0, 2)

        # set Spring Constant
        parameters.addWidget(QtWidgets.QLabel("Spring Constant:"), 1, 0)
        self.Slider_Spring = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_Spring.valueChanged.connect(self.update_label)
        parameters.addWidget(self.Slider_Spring, 1, 1)
        self.Spring_label = QtWidgets.QLabel("NA")    # the label the show the value of the slider
        parameters.addWidget(self.Spring_label, 1, 2)

        # set Damping Coefficient
        parameters.addWidget(QtWidgets.QLabel("Damping Coefficient:"), 2, 0)
        self.Slider_Damping = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.Slider_Damping.valueChanged.connect(self.update_label)
        parameters.addWidget(self.Slider_Damping, 2, 1)
        self.Damping_label = QtWidgets.QLabel("NA")    # the label the show the value of the slider
        parameters.addWidget(self.Damping_label, 2, 2)

        gui_layout.addLayout(parameters)

        # reset button
        Reset_button = QtWidgets.QPushButton("Reset")
        gui_layout.addWidget(Reset_button)

        # update the value of the sliders
        self.update_label()

    def update_label(self):
        self.mess_label.setText("%.1f" % float(str((self.Slider_mess.value())*_ROBOT_MESS_RANGE_/100 + _ROBOT_MESS_MINI_)))
        self.Spring_label.setText("%.1f" % float(str((self.Slider_Spring.value())*_SPRING_MESS_RANGE_/100 + _SPRING_MESS_MINI_)))
        self.Damping_label.setText("%.1f" % float(str((self.Slider_Damping.value())*_DAMPING_MESS_RANGE_/100 + _DAMPING_MESS_MINI_)))
        self.new_parameter_flag |= True
    

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class
        
        self.resize(500, 600)
        self.setWindowTitle('Simulation')

        # show the property
        self.newWin = NewWindow()

        # set up the display

        self.glWidget = SimpleViewer(self)
        
        self.initGUI()
        
        timer = QtCore.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)

        # the button for property
        Run_button = QtWidgets.QPushButton("Property")
        Run_button.clicked.connect(self.newWin.show)
        gui_layout.addWidget(Run_button)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        # sliders x, y, z
        SliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        SliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))
        gui_layout.addWidget(SliderX)

        SliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        SliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))
        gui_layout.addWidget(SliderY)

        # parameters form
        # the redus of the ball
        parameters = QtWidgets.QGridLayout()

        parameters.addWidget(QtWidgets.QLabel("Ball Redius:"), 0, 0)
        self.redius_text = QtWidgets.QLineEdit("0.1")
        self.redius_text.setClearButtonEnabled(True)
        parameters.addWidget(self.redius_text, 0, 1)

        # the mess of the ball
        parameters.addWidget(QtWidgets.QLabel("Ball Mess(kg):"), 1, 0)
        self.mess_text = QtWidgets.QLineEdit("2.0")
        self.mess_text.setClearButtonEnabled(True)
        parameters.addWidget(self.mess_text, 1, 1)

        # the speed of the robot
        parameters.addWidget(QtWidgets.QLabel("Speed(x) of Robot:"), 0, 2)
        self.Speedx_text = QtWidgets.QLineEdit("1.0")
        self.Speedx_text.setClearButtonEnabled(True)
        parameters.addWidget(self.Speedx_text, 0, 3)

        # the speed of the robot
        parameters.addWidget(QtWidgets.QLabel("Speed(x) of Robot:"), 1, 2)
        self.Speedy_text = QtWidgets.QLineEdit("2.0")
        self.Speedy_text.setClearButtonEnabled(True)
        parameters.addWidget(self.Speedy_text, 1, 3)

        gui_layout.addLayout(parameters)

        # the button for run
        Run_button = QtWidgets.QPushButton("Run")
        Run_button.clicked.connect(self.update_parameters)
        gui_layout.addWidget(Run_button)

    def update_parameters(self):
        illegal_flag = False
        if not IsNum(self.redius_text.text()) or float(self.redius_text.text()) <= 0 or float(self.redius_text.text()) > 0.5:
            self.redius_text.clear()
            illegal_flag |= True
        if not IsNum(self.mess_text.text()):
            self.mess_text.clear()
            illegal_flag |= True
        if not IsNum(self.Speedx_text.text()):
            self.Speedx_text.clear()
            illegal_flag |= True
        if not IsNum(self.Speedy_text.text()):
            self.Speedy_text.clear()
            illegal_flag |= True
        if illegal_flag:
            QtWidgets.QMessageBox.about(self,"Error","Illegal input")
            return _ERROR_ILLEGAL_INPUT_
        self.glWidget.model.update_parameters(float(self.redius_text.text()), float(self.mess_text.text()), float(self.Speedx_text.text()),\
            float(self.Speedy_text.text()))


if __name__ == '__main__':

    # create the QApplication
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
