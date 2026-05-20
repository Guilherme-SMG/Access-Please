import pygame
import os
from datetime import datetime

COR_FUNDO_DESKTOP = (0, 128, 128)
COR_BARRA_TAREFAS = (192, 192, 192)
COR_BOTAO = (128, 128, 128)
COR_BOTAO_BRIGHT = (255, 255, 255)
COR_TEXTO = (0, 0, 0)
COR_TEXTO_ICONE = (255, 255, 255)
COR_TERMINAL = (0, 230, 0)


class Desktop:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_padrao = pygame.font.SysFont("tahoma", 13)
        self.fonte_terminal = pygame.font.SysFont("couriernew", 14, bold=True)

        caminho_logo = os.path.join("assets", "images", "doors_logo.png")
        self.logo_original = pygame.image.load(caminho_logo).convert_alpha()
        self.mini_logo = pygame.transform.scale(self.logo_original, (24, 24))

        self.TAMANHO_MAX_ICONE = 52

        def carregar_e_escalar_proporcional(nome_arquivo):
            caminho = os.path.join("assets", "images", nome_arquivo)
            try:
                img = pygame.image.load(caminho).convert_alpha()
                w, h = img.get_size()
                maior_lado = max(w, h)
                fator = self.TAMANHO_MAX_ICONE / maior_lado
                return pygame.transform.scale(img, (int(w * fator), int(h * fator)))
            except FileNotFoundError:
                placeholder = pygame.Surface((self.TAMANHO_MAX_ICONE, self.TAMANHO_MAX_ICONE))
                placeholder.fill((255, 0, 255))
                return placeholder

        self.img_carreira = carregar_e_escalar_proporcional("icone_carreira.png")
        self.img_regras = carregar_e_escalar_proporcional("icone_regras.png")
        self.img_email = carregar_e_escalar_proporcional("icone_email.png")
        self.img_pasta = carregar_e_escalar_proporcional("icone_pasta.png")
        self.img_terminal = carregar_e_escalar_proporcional("icone_terminal.png")
        self.img_halfdead = carregar_e_escalar_proporcional("icone_halfdead.png")

        self.hitboxes = {}
        self.menu_aberto = False

        # --- NOVO GERENCIADOR DE MÚLTIPLAS JANELAS ---
        self.janelas_abertas = []  # Lista que dita a ordem de desenho (o último fica por cima)
        self.janelas_pos = {}  # Dicionário: nome_app -> [x, y]
        self.janela_arrastada = None  # Nome do app sendo arrastado
        self.offset_x = 0
        self.offset_y = 0

        TAMANHO_AVATAR = 80

        def carregar_avatar(nome_arquivo):
            caminho = os.path.join("assets", "images", nome_arquivo)
            try:
                img = pygame.image.load(caminho).convert()
                return pygame.transform.scale(img, (TAMANHO_AVATAR, TAMANHO_AVATAR))
            except FileNotFoundError:
                placeholder = pygame.Surface((TAMANHO_AVATAR, TAMANHO_AVATAR))
                placeholder.fill((255, 0, 255))
                return placeholder

        self.avatar_zoio = carregar_avatar("zoio.jpg")
        self.avatar_abner = carregar_avatar("abner.jpg")
        self.avatar_carlinhos = carregar_avatar("carlinhos.jpg")
        self.avatar_gabe = carregar_avatar("Gabe.jpg")
        self.avatar_indiano = carregar_avatar("Indiano.jpg")
        self.avatar_ney = carregar_avatar("ney.jpg")

        # --- FILA DE REQUISIÇÕES (TEXTOS LIMPOS PARA VOCÊ EDITAR) ---
        self.fila_requisicoes = [
            {"avatar": self.avatar_zoio, "remetente": "Everson Zoio", "cargo": "Estagiário",
             "acesso": "WIFI_MICROONDAS", "corpo": "[ ESCREVA AQUI O PEDIDO DO ZOIO ]"},
            {"avatar": self.avatar_abner, "remetente": "Abner Trovão", "cargo": "Analista de Dados",
             "acesso": "PASTA_CONFIDENCIAL", "corpo": "[ ESCREVA AQUI O PEDIDO DO ABNER ]"},
            {"avatar": self.avatar_carlinhos, "remetente": "Carlinhos", "cargo": "Mestre de Cerimônias",
             "acesso": "PROTOCOLO_FELINO", "corpo": "[ ESCREVA AQUI O PEDIDO DO CARLINHOS ]"},
            {"avatar": self.avatar_gabe, "remetente": "Gabe Newell", "cargo": "CEO", "acesso": "ROOT_SERVER",
             "corpo": "[ ESCREVA AQUI O PEDIDO DO GABE ]"},
            {"avatar": self.avatar_indiano, "remetente": "Analista Indiano", "cargo": "Suporte Técnico",
             "acesso": "FORMAT_C", "corpo": "[ ESCREVA AQUI O PEDIDO DO INDIANO ]"},
            {"avatar": self.avatar_ney, "remetente": "Adulto Ney", "cargo": "Estagiário de Luxo",
             "acesso": "PORTA_FESTA", "corpo": "[ ESCREVA AQUI O PEDIDO DO NEY ]"}
        ]
        self.req_atual = 0

    def desenhar(self, tela):
        tela.fill(COR_FUNDO_DESKTOP)

        altura_barra = 40
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (0, self.altura - altura_barra, self.largura, altura_barra))
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (0, self.altura - altura_barra),
                         (self.largura, self.altura - altura_barra), 2)

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
        tela.blit(pygame.font.SysFont("tahoma", 16, bold=True).render("Doors", True, COR_TEXTO),
                  (x_botoes + 35, y_botoes + 6))

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

        centro_coluna_1, centro_coluna_2, start_y, espacamento_y = 60, 180, 30, 110

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

        # Desenha todas as janelas na ordem correta
        for app_nome in self.janelas_abertas:
            self.desenhar_uma_janela(tela, app_nome)

        if self.menu_aberto:
            self.desenhar_menu_iniciar(tela)

    def desenhar_icone_centralizado(self, tela, centro_x, y, nome, imagem):
        largura_img = imagem.get_width()
        pos_img_x = centro_x - (largura_img // 2)
        tela.blit(imagem, (pos_img_x, y))
        texto_sombra = self.fonte_padrao.render(nome, True, (0, 0, 0))
        texto = self.fonte_padrao.render(nome, True, COR_TEXTO_ICONE)
        pos_texto_x = centro_x - (texto.get_width() // 2)
        pos_texto_y = y + self.TAMANHO_MAX_ICONE + 5
        tela.blit(texto_sombra, (pos_texto_x + 1, pos_texto_y + 1))
        tela.blit(texto, (pos_texto_x, pos_texto_y))
        return pygame.Rect(pos_img_x, y, largura_img, self.TAMANHO_MAX_ICONE + 20)

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

    def desenhar_uma_janela(self, tela, app_nome):
        largura_janela = 600
        altura_janela = 450
        x_janela, y_janela = self.janelas_pos[app_nome]

        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_janela, y_janela, largura_janela, altura_janela))
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_janela, y_janela), (x_janela + largura_janela, y_janela), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_janela, y_janela), (x_janela, y_janela + altura_janela), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_janela + largura_janela, y_janela),
                         (x_janela + largura_janela, y_janela + altura_janela), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_janela, y_janela + altura_janela),
                         (x_janela + largura_janela, y_janela + altura_janela), 2)

        altura_titulo = 25
        pygame.draw.rect(tela, (0, 0, 128), (x_janela + 3, y_janela + 3, largura_janela - 6, altura_titulo))

        # A janela ativa (última da lista) tem título branco, as inativas ficam cinzas
        cor_tit = COR_BOTAO_BRIGHT if app_nome == self.janelas_abertas[-1] else (192, 192, 192)
        tela.blit(pygame.font.SysFont("tahoma", 14, bold=True).render(app_nome, True, cor_tit),
                  (x_janela + 8, y_janela + 7))

        tamanho_x = 21
        x_fechar = x_janela + largura_janela - tamanho_x - 5
        y_fechar = y_janela + 5
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_fechar, y_fechar, tamanho_x, tamanho_x))
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_fechar, y_fechar), (x_fechar + tamanho_x, y_fechar), 1)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_fechar, y_fechar), (x_fechar, y_fechar + tamanho_x), 1)
        pygame.draw.line(tela, COR_TEXTO, (x_fechar + tamanho_x, y_fechar),
                         (x_fechar + tamanho_x, y_fechar + tamanho_x), 1)
        pygame.draw.line(tela, COR_TEXTO, (x_fechar, y_fechar + tamanho_x),
                         (x_fechar + tamanho_x, y_fechar + tamanho_x), 1)
        tela.blit(pygame.font.SysFont("tahoma", 14, bold=True).render("X", True, COR_TEXTO),
                  (x_fechar + 6, y_fechar + 2))

        if app_nome == "OutVision":
            self.desenhar_conteudo_outvision(tela, x_janela, y_janela, largura_janela, altura_janela, altura_titulo)
        elif app_nome == "Regras":
            self.desenhar_conteudo_regras(tela, x_janela, y_janela, largura_janela, altura_titulo)
        elif app_nome == "Terminal SOC":
            self.desenhar_conteudo_terminal(tela, x_janela, y_janela, largura_janela, altura_janela, altura_titulo)

    def tratar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = evento.pos

            # 1. Verifica clique nas janelas abertas (de cima para baixo)
            for i in range(len(self.janelas_abertas) - 1, -1, -1):
                app_nome = self.janelas_abertas[i]
                x_j, y_j = self.janelas_pos[app_nome]
                w_j, h_j = 600, 450
                h_titulo = 25

                rect_janela = pygame.Rect(x_j, y_j, w_j, h_j)
                rect_titulo = pygame.Rect(x_j + 3, y_j + 3, w_j - 35, h_titulo)
                rect_fechar = pygame.Rect(x_j + w_j - 26, y_j + 5, 21, 21)

                if rect_fechar.collidepoint(pos_mouse):
                    self.janelas_abertas.remove(app_nome)
                    return

                if rect_titulo.collidepoint(pos_mouse):
                    self.janela_arrastada = app_nome
                    self.offset_x = pos_mouse[0] - x_j
                    self.offset_y = pos_mouse[1] - y_j
                    self.janelas_abertas.remove(app_nome)
                    self.janelas_abertas.append(app_nome)
                    return

                # Se clicou num botão E essa é a janela da frente (i == len - 1)
                if i == len(self.janelas_abertas) - 1:
                    if app_nome == "OutVision":
                        rect_ant = pygame.Rect(x_j + w_j - 90 - 15 - 90 - 10, y_j + h_j - 26 - 15, 90, 26)
                        rect_prox = pygame.Rect(x_j + w_j - 90 - 15, y_j + h_j - 26 - 15, 90, 26)
                        if rect_ant.collidepoint(pos_mouse):
                            self.req_atual = max(0, self.req_atual - 1)
                            return
                        elif rect_prox.collidepoint(pos_mouse):
                            self.req_atual = min(len(self.fila_requisicoes) - 1, self.req_atual + 1)
                            return

                    elif app_nome == "Terminal SOC":
                        if self.req_atual < len(self.fila_requisicoes):
                            rect_aprovar = pygame.Rect(x_j + (w_j // 2) - 150 - 20, y_j + h_j - 50 - 30, 150, 50)
                            rect_negar = pygame.Rect(x_j + (w_j // 2) + 20, y_j + h_j - 50 - 30, 150, 50)
                            if rect_aprovar.collidepoint(pos_mouse) or rect_negar.collidepoint(pos_mouse):
                                self.fila_requisicoes.pop(self.req_atual)
                                if self.req_atual >= len(self.fila_requisicoes) and self.req_atual > 0:
                                    self.req_atual -= 1
                                return

                # Se clicou no corpo de qualquer janela, apenas traz ela para frente
                if rect_janela.collidepoint(pos_mouse):
                    self.janelas_abertas.remove(app_nome)
                    self.janelas_abertas.append(app_nome)
                    return

                    # 2. Se não clicou em janela nenhuma, verifica a Área de Trabalho
            clicou_em_algo = False
            for nome_icone, hitbox in self.hitboxes.items():
                if hitbox.collidepoint(pos_mouse):
                    clicou_em_algo = True
                    if nome_icone == "Botao Doors":
                        self.menu_aberto = not self.menu_aberto
                    else:
                        self.menu_aberto = False

                        if nome_icone not in self.janelas_abertas:
                            self.janelas_abertas.append(nome_icone)
                            # Efeito cascata para as janelas não nascerem exatamente em cima da outra
                            offset = len(self.janelas_abertas) * 30
                            self.janelas_pos[nome_icone] = [(self.largura / 2) - 300 + offset,
                                                            (self.altura / 2) - 225 + offset]
                        else:
                            self.janelas_abertas.remove(nome_icone)
                            self.janelas_abertas.append(nome_icone)

                        if nome_icone == "OutVision":
                            self.req_atual = 0
                    return

            if not clicou_em_algo:
                self.menu_aberto = False

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.janela_arrastada = None

        elif evento.type == pygame.MOUSEMOTION:
            if self.janela_arrastada:
                self.janelas_pos[self.janela_arrastada][0] = evento.pos[0] - self.offset_x
                self.janelas_pos[self.janela_arrastada][1] = evento.pos[1] - self.offset_y

    def desenhar_botao_os(self, tela, retangulo, texto, cor_fundo=COR_BARRA_TAREFAS):
        pygame.draw.rect(tela, cor_fundo, retangulo)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (retangulo.x, retangulo.y), (retangulo.right, retangulo.y), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (retangulo.x, retangulo.y), (retangulo.x, retangulo.bottom), 2)
        pygame.draw.line(tela, COR_BOTAO, (retangulo.right, retangulo.y), (retangulo.right, retangulo.bottom), 2)
        pygame.draw.line(tela, COR_BOTAO, (retangulo.x, retangulo.bottom), (retangulo.right, retangulo.bottom), 2)
        sup_texto = self.fonte_padrao.render(texto, True, COR_TEXTO)
        pos_x = retangulo.x + (retangulo.width // 2) - (sup_texto.get_width() // 2)
        pos_y = retangulo.y + (retangulo.height // 2) - (sup_texto.get_height() // 2)
        tela.blit(sup_texto, (pos_x, pos_y))

    def desenhar_conteudo_outvision(self, tela, x_j, y_j, w_j, h_j, h_titulo):
        if len(self.fila_requisicoes) == 0:
            tela.blit(self.fonte_padrao.render("Nenhuma requisição pendente. Bom trabalho!", True, COR_TEXTO),
                      (x_j + 20, y_j + h_titulo + 20))
            return

        req = self.fila_requisicoes[self.req_atual]
        y_conteudo = y_j + h_titulo + 10
        x_conteudo = x_j + 10

        tela.blit(req["avatar"], (x_conteudo, y_conteudo))
        x_textos = x_conteudo + 80 + 15
        y_textos = y_conteudo

        fonte_bold = pygame.font.SysFont("tahoma", 13, bold=True)
        tela.blit(fonte_bold.render("De:", True, COR_TEXTO), (x_textos, y_textos))
        tela.blit(self.fonte_padrao.render(f"{req['remetente']} ({req['cargo']})", True, COR_TEXTO),
                  (x_textos + 30, y_textos))
        y_textos += 20
        tela.blit(fonte_bold.render("Acesso Solicitado:", True, COR_TEXTO), (x_textos, y_textos))
        tela.blit(self.fonte_padrao.render(req["acesso"], True, (200, 0, 0)), (x_textos + 130, y_textos))

        y_corpo = y_conteudo + 80 + 20
        pygame.draw.line(tela, COR_BOTAO, (x_conteudo, y_corpo - 10), (x_j + w_j - 10, y_corpo - 10), 1)
        tela.blit(fonte_bold.render("Justificativa:", True, COR_TEXTO), (x_conteudo, y_corpo))
        self.desenhar_texto_com_quebra(tela, req["corpo"], self.fonte_padrao, x_conteudo, y_corpo + 20, w_j - 30)

        largura_btn = 90
        x_btn_prox = x_j + w_j - largura_btn - 15
        y_btn = y_j + h_j - 26 - 15
        x_btn_ant = x_btn_prox - largura_btn - 10

        self.desenhar_botao_os(tela, pygame.Rect(x_btn_ant, y_btn, largura_btn, 26), "< Anterior")
        self.desenhar_botao_os(tela, pygame.Rect(x_btn_prox, y_btn, largura_btn, 26), "Próximo >")

        texto_contador = f"Req: {self.req_atual + 1}/{len(self.fila_requisicoes)}"
        tela.blit(self.fonte_padrao.render(texto_contador, True, COR_BOTAO), (x_btn_ant - 60, y_btn + 5))

    def desenhar_conteudo_regras(self, tela, x_j, y_j, w_j, h_titulo):
        # Aumentei o fundo para caber melhor os textos e limpei o template
        rect_fundo = pygame.Rect(x_j + 5, y_j + h_titulo + 5, w_j - 10, 450 - h_titulo - 10)
        pygame.draw.rect(tela, (255, 255, 255), rect_fundo)
        pygame.draw.rect(tela, COR_BOTAO, rect_fundo, 2)

        texto_regras = """MANUAL DE CONDUTA E ACESSO SOC (V1.0)

[ ESCREVA A SUA REGRA NÚMERO 1 AQUI ]

[ ESCREVA A SUA REGRA NÚMERO 2 AQUI ]

[ ESCREVA A SUA REGRA NÚMERO 3 AQUI ]

[ ESCREVA A SUA REGRA NÚMERO 4 AQUI ]"""

        self.desenhar_texto_com_quebra(tela, texto_regras, self.fonte_padrao, x_j + 15, y_j + h_titulo + 15, w_j - 30)

    def desenhar_conteudo_terminal(self, tela, x_j, y_j, w_j, h_j, h_titulo):
        rect_fundo = pygame.Rect(x_j + 5, y_j + h_titulo + 5, w_j - 10, h_j - h_titulo - 10)
        pygame.draw.rect(tela, (15, 15, 15), rect_fundo)

        if len(self.fila_requisicoes) == 0:
            tela.blit(self.fonte_terminal.render("SISTEMA OCIOSO. NENHUMA REQUISIÇÃO PENDENTE.", True, COR_TERMINAL),
                      (x_j + 20, y_j + h_titulo + 20))
            return

        req = self.fila_requisicoes[self.req_atual]

        textos = [
            "SOC SECURE TERMINAL v4.1",
            "---------------------------------------",
            f"REQUISIÇÃO ATUAL: #{self.req_atual + 1001}",
            f"SOLICITANTE: {req['remetente']}",
            f"CARGO:       {req['cargo']}",
            f"ACESSO ALVO: {req['acesso']}",
            "---------------------------------------",
            "AGUARDANDO DECISÃO DO ANALISTA..."
        ]

        y_linha = y_j + h_titulo + 20
        for linha in textos:
            tela.blit(self.fonte_terminal.render(linha, True, COR_TERMINAL), (x_j + 20, y_linha))
            y_linha += 25

        y_botoes = y_j + h_j - 50 - 30
        x_btn_aprovar = x_j + (w_j // 2) - 150 - 20
        x_btn_negar = x_j + (w_j // 2) + 20

        self.desenhar_botao_os(tela, pygame.Rect(x_btn_aprovar, y_botoes, 150, 50), "APROVAR", (0, 150, 0))
        self.desenhar_botao_os(tela, pygame.Rect(x_btn_negar, y_botoes, 150, 50), "NEGAR", (150, 0, 0))

    def desenhar_texto_com_quebra(self, tela, texto, fonte, x, y, largura_max):
        paragrafos = texto.split('\n')
        y_atual = y
        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
            linha_atual = ""
            for palavra in palavras:
                linha_teste = linha_atual + palavra + " "
                if fonte.size(linha_teste)[0] <= largura_max:
                    linha_atual = linha_teste
                else:
                    tela.blit(fonte.render(linha_atual.strip(), True, COR_TEXTO), (x, y_atual))
                    y_atual += fonte.size(linha_atual.strip())[1] + 2
                    linha_atual = palavra + " "
            tela.blit(fonte.render(linha_atual.strip(), True, COR_TEXTO), (x, y_atual))
            y_atual += fonte.size(linha_atual.strip())[1] + 10


class MenuPrincipal:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = pygame.font.SysFont("impact", 90)
        self.fonte_botoes = pygame.font.SysFont("impact", 40)
        self.hitboxes = {}

    def desenhar(self, tela):
        tela.fill((15, 15, 18))
        texto_sombra = self.fonte_titulo.render("ACCESS, PLEASE", True, (40, 0, 0))
        texto_titulo = self.fonte_titulo.render("ACCESS, PLEASE", True, (200, 40, 40))
        pos_x_titulo = (self.largura // 2) - (texto_titulo.get_width() // 2)
        tela.blit(texto_sombra, (pos_x_titulo + 5, 105))
        tela.blit(texto_titulo, (pos_x_titulo, 100))

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


class TelaBoot:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_log = pygame.font.SysFont("couriernew", 16)
        self.fonte_logo = pygame.font.SysFont("impact", 60)
        self.resetar()
        self.todas_as_linhas = [
            "DOORS BOOT SUBSYSTEM V4.11",
            "COPYRIGHT (C) 1995 DOORS CORPORATION",
            "---------------------------------------",
            "DETECTING HARDWARE...",
            "CPU: GENUINE INTEL(R) PENTIUM(R) @ 133MHz",
            "MEMORY TEST: 16384KB OK",
            "DETECTING IDE DRIVES...",
            "  PRI MASTER: QUANTUM FIREBALL 1080A",
            "  PRI SLAVE:  NONE",
            "DETECTING SCSI DEVICES...",
            "  ID 0: SONY CD-ROM CDU-76S OK",
            "  ID 3: SOC_SECURE_GUARD_HW OK",
            "INITIALIZING NETWORK...",
            "  ADAPTER: NOVELL NE2000 COMPATIBLE",
            "  IP ADDRESS: 192.168.0.42 (DHCP)",
            "---------------------------------------",
            "STARTING DOORS 95...",
            "LOADING GDI.EXE... OK",
            "LOADING USER.EXE... OK",
            "LOADING SOC_KERNEL.SYS... OK",
            "VERIFYING ANALYST CREDENTIALS...",
            "  LOGIN: SOC_STAGIARIO_01... GRANTED",
            "  CLEARANCE: LEVEL 1 (READ-ONLY)",
            "WARNING: UNRESOLVED SECURITY ALERTS PENDING",
            "WARNING: SYSTEM INTEGRITY AT 88%",
            "LOADING ACCESS, PLEASE INTERFACE...",
            "READY."
        ]

    def resetar(self):
        self.linhas_exibidas = []
        self.indice_linha_atual = 0
        self.contador_frames = 0
        self.velocidade_carregamento = 6
        self.tempo_espera_final = 0

    def desenhar(self, tela):
        tela.fill((10, 10, 10))
        largura_logo_area = 300
        x_logo = (self.largura // 2) - (largura_logo_area // 2)
        y_logo = 50

        tamanho_quad = 40
        gap = 5
        pygame.draw.rect(tela, (0, 0, 200), (x_logo, y_logo, tamanho_quad, tamanho_quad))
        pygame.draw.rect(tela, (230, 230, 0), (x_logo + tamanho_quad + gap, y_logo, tamanho_quad, tamanho_quad))
        pygame.draw.rect(tela, (200, 0, 0), (x_logo, y_logo + tamanho_quad + gap, tamanho_quad, tamanho_quad))
        pygame.draw.rect(tela, (0, 200, 0),
                         (x_logo + tamanho_quad + gap, y_logo + tamanho_quad + gap, tamanho_quad, tamanho_quad))

        texto_doors = self.fonte_logo.render("Doors 95", True, (255, 255, 255))
        tela.blit(texto_doors, (x_logo + (tamanho_quad * 2) + 20, y_logo + 5))

        self.contador_frames += 1

        if self.contador_frames >= self.velocidade_carregamento and self.indice_linha_atual < len(self.todas_as_linhas):
            nova_linha = self.todas_as_linhas[self.indice_linha_atual]
            self.linhas_exibidas.append(nova_linha)
            self.indice_linha_atual += 1
            self.contador_frames = 0
            self.velocidade_carregamento = 30 if "LOADING SOC_KERNEL.SYS" in nova_linha else 6

        y_item = self.altura - 30
        x_item = 50

        for linha in reversed(self.linhas_exibidas):
            superficie_texto = self.fonte_log.render(linha, True, COR_TERMINAL)
            tela.blit(superficie_texto, (x_item, y_item))
            y_item -= 22
            if y_item < 180:
                break

        if self.indice_linha_atual >= len(self.todas_as_linhas):
            self.tempo_espera_final += 1
            return self.tempo_espera_final > 120

        return False