from flask import Flask
from modules.user.controllers.api.v1.status_controller import user_status_v1_api

app = Flask(__name__)

app.register_blueprint(user_status_v1_api)

app.run(debug=True)
