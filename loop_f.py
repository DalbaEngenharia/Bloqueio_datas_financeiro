import json
from tratamento_datas import verificar_datas
from iniciar_bloqueio import iniciar_bloqueio

def loop_filiais(driver): 
    with open("json_teste.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    
    listas_de_bloqueio = []
    LIMITE_FINANCEIRO = dados['LIMITE_FINANCEIRO']
    LIMITE_FISCAL = dados['LIMITE_FISCAL']
    LIMITE_DEPRECIACAO = dados['LIMITE_DEPRECIACAO']
    LIMITE_MOVIMENTACAO = dados['LIMITE_MOVIMENTACAO']

    # LIMITE_FINANCEIRO = "32/08/2026"
    lista_dt = [LIMITE_FINANCEIRO, LIMITE_FISCAL, LIMITE_DEPRECIACAO,LIMITE_MOVIMENTACAO]

    
    resultado = verificar_datas(lista_dt)
    print(resultado)
    if resultado == "INSIRA UMA DATA EM UMA OPÇÂO": 
        return resultado
    if all(data == "" for data in resultado):
        print("Erro: é necessário informar pelo menos uma data.")
    else:
        print("Há pelo menos uma data informada.")
    for filial in dados["Filiais"]: 
        
        if len(filial) != 6: 
            print(filial, "-- nao bloqueia")
        else: 
            listas_de_bloqueio.append(filial)
            print(filial, "-- bloqueia")
    print(listas_de_bloqueio)
    iniciar_bloqueio(driver, listas_de_bloqueio, resultado)

    



