import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json


participantes = json.loads(sys.argv[1])
milisegundos = sys.argv[2]
normalizar = (sys.argv[3] == 'true')
museDataPath = sys.argv[4]


json_final = {}
dataframes_a_concatenar = []

url_csv = 'pythonScripts/medidasCalculadas/medidasCalculadasParticipantes.csv'

sensores = ["AF7", "AF8", "TP9", "TP10"]
decisiones = ["p", "q"]

columnas_a_modificar = [
    'ultima_modificacion',
    'raw_minimo_AF7',
    'raw_minimo_AF8',
    'raw_minimo_TP9',
    'raw_minimo_TP10',
    'raw_maximo_AF7',
    'raw_maximo_AF8',
    'raw_maximo_TP9',
    'raw_maximo_TP10',
    'raw_cuartil1_AF7',
    'raw_cuartil1_AF8',
    'raw_cuartil1_TP9',
    'raw_cuartil1_TP10',
    'raw_cuartil2_AF7',
    'raw_cuartil2_AF8',
    'raw_cuartil2_TP9',
    'raw_cuartil2_TP10',
    'raw_cuartil3_AF7',
    'raw_cuartil3_AF8',
    'raw_cuartil3_TP9',
    'raw_cuartil3_TP10',
    'alpha_minimo_AF7',
    'alpha_minimo_AF8',
    'alpha_minimo_TP9',
    'alpha_minimo_TP10',
    'alpha_maximo_AF7',
    'alpha_maximo_AF8',
    'alpha_maximo_TP9',
    'alpha_maximo_TP10',
    'alpha_cuartil1_AF7',
    'alpha_cuartil1_AF8',
    'alpha_cuartil1_TP9',
    'alpha_cuartil1_TP10',
    'alpha_cuartil2_AF7',
    'alpha_cuartil2_AF8',
    'alpha_cuartil2_TP9',
    'alpha_cuartil2_TP10',
    'alpha_cuartil3_AF7',
    'alpha_cuartil3_AF8',
    'alpha_cuartil3_TP9',
    'alpha_cuartil3_TP10',
    'beta_minimo_AF7',
    'beta_minimo_AF8',
    'beta_minimo_TP9',
    'beta_minimo_TP10',
    'beta_maximo_AF7',
    'beta_maximo_AF8',
    'beta_maximo_TP9',
    'beta_maximo_TP10',
    'beta_cuartil1_AF7',
    'beta_cuartil1_AF8',
    'beta_cuartil1_TP9',
    'beta_cuartil1_TP10',
    'beta_cuartil2_AF7',
    'beta_cuartil2_AF8',
    'beta_cuartil2_TP9',
    'beta_cuartil2_TP10',
    'beta_cuartil3_AF7',
    'beta_cuartil3_AF8',
    'beta_cuartil3_TP9',
    'beta_cuartil3_TP10',
    'delta_minimo_AF7',
    'delta_minimo_AF8',
    'delta_minimo_TP9',
    'delta_minimo_TP10',
    'delta_maximo_AF7',
    'delta_maximo_AF8',
    'delta_maximo_TP9',
    'delta_maximo_TP10',
    'delta_cuartil1_AF7',
    'delta_cuartil1_AF8',
    'delta_cuartil1_TP9',
    'delta_cuartil1_TP10',
    'delta_cuartil2_AF7',
    'delta_cuartil2_AF8',
    'delta_cuartil2_TP9',
    'delta_cuartil2_TP10',
    'delta_cuartil3_AF7',
    'delta_cuartil3_AF8',
    'delta_cuartil3_TP9',
    'delta_cuartil3_TP10',
    'theta_minimo_AF7',
    'theta_minimo_AF8',
    'theta_minimo_TP9',
    'theta_minimo_TP10',
    'theta_maximo_AF7',
    'theta_maximo_AF8',
    'theta_maximo_TP9',
    'theta_maximo_TP10',
    'theta_cuartil1_AF7',
    'theta_cuartil1_AF8',
    'theta_cuartil1_TP9',
    'theta_cuartil1_TP10',
    'theta_cuartil2_AF7',
    'theta_cuartil2_AF8',
    'theta_cuartil2_TP9',
    'theta_cuartil2_TP10',
    'theta_cuartil3_AF7',
    'theta_cuartil3_AF8',
    'theta_cuartil3_TP9',
    'theta_cuartil3_TP10',
    'gamma_minimo_AF7',
    'gamma_minimo_AF8',
    'gamma_minimo_TP9',
    'gamma_minimo_TP10',
    'gamma_maximo_AF7',
    'gamma_maximo_AF8',
    'gamma_maximo_TP9',
    'gamma_maximo_TP10',
    'gamma_cuartil1_AF7',
    'gamma_cuartil1_AF8',
    'gamma_cuartil1_TP9',
    'gamma_cuartil1_TP10',
    'gamma_cuartil2_AF7',
    'gamma_cuartil2_AF8',
    'gamma_cuartil2_TP9',
    'gamma_cuartil2_TP10',
    'gamma_cuartil3_AF7',
    'gamma_cuartil3_AF8',
    'gamma_cuartil3_TP9',
    'gamma_cuartil3_TP10',
]

