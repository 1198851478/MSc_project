from OpenGL.GL import *
from math import *
import os
from OpenGL.GLU import *
from numpy import arctan
from regex import P

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *

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
        self.rotation = [80, 60, 45]

    def arctan(self, value1, value2):
        if value1 > 0.0 and value2 == 0.0:
            return pi*0.5
        if value1 < 0.0 and value2 == 0.0:
            return pi*1.5
        if value1 == 0.0 and value2 == 0.0:
            return 0
        return atan(value1/value2)

    def calculate_rotate_angle(self, new_rotation):
        self.rotation = new_rotation
        self.rotation[2] += 3
        self.rotation[1] += 0
        self.rotation[0] += 0
        return self.rotation


    def draw(self):
        glMatrixMode(GL_MODELVIEW);
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D,self.read_texture())

        glPushMatrix(); #remember current matrix

        rotation = self.calculate_rotate_angle(self.rotation)
        glRotate(rotation[0], 1, 0, 0)
        glRotate(rotation[1], 0, 1, 0)
        glRotate(rotation[2], 0, 0, 1)

        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        gluSphere(qobj, 1, 50, 50)
        gluDeleteQuadric(qobj)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix(); #restore matrix


        # # glBindTexture(GL_TEXTURE_2D,self.read_texture())
        # for i in range(0, self.lats + 1):
        #         lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
        #         z0 = sin(lat0)
        #         zr0 = cos(lat0)

        #         lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
        #         z1 = sin(lat1)
        #         zr1 = cos(lat1)

        #         # Use Quad strips to draw the sphere
        #         glBegin(GL_QUAD_STRIP)

        #         for j in range(0, self.longs + 1):
        #             lng = 2 * pi * float(float(j - 1) / float(self.longs))
        #             x = cos(lng)
        #             y = sin(lng)

        #             glColor3f(1.0, 0.0, 0.0);
        #             glNormal3f(x * zr0 * self.redius + self.center[0], y * zr0 * self.redius + self.center[1], z0 * self.redius + self.center[2])
        #             glVertex3f(x * zr0 * self.redius + self.center[0], y * zr0 * self.redius + self.center[1], z0 * self.redius + self.center[2])
        #             glNormal3f(x * zr1 * self.redius + self.center[0], y * zr1 * self.redius + self.center[1], z1 * self.redius + self.center[2])
        #             glVertex3f(x * zr1 * self.redius + self.center[0], y * zr1 * self.redius + self.center[1], z1 * self.redius + self.center[2])

        #         glEnd()

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

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.read_texture())
        glBegin(GL_QUADS)

        glColor3f( 1.0,1.0,1.0)    # use the color of the texture

        glTexCoord2f(1.0, 0.0)
        glVertex3f(self.length/2, self.width/2, -1.0);
        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.length/2, -self.width/2, -1.0);
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-self.length/2, -self.width/2, -1.0);
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-self.length/2, self.width/2, -1.0);
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def read_texture(self):
        if self.offset_x >= self.show_length * 2 or self.offset_x <= 0:
            self.offset_x = self.show_length
        else:
            self.offset_x += 1
        if self.offset_y >= self.show_length * 2 or self.offset_y <= 0:
            self.offset_y = self.show_length
        else:
            self.offset_y += 1
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