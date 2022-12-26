from flask import jsonify
from flask import request
import json
from app.models.vacunattion import Vacunattion
from app.models.vaccine_enfermedad import VaccineEnfermedad
from app.models.patient import Patient
from app.models.provincias import Province
from app.models.distributtion import Distributtion
import pymysql

def mostrar_vacunaciones():
   try:
       vacunaciones_actuales = Vacunattion.query.all()
     #   print(vacunaciones_actuales)
   except:
        return jsonify({"error": "500 Internal server Error"}), 500

   lista_vacunados = []
   for v in  vacunaciones_actuales:
        vacunacion = {
          "id" : v.id,
          "fecha_vacunacion" : v.fecha_vacunacion,
          "numero_dosis" : v.numero_dosis,
          "nombre del paciente" : v.paciente.nombre,
          "apellido del paciente" : v.paciente.apellido,
          "enfermedad" : v.enfermedad.nombre,
          "provincia" : v.provincia.nombre_provincia,
        }
        lista_vacunados.append(vacunacion)
   resp= lista_vacunados 
   return jsonify(resp), 200

def registrar_vacunacion(): 
  try:
      mydb =  pymysql.connect(
      host= "localhost",
      user="root",
      password="",
      database = "grupo6",
      port = 3306 )         
      cursor= mydb.cursor()
      insert_stmt = ("INSERT INTO vacunaciones (fecha_vacunacion, paciente_id, enfermedad_id, provincia_id, numero_dosis, regla_id) VALUES (%s, %s, %s, %s, %s, %s)")
      data = ( request.json['fecha_vacunacion'] , request.json['paciente_id'], request.json['enfermedad_id'],  request.json['provincia_id'], request.json['numero_dosis'], request.json['regla_id'])
      cursor.execute(insert_stmt, data)
      print(data)
      return jsonify("vacunacion registrada")
  except Exception as ex:
        return "error"
