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

        # --- CARREGAMENTO INTELIGENTE DE ÍCONES ---
        self.TAMANHO_MAX_ICONE = 52

        def carregar_e_escalar_proporcional(nome_arquivo):
            caminho = os.path.join("assets", "images", nome_arquivo)
            try:
                img = pygame.image.load(caminho).convert_alpha()
                w, h = img.get_size()
                maior_lado = max(w, h)
                fator = self.TAMANHO_MAX_ICONE / maior_lado
                novo_w = int(w * fator)
                novo_h = int(h * fator)
                return pygame.transform.scale(img, (novo_w, novo_h))
            except FileNotFoundError:
                print(f"ERRO: {nome_arquivo} não encontrado.")
                placeholder = pygame.Surface((self.TAMANHO_MAX_ICONE, self.TAMANHO_MAX_ICONE))
                placeholder.fill((255, 0, 255))
                return placeholder

        self.img_carreira = carregar_e_escalar_proporcional("icone_carreira.png")
        self.img_regras = carregar_e_escalar_proporcional("icone_regras.png")
        self.img_email = carregar_e_escalar_proporcional("icone_email.png")
        self.img_pasta = carregar_e_escalar_proporcional("icone_pasta.png")
        self.img_terminal = carregar_e_escalar_proporcional("icone_terminal.png")
        self.img_halfdead = carregar_e_escalar_proporcional("icone_halfdead.png")

        # --- VARIÁVEIS DE ESTADO E COLISÃO ---
        self.hitboxes = {}
        self.menu_aberto = False

        # Estado das Janelas
        self.janela_aberta = None
        self.hitbox_fechar_janela = None
        self.hitbox_fundo_janela = None

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

        self.hitboxes["Botao Doors"] = pygame.Rect(x_botoes, y_botoes, largura_botao, altura_botao)
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, self.hitboxes["Botao Doors"])

        if self.menu_aberto:
            pygame.draw.line(tela, COR_BOTAO, (x_botoes, y_botoes), (x_botoes + largura_botao, y_botoes), 2)
            pygame.draw.line(tela, COR_BOTAO, (x_botoes, y_botoes), (x_botoes, y_botoes + altura_botao), 2)
            pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_botoes + largura_botao, y_botoes),
                             (x_botoes + largura_botao, y_botoes + altura_botao), 2)
            pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_botoes, y_botoes + altura_botao),
                             (x_botoes + largura_botao, y_botoes + altura_botao), 2)
        else:
            pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_botoes, y_botoes), (x_botoes + largura_botao, y_botoes), 2)
            pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_botoes, y_botoes), (x_botoes, y_botoes + altura_botao), 2)
            pygame.draw.line(tela, COR_BOTAO, (x_botoes + largura_botao, y_botoes),
                             (x_botoes + largura_botao, y_botoes + altura_botao), 2)
            pygame.draw.line(tela, COR_BOTAO, (x_botoes, y_botoes + altura_botao),
                             (x_botoes + largura_botao, y_botoes + altura_botao), 2)

        tela.blit(self.mini_logo, (x_botoes + 6, y_botoes + 3))
        texto_doors = pygame.font.SysFont("tahoma", 16, bold=True).render("Doors", True, COR_TEXTO)
        tela.blit(texto_doors, (x_botoes + 35, y_botoes + 6))

        # --- RELÓGIO DA BARRA DE TAREFAS ---
        agora = datetime.now()
        texto_relogio = agora.strftime("%H:%M   %d/%m/%Y")
        superficie_relogio = self.fonte_padrao.render(texto_relogio, True, COR_TEXTO)

        largura_tray = superficie_relogio.get_width() + 20
        altura_tray = 26
        x_tray = self.largura - largura_tray - 5
        y_tray = self.altura - altura_barra + 7

        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_tray, y_tray, largura_tray, altura_tray))
        pygame.draw.line(tela, COR_BOTAO, (x_tray, y_tray), (x_tray + largura_tray, y_tray), 2)
        pygame.draw.line(tela, COR_BOTAO, (x_tray, y_tray), (x_tray, y_tray + altura_tray), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_tray, y_tray + altura_tray),
                         (x_tray + largura_tray, y_tray + altura_tray), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_tray + largura_tray, y_tray),
                         (x_tray + largura_tray, y_tray + altura_tray), 2)

        tela.blit(superficie_relogio, (x_tray + 10, y_tray + 4))

        # --- ÍCONES DA ÁREA DE TRABALHO ---
        centro_coluna_1 = 60
        centro_coluna_2 = 180
        start_y = 30
        espacamento_y = 110

        self.hitboxes["Minha Carreira"] = self.desenhar_icone_centralizado(tela, centro_coluna_1, start_y,
                                                                           "Minha Carreira", self.img_carreira)
        self.hitboxes["OutVision"] = self.desenhar_icone_centralizado(tela, centro_coluna_1, start_y + espacamento_y,
                                                                      "OutVision", self.img_email)
        self.hitboxes["Terminal SOC"] = self.desenhar_icone_centralizado(tela, centro_coluna_1,
                                                                         start_y + (espacamento_y * 2), "Terminal SOC",
                                                                         self.img_terminal)

        self.hitboxes["Regras"] = self.desenhar_icone_centralizado(tela, centro_coluna_2, start_y, "Regras",
                                                                   self.img_regras)
        self.hitboxes["Arquivos"] = self.desenhar_icone_centralizado(tela, centro_coluna_2, start_y + espacamento_y,
                                                                     "Arquivos", self.img_pasta)
        self.hitboxes["Half Dead 3"] = self.desenhar_icone_centralizado(tela, centro_coluna_2,
                                                                        start_y + (espacamento_y * 2), "Half Dead 3",
                                                                        self.img_halfdead)

        # --- DESENHA A JANELA (SE HOUVER ALGUMA ABERTA) ---
        if self.janela_aberta:
            self.desenhar_janela(tela)

        # --- DESENHA O MENU INICIAR ---
        if self.menu_aberto:
            self.desenhar_menu_iniciar(tela)

    def desenhar_icone_centralizado(self, tela, centro_x, y, nome, imagem):
        largura_img = imagem.get_width()
        altura_img = imagem.get_height()
        pos_img_x = centro_x - (largura_img // 2)
        tela.blit(imagem, (pos_img_x, y))

        texto_sombra = self.fonte_padrao.render(nome, True, (0, 0, 0))
        texto = self.fonte_padrao.render(nome, True, COR_TEXTO_ICONE)

        pos_texto_x = centro_x - (texto.get_width() // 2)
        pos_texto_y = y + self.TAMANHO_MAX_ICONE + 5

        tela.blit(texto_sombra, (pos_texto_x + 1, pos_texto_y + 1))
        tela.blit(texto, (pos_texto_x, pos_texto_y))

        return pygame.Rect(pos_img_x, y, largura_img, altura_img)

    def desenhar_janela(self, tela):
        largura_janela = 600
        altura_janela = 450
        x_janela = (self.largura / 2) - (largura_janela / 2)
        y_janela = (self.altura / 2) - (altura_janela / 2)

        self.hitbox_fundo_janela = pygame.Rect(x_janela, y_janela, largura_janela, altura_janela)

        # Fundo e Bordas
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, self.hitbox_fundo_janela)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_janela, y_janela), (x_janela + largura_janela, y_janela), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_janela, y_janela), (x_janela, y_janela + altura_janela), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_janela + largura_janela, y_janela),
                         (x_janela + largura_janela, y_janela + altura_janela), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_janela, y_janela + altura_janela),
                         (x_janela + largura_janela, y_janela + altura_janela), 2)

        # Barra de Título
        altura_titulo = 25
        pygame.draw.rect(tela, (0, 0, 128), (x_janela + 3, y_janela + 3, largura_janela - 6, altura_titulo))

        # Texto do Título
        fonte_titulo = pygame.font.SysFont("tahoma", 14, bold=True)
        texto_titulo = fonte_titulo.render(self.janela_aberta, True, COR_BOTAO_BRIGHT)
        tela.blit(texto_titulo, (x_janela + 8, y_janela + 7))

        # Botão [X]
        tamanho_x = 21
        x_fechar = x_janela + largura_janela - tamanho_x - 5
        y_fechar = y_janela + 5
        self.hitbox_fechar_janela = pygame.Rect(x_fechar, y_fechar, tamanho_x, tamanho_x)

        pygame.draw.rect(tela, COR_BARRA_TAREFAS, self.hitbox_fechar_janela)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_fechar, y_fechar), (x_fechar + tamanho_x, y_fechar), 1)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_fechar, y_fechar), (x_fechar, y_fechar + tamanho_x), 1)
        pygame.draw.line(tela, COR_TEXTO, (x_fechar + tamanho_x, y_fechar),
                         (x_fechar + tamanho_x, y_fechar + tamanho_x), 1)
        pygame.draw.line(tela, COR_TEXTO, (x_fechar, y_fechar + tamanho_x),
                         (x_fechar + tamanho_x, y_fechar + tamanho_x), 1)

        tela.blit(fonte_titulo.render("X", True, COR_TEXTO), (x_fechar + 6, y_fechar + 2))

    def desenhar_menu_iniciar(self, tela):
        largura_menu = 220
        altura_menu = 320
        x_menu = 0
        y_menu = self.altura - 40 - altura_menu

        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_menu, y_menu, largura_menu, altura_menu))
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_menu, y_menu), (x_menu + largura_menu, y_menu), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_menu, y_menu), (x_menu, y_menu + altura_menu), 2)
        pygame.draw.line(tela, COR_BOTAO, (x_menu + largura_menu, y_menu),
                         (x_menu + largura_menu, y_menu + altura_menu), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_menu + largura_menu + 1, y_menu),
                         (x_menu + largura_menu + 1, y_menu + altura_menu), 1)

        pygame.draw.rect(tela, (0, 0, 128), (x_menu + 2, y_menu + 2, 35, altura_menu - 4))

        texto_rotacionado = pygame.transform.rotate(
            pygame.font.SysFont("tahoma", 20, bold=True).render("Doors OS", True, COR_BOTAO_BRIGHT), 90)
        tela.blit(texto_rotacionado, (x_menu + 7, y_menu + altura_menu - texto_rotacionado.get_height() - 10))

        itens = ["Programas", "Documentos", "Configurações", "Pesquisar", "Ajuda", "Desligar..."]
        y_item = y_menu + 20
        for item in itens:
            tela.blit(self.fonte_padrao.render(item, True, COR_TEXTO), (x_menu + 50, y_item))
            if item == "Ajuda":
                y_linha = y_item + 30
                pygame.draw.line(tela, COR_BOTAO, (x_menu + 50, y_linha), (x_menu + largura_menu - 10, y_linha), 1)
                pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_menu + 50, y_linha + 1),
                                 (x_menu + largura_menu - 10, y_linha + 1), 1)
                y_item += 10
            y_item += 40

    def tratar_clique(self, pos_mouse):
        if self.janela_aberta:
            if self.hitbox_fechar_janela and self.hitbox_fechar_janela.collidepoint(pos_mouse):
                print(f"Fechando janela: {self.janela_aberta}")
                self.janela_aberta = None
                return "Fechou Janela"
            elif self.hitbox_fundo_janela and self.hitbox_fundo_janela.collidepoint(pos_mouse):
                return "Clique na janela"

        clicou_em_algo = False
        for nome_icone, hitbox in self.hitboxes.items():
            if hitbox.collidepoint(pos_mouse):
                clicou_em_algo = True

                if nome_icone == "Botao Doors":
                    self.menu_aberto = not self.menu_aberto
                else:
                    self.menu_aberto = False
                    print(f"Abrindo aplicativo: {nome_icone}")
                    self.janela_aberta = nome_icone

                return nome_icone

        if not clicou_em_algo:
            self.menu_aberto = False

        return None


