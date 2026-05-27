import pygame
import sys
import os
from src.ui import Desktop, MenuPrincipal, TelaBoot, TelaShutdown, TelaGameOver
from src.motor_jogo import MotorJogo

pygame.init()
pygame.mixer.init()  # Garante que o motor de áudio principal está rodando

LARGURA, ALTURA = 1024, 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()

# --- CARREGAMENTO DOS SONS DE DECISÃO ---
try:
    som_correto = pygame.mixer.Sound(os.path.join("assets", "sounds", "correto.mp3"))
    som_errado = pygame.mixer.Sound(os.path.join("assets", "sounds", "errado.mp3"))
    som_correto.set_volume(0.6)
    som_errado.set_volume(0.6)
except (FileNotFoundError, pygame.error):
    print("AVISO: Sons de 'correto' ou 'errado' não encontrados na pasta.")
    som_correto, som_errado = None, None

# --- CARREGAMENTO DA MÚSICA DE FUNDO (BGM) ---
try:
    pygame.mixer.music.load(os.path.join("assets", "sounds", "bgm.mp3"))
    # Volume bem baixo (20%) para ser só uma cama sonora que não cobre os cliques
    pygame.mixer.music.set_volume(0.2)
except (FileNotFoundError, pygame.error):
    print("AVISO: Arquivo 'bgm.mp3' não encontrado na pasta.")

desktop_os = Desktop(LARGURA, ALTURA)
motor = MotorJogo()

menu_principal = MenuPrincipal(LARGURA, ALTURA)
tela_boot = TelaBoot(LARGURA, ALTURA)
tela_shutdown = TelaShutdown(LARGURA, ALTURA)
tela_gameover = TelaGameOver(LARGURA, ALTURA)


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
                        desktop_os = Desktop(LARGURA, ALTURA)
                    elif acao == "SAIR":
                        rodando = False

            elif estado_jogo == "DESKTOP":
                retorno = desktop_os.tratar_eventos(evento)

                if retorno == "SHUTDOWN":
                    estado_jogo = "SHUTDOWN"
                    tela_shutdown.resetar()
                    # Dá um "fade out" (diminui o volume até zerar) em 1.5 segundos
                    pygame.mixer.music.fadeout(1500)

                elif isinstance(retorno, dict) and retorno.get("acao") == "DECISAO":
                    acertou = motor.processar_decisao(retorno["acesso"], retorno["decisao"])

                    if acertou and som_correto:
                        som_correto.play()
                    elif not acertou and som_errado:
                        som_errado.play()

                    if motor.verificar_game_over():
                        estado_jogo = "GAME_OVER"
                        tela_gameover.resetar()
                        # Corta a música de vez para dar impacto na tela de demissão!
                        pygame.mixer.music.stop()

        if estado_jogo == "MENU":
            menu_principal.desenhar(TELA)

        elif estado_jogo == "BOOT":
            if tela_boot.desenhar(TELA):
                estado_jogo = "DESKTOP"
                # O '-1' faz a música de fundo rodar em loop infinito enquanto o turno durar!
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

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()