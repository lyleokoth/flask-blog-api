from app import app
from app import db

@app.route('/', methods=['GET'])
def index():
    return 'Hello from our flask api'