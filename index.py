from flask import Flask
from modules.auth.controllers.api.v1.auth_controller import auth_v1_api
from modules.password.controllers.api.v1.password_controller import password_v1_api
from modules.user.controllers.api.v1.status_controller import user_status_v1_api
from modules.user.controllers.api.v1.user_controller import user_v1_api

app = Flask(__name__)

app.register_blueprint(user_status_v1_api)
app.register_blueprint(user_v1_api)
app.register_blueprint(auth_v1_api)
app.register_blueprint(password_v1_api)


@app.route("/", methods=["GET"])
def health_check():
    """ GET healthcheck
    Returns:
        tuple
    """
    return {
        "test": "hello world"
    }, 200
