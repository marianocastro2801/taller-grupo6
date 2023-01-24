from app.models.provincias import Province
from app.models.shopping import Shopping
from flask import redirect, render_template, request, url_for, abort, session, flash
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
import re
from tkinter import *
from tkinter import messagebox as MessageBox
from datetime import date
import pymysql
import psycopg2


def index(enfermedad_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_index"):  
        abort(401)

    #vacunattiones = Vacunattion.get_vacunattiones_by_provincia(provincia_id)
    distributtiones = Distributtion.get_filtered(enfermedad_id) #de una enferemdad_id
    enfermedades = VaccineEnfermedad.get_all_enfermedades()
    tot = sumar_cantidades(distributtiones)

    #vacunattiones = Vacunattion.get_all_vacunaciones()
    dosisVencidas = sumar_dosis_vencidas(distributtiones)

    tot = tot - dosisVencidas    
    vacuna = VaccineEnfermedad.get_by_id(enfermedad_id)
    vacuna = vacuna.nombre
    provincias = Province.get_all_provincias()

    #CADA VEZ QUE HAGO UNA VACUNACION DEBO DISMINUIR (antes de mandar tot calclulo cuantas vacunaciones tiene y las resto) 

    
    vacunattiones = Vacunattion.get_vacunattiones_by_enfermedad(enfermedad_id)
    cant = len(vacunattiones)

    return render_template(
        "vacunaciones/vacunattion_index.html",
        vacunattiones= vacunattiones,
        tot = tot - cant,      #descuento las vacunaciones para obtener el total correcto
        distributtiones = distributtiones,
        enfermedades= enfermedades,
        vacuna= vacuna,
        provincias= provincias,
        dosisVencidas = dosisVencidas,
    )


def sumar_cantidades (distributtiones):
    suma = 0
    
    for numero in distributtiones:
            suma+= numero.cantidad
    return suma

def sumar_dosis_vencidas(distributtiones):

    suma = 0
    for numero in distributtiones:
        if numero.lote_id == 5:     #si el lote esta vencido o podria preguntar: si el lote. fechaVenc es mayor a la fecha actual
            suma+= numero.cantidad


    return suma

def new():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_new"):  
        abort(401)

    pacientes = Patient.get_all_pacientes()
    enfermedades = VaccineEnfermedad.get_all_enfermedades()
    provincias = Province.get_all_provincias()

    return render_template(
        "vacunaciones/vacunattion_new.html",
        vacunattion=None,
        message="Registrar Vacunacion",
        mode="create",
        pacientes=pacientes,
        enfermedades = enfermedades,
        provincias= provincias,

    )

def save():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_new"): 
        abort(401)

    new_vacunattion = request.form.copy()
    new_vacunattion.pop("id", None)

#validar las vacunaciones antes de guardar
    e = new_vacunattion.pop("enfermedad_id")
    f = new_vacunattion.pop("fecha_vacunacion")



    fecha1 = date(2010, 1, 1)
    fecha2 = date(2010, 12, 31)
    
#IMPEDIR VACUNACION SI NO HAY STOCK 
    distributtiones = Distributtion.get_filtered(e)
    vacunattiones = Vacunattion.get_vacunattiones_by_enfermedad(e)
    tot = sumar_cantidades(distributtiones) - len(vacunattiones)  #tot= stock provincial
    dv= sumar_dosis_vencidas (distributtiones) #CONTROLAR QUE NO VACUNE CON DOSIS VENCIDAS
    if (tot == 0):
        flash("No hay stock para realizar la vacunacion de esa vacuna")
        return redirect(url_for("vacunattiones.vacunattion_index"))
    elif (dv > 0) and (tot == 0): 
        flash("Dosis vencidas. No pueden ser usadas")
        return redirect(url_for("vacunattiones.vacunattion_index"))
    
#----------------------------------------------------------------------------
#BCG
    unicaDosis = new_vacunattion.pop("numero_dosis")
    paciente_id = new_vacunattion.pop("paciente_id")
    paciente = Patient.get_by_id(paciente_id)
    dentro_dos_meses = paciente.fecha_nacimiento + relativedelta(months=2)
    if e == "11" and unicaDosis == '5': # EL USUARIO ELIGIO BCG y ES UNA UNICA DOSIS
        if format(f) < str(dentro_dos_meses):
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("Se ha registrado la vacunacion exitosamente de BCG") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        elif unicaDosis == '5': 
            flash("el paciente no cumple la condicion de los 2 meses recien nacido ")                 
            return redirect(url_for("vacunattiones.vacunattion_index"))
    elif e == "11": 
            flash("La vacuna BCG corresponde: Unica Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))

#----------------------------------------------------------------------------
#TRIPLE BACTERIANA
    dentro_5_year = paciente.fecha_nacimiento + relativedelta(years=5)
    # dentro_6_year = paciente.fecha_nacimiento + relativedelta(year=6)
    if e == "3" and unicaDosis == '5': # EL USUARIO ELIGIO TRIPLE BACTERIANA y ES UNA UNICA DOSIS
        if format(f) < str(dentro_5_year):
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("Se ha registrado la vacunacion exitosamente de TRIPLE BACTERIANA") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        elif unicaDosis == '5': 
            flash("el paciente no cumple la condicion entre los 5 años y 6 años recien nacido ")                 
            return redirect(url_for("vacunattiones.vacunattion_index"))
    elif e == "3": 
            flash("La vacuna TRIPLE BACTERIANA corresponde: Unica Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))
#----------------------------------------------------------------------------
#DOBLE BACTERIANA
    dentro_18_year = paciente.fecha_nacimiento + relativedelta(years=18)
    if e == "16" and unicaDosis == '1': # EL USUARIO ELIGIO TRIPLE BACTERIANA y ES UNA UNICA DOSIS
        if format(f) < str(dentro_18_year):
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("Se ha registrado la vacunacion exitosamente de DOBLE BACTERIANA") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        elif unicaDosis == '1': 
            flash("el paciente no cumple la condicion de ser mayor a 18 años ")                 
            return redirect(url_for("vacunattiones.vacunattion_index"))
    elif e == "3": 
            flash("La vacuna TRIPLE BACTERIANA corresponde: Primera Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))

#----------------------------------------------------------------------------
#fiebre amarrilla
    dentro_18_meses = paciente.fecha_nacimiento + relativedelta(months=18)
    if e == "18" and unicaDosis == '1': # EL USUARIO ELIGIO fiebre amarrilla 
        if format(f) < str(dentro_18_meses):
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("Se ha registrado la vacunacion exitosamente de fiebre amarrilla") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        elif unicaDosis == '1': 
            flash("el paciente no cumple la condicion de los 18 meses")                 
            return redirect(url_for("vacunattiones.vacunattion_index"))
    elif e == "11": 
            flash("La vacuna fiebre amarrilla corresponde a: Primera Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))

#----------------------------------------------------------------------------
#ROTAVIRUS
    dentro_dos_meses = paciente.fecha_nacimiento + relativedelta(months=2)
    dentro_cuatro_meses = paciente.fecha_nacimiento + relativedelta(months=4)
    # EL USUARIO ELIGIO ROTAVIRUS y SON 2 DOSIS
    if e == '156':
        if  unicaDosis == '1':
            if format(f) <= str(dentro_dos_meses) :
                new_vacunattion = request.form.copy()
                new_vacunattion.pop("id", None) 
                Vacunattion(**new_vacunattion).save()
                flash("Se ha registrado la vacunacion exitosamente de ROTAVIRUS al paciente de 2 meses") 
                return redirect(url_for("vacunattiones.vacunattion_index"))
            elif unicaDosis == '1': 
                    flash("el paciente no cumple la condicion de los 2 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
             if unicaDosis == '2':
                if format(f) <= str(dentro_cuatro_meses) :
                    new_vacunattion = request.form.copy()
                    new_vacunattion.pop("id", None) 
                    Vacunattion(**new_vacunattion).save()
                    flash("Se ha registrado la vacunacion exitosamente de ROTAVIRUS al paciente de 4 meses") 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
                elif unicaDosis == '2': 
                    flash("el paciente no cumple la condicion de los 4 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))     
        if unicaDosis != '1' and unicaDosis != '2':
            flash("La vacuna Rotavirus corresponde a : Primera Dosis y  Segunda Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))

#----------------------------------------------------------------------------
#VARICELA
    dentro_15_meses = paciente.fecha_nacimiento + relativedelta(months=15)
    dentro_5_year = paciente.fecha_nacimiento + relativedelta(years=5)
    # EL USUARIO ELIGIO VARICELA y SON 2 DOSIS
    if e == '6':
        if  unicaDosis == '1':
            if format(f) <= str(dentro_15_meses) :
                new_vacunattion = request.form.copy()
                new_vacunattion.pop("id", None) 
                Vacunattion(**new_vacunattion).save()
                flash("Se ha registrado la vacunacion exitosamente de VARICELA al paciente de 15 meses") 
                return redirect(url_for("vacunattiones.vacunattion_index"))
            elif unicaDosis == '1': 
                    flash("el paciente no cumple la condicion de los 15 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
             if unicaDosis == '2':
                if format(f) <= str(dentro_5_year) :
                    new_vacunattion = request.form.copy()
                    new_vacunattion.pop("id", None) 
                    Vacunattion(**new_vacunattion).save()
                    flash("Se ha registrado la vacunacion exitosamente de VARICELA al paciente de 5 años") 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
                elif unicaDosis == '2': 
                    flash("el paciente no cumple la condicion de 5 años ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))     
        if unicaDosis != '1' and unicaDosis != '2':
            flash("La vacuna VARICELA corresponde a : Primera Dosis y  Segunda Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))

            
#----------------------------------------------------------------------------
#Neumococo Conjugada
    dentro_dos_meses = paciente.fecha_nacimiento + relativedelta(months=2)
    dentro_cuatro_meses = paciente.fecha_nacimiento + relativedelta(months=4)
    # EL USUARIO ELIGIO Neumococo Conjugada y SON 2 DOSIS
    if e == '7':
        if  unicaDosis == '1':
            if format(f) <= str(dentro_dos_meses) :
                new_vacunattion = request.form.copy()
                new_vacunattion.pop("id", None) 
                Vacunattion(**new_vacunattion).save()
                flash("Se ha registrado la vacunacion exitosamente de Neumococo Conjugada al paciente de 2 meses") 
                return redirect(url_for("vacunattiones.vacunattion_index"))
            elif unicaDosis == '1': 
                    flash("el paciente no cumple la condicion de los 2 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
             if unicaDosis == '2':
                if format(f) <= str(dentro_cuatro_meses) :
                    new_vacunattion = request.form.copy()
                    new_vacunattion.pop("id", None) 
                    Vacunattion(**new_vacunattion).save()
                    flash("Se ha registrado la vacunacion exitosamente de Neumococo Conjugada al paciente de 4 meses") 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
                elif unicaDosis == '2': 
                    flash("el paciente no cumple la condicion de los 4 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))     
        if unicaDosis != '1' and unicaDosis != '2':
            flash("La vacuna Neumococo Conjugada corresponde a : Primera Dosis y  Segunda Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))

#----------------------------------------------------------------------------
#pentavalente o quíntuple
    dentro_dos_meses = paciente.fecha_nacimiento + relativedelta(months=2)
    dentro_cuatro_meses = paciente.fecha_nacimiento + relativedelta(months=4)
    dentro_seis_meses = paciente.fecha_nacimiento + relativedelta(months=6)
    # EL USUARIO ELIGIO pentavalente o quíntuple y SON 3 DOSIS
    if e == '157':
        if  unicaDosis == '1':
            if format(f) <= str(dentro_dos_meses) :
                new_vacunattion = request.form.copy()
                new_vacunattion.pop("id", None) 
                Vacunattion(**new_vacunattion).save()
                flash("Se ha registrado la vacunacion exitosamente de pentavalente o quíntuple al paciente de 2 meses") 
                return redirect(url_for("vacunattiones.vacunattion_index"))
            elif unicaDosis == '1': 
                    flash("el paciente no cumple la condicion de los 2 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
             if unicaDosis == '2':
                if format(f) <= str(dentro_cuatro_meses) :
                    new_vacunattion = request.form.copy()
                    new_vacunattion.pop("id", None) 
                    Vacunattion(**new_vacunattion).save()
                    flash("Se ha registrado la vacunacion exitosamente de pentavalente o quíntuple al paciente de 4 meses") 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
                elif unicaDosis == '2': 
                    flash("el paciente no cumple la condicion de los 4 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
        if  unicaDosis == '3':
            if format(f) <= str(dentro_seis_meses) :
                    new_vacunattion = request.form.copy()
                    new_vacunattion.pop("id", None) 
                    Vacunattion(**new_vacunattion).save()
                    flash("Se ha registrado la vacunacion exitosamente de pentavalente o quíntuple al paciente de 6 meses") 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
            elif unicaDosis == '3': 
                    flash("el paciente no cumple la condicion de los 6 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index")) 
        if unicaDosis != '1' and unicaDosis != '2' and unicaDosis != '3' :
            flash("La vacuna pentavalente o quíntuple corresponde a : Primera Dosis , Segunda Dosis y Tercera Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))

#----------------------------------------------------------------------------
#SALK
    dentro_dos_meses = paciente.fecha_nacimiento + relativedelta(months=2)
    dentro_cuatro_meses = paciente.fecha_nacimiento + relativedelta(months=4)
    dentro_seis_meses = paciente.fecha_nacimiento + relativedelta(months=6)
    # EL USUARIO ELIGIO SALK y SON 3 DOSIS
    if e == '158':
        if  unicaDosis == '1':
            if format(f) <= str(dentro_dos_meses) :
                new_vacunattion = request.form.copy()
                new_vacunattion.pop("id", None) 
                Vacunattion(**new_vacunattion).save()
                flash("Se ha registrado la vacunacion exitosamente de SALK al paciente de 2 meses") 
                return redirect(url_for("vacunattiones.vacunattion_index"))
            elif unicaDosis == '1': 
                    flash("el paciente no cumple la condicion de los 2 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
             if unicaDosis == '2':
                if format(f) <= str(dentro_cuatro_meses) :
                    new_vacunattion = request.form.copy()
                    new_vacunattion.pop("id", None) 
                    Vacunattion(**new_vacunattion).save()
                    flash("Se ha registrado la vacunacion exitosamente de SALK al paciente de 4 meses") 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
                elif unicaDosis == '2': 
                    flash("el paciente no cumple la condicion de los 4 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
        if  unicaDosis == '3':
            if format(f) <= str(dentro_seis_meses) :
                    new_vacunattion = request.form.copy()
                    new_vacunattion.pop("id", None) 
                    Vacunattion(**new_vacunattion).save()
                    flash("Se ha registrado la vacunacion exitosamente de SALK al paciente de 6 meses") 
                    return redirect(url_for("vacunattiones.vacunattion_index"))
            elif unicaDosis == '3': 
                    flash("el paciente no cumple la condicion de los 6 meses ")                 
                    return redirect(url_for("vacunattiones.vacunattion_index")) 
        if unicaDosis != '1' and unicaDosis != '2' and unicaDosis != '3' :
            flash("La vacuna SALK corresponde a : Primera Dosis , Segunda Dosis y Tercera Dosis")
            return redirect(url_for("vacunattiones.vacunattion_index"))


#----------------------------------------------------------------------------
    if e == "19": #pandemia 2010
        if format(f) < str(fecha1) or format(f) > str(fecha2):
            flash("La vacunacion de la pandemia 2010 ya finalizo, corresponde al año 2010") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("La vacunacion se registro exitosamente") 
            return redirect(url_for("vacunattiones.vacunattion_index"))

#-------------------------------------------------------------------------------
    fecha1 = date(2020, 1, 1)
    fecha2 = date(2023, 12, 31)

    if e == "1": #Covid 19
        if format(f) < str(fecha1) or format(f) > str(fecha2):
            flash("La vacunacion de Covid-19 finalizó") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("La vacunacion se registro exitosamente") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
#-------------------------------------------------------------------------------   
    fecha1 = date(2022, 1, 1)
    fecha2 = date(2022, 12, 31)
    
    if e == "2": #Antigripal
        if format(f) < str(fecha1) or format(f) > str(fecha2):
            flash("La vacunacion Antigripal ya finalizo, corresponde al año 2022") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        else:
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("La vacunacion se registro exitosamente") 
            return redirect(url_for("vacunattiones.vacunattion_index"))

#--------------------------------------------------------------------------------
    paciente_id = new_vacunattion.pop("paciente_id")
    unicaDosis = new_vacunattion.pop("numero_dosis")
    paciente = Patient.get_by_id(paciente_id)

    dentro_de_anio = paciente.fecha_nacimiento + relativedelta(years=1)

    if e == "9" and unicaDosis == '5': #Hepatitis A

        if format(f) > str(dentro_de_anio):
            new_vacunattion = request.form.copy()
            new_vacunattion.pop("id", None) 
            Vacunattion(**new_vacunattion).save()
            flash("Se ha registrado la vacunacion exitosamente") 
            return redirect(url_for("vacunattiones.vacunattion_index"))
        else: 
            flash("Debe esperar 12 meses desde su nacimiento")                 
            return redirect(url_for("vacunattiones.vacunattion_index"))
    else:
        flash("La vacuna Hepatitis-A corresponde: Unica Dosis") 
        return redirect(url_for("vacunattiones.vacunattion_index"))

#----------------------------------------------------------------------------    
        
#------------------------------------------------------------------------------

#    Vacunattion(**new_vacunattion).save()
#    flash("Éxito en la operación")
#    return redirect(url_for("vacunattiones.vacunattion_index"))


def profile(vacunattion_id):
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    
    vacunattion = Vacunattion.get_by_id(vacunattion_id)
   
    return render_template("vacunaciones/vacunattion_profile.html", vacunattion = vacunattion)


#-------------------------------ETL--------------------------------------------

def etl():
    if not authenticated(session):
        return redirect(url_for("auth.login"))
    if not user_has_permission(session, "vacunattion_new"):  
        abort(401)

  

    resultado = MessageBox.showinfo("ETL!", "Extraccion, transformacion y carga") # título, mensaje

    #aca conectarlo a la transaccional
    
    if resultado == "ok":
    
 #LEO LOS DATOS DE LA TRANSACCIONAL

        mydb =  pymysql.connect(
        host= "localhost",
        user="root",
        password="123456",
        database = "grupo6",
        port = 3306   )


    
        cursor= mydb.cursor()
       
       #me quedo con las vacunas
        #query = "SELECT provincias.nombre_provincia, vacuna_enfermedad.nombre FROM vacunaciones inner join vacuna_enfermedad on (vacunaciones.enfermedad_id=vacuna_enfermedad.id) inner join provincias on (vacunaciones.provincia_id = provincias.id)"
        
        query = "SELECT vacunaciones.provincia_id, vacunaciones.enfermedad_id, vacunaciones.id FROM vacunaciones inner join vacuna_enfermedad on (vacunaciones.enfermedad_id=vacuna_enfermedad.id) inner join provincias on (vacunaciones.provincia_id = provincias.id)"
        

        cursor.execute(query)
        
        #VACUNACION: PROVINCIA, VACUNA, LABORATORIO, EDAD
        #for e in cursor:
        #    print(e)
        #CIERRO LA DB TRANSACCIONAL y la info queda guardada en query. AHORA DEBO INSERTAR EN EL DATAWAREHOUSE
        

#-------------------------AHORA TRANSFORMO Y CARGO LOS DATOS EN EL DATAWAREHOUSE-------------------
        connection = psycopg2.connect(
        host= "localhost",
        user="postgres",
        password="123456",
        database = "DW_vacunaciones",
        port = "5432"   )

        connection.autocommit= True    
        cursor_DW = connection.cursor() #conexion al datawarehouse en postregresql

#-------Se inserta en el data warehouse de acuerdo a la base transaccional
   
    #PARA NO TENER ELEMENTOS REPETIDOS EN EL DATAWAREHOUSE)
    #PRIMER CASO BASE:
    #obtengo cantidad de elementos en la db transaccional
    tuplas_db_transaccional = cursor.rowcount
    print("ID de la ultima tupla:", tuplas_db_transaccional)

    #obtengo cantidad de elementos en el DW
    cursor_DW.execute("select * from h_vacunados")
    tuplas_DW = cursor_DW.rowcount 
    print("ID de la ultima tupla:", tuplas_DW)

    if (tuplas_db_transaccional == tuplas_DW):
        return "no hay nuevos elementos para insertar en el DATAWAREHOUSE"
    if (tuplas_db_transaccional > tuplas_DW):
        
     

    #cursor.fetchone() devuelve la primera tupla 
    #id_tiempo y id_laboratorio NO IMPORTAN DEMSSIADO AHORA id:3: laboratorio Pfizer
        for fila in cursor:
            insert_stmt = ("INSERT INTO h_vacunados (id_lugar, id_tiempo, id_vacunado, id_vacuna, id_laboratorio) VALUES (%s, %s, %s, %s, %s)")
            data = (fila[0],2,fila[1],fila[1],3)
            cursor_DW.execute(insert_stmt, data)                   
    
        return "etl ejecutado!"
    

        
       
    

      
      
        
        
     
    cursor_DW.close() #cierro dw
    cursor.close() #cierro transaccional
            
        

    return "ETL ejecutado"

     
        

root = Tk()

Button(root, text = "ETL", command=etl).pack()

root.mainloop()   
