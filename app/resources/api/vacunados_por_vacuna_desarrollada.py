from flask import jsonify
from app.models.vacunattion import Vacunattion

def mostrar_vacunacion_por_vd(id):
     try:
        lista = []
        vacunaciones_por_vacuna = Vacunattion.get_vacunattiones_by_enfermedad(id)
        # print(vacunaciones_por_vacuna)
        for vacuna in vacunaciones_por_vacuna:
                v = {
                    "fecha_vacunacion" : vacuna.fecha_vacunacion,
                    "enfermedad" : vacuna.enfermedad.nombre,
                    "numero_dosis" : vacuna.numero_dosis,
                    "paciente" : vacuna.paciente.nombre,
                    "provincia" : vacuna.provincia.nombre_provincia
                }
                lista.append(v)

     except:
         return jsonify({"error": "500 Internal server Error"}), 500
    
     if not vacunaciones_por_vacuna:
         return jsonify({"error": "404 el id no existe"}), 404
     resp = lista
     return jsonify(resp), 200