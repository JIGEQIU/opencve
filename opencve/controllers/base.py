from flask import current_app as app
from flask_paginate import Pagination


class BaseController(object):
    model = None
    order = None
    per_page_param = None
    schema = {}

    @classmethod
    def build_query(cls, args):
        raise NotImplementedError

    @classmethod
    def parse_args(cls, args):
        parsed_args = {"page": args.get("page", type=int, default=1)}

        for key in args.keys():
            if key in cls.schema.keys():
                parsed_args[key] = args.get(
                    key,
                    type=cls.schema.get(key).get("type"),
                    default=cls.schema.get(key).get("default"),
                )
        return parsed_args

    @classmethod
    def get(cls, filters):
        return cls.model.query.filter_by(**filters).first()

    @classmethod
    def list(cls, args):
        args = cls.parse_args(args)
        query, metas = cls.build_query(args)

        objects = query.order_by(cls.order).paginate(
            args.get("page"), app.config[cls.per_page_param], False
        )

        pagination = Pagination(
            page=args.get("page"),
            total=objects.total,
            per_page=app.config[cls.per_page_param],
            record_name="objects",
            css_framework="bootstrap3",
        )

        return objects.items, metas, pagination

    @classmethod
    def list_items(cls, args):
        items, _, _ = cls.list(args)
        return items
