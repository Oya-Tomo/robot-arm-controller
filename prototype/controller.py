import math

PI = 3.1415


def get_vertex_angle(a: float, b: float, c: float) -> tuple[float, float, float]:
    s = (a + b + c) / 2
    S = math.sqrt(s * (s - a) * (s - b) * (s - c))
    A, B, C = 0, 0, 0

    if a >= b and a >= c:
        h = 2 * S / a
        B = math.asin(h / c)
        C = math.asin(h / b)
        A = PI - B - C

    elif b >= a and b >= c:
        h = 2 * S / b
        A = math.asin(h / c)
        C = math.asin(h / a)
        B = PI - A - C

    else:  # c >= a and c >= b
        h = 2 * S / c
        A = math.asin(h / b)
        B = math.asin(h / a)
        C = PI - A - B

    return A, B, C


class Arm3Joints:
    def __init__(
        self,
        arms_length: tuple[float, float, float],  ## length : mm
        joints_angle: tuple[float, float, float],  ## angle : radian
    ):
        self.arms_length = arms_length
        self.joints_angle = joints_angle

        self.tip_position = None  # arm tip position
        self.tip_angle = None  # arm tip angle

        self._is_checked = False  # check arm length and angles

    def set_tip_position(
        self,
        position: tuple[float, float],
    ) -> None:
        self.tip_position = position

    def set_tip_angle(
        self,
        angle: float,
    ) -> None:
        self.tip_angle = angle

    def convert_angles_quadrant(self):
        for i in range(len(self.joints_angle)):
            pass
            # WIP

    def calculate(self) -> bool:
        arm_root, arm_middle, arm_head = self.arms_length

        # calculate head angle
        x1 = self.tip_position[0] - (math.cos(self.tip_angle) * arm_head)
        y1 = self.tip_position[1] - (math.sin(self.tip_angle) * arm_head)

        # check arm limit
        length = math.sqrt(x1 * x1 + y1 * y1)
        arm_limit = arm_middle + arm_root

        # The limit value is made small to allow for arm length margin.
        if not (10 < length and length < arm_limit - 10):
            return False

        A, B, C = get_vertex_angle(length, arm_root, arm_middle)

        length_angle = math.atan(y1 / x1)

        joint_root = PI / 2 + length_angle + B
        joint_middle = A
        joint_head = C + (PI / 2 - length_angle) + PI / 2 + self.tip_angle
        self.joints_angle = (joint_root, joint_middle, joint_head)

        return True


if __name__ == "__main__":
    controller = Arm3Joints(
        [50, 50, 50],
        [PI / 4 * 3, PI / 2, PI / 4 * 5],
    )

    controller.set_tip_position((120.7, 0))
    controller.set_tip_angle(0)
    print("status : ", controller.calculate())
    print("angles : ", controller.joints_angle)

    # a, b, c = get_vertex_angle(1, 1.7320508, 2)

    # print(math.degrees(a), math.degrees(b), math.degrees(c))
