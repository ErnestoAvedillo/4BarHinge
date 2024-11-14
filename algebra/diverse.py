import math
import numpy as np

def get_angle_vector(vector:np)->float:
	return math.atan2(vector[1], vector[0])

def get_unitary_vector(angle:float) -> np:
	return np.array([math.cos(angle), math.sin(angle)])

def convert_polar_to_cartessian(vector:np) -> np:
    return vector[0] * get_unitary_vector(vector[1])

def convert_cartessian_to_polar(vector:np) -> np:
    return np.array([np.linalg.norm(vector),get_angle_vector(vector)])
