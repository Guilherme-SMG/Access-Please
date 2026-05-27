from src.regras import verificar_decisao

class MotorJogo:
    def __init__(self):
        self.dinheiro = 0
        self.strikes = 0
        self.max_strikes = 3
        self.salario_por_acerto = 50
        self.multa_por_erro = 20

    def processar_decisao(self, acesso, decisao_jogador):
        # Avalia se a decisão do jogador bate com o regras.py
        acertou = verificar_decisao(acesso, decisao_jogador)

        if acertou:
            self.dinheiro += self.salario_por_acerto
            return True # Opcional: usaremos isso no futuro para tocar um som de "Caixa Registradora"
        else:
            self.dinheiro -= self.multa_por_erro
            self.strikes += 1
            return False # Opcional: usaremos isso no futuro para tocar um som de "Erro"

    def verificar_game_over(self):
        # Checa se o jogador atingiu o limite de advertências
        return self.strikes >= self.max_strikes