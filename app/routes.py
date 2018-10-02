from app.server import AppServer
from flask import render_template, flash, redirect, url_for, request, g , current_app
#from app import server
from flask import g
from flask_babel import _, get_locale





@AppServer.route('/', methods=['GET', 'POST'])
@AppServer.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index_1.html', title='Home')
    #return redirect('/app/MyDashApps') 	
