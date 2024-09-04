from flask import Flask, render_template

app = Flask(__name__)
app.static_folder = 'static'
@app.route('/')
def maps():
    # Example data for demonstration purposes
    name = "Aman"
    latitude = 28.547236 
    longitude = 77.272905

    # Packing data into a dictionary to pass to the template
    map_instance = {
        "name": name,
        "latitude": latitude,
        "longitude": longitude
    }

    # Render the maps.html template, passing the map_instance dictionary
    return render_template('maps.html', details=map_instance)

if __name__ == '__main__':
    app.run(debug=True)
