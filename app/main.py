from flask import Flask
from flask_cors import CORS
from controller.usuario_controller import UsuarioController
from controller.dashboard_controller import DashboardController

app = Flask(__name__)
usuario_controller = UsuarioController(app)
dashboard_controller = DashboardController(app)

CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ]
    }
}, supports_credentials=True)

if __name__ == "__main__":
    app.run(debug=True)
