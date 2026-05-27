# Gabarito de acessos: Chave = ID do Acesso, Valor = Decisão Correta (True=Aprovar, False=Negar)
GABARITO_ACESSO = {
    "WIFI_MICROONDAS": False,  # Regra 2: Dispositivos de cozinha não homologados.
    "PASTA_CONFIDENCIAL": False,  # Regra 4: Analista pedindo acesso a pasta confidencial (apenas CEO).
    "PROTOCOLO_FELINO": False,  # Regra 3: Proibido uso de USB para ameaça felina.
    "ROOT_SERVER": True,  # Regra 4/Exceção: Gabe é CEO, logo tem acesso Root.
    "FORMAT_C": False,  # Regra 1: Suporte não pode dar comando de formatação destrutivo.
    "PORTA_FESTA": False  # Segurança Básica: Liberar porta 8080 para festa é falha crítica.
}


def verificar_decisao(acesso, decisao_jogador):
    # Pega a resposta correta no gabarito (por segurança, o padrão para acessos desconhecidos é Negar/False)
    decisao_correta = GABARITO_ACESSO.get(acesso, False)

    # Retorna True se o jogador fez a mesma coisa que o gabarito manda
    return decisao_correta == decisao_jogador