import os

from dateutil.parser import parse
from flask import jsonify, url_for, send_from_directory
from flask import request
from flask_login import LoginManager, login_user
import csv
from statistics import mean

from werkzeug.utils import redirect

from .models import Material, User, db

login_manager = LoginManager()


def get_materials():
    materials = Material.query.all()
    data = [item.serialized for item in materials]
    return jsonify(data)


def get_material(material_id):
    material = Material.query.get(material_id)
    if material:
        return jsonify(material.serialized)
    else:
        return jsonify("Not found"), 404


def add_material():
    data = request.get_json()
    new_items = []
    for item in data:
        material = Material.query.filter(Material.excel_id == item['$id'])
        excel_id = item.pop('$id')
        date_added = parse(item.pop('date_added'))
        if not material.first():
            new_material = Material(**item)
            new_material.excel_id = excel_id
            new_material.date_added = date_added
            new_items.append(new_material)
            db.session.add(new_material)
            db.session.commit()
        else:
            material.update(item)
            db.session.commit()
    return jsonify([item.serialized for item in new_items])


def delete_material(material_id):
    Material.query.filter(Material.id == material_id).delete()
    db.session.commit()
    return jsonify('The item has been deleted successfully')


def update_material(material_id):
    data = request.get_json()
    material = Material.query.filter(Material.id == material_id)
    material.update(data)
    db.session.commit()
    return jsonify([item.serialized for item in material])


def download_file(name):
    current_dir = os.getcwd()
    return send_from_directory(current_dir, name)


def generate_report():
    data = request.get_json()
    materials = Material.query.filter(Material.id.in_(data))
    iron_amount = [item.iron_amount for item in materials]
    silicon_amount = [item.silicon_amount for item in materials]
    aluminum_amount = [item.aluminum_amount for item in materials]
    sodium_amount = [item.sodium_amount for item in materials]
    sulfur_amount = [item.sulfur_amount for item in materials]
    headers_min = ['Минимальное содержание железа',
                   'Минимальное содержание кремния',
                   'Минимальное содержание алюминия',
                   'Минимальное содержание кальция',
                   'Минимальное содержание серы']
    headers_max = ['Максимальное содержание железа',
                   'Максимальное содержание кремния',
                   'Максимальное содержание алюминия',
                   'Максимальное содержание кальция',
                   'Максимальное содержание серы']
    headers_avg = ['Среднее содержание железа',
                   'Среднее содержание кремния',
                   'Среднее содержание алюминия',
                   'Среднее содержание кальция',
                   'Среднее содержание серы']
    with open('report.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(headers_min)
        writer.writerow([min(iron_amount), min(silicon_amount), min(aluminum_amount), min(sodium_amount),
                         min(sulfur_amount)])
        writer.writerow(headers_max)
        writer.writerow([max(iron_amount), max(silicon_amount), max(aluminum_amount), max(sodium_amount),
                         max(sulfur_amount)])
        writer.writerow(headers_avg)
        writer.writerow([mean(iron_amount), mean(silicon_amount), mean(aluminum_amount), mean(sodium_amount),
                         mean(sulfur_amount)])
        return redirect(url_for('materials.download_file', name=file.name))


def get_users():
    users = User.query.all()
    data = [item.serialized for item in users]
    return jsonify(data)


def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    user.set_password(data['password'])
    user.email = data['email']
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialized)


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.get(email == email)
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'authenticated': True})
    else:
        return 'Wrong credentials', 404


def add_user():
    data = request.get_json()
    password = data.pop('password')
    user = User(**data)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    data = user.serialized
    return jsonify(data)
