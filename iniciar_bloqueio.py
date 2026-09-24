import biblioteca_protheus as bp
def iniciar_bloqueio(driver, filiais, datas): 
    print( filiais, datas)
    for filial in filiais: 
        if filial != filiais[0]:
            bp.funcao_tres_e_demais(driver,"wa-menu-item","Bloqueio")

        bp.inserir_texto(driver,"COMP4512",filial)
        bp.funcao_tres_e_demais(driver,"wa-button","Confirmar")
        ids_campos = ["COMP4504","COMP4507","COMP4510","COMP4513"]
        bp.esperar_existir(driver,"wa-button", "Ok")
        for x,id in enumerate(ids_campos): 
            if datas[x] != "": 
                bp.inserir_texto(driver, id, datas[x])
            print(x, "-- ", id)

        bp.funcao_tres_e_demais(driver,"wa-button","Ok")
        bp.log(f"TESTE----CANCELADO---SALVO{filial}--{datas}")