class MenuPrincipal:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        # Fontes mais pesadas e burocráticas
        self.fonte_titulo = pygame.font.SysFont("impact", 90)
        self.fonte_botoes = pygame.font.SysFont("impact", 40)
        self.hitboxes = {}

    def desenhar(self, tela):
        # Fundo quase totalmente preto (clima pesado)
        tela.fill((15, 15, 18))

        # --- TÍTULO ---
        texto_sombra = self.fonte_titulo.render("ACCESS, PLEASE", True, (40, 0, 0))
        texto_titulo = self.fonte_titulo.render("ACCESS, PLEASE", True, (200, 40, 40))

        pos_x_titulo = (self.largura // 2) - (texto_titulo.get_width() // 2)
        tela.blit(texto_sombra, (pos_x_titulo + 5, 105))
        tela.blit(texto_titulo, (pos_x_titulo, 100))

        # --- BOTÕES ---
        textos_botoes = ["INICIAR TURNO", "SAIR"]
        y_atual = 400
        self.hitboxes.clear()

        for texto in textos_botoes:
            superficie_texto = self.fonte_botoes.render(texto, True, (220, 220, 220))
            retangulo_texto = superficie_texto.get_rect(center=(self.largura // 2, y_atual))
            retangulo_botao = retangulo_texto.inflate(60, 20)

            pygame.draw.rect(tela, (40, 40, 40), retangulo_botao)
            pygame.draw.rect(tela, (100, 100, 100), retangulo_botao, 3)
            tela.blit(superficie_texto, retangulo_texto)

            self.hitboxes[texto] = retangulo_botao
            y_atual += 100

    def tratar_clique(self, pos_mouse):
        for acao, hitbox in self.hitboxes.items():
            if hitbox.collidepoint(pos_mouse):
                return acao
        return None