from flask import Flask, render_template, request, redirect
app = Flask(__name__)
inventario = Inventario()

@app.route('/')
def index():
    productos = inventario.mostrar_todos()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        producto = Producto(None, nombre, cantidad, precio)
        inventario.agregar_producto(producto)
        return redirect('/')
    return render_template('agregar.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    inventario.eliminar_producto(id)
    return redirect('/')

@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    productos = inventario.mostrar_todos()
    producto = next((p for p in productos if p[0] == id), None)
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        inventario.actualizar_producto(id, nombre, cantidad, precio)
        return redirect('/')
    return render_template('actualizar.html', producto=producto)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        resultados = inventario.buscar_producto(nombre)
        return render_template('index.html', productos=resultados)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
