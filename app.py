from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
#import secrets
import os

dbUser = os.environ.get('DBUSER')
dbPass = os.environ.get('DBPASS')
dbHost = os.environ.get('DBHOST')
dbName = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbUser, dbPass, dbHost, dbName)


app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class zzhang178_moviesapp(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    director = db.Column(db.String(255))
    running_time = db.Column(db.Integer)

    def __repr__(self):
        return "id: {0} | movie name: {1} | genre: {2} | director: {3} | running_time: {4}".format(self.movieId, self.movie_name, self.genre, self.director, self.running_time)

class MoviesForm(FlaskForm):
    movie_name = StringField('Movie Name:', validators=[DataRequired()])
    genre = StringField('Genre:', validators=[DataRequired()])
    director = StringField('Director:', validators=[DataRequired()])
    running_time = IntegerField('Running Time:', validators=[DataRequired()])

@app.route('/')
def index():
    all_movies = zzhang178_moviesapp.query.all()
    return render_template('index.html', movies=all_movies, pageTitle='New Movies')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = zzhang178_moviesapp.query.filter(or_(zzhang178_moviesapp.movie_name.like(search),
                                                        zzhang178_moviesapp.director.like(search))).all()
        return render_template('index.html', movies=results, pageTitle='New Movies', legend="Search Results")
    else:
        return redirect('/')

@app.route('/movie/new', methods=['GET', 'POST'])
def add_movie():
    form = MoviesForm()
    if form.validate_on_submit():
        movie = zzhang178_moviesapp(movie_name=form.movie_name.data, genre=form.genre.data, director=form.director.data, running_time=form.running_time.data)
        db.session.add(movie)
        db.session.commit()
        return redirect('/')

    return render_template('add_movie.html', form=form, pageTitle='Add A New Movie', legend="Add A New Friend")

@app.route('/movies/<int:movie_id>', methods=['GET','POST'])
def movie(movie_id):
    movies = zzhang178_moviesapp.query.get_or_404(movie_id)
    return render_template('movie.html', form=movies, pageTitle='Movie Details')

@app.route('/movies/<int:movie_id>/update', methods=['GET','POST'])
def update_movie(movie_id):
    movie = zzhang178_moviesapp.query.get_or_404(movie_id)
    form = MoviesForm()
    if form.validate_on_submit():
        movie.movie_name = form.movie_name.data
        movie.genre = form.genre.data
        movie.director = form.director.data
        movie.running_time = form.running_time.data
        db.session.commit()
        flash('The movie has been updated.')
        return redirect(url_for('movie', movie_id=movie.movieId))
    elif request.method == 'GET':
        form.movie_name.data = movie.movie_name
        form.genre.data = movie.genre
        form.director.data = movie.director
        form.running_time = movie.running_time

    return render_template('add_movie.html', form=form, pageTitle='Update Post', legend="Update A Movie")

@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        movie = zzhang178_moviesapp.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        flash('Movie was successfully deleted!')
        return redirect("/")

    else: #if it's a GET request, send them to the home page
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
