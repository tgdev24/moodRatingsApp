PROJECT SETUP

1. copy project
git clone

2. go to directory where project is installed

3. go to terminal window and type
docker compose up

3b. if you need to build image again, type:
docker-compose up -d --no-deps --build helloworld

HOW TO USE:

1. sign up a user using:
url:  http://0.0.0.0:5000/signup
method: POST
request body(EXAMPLE):
{
    "email": "test4@youtube.com",
    "username": "test_dude_4",
    "password": "test_dude_4"
}

2. login a user using:
url:  http://0.0.0.0:5000/login
method: POST
request body(EXAMPLE):
{
    "username": "test_dude_4",
    "password": "test_dude_4"
}

3. see current mood ratings, percentile, and streak for user.
url:  http://0.0.0.0:5000/mood
method: GET

4. add new mood rating
url: http://0.0.0.0:5000/mood
method: POST
request body(EXAMPLE):
{
    "mood": "cool"
}

5. log out user using:
url:  http://0.0.0.0:5000/logout
method: POST


IMPLEMENTATION
percentile on api return includes if other users have same streak as the current user.


IMPROVEMENTS
Q: Document what, if anything, you would do differently if this were a production application and
not an assessment? What tech would you use? How would you handle things differently if it
needed to handle more users, more data, etc?

A: for a production application, I would be more concerned with security(eg. not storing the passwords even hashed
on a database), as well as more error handling to ensure the app is more stable and robust. Also, I would plan out the
database tables so they don't have too much duplicate data and more foreign keys as the data grows. Also, I would try to
make the API fast and efficient as possible with the implementation of the code, possibly storing the streak for users on
the DB instead of calculating at execution so that we can just return it. Also, I would use a better database engine unlike
sqlite that was used here, something like postgresDB.