pre_decision_obtenidos = []


valores_finales_raw = {}
valores_finales_beta = {}
valores_finales_theta = {}
valores_finales_gamma = {}
valores_finales_alpha = {}
valores_finales_delta = {}


def rellenar_json(row):

    if row['post-decision'] == True:
        text = 'Post-decisión'
    else:
        text = 'Pre-decisión'
        pre_decision_obtenidos.append(row['id_participante'])

    for sensor in sensores:
        valores = {
            "minimo" : row['raw_minimo_' + sensor], 
            "maximo" : row['raw_maximo_' + sensor], 
            "cuartil1" : row['raw_cuartil1_' + sensor], 
            "cuartil2" : row['raw_cuartil2_' + sensor], 
            "cuartil3" : row['raw_cuartil3_' + sensor]
        }

        valores_finales_raw.setdefault(row['id_participante'], {})[text + ' de ' + sensor + ' para ' + row['decision']] = valores

        valores = {
            "minimo" : row['beta_minimo_' + sensor], 
            "maximo" : row['beta_maximo_' + sensor], 
            "cuartil1" : row['beta_cuartil1_' + sensor], 
            "cuartil2" : row['beta_cuartil2_' + sensor], 
            "cuartil3" : row['beta_cuartil3_' + sensor]
        }

        valores_finales_beta.setdefault(row['id_participante'], {})[text + ' de ' + sensor + ' para ' + row['decision']] = valores
        
        valores = {
            "minimo" : row['delta_minimo_' + sensor], 
            "maximo" : row['delta_maximo_' + sensor], 
            "cuartil1" : row['delta_cuartil1_' + sensor], 
            "cuartil2" : row['delta_cuartil2_' + sensor], 
            "cuartil3" : row['delta_cuartil3_' + sensor]
        }

        valores_finales_delta.setdefault(row['id_participante'], {})[text + ' de ' + sensor + ' para ' + row['decision']] = valores

        valores = {
            "minimo" : row['theta_minimo_' + sensor], 
            "maximo" : row['theta_maximo_' + sensor], 
            "cuartil1" : row['theta_cuartil1_' + sensor], 
            "cuartil2" : row['theta_cuartil2_' + sensor], 
            "cuartil3" : row['theta_cuartil3_' + sensor]
        }

        valores_finales_theta.setdefault(row['id_participante'], {})[text + ' de ' + sensor + ' para ' + row['decision']] = valores

        valores = {
            "minimo" : row['gamma_minimo_' + sensor], 
            "maximo" : row['gamma_maximo_' + sensor], 
            "cuartil1" : row['gamma_cuartil1_' + sensor], 
            "cuartil2" : row['gamma_cuartil2_' + sensor], 
            "cuartil3" : row['gamma_cuartil3_' + sensor]
        }

        valores_finales_gamma.setdefault(row['id_participante'], {})[text + ' de ' + sensor + ' para ' + row['decision']] = valores

        valores = {
            "minimo" : row['alpha_minimo_' + sensor], 
            "maximo" : row['alpha_maximo_' + sensor], 
            "cuartil1" : row['alpha_cuartil1_' + sensor], 
            "cuartil2" : row['alpha_cuartil2_' + sensor], 
            "cuartil3" : row['alpha_cuartil3_' + sensor]
        }

        valores_finales_alpha.setdefault(row['id_participante'], {})[text + ' de ' + sensor + ' para ' + row['decision']] = valores

