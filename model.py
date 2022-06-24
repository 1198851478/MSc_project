from objects import *

def distance(vector_1, vector_2):
    return sqrt((vector_1[0] - vector_2[0])^2 + (vector_1[1] - vector_2[1])^2 + (vector_1[2] - vector_2[2])^2)

def check_with_cube(center_ball, center_cube, r, b, a, c):
    return abs(center_ball[0] - center_cube[0] < a/2 + r) \
        and abs(center_ball[1] - center_cube[1] < b/2 + r) and abs(center_ball[2] - center_cube[2])<= c/2 + r

class model:
    def __init__(self):
        # objects
        self.robot = robot()
        self.bowl = bowl()
        self.ball = ball()
        self.ground = ground()
        self.k_p = 0.5
        self.k_v = 0.5
        self.ball_speed = [0.0, 0.0, 0.0]

    def collision_detection(self):
        collision_flag = 0x00
        distance_with_bowl = distance(self.ball.center, self.bowl.center)
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

    def collision_force(self, collision_flag):
        if collision_flag & 0x01:
            interact_dis = distance(self.ball.center, self.bowl.center) + self.ball.redius - self.bowl.redius
        pass

    def draw(self):
        # draw objects
        self.robot.draw()
        self.bowl.draw()
        self.ball.draw()
        self.ground.draw()

    def update_parameters(self, parameters):
        self.ball.update_parameters(parameters["redius"], parameters["ball mess"])
        self.ground.update_parameters(parameters["speed x"], parameters["speed y"])