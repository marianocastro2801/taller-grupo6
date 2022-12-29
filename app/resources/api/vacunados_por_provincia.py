from flask import jsonify
from app.models.vacunattion import Vacunattion

def mostrar_vacunacion_por_provincia(id):
     try:
        lista = []
        vacunaciones_por_provincia = Vacunattion.get_vacunattiones_by_provincia(id)
        for vacuna in vacunaciones_por_provincia:
                v = {
                    "fecha_vacunacion" : vacuna.fecha_vacunacion,
                    "enfermedad" : vacuna.enfermedad.nombre,
                    "numero_dosis" : vacuna.numero_dosis,
                    "nombre del paciente" : vacuna.paciente.nombre,
                    "apellido del paciente" : vacuna.paciente.apellido , 
                    "provincia" : vacuna.provincia.nombre_provincia
                }
                lista.append(v)

     except:
         return jsonify({"error": "500 Internal server Error"}), 500
    
     if not vacunaciones_por_provincia:
         return jsonify({"error": "404 el id de la provincia no registra vacunaciones"}), 404
     resp = lista
     return jsonify(resp), 200