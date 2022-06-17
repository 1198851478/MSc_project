import sys

from OpenGL.GL import *
from OpenGL.GLU import *

from simple_viewer import *
from math import *

width = 800
height = 600
aspect = width/height


from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtOpenGL

class SimpleViewer(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor( 0.7, 0.7, 1.0, 0.0 )

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
        # glBegin(GL_QUADS)
        # glVertex3f(-0.5, -0.5, 0.0)
        # glVertex3f(0.5, -0.5, 0.0)
        # glVertex3f(0.5, 0.5, 0.0)
        # glVertex3f(-0.5, 0.5, 0.0)
        # glEnd()
        lats = 100
        longs = 100
        for i in range(0, 50 + 1):
                lat0 = pi * (-0.5 + float(float(i - 1) / float(lats)))
                z0 = sin(lat0)
                zr0 = cos(lat0)

                lat1 = pi * (-0.5 + float(float(i) / float(lats)))
                z1 = sin(lat1)
                zr1 = cos(lat1)

                # Use Quad strips to draw the sphere
                glBegin(GL_QUAD_STRIP)

                for j in range(0, longs + 1):
                    lng = 2 * pi * float(float(j - 1) / float(longs))
                    x = cos(lng)
                    y = sin(lng)
                    glColor3f(0.0, 1.0, 0.0);
                    glNormal3f(x * zr0, y * zr0, z0+1)
                    glVertex3f(x * zr0, y * zr0, z0+1)
                    glNormal3f(x * zr1, y * zr1, z1+1)
                    glVertex3f(x * zr1, y * zr1, z1+1)

                glEnd()

        # top face
        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 0.0);    # Yellow

        glVertex3f(1.0, 1.0, -1.0);
        glVertex3f(-1.0, 1.0, -1.0);
        glVertex3f(-1.0, 1.0, 0.0);
        glVertex3f(1.0, 1.0, 0.0);

        # Bottom face

        glVertex3f(1.0, -1.0, 0.0);
        glVertex3f(-1.0, -1.0, 0.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glVertex3f(1.0, -1.0, -1.0);

        # Front face  (z = 1.0f)

        glVertex3f(1.0, 1.0, 0.0);
        glVertex3f(-1.0, 1.0, 0.0);
        glVertex3f(-1.0, -1.0, 0.0);
        glVertex3f(1.0, -1.0, 0.0);

        # Back face (z = -1.0f)

        glVertex3f(1.0, -1.0, -1.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glVertex3f(-1.0, 1.0, -1.0);
        glVertex3f(1.0, 1.0, -1.0);

        # Left face (x = -1.0f)

        glVertex3f(-1.0, 1.0, 0.0);
        glVertex3f(-1.0, 1.0, -1.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glVertex3f(-1.0, -1.0, 0.0);

        # Right face (x = 1.0f)

        glVertex3f(1.0, 1.0, -1.0);
        glVertex3f(1.0, 1.0, 0.0);
        glVertex3f(1.0, -1.0, 0.0);
        glVertex3f(1.0, -1.0, -1.0);

        glEnd()
    

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
