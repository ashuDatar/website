from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
#from flask_migrate import Migrate
from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
from elasticsearch import Elasticsearch
from flask_babel import Babel, lazy_gettext as _l
import json
import plotly
import pandas as pd
import numpy as np


AppServer = Flask(__name__)

AppServer.config.from_object(Config)
db = SQLAlchemy(AppServer)
babel = Babel()
babel.init_app(AppServer)
db.init_app(AppServer)
AppServer.elasticsearch = Elasticsearch([AppServer.config['ELASTICSEARCH_URL']]) \
       if AppServer.config['ELASTICSEARCH_URL'] else None
#migrate = Migrate(AppServer, db)

from app import routes, models

#@AppServer.route('/', methods=['GET', 'POST'])
#@AppServer.route('/index', methods=['GET', 'POST'])
#def index():
    #return render_template('visualization.html')
