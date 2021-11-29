"""Flask app for Cupcakes"""
from flask import Flask, request, render_template,  redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Cupcake
# from forms import AddSnackForm, EmployeeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "cupcakesaresweet"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def all_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request."""
    data = request.json
    new_cupcake = Cupcake(flavor=data['flavor'], 
                            size=data['size'], 
                            rating=data['rating'], 
                            image=data['image'] or None)
    
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())

    return(response_json, 201)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request."""
    data = request.json
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image'] or None
    
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}."""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = "deleted")





