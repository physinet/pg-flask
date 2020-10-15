import json
import os
from flask import Flask, jsonify, render_template, request, redirect
from sqlalchemy import func

import altair as alt

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



    chart_data = alt.Data(values=[{'name':'Pita', 'votes':votes.get('Pita', 0)},
                  {'name': 'Gummi', 'votes': votes.get('Gummi', 0)}])


    chart = (alt.Chart(chart_data)
                .properties(width=150,
                            height=150)
                .mark_bar()
                .encode(alt.X('name', type='nominal'),
                        alt.Y('votes', type='quantitative')))


    chart.save('tmp/chart.json')
    payload = {
        'gummi_votes': votes.get('Gummi', 0),
        'pita_votes': votes.get('Pita', 0),
        'chart':chart.to_json()}
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
