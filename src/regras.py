# Gabarito Oficial de Acessos SOC
GABARITO_ACESSO = {
    # --- DIA 1 ---
    "Core_do_Sistema": False,  # Erro: Regra 1 (Ameaça)
    "ONGs cadastradas": True,  # Acerto: Regra 3 (Boas intenções/banco restrito)
    "Dados não tão privados": False,  # Erro: Regra 5 (Dados privados)

    # --- DIA 2 ---
    "Estado do jogo \"Half Dead 3\"": True,  # Acerto: Regra 6 (Desenvolvedor Indie)
    "Solicitação de Acesso Emergencial": False,  # Erro: Regra 2 (Derrota Moral)
    "Livro de receitas Brasileiras": True,  # Acerto: Não fere regras

    # --- DIA 3 ---
    "Dados relevantes a minha pessoa": True,  # Acerto: Dados próprios, não fere regra 5
    "طلب رسمي للوصول إلى النظام الوطني": False,  # Erro: Regra 4 (Idioma estrangeiro)
    "Aquisição de Terreno": True  # Acerto: Boas intenções corporativas
}


def verificar_decisao(acesso, decisao_jogador):
    # Retorna o valor do gabarito. Se o acesso não existir, o padrão é negar (False) por segurança.
    decisao_correta = GABARITO_ACESSO.get(acesso, False)
    return decisao_correta == decisao_jogador