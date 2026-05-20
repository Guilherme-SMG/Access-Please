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

        self.hitboxes = {}
        self.menu_aberto = False

        self.janela_aberta = None
        self.hitbox_fechar_janela = None
        self.hitbox_fundo_janela = None

        self.hitbox_btn_anterior = None
        self.hitbox_btn_proximo = None

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

        self.emails_humoristicos = [
            {
                "avatar": self.avatar_zoio,
                "remetente": "Everson Zoio (SOC_STAGIARIO_01)",
                "assunto": "DESAFIO HARDCORE: INSTALAR DOORS 95 NO MICROONDAS",
                "corpo": "E ae, rapaziada! Zoio na area! O desafio é pesado: vou conectar meu microondas no Wi-Fi e tentar emular o Doors 95 nele. O bagulho é doido! Se o SOC detectar picos de temperatura anormal, é só o Gates mandando um update do além. Fica de boa! Falou!"
            },
            {
                "avatar": self.avatar_abner,
                "remetente": "Abner Trovão (Doutor da TI)",
                "assunto": "VAZAMENTO DE DADOS IMPORTANTE (OU NÃO?)",
                "corpo": "Bom dia, SOC. Detectei um vazamento de dados críticos no servidor.\nO arquivo se chama: \n'lista_compras_semanal.txt'\nEle contém informações confidenciais sobre o preço do pão e do leite. Peço providências imediatas antes que os h@ckers comprem tudo no mercado e eu fique sem lanche. Atenciosamente."
            },
            {
                "avatar": self.avatar_carlinhos,
                "remetente": "Carlinhos (Mestre de Cerimônias e Analista Sênior)",
                "assunto": "PROTOCOLOS DE SEGURANÇA AVANÇADOS: GATOS NO TECLADO",
                "corpo": "SOC, atenção para o protocolo G.A.T.O.S.\nSempre que um felino for detectado sobre um teclado, o analista deve:\n1. Oferecer ração ao gato.\n2. Tirar foto para o Instagram.\n3. Bloquear todas as portas USB por 30 minutos.\nEssas medidas são cruciais para a segurança do estado. Grato."
            },
            {
                "avatar": self.avatar_gabe,
                "remetente": "Gabe Newell (O único com a chave do cofre SOC)",
                "assunto": "ONDE ESTÁ HALF DEAD 3? (PEDIDO DE ESCLARECIMENTO SÉRIO!)",
                "corpo": "Prezados analistas.\nComo eu sou o único com a chave de criptografia do SOC, venho informar que o arquivo \n'halfdead3.sys'\nfoi acidentalmente deletado durante uma atualização do Steam. Eu juro que não sei o que aconteceu. De qualquer forma, o Doors 95 é ótimo. Abraços."
            },
            {
                "avatar": self.avatar_indiano,
                "remetente": "Analista Indiano (Tutorial do além)",
                "assunto": "COMO RESOLVER ERRO DE SOC KERNEL (TUTORIAL GRÁTIS!)",
                "corpo": "Hello guys! Tutorial grátis do além!\nSe o seu SOC Kernel der erro, faça:\n1. Pegue um incenso.\n2. Dê três voltas no servidor.\n3. Digite: 'FORMAT C: /Q /y'\n4. O problema desapareceu! Grato. Deixe o like!"
            },
            {
                "avatar": self.avatar_ney,
                "remetente": "Adulto Ney (Estagiário de Luxo do SOC)",
                "assunto": "CONVITE PARA A FESTA DE LANÇAMENTO DO DOORS 96 (SECRETO!)",
                "corpo": "SOC, seguinte. Estou organizando a festa de lançamento secreta do Doors 96.\nO local é: uma ilha particular.\nO traje é: camisas do PSG.\nO convite é: R$ 5.000,00 por pessoa.\nMande as coordenadas para o meu SOC_login: SOC_ESTAGIARIO_LUXO. Não espalha! É secreto!"
            }
        ]

        self.email_idx_atual = 0

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
        texto_doors = pygame.font.SysFont("tahoma", 16, bold=True).render("Doors", True, COR_TEXTO)
        tela.blit(texto_doors, (x_botoes + 35, y_botoes + 6))

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

        if self.janela_aberta:
            self.desenhar_janela(tela)

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

    # --- A FUNÇÃO QUE FALTAVA VOLTOU AQUI ---
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

    def desenhar_janela(self, tela):
        largura_janela = 600
        altura_janela = 450
        x_janela = (self.largura / 2) - (largura_janela / 2)
        y_janela = (self.altura / 2) - (altura_janela / 2)

        self.hitbox_fundo_janela = pygame.Rect(x_janela, y_janela, largura_janela, altura_janela)

        pygame.draw.rect(tela, COR_BARRA_TAREFAS, self.hitbox_fundo_janela)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_janela, y_janela), (x_janela + largura_janela, y_janela), 2)
        pygame.draw.line(tela, COR_BOTAO_BRIGHT, (x_janela, y_janela), (x_janela, y_janela + altura_janela), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_janela + largura_janela, y_janela),
                         (x_janela + largura_janela, y_janela + altura_janela), 2)
        pygame.draw.line(tela, COR_TEXTO, (x_janela, y_janela + altura_janela),
                         (x_janela + largura_janela, y_janela + altura_janela), 2)

        altura_titulo = 25
        pygame.draw.rect(tela, (0, 0, 128), (x_janela + 3, y_janela + 3, largura_janela - 6, altura_titulo))

        fonte_titulo = pygame.font.SysFont("tahoma", 14, bold=True)
        texto_titulo = fonte_titulo.render(self.janela_aberta, True, COR_BOTAO_BRIGHT)
        tela.blit(texto_titulo, (x_janela + 8, y_janela + 7))

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

        if self.janela_aberta == "OutVision":
            self.desenhar_conteudo_email(tela, x_janela, y_janela, largura_janela, altura_janela, altura_titulo)

    def tratar_clique(self, pos_mouse):
        if self.janela_aberta:
            if self.hitbox_fechar_janela and self.hitbox_fechar_janela.collidepoint(pos_mouse):
                self.janela_aberta = None
                return "Fechou Janela"

            if self.janela_aberta == "OutVision":
                if self.hitbox_btn_anterior and self.hitbox_btn_anterior.collidepoint(pos_mouse):
                    self.email_idx_atual = (self.email_idx_atual - 1) % len(self.emails_humoristicos)
                    return "E-mail Anterior"
                elif self.hitbox_btn_proximo and self.hitbox_btn_proximo.collidepoint(pos_mouse):
                    self.email_idx_atual = (self.email_idx_atual + 1) % len(self.emails_humoristicos)
                    return "Próximo E-mail"

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
                    self.janela_aberta = nome_icone

                    if nome_icone == "OutVision":
                        self.email_idx_atual = 0

                return nome_icone

        if not clicou_em_algo:
            self.menu_aberto = False

        return None

    def desenhar_conteudo_email(self, tela, x_j, y_j, w_j, h_j, h_titulo):
        email = self.emails_humoristicos[self.email_idx_atual]

        y_conteudo = y_j + h_titulo + 10
        x_conteudo = x_j + 10

        tela.blit(email["avatar"], (x_conteudo, y_conteudo))

        x_textos = x_conteudo + 80 + 15
        y_textos = y_conteudo

        fonte_cabecalho = pygame.font.SysFont("tahoma", 13, bold=True)

        tela.blit(fonte_cabecalho.render("De:", True, COR_TEXTO), (x_textos, y_textos))
        tela.blit(self.fonte_padrao.render(email["remetente"], True, COR_TEXTO), (x_textos + 30, y_textos))

        y_textos += 20

        tela.blit(fonte_cabecalho.render("Assunto:", True, COR_TEXTO), (x_textos, y_textos))
        largura_max_assunto = w_j - (x_textos - x_j) - 15
        self.desenhar_texto_com_quebra(tela, email["assunto"], self.fonte_padrao, x_textos + 60, y_textos,
                                       largura_max_assunto)

        y_corpo = y_conteudo + 80 + 20
        largura_max_corpo = w_j - 30

        pygame.draw.line(tela, COR_BOTAO, (x_conteudo, y_corpo - 10), (x_j + w_j - 10, y_corpo - 10), 1)
        self.desenhar_texto_com_quebra(tela, email["corpo"], self.fonte_padrao, x_conteudo, y_corpo, largura_max_corpo)

        largura_btn = 90
        altura_btn = 26

        x_btn_prox = x_j + w_j - largura_btn - 15
        y_btn = y_j + h_j - altura_btn - 15
        x_btn_ant = x_btn_prox - largura_btn - 10

        self.hitbox_btn_anterior = pygame.Rect(x_btn_ant, y_btn, largura_btn, altura_btn)
        self.hitbox_btn_proximo = pygame.Rect(x_btn_prox, y_btn, largura_btn, altura_btn)

        def desenhar_botao_os(retangulo, texto):
            pygame.draw.rect(tela, COR_BARRA_TAREFAS, retangulo)
            pygame.draw.line(tela, COR_BOTAO_BRIGHT, (retangulo.x, retangulo.y), (retangulo.right, retangulo.y), 2)
            pygame.draw.line(tela, COR_BOTAO_BRIGHT, (retangulo.x, retangulo.y), (retangulo.x, retangulo.bottom), 2)
            pygame.draw.line(tela, COR_BOTAO, (retangulo.right, retangulo.y), (retangulo.right, retangulo.bottom), 2)
            pygame.draw.line(tela, COR_BOTAO, (retangulo.x, retangulo.bottom), (retangulo.right, retangulo.bottom), 2)

            sup_texto = self.fonte_padrao.render(texto, True, COR_TEXTO)
            pos_x = retangulo.x + (largura_btn // 2) - (sup_texto.get_width() // 2)
            pos_y = retangulo.y + (altura_btn // 2) - (sup_texto.get_height() // 2)
            tela.blit(sup_texto, (pos_x, pos_y))

        desenhar_botao_os(self.hitbox_btn_anterior, "< Anterior")
        desenhar_botao_os(self.hitbox_btn_proximo, "Próximo >")

        texto_contador = f"{self.email_idx_atual + 1}/{len(self.emails_humoristicos)}"
        sup_contador = self.fonte_padrao.render(texto_contador, True, COR_BOTAO)
        tela.blit(sup_contador, (x_btn_ant - 40, y_btn + 5))

    def desenhar_texto_com_quebra(self, tela, texto, fonte, x, y, largura_max):
        paragrafos = texto.split('\n')
        y_atual = y

        for paragrafo in paragrafos:
            palavras = paragrafo.split(' ')
            linha_atual = ""

            for palavra in palavras:
                linha_teste = linha_atual + palavra + " "
                largura_linha_teste = fonte.size(linha_teste)[0]

                if largura_linha_teste <= largura_max:
                    linha_atual = linha_teste
                else:
                    superficie_texto = fonte.render(linha_atual.strip(), True, COR_TEXTO)
                    tela.blit(superficie_texto, (x, y_atual))
                    y_atual += superficie_texto.get_height() + 2
                    linha_atual = palavra + " "

            superficie_texto = fonte.render(linha_atual.strip(), True, COR_TEXTO)
            tela.blit(superficie_texto, (x, y_atual))
            y_atual += superficie_texto.get_height() + 10


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

            if "LOADING SOC_KERNEL.SYS" in nova_linha:
                self.velocidade_carregamento = 30
            else:
                self.velocidade_carregamento = 6

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