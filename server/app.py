# server/app.py
#!/usr/bin/env python3

from flask import Flask,jsonify, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def main(id):
    earthquake=Earthquake.query.get(id)
    if earthquake is None:
        response_body= {"message":f'Earthquake {id} not found.'}
        status=404
    else:
     response_body= {'id':earthquake.id,
                      'location':earthquake.location,
                      'magnitude':earthquake.magnitude,
                      'year':earthquake.year
                    }
     status=200
    return make_response(jsonify(response_body),status)
    
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
