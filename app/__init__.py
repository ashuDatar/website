from flask_migrate import Migrate
from app.server import AppServer
from app.server import db

migrate = Migrate(AppServer, db)
