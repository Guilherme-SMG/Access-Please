import pygame
import sys
from src.ui import Desktop, MenuPrincipal, TelaBoot, TelaShutdown

pygame.init()

LARGURA, ALTURA = 1024, 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()

desktop_os = Desktop(LARGURA, ALTURA)
menu_principal = MenuPrincipal(LARGURA, ALTURA)
tela_boot = TelaBoot(LARGURA, ALTURA)
tela_shutdown = TelaShutdown(LARGURA, ALTURA)  # Nossa nova tela clássica


def main():
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
                    elif acao == "SAIR":
                        rodando = False

            elif estado_jogo == "DESKTOP":
                # LÓGICA QUE FALTAVA: Capturar o sinal de Desligar do ui.py
                sinal = desktop_os.tratar_eventos(evento)
                if sinal == "SHUTDOWN":
                    estado_jogo = "SHUTDOWN"
                    tela_shutdown.resetar()

        # DESENHO E TRANSIÇÕES DE ESTADO
        if estado_jogo == "MENU":
            menu_principal.desenhar(TELA)
        elif estado_jogo == "BOOT":
            if tela_boot.desenhar(TELA):
                estado_jogo = "DESKTOP"
        elif estado_jogo == "DESKTOP":
            desktop_os.desenhar(TELA)
        elif estado_jogo == "SHUTDOWN":
            # Quando os 3 segundos de shutdown acabarem, ele volta para o MENU
            if tela_shutdown.desenhar(TELA):
                estado_jogo = "MENU"

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()