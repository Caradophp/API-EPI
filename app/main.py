from flask import Flask
from app.controller.usuario_controller import UsuarioController
from app.controller.dashboard_controller import DashboardController

app = Flask(__name__)
usuario_controller = UsuarioController(app)
dashboard_controller = DashboardController(app)


if __name__ == "__main__":
    app.run(debug=True)
