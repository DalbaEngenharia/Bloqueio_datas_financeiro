from datetime import datetime

def verificar_datas(lista_dt): 
    LIMITE_FINANCEIRO = lista_dt[0]
    LIMITE_FISCAL = lista_dt[1]
    LIMITE_DEPRECIAÇÃO = lista_dt[2]
    LIMITE_MOVIMENTAÇÃO = lista_dt[3]

    if (
        LIMITE_FINANCEIRO == "" and
        LIMITE_FISCAL== "" and
        LIMITE_DEPRECIAÇÃO == "" and
        LIMITE_MOVIMENTAÇÃO == ""
        ): 
        return "INSIRA UMA DATA EM UMA OPÇÂO" 

    lista_datas_validas = []
    for data in lista_dt: 
        try:
            datetime.strptime(data, "%d/%m/%Y")
            lista_datas_validas.append(data)
            print(data, "True")
         
        except ValueError:
            lista_datas_validas.append("")
            print(data, "False")
    return lista_datas_validas
            