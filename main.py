import pygame
import sys
# Adicionamos a TelaBoot no import
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

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if estado_jogo == "MENU":
                        acao = menu_principal.tratar_clique(evento.pos)
                        if acao == "INICIAR TURNO":
                            # Quando clica em iniciar, vai para a tela de transição
                            estado_jogo = "BOOT"
                            tela_boot.resetar()  # Garante que a animação comece do zero

                    elif estado_jogo == "DESKTOP":
                        desktop_os.tratar_clique(evento.pos)

        # DESENHO DA MÁQUINA DE ESTADOS
        if estado_jogo == "MENU":
            menu_principal.desenhar(TELA)

        elif estado_jogo == "BOOT":
            # A função desenhar da TelaBoot retorna True quando acaba
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