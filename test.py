from PyQt5 import QtCore      # core Qt functionality
from PyQt5 import QtGui       # extends QtCore with GUI functionality
from PyQt5 import QtOpenGL    # provides QGLWidget, a special OpenGL QWidget
from PyQt5.QtWidgets import *

from OpenGL.GL import *        # python wrapping of OpenGL
from OpenGL.GLU import *        # OpenGL Utility Library, extends OpenGL functionality
from OpenGL.GLUT import *

from math import *
import sys                    # we'll need this later to run our Qt application

from OpenGL.arrays import vbo
import numpy as np


# Draw the sphere
def draw():
    lats = 100
    longs = 100

    glBegin(GL_QUADS)
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f(0.5, -0.5, 0.0)
    glVertex3f(0.5, 0.5, 0.0)
    glVertex3f(-0.5, 0.5, 0.0)
    glEnd()


    # for i in range(lats + 1):
    #     # sector angle lat0
    #     lat0 = pi * (-0.5 + float(float(i) / float(lats)))
    #     z0 = sin(lat0)
    #     zr0 = cos(lat0)

    #     lat1 = pi * (-0.5 + float(float(i + 1) / float(lats)))
    #     z1 = sin(lat1)
    #     zr1 = cos(lat1)

    #     # Use Quad strips to draw the sphere
    #     glBegin(GL_QUAD_STRIP)

    #     for j in range(longs + 1):
    #         # stack angle lng
    #         lng = 2 * pi * float(float(j) / float(longs))
    #         x = cos(lng)
    #         y = sin(lng)
    #         glNormal3f(x * zr0, y * zr0, z0)
    #         glVertex3f(x * zr0, y * zr0, z0)
    #         glNormal3f(x * zr1, y * zr1, z1)
    #         glVertex3f(x * zr1, y * zr1, z1)

    #     glEnd()



class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
            
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))    # initialize the screen to blue
        glEnable(GL_DEPTH_TEST)                  # enable depth testing

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
         
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        # d = 2
        gluLookAt(0, 0, 1, 0,0,0, 0, 1, 0)
        gluPerspective( 45.0, aspect, 0.1, 10.0 )
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()    # push the current matrix to the current stack

        glTranslate(0.0, 0.0, -50.0)    # third, translate cube to specified depth
        glScale(20.0, 20.0, 20.0)       # second, scale cube
        glRotate(self.rotX, 1.0, 0.0, 0.0)
        glRotate(self.rotY, 0.0, 1.0, 0.0)
        glRotate(self.rotZ, 0.0, 0.0, 1.0)
        glTranslate(-0.5, -0.5, -0.5)   # first, translate cube center to origin

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        draw()

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        glPopMatrix()    # restore the previous modelview matrix

    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val

    def on_run_clicked(self):
        self.rotX += 1
        self.rotY += 1
        self.rotZ += 1
    
    def on_reset_clicked(self):
        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0


        
class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)    # call the init for the parent class
        
        self.resize(500, 600)
        self.setWindowTitle('Hello OpenGL App')

        self.glWidget = GLWidget(self)
        self.initGUI()
        
        timer = QtCore.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.update_GUI)
        timer.start()
    
    def update_GUI(self):
        self.glWidget.updateGL()
        valuex = self.sliderX.value()
        valuey = self.sliderY.value()
        valuez = self.sliderZ.value()
        self.label_coordinate.setText("x:"+str(valuex)+"\ny:"+str(valuey)+"\nz:"+str(valuez))
    
    # run button callback function
    def on_run_clicked(self):
        self.button_run.setDisabled(True)
        self.run_timer = QtCore.QTimer(self)
        self.run_timer.setInterval(20)   # period, in milliseconds
        self.run_timer.timeout.connect(self.glWidget.on_run_clicked)
        self.run_timer.start()

    # reset button callback function
    def on_reset_clicked(self):
        self.run_timer.stop()
        self.button_run.setEnabled(True)
        self.sliderX.setValue(0)
        self.sliderY.setValue(0)
        self.sliderZ.setValue(0)
        self.glWidget.on_reset_clicked()


    def initGUI(self):
        central_widget = QWidget()
        gui_layout = QVBoxLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        # labels
        self.label_coordinate = QLabel("x:0\ny:0\nz:0")
        gui_layout.addWidget(self.label_coordinate)

        # sliders x, y, z
        self.sliderX = QSlider(QtCore.Qt.Horizontal)
        self.sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        self.sliderY = QSlider(QtCore.Qt.Horizontal)
        self.sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        self.sliderZ = QSlider(QtCore.Qt.Horizontal)
        self.sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        
        gui_layout.addWidget(self.sliderX)
        gui_layout.addWidget(self.sliderY)
        gui_layout.addWidget(self.sliderZ)

        # buttons
        self.button_run = QPushButton('Run')
        self.button_run.clicked.connect(self.on_run_clicked)

        button_reset = QPushButton('reset')
        button_reset.clicked.connect(self.on_reset_clicked)

        gui_layout.addWidget(self.button_run)
        gui_layout.addWidget(button_reset)

        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
    
