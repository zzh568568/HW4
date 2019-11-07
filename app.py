from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class zzhang178_moviesapp(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    director = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | movie name: {1} | genre: {2} | director: {3}".format(self.movieId, self.movie_name, self.genre, self.director)

class MoviesForm(FlaskForm):
    movie_name = StringField('Movie Name:', validators=[DataRequired()])
    genre = StringField('Genre:', validators=[DataRequired()])
    director = StringField('Director:', validators=[DataRequired()])

@app.route('/')
def index():
    all_movies = zzhang178_moviesapp.query.all()
    return render_template('index.html', movies=all_movies, pageTitle='New Movies')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MoviesForm()
    if form.validate_on_submit():
        movie = zzhang178_moviesapp(movie_name=form.movie_name.data, genre=form.genre.data, director=form.director.data)
        db.session.add(movie)
        db.session.commit()
        #return "<h2> The movie is {0}". format(form.movie_name.data)
        return redirect('/')

    return render_template('add_movie.html', form=form, pageTitle='Add A New Movie')

if __name__ == '__main__':
    app.run(debug=True)
