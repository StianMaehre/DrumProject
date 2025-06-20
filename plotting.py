import numpy as np
import matplotlib.pyplot as plt
import os
import sys

from matplotlib.colors import CenteredNorm
from filehandling import getFullFilepath

def plotSolution(mode, kochSquare, Ll, L, title):
    """    Plot the solution of the linear system Ax = 0.       
    Args:               

        eigenvalue (float): The eigenvalue of the solution.
        eigenvector (np.ndarray): The eigenvector of the solution.

    Returns:
        None    

    """
    start = (Ll - L) / 2

    plt.figure(dpi=200)
    plt.title(title)
    plt.imshow(mode, extent=[- start, L + start, - start, L + start], cmap='seismic', norm=CenteredNorm(vcenter=0))
    plt.plot(kochSquare[:, 0], kochSquare[:, 1], 'k-', linewidth=0.5)
    plt.colorbar(label='Amplitude')
    plt.axis("off")
    
    filename = getFullFilepath(f"{title}.png", "plots", True)
    try:
        plt.savefig(filename, bbox_inches='tight')
    except FileNotFoundError:
        print("Directory 'plots' does not exist. Please create it to save the plots.")
    
    if sys.platform.startswith("win"):
        plt.show()
    elif os.environ.get('DISPLAY', '') == '':
        print(f"No display found, unable to show the plot: {title}.")
    else:
        plt.show()
    

def plotEigenvalues(eigenvalues, eigenvectors, kochSquare, level, Ll, L):
    """Plot the eigenvalues and their corresponding eigenvectors.
    Args:
        eigenvalues (np.ndarray): The eigenvalues of the system.
        eigenvectors (np.ndarray): The eigenvectors of the system.
    Returns:
        None
    """

    n = len(eigenvalues)
    N = int(np.sqrt(len(eigenvectors[:, 0])))
    for i in range(n):
        title = f"Eigenvalue_{i + 1}_level_{level}"
        mode = eigenvectors[:, i].reshape((N, N))
        plotSolution(mode, kochSquare, Ll, L, title)