from flask import jsonify, request


from opencve.api._bp import api
from opencve.controllers.cwes import get_cwes


@api.route("/cwe")
def cwes():
    objects, _ = get_cwes(request.args)
    return jsonify(
        [o.to_dict(["cwe_id", "name", "description"]) for o in objects.items]
    )
