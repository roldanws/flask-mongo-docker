from flask import Blueprint, jsonify, request
from flask_restplus import Api, Resource, fields 

bp_api = Blueprint('Api',__name__, url_prefix="/Api")

api =  Api(bp_api, version="1.0", tittle="Api", descripcion="End Points")

