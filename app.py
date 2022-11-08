from flask import Flask,request
from flask import jsonify
import json


######## Cassandra Import Statements ###########
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.query import SimpleStatement

app = Flask(__name__)
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect('Laboratorio')

@app.route("/")
def hello():
    return "Hola mundo, soy una prueba2"

@app.route('/Libros', methods=['GET'])
def get_libros():
    try:
        rows = session.execute("""select * from "Laboratorio"."Libro_Autor" """)
        Libros = []
        i = 0
        for row in rows:
            Libro = {'idTipo': row.idTipo, 'idCategoria': row.idCategoria, 'nombreAutor': row.nombreAutor, 'titulo': row.titulo,
                     'editorial': row.editorial, 'resenia': row.resenia}
            Libros.append(Libro)
            i = i + 1
        return jsonify({'Libros': Libros, 'mensaje': "Se listaron " + str(i) + " Libros.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/Libros_Cat/<codigo>', methods=['GET'])
def get_libros_cat(codigo):
    try:
        rows = session.execute(f'select * from "Laboratorio"."Libro_Autor" where "idTipo" = 1 and "idCategoria" = {codigo}')
        if rows != None:
            Libros = []
            i = 0
            for row in rows:
                Libro = {'idCategoria': row.idCategoria, 'titulo': row.titulo, 'editorial': row.editorial, 'resenia': row.resenia}
                Libros.append(Libro)
                i = i + 1
        return jsonify({'curso': Libros, 'mensaje': "Se listaron " + str(i) + " Libros de la categoria " + str(codigo), 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error cat", 'exito': False})

@app.route('/Autor_Cat/<codigo>', methods=['GET'])
def get_autor_cat(codigo):
    try:
        rows = session.execute(f'select * from "Laboratorio"."Libro_Autor" where "idTipo" = 1 and "idCategoria" = {codigo}')
        if rows != None:
            Libros = []
            i = 0
            for row in rows:
                Libro = {'idCategoria': row.idCategoria, 'nombreAutor': row.nombreAutor,}
                Libros.append(Libro)
                i = i + 1
        return jsonify({'curso': Libros, 'mensaje': "Se listaron " + str(i) + " Autores y su Libro por Categoria " + str(codigo), 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error cat", 'exito': False})

def cargar_Libro(codigo):
    try:
        dataDict = json.loads(codigo)
        fields = list(dataDict.keys())
        values = []
        for key, value in list(dataDict.items()):
            values.append(value)
        ins = """select * from "Laboratorio"."Libro_Autor" where """
        i = 0
        for x in range(6):
            if str(fields[x]) == 'idTipo' or str(fields[x]) == 'idCategoria':
                if x < 5 and i < 3:
                    ins = ins + "\"" + str(fields[x]) + "\" = " + str(values[x]) + " and "
                    i = i + 1
                else:
                    ins = ins + "\"" + str(fields[x]) + "\" = " + str(values[x])
            else:
                if str(fields[x]) == 'nombreAutor' or str(fields[x]) == 'titulo':
                    if x < 5 and i < 3:
                        ins = ins + "\"" + str(fields[x]) + "\" = \'" + str(values[x]) + "\' and "
                        i = i + 1
                    else:
                        ins = ins + "\"" + str(fields[x]) + "\" = \'" + str(values[x]) + "\'"
        rows = session.execute(ins)
        if len(rows.current_rows) != 0:
            return True
        else:
            insert = """INSERT INTO "Laboratorio"."Libro_Autor" (""" + "\"" + str(fields[0]) + "\", \"" + str(fields[1]) + "\", \"" + str(fields[2]) + "\", \"" + str(fields[3]) + "\", \"" + str(fields[4]) + "\", \"" + str(fields[5]) + "\")VALUES("
            for x in range(6):
                if str(fields[x]) == 'idTipo' or str(fields[x]) == 'idCategoria':
                    if x < 5:
                        insert = insert + str(values[x]) + ", "
                    else:
                        insert = insert + str(values[x]) + ")"
                else:
                    if x < 5:
                        insert = insert + "\'" + str(values[x]) + "\', "
                    else:
                        insert = insert + "\'" + str(values[x]) + "\')"
            rows = session.execute(insert)
            return None
    except Exception as ex:
        raise ex


@app.route('/Libros', methods=['POST'])
def registrar_libros():
    try:
        data = request.data
        if cargar_Libro(data) == None:
            return jsonify({'mensaje': "libro registrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "libro ya existe.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


if __name__ == '__main__':
    app.run(debug=True)
