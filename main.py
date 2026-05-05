import pygame
import sys
# Aqui estamos importando a classe que acabamos de criar!
from src.ui import Desktop

pygame.init()

LARGURA = 1024
ALTURA = 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

relogio = pygame.time.Clock()

# Instanciamos o nosso Desktop passando o tamanho da tela
desktop_os = Desktop(LARGURA, ALTURA)


def main():
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # 3. Desenha os elementos na tela (Apagamos o fill() escuro e colocamos isso)
        desktop_os.desenhar(TELA)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()