import sys
import os

#from inventory_api.app import create_app
from app import create_app

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
