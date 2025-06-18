import numpy as np

def writeSolutionToFile(eigenvalues, eigenvectors, kochSquare, level, Ll, L):
    """Write the eigenvalues and eigenvectors to a file."""
    print("Her")
    with open(f"./results/Solution{level}.pkl", "wb") as f:
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
    try:
        with open(f"./results/Solution{level}.pkl", "rb") as f:
            data = np.load(f, allow_pickle=True)
            eigenvalues = data['eigenvalues']
            eigenvectors = data['eigenvectors']
            kochSquare = data['kochSquare']
            Ll = data['Ll']
            L = data['L']
            return eigenvalues, eigenvectors, kochSquare, Ll, L
        
    except FileNotFoundError:
        print(f"File ./results/Solution{level}.pkl not found. Please run the initialization and solving first.")
        return None, None, None, None