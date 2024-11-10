# Funciones asociadas a Bessel de scipy.special
# https://docs.scipy.org/doc/scipy/reference/special.html

import numpy as np
from scipy.special import *
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})


def Bessel(v, x, p__max = 21):
    s = 0
    for p in range(p__max):
        s += (-1)**p * (x/2)**(v+2*p) / factorial(p) / gamma(v + p + 1)
    return s

print(Bessel(0, 3))
print(j0(3))


def plot_Jv():
    x = np.linspace(-10, 10, 1000)

    #v_values = [0, 1, 2, 3, 4]
    #v_values = [0, 0.1, 0.5, 0.8]
    v_values = [0, -1, -2, -3, -4]

    plt.figure()

    for v in v_values:
        plt.plot(x, jv(v, x), label=f'$-\\nu={v}$')

    plt.xlabel(r'$x$')
    plt.ylabel(r'$J_{-\nu}(x)$')
    plt.title(r'Negative Bessel Functions of the First Kind $J_{-\nu}(x)$')
    plt.legend()

    plt.grid(True, color='lightgray')
    plt.savefig('special-functions/images/bessel-negative-integers.pdf', format='pdf')
    plt.show()


def plot_Nn():
    x = np.linspace(0, 10, 1000)

    n_values = [0, 1, 2, 3, 4]

    plt.figure()

    for n in n_values:
        plt.plot(x, yn(n, x), label=f'$n={n}$')

    plt.xlabel(r'$x$')
    plt.ylabel(r'$N_{n}(x)$')
    plt.title(r'Bessel Functions of the Second Kind (Neumann Functions) $Y_{n}(x) = N_n(x)$')
    plt.ylim(-2, 2)
    plt.legend()

    plt.grid(True, color='lightgray')
    plt.savefig('ingresa-la-direccion', format='pdf')
    plt.show()


plot_Jv()