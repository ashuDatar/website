from app.server import AppServer
from app.Dashserver import DashServer
from flask import render_template, flash, redirect, url_for, request, g , current_app
#from app import server
from flask import g
from flask_babel import _, get_locale
from app.models import test_data_dummy_data, search_index
from app.forms import SearchForm, resultForm
from app.search import add_to_index
from app.MyDashApps import dashapp0
from app import dashapp1
from dash.dependencies import Input, State, Output
import dash_html_components as html
import dash
import dash_core_components as dcc

@AppServer.before_request
def before_request():
    g.search_form = SearchForm()
    g.filter = 'None'
    #g.locale = str(get_locale())

@AppServer.route('/', methods=['GET', 'POST'])
@AppServer.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    g.search_form = SearchForm()
    if form.validate_on_submit():
        ...
        return redirect('/result')
    return render_template('search.html', title='Search', form=form)
    #return redirect('/app/MyDashApps') 	

@AppServer.route('/login', methods = ['POST', 'GET'])
def login():
    return render_template('index_1.html', title='Home')

@AppServer.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    return render_template('search.html', title='Search', form=form)

@AppServer.route('/result', methods=['GET', 'POST'])
def result():
    form = resultForm()
    page = request.args.get('page', 1, type=int)
   # lists, total = test_data_dummy_data.search(g.search_form.q.data, page,20)
    lists, total = search_index.search(g.search_form.q.data, page,20)
    next_url = url_for('result', q=g.search_form.q.data, page=page + 1) \
        if total > page * 20 else None
    prev_url = url_for('result', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    if form.validate_on_submit():
        #...
        return redirect('/visualization/<description>')    
    return render_template('result.html', title=_('results'), lists=lists,
                           next_url=next_url, prev_url=prev_url, form=form)
    
    
@AppServer.route('/visualization/<description>', methods=['GET', 'POST'])
def visualization(description):
    path = '/app/MyDashApps/' + description
    #return redirect(url_for('/app/MyDashApps', description=description))
    return redirect(path) 	



DashServer.layout = html.Div([	dcc.Location(id='url', refresh=False),	dcc.Input(id='description', type='text'),			      
                                html.Div(id='signal', style={'display': 'none'}),
			              html.Div(id='page-content')])


@DashServer.callback(Output('signal', 'children'), [Input('url', 'search')])
def compute_value(search):
    # compute value and send a signal when done
    des = str(search) 
    filter = des.split('/')[-1]
    #global_store(value)
    #filter = 'hello world'
    return filter


@DashServer.callback(Output('page-content', 'children'),[Input('url', 'pathname'),Input('signal', 'filter')])
def display_page(pathname, filter):
    pathname = str(pathname) 	
    if pathname.startswith('/app/'):
       #filter = pathname.split('/')[-1]
       #filter = compute_value()
       return dashapp1.layout
    elif pathname == '/app/MyDashApps/dashapp1':
         return dashapp1.layout
    #elif pathname == '/app/MyDashApps/dashapp0':
         #return dashapp0.layout
    else:
        return '404'	
	   	
        
   
