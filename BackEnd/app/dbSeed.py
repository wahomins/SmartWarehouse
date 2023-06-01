import os
import glob
import importlib.util
from flask import current_app
from werkzeug.local import LocalProxy



logger = LocalProxy(lambda: current_app.logger)

def run_seed():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the module name
    module_name = os.path.basename(current_dir)

    # Path to the seed folder
    seed_folder = os.path.join(current_dir, "seed")

    # Check if the seed folder exists
    if os.path.isdir(seed_folder):
        # Get all the Python files in the seed folder
        seed_files = [f for f in os.listdir(seed_folder) if f.endswith(".py")]

        # Import and execute each seed file
        for seed_file in seed_files:
            try:
                seed_file_path = os.path.join(seed_folder, seed_file)
                
                # Import and execute the seed file
                spec = importlib.util.spec_from_file_location(f"{module_name}_seed", seed_file_path)
                seed_module = importlib.util.module_from_spec(spec)
                logger.info(f'Executing seed file: {seed_file_path}')
                spec.loader.exec_module(seed_module)
            except Exception as e:
                logger.error(f'Error executing seed file: {seed_file}')
                logger.exception(e)
