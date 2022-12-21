from flask import jsonify
from flask import request
import json
from app.models.vacunattion import Vacunattion
from app.models.patient import Patient

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
    paciente_actual = Patient.get_by_id(idpaciente)
    try:
        if request.method == "POST":
            vacunacion = json.loads(request.data)
            paciente = vacunacion.get('idPaciente')
            vacuna = vacunacion.get('vacuna')
            provincia = vacunacion.get('provincia')
            fecha = vacunacion.get('fecha')
            # if cuota is None:
            #     return jsonify({"error": "404 la cuota no existe"}), 404
            # if Pago.pago_de_una_cuota(cuota.id) is None:
            #     cuota.estado = Cuota.get_estado_paga()
            #     fecha_hoy = datetime.now()
            #     recargo_cuota = Config.get_valor_porcentaje()
            #     dia_actual = int(fecha_hoy.strftime('%d'))
            #     mes_actual = int(fecha_hoy.strftime('%m'))
            #     if dia_actual >= 1 and dia_actual <= 10:
            #         cuota.register_cuota_database()
            #         pago = Pago(cuota.id, monto_sin_recargo,periodo)
            #         pago.register_pago_database()
            #     else:
            #         recargo = (cuota.monto * recargo_cuota)/100
            #         monto_recargo = cuota.monto + recargo
            #         cuota.monto = monto_recargo
            #         cuota.register_cuota_database()
            #         pago = Pago(cuota.id, monto_recargo,cuota.periodo)
            #         pago.register_pago_database()
            # else:
            #     return "la cuota ya fue pagada"
        return "la vacunacion se realizo con exito"
    except:
        return jsonify({"error": " al cargar datos"}), 404
