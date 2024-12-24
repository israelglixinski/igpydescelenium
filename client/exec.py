import requests
import socket
import json
import os
from time import sleep
from datetime import datetime
import centro_acoes

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
passos = None

def obter_configs_locais():
    config_file = open(f'{diretorio_atual}\\configs.json')    
    configs_locais = json.load(config_file) 
    config_file.close()
    return configs_locais
configs_locais = obter_configs_locais()

def obter_configs_finais():
    global configs_locais, configs_finais
    configs_locais = obter_configs_locais()
    user = os.getlogin()
    hostname = socket.gethostname()
    usrhost = f"{user}---{hostname}"
    solicitacao = {"usrhost":usrhost,"configs_locais":configs_locais}
    url = configs_locais['endpoint_api']
    configs_finais = (requests.get(f'{url}configs',json=solicitacao).json())['resposta']
    return configs_finais

def obter_passos():
    global passos
    url = configs_finais['endpoint_api']
    rotina = configs_finais['rotina']
    solicitacao = {"rotina":rotina}
    passos = requests.get(f'{url}passos',json=solicitacao).json()['resposta']
    return passos

def obter_horarios():
    url = configs_finais['endpoint_api']
    horarios_exec = configs_finais['horarios_exec']
    solicitacao = {"horarios_exec":horarios_exec}
    horarios = requests.get(f'{url}horarios',json=solicitacao).json()['resposta']
    return horarios

def obter_lote():
    url             = configs_finais['endpoint_api']
    rotina          = configs_finais['rotina']
    lote            = configs_finais['lote']
    max_qt_lote     = configs_finais['max_qt_lote']
    usr_host        = configs_finais['usr_host']
    solicitacao     = {"rotina":rotina,"lote":lote,"max_qt_lote":max_qt_lote,"usr_host":usr_host}
    lote            = requests.get(f'{url}lotes',json=solicitacao).json()['resposta']
    return lote


def executa_passo(passo_atual):
    global passos
    retorno = centro_acoes.acionador(passo_atual)
    if retorno['SITUACAO'] == 'SUB_PASSO': 
        nu_prox_passo = retorno['NU_PROX_PASSO'] 
        prox_passo = passos['acoes'][str(nu_prox_passo)]
        retorno = executa_passo(prox_passo)
    else:
        return retorno

def orquestrador():
    global passos
    passos = obter_passos()
    horarios = obter_horarios()
    dias_da_semana = ['SEG','TER','QUA','QUI','SEX','SAB','DOM']
    
    try:
        for numero_passo in passos['ordem_acoes']["INICIAL"]:
            passo = passos['acoes'][str(numero_passo)]
            executa_passo(passo)
    except: pass

    while True:
        
        try:
            for numero_passo in passos['ordem_acoes']["PRE_HORA"]:
                passo = passos['acoes'][str(numero_passo)]
                executa_passo(passo)
        except: pass    
        
        indice_dia = datetime.now().weekday()
        dia_da_semana =  dias_da_semana[indice_dia]
        horarios_hoje = horarios[dia_da_semana]
        hora_agora = datetime.now().strftime('%H:%M')
        
        if (
            ((horarios_hoje["horario_ini" ] != "NAO") and (horarios_hoje["horario_fin" ] != "NAO") and (hora_agora > horarios_hoje["horario_ini" ]) and (hora_agora < horarios_hoje["horario_fin" ])) and not
            ((horarios_hoje["excluir1_ini"] != "NAO") and (horarios_hoje["excluir1_fin"] != "NAO") and (hora_agora > horarios_hoje["excluir1_ini"]) and (hora_agora < horarios_hoje["excluir1_fin"])) and not
            ((horarios_hoje["excluir2_ini"] != "NAO") and (horarios_hoje["excluir1_fin"] != "NAO") and (hora_agora > horarios_hoje["excluir2_ini"]) and (hora_agora < horarios_hoje["excluir1_fin"])) and not
            ((horarios_hoje["excluir3_ini"] != "NAO") and (horarios_hoje["excluir1_fin"] != "NAO") and (hora_agora > horarios_hoje["excluir3_ini"]) and (hora_agora < horarios_hoje["excluir1_fin"]))
            ):

            print('dentro do horario de execução')
            print('buscando lote')
            lote = obter_lote()
            if len(lote) == 0:
                print("não temos mais lotes para trabalhar")
                dormir = 1
            else:
    
                try:
                    for numero_passo in passos['ordem_acoes']["PRE_LOOP"]:
                        passo = passos['acoes'][str(numero_passo)]
                        executa_passo(passo)
                except: pass            
    
                for registro in lote:
                    print(f'Iniciando o registro: {registro['id_reg']}')
 
                    try:
                        for numero_passo in passos['ordem_acoes']["IN_LOOP"]:
                            passo = passos['acoes'][str(numero_passo)]
                            executa_passo(passo)
                    except: pass

                    
                    print(f'Finalizado o registro: {registro['id_reg']}')
                
                
                try:
                    for numero_passo in passos['ordem_acoes']["POS_LOOP"]:
                        passo = passos['acoes'][str(numero_passo)]
                        executa_passo(passo)
                except: pass
                
                
                print('finalizado lote')
                dormir = 0


        else:
            print('fora do horario de execução')
            dormir = 1

        try:
            for numero_passo in passos['ordem_acoes']["POS_HORA"]:
                passo = passos['acoes'][str(numero_passo)]
                executa_passo(passo)
        except: pass

        if dormir: sleep(configs_finais["sleep_time"])
        pass
    pass

def iniciar():
    global configs_finais
    configs_finais = obter_configs_finais()
    orquestrador()



if __name__ == "__main__":
    iniciar()