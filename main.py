import argparse
import numpy as np
import pickle
import time

from initialize import initialize
from solving import solve
from plotting import plotEigenvalues
from filehandling import writeSolutionToFile, readSolutionFromFile
from config import DEFAULT_L, MAXIMUM_LEVEL

def checkArgLevel(value):
    """Check if the argument level is a non-negative integer."""
    try:
        value = int(value)
        if value < 0:
            raise argparse.ArgumentTypeError("level must be a non-negative integer.")
        elif value > MAXIMUM_LEVEL:
            raise argparse.ArgumentTypeError(f"level must be less than or equal to {MAXIMUM_LEVEL}.")
        elif value > 4:
            print("Warning: Level greater than 4 may take a long time to compute.")
        return value
    except ValueError:
        raise argparse.ArgumentTypeError("level must be a non-negative integer.")

def main():
    level, action = Argparser()
    L = DEFAULT_L

    if action == "initializeAndSolve":
        print(f"Level: {level}, Length: {L}")
        print("Initializing the system...")
        starttime = time.time()
        A, kochSquare, Ll, L = initialize(L, level)
        print(f"Initialization took {time.time() - starttime:.2f} seconds.\n")

        print("Solving the system...")
        starttime = time.time()
        eigenvalues, eigenvectors = solve(A)
        print(f"Solving took {time.time() - starttime:.2f} seconds.\n")

        print("Writing solution to file...")
        writeSolutionToFile(eigenvalues, eigenvectors, kochSquare, level, Ll, L)
        print("Solution written to file successfully.")

    elif action == "plot":
        print(f"Level: {level}, Length: {L}")
        eigenvalues, eigenvectors, kochSquare, Ll, L = readSolutionFromFile(level)
        if eigenvalues is None or eigenvectors is None:
            print("No solution found. Please run the initialization and solving first.")
        else:
            plotEigenvalues(eigenvalues, eigenvectors, kochSquare, level, Ll, L)
            print("Plotting completed successfully.")
    
    elif action == "all":
        print(f"Level: {level}, Length: {L}")
        print("Initializing the system...")
        starttime = time.time()
        A, kochSquare, Ll, L = initialize(L, level)
        print(f"Initialization took {time.time() - starttime:.2f} seconds. \n")

        print("Solving the system...")
        starttime = time.time()
        eigenvalues, eigenvectors = solve(A)
        print(f"Solving took {time.time() - starttime:.2f} seconds.\n")

        print("Writing solution to file...")
        writeSolutionToFile(eigenvalues, eigenvectors, kochSquare, level, Ll, L)
        print("Solution written to file successfully.\n")

        print("Plotting the eigenvalues and eigenvectors...")
        plotEigenvalues(eigenvalues, eigenvectors, kochSquare, level, Ll, L)
        print("Plotting completed successfully.")

def Argparser():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["initializeAndSolve", "plot", "all"], default="all", help="Action to perform: initialize and solve, plot or all. Default is all")
    parser.add_argument("--level", type=int, default=2, help=f"Level of detail for the Koch curve (0-{MAXIMUM_LEVEL}).")
    args = parser.parse_args()
    return args.level, args.action

if __name__ == "__main__":
    main() 