if os.path.isfile(url_csv):
    dataframe_csv = pd.read_csv(url_csv)

    for index, row in dataframe_csv.iterrows():

        url_participante = "data/results" + str(row['id_participante']) + '.csv'

        if os.path.isfile(url_participante):
            info_archivo = os.stat(url_participante)
            fecha_modificacion = info_archivo.st_mtime
            fecha_legible = datetime.fromtimestamp(fecha_modificacion).strftime('%Y-%m-%d %H:%M:%S')

            if fecha_legible == row['ultima_modificacion']:
                if str(row['id_participante']) in participantes and row['normalizado'] == normalizar and (row['milisegundos'] == 0 or row['milisegundos'] == int(milisegundos)):
                    rellenar_json(row)

                    json_final[row['id_participante']] = {
                        "alpha" : valores_finales_alpha[row['id_participante']],
                        "beta" : valores_finales_beta[row['id_participante']],
                        "delta" : valores_finales_delta[row['id_participante']],
                        "theta" : valores_finales_theta[row['id_participante']],
                        "gamma" : valores_finales_gamma[row['id_participante']],
                        "raw" : valores_finales_raw[row['id_participante']]
                    }
else:
    estructura_csv = {
        'id_participante' : [],
        'post-decision' : [],
        'normalizado' : [],
        'milisegundos' : [],
        'decision' : [],
        'ultima_modificacion' : [],
        'raw_minimo_AF7' : [],
        'raw_minimo_AF8' : [],
        'raw_minimo_TP9' : [],
        'raw_minimo_TP10' : [],
        'raw_maximo_AF7' : [],
        'raw_maximo_AF8' : [],
        'raw_maximo_TP9' : [],
        'raw_maximo_TP10' : [],
        'raw_cuartil1_AF7' : [],
        'raw_cuartil1_AF8' : [],
        'raw_cuartil1_TP9' : [],
        'raw_cuartil1_TP10' : [],
        'raw_cuartil2_AF7' : [],
        'raw_cuartil2_AF8' : [],
        'raw_cuartil2_TP9' : [],
        'raw_cuartil2_TP10' : [],
        'raw_cuartil3_AF7' : [],
        'raw_cuartil3_AF8' : [],
        'raw_cuartil3_TP9' : [],
        'raw_cuartil3_TP10' : [],
        'alpha_minimo_AF7' : [],
        'alpha_minimo_AF8' : [],
        'alpha_minimo_TP9' : [],
        'alpha_minimo_TP10' : [],
        'alpha_maximo_AF7' : [],
        'alpha_maximo_AF8' : [],
        'alpha_maximo_TP9' : [],
        'alpha_maximo_TP10' : [],
        'alpha_cuartil1_AF7' : [],
        'alpha_cuartil1_AF8' : [],
        'alpha_cuartil1_TP9' : [],
        'alpha_cuartil1_TP10' : [],
        'alpha_cuartil2_AF7' : [],
        'alpha_cuartil2_AF8' : [],
        'alpha_cuartil2_TP9' : [],
        'alpha_cuartil2_TP10' : [],
        'alpha_cuartil3_AF7' : [],
        'alpha_cuartil3_AF8' : [],
        'alpha_cuartil3_TP9' : [],
        'alpha_cuartil3_TP10' : [],
        'beta_minimo_AF7' : [],
        'beta_minimo_AF8' : [],
        'beta_minimo_TP9' : [],
        'beta_minimo_TP10' : [],
        'beta_maximo_AF7' : [],
        'beta_maximo_AF8' : [],
        'beta_maximo_TP9' : [],
        'beta_maximo_TP10' : [],
        'beta_cuartil1_AF7' : [],
        'beta_cuartil1_AF8' : [],
        'beta_cuartil1_TP9' : [],
        'beta_cuartil1_TP10' : [],
        'beta_cuartil2_AF7' : [],
        'beta_cuartil2_AF8' : [],
        'beta_cuartil2_TP9' : [],
        'beta_cuartil2_TP10' : [],
        'beta_cuartil3_AF7' : [],
        'beta_cuartil3_AF8' : [],
        'beta_cuartil3_TP9' : [],
        'beta_cuartil3_TP10' : [],
        'delta_minimo_AF7' : [],
        'delta_minimo_AF8' : [],
        'delta_minimo_TP9' : [],
        'delta_minimo_TP10' : [],
        'delta_maximo_AF7' : [],
        'delta_maximo_AF8' : [],
        'delta_maximo_TP9' : [],
        'delta_maximo_TP10' : [],
        'delta_cuartil1_AF7' : [],
        'delta_cuartil1_AF8' : [],
        'delta_cuartil1_TP9' : [],
        'delta_cuartil1_TP10' : [],
        'delta_cuartil2_AF7' : [],
        'delta_cuartil2_AF8' : [],
        'delta_cuartil2_TP9' : [],
        'delta_cuartil2_TP10' : [],
        'delta_cuartil3_AF7' : [],
        'delta_cuartil3_AF8' : [],
        'delta_cuartil3_TP9' : [],
        'delta_cuartil3_TP10' : [],
        'theta_minimo_AF7' : [],
        'theta_minimo_AF8' : [],
        'theta_minimo_TP9' : [],
        'theta_minimo_TP10' : [],
        'theta_maximo_AF7' : [],
        'theta_maximo_AF8' : [],
        'theta_maximo_TP9' : [],
        'theta_maximo_TP10' : [],
        'theta_cuartil1_AF7' : [],
        'theta_cuartil1_AF8' : [],
        'theta_cuartil1_TP9' : [],
        'theta_cuartil1_TP10' : [],
        'theta_cuartil2_AF7' : [],
        'theta_cuartil2_AF8' : [],
        'theta_cuartil2_TP9' : [],
        'theta_cuartil2_TP10' : [],
        'theta_cuartil3_AF7' : [],
        'theta_cuartil3_AF8' : [],
        'theta_cuartil3_TP9' : [],
        'theta_cuartil3_TP10' : [],
        'gamma_minimo_AF7' : [],
        'gamma_minimo_AF8' : [],
        'gamma_minimo_TP9' : [],
        'gamma_minimo_TP10' : [],
        'gamma_maximo_AF7' : [],
        'gamma_maximo_AF8' : [],
        'gamma_maximo_TP9' : [],
        'gamma_maximo_TP10' : [],
        'gamma_cuartil1_AF7' : [],
        'gamma_cuartil1_AF8' : [],
        'gamma_cuartil1_TP9' : [],
        'gamma_cuartil1_TP10' : [],
        'gamma_cuartil2_AF7' : [],
        'gamma_cuartil2_AF8' : [],
        'gamma_cuartil2_TP9' : [],
        'gamma_cuartil2_TP10' : [],
        'gamma_cuartil3_AF7' : [],
        'gamma_cuartil3_AF8' : [],
        'gamma_cuartil3_TP9' : [],
        'gamma_cuartil3_TP10' : [],
    }

    dataframe_csv = pd.DataFrame(estructura_csv)
    dataframe_csv.to_csv(url_csv, index=False)

