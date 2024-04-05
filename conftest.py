import sys
import os

# Get the current directory of this file
current_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory (project root) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, '..')))
