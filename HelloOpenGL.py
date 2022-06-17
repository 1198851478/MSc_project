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


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
            
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))    # initialize the screen to blue
        glEnable(GL_DEPTH_TEST)                  # enable depth testing

        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
         
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        gluPerspective(45.0, aspect, 1.0, 100.0)
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

        glVertexPointer(3, GL_FLOAT, 0, self.vertVBO)
        glColorPointer(3, GL_FLOAT, 0, self.colorVBO)

        glDrawElements(GL_QUADS, len(self.cubeIdxArray), GL_UNSIGNED_INT, self.cubeIdxArray)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        glPopMatrix()    # restore the previous modelview matrix

    def initGeometry(self):
        self.cubeVtxArray = np.array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 0.5],
                 [1.0, 0.0, 0.5],
                 [1.0, 1.0, 0.5],
                 [0.0, 1.0, 0.5]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()
        
        self.cubeClrArray = np.array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 0.5],
                 [1.0, 0.0, 0.5],
                 [1.0, 1.0, 0.5],
                 [0.0, 1.0, 0.5 ]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
                                           (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
                [0, 1, 2, 3,
                 3, 2, 6, 7,
                 1, 0, 4, 5,
                 2, 1, 5, 6,
                 0, 3, 7, 4,
                 7, 6, 5, 4 ])

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
        
        self.resize(600, 800)
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
    
    def update_rot(self):
        self.glWidget.on_run_clicked()
        self.label_coordinate.setText("x:"+str(self.sliderX.value())+"\ny:"+str(self.sliderY.value())+"\nz:"+str(self.sliderZ.value()))

    # run button callback function
    def on_run_clicked(self):
        self.button_run.setDisabled(True)
        self.run_timer = QtCore.QTimer(self)
        self.run_timer.setInterval(20)   # period, in milliseconds
        self.run_timer.timeout.connect(self.update_rot)
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
        self.label_coordinate.setFixedHeight(80)
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

        # parameters form
        parameters = QGridLayout()
        parameters.addWidget(QLabel("Ball Masss:"), 0, 0)
        parameters.addWidget(QLineEdit(), 0, 1)
        parameters.addWidget(QLabel("Traction of Robot:"), 1, 0)
        parameters.addWidget(QLineEdit(), 1, 1)

        gui_layout.addLayout(parameters)

        # buttons
        self.button_run = QPushButton('Run')
        self.button_run.clicked.connect(self.on_run_clicked)

        button_reset = QPushButton('Reset')
        button_reset.clicked.connect(self.on_reset_clicked)

        gui_layout.addWidget(self.button_run)
        gui_layout.addWidget(button_reset)

        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
    