nuevos_participantes = []

for participante in participantes:
    if not (int(participante) in pre_decision_obtenidos): 
        nuevos_participantes.append(participante)

participantes = nuevos_participantes

dataframe_csv = pd.read_csv(url_csv)

def get_limites_de_tiempo(dataframe):
    dataframe = dataframe.drop(columns=['ID del participante', 'Trial', 'Respuesta', 'Tiempo de inicio', 'Tiempo de aparición de letras', 'Letra observada'])

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

def get_datos(dataframe, participante):
    dataframe = dataframe.drop(columns=['AUX_RIGHT', 'Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'HeadBandOn', 'HSI_TP9', 'HSI_AF7', 'HSI_AF8', 'HSI_TP10', 'Battery', 'Elements'])
    
    indice_pre_decision_p = 0
    indice_pre_decision_q = 0
    indice_post_decision_p = 0
    indice_post_decision_q = 0

    for index, row in dataframe.iloc[1:].iterrows():
        if row['TimeStamp'] <= limites_de_tiempo_predecision_p[indice_pre_decision_p]['Tiempo impulso'] and row['TimeStamp'] >= limites_de_tiempo_predecision_p[indice_pre_decision_p]['Tiempo pre-decision']:
            for sensor in sensores:
                datos_predecision_alpha[participante]['p'][sensor].append(row['Alpha_' + sensor])
                datos_predecision_delta[participante]['p'][sensor].append(row['Delta_' + sensor])
                datos_predecision_theta[participante]['p'][sensor].append(row['Theta_' + sensor])
                datos_predecision_beta[participante]['p'][sensor].append(row['Beta_' + sensor])
                datos_predecision_gamma[participante]['p'][sensor].append(row['Gamma_' + sensor])
                datos_predecision_raw[participante]['p'][sensor].append(row['RAW_' + sensor])
        elif row['TimeStamp'] > limites_de_tiempo_predecision_p[indice_pre_decision_p]['Tiempo impulso'] and indice_pre_decision_p < len(limites_de_tiempo_predecision_p)-2:
            indice_pre_decision_p += 1

        if row['TimeStamp'] <= limites_de_tiempo_predecision_q[indice_pre_decision_q]['Tiempo impulso'] and row['TimeStamp'] >= limites_de_tiempo_predecision_q[indice_pre_decision_q]['Tiempo pre-decision']:
            for sensor in sensores:
                datos_predecision_alpha[participante]['q'][sensor].append(row['Alpha_' + sensor])
                datos_predecision_delta[participante]['q'][sensor].append(row['Delta_' + sensor])
                datos_predecision_theta[participante]['q'][sensor].append(row['Theta_' + sensor])
                datos_predecision_beta[participante]['q'][sensor].append(row['Beta_' + sensor])
                datos_predecision_gamma[participante]['q'][sensor].append(row['Gamma_' + sensor])
                datos_predecision_raw[participante]['q'][sensor].append(row['RAW_' + sensor])
        elif row['TimeStamp'] > limites_de_tiempo_predecision_q[indice_pre_decision_q]['Tiempo impulso'] and indice_pre_decision_q < len(limites_de_tiempo_predecision_q)-2:
            indice_pre_decision_q += 1

        if row['TimeStamp'] <= limites_de_tiempo_postdecision_p[indice_post_decision_p]['Tiempo post-decision'] and row['TimeStamp'] >= limites_de_tiempo_postdecision_p[indice_post_decision_p]['Tiempo impulso']:
            for sensor in sensores:
                datos_postdecision_alpha[participante]['p'][sensor].append(row['Alpha_' + sensor])
                datos_postdecision_delta[participante]['p'][sensor].append(row['Delta_' + sensor])
                datos_postdecision_theta[participante]['p'][sensor].append(row['Theta_' + sensor])
                datos_postdecision_beta[participante]['p'][sensor].append(row['Beta_' + sensor])
                datos_postdecision_gamma[participante]['p'][sensor].append(row['Gamma_' + sensor])
                datos_postdecision_raw[participante]['p'][sensor].append(row['RAW_' + sensor])
        elif row['TimeStamp'] > limites_de_tiempo_postdecision_p[indice_post_decision_p]['Tiempo post-decision'] and indice_post_decision_p < len(limites_de_tiempo_postdecision_p)-2:
            indice_post_decision_p += 1

        if row['TimeStamp'] <= limites_de_tiempo_postdecision_q[indice_post_decision_q]['Tiempo post-decision'] and row['TimeStamp'] >= limites_de_tiempo_postdecision_q[indice_post_decision_q]['Tiempo impulso']:
            for sensor in sensores:
                datos_postdecision_alpha[participante]['q'][sensor].append(row['Alpha_' + sensor])
                datos_postdecision_delta[participante]['q'][sensor].append(row['Delta_' + sensor])
                datos_postdecision_theta[participante]['q'][sensor].append(row['Theta_' + sensor])
                datos_postdecision_beta[participante]['q'][sensor].append(row['Beta_' + sensor])
                datos_postdecision_gamma[participante]['q'][sensor].append(row['Gamma_' + sensor])
                datos_postdecision_raw[participante]['q'][sensor].append(row['RAW_' + sensor])
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

for participante in participantes:

    limites_de_tiempo_predecision_p = []
    limites_de_tiempo_predecision_q = []
    limites_de_tiempo_postdecision_p = []
    limites_de_tiempo_postdecision_q = []

    dataframe_local = pd.read_csv('data/results' + str(participante) + '.csv')
    get_limites_de_tiempo(dataframe_local)

    for decision in decisiones:
        datos_predecision_delta.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_predecision_theta.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_predecision_alpha.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_predecision_beta.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_predecision_gamma.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_predecision_raw.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}

        datos_postdecision_delta.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_postdecision_theta.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_postdecision_alpha.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_postdecision_beta.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_postdecision_gamma.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}
        datos_postdecision_raw.setdefault(participante, {})[decision] = {"AF7" : [], "AF8" : [], "TP9" : [], "TP10" : []}

    if os.path.isfile(museDataPath + '/museData' + str(participante) + '.csv'):
        dataframe_muse = pd.read_csv(museDataPath + '/museData' + str(participante) + '.csv', low_memory=False)
        get_datos(dataframe_muse, participante)

    for sensor in sensores:
        for decision in decisiones:
            valores_finales_alpha["Pre-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_predecision_alpha[participante][decision][sensor])
            valores_finales_alpha["Post-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_postdecision_alpha[participante][decision][sensor])
            valores_finales_beta["Pre-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_predecision_beta[participante][decision][sensor])
            valores_finales_beta["Post-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_postdecision_beta[participante][decision][sensor])
            valores_finales_delta["Pre-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_predecision_delta[participante][decision][sensor])
            valores_finales_delta["Post-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_postdecision_delta[participante][decision][sensor])
            valores_finales_theta["Pre-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_predecision_theta[participante][decision][sensor])
            valores_finales_theta["Post-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_postdecision_theta[participante][decision][sensor])
            valores_finales_gamma["Pre-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_predecision_gamma[participante][decision][sensor])
            valores_finales_gamma["Post-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_postdecision_gamma[participante][decision][sensor])
            valores_finales_raw["Pre-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_predecision_raw[participante][decision][sensor])
            valores_finales_raw["Post-decisión de " + sensor + " para " + decision] = get_valores_finales(datos_postdecision_raw[participante][decision][sensor])

    json_final[participante] = {
        "alpha" : valores_finales_alpha,
        "beta" : valores_finales_beta,
        "delta" : valores_finales_delta,
        "theta" : valores_finales_theta,
        "gamma" : valores_finales_gamma,
        "raw" : valores_finales_raw
    }

    condicion_predecision = (dataframe_csv['id_participante'] == participante) & (dataframe_csv['post-decision'] == False) & (dataframe_csv['normalizado'] == normalizar) & (dataframe_csv['milisegundos'] == milisegundos)    
    filas_pre = dataframe_csv[condicion_predecision]

    info_archivo = os.stat("data/results" + str(participante) + '.csv')
    fecha_modificacion = info_archivo.st_mtime
    fecha_legible = datetime.fromtimestamp(fecha_modificacion).strftime('%Y-%m-%d %H:%M:%S')

    if not filas_pre.empty:
        valores_a_introducir_predecision = []
        valores_a_introducir_postdecision = []

        valores_a_introducir_predecision.append(fecha_legible)
        valores_a_introducir_postdecision.append(fecha_legible)

        # Recorremos el diccionario y obtenemos las claves que nos interesan
        af7_pre = [key for key in valores_finales_raw.keys() if "Pre-decisión de AF7" in key]
        af8_pre = [key for key in valores_finales_raw.keys() if "Pre-decisión de AF8" in key]
        tp9_pre = [key for key in valores_finales_raw.keys() if "Pre-decisión de TP9" in key]
        tp10_pre = [key for key in valores_finales_raw.keys() if "Pre-decisión de TP10" in key]

        # Clasificamos por pre-decision o post-decision y obtenemos los valores correspondientes
        valores_a_introducir_predecision.append([valores_finales_raw[key]["minimo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_raw[key]["maximo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_raw[key]["cuartil1"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_raw[key]["cuartil2"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_raw[key]["cuartil3"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_alpha[key]["minimo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_alpha[key]["maximo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_alpha[key]["cuartil1"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_alpha[key]["cuartil2"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_alpha[key]["cuartil3"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_beta[key]["minimo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_beta[key]["maximo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_beta[key]["cuartil1"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_beta[key]["cuartil2"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_beta[key]["cuartil3"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_delta[key]["minimo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_delta[key]["maximo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_delta[key]["cuartil1"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_delta[key]["cuartil2"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_delta[key]["cuartil3"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_theta[key]["minimo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_theta[key]["maximo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_theta[key]["cuartil1"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_theta[key]["cuartil2"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_theta[key]["cuartil3"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_gamma[key]["minimo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_gamma[key]["maximo"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_gamma[key]["cuartil1"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_gamma[key]["cuartil2"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre] + \
                    [valores_finales_gamma[key]["cuartil3"] for key in af7_pre + af8_pre + tp9_pre + tp10_pre]
                    )

        dataframe_csv.loc[condicion_predecision, columnas_a_modificar] = valores_a_introducir_predecision
        dataframe_csv.to_csv(url_csv, index=False)

    else:
        nueva_fila = {}
        nueva_fila['id_participante'] = participante
        nueva_fila['post-decision'] = False
        nueva_fila['normalizado'] = normalizar
        nueva_fila['milisegundos'] = milisegundos
        nueva_fila['ultima_modificacion'] = fecha_legible

        for decision in decisiones:
            nueva_fila['decision'] = decision

            for sensor in sensores:
                nueva_fila['raw_minimo_' + sensor] = valores_finales_raw["Post-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['raw_maximo_' + sensor] = valores_finales_raw["Post-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['raw_cuartil1_' + sensor] = valores_finales_raw["Post-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['raw_cuartil2_' + sensor] = valores_finales_raw["Post-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['raw_cuartil3_' + sensor] = valores_finales_raw["Post-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['alpha_minimo_' + sensor] = valores_finales_alpha["Post-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['alpha_maximo_' + sensor] = valores_finales_alpha["Post-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['alpha_cuartil1_' + sensor] = valores_finales_alpha["Post-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['alpha_cuartil2_' + sensor] = valores_finales_alpha["Post-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['alpha_cuartil3_' + sensor] = valores_finales_alpha["Post-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['beta_minimo_' + sensor] = valores_finales_beta["Post-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['beta_maximo_' + sensor] = valores_finales_beta["Post-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['beta_cuartil1_' + sensor] = valores_finales_beta["Post-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['beta_cuartil2_' + sensor] = valores_finales_beta["Post-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['beta_cuartil3_' + sensor] = valores_finales_beta["Post-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['delta_minimo_' + sensor] = valores_finales_delta["Post-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['delta_maximo_' + sensor] = valores_finales_delta["Post-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['delta_cuartil1_' + sensor] = valores_finales_delta["Post-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['delta_cuartil2_' + sensor] = valores_finales_delta["Post-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['delta_cuartil3_' + sensor] = valores_finales_delta["Post-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['theta_minimo_' + sensor] = valores_finales_theta["Post-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['theta_maximo_' + sensor] = valores_finales_theta["Post-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['theta_cuartil1_' + sensor] = valores_finales_theta["Post-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['theta_cuartil2_' + sensor] = valores_finales_theta["Post-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['theta_cuartil3_' + sensor] = valores_finales_theta["Post-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['gamma_minimo_' + sensor] = valores_finales_gamma["Post-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['gamma_maximo_' + sensor] = valores_finales_gamma["Post-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['gamma_cuartil1_' + sensor] = valores_finales_gamma["Post-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['gamma_cuartil2_' + sensor] = valores_finales_gamma["Post-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['gamma_cuartil3_' + sensor] = valores_finales_gamma["Post-decisión de " + sensor + " para " + decision]['cuartil3']

            dataframes_a_concatenar.append(pd.DataFrame([pd.Series(nueva_fila)], index=[0]))

    condicion_postdecision = (dataframe_csv['id_participante'] == participante) & (dataframe_csv['post-decision'] == True) & (dataframe_csv['normalizado'] == normalizar) & (dataframe_csv['milisegundos'] == 0)
    filas_post = dataframe_csv[condicion_postdecision]

    if not filas_post.empty:
        valores_a_introducir_postdecision = []
        valores_a_introducir_postdecision.append(fecha_legible)

        # Recorremos el diccionario y obtenemos las claves que nos interesan
        af7_post = [key for key in valores_finales_raw.keys() if "Post-decisión de AF7" in key]
        af8_post = [key for key in valores_finales_raw.keys() if "Post-decisión de AF8" in key]
        tp9_post = [key for key in valores_finales_raw.keys() if "Post-decisión de TP9" in key]
        tp10_post = [key for key in valores_finales_raw.keys() if "Post-decisión de TP10" in key]

        # Clasificamos por pre-decision o post-decision y obtenemos los valores correspondientes
        valores_a_introducir_postdecision.append([valores_finales_raw[key]["minimo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_raw[key]["maximo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_raw[key]["cuartil1"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_raw[key]["cuartil2"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_raw[key]["cuartil3"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_alpha[key]["minimo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_alpha[key]["maximo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_alpha[key]["cuartil1"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_alpha[key]["cuartil2"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_alpha[key]["cuartil3"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_beta[key]["minimo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_beta[key]["maximo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_beta[key]["cuartil1"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_beta[key]["cuartil2"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_beta[key]["cuartil3"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_delta[key]["minimo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_delta[key]["maximo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_delta[key]["cuartil1"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_delta[key]["cuartil2"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_delta[key]["cuartil3"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_theta[key]["minimo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_theta[key]["maximo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_theta[key]["cuartil1"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_theta[key]["cuartil2"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_theta[key]["cuartil3"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_gamma[key]["minimo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_gamma[key]["maximo"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_gamma[key]["cuartil1"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_gamma[key]["cuartil2"] for key in af7_post + af8_post + tp9_post + tp10_post] + \
                    [valores_finales_gamma[key]["cuartil3"] for key in af7_post + af8_post + tp9_post + tp10_post]
                    )
        
        dataframe_csv.loc[condicion_postdecision, columnas_a_modificar] = valores_a_introducir_postdecision
        dataframe_csv.to_csv(url_csv, index=False)

    else:
        nueva_fila = {}
        nueva_fila['id_participante'] = participante
        nueva_fila['post-decision'] = True
        nueva_fila['normalizado'] = normalizar
        nueva_fila['milisegundos'] = 0
        nueva_fila['ultima_modificacion'] = fecha_legible

        for decision in decisiones:
            nueva_fila['decision'] = decision

            for sensor in sensores:
                nueva_fila['raw_minimo_' + sensor] = valores_finales_raw["Pre-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['raw_maximo_' + sensor] = valores_finales_raw["Pre-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['raw_cuartil1_' + sensor] = valores_finales_raw["Pre-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['raw_cuartil2_' + sensor] = valores_finales_raw["Pre-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['raw_cuartil3_' + sensor] = valores_finales_raw["Pre-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['alpha_minimo_' + sensor] = valores_finales_alpha["Pre-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['alpha_maximo_' + sensor] = valores_finales_alpha["Pre-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['alpha_cuartil1_' + sensor] = valores_finales_alpha["Pre-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['alpha_cuartil2_' + sensor] = valores_finales_alpha["Pre-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['alpha_cuartil3_' + sensor] = valores_finales_alpha["Pre-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['beta_minimo_' + sensor] = valores_finales_beta["Pre-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['beta_maximo_' + sensor] = valores_finales_beta["Pre-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['beta_cuartil1_' + sensor] = valores_finales_beta["Pre-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['beta_cuartil2_' + sensor] = valores_finales_beta["Pre-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['beta_cuartil3_' + sensor] = valores_finales_beta["Pre-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['delta_minimo_' + sensor] = valores_finales_delta["Pre-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['delta_maximo_' + sensor] = valores_finales_delta["Pre-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['delta_cuartil1_' + sensor] = valores_finales_delta["Pre-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['delta_cuartil2_' + sensor] = valores_finales_delta["Pre-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['delta_cuartil3_' + sensor] = valores_finales_delta["Pre-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['theta_minimo_' + sensor] = valores_finales_theta["Pre-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['theta_maximo_' + sensor] = valores_finales_theta["Pre-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['theta_cuartil1_' + sensor] = valores_finales_theta["Pre-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['theta_cuartil2_' + sensor] = valores_finales_theta["Pre-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['theta_cuartil3_' + sensor] = valores_finales_theta["Pre-decisión de " + sensor + " para " + decision]['cuartil3']

                nueva_fila['gamma_minimo_' + sensor] = valores_finales_gamma["Pre-decisión de " + sensor + " para " + decision]['minimo']
                nueva_fila['gamma_maximo_' + sensor] = valores_finales_gamma["Pre-decisión de " + sensor + " para " + decision]['maximo']
                nueva_fila['gamma_cuartil1_' + sensor] = valores_finales_gamma["Pre-decisión de " + sensor + " para " + decision]['cuartil1']
                nueva_fila['gamma_cuartil2_' + sensor] = valores_finales_gamma["Pre-decisión de " + sensor + " para " + decision]['cuartil2']
                nueva_fila['gamma_cuartil3_' + sensor] = valores_finales_gamma["Pre-decisión de " + sensor + " para " + decision]['cuartil3']

            dataframes_a_concatenar.append(pd.DataFrame([pd.Series(nueva_fila)], index=[0]))

if dataframes_a_concatenar != []:
    dataframes_a_concatenar.insert(0, dataframe_csv)
    dataframe_csv = pd.concat(dataframes_a_concatenar)
    dataframe_csv.to_csv(url_csv, index=False)


print(json.dumps(json_final))
