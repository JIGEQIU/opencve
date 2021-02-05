from flask import Blueprint
from flask_restful import Api

from opencve.api.vendors import VendorListResource


custom_errors = {
    "ResourceNotFound": {
        "message": "Not found.",
        "status": 404,
    }
}

api_bp = Blueprint("api", __name__)
api = Api(api_bp, errors=custom_errors)


# Routes
api.add_resource(VendorListResource, "/vendors")
