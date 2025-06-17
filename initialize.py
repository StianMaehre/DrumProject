import numpy as np
import scipy.sparse as sp
import math

from matplotlib import Path

def makeKochLine(startX, startY, endX, endY):
    """
    Create a Koch curve line segment from (startX, startY) to (endX, endY).

    Args:   
        startX (float): The x-coordinate of the starting point.
        startY (float): The y-coordinate of the starting point.
        endX (float): The x-coordinate of the ending point.
        endY (float): The y-coordinate of the ending point.
    
    Returns:
        numpy.ndarray: An array of points representing the Koch curve line segment.

    Raises:
        ValueError: If the line segment is neither vertical nor horizontal.
    """
    if startX != endX and startY != endY:
        raise ValueError("The line segment must be either vertical or horizontal.")

    points = np.zeros((9, 2))

    if startX == endX:
        # Vertical line segment
        part = (endY - startY) / 4
        x = startX
        points[0] = x, startY
        points[1] = x, startY + part
        points[2] = x - part, startY + part
        points[3] = x - part, startY + 2 * part
        points[4] = x, startY + 2 * part
        points[5] = x + part, startY + 2 * part
        points[6] = x + part, startY + 3 * part
        points[7] = x, startY + 3 * part
        points[8] = x, endY

    else:
        part = (endX - startX) / 4
        y = startY
        points[0] = startX, y
        points[1] = startX + part, y
        points[2] = startX + part, y + part
        points[3] = startX + 2 * part, y + part
        points[4] = startX + 2 * part, y
        points[5] = startX + 2 * part, y - part
        points[6] = startX + 3 * part, y - part
        points[7] = startX + 3 * part, y
        points[8] = endX, y
    return points

def makeKochSquareStep(points):
    """
    Create one level higher Koch square, by
    generating Koch lines between given points.

    Args:
        points (numpy.ndarray): An array of points representing the Koch square.
    
    Returns:
        numpy.ndarray: An array of points representing the Koch square at the next level.
    """
    N = len(points) - 1
    ResPoints = np.zeros((N * 9 + 1, 2))

    for i in range(N):
        ResPoints[i * 9: (i + 1) * 9] = makeKochLine(points[i, 0], points[i, 1], points[i + 1, 0], points[i + 1, 1])
    
    ResPoints[-1] = points[-1]

    return ResPoints

def makeKochSquare(L, level):
    """
    Create a Koch square of size L and level of detail.
    """
    if level < 0:
        raise ValueError("Level must be non-negative.")
    
    points = np.zeros((5, 2))

    points[0] = 0, 0
    points[1] = L, 0
    points[2] = L, L
    points[3] = 0, L
    points[4] = 0, 0

    for i in range(level):
        points = makeKochSquareStep(points)

    return points

def isInsideKochSquare(point, kochSquare):
    """Check if a point is inside the Koch square.

    Args:
        point (tuple): A tuple (x, y) representing the point to check.
        kochSquare (numpy.ndarray): The Koch square points. 

    Returns:
        bool: True if the point is inside the Koch square, False otherwise.
    """
    path = Path(kochSquare)
    return path.contains_point(point)

def CreateAMatrix(N, interior, a):
    """ Create a sparse matrix A for the finite difference method on a grid of size N x N.

    Args:
        N (int): The size of the grid (N x N).
        interior (numpy.ndarray): A boolean array indicating which points are interior.
        a (float): The grid spacing.
    
    Returns:        
        scipy.sparse.csc_matrix: The sparse matrix A nomalized by a^2.
    """
    gridSize = N * N

    diagMain = 4 * np.ones(gridSize)
    diagx = - np.ones(gridSize - 1)
    diagy = - np.ones(gridSize - N)

    # Boundary conditions
    for i in range(1, N):
        diagx[i * N - 1] = 0

    A = sp.csc_matrix((gridSize, gridSize))

    A.setdiag(diagMain)
    A.setdiag(diagx, -1)
    A.setdiag(diagx, 1)
    A.setdiag(diagy, -N)
    A.setdiag(diagy, N)

    # Set boundary conditions for the Koch square
    for i in range(N):
        for j in range(N):
            if not interior[i, j]:
                k = N * i +  j
                A[k, :] = sp.lil_matrix((1, gridSize))
                A[k, k] = 1 

    # Convert to CSC format for efficient arithmetic operations and memory usage
    A = A.tocsc()
    A.eliminate_zeros()
    
    return A / a**2

def CalculateLl(L, level):
    """Calculate the length of the Koch curve for a given level.

    Args:
        L (float): The length of the Koch curve at level 0.
        level (int): The level of detail for the Koch curve.

    Returns:
        float: The length of the Koch curve at the specified level.
    """ 

    if level < 0:
        print("Error: Level must be non-negative.")
        return None
    
    Ll = 1
    for i in range(1, level + 1):
        Ll += 2 * 4**(-i)

    return Ll * L

def initialize(L, level, levelMin=2):
    """Initialize the Koch square and the finite difference matrix.
    Args:
        L (float): The length of the Koch square at level 0.
        level (int): The level of detail for the Koch square.
        levelMin (int, optional): The minimum level of detail. Defaults to 2.
    
    Returns:
        scipy.sparse.csc_matrix: The sparse matrix A representing the finite difference method.
        np.ndarray: the Koch square points.
        float: The length of the Koch curve Ll.
        float: The length L of the Koch square at level 0.
    """

    # Create Koch square

    if level < levelMin:
        a = L / (4**levelMin)

    else:
        a = L / (4**level)
    
    Ll = CalculateLl(L, level)
    N = math.ceil(Ll / a)

    start = (Ll - L) / 2
    end = start + L

    # Create a grid of points
    X = np.linspace(- start, end, N)
    Y = np.linspace(- start, end, N)
    kochSquare = makeKochSquare(Ll, level)
    interior = np.zeros((N, N), dtype=bool)

    # Check which points are inside the Koch square
    for i in range(N):
        for j in range(N):
            point = (X[i], Y[j])
            if isInsideKochSquare(point, kochSquare):
                interior[i, j] = True
    
    # Create the sparse matrix A
    A = CreateAMatrix(N, interior, a)
    return A, kochSquare, Ll, L

