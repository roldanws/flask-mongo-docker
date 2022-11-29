from flask import blueprint, jsonify, request
from flask_restplus import Api, Resource, fields 

bp_api = Bluepirnt('Api',__name__, url_prefix="/Api")

api =  Api(bp_api, version="1.0", tittle="Api", descripcion="End Points")

