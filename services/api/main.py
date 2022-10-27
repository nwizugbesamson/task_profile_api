import pathlib
import dotenv
from flask import Flask, jsonify
from flask.cli import FlaskGroup
from flask_cors import CORS 
from flask_restx import Api, Resource, fields
from decouple import config


## load environment variables
DOT_ENV_PATH = pathlib.Path() / '.env.*.*'
if DOT_ENV_PATH.exists():
    dotenv.load_dotenv(dotenv_path=str(DOT_ENV_PATH))


## configuration for flask object
class Config:
    SECRET_KEY: str = config('SECRET_KEY', 'abc1234')
    DEBUG: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False



## instantiate application
app = Flask(__name__)
app.config.from_object(Config)

## cors module for cross platform integration
cors = CORS()
cors.init_app(app)

## instantiate restx api with application instance
api = Api(
    app,
    version="1.0",
    title="profile API",
    description="Hng Profile API task",
    doc="/ui"
)



## response model
profile_model = api.model(
    "Profile", {
        "slackUsername": fields.String(required=True, description="username"),
        "backend": fields.Boolean(required=True),
        "age": fields.Integer(required=True, description="age"),
        "bio": fields.String(required=True, description="user bio information")
        }
)




@api.route("/profile")
@api.doc(responses={200: "user profile information"})
class Profile(Resource):
    """return user profile information"""

    @api.doc(description="return user profile")
    @api.marshal_with(profile_model)
    def get(self):
        """Fetch user profile information"""
        return {
                "slackUsername": "samson6398",
                "backend": True,
                "age": 24,
                "bio": "intermediate python developer"
        }
        
        


cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()