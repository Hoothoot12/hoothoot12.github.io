from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField , IntegerField ,SelectField , TimeField
from wtforms.validators import DataRequired , URL
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditor, CKEditorField
from werkzeug.utils import secure_filename
import os
import random
import fontawesomefree

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

#-----Database-----
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#-----DB create table-----
class Cafe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)


#-----Force To load-----
def create_app():
    with app.app_context():
        return db.create_all()
create_app()

#-----Form-----
class CafesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = StringField('Map', validators=[DataRequired(),URL()])
    img_url = StringField('Image', validators=[DataRequired(),URL()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = SelectField('Socket',choices=[(0), (1)], validators=[DataRequired()])
    has_toilet = SelectField('Toilet', choices=[(0), (1)], validators=[DataRequired()])
    has_wifi = SelectField('Wifi', choices=[(0), (1)], validators=[DataRequired()])
    can_take_calls = SelectField('Can take calls', choices=[(0),(1)], validators=[DataRequired()])
    seats = SelectField('Seats', choices=[('0-10'), ('10-20'), ('20-30'), ('30-40'), ('40-50'), ('50+')], validators=[DataRequired()])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    description = CKEditorField("Tell us about the cafe", validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])

#-----Some variables------
post = ''

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', shop=post)

@app.route('/surpise')
def surpise():
    global post
    all_cafe = Cafe.query.all()
    post = random.choice(all_cafe)
    return redirect(url_for('home'))

@app.route('/places', methods=['GET', 'POST'])
def place():
    all_cafes = Cafe.query.all()
    return render_template('places.html', cafes=all_cafes, number=len(all_cafes),post_id='')

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = CafesForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name= form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            has_sockets = form.has_sockets.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            can_take_calls = form.can_take_calls.data,
            seats = form.seats.data,
            coffee_price = form.coffee_price.data,
            description = form.description.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('add.html',form=form)

@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    edit_post = Cafe.query.get(post_id)
    form = CafesForm(
        name=edit_post.name,
        map_url=edit_post.map_url,
        img_url=edit_post.img_url,
        location=edit_post.location,
        has_sockets=edit_post.has_sockets,
        has_toilet=edit_post.has_toilet,
        has_wifi=edit_post.has_wifi,
        can_take_calls=edit_post.can_take_calls,
        seats=edit_post.seats,
        coffee_price=edit_post.coffee_price,
        description=edit_post.description
    )
    if request.method == 'POST':
        edit_post.name = form.name.data
        edit_post.map_url = form.map_url.data
        edit_post.img_url = form.img_url.data
        edit_post.location = form.location.data
        edit_post.has_sockets = form.has_sockets.data
        edit_post.has_toilet = form.has_toilet.data
        edit_post.has_wifi = form.has_wifi.data
        edit_post.can_take_calls = form.can_take_calls.data
        edit_post.seats = form.seats.data
        edit_post.coffee_price = form.coffee_price.data
        edit_post.description = form.description.data

        db.session.commit()
        return redirect(url_for('place'))
    return render_template('add.html',form=form)

@app.route('/delete/<post_id>')
def delete(post_id):
    cafe_to_delete = Cafe.query.get(post_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('place'))

@app.route('/coffees', methods=['GET', 'POST'])
def coffee():
    return render_template('coffee.html')

if __name__ == "__main__":
    app.run(debug=True)