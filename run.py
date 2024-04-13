import sys
sys.path.append('./dashboard')
from dashboard.app import app


app.run_server(debug=True)