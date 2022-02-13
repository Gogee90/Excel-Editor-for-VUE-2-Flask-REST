from flask import Flask
from flask_user import UserManager
from flask_cors import CORS

from raw_material_quality_app.models import db, User
from raw_material_quality_app.routes import materials
from raw_material_quality_app.views import login_manager

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['USER_EMAIL_SENDER_EMAIL'] = 'admin@example.com'
app.secret_key = 'xxxxyyyyyzzzzz'
login_manager.init_app(app)
app.register_blueprint(materials)
db.init_app(app)

user_manager = UserManager(app, db, User)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
