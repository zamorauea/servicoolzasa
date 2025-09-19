import sqlite3

# Clase AireAcondicionado
class AireAcondicionado:
    def __init__(self, id_ac, modelo, capacidad, marca, cantidad, precio):
        self.id_ac = id_ac
        self.modelo = modelo
        self.capacidad = capacidad
        self.marca = marca
        self.cantidad = cantidad
        self.precio = precio

# Clase Inventario
class Inventario:
    def __init__(self):
        self.conn = sqlite3.connect("inventario.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS aires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modelo TEXT NOT NULL,
                capacidad TEXT NOT NULL,
                marca TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
                )
        ''')
        self.conn.commit()

    def agregar_ac(self, modelo, capacidad, marca, cantidad, precio):
        self.cursor.execute(
            "INSERT INTO aires (modelo, capacidad, marca, cantidad, precio) VALUES (?, ?, ?, ?, ?)",
            (modelo, capacidad, marca, cantidad, precio)
        )
        self.conn.commit()

    def mostrar_aires(self):
        self.cursor.execute("SELECT * FROM aires")
        return self.cursor.fetchall()

    def eliminar_ac(self, id_ac):
        self.cursor.execute("DELETE FROM aires WHERE id=?", (id_ac,))
        self.conn.commit()
