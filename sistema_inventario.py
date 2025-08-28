import sqlite3

class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

class Inventario:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    cantidad INTEGER,
                    precio REAL
                )
            """)
            conn.commit()

    def agregar_producto(self, producto):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                (producto.nombre, producto.cantidad, producto.precio)
            )
            conn.commit()

    def eliminar_producto(self, id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id=?", (id,))
            conn.commit()

    def actualizar_producto(self, id, nombre=None, cantidad=None, precio=None):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if nombre:
                cursor.execute("UPDATE productos SET nombre=? WHERE id=?", (nombre, id))
            if cantidad is not None:
                cursor.execute("UPDATE productos SET cantidad=? WHERE id=?", (cantidad, id))
            if precio is not None:
                cursor.execute("UPDATE productos SET precio=? WHERE id=?", (precio, id))
            conn.commit()

    def buscar_producto(self, nombre):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
            return cursor.fetchall()

    def mostrar_todos(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            return cursor.fetchall()
