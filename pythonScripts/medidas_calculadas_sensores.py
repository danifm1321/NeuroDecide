import re
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

#sensores = [sys.argv[1]]
sensores = json.loads(sys.argv[1])
milisegundos = sys.argv[2]
normalizar = (sys.argv[3] == 'true')
museDataPath = sys.argv[4]

json_final = {}
dataframes_a_concatenar = []

url_csv = 'pythonScripts/medidasCalculadas/medidasCalculadasSensores.csv'

decisiones = ["p", "q"]

columnas_a_modificar = [
    'ultima_modificacion',
    'raw_minimo',
    'raw_maximo',
    'raw_cuartil1',
    'raw_cuartil2',
    'raw_cuartil3',
    'alpha_minimo',
    'alpha_maximo',
    'alpha_cuartil1',
    'alpha_cuartil2',
    'alpha_cuartil3',
    'beta_minimo',
    'beta_maximo',
    'beta_cuartil1',
    'beta_cuartil2',
    'beta_cuartil3',
    'delta_minimo',
    'delta_maximo',
    'delta_cuartil1',
    'delta_cuartil2',
    'delta_cuartil3',
    'theta_minimo',
    'theta_maximo',
    'theta_cuartil1',
    'theta_cuartil2',
    'theta_cuartil3',
    'gamma_minimo',
    'gamma_maximo',
    'gamma_cuartil1',
    'gamma_cuartil2',
    'gamma_cuartil3',
]


# Obtener la lista de archivos en la carpeta
archivos = os.listdir('data')

# Inicializar la variable para almacenar la fecha más reciente
fecha_mas_reciente = 0

# Recorrer todos los archivos y obtener la fecha de modificación más reciente
for archivo in archivos:
    ruta_archivo = os.path.join('data', archivo)
    fecha_modificacion = os.stat(ruta_archivo).st_mtime
    if fecha_modificacion > fecha_mas_reciente:
        fecha_mas_reciente = fecha_modificacion

# Convertir la fecha más reciente a un formato legible
fecha_legible = datetime.fromtimestamp(fecha_mas_reciente).strftime('%Y-%m-%d %H:%M:%S')

pre_decision_obtenidos = []

def rellenar_json(row):
    if row['post-decision'] == True:
        text = 'Post-decisión'
    else:
        text = 'Pre-decisión'
        pre_decision_obtenidos.append(row['sensor'])

    valores = {
        "minimo" : row['raw_minimo'], 
        "maximo" : row['raw_maximo'], 
        "cuartil1" : row['raw_cuartil1'], 
        "cuartil2" : row['raw_cuartil2'], 
        "cuartil3" : row['raw_cuartil3']
    }

    valores_finales_raw.setdefault(row['sensor'], {})[text + ' para ' + row['decision']] = valores

    valores = {
        "minimo" : row['beta_minimo'], 
        "maximo" : row['beta_maximo'], 
        "cuartil1" : row['beta_cuartil1'], 
        "cuartil2" : row['beta_cuartil2'], 
        "cuartil3" : row['beta_cuartil3']
    }

    valores_finales_beta.setdefault(row['sensor'], {})[text + ' para ' + row['decision']] = valores
    
    valores = {
        "minimo" : row['delta_minimo'], 
        "maximo" : row['delta_maximo'], 
        "cuartil1" : row['delta_cuartil1'], 
        "cuartil2" : row['delta_cuartil2'], 
        "cuartil3" : row['delta_cuartil3']
    }

    valores_finales_delta.setdefault(row['sensor'], {})[text + ' para ' + row['decision']] = valores

    valores = {
        "minimo" : row['theta_minimo'], 
        "maximo" : row['theta_maximo'], 
        "cuartil1" : row['theta_cuartil1'], 
        "cuartil2" : row['theta_cuartil2'], 
        "cuartil3" : row['theta_cuartil3']
    }

    valores_finales_theta.setdefault(row['sensor'], {})[text + ' para ' + row['decision']] = valores

    valores = {
        "minimo" : row['gamma_minimo'], 
        "maximo" : row['gamma_maximo'], 
        "cuartil1" : row['gamma_cuartil1'], 
        "cuartil2" : row['gamma_cuartil2'], 
        "cuartil3" : row['gamma_cuartil3']
    }

    valores_finales_gamma.setdefault(row['sensor'], {})[text + ' para ' + row['decision']] = valores

    valores = {
        "minimo" : row['alpha_minimo'], 
        "maximo" : row['alpha_maximo'], 
        "cuartil1" : row['alpha_cuartil1'], 
        "cuartil2" : row['alpha_cuartil2'], 
        "cuartil3" : row['alpha_cuartil3']
    }

    valores_finales_alpha.setdefault(row['sensor'], {})[text + ' para ' + row['decision']] = valores

