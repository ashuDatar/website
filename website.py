from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from app.server import AppServer
from app.webroutes import webServer
import sys,os
#from app.models import test_data_dummy_data, search_index



#@server.shell_context_processor
#def make_shell_context():
 #   return {'db': db, 'test_data_dummy_data': test_data_dummy_data, 'search_index': search_index}

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

myApp = DispatcherMiddleware(AppServer,{'/app': webServer})

if __name__ == '__main__':
   myApp.run_server(debug=True)
   #run_simple('127.0.0.1', 5000, myApp, use_reloader=True, use_debugger=True)
  

