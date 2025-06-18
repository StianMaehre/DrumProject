import argparse
import numpy as np
import pickle
import time

from initialize import initialize
from solving import solve
from plotting import plotEigenvalues
from filehandling import writeSolutionToFile, readSolutionFromFile

def checkArgLevel(value):
    """Check if the argument level is a non-negative integer."""
    try:
        value = int(value)
        if value < 0:
            raise argparse.ArgumentTypeError("level must be a non-negative integer.")
        elif value > 10:
            raise argparse.ArgumentTypeError("level must be less than or equal to 10.")
        elif value > 4:
            print("Warning: Level greater than 4 may take a long time to compute.")
        return value
    except ValueError:
        raise argparse.ArgumentTypeError("level must be a non-negative integer.")


def main():
    L, level, action = Argparser()

    if action == "initialize and solve":
        print(f"Level: {level}, Length: {L}")
        print("Initializing the Koch square and solving the system...")
        starttime = time.time()
        A, kochSquare, Ll, L = initialize(L, level)
        print(f"Initialization took {time.time() - starttime:.2f} seconds.")

        print("Solving the system...")
        starttime = time.time()
        eigenvalues, eigenvectors = solve(A)
        print(f"Solving took {time.time() - starttime:.2f} seconds.")
        print("Writing solution to file...")
        writeSolutionToFile(eigenvalues, eigenvectors, kochSquare, level, Ll, L)
        print("Solution written to file successfully.")

    elif action == "plot":
        print(f"Level: {level}, Length: {L}")
        eigenvalues, eigenvectors, kochSquare, Ll, L = readSolutionFromFile(level)
        if eigenvalues is None or eigenvectors is None:
            print("No solution found. Please run the initialization and solving first.")
        else:
            plotEigenvalues(eigenvalues, eigenvectors, kochSquare, Ll, L)
            print("Plotting completed successfully.")
    
    elif action == "all":
        print(f"Level: {level}, Length: {L}")
        print("Initializing the Koch square and solving the system...")
        starttime = time.time()
        A, kochSquare, Ll, L = initialize(L, level)
        print(f"Initialization took {time.time() - starttime:.2f} seconds.")

        print("Solving the system...")
        starttime = time.time()
        eigenvalues, eigenvectors = solve(A)
        print(f"Solving took {time.time() - starttime:.2f} seconds.")

        print("Writing solution to file...")
        writeSolutionToFile(eigenvalues, eigenvectors, kochSquare, level, Ll, L)
        print("Solution written to file successfully.")

        print("Plotting the eigenvalues and eigenvectors...")
        plotEigenvalues(eigenvalues, eigenvectors, kochSquare, Ll, L)
        print("Plotting completed successfully.")

def Argparser():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    #parser.add_argument("--help", action="help", help="Show this help message and exit.")
    parser.add_argument("--action", choices=["initializeAndSolve", "plot", "all"], default="all", help="Action to perform: initialize, solve, plot, or all.")
    parser.add_argument("--L", type=float, default=1.0)
    parser.add_argument("--level", type=int, default=2)
    args = parser.parse_args()
    return args.L, args.level, args.action

if __name__ == "__main__":
    main() 