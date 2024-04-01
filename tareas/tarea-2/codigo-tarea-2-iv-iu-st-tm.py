from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.integrate import dblquad
from matplotlib.animation import FFMpegWriter, PillowWriter

# Es necesario instalar el programa ffmpeg y poner el camino hacia el archivo ejecutable
# El archivo ffmpeg.exe está en la carpeta, pero se debe descomprimir primero
plt.rcParams['animation.ffmpeg_path'] = r"C:\Users\thomm\Documents\GitHub\fisica-matematica-2\tareas\tarea-2\ffmpeg.exe"

metadata = dict(title='gaussiana', artist='santiago-tolosa')
writer = FFMpegWriter(fps=15, metadata=metadata)

# Definir constantes
a = float(input('Ingrese la longitud en x de la placa (en m): '))
b = float(input('Ingrese la longitud en y de la placa (en m): '))
alpha = float(input('Ingrese la constante de difusión térmica α (en m^2/s): '))
f_opt = input('Ingrese alguna de las siguientes opciones para la distribución inicial del calor f(x,y):\n1. Distribución Gaussiana\n2. Seno-exponencial\n3. Personalizada\n')

# Cambiar la funcion acorde a la seleccion
while(True):
    if f_opt == '1':
        def f(x, y):
            x_center = a / 2
            y_center = b / 2

            amplitude = 15
            sigma_x = a / 8  # Controla la dispersión en dirección x
            sigma_y = b / 8  # Controla la dispersión en dirección y

            gaussian = amplitude * exp(-((x - x_center)**2 / (2 * sigma_x**2) + (y - y_center)**2 / (2 * sigma_y**2)))
            return gaussian
        break
    elif f_opt == '2':
        def f(x, y):
            return 10 * sin(9*x)**2 + 3**y
        break
    elif f_opt == '3':
        f_str = input('Ingrese la función f(x,y) = ')
        def f(x, y):
            return eval(f_str)
        break
    else:
        f_opt = input('Ingresa alguna de las 3 opciones: ')

# Calcular los coeficientes Cnm
def Cnm(n, m):
    integrand = lambda x, y: f(x, y) * np.sin(n * np.pi * x / a) * np.sin(m * np.pi * y / b)
    integral, _ = dblquad(integrand, 0, b, lambda y: 0, lambda y: a)
    return (4 / (a * b)) * integral

# Calcular la temperatura en un punto (x, y, t)
def temperature(x, y, t, n_max=6, m_max=6):
    result = 0
    for n in range(1, n_max + 1):
        for m in range(1, m_max + 1):
            lambda_nm = (n * np.pi / a)**2 + (m * np.pi / b)**2
            result += Cnm(n, m) * np.sin(n * np.pi * x / a) * np.sin(m * np.pi * y / b) * np.exp(-alpha * lambda_nm * t)
    return result

# Crear la malla de puntos en la placa
x = np.linspace(0, a, 100)
y = np.linspace(0, b, 100)
X, Y = np.meshgrid(x, y)

# Crear la figura y el subplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Función para generar los datos de temperatura en cada instante de tiempo
def generate_data(frame):
    Z = temperature(X, Y, frame)
    return Z

initial_temperature = generate_data(0)
max_temperature = initial_temperature.max()

# Función para la distribución inicial del calor
def initial_distribution(x, y):
    if f_opt == '1':
        return r'$f(x,y) \sim e^{x^2 + y^2}$'
    elif f_opt == '2':
        return r'$f(x,y) = 10\sin(9x)^2 + 3^y$'
    elif f_opt == '3':
        return r'$f(x,y) = ' + f_str + '$'


# Crear la animación
with writer.saving(fig, "gaussiana.mp4", 150):
    for tval in np.linspace(0,5,150):
        print(tval)
        Z = generate_data(tval)
        ax.set_zlim(0, max_temperature)
        ax.plot_surface(X,Y,Z,cmap='hot', vmin=0, vmax=max_temperature)

        # Agregar texto con la distribución inicial del calor
        ax.text2D(0.05, 0.95, initial_distribution(X, Y) + '\n' + r'$\alpha = {:.2f} \, \mathrm{{m^2/s}}$'.format(alpha), transform=ax.transAxes, ha='left')

        # Agregar texto con el valor del tiempo en segundos
        ax.text2D(0.95, 0.95, 't = {:.1f} s'.format(tval), transform=ax.transAxes, ha='right', color='black')

        writer.grab_frame()
        plt.cla()
