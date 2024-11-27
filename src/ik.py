import math


def get_vertex_angle(a: float, b: float, c: float) -> tuple[float, float, float]:
    s = (a + b + c) / 2
    S = math.sqrt(s * (s - a) * (s - b) * (s - c))
    A, B, C = 0, 0, 0

    if a >= b and a >= c:
        h = 2 * S / a
        B = math.asin(h / c)
        C = math.asin(h / b)
        A = math.pi - B - C

    elif b >= a and b >= c:
        h = 2 * S / b
        A = math.asin(h / c)
        C = math.asin(h / a)
        B = math.pi - A - C

    else:  # c >= a and c >= b
        h = 2 * S / c
        A = math.asin(h / b)
        B = math.asin(h / a)
        C = math.pi - A - B

    return A, B, C


def deg_to_rad(deg: float) -> float:
    return deg * math.pi / 180


def rad_to_deg(rad: float) -> float:
    return rad * 180 / math.pi


class ArmIK:
    def __init__(self, tip, mid, base):
        self.tip = tip
        self.mid = mid
        self.base = base

    def calculate(self, x, y, tip_angle) -> tuple[float, float, float] | None:
        if x < 0:
            return None

        if not (-math.pi / 2 <= tip_angle <= math.pi / 2):
            return None

        x1 = x - (math.cos(tip_angle) * self.tip)
        y1 = y - (math.sin(tip_angle) * self.tip)

        dist = math.sqrt(x1 * x1 + y1 * y1)

        if dist > self.mid + self.base:
            return None

        a, b, c = get_vertex_angle(self.mid, self.base, dist)

        dist_angle = math.atan2(y1, x1)

        jb = math.pi / 2 + dist_angle + a
        jm = c
        jt = b + (math.pi / 2 - dist_angle) + math.pi / 2 + tip_angle
        return jb, jm, jt


if __name__ == "__main__":
    ik = ArmIK(10, 10, 10)
