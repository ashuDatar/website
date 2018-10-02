from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
#from flask_migrate import Migrate
from flask_babel import Babel, lazy_gettext as _l
import json
import pandas as pd
import numpy as np
import os, base64, re, logging

AppServer = Flask(__name__)

AppServer.config.from_object(Config)
db = SQLAlchemy(AppServer)
babel = Babel()
babel.init_app(AppServer)


#migrate = Migrate(AppServer, db)

from app import routes

