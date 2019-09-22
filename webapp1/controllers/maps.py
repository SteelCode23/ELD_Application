from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from webapp1.models import truck, db, User, company, Device, drivers
import math
from flask import request
import argparse


map_blueprint = Blueprint(
    'maps',
    __name__,
    template_folder='../templates/maps',
    url_prefix="/maps"
    )

@login_required
@map_blueprint.route('/viewmaps')
def showmap():
    _truck_to_show_ = request.args.get('uid')
    _truck_to_show_ = 1
    _truck_ = truck.query.filter_by(uid=_truck_to_show_).all()


    return render_template('maps.html', truck = _truck_[0])



@login_required
@map_blueprint.route('/mobile_map')
def mobile_map():
    return render_template('mobile_map.html')


@ login_required
@map_blueprint.route('/routetrucks')
def routetrucks():
    distance = math.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)
    return render_template('maps.html')


@map_blueprint.route('/maptest')
def showmaptest():
    return render_template('iframetest.html')


@map_blueprint.route('/view_drivers')
def view_drivers():
    return render_template('_test_leaflet_.html')

@map_blueprint.route('/mapindex')
def showmaptestindex():
    return render_template('maptest.html')