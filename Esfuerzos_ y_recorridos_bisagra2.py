import xlwings as xw
import numpy as np 
from calculo_bisagra import Bisagra
from algebra.barra import Barra
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from muelle_compresion  import MuelleCompresion
from muelle_traccion import MuelleTraccion
from algebra.uniones import Union
@xw.func
def hello(name):
    return 'Hello {0}'.format(name)


# Longitudes de las barras (puedes cambiar estos valores)
l1 = 2  # Barra fija (base)
l2 = 1  # Barra de entrada
l3 = 1  # Barra acoplada
l4 = 1.5  # Barra de salida

# Ángulos iniciales
theta2 = 90  # Ángulo inicial de la barra de entrada

# Función de animación
def animate(i,mi_bisagra:Bisagra, ax):
    global theta2      
    theta2 = 20 * i / 100  # Movimiento oscilante de la barra de entrada
    # Actualizar posiciones de las barras
    barra1, barra2, barra3, barra0= mi_bisagra.get_complete_geometry(theta2)
    #print (mi_bisagra)
    # Limpiar la figura
    ax.cla()
    # Dibujar barras
    A,B = barra0.get_array_to_plot()
    ax.plot(A,B, 'ko-', lw=2, label="Barra 0 (Fija)")
    A,B = barra1.get_array_to_plot()
    ax.plot(A,B, 'bo-', lw=2, label="Barra 1 (entrada)")
    A,B = barra2.get_array_to_plot()
    ax.plot(A,B, 'ro-', lw=2, label="Barra 2 (acoplada)")
    A,B = barra3.get_array_to_plot()
    ax.plot(A,B, 'go-', lw=2, label="Barra 3 (salida)")
  #  ax.plot([barra1.get_start_point()[0], barra2.get_start_point()[0]],[barra1.get_start_point()[1], barra2.get_start_point()[1]],  'ko-', lw=2, label="Barra fija")
    
    # Configuraciones de la gráfica
    ax.set_xlim(-100, 100)
    ax.set_ylim(-2, 150)
    ax.set_aspect('equal')
    ax.grid(True)
#    if i == 1:
#        ani.event_source.stop()
#        input("press enter to continue")
#        ani.event_source.start() 
    if i == 99:
        for i in range(99, -1, -1):
            theta2 = 20 * i / 100  # Movimiento oscilante de la barra de entrada
            mi_bisagra.rotate(theta2)

def print_forces(mi_bisagra:Bisagra, ax3, ax4):
    steps = 100
    angle = 20
    angles = np.arange(0, steps) * angle / steps  # Movimiento oscilante de la barra de entrada
    distance_actuator = np.zeros(steps)
    forces = np.zeros(steps)
    distance = np.zeros(steps)
    distance_ref = mi_bisagra.get_actuators_distance(1)
    #muelle = MuelleCompresion (100, 3)
    muelle = MuelleCompresion (65, 5)
    muelle.add_constant(35, 10)
    for value in range (0, steps):
        mi_bisagra.rotate(angles[value])
        #forces[value] = mi_bisagra.get_force(0, muelle1.get_force)
        distance_actuator[value] = mi_bisagra.get_actuators_distance(0)
        forces[value] = muelle.get_force(distance_actuator[value])
        distance[value] = mi_bisagra.get_actuators_distance(1) - distance_ref
    for value in range(steps - 1, -1, -1):
        mi_bisagra.rotate(angles[value])
    ax3.plot(distance, forces)
    ax4.plot(distance, distance_actuator)
#inicio programa proncipal

#A = Barra(np.array([0, 0]),np.array([-16, 85.5]))  # Fijo en el origen
A = Barra(Union(np.array([0, 0])),Union(np.array([-40, 110])))  # Fijo en el origen
#B = Barra(np.array([30.7, 26.6]),np.array([14.68, 112.14]))  # Fijo en el origen
B = Barra(Union(np.array([30, 27])),Union(np.array([10, 95])))  # Fijo en el origen
mi_bisagra = Bisagra(A,B)
mi_bisagra.barra3.set_actuator_point(Union(np.array([25, 90])))
mi_bisagra.barra3.set_actuator_point(Union(np.array([38.55, 131.95])))
mi_bisagra.barra0.set_actuator_point(Union(np.array([20.85, 12.18])))
mi_bisagra.barra0.set_actuator_point(Union(np.array([1000, 150])))
mi_bisagra.barra1.set_actuator_point(Union(np.array([0,40])))
mi_bisagra.barra1.set_actuator_point(Union(np.array([-40,30])))
mi_bisagra.barra2.set_actuator_point(Union(np.array([60, 60])))
mi_bisagra.barra2.set_actuator_point(Union(np.array([22.7, 69.37])))

mi_bisagra.define_actuators(mi_bisagra.barra1.get_actuator(0),mi_bisagra.barra3.get_actuator(0))
mi_bisagra.define_actuators(mi_bisagra.barra0.get_actuator(1),mi_bisagra.barra3.get_actuator(1))



# Configurar la figura
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

print_forces(mi_bisagra, ax3, ax4)
# Crear la animación
ani = FuncAnimation(fig, animate, frames=100, interval=50, fargs=(mi_bisagra,ax1))

# Mostrar la animación
plt.show()

"""
Ángulo : ==  0.0
Barra1: Start [0 0], End [-16.   85.5]
Barra2: Start [30.7 26.6], End [ 14.68 112.14]

Ángulo : ==  0.0
Barra1: Start [0 0], End [-66.82796301  55.68009842]
Barra2: Start [30.7 26.6], End [-36.14930816  82.32164749]

"""