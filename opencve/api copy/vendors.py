"""from flask import jsonify, request


from opencve.api._bp import api
from opencve.controllers.vendors import get_vendors


@api.route("/vendors")
def vendors():
    objects, _, _ = get_vendors(request.args)
    return jsonify([o.to_dict(["name", "human_name"]) for o in objects.items])"""


from flask_restful import fields, marshal_with

from opencve.api.base import BaseResource
from opencve.api.fields import HumanizedNameField


vendor_list_fields = {
    "name": fields.String(attribute="name"),
    "human_name": HumanizedNameField(attribute="name"),
}


class VendorListResource(BaseResource):
    @marshal_with(vendor_list_fields)
    def get(self):
        args = self.get_arguments({"page": {"type": int, "default": 1}})

        q = Vendor.query.order_by(Vendor.name.asc())
        vendors = q.paginate(args["page"], 10, False).items

        return vendors
