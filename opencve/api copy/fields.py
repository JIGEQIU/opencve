from flask_restful import fields

from opencve.context import _humanize_filter


class HumanizedNameField(fields.Raw):
    """
    Returns a humanized name.
    """

    def format(self, value):
        return _humanize_filter(value)
