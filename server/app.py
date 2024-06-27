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
def get_earthquake_by_id(id):
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

@app.route('/earthquakes/magnitude/<float:min_magnitude>',methods=['GET'])    
def query_magnitudes(min_magnitude):
    earthquake=Earthquake.query.filter(Earthquake.magnitude>=min_magnitude).all()
  
    e_quake_list=[
         {
            "id":e_quake.id,
            "location":e_quake.location,
            "magnitude":e_quake.magnitude,
            "year":e_quake.year
         }
      for e_quake in earthquake]
    response_body={
         "count":len(e_quake_list),
         "quakes":e_quake_list
      }
    status=200
    return make_response(jsonify(response_body),status)
   
  

if __name__ == '__main__':
    app.run(port=5555, debug=True)
