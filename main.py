import argparse
import numpy as np
import pickle
from initialize import initialize
from solving import solve
from plotting import plotEigenvalues

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("action", choices=["initialize", "solve", "plot"])
    parser.add_argument("--L", type=float, default=1.0)
    parser.add_argument("--level", type=int, default=2)
    parser.add_argument("--solutionfile", default="solution.npy")
    parser.add_argument("--matrixfile", default="matrix.pkl")
    args = parser.parse_args()

    A, kochSquare, Ll, L = initialize(args.L, args.level)
    eigenvalues, eigenvectors = solve(A)
    plotEigenvalues(eigenvalues, eigenvectors, kochSquare, Ll, L)

if __name__ == "__main__":
    main()