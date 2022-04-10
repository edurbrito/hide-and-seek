from operator import ne
import random
from math import pi, cos, sin, atan2, sqrt


EARTH_RADIUS = 6371000
RANGE = (10, 300)
RAD = pi / 180
DEG = 180 / pi


def calculate_circle_center(position):
    latitude = float(position[0])
    longitude = float(position[1])
    dx = random.randint(RANGE[0], RANGE[1])
    dy = random.random(RANGE[0], RANGE[1])
    new_latitude = latitude + (dy / EARTH_RADIUS) * DEG
    new_longitude = longitude + (dx / EARTH_RADIUS) * DEG / cos(longitude * RAD)

    return new_latitude, new_longitude

def calculate_distance(position1, position2):
    latitude1 = float(position1[0])
    longitude1 = float(position1[1])
    latitude2 =float(position2[0])
    longitude2 = float(position2[1])

    phi1 = latitude1 * RAD
    phi2 = latitude2 * RAD
    dphi = (latitude2 - latitude1) * RAD
    dlambda = (longitude2 - longitude1) * RAD

    a = sin(dphi/2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = EARTH_RADIUS * c
    return distance
