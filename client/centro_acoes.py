
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from time import sleep
import ast
import os



diretorio_atual = os.path.dirname(os.path.abspath(__file__))
endereco_driver = None
navegador = None



def acionador(passo):

    estagio     = passo["estagio"     ]
    ordem       = passo["ordem"       ]
    acao        = passo["acao"        ]
    var_dict    = passo["var_dict"    ]
    sub_passos  = passo["sub_passos"  ]

    try:
        varia_dicts = ast.literal_eval(var_dict)
    except:
        varia_dicts = None
    retorno = {}


    funcao = globals().get(f"func_{acao}")  # Use locals() se estiver dentro de um escopo fechado
    if callable(funcao):
        resp_func = funcao()  # Chama a função
    else:
        print(f"A função '{acao}' não foi encontrada ou não é executável.")


    if sub_passos != None:
        retorno['SITUACAO']='SUB_PASSOS'
        retorno['NU_PROX_PASSO'] = varia_dicts[resp_func]
    else:
        retorno['SITUACAO']='FINALIZADO'


    return retorno


def func_OBTER_DRIVER():
    global endereco_driver,diretorio_atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_webdrivers = f"{diretorio_atual}\\webdrivers"
    subpastas_com_webdriver = []
    for root, dirs, files in os.walk(diretorio_webdrivers):
        if "msedgedriver.exe" in files:
            subpastas_com_webdriver.append(str(root).split('\\')[-1])
    endereco_driver = f"{diretorio_webdrivers}\\{subpastas_com_webdriver[0]}\\msedgedriver.exe"
    return endereco_driver

def func_INICIAR_NAVEGADOR(): 
    global endereco_driver, navegador
    try:
        endereco_driver = func_OBTER_DRIVER()
        servico = Service(endereco_driver)
        navegador = webdriver.Edge(service=servico)    
        return "OK"
    except:
        return "FALHA"

def func_ACESSA_URL(): 
    global navegador
    navegador.get('https://www.google.com')
    pass

def func_DORME(): 
    sleep(20)
    pass

def func_PROCURA_ELEMENTO(): 
    pass

def func_PASS(): 
    pass



if __name__ == "__main__":
    func_INICIAR_NAVEGADOR()
    pass