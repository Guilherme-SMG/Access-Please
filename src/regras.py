# Gabarito Oficial de Acessos SOC
GABARITO_ACESSO = {
    # --- DIA 1 ---
    "Core_do_Sistema": False,
    "ONGs cadastradas": True,
    "Dados não tão privados": False,

    # --- DIA 2 ---
    "Estado do jogo \"Half Dead 3\"": True,
    "Solicitação de Acesso Emergencial": False,
    "Livro de receitas Brasileiras": True,

    # --- DIA 3 ---
    "Dados relevantes a minha pessoa": True,
    "طلب رسمي للوصول إلى النظام الوطني": False,
    "Aquisição de Terreno": True
}


def verificar_decisao(acesso, decisao_jogador):
    decisao_correta = GABARITO_ACESSO.get(acesso, False)
    return decisao_correta == decisao_jogador