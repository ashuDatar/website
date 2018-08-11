import dash
#import os,sys
from app.server import AppServer

DashServer = dash.Dash(
	name='analysis', 
	sharing=True,
    server = AppServer,
	static_folder='static', 
	url_base_pathname='/app/')


DashServer.scripts.config.serve_locally=True
DashServer.css.config.serve_locally=True
DashServer.server.secret_key = os.environ.get('secret_key','secret')
DashServer.config['suppress_callback_exceptions']=True
