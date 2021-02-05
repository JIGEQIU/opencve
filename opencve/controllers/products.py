from flask import current_app as app
from flask import abort
from flask_paginate import Pagination

from opencve.models.products import Product
from opencve.models.vendors import Vendor


def get_products(vendor, args):
    vendor = Vendor.query.filter_by(name=vendor).first()
    if not vendor:
        abort(404)

    q = Product.query.filter_by(vendor=vendor)

    # Search by term
    if args.get("search"):
        search = args.get("search").lower().replace("%", "").replace("_", "")
        q = q.filter(Product.name.like("%{}%".format(search)))

    page = args.get("page", type=int, default=1)
    objects = q.order_by(Product.name.asc()).paginate(
        page, app.config["PRODUCTS_PER_PAGE"], True
    )
    pagination = Pagination(
        page=page,
        total=objects.total,
        per_page=app.config["PRODUCTS_PER_PAGE"],
        record_name="products",
        css_framework="bootstrap3",
    )

    return objects, vendor, pagination
