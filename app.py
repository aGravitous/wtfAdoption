from flask import Flask, request, flash, redirect, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Optional, Email
from flask_debugtoolbar import DebugToolbarExtension
from models import Pet, db, connect_db
from forms import AddPet, EditPet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route('/')
def home_page():
    ''' Display home page and pets to client. '''

    pets = Pet.query.all()

    return render_template('/index.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Pet add form; handle adding"""
    form = AddPet()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(name=name,
                      species=species,
                      photo_url=photo_url,
                      age=age,
                      notes=notes)

        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('/add_form.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_and_edit(pet_id):
    ''' Shows pet details and detail edit form '''

    pet = Pet.query.get(pet_id)
    form = EditPet()
    if form.validate_on_submit():
        photo_url = form.photo_url.data
        notes = form.notes.data
        is_available = form.is_available.data

        pet.photo_url = photo_url
        pet.notes = notes
        pet.available = is_available

        db.session.commit()
        return redirect(f'/{pet.id}')
    else:
        return render_template('pet_profile.html', pet=pet, form=form)

    
