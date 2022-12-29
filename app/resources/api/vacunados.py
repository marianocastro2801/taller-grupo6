from flask import jsonify
from flask import request
import json
from datetime import datetime
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
        if request.method == "POST":
            vacunacion = json.loads(request.data)
            fecha_vacunacion = vacunacion.get('fecha_vacunacion')
            paciente_id = vacunacion.get('paciente_id')
            enfermedad_id = vacunacion.get('enfermedad_id')
            provincia_id = vacunacion.get('provincia_id')
            numero_dosis = vacunacion.get('numero_dosis')
            vacunacion= Vacunattion(fecha_vacunacion,paciente_id,enfermedad_id, provincia_id, numero_dosis)
            vacunacion.save()
            print(vacunacion) 
        return "se realizo la vacunacion exitosamente"
    except:
      return jsonify({"error": " al cargar datos"}), 404

