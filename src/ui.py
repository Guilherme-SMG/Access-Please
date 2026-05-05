import pygame
import os
from datetime import datetime

# Paleta de Cores Clássica (Doors OS 95 Edition)
COR_FUNDO_DESKTOP = (0, 128, 128)
COR_BARRA_TAREFAS = (192, 192, 192)
COR_BOTAO = (128, 128, 128)
COR_BOTAO_BRIGHT = (255, 255, 255)
COR_TEXTO = (0, 0, 0)
COR_TEXTO_ICONE = (255, 255, 255)


class Desktop:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_padrao = pygame.font.SysFont("tahoma", 13)

        # --- LOGO DO BOTAO DOORS ---
        caminho_logo = os.path.join("assets", "images", "doors_logo.png")
        self.logo_original = pygame.image.load(caminho_logo).convert_alpha()
        self.mini_logo = pygame.transform.scale(self.logo_original, (24, 24))

        # --- CARREGAMENTO INTELIGENTE DE ÍCONES (Mantendo Proporção) ---
        self.TAMANHO_MAX_ICONE = 52  # Tamanho máximo que um lado do ícone pode ter

        def carregar_e_escalar_proporcional(nome_arquivo):
            caminho = os.path.join("assets", "images", nome_arquivo)
            try:
                img = pygame.image.load(caminho).convert_alpha()
                w, h = img.get_size()
                # Descobre qual é o maior lado e calcula o fator de escala
                maior_lado = max(w, h)
                fator = self.TAMANHO_MAX_ICONE / maior_lado
                novo_w = int(w * fator)
                novo_h = int(h * fator)
                return pygame.transform.scale(img, (novo_w, novo_h))
            except FileNotFoundError:
                print(f"ERRO: {nome_arquivo} não encontrado.")
                placeholder = pygame.Surface((self.TAMANHO_MAX_ICONE, self.TAMANHO_MAX_ICONE))
                placeholder.fill((255, 0, 255))  # Rosa choque para avisar do erro
                return placeholder

        # Carregando as imagens
        self.img_carreira = carregar_e_escalar_proporcional("icone_carreira.png")
        self.img_regras = carregar_e_escalar_proporcional("icone_regras.png")
        self.img_email = carregar_e_escalar_proporcional("icone_email.png")
        self.img_pasta = carregar_e_escalar_proporcional("icone_pasta.png")
        self.img_terminal = carregar_e_escalar_proporcional("icone_terminal.png")
        self.img_halfdead = carregar_e_escalar_proporcional("icone_halfdead.png")

    def desenhar(self, tela):
        # 1. Papel de Parede
        tela.fill(COR_FUNDO_DESKTOP)

        # 2. Barra de Tarefas
        altura_barra = 40
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (0, self.altura - altura_barra, self.largura, altura_barra))
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (0, self.altura - altura_barra),
                         (self.largura, self.altura - altura_barra), 2)

        # 3. Botão "Doors"
        x_botoes = 5
        y_botoes = self.altura - altura_barra + 5
        largura_botao = 90
        altura_botao = 30
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_botoes, y_botoes, largura_botao, altura_botao))
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_botoes, y_botoes), (x_botoes + largura_botao, y_botoes), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_botoes, y_botoes), (x_botoes, y_botoes + altura_botao), 2)
        pygame.draw.line(tela, COR_BOTAO, (x_botoes + largura_botao, y_botoes),
                         (x_botoes + largura_botao, y_botoes + altura_botao), 2)
        pygame.draw.line(tela, COR_BOTAO, (x_botoes, y_botoes + altura_botao),
                         (x_botoes + largura_botao, y_botoes + altura_botao), 2)
        tela.blit(self.mini_logo, (x_botoes + 6, y_botoes + 3))
        texto_doors = pygame.font.SysFont("tahoma", 16, bold=True).render("Doors", True, COR_TEXTO)
        tela.blit(texto_doors, (x_botoes + 35, y_botoes + 6))

        # --- RELÓGIO DA BARRA DE TAREFAS (SYSTEM TRAY) ---
        # Pegando a hora e formatando (ex: 10:18   05/05/2026)
        agora = datetime.now()
        texto_relogio = agora.strftime("%H:%M   %d/%m/%Y")
        superficie_relogio = self.fonte_padrao.render(texto_relogio, True, COR_TEXTO)

        # Calculando o tamanho da caixinha baseado no tamanho do texto
        largura_tray = superficie_relogio.get_width() + 20
        altura_tray = 26
        x_tray = self.largura - largura_tray - 5
        y_tray = self.altura - altura_barra + 7

        # Efeito 3D "Afundado" (Inset)
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_tray, y_tray, largura_tray, altura_tray))
        pygame.draw.line(tela, COR_BOTAO, (x_tray, y_tray), (x_tray + largura_tray, y_tray), 2)  # Topo escuro
        pygame.draw.line(tela, COR_BOTAO, (x_tray, y_tray), (x_tray, y_tray + altura_tray), 2)  # Esquerda escura
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_tray, y_tray + altura_tray),
                         (x_tray + largura_tray, y_tray + altura_tray), 2)  # Baixo branco
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_tray + largura_tray, y_tray),
                         (x_tray + largura_tray, y_tray + altura_tray), 2)  # Direita branca

        # Colocando o texto do relógio dentro da caixinha
        pos_relogio_x = x_tray + 10
        pos_relogio_y = y_tray + 4
        tela.blit(superficie_relogio, (pos_relogio_x, pos_relogio_y))

        # --- ÍCONES ALINHADOS PELO CENTRO ---
        centro_coluna_1 = 60
        centro_coluna_2 = 180

        start_y = 30
        espacamento_y = 110

        # Coluna 1
        self.desenhar_icone_centralizado(tela, centro_coluna_1, start_y, "Minha Carreira", self.img_carreira)
        self.desenhar_icone_centralizado(tela, centro_coluna_1, start_y + espacamento_y, "OutVision", self.img_email)
        self.desenhar_icone_centralizado(tela, centro_coluna_1, start_y + (espacamento_y * 2), "Terminal SOC",
                                         self.img_terminal)

        # Coluna 2
        self.desenhar_icone_centralizado(tela, centro_coluna_2, start_y, "Regras", self.img_regras)
        self.desenhar_icone_centralizado(tela, centro_coluna_2, start_y + espacamento_y, "Arquivos", self.img_pasta)
        self.desenhar_icone_centralizado(tela, centro_coluna_2, start_y + (espacamento_y * 2), "Half Dead 3",
                                         self.img_halfdead)

    def desenhar_icone_centralizado(self, tela, centro_x, y, nome, imagem):
        largura_img = imagem.get_width()

        # Desenha a imagem centralizada no X
        pos_img_x = centro_x - (largura_img // 2)
        tela.blit(imagem, (pos_img_x, y))

        # Renderiza o texto e a sombra
        texto_sombra = self.fonte_padrao.render(nome, True, (0, 0, 0))
        texto = self.fonte_padrao.render(nome, True, COR_TEXTO_ICONE)
        largura_texto = texto.get_width()

        # Desenha o texto centralizado no X, logo abaixo do espaço máximo da imagem
        pos_texto_x = centro_x - (largura_texto // 2)
        pos_texto_y = y + self.TAMANHO_MAX_ICONE + 5

        tela.blit(texto_sombra, (pos_texto_x + 1, pos_texto_y + 1))
        tela.blit(texto, (pos_texto_x, pos_texto_y))