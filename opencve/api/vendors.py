from flask import request
from flask_restful import fields, marshal_with

from opencve.api.base import BaseResource
from opencve.api.fields import HumanizedNameField, ProductsListField
from opencve.controllers.vendors import VendorController


vendor_list_fields = {
    "name": fields.String(attribute="name"),
    "human_name": HumanizedNameField(attribute="name"),
}

vendor_fields = dict(vendor_list_fields, **{
    'products': ProductsListField(attribute='products')
})


class VendorListResource(BaseResource):
    @marshal_with(vendor_list_fields)
    def get(self):
        return VendorController.list_items(request.args)


class VendorResource(BaseResource):
    @marshal_with(vendor_fields)
    def get(self, name):
        return VendorController.get({"name": name})
