from objects import *
import numpy as np

_GRAVITATIONAL_ACCELERATION_ = np.array([0, 0, 9.8])
_UPDATE_INTERVAL_ = 20

# calculate the distance between two point
def vector_length(vector):
    return sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

# check whether the ball interact with the cube
def check_with_cube(center_ball, center_cube, r, b, a, c):
    return abs(center_ball[0] - center_cube[0] < a/2 + r) \
        and abs(center_ball[1] - center_cube[1] < b/2 + r) and abs(center_ball[2] - center_cube[2])<= c/2 + r

# calculate the angle of v1 and v2
def angle_of_vector(v1, v2):
    vector_prod = v1[0] * v2[0] + v1[1] * v2[1] +  v1[2] * v2[2]
    length_prod = sqrt(pow(v1[0], 2) + pow(v1[1], 2) + pow(v1[2], 2)) * sqrt(pow(v2[0], 2) + pow(v2[1], 2) + pow(v2[2], 2))
    cos = vector_prod * 1.0 / (length_prod * 1.0 + 1e-6)
    return acos(cos)

# Cartesian to spherical 
def Cartesian2Spherical(Cartesian):
    x = Cartesian[0]
    y = Cartesian[1]
    z = Cartesian[2]
    r = sqrt(x**2 + y**2 + z**2)
    Theta = acos(z/r)
    if x == 0 and y > 0:
        Phi = pi/2
    elif x == 0 and y < 0:
        Phi = pi * 3/2
    elif x == 0 and y == 0:
        Phi = inf
    elif x * y < 0:
        Phi = atan(y/x) + pi
    else:
        Phi = atan(y/x)
    return np.array([r, Theta, Phi])

def Spherical2Cartesian(Spherical):
    r = Spherical[0]
    Theta = Spherical[1]
    Phi = Spherical[2]
    x = r * sin(Theta) * cos(Phi)
    y = r * sin(Theta) * sin(Phi)
    z = r * cos(Theta)
    return np.array([x, y, z])

def normalize(vector):
    return vector/np.linalg.norm(vector)

