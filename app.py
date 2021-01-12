from flask_mysqldb import MySQL
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

app.config['MYSQL_USER'] = 'logiuser'
app.config['MYSQL_PASSWORD'] = 'logipass'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'crud-app'

mysql = MySQL(app)


@app.route('/')
def hello():
    return {
        "status": "ok",
        "message": "hello world"
    }


@app.route('/users')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users''')
    users = cur.fetchall()
    return {
        "users": users,
    }


@app.route('/users/<user_id>')
def show(user_id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE users.id = {user_id}")
    user = cur.fetchone()

    if not user:
        return make_response(jsonify({
            "message": "User not found"
        }), 404)

    return {
        "users": user,
    }


@app.route('/search')
def search():
    name = request.args.get('name')
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE users.name='{name}'")
    user = cur.fetchone()

    if not user:
        return make_response(jsonify({
            "message": "User not found"
        }), 404)

    return {
        "users": user,
    }


@app.route('/users', methods=['POST'])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')

    cur = mysql.connection.cursor()
    res2 = cur.execute(
        f"INSERT INTO `users` (`name`, `email`, `mobile`) VALUES ('{name}', '{email}', '{mobile}')")
    res = mysql.connection.commit()

    cur.execute('''SELECT * FROM users''')
    users = cur.fetchall()
    return {
        "users": users,
    }


@app.route('/users/<user_id>', methods=['PUT'])
def update(user_id):
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')

    cur = mysql.connection.cursor()
    res2 = cur.execute(
        f"UPDATE users SET `email` = '{email}',`name` = '{name}', `mobile` = '{mobile}' WHERE `users`.`id` = {int(user_id)}")

    res = mysql.connection.commit()

    cur.execute(f'SELECT * FROM users WHERE users.id={user_id}')
    user = cur.fetchone()
    return {
        "user": user,
    }


@app.route('/users/<user_id>', methods=['DELETE'])
def destroy(user_id):
    cur = mysql.connection.cursor()
    if not cur.execute(f"DELETE FROM users WHERE users.id={int(user_id)}"):
        return make_response({
            "message": "user not found"
        }, 404)
    res = mysql.connection.commit()

    cur.execute(f'SELECT * FROM users')
    users = cur.fetchall()
    return {
        "users": users,
    }
