from app.server import AppServer
from app.Dashserver import DashServer
from flask import render_template, flash, redirect, url_for, request, g , current_app
#from app import server
from flask import g
from flask_babel import _, get_locale
#from app.models import search_index
#from app.forms import SearchForm, resultForm
#from app.search import add_to_index
from app.MyDashApps import dashapp0
from app.MyDashApps import dashapp1
from dash.dependencies import Input, State, Output
import dash_html_components as html
import dash
import dash_core_components as dcc



@AppServer.route('/', methods=['GET', 'POST'])
@AppServer.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index_1.html', title='Home')
    #return redirect('/app/MyDashApps') 	
