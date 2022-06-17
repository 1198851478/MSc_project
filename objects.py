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

        # glVertex3f(1.0, 1.0, -1.0);
        # glVertex3f(-1.0, 1.0, -1.0);
        # glVertex3f(-1.0, 1.0, 0.0);
        # glVertex3f(1.0, 1.0, 0.0);

        # # Bottom face

        # glVertex3f(1.0, -1.0, 0.0);
        # glVertex3f(-1.0, -1.0, 0.0);
        # glVertex3f(-1.0, -1.0, -1.0);
        # glVertex3f(1.0, -1.0, -1.0);

        # # Front face

        # glVertex3f(1.0, 1.0, 0.0);
        # glVertex3f(-1.0, 1.0, 0.0);
        # glVertex3f(-1.0, -1.0, 0.0);
        # glVertex3f(1.0, -1.0, 0.0);

        # # Back face

        # glVertex3f(1.0, -1.0, -1.0);
        # glVertex3f(-1.0, -1.0, -1.0);
        # glVertex3f(-1.0, 1.0, -1.0);
        # glVertex3f(1.0, 1.0, -1.0);

        # # Left face

        # glVertex3f(-1.0, 1.0, 0.0);
        # glVertex3f(-1.0, 1.0, -1.0);
        # glVertex3f(-1.0, -1.0, -1.0);
        # glVertex3f(-1.0, -1.0, 0.0);

        # # Right face

        # glVertex3f(1.0, 1.0, -1.0);
        # glVertex3f(1.0, 1.0, 0.0);
        # glVertex3f(1.0, -1.0, 0.0);
        # glVertex3f(1.0, -1.0, -1.0);

        glEnd()


class bowl:
    def draw(self):
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