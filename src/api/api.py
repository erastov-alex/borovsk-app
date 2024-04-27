from flask_jwt_extended import JWTManager

class Api:
    def __init__(self, app, key) -> None:
        app.config["JWT_SECRET_KEY"] = key
        self.jwt = JWTManager(app)
