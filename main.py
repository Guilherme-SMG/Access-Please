import pygame
import sys
import os
from src.ui import Desktop, MenuPrincipal, TelaBoot, TelaShutdown, TelaGameOver, TelaFimExpediente, TelaVitoria
from src.motor_jogo import MotorJogo

pygame.init()
pygame.mixer.init()

LARGURA, ALTURA = 1024, 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()

try:
    som_correto = pygame.mixer.Sound(os.path.join("assets", "sounds", "correto.mp3"))
    som_errado = pygame.mixer.Sound(os.path.join("assets", "sounds", "errado.mp3"))
    som_correto.set_volume(0.6)
    som_errado.set_volume(0.6)
except (FileNotFoundError, pygame.error):
    som_correto, som_errado = None, None

try:
    pygame.mixer.music.load(os.path.join("assets", "sounds", "bgm.mp3"))
    pygame.mixer.music.set_volume(0.2)
except (FileNotFoundError, pygame.error):
    pass

motor = MotorJogo()
desktop_os = Desktop(LARGURA, ALTURA, motor.dia_atual)

menu_principal = MenuPrincipal(LARGURA, ALTURA)
tela_boot = TelaBoot(LARGURA, ALTURA)
tela_shutdown = TelaShutdown(LARGURA, ALTURA)
tela_gameover = TelaGameOver(LARGURA, ALTURA)
tela_fim_expediente = TelaFimExpediente(LARGURA, ALTURA)
tela_vitoria = TelaVitoria(LARGURA, ALTURA)


def main():
    global desktop_os, motor
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
                        motor = MotorJogo()
                        desktop_os = Desktop(LARGURA, ALTURA, motor.dia_atual)
                    elif acao == "SAIR":
                        rodando = False

            elif estado_jogo == "DESKTOP":
                retorno = desktop_os.tratar_eventos(evento)

                if retorno == "SHUTDOWN":
                    estado_jogo = "SHUTDOWN"
                    tela_shutdown.resetar()
                    pygame.mixer.music.fadeout(1500)

                elif isinstance(retorno, dict):
                    if retorno.get("acao") == "DECISAO":
                        acertou = motor.processar_decisao(retorno["acesso"], retorno["decisao"])

                        if acertou and som_correto:
                            som_correto.play()
                        elif not acertou and som_errado:
                            som_errado.play()

                        if motor.verificar_game_over():
                            estado_jogo = "GAME_OVER"
                            tela_gameover.resetar()
                            pygame.mixer.music.stop()

                            # --- A LÓGICA QUE FALTAVA ---
                    elif retorno.get("acao") == "ENCERRAR_DIA":
                        pygame.mixer.music.stop()
                        if motor.dia_atual < motor.max_dias:
                            estado_jogo = "FIM_DIA"
                        else:
                            estado_jogo = "VITORIA"

            elif estado_jogo == "FIM_DIA":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    acao = tela_fim_expediente.tratar_clique(evento.pos)
                    if acao == "PROXIMO_DIA":
                        motor.avancar_dia()
                        desktop_os = Desktop(LARGURA, ALTURA, motor.dia_atual)
                        estado_jogo = "BOOT"
                        tela_boot.resetar()

            elif estado_jogo == "VITORIA":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    acao = tela_vitoria.tratar_clique(evento.pos)
                    if acao == "MENU":
                        estado_jogo = "MENU"

        # --- LÓGICA DE DESENHO ---
        if estado_jogo == "MENU":
            menu_principal.desenhar(TELA)
        elif estado_jogo == "BOOT":
            if tela_boot.desenhar(TELA):
                estado_jogo = "DESKTOP"
                pygame.mixer.music.play(-1)
        elif estado_jogo == "DESKTOP":
            desktop_os.desenhar(TELA, motor.dinheiro, motor.strikes)
        elif estado_jogo == "SHUTDOWN":
            if tela_shutdown.desenhar(TELA):
                estado_jogo = "MENU"
        elif estado_jogo == "GAME_OVER":
            if tela_gameover.desenhar(TELA):
                estado_jogo = "SHUTDOWN"
                tela_shutdown.resetar()
        elif estado_jogo == "FIM_DIA":
            tela_fim_expediente.desenhar(TELA, motor.dia_atual, motor.dinheiro, motor.strikes)
        elif estado_jogo == "VITORIA":
            tela_vitoria.desenhar(TELA, motor.dinheiro)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()