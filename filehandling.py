import numpy as np
import os

def getFullFilepath(filename, subdir, makeNewDir) -> str:
    """
    Return the full path to a results file in the specified subdirectory.

    Args:
        filename (str): filname to be saved
        subdir (str): Name of the subdirectory where the file will be saved.

    Returns:
        str: Full path to the results file.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, subdir)
    if not os.path.exists(subdir):
        if makeNewDir:
            print(f"Creating directory: {subdir}")
            os.makedirs(subdir)
        else:
            raise NotADirectoryError(f"{subdir} is not a directory.")
    
    os.makedirs(target_dir, exist_ok=True)
    return os.path.join(target_dir, filename)

def writeSolutionToFile(eigenvalues, eigenvectors, kochSquare, level, Ll, L):
    """Write the eigenvalues and eigenvectors to a file."""

    filename = getFullFilepath(f"Solution{level}.pkl", "results", True)
    with open(filename, "wb") as f:
        data = {
            "eigenvalues": eigenvalues,
            "eigenvectors": eigenvectors,
            "kochSquare": kochSquare,
            "Ll": Ll,
            "L": L
        }
        np.savez(f, **data)

    print(f"Solution for level {level} written to ./results/Solution{level}.pkl successfully.")

def readSolutionFromFile(level):
    """Read the eigenvalues and eigenvectors from a file."""

    filename = getFullFilepath(f"Solution{level}.pkl", "results", False)

    if not os.path.exists(filename):
        raise FileNotFoundError(f"File ./results/Solution{level}.pkl not found. Please run the initialization and solving first for level: {level}.")
    
    with open(f"./results/Solution{level}.pkl", "rb") as f:
        data = np.load(f, allow_pickle=True)
        eigenvalues = data['eigenvalues']
        eigenvectors = data['eigenvectors']
        kochSquare = data['kochSquare']
        Ll = data['Ll']
        L = data['L']
        return eigenvalues, eigenvectors, kochSquare, Ll, L
    