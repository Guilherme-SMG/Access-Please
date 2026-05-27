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
        self.itens_menu = ["Programas", "Documentos", "Configurações", "Pesquisar", "Ajuda", "Desligar..."]
        self.hitboxes_itens_menu = []

        self.janelas_abertas = []
        self.janelas_pos = {}
        self.janela_arrastada = None
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

        # --- CARREGAMENTO DO SOM DE CLIQUE ---
        pygame.mixer.init()
        try:
            self.som_click = pygame.mixer.Sound(os.path.join("assets", "sounds", "click.mp3"))
            self.som_click.set_volume(0.3)  # Volume mais baixo para não irritar
        except (FileNotFoundError, pygame.error):
            self.som_click = None

        self.fila_requisicoes = [
            {"avatar": self.avatar_zoio, "remetente": "Everson Zoio", "cargo": "Estagiário",
             "acesso": "WIFI_MICROONDAS",
             "corpo": "E ae, rapaziada! Zoio na area! Solicito acesso à rede Wi-Fi restrita do SOC para conectar meu microondas. Quero tentar emular o Doors 95 nele. O bagulho é doido! Libera o IP ai, confia!"},
            {"avatar": self.avatar_abner, "remetente": "Abner Trovão", "cargo": "Analista de Dados",
             "acesso": "PASTA_CONFIDENCIAL",
             "corpo": "Bom dia, SOC. Solicito acesso à pasta confidencial 'lista_compras_semanal.txt'. Detectei um possível vazamento de dados sobre o preço do pão. Preciso analisar antes que os h@ckers comprem todo o lanche."},
            {"avatar": self.avatar_carlinhos, "remetente": "Carlinhos", "cargo": "Mestre de Cerimônias",
             "acesso": "PROTOCOLO_FELINO",
             "corpo": "Solicito aprovação de acesso USB imediato. Meu gato deitou no teclado e o protocolo G.A.T.O.S bloqueou minhas portas. Preciso conectar meu pendrive para salvar as fotos dele para o Instagram."},
            {"avatar": self.avatar_gabe, "remetente": "Gabe Newell", "cargo": "CEO", "acesso": "ROOT_SERVER",
             "corpo": "Prezados. Solicito acesso ROOT ao servidor central. O arquivo 'halfdead3.sys' sumiu e preciso procurá-lo nas pastas de sistema. Sou o único com a chave do cofre, liberem meu acesso imediatamente."},
            {"avatar": self.avatar_indiano, "remetente": "Analista Indiano", "cargo": "Suporte Técnico",
             "acesso": "FORMAT_C",
             "corpo": "Hello guys! Solicito permissão nível 5 para executar o comando 'FORMAT C: /Q /y' no servidor principal. É parte do meu novo tutorial grátis do além para resolver erros do SOC Kernel. Deixe o like!"},
            {"avatar": self.avatar_ney, "remetente": "Adulto Ney", "cargo": "Estagiário de Luxo",
             "acesso": "PORTA_FESTA",
             "corpo": "SOC, seguinte. Solicito a liberação da Porta 8080 do firewall. Preciso enviar os convites da festa secreta do Doors 96. O traje é camisa do PSG. Libera aí que te coloco na lista VIP!"}
        ]
        self.req_atual = 0

        # --- ATENÇÃO: Recebe os parâmetros de dinheiro e strikes! ---

    def desenhar(self, tela, dinheiro=0, strikes=0):
        tela.fill(COR_FUNDO_DESKTOP)

        # --- PAINEL DO SOC (HUD) ---
        pygame.draw.rect(tela, (20, 20, 20), (self.largura - 170, 10, 160, 60))
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (self.largura - 170, 10, 160, 60), 2)

        texto_dinheiro = self.fonte_padrao.render(f"Saldo: ${dinheiro}", True, (50, 255, 50))
        cor_strike = (255, 50, 50) if strikes > 0 else COR_BOTAO_BRIGHT
        texto_strikes = self.fonte_padrao.render(f"Advertências: {strikes}/3", True, cor_strike)

        tela.blit(texto_dinheiro, (self.largura - 160, 20))
        tela.blit(texto_strikes, (self.largura - 160, 40))

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
        x_tray = self.largura - superficie_relogio.get_width() - 25
        y_tray = self.altura - altura_barra + 7
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_tray, y_tray, superficie_relogio.get_width() + 20, 26))
        pygame.draw.line(tela, COR_BOTAO, (x_tray, y_tray), (x_tray + superficie_relogio.get_width() + 20, y_tray), 2)
        pygame.draw.line(tela, COR_BOTAO, (x_tray, y_tray), (x_tray, y_tray + 26), 2)
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
        pygame.draw.rect(tela, (0, 0, 128), (x_menu + 2, y_menu + 2, 35, altura_menu - 4))

        texto_rotacionado = pygame.transform.rotate(
            pygame.font.SysFont("tahoma", 20, bold=True).render("Doors OS", True, COR_BOTAO_BRIGHT), 90)
        tela.blit(texto_rotacionado, (x_menu + 7, y_menu + altura_menu - texto_rotacionado.get_height() - 10))

        self.hitboxes_itens_menu = []
        y_item = y_menu + 20
        for item in self.itens_menu:
            rect_item = pygame.Rect(x_menu + 40, y_item - 5, largura_menu - 45, 35)
            self.hitboxes_itens_menu.append((item, rect_item))

            tela.blit(self.fonte_padrao.render(item, True, COR_TEXTO), (x_menu + 50, y_item))
            if item == "Ajuda":
                y_linha = y_item + 30
                pygame.draw.line(tela, COR_BOTAO, (x_menu + 50, y_linha), (x_menu + largura_menu - 10, y_linha), 1)
                pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_menu + 50, y_linha + 1),
                                 (x_menu + largura_menu - 10, y_linha + 1), 1)
                y_item += 10
            y_item += 40

    def desenhar_uma_janela(self, tela, app_nome):
        largura_janela, altura_janela = 600, 450
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
        cor_tit = COR_BOTAO_BRIGHT if app_nome == self.janelas_abertas[-1] else (192, 192, 192)
        tela.blit(pygame.font.SysFont("tahoma", 14, bold=True).render(app_nome, True, cor_tit),
                  (x_janela + 8, y_janela + 7))

        x_fechar = x_janela + largura_janela - 26
        y_fechar = y_janela + 5
        pygame.draw.rect(tela, COR_BARRA_TAREFAS, (x_fechar, y_fechar, 21, 21))
        tela.blit(pygame.font.SysFont("tahoma", 14, bold=True).render("X", True, COR_TEXTO),
                  (x_fechar + 6, y_fechar + 2))

        if app_nome == "OutVision":
            self.desenhar_conteudo_outvision(tela, x_janela, y_janela, largura_janela, altura_janela, altura_titulo)
        elif app_nome == "Regras":
            self.desenhar_conteudo_regras(tela, x_janela, y_janela, largura_janela, altura_titulo)
        elif app_nome == "Terminal SOC":
            self.desenhar_conteudo_terminal(tela, x_janela, y_janela, largura_janela, altura_janela, altura_titulo)
        else:
            aviso = self.fonte_padrao.render("Aplicativo indisponível.", True, COR_TEXTO)
            tela.blit(aviso, (x_janela + 20, y_janela + altura_titulo + 20))

    def tratar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = evento.pos
            if hasattr(self, 'som_click') and self.som_click:
                self.som_click.play()

            if self.menu_aberto:
                rect_menu_inteiro = pygame.Rect(0, self.altura - 40 - 320, 220, 320)
                if rect_menu_inteiro.collidepoint(pos_mouse):
                    for item_nome, item_rect in self.hitboxes_itens_menu:
                        if item_rect.collidepoint(pos_mouse):
                            self.menu_aberto = False
                            if item_nome == "Desligar...":
                                return "SHUTDOWN"
                            else:
                                if item_nome not in self.janelas_abertas:
                                    self.janelas_abertas.append(item_nome)
                                    offset = len(self.janelas_abertas) * 30
                                    self.janelas_pos[item_nome] = [200 + offset, 150 + offset]
                                else:
                                    self.janelas_abertas.append(
                                        self.janelas_abertas.pop(self.janelas_abertas.index(item_nome)))
                            return None
                    return None
                else:
                    if not self.hitboxes.get("Botao Doors").collidepoint(pos_mouse):
                        self.menu_aberto = False

            for i in range(len(self.janelas_abertas) - 1, -1, -1):
                app_nome = self.janelas_abertas[i]
                x_j, y_j = self.janelas_pos[app_nome]
                rect_janela = pygame.Rect(x_j, y_j, 600, 450)
                rect_titulo = pygame.Rect(x_j + 3, y_j + 3, 565, 25)
                rect_fechar = pygame.Rect(x_j + 574, y_j + 5, 21, 21)

                if rect_fechar.collidepoint(pos_mouse):
                    self.janelas_abertas.remove(app_nome)
                    return None

                if rect_titulo.collidepoint(pos_mouse):
                    self.janela_arrastada = app_nome
                    self.offset_x, self.offset_y = pos_mouse[0] - x_j, pos_mouse[1] - y_j
                    self.janelas_abertas.append(self.janelas_abertas.pop(i))
                    return None

                if i == len(self.janelas_abertas) - 1:
                    if app_nome == "OutVision":
                        if pygame.Rect(x_j + 405, y_j + 409, 90, 26).collidepoint(pos_mouse):
                            self.req_atual = max(0, self.req_atual - 1)
                        elif pygame.Rect(x_j + 495, y_j + 409, 90, 26).collidepoint(pos_mouse):
                            self.req_atual = min(len(self.fila_requisicoes) - 1, self.req_atual + 1)

                    elif app_nome == "Terminal SOC" and len(self.fila_requisicoes) > 0:
                        # --- MODIFICAÇÃO CHAVE: Retorna a decisão para o main.py ---
                        req = self.fila_requisicoes[self.req_atual]

                        if pygame.Rect(x_j + 130, y_j + 370, 150, 50).collidepoint(pos_mouse):  # APROVAR
                            self.fila_requisicoes.pop(self.req_atual)
                            self.req_atual = max(0, min(self.req_atual, len(self.fila_requisicoes) - 1))
                            return {"acao": "DECISAO", "acesso": req["acesso"], "decisao": True}

                        elif pygame.Rect(x_j + 320, y_j + 370, 150, 50).collidepoint(pos_mouse):  # NEGAR
                            self.fila_requisicoes.pop(self.req_atual)
                            self.req_atual = max(0, min(self.req_atual, len(self.fila_requisicoes) - 1))
                            return {"acao": "DECISAO", "acesso": req["acesso"], "decisao": False}

                if rect_janela.collidepoint(pos_mouse):
                    self.janelas_abertas.append(self.janelas_abertas.pop(i))
                    return None

            for nome_icone, hitbox in self.hitboxes.items():
                if hitbox.collidepoint(pos_mouse):
                    if nome_icone == "Botao Doors":
                        self.menu_aberto = not self.menu_aberto
                    else:
                        self.menu_aberto = False
                        if nome_icone not in self.janelas_abertas:
                            self.janelas_abertas.append(nome_icone)
                            offset = len(self.janelas_abertas) * 30
                            self.janelas_pos[nome_icone] = [200 + offset, 150 + offset]
                        else:
                            self.janelas_abertas.append(
                                self.janelas_abertas.pop(self.janelas_abertas.index(nome_icone)))
                    return None
            return None

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.janela_arrastada = None
        elif evento.type == pygame.MOUSEMOTION and self.janela_arrastada:
            self.janelas_pos[self.janela_arrastada] = [evento.pos[0] - self.offset_x, evento.pos[1] - self.offset_y]

    def desenhar_botao_os(self, tela, retangulo, texto, cor_fundo=COR_BARRA_TAREFAS):
        pygame.draw.rect(tela, cor_fundo, retangulo)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (retangulo.x, retangulo.y), (retangulo.right, retangulo.y), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (retangulo.x, retangulo.y), (retangulo.x, retangulo.bottom), 2)
        pygame.draw.line(tela, COR_BOTAO, (retangulo.right, retangulo.y), (retangulo.right, retangulo.bottom), 2)
        pygame.draw.line(tela, COR_BOTAO, (retangulo.x, retangulo.bottom), (retangulo.right, retangulo.bottom), 2)
        sup_texto = self.fonte_padrao.render(texto, True, COR_TEXTO)
        tela.blit(sup_texto,
                  (retangulo.centerx - sup_texto.get_width() // 2, retangulo.centery - sup_texto.get_height() // 2))

    def desenhar_conteudo_outvision(self, tela, x_j, y_j, w_j, h_j, h_titulo):
        if len(self.fila_requisicoes) == 0:
            tela.blit(self.fonte_padrao.render("Nenhuma requisição pendente.", True, COR_TEXTO),
                      (x_j + 20, y_j + h_titulo + 20))
            return
        req = self.fila_requisicoes[self.req_atual]
        tela.blit(req["avatar"], (x_j + 10, y_j + h_titulo + 10))
        fonte_bold = pygame.font.SysFont("tahoma", 13, bold=True)
        tela.blit(fonte_bold.render("De:", True, COR_TEXTO), (x_j + 105, y_j + h_titulo + 10))
        tela.blit(self.fonte_padrao.render(f"{req['remetente']} ({req['cargo']})", True, COR_TEXTO),
                  (x_j + 135, y_j + h_titulo + 10))
        tela.blit(fonte_bold.render("Acesso:", True, COR_TEXTO), (x_j + 105, y_j + h_titulo + 30))
        tela.blit(self.fonte_padrao.render(req["acesso"], True, (200, 0, 0)), (x_j + 160, y_j + h_titulo + 30))
        pygame.draw.line(tela, COR_BOTAO, (x_j + 10, y_j + h_titulo + 100), (x_j + w_j - 10, y_j + h_titulo + 100), 1)
        self.desenhar_texto_com_quebra(tela, req["corpo"], self.fonte_padrao, x_j + 15, y_j + h_titulo + 115, w_j - 30)
        self.desenhar_botao_os(tela, pygame.Rect(x_j + 405, y_j + 409, 90, 26), "< Anterior")
        self.desenhar_botao_os(tela, pygame.Rect(x_j + 495, y_j + 409, 90, 26), "Próximo >")
        texto_contador = f"Req: {self.req_atual + 1}/{len(self.fila_requisicoes)}"
        tela.blit(self.fonte_padrao.render(texto_contador, True, COR_BOTAO), (x_j + 405 - 60, y_j + 409 + 5))

    def desenhar_conteudo_regras(self, tela, x_j, y_j, w_j, h_titulo):
        pygame.draw.rect(tela, (255, 255, 255), (x_j + 5, y_j + h_titulo + 5, w_j - 10, 410))
        pygame.draw.rect(tela, COR_BOTAO, (x_j + 5, y_j + h_titulo + 5, w_j - 10, 410), 2)
        texto_regras = "MANUAL DE CONDUTA SOC (V1.0)\n\n[REGRAS AQUI]"
        self.desenhar_texto_com_quebra(tela, texto_regras, self.fonte_padrao, x_j + 15, y_j + h_titulo + 15, w_j - 30)

    def desenhar_conteudo_terminal(self, tela, x_j, y_j, w_j, h_j, h_titulo):
        pygame.draw.rect(tela, (15, 15, 15), (x_j + 5, y_j + h_titulo + 5, w_j - 10, h_j - h_titulo - 10))
        if len(self.fila_requisicoes) == 0:
            tela.blit(self.fonte_terminal.render("SISTEMA OCIOSO.", True, COR_TERMINAL),
                      (x_j + 20, y_j + h_titulo + 20))
            return
        req = self.fila_requisicoes[self.req_atual]
        linhas = ["SOC TERMINAL v4.1", "---", f"REQ: #{self.req_atual + 1001}", f"DE: {req['remetente']}",
                  f"ALVO: {req['acesso']}", "---", "AGUARDANDO..."]
        for idx, linha in enumerate(linhas):
            tela.blit(self.fonte_terminal.render(linha, True, COR_TERMINAL),
                      (x_j + 20, y_j + h_titulo + 20 + (idx * 25)))
        self.desenhar_botao_os(tela, pygame.Rect(x_j + 130, y_j + 370, 150, 50), "APROVAR", (0, 150, 0))
        self.desenhar_botao_os(tela, pygame.Rect(x_j + 320, y_j + 370, 150, 50), "NEGAR", (150, 0, 0))

    def desenhar_texto_com_quebra(self, tela, texto, fonte, x, y, largura_max):
        paragrafos = texto.split('\n')
        y_atual = y
        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
            linha_atual = ""
            for palavra in palavras:
                if fonte.size(linha_atual + palavra)[0] <= largura_max:
                    linha_atual += palavra + " "
                else:
                    tela.blit(fonte.render(linha_atual.strip(), True, COR_TEXTO), (x, y_atual))
                    y_atual += fonte.size("A")[1] + 2
                    linha_atual = palavra + " "
            tela.blit(fonte.render(linha_atual.strip(), True, COR_TEXTO), (x, y_atual))
            y_atual += fonte.size("A")[1] + 10


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

        pygame.mixer.init()
        caminho_som_boot = os.path.join("assets", "sounds", "boot.mp3")
        try:
            self.som_boot = pygame.mixer.Sound(caminho_som_boot)
            self.som_boot.set_volume(0.5)
        except (FileNotFoundError, pygame.error):
            print("AVISO: Arquivo 'boot.mp3' não encontrado na pasta assets/sounds/")
            self.som_boot = None

        # PASSAMOS 'False' AQUI PARA NÃO TOCAR QUANDO O JOGO ABRE!
        self.resetar(tocar_som=False)

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

    # ADICIONAMOS O PARÂMETRO 'tocar_som=True' PARA QUANDO O BOTÃO FOR CLICADO
    def resetar(self, tocar_som=True):
        self.linhas_exibidas = []
        self.indice_linha_atual = 0
        self.contador_frames = 0
        self.velocidade_carregamento = 6
        self.tempo_espera_final = 0

        # SÓ TOCA SE A VARIÁVEL FOR VERDADEIRA
        if tocar_som and hasattr(self, 'som_boot') and self.som_boot:
            self.som_boot.play()

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


class TelaShutdown:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_msg = pygame.font.SysFont("tahoma", 28)
        self.fonte_logo = pygame.font.SysFont("impact", 60, italic=True)
        self.timer = 0

    def resetar(self):
        self.timer = 0

    def desenhar(self, tela):
        for y in range(self.altura):
            cor = (100 + (y // 10), 150 + (y // 15), 255)
            pygame.draw.line(tela, cor, (0, y), (self.largura, y))

        msg = "Aguarde enquanto seu computador é desligado."
        sup_msg = self.fonte_msg.render(msg, True, (200, 50, 50))
        tela.blit(sup_msg, (self.largura // 2 - sup_msg.get_width() // 2, self.altura // 2 - 50))

        logo_txt = self.fonte_logo.render("Doors 95", True, (255, 255, 255))
        tela.blit(logo_txt, (self.largura // 2 - logo_txt.get_width() // 2, self.altura // 2 + 50))

        self.timer += 1
        return self.timer > 180

    # --- NOVA CLASSE: TELA DE GAME OVER (Demitido!) ---


class TelaGameOver:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = pygame.font.SysFont("impact", 70)
        self.fonte_sub = pygame.font.SysFont("tahoma", 24, bold=True)
        self.timer = 0

    def resetar(self):
        self.timer = 0

    def desenhar(self, tela):
        tela.fill((150, 0, 0))  # Fundo vermelho fatal (Estilo Tela Azul da Morte, mas vermelha)

        txt = self.fonte_titulo.render("SISTEMA BLOQUEADO", True, (255, 255, 255))
        sub = self.fonte_sub.render("Múltiplas violações de segurança detectadas. Você foi demitido.", True,
                                    (255, 255, 255))

        tela.blit(txt, (self.largura // 2 - txt.get_width() // 2, self.altura // 2 - 60))
        tela.blit(sub, (self.largura // 2 - sub.get_width() // 2, self.altura // 2 + 30))

        self.timer += 1
        return self.timer > 240  # Espera 4 segundos para desligar o PC