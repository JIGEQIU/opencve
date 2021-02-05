from flask import jsonify, request


from opencve.api._bp import api
from opencve.controllers.products import get_products


@api.route("/vendors/<vendor>/products")
def products(vendor):
    objects, _, _ = get_products(vendor, request.args)
    return jsonify([o.to_dict(["name", "human_name"]) for o in objects.items])
