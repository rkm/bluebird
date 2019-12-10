"""
Contains logic for flask and our app routes
"""

from http import HTTPStatus
import logging

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api

from bluebird.settings import Settings
from bluebird.api import resources as res


class BlueBirdApi(Api):
    """
    Subclass of the Flask API object - allows us to customise it later if needed
    """

    def __init__(self, *args, **kwargs):
        super(BlueBirdApi, self).__init__(*args, **kwargs)


# Create the Flask app & API, with the given prefix
FLASK_APP = Flask(__name__)
CORS(FLASK_APP)
FLASK_API = BlueBirdApi(FLASK_APP, prefix="/api/v" + str(Settings.API_VERSION))

# Add hooks to log request response data

LOGGER = logging.getLogger(__name__)


@FLASK_APP.before_request
def before_req():
    """
    Method called before every request is handled
    :return:
    """

    json = request.get_json()

    if "loadlog" in request.url.lower():
        json = "<LOADLOG data>"

    LOGGER.info(f'REQ {request.method} {request.full_path} "{json if json else ""}"')


# TODO(RKM 2019-11-18) We could modify the standard Flask "missing argument" response
# here so that users can more clearly see the mistake
@FLASK_APP.after_request
def after_req(response):
    """
    Method called before any response is returned
    :param response:
    :return:
    """

    data = response.get_json()
    if not data:
        data = response.data.decode()

    if "eplog" in request.url.lower() and response.status_code == HTTPStatus.OK:
        data = "<EPLOG data>"

    if isinstance(data, str):
        data = data.replace("\n", "")
    LOGGER.info(f'RESP {response.status_code} "{data}"')

    return response


# NOTE(RKM 2019-11-26) This is where we introduce the API endpoints to the Flask app

# Aircraft control
FLASK_API.add_resource(res.AddWpt, "/addwpt")
FLASK_API.add_resource(res.Alt, "/alt")
FLASK_API.add_resource(res.Cre, "/cre")
FLASK_API.add_resource(res.Direct, "/direct")
FLASK_API.add_resource(res.Hdg, "/hdg")
FLASK_API.add_resource(res.ListRoute, "/listroute")
FLASK_API.add_resource(res.Pos, "/pos")
FLASK_API.add_resource(res.Spd, "/spd")
FLASK_API.add_resource(res.Vs, "/vs")

# Simulation control
FLASK_API.add_resource(res.DefWpt, "/defwpt")
FLASK_API.add_resource(res.DtMult, "/dtmult")
FLASK_API.add_resource(res.Hold, "/hold")
FLASK_API.add_resource(res.Ic, "/ic")
FLASK_API.add_resource(res.LoadLog, "/loadlog")
FLASK_API.add_resource(res.Op, "/op")
FLASK_API.add_resource(res.Reset, "/reset")
FLASK_API.add_resource(res.Sectors, "/sectors")
FLASK_API.add_resource(res.Seed, "/seed")
FLASK_API.add_resource(res.Step, "/step")
FLASK_API.add_resource(res.Time, "/time")
FLASK_API.add_resource(res.UploadScenario, "/uploadScenario")
FLASK_API.add_resource(res.UploadSector, "/uploadSector")

# Application control
# FLASK_API.add_resource(res.EpInfo, '/epinfo')
FLASK_API.add_resource(res.EpLog, "/eplog")
FLASK_API.add_resource(res.SimInfo, "/siminfo")
# FLASK_API.add_resource(res.SimMode, "/simmode")
FLASK_API.add_resource(res.Shutdown, "/shutdown")

# Metrics
FLASK_API.add_resource(res.Metric, "/metric")
FLASK_API.add_resource(res.MetricProviders, "/metricproviders")
