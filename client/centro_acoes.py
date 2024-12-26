
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import requests
import base64
import json
import ast
import os



diretorio_atual = os.path.dirname(os.path.abspath(__file__))
endereco_driver = None
navegador = None



def obter_configs_locais():
    config_file = open(f'{diretorio_atual}\\configs.json')    
    configs_locais = json.load(config_file) 
    config_file.close()
    return configs_locais
configs_locais = obter_configs_locais()
url = configs_locais['endpoint_api']



def acionador(passo, identificador=0, varia_dicts_reg={}):

    estagio     = passo["estagio"     ]
    ordem       = passo["ordem"       ]
    acao        = passo["acao"        ]
    var_dict    = passo["var_dict"    ]
    sub_passos  = passo["sub_passos"  ]

    try:
        varia_dicts_pas = ast.literal_eval(var_dict)
    except:
        varia_dicts_pas = None
    retorno = {}


    funcao = globals().get(f"func_{acao}")
    if callable(funcao):
        resp_func = funcao(identificador, varia_dicts_reg ,varia_dicts_pas)
    else:
        print(f"A função '{acao}' não foi encontrada ou não é executável.")


    if sub_passos != None:
        sub_passos_dict = ast.literal_eval(sub_passos)
        retorno['SITUACAO']='SUB_PASSOS'
        retorno['NU_PROX_PASSO'] = sub_passos_dict[resp_func]
    else:
        retorno['SITUACAO']='FINALIZADO'


    return retorno

def func_OBTER_DRIVER           (identificador, varia_dicts_reg ,varia_dicts_pas):
    global endereco_driver,diretorio_atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_webdrivers = f"{diretorio_atual}\\webdrivers"
    subpastas_com_webdriver = []
    for root, dirs, files in os.walk(diretorio_webdrivers):
        if "msedgedriver.exe" in files:
            subpastas_com_webdriver.append(str(root).split('\\')[-1])
    endereco_driver = f"{diretorio_webdrivers}\\{subpastas_com_webdriver[0]}\\msedgedriver.exe"
    return endereco_driver

def func_CONFERE_DRIVERS           (identificador, varia_dicts_reg ,varia_dicts_pas):
    global endereco_driver,diretorio_atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_webdrivers = f"{diretorio_atual}\\webdrivers"
    subpastas_com_webdriver = []
    for root, dirs, files in os.walk(diretorio_webdrivers):
        if "msedgedriver.exe" in files:
            subpastas_com_webdriver.append(str(root).split('\\')[-1])
    drivers_locais  = subpastas_com_webdriver
    solicitacao     = {"drivers_locais":drivers_locais}
    configs_locais  = obter_configs_locais()
    url = configs_locais['endpoint_api']
    novos_drivers   = requests.get(f'{url}verifica_drivers',json=solicitacao).json()['resposta']    
    for novo_driver in novos_drivers:
        print(novo_driver["versao"])
    print(type(novos_drivers))
    return None

def func_INICIA_NAVEGADOR       (identificador, varia_dicts_reg ,varia_dicts_pas): 
    global endereco_driver, navegador, servico
    try:
        endereco_driver = func_OBTER_DRIVER(identificador, varia_dicts_reg, varia_dicts_pas)
        servico = Service(endereco_driver)
        navegador = webdriver.Edge(service=servico)    
        return "OK"
    except:
        return "FALHA"

def func_VERIFICA_NAVEGADOR     (identificador, varia_dicts_reg ,varia_dicts_pas): 
    global endereco_driver, navegador, servico
    try:    
        navegador.get("about:blank")
        return "FUNCIONANDO"
    except:
        try:
            try: navegador.quit()
            except: pass
            endereco_driver = func_OBTER_DRIVER(identificador, varia_dicts_reg, varia_dicts_pas)
            servico = Service(endereco_driver)
            navegador = webdriver.Edge(service=servico)    
            return "REINICIADO"
        except:
            return "FALHA"

def func_ACESSA_URL             (identificador, varia_dicts_reg ,varia_dicts_pas): 
    global navegador
    try:
        url = varia_dicts_pas["url"]
        navegador.get(url)
        return "OK"
    except:
        return "FALHA"

def func_DORME                  (identificador, varia_dicts_reg ,varia_dicts_pas): 
    tempo = varia_dicts_pas['tempo']
    try:
        sleep(tempo)
        return "OK"
    except:
        return "FALHA"

def func_PROCURA_ELEMENTO       (identificador, varia_dicts_reg ,varia_dicts_pas): 
    tipo = varia_dicts_pas['tipo']
    elemento = varia_dicts_pas['elemento']
    try:
        navegador.find_element(tipo,elemento)
        return "SIM"
    except:
        return "NAO"

def func_ENVIA_TEXTO            (identificador, varia_dicts_reg ,varia_dicts_pas): 
    tipo = varia_dicts_pas['tipo']
    elemento = varia_dicts_pas['elemento']
    texto= varia_dicts_pas['texto']
    try:
        navegador.find_element(tipo,elemento).send_keys(texto)
        return "OK"
    except:
        return "FALHA"

def func_ENVIA_TECLA            (identificador, varia_dicts_reg ,varia_dicts_pas): 
    tipo = varia_dicts_pas['tipo']
    elemento = varia_dicts_pas['elemento']
    tecla_string= varia_dicts_pas['tecla']
    
    try: 
        tecla = getattr(Keys,str(tecla_string).upper())
    except:
        tecla = None
    
    try:
        navegador.find_element(tipo,elemento).send_keys(tecla)
        return "OK"
    except:
        return "FALHA"

def func_ENVIA_CLICK            (identificador, varia_dicts_reg ,varia_dicts_pas): 
    tipo = varia_dicts_pas['tipo']
    elemento = varia_dicts_pas['elemento']
    try:
        navegador.find_element(tipo,elemento).click()
        return "OK"
    except:
        return "FALHA"

def func_PASS                   (identificador, varia_dicts_reg ,varia_dicts_pas): 
    pass



if __name__ == "__main__":
    # func_INICIA_NAVEGADOR()
    func_CONFERE_DRIVERS(None,None,None)
    pass