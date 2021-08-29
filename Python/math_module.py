import numpy as np


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def landmarks2quaternion(u, v):
    theta = get_angle(u, v)
    axis = get_vector(u, v)

    w = np.cos(theta / 2)
    sin = np.sin(theta / 2)
    x = axis.x * sin
    y = axis.y * sin
    z = axis.z * sin

    return [x, y, z, w]


def get_angle(u, v):
    return np.arctan((norm(cross_product(u, v)) / dot_product(u, v)))


def get_vector(u, v):
    x = cross_product(u, v)
    y = norm(x)
    x_1 = x.x / y
    x_2 = x.y / y
    x_3 = x.z / y

    return Vector(x_1, x_2, x_3)


def norm(d3_v):  # 놂
    array = np.array([d3_v.x, d3_v.y, d3_v.z])  # 배열의 생성
    square = np.square(array)  # 원소들의 제곱
    squaresum = np.sum(square)  # 원소들의 합
    sqrt = np.sqrt(squaresum)  # 합의 제곱근
    return sqrt  # 제곱근의 반환


def normalized(d3_v):  # normalized 된 벡터를 반환하는 함수를 정의한다
    value = norm(d3_v)  # 입력된 벡터의 magnitude을 구한다
    x = d3_v.x / value  # 입력된 벡터의 각 성분들을 입력된 vector의 magnitude로 나눈다.
    y = d3_v.y / value
    z = d3_v.z / value

    return Vector(x, y, z)


def cross_product(d3_u, d3_v):  # cross product를 정의한다
    x_1 = (d3_u.y * d3_v.z) - (d3_u.z * d3_v.y)  # u2v3-u3v2
    x_2 = (d3_u.z * d3_v.x) - (d3_u.x * d3_v.z)  # u3v1-u1v3
    x_3 = (d3_u.x * d3_v.y) - (d3_u.y * d3_v.x)  # u1v2-u2v1

    return Vector(x_1, x_2, x_3)  # 입력된 두 벡터에 모두 수직인 벡터를 반환


def dot_product(d3_u, d3_v):  # dot product를 정의한다
    scalar = (d3_u.x * d3_v.x) + (d3_u.y * d3_v.y) + (d3_u.z * d3_v.z)  # u1v1 + u2v2 + u3v3
    return scalar