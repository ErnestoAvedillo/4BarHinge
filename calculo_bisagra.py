import numpy as np
from algebra.intersection_circle_circle import IntersectionCircleCircle
from algebra.intersection_line_line import IntersectionLineLine
from algebra.barra import Barra
from algebra.vector import Vector
from algebra.uniones import Union
from enum import Enum

class Reacciones(Enum):
    R10x = 0
    R10y = 1
    R11x = 2
    R11y = 3
    R20x = 4
    R20y = 5
    R21x = 6
    R21y = 7
    R30x = 8
    R30y = 9
    R31x = 10
    R31y = 11
    Fx = 12
    Fy = 13
    
class Bisagra(Barra):
	def __init__(self, barra1:Barra, barra2:Barra) -> None:
		self.barra1 = barra1
		self.barra2 = barra2
		self.barra3 = Barra(barra1.get_end_union(), barra2.get_end_union())
		self.barra0 = Barra(barra1.get_start_union(), barra2.get_start_union())
		self.angle_rot = 0
		self.cir = IntersectionLineLine(barra1.get_start_point(), barra1.get_end_point(), barra2.get_start_point(), barra2.get_end_point())
		self.actuators = []
  
	def __str__(self):
		barra0_start = self.barra0.get_start_point()
		barra0_end = self.barra0.get_end_point()
		barra1_start = self.barra1.get_start_point()
		barra1_end = self.barra1.get_end_point()
		barra2_start = self.barra2.get_start_point()
		barra2_end = self.barra2.get_end_point()
		barra3_start = self.barra3.get_start_point()
		barra3_end = self.barra3.get_end_point()
		return (f"Barra0: Start {barra0_start}, End {barra0_end}\n"
      			f"Barra1: Start {barra1_start}, End {barra1_end}\n"
				f"Barra2: Start {barra2_start}, End {barra2_end}\n"
				f"Barra3: Start {barra3_start}, End {barra3_end}\n")
  
	def get_barra1(self):
		return self.barra1
	def get_barra2(self):
		return self.barra2
	def rotate(self, angle:float):
		self.barra1.rotate(angle, degrees=True)
		intersection = IntersectionCircleCircle(self.barra1.get_end_point(), self.barra3.get_length(), self.barra2.get_start_point(), self.barra2.get_length())
		Intersection_point1, Intersection_point2 = intersection.get_cartesian_intersection()
		move1 = Intersection_point1 - self.barra2.get_end_point()
		move2 = Intersection_point2 - self.barra2.get_end_point()
		if np.linalg.norm(move1) < np.linalg.norm(move2):
			self.barra2.set_new_geometry(Union(Intersection_point1))
		else:
			self.barra2.set_new_geometry(Union(Intersection_point2))
		self.barra3.set_new_geometry(Union(self.barra2.get_end_point()), Union(self.barra1.get_end_point()))
		return

	def get_complete_geometry(self, Theta:float):
		if not Theta == 0:
			self.rotate(Theta)
		return self.barra1, self.barra2, self.barra3, self.barra0

	def define_actuators(self, actuator1:Vector, actuator2:Vector):
		index = self.actuators.append([actuator1, actuator2])
		return index
	def get_actuators_distance (self, index):
		start_position = self.actuators[index][0].get_cartessian_end_point()
		end_position = self.actuators[index][1].get_cartessian_end_point()
		return np.linalg.norm(start_position - end_position)
	def get_force(self, index, law):
		return law(np.linalg.norm(self.actuators[index]))

	def calculo_dinamico():
		#Defino las ecuaciones de resolución:
		#Barra0,Barra1,Barra2(Entrada),Barra3(barra fija)
		#Descriocion de cada incógnita
  		#R00x,R00y,R01x,R01y,R10x,R10y,R11x,R11y,R20x,R20y,R21x,R21y,R30x,R30y,R31x,R31y,F2x,F2y,F3x,F3y,M0,M1,M2,M3,SF0x,SF0y+Peso,SF1x,SF1y+Peso,SF2x,SF2y+Peso,SF3x,SF3y
		#Ecuacion a resolver es del tipo AX = B
		#Matriz B 
		B = np.zeros(15)
		#Matriz A
		A = np.zeros(14,15)
		#Igualdades entre reacciones:
		reacciones = Reacciones()
		#Ecuación 0 y 1 R11 + R20 =0
		A[reacciones.R11x,0] =1
		A[reacciones.R30x,0] =1
		A[reacciones.R11y,1] =1
		A[reacciones.R30y,1] =1
		#Ecuación 1 y 2 R21 + R30 = 0
		A[reacciones.R21x,2] =1
		A[reacciones.R31x,2] =1
		A[reacciones.R21y,3] =1
		A[reacciones.R31y,3] =1
		#Equilibrio barra1
		A[reacciones.R10x,4] =1
		A[reacciones.R11x,4] =1
		A[reacciones.R10y,4] =1
		A[reacciones.R11y,4] =1

