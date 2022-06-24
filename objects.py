from OpenGL.GL import *
from math import *
import os
from OpenGL.GLU import *

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *

import numpy as np

class robot:
    def __init__(self):
        # def _init_():
        self.length = 2.0
        self.width = 2.0
        self.height = 1.0
        self.center = np.array([0.0, 0.0, -0.5])
        self.mess = 1.0

        # botton front right
        self.position_b_f_r = [self.center[0] + self.length/2, self.center[0] + self.width/2 , self.center[2] - self.height/2]

        # botton front left
        self.position_b_f_l = [self.center[0] + self.length/2, self.center[0] - self.width/2 , self.center[2] - self.height/2]

        # top front left
        self.position_t_f_l = [self.center[0] + self.length/2, self.center[0] - self.width/2 , self.center[2] + self.height/2]

        # top front right
        self.position_t_f_r = [self.center[0] + self.length/2, self.center[0] + self.width/2 , self.center[2] + self.height/2]

        # botton back right
        self.position_b_b_r = [self.center[0] - self.length/2, self.center[0] + self.width/2 , self.center[2] - self.height/2]

        # botton back left
        self.position_b_b_l = [self.center[0] - self.length/2, self.center[0] - self.width/2 , self.center[2] - self.height/2]

        # top back left
        self.position_t_b_l = [self.center[0] - self.length/2, self.center[0] - self.width/2 , self.center[2] + self.height/2]

        # top back right
        self.position_t_b_r = [self.center[0] - self.length/2, self.center[0] + self.width/2 , self.center[2] + self.height/2]

        
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
        self.center = np.array([0.0, 0.0, 1.0])
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
        self.center = np.array([0.0, 0.0, 0.2])
        self.redius = 0.1
        self.rotation = np.array([0, 0, 0])
        self.position = np.array([0, 0, 0.1])
        self.mess = 0.1

    # change the redus and the mess of the ball
    def update_parameters(self, redius, mess):
        self.redius = redius

    def update_position(self, new_rotation, new_position):
        self.rotation = new_rotation
        self.position = new_position

    def draw(self):
        glMatrixMode(GL_MODELVIEW);
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D,self.read_texture())

        glPushMatrix(); #remember current matrix
        
        glTranslatef(self.position[0], self.position[1], self.position[2])

        glRotate(self.rotation[0], 1, 0, 0)
        glRotate(self.rotation[1], 0, 1, 0)
        glRotate(self.rotation[2], 0, 0, 1)

        glColor3f( 1.0,1.0,1.0)    # use the color of the texture
        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        gluSphere(qobj, self.redius, 50, 50)
        gluDeleteQuadric(qobj)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix(); #restore matrix

    def read_texture(self):
        textureSurface = image.load('figure/football.jpg')
        textureData = image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        textID = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, textID)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return textID

class ground:
    def __init__(self):
        self.length = 8
        self.width = 8
        self.textureSurface = image.load('figure/ground3.png')
        self.show_length = min(self.textureSurface.get_height(), self.textureSurface.get_width())/3
        self.offset_x = self.show_length
        self.offset_y = self.show_length
        self.coordinate_z = -1.0

    def update_offset(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

        if self.offset_x >= self.show_length * 2 or self.offset_x <= 0:
            self.offset_x = self.offset_x % self.show_length + self.show_length

        if self.offset_y >= self.show_length * 2 or self.offset_y <= 0:
            self.offset_y = self.offset_y % self.show_length + self.show_length

    def update_parameters(self, speedx, speedy):
        print("set speedx sppeedy", speedx, speedy)

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.read_texture())
        glBegin(GL_QUADS)

        glColor3f( 1.0,1.0,1.0)    # use the color of the texture

        glTexCoord2f(1.0, 0.0)
        glVertex3f(self.length/2, self.width/2, self.coordinate_z);
        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.length/2, -self.width/2, self.coordinate_z);
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-self.length/2, -self.width/2, self.coordinate_z);
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-self.length/2, self.width/2, self.coordinate_z);
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def read_texture(self):
        textureSurface = self.textureSurface.subsurface(self.offset_x, self.offset_y, self.show_length, self.show_length)
        textureData = image.tostring(textureSurface, "RGBA", 1)

        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.show_length, self.show_length,
                    0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return texid