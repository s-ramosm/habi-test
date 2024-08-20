import mysql.connector
# Configura los parámetros de conexión
conexion = mysql.connector.connect(
    host="3.138.156.32",
    user="pruebas",
    password="VGbt3Day5R",
    database="habi_db",
    port = "3309"
)


cursor = conexion.cursor()

if __name__ == "__main__":
    cursor.execute("SHOW TABLES")


    tablas = cursor.fetchall()
    for tabla in tablas:
        print(tabla[0])
        cursor.execute(f"SHOW COLUMNS FROM {tabla[0]}")
        columnas = cursor.fetchall()
        for columna in columnas:
            print(f"Nombre: {columna[0]}, Tipo: {columna[1]}")

        print ("______________________________________________________")