from flask import Blueprint
from .views import get_materials, add_material, update_material, get_users, add_user, update_user, get_material, \
    get_user, login, delete_material, generate_report, download_file

materials = Blueprint('materials', __name__)
materials.route('/', methods=['GET'])(get_materials)
materials.route('/add-material', methods=['GET', 'POST'])(add_material)
materials.route('/get-material/<int:material_id>', methods=['GET'])(get_material)
materials.route('/update-material/<int:material_id>', methods=['GET', 'POST', 'PUT', 'PATCH'])(update_material)
materials.route('/delete-material/<int:material_id>', methods=['GET', 'POST'])(delete_material)
materials.route('/login', methods=['GET', 'POST'])(login)
materials.route('/users', methods=['GET'])(get_users)
materials.route('/add-user', methods=['GET', 'POST'])(add_user)
materials.route('/get-user/<int:user_id>', methods=['GET'])(get_user)
materials.route('/update-user/<int:user_id>', methods=['GET', 'POST', 'PUT', 'PATCH'])(update_user)
materials.route('/generate-report', methods=['GET', 'POST'])(generate_report)
materials.route("/uploads/<name>", endpoint="download_file")(download_file)
