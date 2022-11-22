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

# def mostrar_vacunacion_por_vacuna_desarrollada(id):
#     try:
#         vacunaciones_por_vacuna = Vacunattion.query.filter(id)
#         print(vacunaciones_por_vacuna)
#     except:
#         return jsonify({"error": "500 Internal server Error"}), 500
    
#     if not vacunaciones_por_vacuna:
#         return jsonify({"error": "404 el id no existe"}), 404
    
#     dic= { 
#             "fecha_vacunacion" : vacunaciones_por_vacuna.fecha_vacunacion,
#             "numero_dosis" : vacunaciones_por_vacuna.numero_dosis,
#             "paciente" : vacunaciones_por_vacuna.paciente_id,
#             "provincia" : vacunaciones_por_vacuna.provincia_id,
#          }
    
#     resp= {'atributos':dic }
#     return jsonify(resp), 200