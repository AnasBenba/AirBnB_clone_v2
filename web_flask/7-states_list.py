#!/usr/bin/python3
""" Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def storage(self):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def is_state():
    data = storage.all(State).values()
    return render_template('7-states_list.html', data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
