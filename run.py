from app import create_app
from flask_cors import CORS

app = create_app()

# Enable CORS for all routes and origins
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)  # Set debug to False in production
