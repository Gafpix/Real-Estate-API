from flask import Flask, jsonify, request, g
from flask_httpauth import HTTPBasicAuth
import connexion

app = connexion.FlaskApp(__name__)
app.add_api('app.yaml')
application = app.app

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
application.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'Arcane'

if __name__ == '__main__':
    from database import db
    db.create_all()
    app.run(debug=True)