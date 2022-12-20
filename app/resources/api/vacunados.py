from flask import jsonify
from app.models.vacunattion import Vacunattion

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
          "paciente" : v.paciente.nombre,
          "enfermedad" : v.enfermedad.nombre,
          "provincia" : v.provincia.nombre_provincia,
        }
        lista_vacunados.append(vacunacion)
   resp= lista_vacunados 
   return jsonify(resp), 200

