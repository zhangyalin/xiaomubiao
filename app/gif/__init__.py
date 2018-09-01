#-*- coding: UTF-8 -*-    
from flask import Blueprint

gif = Blueprint('gif', __name__)

from . import webdb
