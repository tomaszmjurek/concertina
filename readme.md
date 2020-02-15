# Concertina
Flask app with postgres database for storing information about concerts and bands

## How to run
To run the app the following steps are necessary:

* Set env variable `FLASK_APP` to concertina/app.py
* Create PostgreSQL database (default name is *concertina* - in case of any different make sure to check `configs.py` file)
* Once the previous steps are done, tables in our database may be created - simply use the following commands:
    * `flask db init`
    * `flask db upgrade`
    * `flask db migrate`
* Use `flask run` to run the app

## How it looks
<img src=https://github.com/tomaszmjurek/readme-images/blob/master/concertina.png>


## Built With
* Python 3.7
* PostgreSQL
* Flask
* HTML
* CSS

## Authors
* **Aleksy Królczyk** - [aleksykrolczyk](https://github.com/aleksykrolczyk)
* **Tomasz Jurek** - [tomaszmjurek](https://github.com/tomaszmjurek)
