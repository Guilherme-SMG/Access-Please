import pygame
import sys
from src.ui import Desktop, MenuPrincipal

pygame.init()

LARGURA = 1024
ALTURA = 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()

desktop_os = Desktop(LARGURA, ALTURA)
menu_principal = MenuPrincipal(LARGURA, ALTURA)


def main():
    rodando = True
    estado_jogo = "MENU"

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if estado_jogo == "MENU":
                        acao = menu_principal.tratar_clique(evento.pos)
                        if acao == "INICIAR TURNO":
                            estado_jogo = "DESKTOP"
                            print("SISTEMA INICIADO.")
                        elif acao == "SAIR":
                            rodando = False

                    elif estado_jogo == "DESKTOP":
                        desktop_os.tratar_clique(evento.pos)

        if estado_jogo == "MENU":
            menu_principal.desenhar(TELA)
        elif estado_jogo == "DESKTOP":
            desktop_os.desenhar(TELA)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()