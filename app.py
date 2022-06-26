from dis import dis
from operator import truediv
import backend 
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="../webscraper-react-flask/build")
CORS(app)

@app.route("/api/scrape", methods=["POST","GET"], strict_slashes=False)
@cross_origin()
def add_data():
    #getting the data as POST 
    title = request.json['title']
    location = request.json['location']
    pages = request.json['pages']
    country = request.json['country']
    distance = request.json['distance']
    date = request.json['date']

    #processing data
    dataObject = backend.Backend(title, location, pages,country, distance, date)
    data = dataObject.scrape()
    #print(data)
    return jsonify(results = data)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)