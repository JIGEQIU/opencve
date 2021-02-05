from flask import jsonify, request

from opencve.api import auth_required
from opencve.api._bp import api
from opencve.api.alerts import _alert_to_dict
from opencve.models.cve import Cve
from opencve.controllers.reports import get_reports, get_report


def _report_to_dict(report):
    data = report.to_dict(["created_at", "public_link"])

    # Change the public_link name
    data["id"] = data["public_link"]
    del data["public_link"]

    # Add the associated vendors and products
    data.update({"handlers": report.details})

    return data


@api.route("/reports")
@auth_required
def reports():
    reports, _ = get_reports()
    return jsonify([_report_to_dict(r) for r in reports.items])


@api.route("/reports/<link>")
def report(link):
    report, alerts = get_report(link)

    # Construct the response
    data = _report_to_dict(report)
    data.update({"alerts": [_alert_to_dict(a) for a in alerts]})

    return jsonify(data)
