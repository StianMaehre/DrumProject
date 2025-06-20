import pytest
import numpy as np
import os
import sys

from initialize import initialize, makeKochLine
from filehandling import writeSolutionToFile, readSolutionFromFile
from solving import solve
from plotting import plotSolution

## Initialize function tests
@pytest.fixture
def initlize_fixture():
    # Fixture to initialize the system with a specific level
    return initialize(1.0, 2)  # Example level 2 with length 1.0

def test_initialize_valid():
    # Test the initialize function with a valid level
    # and check if the returned matrix A is square and kochSquare has 2 columns.
    A, kochSquare, Ll, L = initialize(1.0, 2)
    assert A.shape[0] == A.shape[1]
    assert kochSquare.shape[1] == 2
    assert Ll > 0 and L > 0

def test_makeKochLine_horizontal():
    # Test makeKochLine for a horizontal line
    pts = makeKochLine(0, 0, 1, 0)
    assert isinstance(pts, list) or isinstance(pts, np.ndarray)

def test_makeKochLine_vertical():
    # Test makeKochLine for a vertical line
    pts = makeKochLine(0, 0, 0, 1)
    assert isinstance(pts, list) or isinstance(pts, np.ndarray)

def test_makeKochLine_diagonal():
    # Test makeKochLine for a diagonal line
    with pytest.raises(ValueError):
        makeKochLine(0, 0, 1, 1)

## Test File handling
def test_file_save_and_load(initlize_fixture):
    # Test saving and loading a numpy array to/from a file
    A, kochSquare, Ll, L = initlize_fixture
    eigenvalues, eigenvectors = solve(A)
    writeSolutionToFile(eigenvalues, eigenvectors, kochSquare, 2, Ll, L)
    loaded = readSolutionFromFile(2)
    np.testing.assert_array_equal(eigenvalues, loaded[0])
    np.testing.assert_array_equal(eigenvectors, loaded[1])
    np.testing.assert_array_equal(kochSquare, loaded[2])
    assert Ll == loaded[3]
    assert L == loaded[4]


def test_file_missing():
    # Test loading from a non-existent file
    with pytest.raises(FileNotFoundError):
        readSolutionFromFile(999)  # Assuming 999 is a non-existent level

# Test plotting
def test_plotting_no_display(monkeypatch, tmp_path):
    # Test plotting when no display is available
    monkeypatch.setenv("DISPLAY", "")
    monkeypatch.setattr(sys, "platform", "linux")
    arr = np.random.rand(10, 10)
    koch = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]])
    plotSolution(arr, koch, 1, 1, title="test")
    assert os.path.exists(f"./plots/test.png")

# 6. Test argument parsing
import subprocess
def test_help_argument():
    result = subprocess.run(
        ["python", "main.py", "--help"],
        capture_output=True, text=True
    )
    assert "usage" in result.stdout.lower()