if os.path.isfile(url_csv):
    valores_finales_raw = {}
    valores_finales_beta = {}
    valores_finales_theta = {}
    valores_finales_gamma = {}
    valores_finales_alpha = {}
    valores_finales_delta = {}

    dataframe_csv = pd.read_csv(url_csv)

    for index, row in dataframe_csv.iterrows():
        if fecha_legible == row['ultima_modificacion']:

            if str(row['sensor']) in sensores and row['normalizado'] == normalizar and (row['milisegundos'] == 0 or row['milisegundos'] == int(milisegundos)):
                rellenar_json(row)

                json_final[row['sensor']] = {
                    "alpha" : valores_finales_alpha[row['sensor']],
                    "beta" : valores_finales_beta[row['sensor']],
                    "delta" : valores_finales_delta[row['sensor']],
                    "theta" : valores_finales_theta[row['sensor']],
                    "gamma" : valores_finales_gamma[row['sensor']],
                    "raw" : valores_finales_raw[row['sensor']]
                }
else:
    estructura_csv = {
        'sensor' : [],
        'post-decision' : [],
        'normalizado' : [],
        'milisegundos' : [],
        'decision' : [],
        'ultima_modificacion' : [],
        'raw_minimo' : [],
        'raw_maximo' : [],
        'raw_cuartil1' : [],
        'raw_cuartil2' : [],
        'raw_cuartil3' : [],
        'alpha_minimo' : [],
        'alpha_maximo' : [],
        'alpha_cuartil1' : [],
        'alpha_cuartil2' : [],
        'alpha_cuartil3' : [],
        'beta_minimo' : [],
        'beta_maximo' : [],
        'beta_cuartil1' : [],
        'beta_cuartil2' : [],
        'beta_cuartil3' : [],
        'delta_minimo' : [],
        'delta_maximo' : [],
        'delta_cuartil1' : [],
        'delta_cuartil2' : [],
        'delta_cuartil3' : [],
        'theta_minimo' : [],
        'theta_maximo' : [],
        'theta_cuartil1' : [],
        'theta_cuartil2' : [],
        'theta_cuartil3' : [],
        'gamma_minimo' : [],
        'gamma_maximo' : [],
        'gamma_cuartil1' : [],
        'gamma_cuartil2' : [],
        'gamma_cuartil3' : [],
    }

    dataframe_csv = pd.DataFrame(estructura_csv)
    dataframe_csv.to_csv(url_csv, index=False)

nuevos_sensores = []

for sensor in sensores:
    if not (sensor in pre_decision_obtenidos):
        nuevos_sensores.append(sensor)

sensores = nuevos_sensores

dataframe_csv = pd.read_csv(url_csv)

def get_limites_de_tiempo(dataframe):
    dataframe = dataframe.drop(columns=['ID del participante', 'Respuesta', 'Tiempo de inicio', 'Tiempo de aparición de letras', 'Letra observada'])

    for index, row in dataframe.iloc[1:].iterrows():
        tiempo_impulso = datetime.strptime(row['Tiempo de aparición de la letra observada'], '%Y-%m-%d %H:%M:%S.%f')
        tiempo_pulsacion = datetime.strptime(row['Tiempo de la pulsación'], '%Y-%m-%d %H:%M:%S.%f')
        tiempo_pre_decision = tiempo_impulso - timedelta(milliseconds=int(milisegundos))
        tiempo_post_decision = tiempo_pulsacion + timedelta(milliseconds=500)

        if row['Tecla elegida'] == 'p':
            limites_de_tiempo_predecision_p.append({
                "Tiempo impulso" : tiempo_impulso.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "Tiempo pre-decision" : tiempo_pre_decision.strftime('%Y-%m-%d %H:%M:%S.%f')
            })

            limites_de_tiempo_postdecision_p.append({
                "Tiempo impulso" : tiempo_impulso.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "Tiempo post-decision" : tiempo_post_decision.strftime('%Y-%m-%d %H:%M:%S.%f')
            })
        else:
            limites_de_tiempo_predecision_q.append({
                "Tiempo impulso" : tiempo_impulso.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "Tiempo pre-decision" : tiempo_pre_decision.strftime('%Y-%m-%d %H:%M:%S.%f')
            })

            limites_de_tiempo_postdecision_q.append({
                "Tiempo impulso" : tiempo_impulso.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "Tiempo post-decision" : tiempo_post_decision.strftime('%Y-%m-%d %H:%M:%S.%f')
            }) 

