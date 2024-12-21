from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
bootstrap = Bootstrap(app)

# Ruta principal
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    data = cursor.fetchall()
    return render_template('index.html', usuarios=data)

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        mysql.connection.commit()
        flash('Usuario agregado exitosamente')
        return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        cursor.execute("UPDATE usuarios SET nombre = %s, correo = %s WHERE id = %s", (nombre, correo, id))
        mysql.connection.commit()
        flash('Usuario actualizado exitosamente')
        return redirect('/')
    else:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        return render_template('edit.html', usuario=usuario)

@app.route('/delete/<int:id>')
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Usuario eliminado exitosamente')
    return redirect('/')