class model:
    def __init__(self):
        # objects
        self.robot = robot()
        self.bowl = bowl()
        self.ball = ball()
        self.ground = ground()
        self.k_p = 0.5
        self.k_v = 0.5
        self.k_f = 0.5 # energy loss
        self.ball_speed = np.array([0.0, 0.0, 0.0])
        self.contact_point = Cartesian2Spherical(self.ball.center - self.bowl.center)
        self.contact_point[0] = self.bowl.redius

    # check whether collision occurs
    def collision_detection(self):
        collision_flag = 0x00
        distance_with_bowl = vector_length(self.ball.center - self.bowl.center)
        # check whether the ball sticks to the bowl in a circular motion
        if distance_with_bowl != self.bowl.redius - self.ball.redius:
            self.contact_point = -1
        # check whether the ball interact with the bowl
        if distance_with_bowl > self.bowl.redius - self.ball.redius and distance_with_bowl < self.bowl.redius + self.ball.redius \
            and self.ball.center[2] <= self.bowl.center[2]:
            collision_flag |= 0x01
        # check whether the ball interact with the cube
        if check_with_cube(self.ball.center, self.robot.center, self.ball.redius, self.robot.length, self.robot.width, self.robot.height):
            collision_flag |= 0x02
        # check whether the ball interact with the ground
        if self.ball.center[2] - self.ground.coordinate_z < self.ball.redius:
            collision_flag |= 0x04
        return collision_flag

    # calculate collision forces
    def collision_force(self, collision_flag):
        collision_forces = []
        if collision_flag & 0x01:
            distance_with_bowl = vector_length(self.ball.center - self.bowl.center)
            # the direction of collision force
            normal = -normalize(self.contact_point)

            interact_dis = distance_with_bowl + self.ball.redius - self.bowl.redius
            angle = angle_of_vector(normal, self.ball_speed)
            velocity_collision = vector_length(self.ball_speed) * cos(angle)
            # gravity
            gravity = self.ball.mess * _GRAVITATIONAL_ACCELERATION_ * [0, 0, -1] * normal
            # collision force: f_n = mg + mp_z
            acceleration_collision = self.k_p * interact_dis - self.k_v * velocity_collision

            if distance_with_bowl > self.bowl.redius:
                collision_force_with_bowl = acceleration_collision * normal * self.ball.mess + gravity
            else:
                collision_force_with_bowl = -acceleration_collision * normal * self.ball.mess + gravity

            collision_forces.append(collision_force_with_bowl)
        if collision_flag & 0x02:
            pass
        if collision_flag & 0x04:
            interact_dis = self.ball.redius - (self.ball.center[2] - self.ground.coordinate_z)
            normal = np.array([0,0,1])
            angle = angle_of_vector(normal, self.ball_speed)
            velocity_collision = vector_length(self.ball_speed) * cos(angle)
            acceleration_collision = self.k_p * interact_dis - self.k_v * velocity_collision
            # gravity
            gravity = self.ball.mess * _GRAVITATIONAL_ACCELERATION_ * [0, 0, -1]
            # collision force: f_n = mg + mp_z
            collision_force_with_ground = acceleration_collision * normal * self.ball.mess + gravity
            collision_forces.append(collision_force_with_ground)
        return collision_forces

    # forces analysis
    def forces_analysis(self, collision_forces):
        composition_force = 0
        # air resistance
        damping_force = -self.k_f * (pi * self.ball.redius**2) * vector_length(self.ball_speed) * normalize(self.ball_speed)
        composition_force += damping_force
        
        # the ball is not in the bottom of the bowl
        if self.contact_point[1] != 0:
            gravity = self.ball.mess * _GRAVITATIONAL_ACCELERATION_ * [0, 0, -1]
            # The component of gravity in the direction of velocity
            gravity_speed = gravity * normalize(self.ball_speed)
            composition_force += gravity_speed

        for collision_force in collision_forces:
            composition_force += collision_force

        return composition_force

    # motion analysis
    def motion_analysis(self, F):
        a = F/self.ball.mess
        if (self.ball_speed * (self.contact_point)).all() == 0:    # circular motion
            d_Theta, d_Phi = self.line_speed2angular_speed()
            new_contact_point = self.contact_point
            new_contact_point[1] += d_Theta * _UPDATE_INTERVAL_
            if d_Phi != inf:
                new_contact_point[2] += d_Phi * _UPDATE_INTERVAL_
            # the spherical coordination of the ball
            spherical_ball_center = np.array(self.bowl.redius - self.ball.redius, new_contact_point[1], new_contact_point[2])
            # translate spherical coordination to Cartesian coordination
            self.ball.center = Spherical2Cartesian(spherical_ball_center)   # update the position of the ball

            # update ball speed
            value_velocity = vector_length(self.ball_speed)
            value_a = vector_length(a)
            value_velocity += value_a * _UPDATE_INTERVAL_
            # the normal of the plane
            normal = np.cross(new_contact_point, self.contact_point)
            self.ball_speed = value_velocity * normalize(normal * new_contact_point)
        else:       # Linear motion
            self.ball.center += self.ball_speed*_UPDATE_INTERVAL_
            self.ball_speed += (a*_UPDATE_INTERVAL_)


    # translate line speed(x, y, z) to angle speed(Theta Phi)
    def line_speed2angular_speed(self):
        e_r = normalize(self.contact_point)
        e_Phi = np.cross(np.array([0, 0, 1]), e_r)
        e_Theta = np.cross(e_Phi, e_r)

        # The projection vector of the linear velocity in the rotation direction of phi
        Phi_line_velocity = self.ball_speed * e_Phi

        # The projection vector of the linear velocity in the rotation direction of Theta
        Theta_line_velocity = self.ball_speed * e_Theta
        
        # Theta is theta and Phi of the spherical coordination of the contact point of the ball and the bowl
        Theta = Cartesian2Spherical(self.contact_point)[1]

        # the redius of phi plane
        redius_Phi_plane = self.bowl.redius * sin(Theta)
        # the redius of Theta plane
        redius_Theta_plane = self.bowl.redius

        v_Phi = vector_length(Phi_line_velocity)
        v_Theta = vector_length(Theta_line_velocity)
        if redius_Phi_plane == 0:
            d_Phi = 0
        else:
            d_Phi = v_Phi/redius_Phi_plane
        
        if Phi_line_velocity * e_Phi < 0:
            d_Phi = -d_Phi
        
        d_Theta = v_Theta/redius_Theta_plane

        return d_Theta, d_Phi

    
    def Physics_analysis(self):
        # check the status of the ball
        collision_flag = self.collision_detection()
        # analyize collision force
        collision_forces = self.collision_force(collision_flag)
        # compose all forces
        composition_force = self.forces_analysis(collision_forces)
        # based on composition force to update the position of the ball and update the velocity of the ball
        self.motion_analysis(composition_force)

    def draw(self):
        # draw objects
        self.robot.draw()
        self.bowl.draw()
        self.ball.draw()
        self.ground.draw()

    def update_parameters(self, parameters):
        self.ball.update_parameters(parameters["redius"], parameters["ball mess"])
        self.ground.update_parameters(parameters["speed x"], parameters["speed y"])