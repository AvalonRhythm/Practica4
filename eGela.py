# -*- coding: UTF-8 -*-
from tkinter import messagebox
import requests
import urllib
from bs4 import BeautifulSoup
import time
import helper
import getpass
import sys
import msvcrt
import os
import codecs


class eGela:
    _login = 0
    _cookie = ""
    _refs = []
    _root = None
    _cookie=-1
    _pagina="mierda" #almacena la pagina principal de egela
    _tieneSisWeb=False # variable que indica si está matriculado en sisweb

    def __init__(self, root):
        self._root = root

    ################################################################################
    # --> LOGEARSE EN EGELA CON LAS CREDENCIALES INTRODUCIDAS EN LA INTERFAZ GRAFICA
    # --> EL METODO ACTUALIZA _login=1 Y DEVUELVE LA COOKIE SI EL LOGIN ES CORRECTO
    ################################################################################
    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        try:

            tieneSisWeb = False
            # RELLENAR ESTA MIERDA CON LOS ARGUMENTOS
            ldap = username
            passwd = password

            print("######## 1. PETICION --> index de egela obtener token ########")
            metodo = 'GET'
            uri = "https://egela.ehu.eus/login/index.php"
            cabeceras = {'Host': 'egela.ehu.eus'}
            cuerpo = ''
            print(metodo + " --> " + uri)
            print(cuerpo)

            respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)
            codigo = respuesta.status_code
            descripcion = respuesta.reason
            print("\n\n++++++++ respuesta: ++++++++")
            print(str(codigo) + " " + descripcion)  # CODIGO DE RESPUESTA Y SIGNIFICADO
            for cabecera in respuesta.headers:
                if cabecera == 'Location' or cabecera == 'Set-Cookie':
                    print(cabecera + ": " + respuesta.headers[cabecera])
                    cuerpo = respuesta.content

            # OBTENER OBJETO BS DEL CUERPO DE LA RESPUESTA
            _pagina = BeautifulSoup(cuerpo, 'html.parser')

            # OBTENER LOGINTOKEN Y LA REDIRECCION DE LA SIGUIENTE PETICION
            redireccion = _pagina.find('form', class_="m-t-1 ehuloginform").get('action')
            loginToken = _pagina.find('input', {"name": "logintoken"}).get('value')

            # OBTENER LA COOKIE DE SESION DADA EN LA RESPUESTA
            cookie = respuesta.headers['Set-Cookie'].split(';')[0]  # aislar el campo de la moodlesesionegela

            #########################################################
            progress = 25
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(1)
            #########################################################


            print("##### 2. PETICION --> logeo en index (obtener testsesion) #####")
            metodo = 'POST'
            uri = redireccion
            cabeceras = {'Host': 'egela.ehu.eus',
                         'Content-Type': 'application/x-www-form-urlencoded',
                         'Cookie': cookie}
            cuerpo = {"logintoken": loginToken,
                      "username": ldap,
                      "password": passwd}

            cuerpo_encoded = urllib.parse.urlencode(cuerpo)
            cabeceras['Content-Lenght'] = str(len(cuerpo))
            print(metodo + " --> " + uri)
            print(cuerpo)

            respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)
            codigo = respuesta.status_code
            descripcion = respuesta.reason
            print("\n\n++++++++ respuesta: ++++++++")
            print(str(codigo) + " " + descripcion)
            for cabecera in respuesta.headers:
                if cabecera == 'Location' or cabecera == 'Set-Cookie':
                    print(cabecera + ": " + respuesta.headers[cabecera])
            cuerpo = respuesta.content

            # OBTENER URI+TESTSESSION DE LA SIGUIENTE CONSULTA Y LA NUEVA COOKIE
            uri_testsesion = respuesta.headers['Location']
            cookie = respuesta.headers['Set-Cookie'].split(';')[0]  # obtener la cookie

            #########################################################
            progress = 50
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(1)
            #########################################################


            print("\n##### 3. PETICION --> obtener la pagina principal #####")
            metodo = 'GET'
            uri = uri_testsesion
            cabeceras = {'Host': 'egela.ehu.eus',
                         'Cookie': cookie}
            cuerpo = ''
            print(metodo + " --> " + uri)
            print(cuerpo)

            respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)
            codigo = respuesta.status_code
            descripcion = respuesta.reason
            print("\n\n++++++++ respuesta: ++++++++")
            print(str(codigo) + " " + descripcion)
            for cabecera in respuesta.headers:
                if cabecera == 'Location' or cabecera == 'Set-Cookie':
                    print(cabecera + ": " + respuesta.headers[cabecera])
            cuerpo = respuesta.content
            # print(cuerpo)

            paginaPrincipal = respuesta.headers[
                'Location']  # si se ha iniciado bien la sesion nos redirige a nuestra pagina principal de egela

            #########################################################
            progress = 75
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(1)
            #########################################################

            print("\n##### 4. PETICION --> conectarse a la pagina principal de egela #####")
            metodo = 'GET'
            uri = paginaPrincipal
            cabeceras = {'Host': 'egela.ehu.eus',
                         'Cookie': cookie}
            cuerpo = ''
            print(metodo + " --> " + uri)
            print(cuerpo)

            respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)
            codigo = respuesta.status_code
            descripcion = respuesta.reason
            print("\n\n++++++++ respuesta: ++++++++")
            print(str(codigo) + " " + descripcion)
            for cabecera in respuesta.headers:
                if cabecera == 'Location' or cabecera == 'Set-Cookie':
                    print(cabecera + ": " + respuesta.headers[cabecera])
            cuerpo = str(respuesta.content)
            # print(cuerpo)

            #########################################################
            progress = 100
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(1)
            popup.destroy()
            #########################################################

            #COMPROBAR DATOS DEL LOGIN
            _pagina = BeautifulSoup(cuerpo, 'html.parser')
            messagebox.showinfo("INFORMACIÓN", "\n Autenticado como: " + str(_pagina.find('span', class_="usertext mr-1").text))

            # ACTUALIZAR LAS VARIABLES
            self._login = 1
            _login=1
            self._cookie = cookie
            _cookie=1
            self._root.destroy()

        except:
            messagebox.showinfo("Alert Message", "Login incorrect!")

        print(_login)
        return _pagina

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()
        print(_pagina)

        #HAY QUE AÑADIR LA ULTIMA PAGINA DE EGELA

        print("\n --- Estos son los cursos actuales de " + str(_pagina.find('span', class_="usertext mr-1").text)  + " ---")
        for h3 in _pagina.find_all("h3", class_="coursename"):  # OBTENER TODOS LOS CAMPOS coursename DE EGELA
            a = h3.find("a")  # EXTRAER LA CLAUSULA <a></a>
            nombreCurso = a.getText()
            link = a["href"]
            print("Nombre curso : " + nombreCurso + " --> " + link)

            if nombreCurso == "Sistemas Web":
                tieneSisWeb=True
                cursoSisWeb=link

        messagebox.showinfo("INFORMACIÓN", "SE VAN A DESCARGAR TODOS LOS PDFs DE LA ASIGNATURA 'SISTEMAS WEB'")


        if tieneSisWeb==True: #si el alumno etá matriculado --> se descargan los pdfs

            print("\n##### 5. PETICION --> acceder al curso de sistemas web #####")
            metodo = 'GET'
            uri = cursoSisWeb
            cabeceras = {'Host': 'egela.ehu.eus',
                         'Cookie': _cookie}
            cuerpo = ''
            print(metodo + " --> " + uri)
            print(cuerpo)

            respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)
            codigo = respuesta.status_code
            descripcion = respuesta.reason
            print("\n\n++++++++ respuesta: ++++++++")
            print(str(codigo) + " " + descripcion)
            for cabecera in respuesta.headers:
                if cabecera == 'Location' or cabecera == 'Set-Cookie':
                    print(cabecera + ": " + respuesta.headers[cabecera])
            cuerpo = respuesta.content
            # print(cuerpo)


            #--> CALCULAR EL NUMERO DE PDFS QUE HAY EN SISTEMAS WEB
            numeroDePDFs=0
            SisWebContent = BeautifulSoup(cuerpo, 'html.parser')  # OBTIENE EL OBJETO BS

            for div in SisWebContent.find_all("div", class_="activityinstance"): #RECORRER LAS ACTIVIDADES DE LA ASIGNATURA
                img = div.find("img").attrs['src']  # EXTRAER EL ICONO DE LA ACTIVIDAD

                if "pdf" in img:  # SI EL ICONO DE LA ACTIVIDAD CONTIENE LA PALABRA PDF --> EL ARCHIVO ES UN PDF
                    #ACTUALIZAMOS EL CONADOR DE PDFs
                    numeroDePDFs = numeroDePDFs+1

            progress=0
            progress_var.set(progress) #inicializar la barra de progreso a 0
            progress_step = float(100.0 / len(numeroDePDFs)) #calcular lo que sube la barra por cada pdf descargado


            # --> OBTENER EL PAR DE (nombrePDF, enlacePDF):
            SisWebContent = BeautifulSoup(cuerpo, 'html.parser') # OBTIENE EL OBJETO BS

            for div in SisWebContent.find_all("div", class_="activityinstance"):
                img = div.find("img").attrs['src']  # EXTRAER LA EL ICONO DE LA ACTIVIDAD
                pdf = div.find("a")["href"]  # EXTRAER EL LINK DE LA CLAUSULA <a></a>

                #OBTENER EL NOMBRE DEL PDF PARA GUARDAR PERO SIN LA ULTIMA PALABRA 'fitxategia'
                nomPDF = str(div.find("span", class_="instancename").text).rsplit(' ',1)[0]

                if "pdf" in img: #SI EL ICONO DE LA ACTIVIDAD CONTIENE LA PALABRA PDF --> EL ARCHIVO ES UN PDF

                    if "/" in nomPDF:  #QUITAR LAS '/' DE LOS NOMBRES QUE HACEN CONFLICTO CON EL DIRECTORIO
                        nomPDF=nomPDF.replace("/","-")

                        nuevoPDF = {"pdf_name": nomPDF,
                                   "pdf_link": pdf}

                        self._refs.append(nuevoPDF) #AÑADIR A LA LISTA EL NUEVO PDF

                        # INICIALIZA Y ACTUALIZAR BARRA DE PROGRESO
                        # POR CADA PDF ANIADIDO EN self._refs
                        progress += progress_step
                        progress_var.set(progress)
                        progress_bar.update()
                        time.sleep(0.1)

        else:
            messagebox.showinfo("INFORMACIÓN", "NO ESTÁS MATRICULADO EN 'SISTEMAS WEB'")

        popup.destroy()
        print(self._refs)
        return self._refs

