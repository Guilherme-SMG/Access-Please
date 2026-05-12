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

        # --- VARIÁVEIS DE ESTADO E COLISÃO ---
        # Dicionário para guardar as Hitboxes de cada ícone e do botão Iniciar
        self.hitboxes = {}
        # Estado do Menu Iniciar (Começa fechado)
        self.menu_aberto = False

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

        # Salvando a Hitbox do botão Doors
        self.hitboxes["Botao Doors"] = pygame.Rect(x_botoes, y_botoes, largura_botao, altura_botao)

        pygame.draw.rect(tela, COR_BARRA_TAREFAS, self.hitboxes["Botao Doors"])

        # Efeito de botão "apertado" se o menu estiver aberto, ou normal se estiver fechado
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

        # --- RELÓGIO DA BARRA DE TAREFAS (SYSTEM TRAY) ---
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

        pos_relogio_x = x_tray + 10
        pos_relogio_y = y_tray + 4
        tela.blit(superficie_relogio, (pos_relogio_x, pos_relogio_y))

        # --- ÍCONES ALINHADOS PELO CENTRO ---
        centro_coluna_1 = 60
        centro_coluna_2 = 180

        start_y = 30
        espacamento_y = 110

        # Guardando as Hitboxes retornadas no dicionário
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

        # --- DESENHA O MENU INICIAR (POR CIMA DE TUDO) ---
        if self.menu_aberto:
            self.desenhar_menu_iniciar(tela)

    def desenhar_icone_centralizado(self, tela, centro_x, y, nome, imagem):
        largura_img = imagem.get_width()
        altura_img = imagem.get_height()

        pos_img_x = centro_x - (largura_img // 2)
        tela.blit(imagem, (pos_img_x, y))

        texto_sombra = self.fonte_padrao.render(nome, True, (0, 0, 0))
        texto = self.fonte_padrao.render(nome, True, COR_TEXTO_ICONE)
        largura_texto = texto.get_width()

        pos_texto_x = centro_x - (largura_texto // 2)
        pos_texto_y = y + self.TAMANHO_MAX_ICONE + 5

        tela.blit(texto_sombra, (pos_texto_x + 1, pos_texto_y + 1))
        tela.blit(texto, (pos_texto_x, pos_texto_y))

        # Cria e retorna um Retângulo invisível que cobre a imagem
        return pygame.Rect(pos_img_x, y, largura_img, altura_img)

    def tratar_clique(self, pos_mouse):
        clicou_em_algo = False

        for nome_icone, hitbox in self.hitboxes.items():
            if hitbox.collidepoint(pos_mouse):
                clicou_em_algo = True

                # Se clicou no Botão Doors, inverte o menu (Abre/Fecha)
                if nome_icone == "Botao Doors":
                    self.menu_aberto = not self.menu_aberto
                    print("Menu Doors: ", "ABERTO" if self.menu_aberto else "FECHADO")
                else:
                    # Se clicou em outro ícone, fecha o menu e avisa o que abriu
                    self.menu_aberto = False
                    print(f"CLIQUE DETECTADO: Você abriu {nome_icone}")

                return nome_icone

        # Se clicou no vazio (fundo da tela), apenas fecha o menu
        if not clicou_em_algo:
            self.menu_aberto = False

        return None

    def desenhar_menu_iniciar(self, tela):
        largura_menu = 220
        altura_menu = 320
        x_menu = 0
        # O Y é calculado para ficar exatamente em cima da barra de tarefas
        y_menu = self.altura - 40 - altura_menu

        # 1. Fundo e Borda 3D do Menu
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_menu, y_menu, largura_menu, altura_menu))
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_menu, y_menu), (x_menu + largura_menu, y_menu), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_menu, y_menu), (x_menu, y_menu + altura_menu), 2)
        pygame.draw.line(tela, COR_BOTAO, (x_menu + largura_menu, y_menu),
                         (x_menu + largura_menu, y_menu + altura_menu), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_menu + largura_menu + 1, y_menu),
                         (x_menu + largura_menu + 1, y_menu + altura_menu), 1)

        # 2. A Faixa Lateral Azul Clássica
        largura_faixa = 35
        cor_faixa = (0, 0, 128)  # Azul marinho
        pygame.draw.rect(tela, cor_faixa, (x_menu + 2, y_menu + 2, largura_faixa, altura_menu - 4))

        # 3. O Texto "Doors OS" rotacionado 90 graus
        fonte_faixa = pygame.font.SysFont("tahoma", 20, bold=True)
        texto_faixa = fonte_faixa.render("Doors OS", True, COR_BOTAO_BRIGHT)
        texto_rotacionado = pygame.transform.rotate(texto_faixa, 90)  # Gira o texto para cima
        # Posiciona o texto colado no canto inferior da faixa azul
        tela.blit(texto_rotacionado, (x_menu + 7, y_menu + altura_menu - texto_rotacionado.get_height() - 10))

        # 4. Itens do Menu (Apenas visuais por enquanto)
        itens = ["Programas", "Documentos", "Configurações", "Pesquisar", "Ajuda", "Desligar..."]
        y_item = y_menu + 20
        x_item = x_menu + 50

        for item in itens:
            texto_item = self.fonte_padrao.render(item, True, COR_TEXTO)
            tela.blit(texto_item, (x_item, y_item))

            # Desenha uma linha separadora antes do botão "Desligar"
            if item == "Ajuda":
                y_linha = y_item + 30
                pygame.draw.line(tela, COR_BOTAO, (x_item, y_linha), (x_menu + largura_menu - 10, y_linha), 1)
                pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_item, y_linha + 1),
                                 (x_menu + largura_menu - 10, y_linha + 1), 1)
                y_item += 10  # Pula um espacinho extra

            y_item += 40