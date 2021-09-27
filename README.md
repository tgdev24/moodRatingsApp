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