def get_datos(dataframe):
    dataframe = dataframe.drop(columns=['AUX_RIGHT', 'Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'HeadBandOn', 'HSI_TP9', 'HSI_AF7', 'HSI_AF8', 'HSI_TP10', 'Battery', 'Elements'])
    #dataframe = dataframe.drop(dataframe[(dataframe['TimeStamp'] < limites_de_tiempo_predecision[0]['Tiempo impulso']) or (dataframe['TimeStamp'] > limites_de_tiempo_postdecision[len(limites_de_tiempo_postdecision)-1]['Tiempo post-decision'])].index)
    posibles_sensores = ['Alpha_AF7', 'Alpha_TP10', 'Alpha_TP9', 'Alpha_AF8', 'Beta_AF7', 'Beta_TP10', 'Beta_TP9', 'Beta_AF8', 'Delta_AF7', 'Delta_TP10', 'Delta_TP9', 'Delta_AF8', 'Theta_AF7', 'Theta_TP10', 'Theta_TP9', 'Theta_AF8', 'Gamma_AF7', 'Gamma_TP10', 'Gamma_TP9', 'Gamma_AF8', 'RAW_AF7', 'RAW_TP10', 'RAW_TP9', 'RAW_AF8']
    
    for sensor in sensores:
        posibles_sensores = [elemento for elemento in posibles_sensores if not elemento.endswith(sensor)]
    dataframe = dataframe.drop(columns=posibles_sensores)

    #dataframe = dataframe.drop(dataframe[dataframe['TimeStamp'] < limites_de_tiempo_predecision[0]['Tiempo impulso']].index)
    #dataframe = dataframe.drop(dataframe[dataframe['TimeStamp'] > limites_de_tiempo_postdecision[len(limites_de_tiempo_postdecision)-1]['Tiempo post-decision']].index)


    indice_pre_decision_p = 0
    indice_pre_decision_q = 0
    indice_post_decision_p = 0
    indice_post_decision_q = 0

    for index, row in dataframe.iloc[1:].iterrows():
        if row['TimeStamp'] <= limites_de_tiempo_predecision_p[indice_pre_decision_p]['Tiempo impulso'] and row['TimeStamp'] >= limites_de_tiempo_predecision_p[indice_pre_decision_p]['Tiempo pre-decision']:
            for sensor in sensores:
                datos_predecision_alpha[sensor]['p'].append(row['Alpha_' + sensor])
                datos_predecision_delta[sensor]['p'].append(row['Delta_' + sensor])
                datos_predecision_theta[sensor]['p'].append(row['Theta_' + sensor])
                datos_predecision_beta[sensor]['p'].append(row['Beta_' + sensor])
                datos_predecision_gamma[sensor]['p'].append(row['Gamma_' + sensor])
                datos_predecision_raw[sensor]['p'].append(row['RAW_' + sensor])
        elif row['TimeStamp'] > limites_de_tiempo_predecision_p[indice_pre_decision_p]['Tiempo impulso'] and indice_pre_decision_p < len(limites_de_tiempo_predecision_p)-2:
            indice_pre_decision_p += 1

        if row['TimeStamp'] <= limites_de_tiempo_predecision_q[indice_pre_decision_q]['Tiempo impulso'] and row['TimeStamp'] >= limites_de_tiempo_predecision_q[indice_pre_decision_q]['Tiempo pre-decision']:
            for sensor in sensores:
                datos_predecision_alpha[sensor]['q'].append(row['Alpha_' + sensor])
                datos_predecision_delta[sensor]['q'].append(row['Delta_' + sensor])
                datos_predecision_theta[sensor]['q'].append(row['Theta_' + sensor])
                datos_predecision_beta[sensor]['q'].append(row['Beta_' + sensor])
                datos_predecision_gamma[sensor]['q'].append(row['Gamma_' + sensor])
                datos_predecision_raw[sensor]['q'].append(row['RAW_' + sensor])
        elif row['TimeStamp'] > limites_de_tiempo_predecision_q[indice_pre_decision_q]['Tiempo impulso'] and indice_pre_decision_q < len(limites_de_tiempo_predecision_q)-2:
            indice_pre_decision_q += 1

        if row['TimeStamp'] <= limites_de_tiempo_postdecision_p[indice_post_decision_p]['Tiempo post-decision'] and row['TimeStamp'] >= limites_de_tiempo_postdecision_p[indice_post_decision_p]['Tiempo impulso']:
            for sensor in sensores:
                datos_postdecision_alpha[sensor]['p'].append(row['Alpha_' + sensor])
                datos_postdecision_delta[sensor]['p'].append(row['Delta_' + sensor])
                datos_postdecision_theta[sensor]['p'].append(row['Theta_' + sensor])
                datos_postdecision_beta[sensor]['p'].append(row['Beta_' + sensor])
                datos_postdecision_gamma[sensor]['p'].append(row['Gamma_' + sensor])
                datos_postdecision_raw[sensor]['p'].append(row['RAW_' + sensor])
        elif row['TimeStamp'] > limites_de_tiempo_postdecision_p[indice_post_decision_p]['Tiempo post-decision'] and indice_post_decision_p < len(limites_de_tiempo_postdecision_p)-2:
            indice_post_decision_p += 1

        if row['TimeStamp'] <= limites_de_tiempo_postdecision_q[indice_post_decision_q]['Tiempo post-decision'] and row['TimeStamp'] >= limites_de_tiempo_postdecision_q[indice_post_decision_q]['Tiempo impulso']:
            for sensor in sensores:
                datos_postdecision_alpha[sensor]['q'].append(row['Alpha_' + sensor])
                datos_postdecision_delta[sensor]['q'].append(row['Delta_' + sensor])
                datos_postdecision_theta[sensor]['q'].append(row['Theta_' + sensor])
                datos_postdecision_beta[sensor]['q'].append(row['Beta_' + sensor])
                datos_postdecision_gamma[sensor]['q'].append(row['Gamma_' + sensor])
                datos_postdecision_raw[sensor]['q'].append(row['RAW_' + sensor])
        elif row['TimeStamp'] > limites_de_tiempo_postdecision_q[indice_post_decision_q]['Tiempo post-decision'] and indice_post_decision_q < len(limites_de_tiempo_postdecision_q)-2:
            indice_post_decision_q += 1

def get_valores_finales(array):
    
    array = np.where(np.isinf(array), np.nan, array)
    array = array[~np.isnan(array)]

    minimo = np.min(array)
    maximo = np.max(array)

    if normalizar:
        array = [normalize(val, maximo, minimo) for val in array]
        minimo = np.min(array)
        maximo = np.max(array)
        q1 = np.percentile(array, 25)
        mediana = np.median(array)
        q3 = np.percentile(array, 75)
    else:
        q1 = np.percentile(array, 25)
        mediana = np.median(array)
        q3 = np.percentile(array, 75)

    estructura = {"minimo" : minimo, "maximo" : maximo, "cuartil1" : q1, "cuartil2" : mediana, "cuartil3" : q3}

    return estructura

def normalize(val, max_val, min_val):
    return (val - min_val) / (max_val - min_val) * 2 - 1


limites_de_tiempo_predecision_p = []
limites_de_tiempo_predecision_q = []
limites_de_tiempo_postdecision_p = []
limites_de_tiempo_postdecision_q = []

datos_predecision_delta = {}
datos_predecision_theta = {}
datos_predecision_alpha = {}
datos_predecision_beta = {}
datos_predecision_gamma = {}
datos_predecision_raw = {}

datos_postdecision_delta = {}
datos_postdecision_theta = {}
datos_postdecision_alpha = {}
datos_postdecision_beta = {}
datos_postdecision_gamma = {}
datos_postdecision_raw = {}

for sensor in sensores:
    for decision in decisiones:
        datos_predecision_delta.setdefault(sensor, {})[decision] = []
        datos_predecision_theta.setdefault(sensor, {})[decision] = []
        datos_predecision_alpha.setdefault(sensor, {})[decision] = []
        datos_predecision_beta.setdefault(sensor, {})[decision] = []
        datos_predecision_gamma.setdefault(sensor, {})[decision] = []
        datos_predecision_raw.setdefault(sensor, {})[decision] = []

        datos_postdecision_delta.setdefault(sensor, {})[decision] = []
        datos_postdecision_theta.setdefault(sensor, {})[decision] = []
        datos_postdecision_alpha.setdefault(sensor, {})[decision] = []
        datos_postdecision_beta.setdefault(sensor, {})[decision] = []
        datos_postdecision_gamma.setdefault(sensor, {})[decision] = []
        datos_postdecision_raw.setdefault(sensor, {})[decision] = []



archivos_csv = os.listdir("data")

archivos_csv_structure = re.compile(r'^results\d+\.csv$')

archivos_csv = [filename for filename in archivos_csv if archivos_csv_structure.match(filename)]
#archivos_csv = archivos_csv[0:2]

if sensores != []:
    for archivo in archivos_csv:
        participante = archivo.split(".")[0].split("results")[1]
        if int(participante) >= 0:
            dataframe_local = pd.read_csv('data/' + archivo)
            get_limites_de_tiempo(dataframe_local)
            if os.path.isfile(museDataPath + '/museData' + participante + '.csv'):
                dataframe_muse = pd.read_csv(museDataPath + '/museData' + participante + '.csv', low_memory=False)
                get_datos(dataframe_muse)
                limites_de_tiempo_predecision_p = []
                limites_de_tiempo_predecision_q = []
                limites_de_tiempo_postdecision_p = []
                limites_de_tiempo_postdecision_q = []

for sensor in sensores:
    for decision in decisiones:
        valores_finales_alpha["Pre-decisión para " + decision] = get_valores_finales(datos_predecision_alpha[sensor][decision])
        valores_finales_alpha["Post-decisión para " + decision] = get_valores_finales(datos_postdecision_alpha[sensor][decision])
        valores_finales_beta["Pre-decisión para " + decision] = get_valores_finales(datos_predecision_beta[sensor][decision])
        valores_finales_beta["Post-decisión para " + decision] = get_valores_finales(datos_postdecision_beta[sensor][decision])
        valores_finales_delta["Pre-decisión para " + decision] = get_valores_finales(datos_predecision_delta[sensor][decision])
        valores_finales_delta["Post-decisión para " + decision] = get_valores_finales(datos_postdecision_delta[sensor][decision])
        valores_finales_theta["Pre-decisión para " + decision] = get_valores_finales(datos_predecision_theta[sensor][decision])
        valores_finales_theta["Post-decisión para " + decision] = get_valores_finales(datos_postdecision_theta[sensor][decision])
        valores_finales_gamma["Pre-decisión para " + decision] = get_valores_finales(datos_predecision_gamma[sensor][decision])
        valores_finales_gamma["Post-decisión para " + decision] = get_valores_finales(datos_postdecision_gamma[sensor][decision])
        valores_finales_raw["Pre-decisión para " + decision] = get_valores_finales(datos_predecision_raw[sensor][decision])
        valores_finales_raw["Post-decisión para " + decision] = get_valores_finales(datos_postdecision_raw[sensor][decision])

    json_final[sensor] = {
        "alpha" : valores_finales_alpha,
        "beta" : valores_finales_beta,
        "delta" : valores_finales_delta,
        "theta" : valores_finales_theta,
        "gamma" : valores_finales_gamma,
        "raw" : valores_finales_raw
    }

    condicion_predecision = (dataframe_csv['sensor'] == sensor) & (dataframe_csv['post-decision'] == False) & (dataframe_csv['normalizado'] == normalizar) & (dataframe_csv['milisegundos'] == milisegundos)    
    filas_pre = dataframe_csv[condicion_predecision]

    if not filas_pre.empty:

        for decision in decisiones:

            condicion_predecision = (dataframe_csv['sensor'] == sensor) & (dataframe_csv['post-decision'] == False) & (dataframe_csv['normalizado'] == normalizar) & (dataframe_csv['milisegundos'] == milisegundos) & (dataframe_csv['decision'] == decision)

            valores_a_introducir_predecision = []

            valores_a_introducir_predecision.append(fecha_legible)
            valores_a_introducir_predecision.append(valores_finales_raw["Pre-decisión para " + decision]["minimo"])
            valores_a_introducir_predecision.append(valores_finales_raw["Pre-decisión para " + decision]["maximo"])
            valores_a_introducir_predecision.append(valores_finales_raw["Pre-decisión para " + decision]["cuartil1"])
            valores_a_introducir_predecision.append(valores_finales_raw["Pre-decisión para " + decision]["cuartil2"])
            valores_a_introducir_predecision.append(valores_finales_raw["Pre-decisión para " + decision]["cuartil3"])
            valores_a_introducir_predecision.append(valores_finales_alpha["Pre-decisión para " + decision]["minimo"])
            valores_a_introducir_predecision.append(valores_finales_alpha["Pre-decisión para " + decision]["maximo"])
            valores_a_introducir_predecision.append(valores_finales_alpha["Pre-decisión para " + decision]["cuartil1"])
            valores_a_introducir_predecision.append(valores_finales_alpha["Pre-decisión para " + decision]["cuartil2"])
            valores_a_introducir_predecision.append(valores_finales_alpha["Pre-decisión para " + decision]["cuartil3"])
            valores_a_introducir_predecision.append(valores_finales_beta["Pre-decisión para " + decision]["minimo"])
            valores_a_introducir_predecision.append(valores_finales_beta["Pre-decisión para " + decision]["maximo"])
            valores_a_introducir_predecision.append(valores_finales_beta["Pre-decisión para " + decision]["cuartil1"])
            valores_a_introducir_predecision.append(valores_finales_beta["Pre-decisión para " + decision]["cuartil2"])
            valores_a_introducir_predecision.append(valores_finales_beta["Pre-decisión para " + decision]["cuartil3"])
            valores_a_introducir_predecision.append(valores_finales_delta["Pre-decisión para " + decision]["minimo"])
            valores_a_introducir_predecision.append(valores_finales_delta["Pre-decisión para " + decision]["maximo"])
            valores_a_introducir_predecision.append(valores_finales_delta["Pre-decisión para " + decision]["cuartil1"])
            valores_a_introducir_predecision.append(valores_finales_delta["Pre-decisión para " + decision]["cuartil2"])
            valores_a_introducir_predecision.append(valores_finales_delta["Pre-decisión para " + decision]["cuartil3"])
            valores_a_introducir_predecision.append(valores_finales_theta["Pre-decisión para " + decision]["minimo"])
            valores_a_introducir_predecision.append(valores_finales_theta["Pre-decisión para " + decision]["maximo"])
            valores_a_introducir_predecision.append(valores_finales_theta["Pre-decisión para " + decision]["cuartil1"])
            valores_a_introducir_predecision.append(valores_finales_theta["Pre-decisión para " + decision]["cuartil2"])
            valores_a_introducir_predecision.append(valores_finales_theta["Pre-decisión para " + decision]["cuartil3"])
            valores_a_introducir_predecision.append(valores_finales_gamma["Pre-decisión para " + decision]["minimo"])
            valores_a_introducir_predecision.append(valores_finales_gamma["Pre-decisión para " + decision]["maximo"])
            valores_a_introducir_predecision.append(valores_finales_gamma["Pre-decisión para " + decision]["cuartil1"])
            valores_a_introducir_predecision.append(valores_finales_gamma["Pre-decisión para " + decision]["cuartil2"])
            valores_a_introducir_predecision.append(valores_finales_gamma["Pre-decisión para " + decision]["cuartil3"])

            dataframe_csv.loc[condicion_predecision, columnas_a_modificar] = valores_a_introducir_predecision
            dataframe_csv.to_csv(url_csv, index=False)
    else:

        nueva_fila = {}
        nueva_fila['sensor'] = sensor
        nueva_fila['post-decision'] = False
        nueva_fila['normalizado'] = normalizar
        nueva_fila['milisegundos'] = milisegundos
        nueva_fila['ultima_modificacion'] = fecha_legible

        for decision in decisiones:
            nueva_fila['decision'] = decision
            nueva_fila['raw_minimo'] = valores_finales_raw["Pre-decisión para " + decision]['minimo']
            nueva_fila['raw_maximo'] = valores_finales_raw["Pre-decisión para " + decision]['maximo']
            nueva_fila['raw_cuartil1'] = valores_finales_raw["Pre-decisión para " + decision]['cuartil1']
            nueva_fila['raw_cuartil2'] = valores_finales_raw["Pre-decisión para " + decision]['cuartil2']
            nueva_fila['raw_cuartil3'] = valores_finales_raw["Pre-decisión para " + decision]['cuartil3']
            nueva_fila['alpha_minimo'] = valores_finales_alpha["Pre-decisión para " + decision]['minimo']
            nueva_fila['alpha_maximo'] = valores_finales_alpha["Pre-decisión para " + decision]['maximo']
            nueva_fila['alpha_cuartil1'] = valores_finales_alpha["Pre-decisión para " + decision]['cuartil1']
            nueva_fila['alpha_cuartil2'] = valores_finales_alpha["Pre-decisión para " + decision]['cuartil2']
            nueva_fila['alpha_cuartil3'] = valores_finales_alpha["Pre-decisión para " + decision]['cuartil3']
            nueva_fila['beta_minimo'] = valores_finales_beta["Pre-decisión para " + decision]['minimo']
            nueva_fila['beta_maximo'] = valores_finales_beta["Pre-decisión para " + decision]['maximo']
            nueva_fila['beta_cuartil1'] = valores_finales_beta["Pre-decisión para " + decision]['cuartil1']
            nueva_fila['beta_cuartil2'] = valores_finales_beta["Pre-decisión para " + decision]['cuartil2']
            nueva_fila['beta_cuartil3'] = valores_finales_beta["Pre-decisión para " + decision]['cuartil3']
            nueva_fila['theta_minimo'] = valores_finales_theta["Pre-decisión para " + decision]['minimo']
            nueva_fila['theta_maximo'] = valores_finales_theta["Pre-decisión para " + decision]['maximo']
            nueva_fila['theta_cuartil1'] = valores_finales_theta["Pre-decisión para " + decision]['cuartil1']
            nueva_fila['theta_cuartil2'] = valores_finales_theta["Pre-decisión para " + decision]['cuartil2']
            nueva_fila['theta_cuartil3'] = valores_finales_theta["Pre-decisión para " + decision]['cuartil3']
            nueva_fila['delta_minimo'] = valores_finales_delta["Pre-decisión para " + decision]['minimo']
            nueva_fila['delta_maximo'] = valores_finales_delta["Pre-decisión para " + decision]['maximo']
            nueva_fila['delta_cuartil1'] = valores_finales_delta["Pre-decisión para " + decision]['cuartil1']
            nueva_fila['delta_cuartil2'] = valores_finales_delta["Pre-decisión para " + decision]['cuartil2']
            nueva_fila['delta_cuartil3'] = valores_finales_delta["Pre-decisión para " + decision]['cuartil3']
            nueva_fila['gamma_minimo'] = valores_finales_gamma["Pre-decisión para " + decision]['minimo']
            nueva_fila['gamma_maximo'] = valores_finales_gamma["Pre-decisión para " + decision]['maximo']
            nueva_fila['gamma_cuartil1'] = valores_finales_gamma["Pre-decisión para " + decision]['cuartil1']
            nueva_fila['gamma_cuartil2'] = valores_finales_gamma["Pre-decisión para " + decision]['cuartil2']
            nueva_fila['gamma_cuartil3'] = valores_finales_gamma["Pre-decisión para " + decision]['cuartil3']

            dataframes_a_concatenar.append(pd.DataFrame([pd.Series(nueva_fila)], index=[0]))

    condicion_postdecision = (dataframe_csv['sensor'] == sensor) & (dataframe_csv['post-decision'] == True) & (dataframe_csv['normalizado'] == normalizar) & (dataframe_csv['milisegundos'] == milisegundos)    
    filas_post = dataframe_csv[condicion_postdecision]

    if not filas_post.empty:

        for decision in decisiones:

            condicion_postdecision = (dataframe_csv['sensor'] == sensor) & (dataframe_csv['post-decision'] == True) & (dataframe_csv['normalizado'] == normalizar) & (dataframe_csv['milisegundos'] == milisegundos) & (dataframe_csv['decision'] == decision)

            valores_a_introducir_postdecision = []

            valores_a_introducir_postdecision.append(fecha_legible)
            valores_a_introducir_postdecision.append(valores_finales_raw["Post-decisión para " + decision]["minimo"])
            valores_a_introducir_postdecision.append(valores_finales_raw["Post-decisión para " + decision]["maximo"])
            valores_a_introducir_postdecision.append(valores_finales_raw["Post-decisión para " + decision]["cuartil1"])
            valores_a_introducir_postdecision.append(valores_finales_raw["Post-decisión para " + decision]["cuartil2"])
            valores_a_introducir_postdecision.append(valores_finales_raw["Post-decisión para " + decision]["cuartil3"])
            valores_a_introducir_postdecision.append(valores_finales_alpha["Post-decisión para " + decision]["minimo"])
            valores_a_introducir_postdecision.append(valores_finales_alpha["Post-decisión para " + decision]["maximo"])
            valores_a_introducir_postdecision.append(valores_finales_alpha["Post-decisión para " + decision]["cuartil1"])
            valores_a_introducir_postdecision.append(valores_finales_alpha["Post-decisión para " + decision]["cuartil2"])
            valores_a_introducir_postdecision.append(valores_finales_alpha["Post-decisión para " + decision]["cuartil3"])
            valores_a_introducir_postdecision.append(valores_finales_beta["Post-decisión para " + decision]["minimo"])
            valores_a_introducir_postdecision.append(valores_finales_beta["Post-decisión para " + decision]["maximo"])
            valores_a_introducir_postdecision.append(valores_finales_beta["Post-decisión para " + decision]["cuartil1"])
            valores_a_introducir_postdecision.append(valores_finales_beta["Post-decisión para " + decision]["cuartil2"])
            valores_a_introducir_postdecision.append(valores_finales_beta["Post-decisión para " + decision]["cuartil3"])
            valores_a_introducir_postdecision.append(valores_finales_delta["Post-decisión para " + decision]["minimo"])
            valores_a_introducir_postdecision.append(valores_finales_delta["Post-decisión para " + decision]["maximo"])
            valores_a_introducir_postdecision.append(valores_finales_delta["Post-decisión para " + decision]["cuartil1"])
            valores_a_introducir_postdecision.append(valores_finales_delta["Post-decisión para " + decision]["cuartil2"])
            valores_a_introducir_postdecision.append(valores_finales_delta["Post-decisión para " + decision]["cuartil3"])
            valores_a_introducir_postdecision.append(valores_finales_theta["Post-decisión para " + decision]["minimo"])
            valores_a_introducir_postdecision.append(valores_finales_theta["Post-decisión para " + decision]["maximo"])
            valores_a_introducir_postdecision.append(valores_finales_theta["Post-decisión para " + decision]["cuartil1"])
            valores_a_introducir_postdecision.append(valores_finales_theta["Post-decisión para " + decision]["cuartil2"])
            valores_a_introducir_postdecision.append(valores_finales_theta["Post-decisión para " + decision]["cuartil3"])
            valores_a_introducir_postdecision.append(valores_finales_gamma["Post-decisión para " + decision]["minimo"])
            valores_a_introducir_postdecision.append(valores_finales_gamma["Post-decisión para " + decision]["maximo"])
            valores_a_introducir_postdecision.append(valores_finales_gamma["Post-decisión para " + decision]["cuartil1"])
            valores_a_introducir_postdecision.append(valores_finales_gamma["Post-decisión para " + decision]["cuartil2"])
            valores_a_introducir_postdecision.append(valores_finales_gamma["Post-decisión para " + decision]["cuartil3"])

            dataframe_csv.loc[condicion_postdecision, columnas_a_modificar] = valores_a_introducir_postdecision
            dataframe_csv.to_csv(url_csv, index=False)
    
    else:
        nueva_fila = {}
        nueva_fila['sensor'] = sensor
        nueva_fila['post-decision'] = True
        nueva_fila['normalizado'] = normalizar
        nueva_fila['milisegundos'] = 0
        nueva_fila['ultima_modificacion'] = fecha_legible

        for decision in decisiones:
            nueva_fila['decision'] = decision
            nueva_fila['raw_minimo'] = valores_finales_raw["Post-decisión para " + decision]['minimo']
            nueva_fila['raw_maximo'] = valores_finales_raw["Post-decisión para " + decision]['maximo']
            nueva_fila['raw_cuartil1'] = valores_finales_raw["Post-decisión para " + decision]['cuartil1']
            nueva_fila['raw_cuartil2'] = valores_finales_raw["Post-decisión para " + decision]['cuartil2']
            nueva_fila['raw_cuartil3'] = valores_finales_raw["Post-decisión para " + decision]['cuartil3']
            nueva_fila['alpha_minimo'] = valores_finales_alpha["Post-decisión para " + decision]['minimo']
            nueva_fila['alpha_maximo'] = valores_finales_alpha["Post-decisión para " + decision]['maximo']
            nueva_fila['alpha_cuartil1'] = valores_finales_alpha["Post-decisión para " + decision]['cuartil1']
            nueva_fila['alpha_cuartil2'] = valores_finales_alpha["Post-decisión para " + decision]['cuartil2']
            nueva_fila['alpha_cuartil3'] = valores_finales_alpha["Post-decisión para " + decision]['cuartil3']
            nueva_fila['beta_minimo'] = valores_finales_beta["Post-decisión para " + decision]['minimo']
            nueva_fila['beta_maximo'] = valores_finales_beta["Post-decisión para " + decision]['maximo']
            nueva_fila['beta_cuartil1'] = valores_finales_beta["Post-decisión para " + decision]['cuartil1']
            nueva_fila['beta_cuartil2'] = valores_finales_beta["Post-decisión para " + decision]['cuartil2']
            nueva_fila['beta_cuartil3'] = valores_finales_beta["Post-decisión para " + decision]['cuartil3']
            nueva_fila['theta_minimo'] = valores_finales_theta["Post-decisión para " + decision]['minimo']
            nueva_fila['theta_maximo'] = valores_finales_theta["Post-decisión para " + decision]['maximo']
            nueva_fila['theta_cuartil1'] = valores_finales_theta["Post-decisión para " + decision]['cuartil1']
            nueva_fila['theta_cuartil2'] = valores_finales_theta["Post-decisión para " + decision]['cuartil2']
            nueva_fila['theta_cuartil3'] = valores_finales_theta["Post-decisión para " + decision]['cuartil3']
            nueva_fila['delta_minimo'] = valores_finales_delta["Post-decisión para " + decision]['minimo']
            nueva_fila['delta_maximo'] = valores_finales_delta["Post-decisión para " + decision]['maximo']
            nueva_fila['delta_cuartil1'] = valores_finales_delta["Post-decisión para " + decision]['cuartil1']
            nueva_fila['delta_cuartil2'] = valores_finales_delta["Post-decisión para " + decision]['cuartil2']
            nueva_fila['delta_cuartil3'] = valores_finales_delta["Post-decisión para " + decision]['cuartil3']
            nueva_fila['gamma_minimo'] = valores_finales_gamma["Post-decisión para " + decision]['minimo']
            nueva_fila['gamma_maximo'] = valores_finales_gamma["Post-decisión para " + decision]['maximo']
            nueva_fila['gamma_cuartil1'] = valores_finales_gamma["Post-decisión para " + decision]['cuartil1']
            nueva_fila['gamma_cuartil2'] = valores_finales_gamma["Post-decisión para " + decision]['cuartil2']
            nueva_fila['gamma_cuartil3'] = valores_finales_gamma["Post-decisión para " + decision]['cuartil3']

            dataframes_a_concatenar.append(pd.DataFrame([pd.Series(nueva_fila)], index=[0]))

if dataframes_a_concatenar != []:
    dataframes_a_concatenar.insert(0, dataframe_csv)
    dataframe_csv = pd.concat(dataframes_a_concatenar)
    dataframe_csv.to_csv(url_csv, index=False)

print(json.dumps(json_final))
