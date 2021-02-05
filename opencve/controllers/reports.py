from flask import current_app as app
from flask import abort, request, url_for
from flask_paginate import Pagination
from flask_user import current_user
from sqlalchemy.orm import joinedload

from opencve.extensions import db
from opencve.models.alerts import Alert
from opencve.models.reports import Report


def get_reports():
    q = Report.query.filter_by(user=current_user).order_by(Report.created_at.desc())

    page = request.args.get("page", type=int, default=1)
    reports = q.paginate(page, app.config["REPORTS_PER_PAGE"], True)
    pagination = Pagination(
        page=page,
        total=reports.total,
        per_page=app.config["REPORTS_PER_PAGE"],
        record_name="reports",
        css_framework="bootstrap3",
    )
    return reports, pagination


def get_report(link):
    report = Report.query.filter_by(public_link=link).first()
    if not report:
        abort(404)

    # The report is now seen
    report.seen = True
    db.session.commit()

    alerts = Alert.query.options(joinedload("cve")).filter_by(report_id=report.id).all()
    return report, alerts
