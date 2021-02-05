from flask import request, render_template

from opencve.controllers.main import main
from opencve.controllers.products import get_products


@main.route("/vendors/<vendor>/products")
def products(vendor):
    products, vendor, pagination = get_products(vendor, request.args)

    return render_template(
        "products.html", products=products, vendor=vendor, pagination=pagination
    )
