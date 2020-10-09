import os
from flask import Flask, jsonify, render_template, request, redirect
from sqlalchemy import func

import commands
import database
from model import Model


# init flask app instance
app = Flask(__name__)

# setup with the configuration provided by the user / environment
app.config.from_object(os.environ['APP_SETTINGS'])

database.init_app(app)
commands.init_app(app)


@app.route("/")
def main_page():
    votes = dict(Model
                 .query
                 .with_entities(Model.vote, func.count(Model.vote))
                 .group_by(Model.vote)
                 .all())

    payload = {
        'gummi_votes': votes['Gummi'],
        'pita_votes': votes['Pita']}

    return render_template('index.html', **payload)


@app.route("/add", methods=['GET', 'POST'])
def add_new_item():

    # request.args is a dict of key/value pairs from the webform
    vote = request.args['voteSubmit']
    new_row = Model(vote=vote)

    # add to the database session
    database.db.session.add(new_row)

    # commit to persist into the database
    database.db.session.commit()

    return redirect('/')
