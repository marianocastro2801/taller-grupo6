from flask import jsonify
from flask import request
import json
from app.models.vacunattion import Vacunattion
from app.models.vaccine_enfermedad import VaccineEnfermedad
from app.models.patient import Patient
from app.models.provincias import Province
from app.models.distributtion import Distributtion
from dateutil.relativedelta import relativedelta

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
        # traer valores del  formulario
        if request.method == "POST":
            vacunacion = json.loads(request.data)
            idPaciente = vacunacion.get('idPaciente')
            idProvincia = vacunacion.get('idProvincia')
            idVacuna = vacunacion.get('idVacuna')
            fecha = vacunacion.get('fecha')
            numero_dosis = vacunacion.get('numero_dosis')       
            #registrar pago en la bd     
        return "se registro la vacunacion con exito"
  except:
        return jsonify({"error": " al cargar datos"}), 404
  