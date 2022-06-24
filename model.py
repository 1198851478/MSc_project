from dis import dis
from objects import *
import numpy as np

_GRAVITATIONAL_ACCELERATION_ = np.array([0, 0, 9.8])
_UPDATE_INTERVAL_ = 20

# calculate the distance between two point
def vector_length(vector):
    return sqrt(vector[0]^2 + vector[1]^2 + vector[2]^2)

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

    # check whether collision occurs
    def collision_detection(self):
        collision_flag = 0x00
        distance_with_bowl = vector_length(self.ball.center - self.bowl.center)
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
            if distance_with_bowl > self.bowl.redius:
                normal = np.linalg.norm(self.ball.center - self.bowl.center)
            else:
                normal = np.linalg.norm(self.bowl.center - self.ball.center)
            interact_dis = distance_with_bowl + self.ball.redius - self.bowl.redius
            angle = angle_of_vector(normal, self.ball_speed)
            velocity_collision = vector_length(self.ball_speed) * cos(angle)
            acceleration_collision = self.k_p * interact_dis - self.k_v * velocity_collision
            collision_force_with_bowl = acceleration_collision * normal * self.ball.mess
            collision_forces.append(collision_force_with_bowl)
        if collision_flag & 0x02:
            pass
        if collision_flag & 0x04:
            interact_dis = self.ball.redius - (self.ball.center[2] - self.ground.coordinate_z)
            normal = np.array([0,0,1])
            angle = angle_of_vector(normal, self.ball_speed)
            velocity_collision = vector_length(self.ball_speed) * cos(angle)
            acceleration_collision = self.k_p * interact_dis - self.k_v * velocity_collision
            collision_force_with_ground = acceleration_collision * normal * self.ball.mess
            collision_forces.append(collision_force_with_ground)
        return collision_forces

    # forces analysis
    def forces_analysis(self, collision_forces, collision_flag):
        composition_force = 0
        gravity = self.ball * _GRAVITATIONAL_ACCELERATION_
        # air resistance
        damping_force = -self.k_f * (pi * self.ball.redius^2) * vector_length(self.ball_speed) * np.linalg.norm(self.ball_speed)
        composition_force += gravity
        composition_force += damping_force
        
        for collision_force in collision_forces:
            composition_force += collision_force

        return composition_force
    
    def update_position_speed(self, force):
        # check whether the speed is line speed
        if sin(angle_of_vector(self.ball_speed, self.ball.center - self.bowl.center)) == 0:
            displacement = _UPDATE_INTERVAL_ * 0.001 * vector_length(self.ball_speed)
            angle = (displacement * self.bowl.redius/(self.bowl.redius - self.ball.redius))/self.bowl.redius

        a = force/self.ball.mess
        self.ball_speed += _UPDATE_INTERVAL_ * 0.001 * a


    def draw(self):
        # draw objects
        self.robot.draw()
        self.bowl.draw()
        self.ball.draw()
        self.ground.draw()

    def update_parameters(self, parameters):
        self.ball.update_parameters(parameters["redius"], parameters["ball mess"])
        self.ground.update_parameters(parameters["speed x"], parameters["speed y"])