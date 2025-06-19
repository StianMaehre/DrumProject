import scipy as sp

from config import NUMBER_OF_EIGENVALUES

def solve(A, n=10):
    """Solve the linear system Ax = 0 with a given tolerance.

    Args:
        A (scipy.sparse.csc_matrix): The sparse matrix representing the system.
        n (int, optional): The number of smallest eigenvalues to compute. Defaults to 10.
    
    Returns:
        np.ndarray: The solution vector x.
    """

    n = NUMBER_OF_EIGENVALUES
    eigenvalues, eigenvectors = sp.sparse.linalg.eigsh(A, k=n, which='SM')

    return eigenvalues, eigenvectors
