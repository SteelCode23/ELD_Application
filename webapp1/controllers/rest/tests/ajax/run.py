# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~
    A simple application that shows how Flask and jQuery get along.0561
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("Hello World")
    return jsonify(result=a + b +1)

@app.route('/DRIVING')
def driving():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("Driving")
    return jsonify(result=a + b)

@app.route('/ONDUTY')
def onduty():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("on duty")
    return jsonify(result=a + b)

@app.route('/SLEEPING')
def sleeping():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("Sleep")
    return jsonify(result=a + b)


@app.route('/OFFDUTY')
def offduty():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print("off duty")
    return jsonify(result=a + b)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port = 5144)