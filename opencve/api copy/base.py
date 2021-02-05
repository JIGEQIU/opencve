from functools import wraps

from flask import request
from flask import current_app as app
from flask_restful import Resource, reqparse, HTTPException

# from saucs.extensions import limiter
from opencve.models.users import User


class ResourceNotFound(HTTPException):
    code = 404


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization

        def error_message():
            return (
                {"message": "Authentication required."},
                401,
                {"WWW-Authenticate": 'Basic realm="Authentication Required"'},
            )

        # Auth not provided
        if not auth:
            return error_message()

        # User not found
        user = User.query.filter_by(username=auth.username).first()
        if not user:
            return error_message()

        # Bad credentials
        if not app.user_manager.verify_password(auth.password, user):
            return error_message()

        f = func(*args, **kwargs)

        return f

    return wrapper


class BaseResource(Resource):
    """decorators = [
        limiter.shared_limit(
            scope='api',
            limit_value=lambda: app.config['API_RATELIMIT'],
            key_func=lambda: request.authorization.username,

            # Hardcoded admins here instead of finding it in
            # database to avoid a query during each request.
            exempt_when=lambda: request.authorization.username in ['ncrocfer', 'Laurent']
        ),
        auth_required
    ]"""

    decorators = [
        auth_required,
    ]

    def get_arguments(self, arguments):
        parser = reqparse.RequestParser()

        for name, properties in arguments.items():
            kwargs = {"location": "args", "type": properties["type"]}

            if "default" in properties:
                kwargs["default"] = properties["default"]

            parser.add_argument(name, **kwargs)

        return parser.parse_args()
