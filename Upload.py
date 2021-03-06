directorio = 'C:/Users/Workstation 4/PycharmProjects/TWSPythonCode'

import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import time
from datetime import date
from timeit import default_timer as timer

directorio_credenciales = 'credentials_module.json'


# iniciar sesion
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)


# Crear archivo de texto simple
def crear_archivo_texto(nombre_archivo, contenido, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'title': nombre_archivo,
                                       'parents': [{'kind': 'drive#filelink', 'id': id_folder}]})
    archivo.SetContentString(contenido)
    archivo.Upload()


# SUBIR UN ARCHIVO A DRIVE
def subir_archivo(ruta_archivo, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",
                                                    "id": id_folder}]})
    archivo['title'] = ruta_archivo.split("/")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()


# DESCARGAR UN ARCHIVO DE DRIVE POR ID
def bajar_archivo_por_id(id_drive, ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_drive})
    nombre_archivo = archivo['title']
    archivo.GetContentFile(ruta_descarga + nombre_archivo)


# BUSCAR ARCHIVOS
def busca(query):
    resultado = []
    credenciales = login()
    # Archivos con el nombre 'mooncode': title = 'mooncode'
    # Archivos que contengan 'mooncode' y 'mooncoders': title contains 'mooncode' and title contains 'mooncoders'
    # Archivos que NO contengan 'mooncode': not title contains 'mooncode'
    # Archivos que contengan 'mooncode' dentro del archivo: fullText contains 'mooncode'
    # Archivos en el basurero: trashed=true
    # Archivos que se llamen 'mooncode' y no esten en el basurero: title = 'mooncode' and trashed = false
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        # ID Drive
        print('ID Drive:', f['id'])
        resultado.append(f['id'])
        # Link de visualizacion embebido
        print('Link de visualizacion embebido:', f['embedLink'])
        resultado.append(f['embedLink'])
        # Link de descarga
        print('Link de descarga:', f['downloadUrl'])
        resultado.append(f['downloadUrl'])
        # Nombre del archivo
        print('Nombre del archivo:', f['title'])
        resultado.append(f['title'])
        # Tipo de archivo
        print('Tipo de archivo:', f['mimeType'])
        resultado.append(f['mimeType'])
        # Esta en el basurero
        print('Esta en el basurero:', f['labels']['trashed'])
        resultado.append(f['labels']['trashed'])
        # Fecha de creacion
        print('Fecha de creacion:', f['createdDate'])
        resultado.append(f['createdDate'])
        # Fecha de ultima modificacion
        print('Fecha de ultima modificacion:', f['modifiedDate'])
        resultado.append(f['modifiedDate'])
        # Version
        print('Version:', f['version'])
        resultado.append(f['version'])
        # Tamanio
        print('Tamanio:', f['fileSize'])
        resultado.append(f['fileSize'])

    return resultado


# DESCARGAR UN ARCHIVO DE DRIVE POR NOMBRE
def bajar_archivo_por_nombre(nombre_archivo, ruta_descarga):
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': "title = '" + nombre_archivo + "'"}).GetList()
    if not lista_archivos:
        print('No se encontro el archivo: ' + nombre_archivo)
    archivo = credenciales.CreateFile({'id': lista_archivos[0]['id']})
    archivo.GetContentFile(ruta_descarga + nombre_archivo)


# BORRAR/RECUPERAR ARCHIVOS
def borrar_recuperar(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    # MOVER A BASURERO
    archivo.Trash()
    # SACAR DE BASURERO
    archivo.UnTrash()
    # ELIMINAR PERMANENTEMENTE
    archivo.Delete()


# CREAR CARPETA
def crear_carpeta(nombre_carpeta, id_folder):
    credenciales = login()
    folder = credenciales.CreateFile({'title': nombre_carpeta,
                                      'mimeType': 'application/vnd.google-apps.folder',
                                      'parents': [{"kind": "drive#fileLink",
                                                   "id": id_folder}]})
    folder.Upload()


# MOVER ARCHIVO
def mover_archivo(id_archivo, id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    propiedades_ocultas = archivo['parents']
    archivo['parents'] = [{'isRoot': False,
                           'kind': 'drive#parentReference',
                           'id': id_folder,
                           'selfLink': 'https://www.googleapis.com/drive/v2/files/' + id_archivo + '/parents/' + id_folder,
                           'parentLink': 'https://www.googleapis.com/drive/v2/files/' + id_folder}]
    archivo.Upload(param={'supportsTeamDrives': True})


# ENLISTAR LOS PERMISOS ACTUALES
def enlistar_permisos_actuales(id_drive):
    drive = login()
    file1 = drive.CreateFile({'id': id_drive})
    permissions = file1.GetPermissions()
    lista_de_permisos = file1['permissions']

    for permiso in lista_de_permisos:
        # ID DEL PERMISO
        print('ID PERMISO: {}'.format(permiso['id']))
        # ROLE = owner | organizer | fileOrganizer | writer | reader
        print('ROLE: {}'.format(permiso['role']))
        # TYPE (A QUIEN SE LE COMPARTIRA LOS PERMISOS) = anyone | group | user
        print('TYPE: {}'.format(permiso['type']))

        # EMAIL
        if permiso.get('emailAddress'):
            print('EMAIL: {}'.format(permiso['emailAddress']))

        # NAME
        if permiso.get('name'):
            print('NAME: {}'.format(permiso['name']))

        print('=====================================================')


# INSERTAR/ OTORGAR PERMISOS
def insertar_permisos(id_drive, type, value, role):
    drive = login()
    file1 = drive.CreateFile({'id': id_drive})
    # VALUE (EMAIL DE A QUIEN SE LE OTORGA EL PERMISO)
    permission = file1.InsertPermission({'type': type, 'value': value, 'role': role})


# ELIMINAR PERMISOS
def eliminar_permisos(id_drive, permission_id=None, email=None):
    drive = login()
    file1 = drive.CreateFile({'id': id_drive})
    permissions = file1.GetPermissions()
    if permission_id:
        file1.DeletePermission(permission_id)
    elif email:
        for permiso in permissions:
            if permiso.get('emailAddress'):
                if permiso.get('emailAddress') == email:
                    file1.DeletePermission(permiso['id'])

if __name__ == "__main__":
    ruta_descarga = directorio
    id_folder = '188KO4gb2pSQBYND0c7sqlpNP-l9TxgFc'
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    archivo = f"{directorio}/SPXU.csv"
    nombre_nuevo = f"{directorio}/SPXU TeamViewer {d1}.csv"
    os.rename(archivo, nombre_nuevo)
    subir_archivo(nombre_nuevo, id_folder)

    print('Listo')