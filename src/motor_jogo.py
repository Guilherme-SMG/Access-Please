from src.regras import verificar_decisao


class MotorJogo:
    def __init__(self):
        self.dinheiro = 0
        self.strikes = 0
        self.max_strikes = 3
        self.salario_por_acerto = 50
        self.multa_por_erro = 20

        # --- NOVO: CONTROLE DE DIAS ---
        self.dia_atual = 1
        self.max_dias = 3

    def processar_decisao(self, acesso, decisao_jogador):
        acertou = verificar_decisao(acesso, decisao_jogador)

        if acertou:
            self.dinheiro += self.salario_por_acerto
            return True
        else:
            self.dinheiro -= self.multa_por_erro
            self.strikes += 1
            return False

    def verificar_game_over(self):
        return self.strikes >= self.max_strikes

    def avancar_dia(self):
        self.dia_atual += 1