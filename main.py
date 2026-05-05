import pygame
import sys
from src.ui import Desktop

pygame.init()

LARGURA = 1024
ALTURA = 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()
desktop_os = Desktop(LARGURA, ALTURA)


def main():
    rodando = True

    while rodando:
        # 1. Verifica Eventos (Ouvidos do Jogo)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # NOVO: Escutando o clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # 1 é o botão esquerdo do mouse
                    # Posição exata (X, Y) do clique para o Desktop analisar
                    desktop_os.tratar_clique(evento.pos)

        # 2. Desenha os elementos na tela
        desktop_os.desenhar(TELA)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()