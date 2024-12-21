import ast


def acionador(passo):
    
    acao      = passo['acao'      ] 
    ordem     = passo['ordem'     ] 
    variavel1 = passo['variavel1' ] 
    variavel2 = passo['variavel2' ] 
    variavel3 = passo['variavel3' ] 
    variavel4 = passo['variavel4' ] 
    variavel5 = passo['variavel5' ] 

    try:
        varia_dicts = ast.literal_eval(variavel1)
    except:
        varia_dicts = None
    retorno = {}


    funcao = globals().get(f"func_{acao}")  # Use locals() se estiver dentro de um escopo fechado
    if callable(funcao):
        resp_func = funcao()  # Chama a função
    else:
        print(f"A função '{acao}' não foi encontrada ou não é executável.")


    if variavel5 == 'SUB_LOOP':
        retorno['SITUACAO']='SUB_LOOP'
        retorno['NU_PROX_PASSO'] = varia_dicts[resp_func]
    else:
        retorno['SITUACAO']='FINALIZADO'


    return retorno

def sub_loop(passo_atual):
    passos = ''
    retorno = acionador(passo_atual)
    if retorno['SITUACAO'] == 'SUB_LOOP': 
        nu_prox_passo = retorno['NU_PROX_PASSO'] 
        prox_passo = passos['acoes'][str(nu_prox_passo)]
        retorno = acionador(prox_passo)
    else:
        return retorno







def func_INICIA_NAVEGADOR   ():
    return 'OK'

def func_DORME              ():
    return 'OK'

def func_VERIFICA_NAVEGADOR ():
    return 'NAO'

def func_DORME              ():
    return 'OK'

def func_PASS               ():
    return 'OK'

def func_INICIA_NAVEGADOR   ():
    return 'OK'

def func_FINALIZA_NAVEGADOR ():
    return 'OK'

def func_DORME              ():
    return 'OK'

def func_FIM_DA_ROTINA      ():
    return 'OK'


