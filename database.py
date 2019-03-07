from flask_sqlalchemy import SQLAlchemy, event
from main import app
from itsdangerous import (TimedJSONWebSignatureSerializer as
                          Serializer, BadSignature, SignatureExpired)

db = SQLAlchemy(app.app)
salt = '$*%klJf9'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    firstname = db.Column(db.Text)
    birthdate = db.Column(db.Date)
    login = db.Column(db.Text)
    password = db.Column(db.Integer)
    properties = db.relationship('Property', backref='owner', cascade='delete', lazy='dynamic')

    @property
    def serialize(self):
        """Converts the object to make it serializable"""
        return {
            'ID': self.id,
            'Name': self.name,
            'Firstname': self.firstname,
            'Birthdate': self.serialize_date,
            'Properties': self.serialize_properties
        }

    @property
    def serialize_date(self):
        """Converts the object to make it serializable"""
        try:
            return self.birthdate.strftime("%d-%m-%Y")
        except:
            return None

    @property
    def serialize_properties(self):
        """Converts the object to make it serializable"""
        return [item.serialize for item in self.properties]

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.filter_by(id=data['id']).first()
        return user

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    def verify_password(self, password):
        password = salt + password
        return hash(password) == self.password


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    description = db.Column(db.Text)
    city = db.Column(db.Text)
    address = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rooms = db.relationship('Room', backref='property', cascade='delete', lazy='dynamic')

    @property
    def serialize(self):
        """Converts the object to make it serializable"""
        return {
            'ID': self.id,
            'Name': self.name,
            'Type': self.type,
            'Description': self.description,
            'City': self.city,
            'Address': self.address,
            'Owner': self.serialize_owner,
            'Rooms': self.serialize_rooms
        }

    @property
    def serialize_owner(self):
        value = self.owner
        return {
            'ID' : value.id,
            'Name': value.name,
            'Firstname': value.firstname,
            'Birthdate': value.serialize_date
        }

    @property
    def serialize_rooms(self):
        """Converts the object to make it serializable"""
        return [item.serialize for item in self.rooms]

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float)
    description = db.Column(db.Text)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))

    @property
    def serialize(self):
        """Converts the object to make it serializable"""
        return {
            'ID': self.id,
            'Area': self.area,
            'Description': self.description
        }

    @property
    def serialize_property(self):
        value = self.property
        return {
            'ID': value.id,
            'Nom': value.name,
            'Type': value.type,
            'Description': value.description,
            'Ville': value.city,
            'Proprietaire': value.serialize_owner
        }
