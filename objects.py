from OpenGL.GL import *
from math import *

class robot:
    def __init__(self):
        # def _init_():
        length = 2.0
        width = 2.0
        height = 1.0
        center = [0.0, 0.0, -0.5]

        # botton front right
        self.position_b_f_r = [center[0] + length/2, center[0] + width/2 , center[2] - height/2]

        # botton front left
        self.position_b_f_l = [center[0] + length/2, center[0] - width/2 , center[2] - height/2]

        # top front left
        self.position_t_f_l = [center[0] + length/2, center[0] - width/2 , center[2] + height/2]

        # top front right
        self.position_t_f_r = [center[0] + length/2, center[0] + width/2 , center[2] + height/2]

        # botton back right
        self.position_b_b_r = [center[0] - length/2, center[0] + width/2 , center[2] - height/2]

        # botton back left
        self.position_b_b_l = [center[0] - length/2, center[0] - width/2 , center[2] - height/2]

        # top back left
        self.position_t_b_l = [center[0] - length/2, center[0] - width/2 , center[2] + height/2]

        # top back right
        self.position_t_b_r = [center[0] - length/2, center[0] + width/2 , center[2] + height/2]

        
    def draw(self):
        # top face
        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 0.0);    # Yellow

        glVertex3f(self.position_b_f_r[0], self.position_b_f_r[1], self.position_b_f_r[2]);
        glVertex3f(self.position_b_b_r[0], self.position_b_b_r[1], self.position_b_b_r[2]);
        glVertex3f(self.position_t_b_r[0], self.position_t_b_r[1], self.position_t_b_r[2]);
        glVertex3f(self.position_t_f_r[0], self.position_t_f_r[1], self.position_t_f_r[2]);

        # Bottom face

        glVertex3f(self.position_t_f_l[0], self.position_t_f_l[1], self.position_t_f_l[2]);
        glVertex3f(self.position_t_b_l[0], self.position_t_b_l[1], self.position_t_b_l[2]);
        glVertex3f(self.position_b_b_l[0], self.position_b_b_l[1], self.position_b_b_l[2]);
        glVertex3f(self.position_b_f_l[0], self.position_b_f_l[1], self.position_b_f_l[2]);

        # Front face

        glVertex3f(self.position_t_f_r[0], self.position_t_f_r[1], self.position_t_f_r[2]);
        glVertex3f(self.position_t_b_r[0], self.position_t_b_r[1], self.position_t_b_r[2]);
        glVertex3f(self.position_t_b_l[0], self.position_t_b_l[1], self.position_t_b_l[2]);
        glVertex3f(self.position_t_f_l[0], self.position_t_f_l[1], self.position_t_f_l[2]);

        # Back face

        glVertex3f(self.position_b_f_l[0], self.position_b_f_l[1], self.position_b_f_l[2]);
        glVertex3f(self.position_b_b_l[0], self.position_b_b_l[1], self.position_b_b_l[2]);
        glVertex3f(self.position_b_b_r[0], self.position_b_b_r[1], self.position_b_b_r[2]);
        glVertex3f(self.position_b_f_r[0], self.position_b_f_r[1], self.position_b_f_r[2]);

        # Left face

        glVertex3f(self.position_t_b_r[0], self.position_t_b_r[1], self.position_t_b_r[2]);
        glVertex3f(self.position_b_b_r[0], self.position_b_b_r[1], self.position_b_b_r[2]);
        glVertex3f(self.position_b_b_l[0], self.position_b_b_l[1], self.position_b_b_l[2]);
        glVertex3f(self.position_t_b_l[0], self.position_t_b_l[1], self.position_t_b_l[2]);

        # Right face

        glVertex3f(self.position_b_f_r[0], self.position_b_f_r[1], self.position_b_f_r[2]);
        glVertex3f(self.position_t_f_r[0], self.position_t_f_r[1], self.position_t_f_r[2]);
        glVertex3f(self.position_t_f_l[0], self.position_t_f_l[1], self.position_t_f_l[2]);
        glVertex3f(self.position_b_f_l[0], self.position_b_f_l[1], self.position_b_f_l[2]);

        glEnd()


class bowl:
    def __init__(self):
        self.lats = 100
        self.longs = 100
        self.center = [0.0, 0.0, 1.0]
        self.redius = 1.0

    def draw(self):
        for i in range(0, 50 + 1):
                lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
                z0 = sin(lat0)
                zr0 = cos(lat0)

                lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
                z1 = sin(lat1)
                zr1 = cos(lat1)

                # Use Quad strips to draw the sphere
                glBegin(GL_QUAD_STRIP)

                for j in range(0, self.longs + 1):
                    lng = 2 * pi * float(float(j - 1) / float(self.longs))
                    x = cos(lng)
                    y = sin(lng)
                    glColor3f(0.0, 1.0, 0.0);
                    glNormal3f(x * zr0 * self.redius + self.center[0], y * zr0 * self.redius + self.center[1], z0 * self.redius + self.center[2])
                    glVertex3f(x * zr0 * self.redius + self.center[0], y * zr0 * self.redius + self.center[1], z0 * self.redius + self.center[2])
                    glNormal3f(x * zr1 * self.redius + self.center[0], y * zr1 * self.redius + self.center[1], z1 * self.redius + self.center[2])
                    glVertex3f(x * zr1 * self.redius + self.center[0], y * zr1 * self.redius + self.center[1], z1 * self.redius + self.center[2])

                glEnd()


class ball:
    def __init__(self):
        self.lats = 100
        self.longs = 100
        self.center = [0.0, 0.0, 0.2]
        self.redius = 0.2

    def draw(self):
        for i in range(0, self.lats + 1):
                lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
                z0 = sin(lat0)
                zr0 = cos(lat0)

                lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
                z1 = sin(lat1)
                zr1 = cos(lat1)

                # Use Quad strips to draw the sphere
                glBegin(GL_QUAD_STRIP)

                for j in range(0, self.longs + 1):
                    lng = 2 * pi * float(float(j - 1) / float(self.longs))
                    x = cos(lng)
                    y = sin(lng)

                    glColor3f(1.0, 0.0, 0.0);
                    glNormal3f(x * zr0 * self.redius + self.center[0], y * zr0 * self.redius + self.center[1], z0 * self.redius + self.center[2])
                    glVertex3f(x * zr0 * self.redius + self.center[0], y * zr0 * self.redius + self.center[1], z0 * self.redius + self.center[2])
                    glNormal3f(x * zr1 * self.redius + self.center[0], y * zr1 * self.redius + self.center[1], z1 * self.redius + self.center[2])
                    glVertex3f(x * zr1 * self.redius + self.center[0], y * zr1 * self.redius + self.center[1], z1 * self.redius + self.center[2])

                glEnd()

class ground:
    def __init__(self):
        self.length = 8
        self.width = 8

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.3, 0.7);    # Yellow
        glVertex3f(self.length/2, self.width/2, -1.0);
        glVertex3f(self.length/2, -self.width/2, -1.0);
        glVertex3f(-self.length/2, -self.width/2, -1.0);
        glVertex3f(-self.length/2, self.width/2, -1.0);
        glEnd()