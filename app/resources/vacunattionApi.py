from app.models.provincias import Province
from app.models.shopping import Shopping
from flask import redirect, render_template, request, url_for, abort, session, flash, json
import random
from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql.expression import true
from app.helpers.auth import authenticated
from app.helpers.verifications import user_has_permission
from app.models.user import User
from app.models.vaccine import Vaccine
from app.models.vaccine_type import VaccineType
from app.models.vaccine_lote import VaccineLote
from app.models.vaccine_developer import VaccineDeveloper
from app.models.vaccine_enfermedad import VaccineEnfermedad
from app.models.vacunattion import Vacunattion
from app.models.distributtion import Distributtion
from app.models.vaccine_vencidas import VaccineVencida
from app.models.patient import Patient
from app.models.rol import Rol
from app.models.vacunaciones_api import VacunattionApi
import re
from tkinter import *
from tkinter import messagebox as MessageBox
from datetime import date
import pymysql
import psycopg2
import requests
import dateutil.parser




#------------------------------------------------
def new_con_api():
    if not authenticated(session):
         return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_new"):  
        abort(401)

    pacientes = Patient.get_all_pacientes()

    url = "https://api.claudioraverta.com/personas/33333331/"
    response = requests.get(url)
    if response.status_code == 200:
    #    print (response.content)
        data = response.json()
    #    print (data)
        
        #import json 
        array = json.dumps(data)
        a = json.loads(array)
    #    print (a)
    #DATOS PACIENTE 33333331
        dniPaciente = a['DNI']
        nombre = a['nombre']
        apellido = a['apellido']
        ciudad = a['ciudad']
        fechaNac = a['fecha_hora_nacimiento']

    
    
    enfermedades = VaccineEnfermedad.get_all_enfermedades()
    provincias = Province.get_all_provincias()

    return render_template(
        "vacunaciones/index.html",
        vacunattionApi=None,
        message="consumiendo datos desde api Claudio",
        mode="create",
        pacientes=pacientes,
        enfermedades = enfermedades,
        provincias= provincias,
        
        #estos son de ejemplo paciente 33333331
        dniPaciente = dniPaciente,
        nombre = nombre,
        apellido = apellido,
        ciudad = ciudad,
        fechaNac = fechaNac,
    

        )

def save_con_api():
    
    new_vacunattion = request.form.copy()
    new_vacunattion.pop("id", None)
    #recupero DNI del formulario 
    dniFormulario = new_vacunattion.pop("dni")

    fecha_vacunacion = new_vacunattion.pop("fecha_vacunacion")
    vacunaContra = new_vacunattion.pop("enfermedad_id")
    provincia = new_vacunattion.pop("provincia_id")

        
    #Busco en la API DE CLAUDIO datos del paciente con dniFormulario 
    url = "https://api.claudioraverta.com/personas/"+ dniFormulario
    response = requests.get(url)
    if response.status_code == 200:
        #print (response.content)
        data = response.json()
        #print (data)
            
         #import json 
        array = json.dumps(data)
        a = json.loads(array)
        #print (a)

        #YA CON LOS DATOS DEL PACIENTE DE LA API DE CLAUDIO

        #dni = a['DNI']
        nombre = a['nombre']
        apellido = a['apellido']
        fecha_nacimiento = a['fecha_hora_nacimiento']

        new_vacunattion = request.form.copy()
        new_vacunattion.pop("id", None)
            
        #DEBO GUARDARLOS EN LA BASE DE DATOS

        mydb =  pymysql.connect(
        host= "localhost",
        user="root",
        password="",
        database = "grupo6",
        port = 3306   )
            
        cursor= mydb.cursor()
#NO HACE FALTA PONER EL ID ES AUTOINCREMENTAL !!!!!!!!!!!! UNICO
        insert_stmt = ("INSERT INTO vacunaciones_api (dni, nombre, apellido, fecha_nacimiento, enfermedad_id, provincia_id, fecha_vacunacion) VALUES ( %s, %s,%s, %s, %s, %s, %s)")    
        
            #debo convertir el datetime a date sino no lo toma
            
            
        fecha_nacimiento = dateutil.parser.parse(fecha_nacimiento).date()
            
            

            
        data = (dniFormulario,str(nombre),str(apellido),fecha_nacimiento,int(vacunaContra),int(provincia),fecha_vacunacion)
        cursor.execute(insert_stmt, data)   
            
        mydb.commit() #gracias padre si funciona!!
        cursor.close()
            

        flash("Vacunacion con Api de claudio exitosa")
        return redirect(url_for("vacunattiones.vacunattion_index"))

    else: print ("NO INSERTA")


#----------------------------- 