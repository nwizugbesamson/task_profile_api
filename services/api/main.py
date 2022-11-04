import pathlib
import dotenv
from http import HTTPStatus
from flask import Flask, request
from flask.cli import FlaskGroup
from flask_cors import CORS 
from flask_restx import Api, Resource, fields
from decouple import config
from calculator import process_operation


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



## models
profile_model = api.model(
    "Profile", {
        "slackUsername": fields.String(required=True, description="username"),
        "backend": fields.Boolean(required=True),
        "age": fields.Integer(required=True, description="age"),
        "bio": fields.String(required=True, description="user bio information")
        }
)

operation_payload = api.model(
    "Operation_payload", {
        "operation_type": fields.String(
            required=True,
            description="specified operator. Enum<addition | subtraction | multiplication>"
        ),
        "x": fields.Integer(required=False, description="first operand"),
        "y": fields.Integer(required=False, description="second operand"),
    }
)


operation_response = api.model(
    "Operation_response", {
        "slackUsername": fields.String(
            required=True,
            description="author identification"
        ),
        "result": fields.Integer(
            description="operation result"
        ),
        "operation_type": fields.String(
            description="input operator"
        )
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
        
        
@api.route("/calculator")
@api.doc(responses={
    HTTPStatus.OK: 'operation result',
    HTTPStatus.BAD_REQUEST: "provide valid input operands",
    HTTPStatus.BAD_REQUEST: "failed to calculate result",
},
params={
    "operation_type": "Enum<addition | subtraction | multiplication>",
    "x": "first operand",
    "y": "second operand"
})
class Calculator(Resource):
    """Return result of input operands and operator"""

    @api.expect(operation_payload)
    @api.marshal_with(operation_response)
    def post(self):
        """return result of simple calculation model
        """
        
        data = request.get_json()
        print(f'DATA IS: {data}')
        return process_operation(data)


cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()