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

        '''
        en check credentials se meten texto
        y hay que leer del intergace
        username.get(valor)
        '''

        #RELLENAR ESTA MIERDA CON LOS ARGUMENTOS
        ldap = sys.argv[1]
        nom = sys.argv[2].split(' ')[0].lower()  # OBTENER NOMBRE EN MINUSCULAS
        apel = sys.argv[2].split(' ')[1].lower()  # OBTENER APELL EN MINUSCULAS
        passwd = getpass.getpass(prompt="introduzca la contraseña para el usuario '" + ldap + "' : ")
        tieneSisWeb = False




        print("######## 1. PETICION ########")
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
        pagina = BeautifulSoup(cuerpo, 'html.parser')

        # OBTENER LOGINTOKEN Y LA REDIRECCION DE LA SIGUIENTE PETICION
        redireccion = pagina.find('form', class_="m-t-1 ehuloginform").get('action')
        loginToken = pagina.find('input', {"name": "logintoken"}).get('value')

        # OBTENER LA COOKIE DE SESION DADA EN LA RESPUESTA
        cookie = respuesta.headers['Set-Cookie'].split(';')[0]  # aislar el campo de la moodlesesionegela

        #########################################################
        progress = 25
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)
        #########################################################




        print("##### 2. PETICION #####")
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



        print("\n##### 3. PETICION #####")
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




        print("\n##### 4. PETICION #####")
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


        if nom in cuerpo.lower() and apel in cuerpo.lower():

            pagina = BeautifulSoup(cuerpo, 'html.parser')
            print("\n --- Autenticacion correcta como --> " + str(
                pagina.find('span', class_="usertext mr-1").text) + " ---")
            print("\n Pulse cualquier tecla para continuar...")
            msvcrt.getch()  # ESPERA HASTA QUE EL USER PULSE TECLA

            #ACTUALIZAR LAS VARIABLES
            _login = 1
            _cookie = cookie
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")


'''
    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. PETICION (Página principal de la asignatura en eGela) #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        progress_step = float(100.0 / len(NUMERO DE PDF_EN_EGELA))


        print("\n##### Analisis del HTML... #####")
        #############################################
        # ANALISIS DE LA PAGINA DEL AULA EN EGELA
        # PARA BUSCAR PDFs
        #############################################

        # INICIALIZA Y ACTUALIZAR BARRA DE PROGRESO
        # POR CADA PDF ANIADIDO EN self._refs
         progress_step = float(100.0 / NUMERO_DE_PDFs_EN_EGELA)


                progress += progress_step
                progress_var.set(progress)
                progress_bar.update()
                time.sleep(0.1)

        popup.destroy()
        return self._refs

    def get_pdf(self, selection):

        print("\t##### descargando  PDF... #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        return pdf_name, pdf_content
'''