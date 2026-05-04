import pygame
import sys

# Inicializa todas as bibliotecas internas do Pygame
pygame.init()

# Configurações básicas da tela
LARGURA = 1024
ALTURA = 768
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Access, Please - Terminal SOC")

# Define as cores
COR_FUNDO = (15, 15, 20)  # Motivo da tela preta

# FPS
relogio = pygame.time.Clock()


def main():
    rodando = True

    # Game Loop
    while rodando:
        # 1. Verifica os eventos (cliques, teclado, fechar janela)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # 2. Atualiza a lógica do jogo (aqui entrarão as regras depois)

        # 3. Desenha os elementos na tela
        TELA.fill(COR_FUNDO)  # Pinta o fundo a cada frame para limpar a tela

        # Atualiza o display para mostrar o que foi desenhado
        pygame.display.flip()

        # Crava o jogo em 60 FPS
        relogio.tick(60)

    # Encerra o Pygame corretamente quando sair do loop
    pygame.quit()
    sys.exit()


# Garante que o jogo só rode se este arquivo for executado diretamente
if __name__ == "__main__":
    main()