'''
    def get_pdf(self, selection):

        print("\t##### descargando  PDF... #####")
        print("\n##### 5. PETICION --> obtener el pdf #####")
        metodo = 'GET'
        uri = pdf
        cabeceras = {'Host': 'egela.ehu.eus',
                     'Cookie': cookie}
        cuerpo = ''
        print(metodo + " --> " + uri)
        print(cuerpo)

        respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)
        codigo = respuesta.status_code
        descripcion = respuesta.reason
        print("\n\n++++++++ respuesta: ++++++++")
        print(str(codigo) + " " + descripcion)
        for cabecera in respuesta.headers:
            if cabecera == 'Location' or cabecera == 'Set-Cookie':
                print(cabecera + ": " + respuesta.headers[cabecera])
        cuerpo = respuesta.content
        # print(cuerpo)



        # Peticion 7 (redireccionamiento --> obtener cada pdf)
        print("\n\n--------------------------- PETICION 7 -----------------------------")
        metodo = 'GET'
        uri = respuesta.headers['Location']
        cabeceras = {'Host': 'egela.ehu.eus',
                     'Cookie': cookie}
        cuerpo = ''
        print(metodo + " --> " + uri)
        print(cuerpo)

        respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo,
                                     allow_redirects=False)
        codigo = respuesta.status_code
        descripcion = respuesta.reason
        print("\n\n++++++++ respuesta: ++++++++")
        print(str(codigo) + " " + descripcion)
        for cabecera in respuesta.headers:
            if cabecera=='Location' or cabecera=='Set-Cookie':
                print(cabecera + ": " + respuesta.headers[cabecera])
        cuerpo = respuesta.content
        # print(cuerpo)

        return pdf_name, pdf_content
'''