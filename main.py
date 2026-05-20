import pygame
import sys
from src.ui import Desktop, MenuPrincipal, TelaBoot

pygame.init()

LARGURA = 1024
ALTURA = 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()

desktop_os = Desktop(LARGURA, ALTURA)
menu_principal = MenuPrincipal(LARGURA, ALTURA)
tela_boot = TelaBoot(LARGURA, ALTURA)


def main():
    rodando = True
    estado_jogo = "MENU"

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # Se for MENU, só ligamos para os cliques
            if estado_jogo == "MENU":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    acao = menu_principal.tratar_clique(evento.pos)
                    if acao == "INICIAR TURNO":
                        estado_jogo = "BOOT"
                        tela_boot.resetar()

                        # Se for DESKTOP, passamos o EVENTO INTEIRO (cliques, solturas e movimento)
            elif estado_jogo == "DESKTOP":
                desktop_os.tratar_eventos(evento)

        if estado_jogo == "MENU":
            menu_principal.desenhar(TELA)
        elif estado_jogo == "BOOT":
            animacao_terminou = tela_boot.desenhar(TELA)
            if animacao_terminou:
                estado_jogo = "DESKTOP"
        elif estado_jogo == "DESKTOP":
            desktop_os.desenhar(TELA)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()