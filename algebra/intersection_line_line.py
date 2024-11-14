import numpy as np
class IntersectionLineLine:
    def __init__(self, vector1:np, point1:np, vector2:np, point2:np):
        self.vector1 = vector1
        self.vector2 = vector2
        self.point1 = point1
        self.point2 = point2
        
    def get_cartesian_intersection(self):
        # Solve for t and s in the parametric equations of the lines
        A = np.array([self.vector1, -self.vector2]).T
        b = np.array(self.point2 - self.point1)
        try:
            t, s = np.linalg.solve(A, b)
            intersection_point = self.point1 + t * self.vector1
            return intersection_point
        except np.linalg.LinAlgError:
            return None  # No intersection or infinite intersections
    def get_polar_intersection(self):
        intersection_point=self.get_cartesian_intersection()
        return np.linalg.norm(intersection_point), np.arctan2(intersection_point[1], intersection_point[0])