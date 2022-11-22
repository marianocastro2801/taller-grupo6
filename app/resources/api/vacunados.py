from flask import jsonify
from app.models.vacunattion import Vacunattion

def mostrar_vacunaciones():
   try:
       vacunaciones_actuales = Vacunattion.query.all()
   except:
        return jsonify({"error": "500 Internal server Error"}), 500

   lista_vacunados = []
   for v in  vacunaciones_actuales:
        vacunacion = {
          "fecha_vacunacion" : v.fecha_vacunacion,
          "numero_dosis" : v.numero_dosis,
          "paciente" : v.paciente_id,
          "enfermedad" : v.enfermedad.id,
          "provincia" : v.provincia_id,
        }
        lista_vacunados.append(vacunacion)
   resp= lista_vacunados 
   return jsonify(resp), 200