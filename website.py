#from werkzeug.wsgi import DispatcherMiddleware
#from werkzeug.serving import run_simple
#from app.server import AppServer
from app import AppServer
#from app.webroutes import webServer
from app.Dashserver import DashServer
#import os
#from app.models import test_data_dummy_data, search_index



#@server.shell_context_processor
#def make_shell_context():
 #   return {'db': db, 'test_data_dummy_data': test_data_dummy_data, 'search_index': search_index}

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#myApp = DispatcherMiddleware(AppServer,{'/app': webServer})

if __name__ == '__main__':
   AppServer.run(debug=True, use_reloader=True)
   #port = int(os.environ.get('PORT', 5000))
   #AppServer.run(host='0.0.0.0', port=port, debug=True)
  

