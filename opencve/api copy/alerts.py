from flask import abort, jsonify

from opencve.api._bp import api
from opencve.controllers.reports import get_report
from opencve.models import is_valid_uuid
from opencve.models.alerts import Alert


def _alert_to_dict(alert):
    data = alert.to_dict(["id", "created_at"])

    # Handle the CVE
    data.update(
        {
            "cve": alert.cve.cve_id,
            "handlers": {
                "vendors": alert.details["vendors"],
                "products": alert.details["products"],
            },
        }
    )

    return data


@api.route("/reports/<link>/alerts")
def alerts(link):
    _, alerts = get_report(link)
    return jsonify([_alert_to_dict(a) for a in alerts])


@api.route("/reports/<link>/alerts/<id>")
def alert(link, id):
    if not is_valid_uuid(id):
        abort(404)

    # Get the wanted alert
    report, _ = get_report(link)
    alert = Alert.query.filter_by(id=id, report_id=report.id).first()
    if not alert:
        abort(404)

    # Get the associated events
    data = []
    for event in alert.events:
        data.append(
            {
                "message": event.type.value,
                "type": event.type.code,
                "details": event.details,
            }
        )

    return jsonify(data)
