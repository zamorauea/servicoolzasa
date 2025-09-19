from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os, json
from inventario import Inventario  # Tu archivo inventario.py

app = Flask(__name__)

# Configuración SQLite para clientes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    mensaje = db.Column(db.Text)

with app.app_context():
    db.create_all()

# Instancia de inventario
inventario = Inventario()

# ------------------ Rutas principales ------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/servicios')
def servicios():
    return render_template("servicios.html")

@app.route('/productos')
def productos():
    return render_template("productos.html")

@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/formulario_aires')
def formulario_aires():
    return render_template("formulario_aires.html")


@app.route('/agregar_ac', methods=['POST'])
def agregar_ac():
    modelo = request.form['modelo']
    capacidad = request.form['capacidad']
    marca = request.form['marca']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])

    inventario.agregar_ac(modelo, capacidad, marca, cantidad, precio)
    return redirect(url_for('listar_aires'))


# ------------------ Clientes ------------------
@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    mensaje = request.form['mensaje']

    # Guardar en JSON
    archivo = "datos/clientes.json"
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            clientes = json.load(f)
    else:
        clientes = []
    clientes.append({"nombre": nombre, "correo": correo, "mensaje": mensaje})
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

    # Guardar en SQLite
    nuevo_cliente = Cliente(nombre=nombre, correo=correo, mensaje=mensaje)
    db.session.add(nuevo_cliente)
    db.session.commit()

    return redirect(url_for("index"))

@app.route('/clientes')
def ver_clientes():
    clientes = Cliente.query.all()
    return render_template("resultado.html", datos=clientes)

@app.route('/clientes_json')
def ver_clientes_json():
    archivo = "datos/clientes.json"
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            clientes = json.load(f)
    else:
        clientes = []
    return render_template("resultado.html", datos=clientes)

# ------------------ Aires acondicionados ------------------
@app.route('/formulario_aires')
def formulario_aires():
    return render_template("formulario_aires.html")

@app.route('/agregar_ac', methods=['POST'])
def agregar_ac():
    modelo = request.form['modelo']
    capacidad = request.form['capacidad']
    marca = request.form['marca']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])

    inventario.agregar_ac(modelo, capacidad, marca, cantidad, precio)
    return redirect(url_for('listar_aires'))

@app.route('/listar_aires')
def listar_aires():
    aires = inventario.mostrar_aires()
    return render_template("resultado_aires.html", datos=aires)


# ------------------ Ejecutar app ------------------
if __name__ == '__main__':
    app.run(debug=True)
