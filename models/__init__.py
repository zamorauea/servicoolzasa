from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # o usa Config

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # ruta de login

from app.models.model_login import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

from app import routes
