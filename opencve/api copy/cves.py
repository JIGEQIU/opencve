from flask import jsonify, request


from opencve.api._bp import api
from opencve.controllers.cves import get_cves, get_cve

CVE_FIELDS = [
    "id",
    "created_at",
    "updated_at",
    "cve_id",
    "summary",
    "cvss2",
    "cvss3",
]


@api.route("/cve")
def cves():
    objects, _, _, _ = get_cves(request.args)
    data = [o.to_dict(CVE_FIELDS) for o in objects.items]
    return jsonify(data)


@api.route("/cve/<cve_id>")
def cve(cve_id):
    cve, vendors, cwes = get_cve(cve_id)
    data = cve.to_dict(CVE_FIELDS)
    data.update({"vendors": vendors, "cwes": cwes})
    return jsonify(data)
