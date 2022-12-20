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
from app.models.patient import Patient
from app.models.rol import Rol
import re
from tkinter import *
from tkinter import messagebox as MessageBox
from datetime import date

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
    
    vacuna = VaccineEnfermedad.get_by_id(enfermedad_id)
    vacuna = vacuna.nombre
    provincias = Province.get_all_provincias()

    #CADA VEZ QUE HAGO UNA VACUNACION DEBO DISMINUIR (antes de mandar tot calclulo cuantas vacunaciones tiene y las resto) 

    
    vacunattiones = Vacunattion.get_vacunattiones_by_enfermedad(enfermedad_id)
    cant = len(vacunattiones)

    return render_template(
        "vacunaciones/vacunattion_index.html",
        vacunattiones= vacunattiones,
        tot = tot - cant,
        distributtiones = distributtiones,
        enfermedades= enfermedades,
        vacuna= vacuna,
        provincias= provincias,
    )


def sumar_cantidades (distributtiones):
    suma = 0
    
    for numero in distributtiones:
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
    tot = sumar_cantidades(distributtiones) - len(vacunattiones)
    
    if (tot == 0):
        flash("No hay stock para realizar la vacunacion de esa vacuna")
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

    
    
    if resultado == "ok":

        connection = psycopg2.connect(
        host= "localhost",
        user="postgres",
        password="123456",
        database = "etapa 2",
        port = "5432"   )

        connection.autocommit= True
            
        cursor = connection.cursor()
    

       
        
        query = ( """SELECT vacunaciones.id_provincia, vacunaciones.id_laboratorio, vacunaciones.id_paciente, vacunaciones.id_vacuna
         FROM public.vacunaciones  """)

        cursor.execute(query)
        
        for fila in cursor:
            lugar = fila[0]
            vacunado = fila[3]
            vacuna = fila[2] 
            laboratorio = fila[1]           
     
        cursor.close() #CIERRO LA DB TRANSACCIONAL

#-------------------------AHORA TRANSFORMO Y CARGO LOS DATOS EN EL DATAWAREHOUSE-------------------
        connection = psycopg2.connect(
        host= "localhost",
        user="postgres",
        password="123456",
        database = "DW_vacunaciones",
        port = "5432"   )

        connection.autocommit= True    
        cursor_DW = connection.cursor() #conexion al datawarehouse en postregresql

            
        
       
#Se inserta en el data warehouse de acuerdo a la base transaccional
    for i in range(10):
        insert_stmt = ("INSERT INTO h_vacunados (id_lugar, id_tiempo, id_vacunado, id_vacuna, id_laboratorio) VALUES (%s, %s, %s, %s, %s)")
        data = (lugar,1,vacunado,1,laboratorio)
        cursor_DW.execute(insert_stmt, data)
        lugar= lugar -1 
        vacunado= vacunado +1
        cursor_DW.execute(insert_stmt, data)
        
     
    cursor_DW.close()
    return "ETL ejecutado"
    
    
        

     
        

root = Tk()

Button(root, text = "ETL", command=etl).pack()

root.mainloop()   
    


