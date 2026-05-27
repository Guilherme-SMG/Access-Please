import pygame
import sys
from src.ui import Desktop, MenuPrincipal, TelaBoot, TelaShutdown, TelaGameOver
from src.motor_jogo import MotorJogo

pygame.init()

LARGURA, ALTURA = 1024, 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()

# Instâncias Iniciais (Serão resetadas ao iniciar o turno)
desktop_os = Desktop(LARGURA, ALTURA)
motor = MotorJogo()

menu_principal = MenuPrincipal(LARGURA, ALTURA)
tela_boot = TelaBoot(LARGURA, ALTURA)
tela_shutdown = TelaShutdown(LARGURA, ALTURA)
tela_gameover = TelaGameOver(LARGURA, ALTURA)  # Nova tela de punição!


def main():
    global desktop_os, motor  # Permite recriar essas variáveis ao reiniciar o turno
    rodando = True
    estado_jogo = "MENU"

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if estado_jogo == "MENU":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    acao = menu_principal.tratar_clique(evento.pos)
                    if acao == "INICIAR TURNO":
                        estado_jogo = "BOOT"
                        tela_boot.resetar()
                        # Reseta o progresso e o Desktop para um novo dia de trabalho
                        motor = MotorJogo()
                        desktop_os = Desktop(LARGURA, ALTURA)
                    elif acao == "SAIR":
                        rodando = False

            elif estado_jogo == "DESKTOP":
                # O Desktop agora pode retornar dicionários com as decisões tomadas
                retorno = desktop_os.tratar_eventos(evento)

                if retorno == "SHUTDOWN":
                    estado_jogo = "SHUTDOWN"
                    tela_shutdown.resetar()

                # Checa se o retorno é um dicionário (Decisão de Aprovar/Negar)
                elif isinstance(retorno, dict) and retorno.get("acao") == "DECISAO":
                    # Manda o acesso e a decisão (True/False) para o Cérebro do jogo
                    motor.processar_decisao(retorno["acesso"], retorno["decisao"])

                    # Checa se o jogador foi demitido (tomou 3 strikes)
                    if motor.verificar_game_over():
                        estado_jogo = "GAME_OVER"
                        tela_gameover.resetar()

        # --- DESENHO E TRANSIÇÕES DE ESTADO ---
        if estado_jogo == "MENU":
            menu_principal.desenhar(TELA)

        elif estado_jogo == "BOOT":
            if tela_boot.desenhar(TELA):
                estado_jogo = "DESKTOP"

        elif estado_jogo == "DESKTOP":
            # Passamos o dinheiro e os strikes para o Desktop desenhar no painel
            desktop_os.desenhar(TELA, motor.dinheiro, motor.strikes)

        elif estado_jogo == "SHUTDOWN":
            if tela_shutdown.desenhar(TELA):
                estado_jogo = "MENU"

        elif estado_jogo == "GAME_OVER":
            if tela_gameover.desenhar(TELA):
                estado_jogo = "SHUTDOWN"  # Toma Game Over e força o desligamento da máquina!
                tela_shutdown.resetar()

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()