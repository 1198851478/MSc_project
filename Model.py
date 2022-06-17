import sys

from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtOpenGL

from objects import *

width = 800
height = 600
aspect = width/height

class SimpleViewer(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        
        # Direction of light
        self.direction = [1.0, 2.0, 1.0, 1.0]

        # Intensity of light
        self.intensity = [0.7, 0.7, 0.7, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [0.3, 0.3, 0.3, 1.0]

        # The surface type(Flat or Smooth)
        self.surface = GL_SMOOTH

        # objects
        self.robot = robot()
        self.bowl = bowl()

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
        width = width
        height = height
        aspect = width/height
        glViewport( 0, 0, width, height )

        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective( 45.0, aspect, 0.1, 10.0 )

        gluLookAt( 6.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0 )

        # glPointSize(5.0)
        # glLineWidth(5.0)

    def paintGL(self):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        
        # Set shade model
        glShadeModel(self.surface)

        # draw objects
        self.robot.draw()
        self.bowl.draw()
    

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class
        
        self.resize(500, 600)
        self.setWindowTitle('Hello OpenGL App')


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

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

if __name__ == '__main__':

    # create the QApplication
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
