from flask import Flask, render_template, redirect, url_for, request, json, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superSecretKey'
# uncomment below for local use.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users/thomasg/PycharmProjects/neuroFlowAssessment/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/database.db'

Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    # moods = db.relationship('MoodRating', backref='person')


class MoodRating(db.Model):
    __tablename__ = 'MoodRating'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.id'))
    createdOn = db.Column(db.DateTime, default=datetime.now)
    mood = db.Column(db.String(50))

    def serialize(self):
        return {
            'moodRating': self.mood,
            'createdOn': self.createdOn
        }


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    login_valid = 'user' in session  # or whatever you use to check valid login

    if not current_user.is_authenticated and not login_valid:
        return json.jsonify(success=False, msg="You are not logged in. Please use the /login api to login first")


# @app.before_request
# def check_valid_login():
#     pass

@app.route('/')
def index():
    return json.jsonify(msg='endpoint for mood rating is /mood')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') and data.get('password'):
        user = User.query.filter_by(username=data.get('username')).first()
        if user:
            if check_password_hash(user.password, data.get('password')):
                login_user(user)
                return json.jsonify(success=True, msg='logged in user', userID=user.id)
        return json.jsonify(success=False, msg='Invalid username/password')
    return json.jsonify(success=False, msg='Missing Username/Password')


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if email and password and username:
        # check if user or email is already taken
        userWithEmail = User.query.filter_by(email=email).first()
        userWithUsername = User.query.filter_by(username=username).first()
        if userWithEmail or userWithUsername:
            return json.jsonify(success=False, msg='Sorry, that username/email is already taken.')
        hashed_pass = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_pass, email=email)
        db.session.add(new_user)
        db.session.commit()
        return json.jsonify(success=True, msg='New user has been created')

    return json.jsonify(success=False, msg='Not enough info for new account. Pls provide email, username, and password')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return json.jsonify(success=True, msg="Successfully logged out user")


def get_streak(ratings):
    streak = 0
    s = set()
    listOfTimes = []
    # get the dates of all times when user posted a mood rating
    for i in ratings:
        dateExtracted = i.createdOn.date()
        s.add(dateExtracted)
        listOfTimes.append(dateExtracted)

    # keep a counter of how many executive days of the dates and
    # if there separate consecutive days then choose the longest one.
    for i in range(len(listOfTimes)):
        if (listOfTimes[i] - timedelta(days=1)) not in s:
            j = listOfTimes[i]
            while (j in s):
                j = j + timedelta(days=1)
            streak = max(streak, (j - listOfTimes[i]).days)
    return streak


@app.route('/mood', methods=['GET', 'POST'])
@login_required
def mood():
    if request.method == 'POST':
        mood = request.json.get('mood')  # Your form's
        if mood:
            rating = MoodRating(mood=mood, userID=current_user.id)
            db.session.add(rating)
            db.session.commit()
            return json.jsonify(success=True, msg=f'added a new rating {mood} for user with id: {current_user.id}')
    else:
        users = db.session.query(User).all()
        userStreaks = {}
        currentUserRatings = []
        currentUserStreak = 0
        for user in users:
            ratings = db.session.query(MoodRating).filter(MoodRating.userID == user.id).order_by(
                MoodRating.createdOn).all()
            streakLength = get_streak(ratings)
            userStreaks[user.id] = streakLength
            if current_user.id == user.id:
                currentUserRatings = ratings
                currentUserStreak = streakLength

        # calculate the percentile
        # grab number of users, see how many users have streak less than current user's streak.
        numUsersWithLessStreak = len([v for v in userStreaks.values() if int(v) <= currentUserStreak])

        percentile = numUsersWithLessStreak / len(users) * 100
        if percentile >= 50:
            return json.jsonify(ratings=[e.serialize() for e in currentUserRatings], streak=currentUserStreak,
                                percentile=percentile)
        return json.jsonify(ratings=[e.serialize() for e in currentUserRatings], streak=currentUserStreak)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
