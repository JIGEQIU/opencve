from flask import Blueprint
from flask_restful import Api

from opencve.api.cves import CveListResource, CveResource
from opencve.api.cwes import CweListResource, CweResource
from opencve.api.vendors import VendorListResource, VendorResource


api_bp = Blueprint("api", __name__)
api = Api(api_bp)


# Routes
api.add_resource(VendorListResource, "/vendors")
api.add_resource(VendorResource, "/vendors/<string:name>")
api.add_resource(CweListResource, "/cwe")
api.add_resource(CweResource, "/cwe/<string:id>")
api.add_resource(CveListResource, "/cve")
api.add_resource(CveResource, "/cve/<string:id>")
