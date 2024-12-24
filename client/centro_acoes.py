
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from time import sleep
import ast
import os



diretorio_atual = os.path.dirname(os.path.abspath(__file__))
endereco_driver = None
navegador = None



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

def func_OBTER_DRIVER(identificador, varia_dicts_reg ,varia_dicts_pas):
    global endereco_driver,diretorio_atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_webdrivers = f"{diretorio_atual}\\webdrivers"
    subpastas_com_webdriver = []
    for root, dirs, files in os.walk(diretorio_webdrivers):
        if "msedgedriver.exe" in files:
            subpastas_com_webdriver.append(str(root).split('\\')[-1])
    endereco_driver = f"{diretorio_webdrivers}\\{subpastas_com_webdriver[0]}\\msedgedriver.exe"
    return endereco_driver

def func_INICIAR_NAVEGADOR(identificador, varia_dicts_reg ,varia_dicts_pas): 
    global endereco_driver, navegador, servico
    try:
        endereco_driver = func_OBTER_DRIVER(identificador, varia_dicts_reg, varia_dicts_pas)
        servico = Service(endereco_driver)
        navegador = webdriver.Edge(service=servico)    
        return "OK"
    except:
        return "FALHA"

def func_ACESSA_URL(identificador, varia_dicts_reg ,varia_dicts_pas): 
    global navegador
    navegador.get('https://www.google.com')
    pass

def func_DORME(identificador, varia_dicts_reg ,varia_dicts_pas): 
    tempo = varia_dicts_pas['tempo']
    try:
        sleep(tempo)
        return "OK"
    except:
        return "FALHA"

def func_PROCURA_ELEMENTO(identificador, varia_dicts_reg ,varia_dicts_pas): 
    tipo = varia_dicts_pas['tipo']
    elemento = varia_dicts_pas['elemento']
    try:
        navegador.find_element(tipo,elemento)
        return "SIM"
    except:
        return "NAO"

def func_PASS(identificador, varia_dicts_reg ,varia_dicts_pas): 
    pass



if __name__ == "__main__":
    func_INICIAR_NAVEGADOR()
    pass