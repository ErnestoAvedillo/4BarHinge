import numpy as np

class DistancePointLine:
    def __init__(self, point:np, vector:np, vector_point:np):
        self.point = point
        self.vector = vector / np.linalg.norm(vector)
        self.vector_point = vector_point
    def get_distance(self)->float:
        vector_point1_point2 = self.point - self.vector_point
        return (np.cross(self.vector, vector_point1_point2) )
    def get_cartessian_proyection_point(self)->np:
        if self.get_distance() == 0.0:
            return self.point
        vector_point_point2 = self.point - self.vector_point
        vector_proyection = self.vector * abs(np.cross(self.vector, vector_point_point2)) 
        return (self.vector_point + vector_proyection)
    def get_polar_point_proyection(self)->np:
        proyection_point = self.get_proyection_point()
        return (np.linalg.norm(proyection_point), np.arctan2(proyection_point[1], proyection_point[0]))


"""
v1 = np.array([4, 4])
v2 = np.array([2, 0])
p1 = np.array([1, 0])
a = DistancePointLine(v1, v2, p1)
print(a.get_distance())
print(a.get_cartessian_proyection_point())
b= DistancePointLine(v2,v1,p1)
print(b.get_distance())
print(b.get_cartessian_proyection_point())

"""