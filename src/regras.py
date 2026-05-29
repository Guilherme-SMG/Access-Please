GABARITO_ACESSO = {
    # DIA 1
    "WIFI_MICROONDAS": False,
    "PASTA_CONFIDENCIAL": False,
    "PROTOCOLO_FELINO": False,
    # DIA 2
    "ROOT_SERVER": True,
    "FORMAT_C": False,
    "PORTA_FESTA": False,
    # DIA 3
    "ACESSO_NOVO_1": False,
    "ACESSO_NOVO_2": True,
    "ACESSO_NOVO_3": False
}

def verificar_decisao(acesso, decisao_jogador):
    decisao_correta = GABARITO_ACESSO.get(acesso, False)
    return decisao_correta == decisao_jogador