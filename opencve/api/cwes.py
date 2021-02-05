from flask import request
from flask_restful import fields, marshal_with

from opencve.api.base import BaseResource
from opencve.controllers.cwes import CweController


cwes_fields = {
    "id": fields.String(attribute="cwe_id"),
    "name": fields.String(attribute="name"),
    "description": fields.String(attribute="description"),
}


class CweListResource(BaseResource):
    @marshal_with(cwes_fields)
    def get(self):
        return CweController.list_items(request.args)


class CweResource(BaseResource):
    @marshal_with(cwes_fields)
    def get(self, id):
        return CweController.get({"cwe_id": id})
