import json
import pandas as pd
import os 
import platform
from copy import deepcopy
import re

"""
def get_nombre_archivo(cadena):
    resultado = re.search(r'/(.+)\.json$', cadena)

    if resultado:
        texto_extraido = resultado.group(1)
        return texto_extraido
    else:
        print("No se encontró ninguna coincidencia.")    

"""
def borrar_archivo_json_auxiliar(ruta):
    if os.path.exists(ruta):
        os.remove(ruta)
        print(f'El archivo "{ruta}" ha sido eliminado.')
    else:
        print(f'El archivo "{ruta}" no existe.')    

def get_nombre_archivo(cadena):
    # Obtener el nombre del archivo sin extensión
    nombre_archivo_sin_extension = os.path.splitext(os.path.basename(cadena))[0]    
    return nombre_archivo_sin_extension



def limpiar_pantalla():
    os.system('cls') if platform.system() == 'Windows' else os.system('clear')


def listar_archivos_json(carpetapath):
    archivos_json = []
    # Obtener la lista de archivos en la carpeta
    archivos_en_carpeta = os.listdir(carpetapath)
    # Filtrar archivos que tengan la extensión .json
    archivos_json = [archivo for archivo in archivos_en_carpeta if archivo.endswith(".json")]
    return archivos_json


def mostrar_archivos(archivos_json_en_carpeta):
    for indice, archivo in enumerate(archivos_json_en_carpeta):
        print(f"[{indice}] - {archivo}")



def elegir_archivo(archivos_json):
    limpiar_pantalla()
    while True:
        print("elegir archivo json a transformar:")        
        print("")                
        mostrar_archivos(archivos_json)        
        opcion = input("> ")
        if int(opcion) in range(0,len(archivos_json)):
            return archivos_json[int(opcion)]
                
       
def get_json(path):
    file = open(path, encoding="UTF-8")
    data = json.load(file)
    file.close()
    return data


def process_operations(node, operations):
    children = []
    for operation in operations:
        if operation["operation"] == "move_topics" and operation["parentLabel"] == node:
            children = [{"name": child, "children": process_operations(child, operations)}
                        for child in operation["childLabels"]]
    return children


def tags_to_json(archivo_a_transformar):
    with open(archivo_a_transformar, encoding="UTF-8") as file:
        data = json.load(file)

    lista = []
    for node in data['rootNodes']:
        ddict = {"name": node, "children": process_operations(node, data["operations"])}
        lista.append(ddict)        
    nombre_archivo = get_nombre_archivo(archivo_a_transformar)  
    archivo_json_jerarquizado = nombre_archivo + '_jerarquia.json'  
    with open(archivo_json_jerarquizado, 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)
    return nombre_archivo


def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for item in data:
                [rows.append(elem) for elem in flatten_list(flatten_json(item, prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pd.DataFrame(flatten_json(data_in))

def df_to_csv(df,filename):
        columns_name = ['nivel ' + str(i) for i in range(1, len(df.axes[1]) + 1)]
        df.columns = columns_name
        df.to_csv(f'{filename}.csv', encoding="utf_8_sig", sep=';', index=False)
        

if __name__ == '__main__':
    # TODO listar archivos en la carpeta
    carpeta_path_json = "./Json"
    carpeta_path_csv = "./csv"
    archivos_json_en_carpeta = listar_archivos_json(carpeta_path_json)
    archivo_elegido = elegir_archivo(archivos_json_en_carpeta)
    #archivo_elegido_nombre = archivo_elegido.split('.json')[0]
    archivo_a_transformar = carpeta_path_json + "/" + archivo_elegido    

    #tags_to_json(archivo_a_transformar)
    try:
        nombre_archivo = tags_to_json(archivo_a_transformar)
        json_data = get_json(nombre_archivo + '_jerarquia.json')
        df = json_to_dataframe(json_data)
        archivo_a_guardar = carpeta_path_csv + "/" + nombre_archivo
        df_to_csv(df, archivo_a_guardar)
        borrar_archivo_json_auxiliar(nombre_archivo + '_jerarquia.json')
    except PermissionError:
        print("error de permisos. ¿el archivo esta abierto?")
    except FileNotFoundError:
        print("no se encontro el archivo")
    except Exception as e:
        print(f"error inesperado " + str(e))



