import os
import sys
import subprocess

# Helper function to execute shell commands
def run_command(command, error_message):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message}\nDetails: {e}")
        sys.exit(1)

def main():
    # Check Python version
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        sys.exit(1)

    # Define virtual environment directory
    venv_dir = "venv"

    # Step 1: Create a virtual environment
    print("Creating virtual environment...")
    if not os.path.exists(venv_dir):
        run_command(f"{sys.executable} -m venv {venv_dir}", "Failed to create virtual environment.")
    else:
        print("Virtual environment already exists.")

    # Step 2: Activate the virtual environment
    print("Activating virtual environment...")
    if os.name == "nt":  # Windows
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:  # macOS/Linux
        activate_script = os.path.join(venv_dir, "bin", "activate")

    if not os.path.exists(activate_script):
        print("Error: Activation script not found.")
        sys.exit(1)

    # Step 3: Install packages from requirements.txt
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print("Error: requirements.txt file not found in the current directory.")
        sys.exit(1)

    print("Installing packages from requirements.txt...")
    run_command(f"{venv_dir}/bin/pip install -r {requirements_file}" if os.name != "nt" else f"{venv_dir}\\Scripts\\pip install -r {requirements_file}", "Failed to install required packages.")

    # Step 4: Run app.py
    app_file = "app.py"
    if not os.path.exists(app_file):
        print("Error: app.py file not found in the current directory.")
        sys.exit(1)

    print("Running app.py...")
    run_command(f"{venv_dir}/bin/python {app_file}" if os.name != "nt" else f"{venv_dir}\\Scripts\\python {app_file}", "Failed to run app.py.")

if __name__ == "__main__":
    main()
