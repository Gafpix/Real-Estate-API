from flask import jsonify, g, request
from flask_httpauth import HTTPBasicAuth

salt = '$*%klJf9'
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    from database import User
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(login=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


def recherche():
    from database import Property
    informations = request.get_json()
    if 'city' in informations:
        city = informations['city'].lower()
        properties = Property.query.filter_by(city=city).all()
        return jsonify([property.serialize for property in properties])
    else:
        return jsonify({'error': 'City is missing'}), 404


def add_user():
    from database import User, db
    import datetime
    informations = request.get_json()
    if 'login' in informations and 'password' in informations:
        if User.query.filter_by(login=informations['login']).first() is None:
            user = User()
            user.password = hash(salt + informations['password'])
            user.login = informations['login']
            if 'birthdate' in informations:
                dd_mm_aaaa = informations['birthdate']
                date = dd_mm_aaaa.split('_')
                if len(date) != 3:
                    user.birthdate = None
                else:
                    year = int(date[2])
                    month = int(date[1])
                    day = int(date[0])
                    if year > 1900 and day >=1:
                        if (month in [1,3,5,7,8,10,12] and day <=31) or (month in [4,6,9,11] and day <=30) or \
                                (month == 2 and day <=29):
                            user.birthdate = datetime.date(year, month, day)
                    else:
                        user.birthdate = None
            else:
                user.birthdate = None
            if 'name' in informations:
                user.name = informations['name']
            else:
                user.name = None
            if 'firstname' in informations:
                user.firstname = informations['firstname']
            else:
                user.firstname = None
            db.session.add(user)
            db.session.commit()
            return jsonify(user.serialize)
        else:
            return jsonify({'error': 'Login already exists'}), 404
    else:
        return jsonify({'error': 'Login or password is missing'}), 405


def get_users():
    from database import User
    return jsonify([user.serialize for user in User.query.all()])


@auth.login_required
def get_user():
    return jsonify(g.user.serialize)


@auth.login_required
def edit_user():
    import datetime
    from database import db
    informations = request.get_json()
    user = g.user
    if 'birthdate' in informations:
        dd_mm_aaaa = informations['birthdate']
        date = dd_mm_aaaa.split('_')
        if len(date) == 3:
            year = int(date[2])
            month = int(date[1])
            day = int(date[0])
            if year > 1900 and day >= 1:
                if (month in [1, 3, 5, 7, 8, 10, 12] and day <= 31) or (month in [4, 6, 9, 11] and day <= 30) or \
                        (month == 2 and day <= 29):
                    user.birthdate = datetime.date(year, month, day)
    if 'name' in informations:
        user.name = informations['name']
    if 'firstname' in informations:
        user.firstname = informations['firstname']
    if 'password' in informations:
        user.password = hash(salt + informations['password'])
    db.session.commit()
    return jsonify(user.serialize)


@auth.login_required
def add_property():
    from database import Property, Room, db
    informations = request.get_json()
    if 'name' in informations and 'city' in informations:
        if Property.query.filter_by(name=informations['name'], owner_id=g.user.id).first() is None:
            property = Property()
            property.name = informations['name']
            property.city = informations['city']
            property.owner_id = g.user.id
            if 'type' in informations:
                property.type = informations['type']
            else:
                property.type = ""
            if 'description' in informations:
                property.description = informations['description']
            else:
                property.description = ""
            if 'address' in informations:
                property.address = informations['address']
            else:
                property.address = ""
            db.session.add(property)
            db.session.commit()
            if 'rooms' in informations:
                property_id = Property.query.filter_by(name=informations['name'], owner_id=g.user.id).first().id
                for room in informations['rooms']:
                    var = Room()
                    var.property_id = property_id
                    if 'area' in room:
                        var.area = room['area']
                    else:
                        var.area = None
                    if 'description' in room:
                        var.description = room['description']
                    else:
                        var.description = ""
                    db.session.add(var)
                db.session.commit()
            final_property = Property.query.filter_by(name=informations['name'], owner_id=g.user.id).first()
            return jsonify(final_property.serialize)
        else:
            return jsonify({'error': 'Name already existing'}), 404
    else:
        return jsonify({'error': 'City or name is missing'}), 405


@auth.login_required
def edit_property():
    from database import Property, Room, db
    informations = request.get_json()
    if 'id' in informations:
        property = Property.query.filter_by(id=informations['id'], owner_id=g.user.id).first()
        if not property:
            return jsonify({'error': 'Property not existing or not yours'}), 405
        else:
            if 'name' in informations:
                if informations['name'] != property.name and Property.query.filter_by(name = informations['name']).count() == 0:
                    property.name = informations['name']
            if 'city' in informations:
                property.city = informations['city']
            if 'type' in informations:
                property.type = informations['type']
            if 'description' in informations:
                property.description = informations['description']
            if 'address' in informations:
                property.address = informations['address']
            if 'rooms' in informations:
                for room in informations['rooms']:
                    if 'action' in room:
                        if room['action'] == 'add':
                            var = Room()
                            var.property_id = property.id
                            if 'area' in room:
                                var.area = room['area']
                            else:
                                var.area = None
                            if 'description' in room:
                                var.description = room['description']
                            else:
                                var.description = ""
                            db.session.add(var)
                        elif room['action'] == 'delete' and 'id' in room:
                            var = Room.query.filter_by(id = room['id']).first()
                            db.session.delete(var)
                        elif room['action'] == 'edit' and 'id' in room:
                            var = Room.query.filter_by(id = room['id']).first()
                            if 'area' in room:
                                var.area = room['area']
                            if 'description' in room:
                                var.description = room['description']
            db.session.commit()
            final_property = Property.query.filter_by(id=informations['id']).first()
            return jsonify(final_property.serialize)
    else:
        return jsonify({'error': 'ID of property missing'}), 404


@auth.login_required
def get_properties():
    from database import Property
    properties = Property.query.filter_by(owner_id=g.user.id).all()
    return jsonify([property.serialize for property in properties])
