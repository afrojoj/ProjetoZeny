import cv2
import os
import numpy as np
from PIL import ImageGrab


class DetectorDeAlvos:
    def __init__(self, pasta_sprites='assets\\monsters'):
        """
        Inicializa o detector de alvos carregando todos os sprites dos monstros.

        :param pasta_sprites: Caminho para a pasta contendo os sprites
        """
        self.sprites = self.carregar_sprites(pasta_sprites)
        self.tipos_monstros = ["agressor", "aquecedor", "congelador", "batedor"]

    def carregar_sprites(self, pasta_sprites):
        """
        Carrega todos os sprites dos monstros da pasta especificada.

        :param pasta_sprites: Caminho para a pasta contendo os sprites
        :return: Dicionário com os sprites organizados por tipo de monstro
        """
        sprites = {}

        # Verifica se o diretório existe
        if not os.path.exists(pasta_sprites):
            print(f"Aviso: O diretório {pasta_sprites} não foi encontrado!")
            return sprites

        # Procura por todos os arquivos na pasta de sprites
        for arquivo in os.listdir(pasta_sprites):
            caminho_completo = os.path.join(pasta_sprites, arquivo)

            if not arquivo.endswith(('.png', '.jpg', '.jpeg')) or os.path.isdir(caminho_completo):
                continue

            # Decompõe o nome do arquivo para identificar o monstro e direção
            partes = arquivo.split('.')[0].split('_')

            if len(partes) < 3:
                print(f"Aviso: O arquivo {arquivo} não segue o padrão de nomenclatura esperado.")
                continue  # Pula arquivos que não seguem o padrão

            nome_monstro = partes[0]

            # Verifica se é um dos monstros que estamos procurando
            if nome_monstro not in self.tipos_monstros:
                continue

            # Inicializa a entrada para este monstro se ainda não existir
            if nome_monstro not in sprites:
                sprites[nome_monstro] = []

            # Carrega o sprite
            sprite = cv2.imread(caminho_completo, cv2.IMREAD_UNCHANGED)

            if sprite is not None:
                # Determina o estado do fogo para aquecedores
                estado_fogo = None
                if nome_monstro == "aquecedor" and len(partes) > 3:
                    if "fire" in partes[3:]:
                        estado_fogo = "fire"
                    elif "nofire" in partes[3:]:
                        estado_fogo = "nofire"

                # Armazena o sprite com metadados sobre ele
                sprites[nome_monstro].append({
                    'imagem': sprite,
                    'nome_arquivo': arquivo,
                    'direcao_vertical': partes[1],  # 'front' ou 'back'
                    'direcao_horizontal': partes[2],  # 'left' ou 'right'
                    'estado_fogo': estado_fogo
                })
                print(f"Sprite carregado: {arquivo}")
            else:
                print(f"Erro ao carregar sprite: {arquivo}")

        # Imprime um resumo dos sprites carregados
        for nome_monstro, lista_sprites in sprites.items():
            print(f"Carregados {len(lista_sprites)} sprites para {nome_monstro}")

        return sprites

    def capturar_tela(self, area=None):
        """
        Captura a tela do jogo.

        :param area: Tupla (x1, y1, x2, y2) representando a área da tela a ser capturada
        :return: Imagem capturada em formato numpy array
        """
        captura = ImageGrab.grab(bbox=area)
        return np.array(captura)[:, :, ::-1]  # Converte RGB para BGR para OpenCV

    def encontrar_monstro(self, tela, tipo_monstro, limite_confianca=0.75):
        """
        Procura por um tipo específico de monstro na tela.

        :param tela: Imagem da tela onde procurar
        :param tipo_monstro: Tipo de monstro a ser procurado
        :param limite_confianca: Limiar mínimo de confiança para considerar uma detecção
        :return: Lista de detecções com posição, confiança e metadados
        """
        if tipo_monstro not in self.sprites:
            return []

        deteccoes = []

        for sprite_info in self.sprites[tipo_monstro]:
            sprite = sprite_info['imagem']

            # Verifica se as dimensões são válidas
            if sprite.shape[0] > tela.shape[0] or sprite.shape[1] > tela.shape[1]:
                print(f"Sprite {sprite_info['nome_arquivo']} é maior que a imagem da tela. Pulando...")
                continue

            # Aplica template matching
            try:
                resultado = cv2.matchTemplate(tela, sprite, cv2.TM_CCOEFF_NORMED)
                localizacoes = np.where(resultado >= limite_confianca)

                # Processa todas as detecções acima do limiar
                for pt in zip(*localizacoes[::-1]):
                    h, w = sprite.shape[:2]
                    deteccoes.append({
                        'posicao': pt,
                        'centro': (pt[0] + w // 2, pt[1] + h // 2),
                        'confianca': resultado[pt[1], pt[0]],
                        'altura': h,
                        'largura': w,
                        'direcao_vertical': sprite_info['direcao_vertical'],
                        'direcao_horizontal': sprite_info['direcao_horizontal'],
                        'estado_fogo': sprite_info.get('estado_fogo'),
                        'nome_arquivo': sprite_info['nome_arquivo']
                    })
            except Exception as e:
                print(f"Erro ao processar o sprite {sprite_info['nome_arquivo']}: {e}")

        # Ordena as detecções por confiança (maior primeiro)
        deteccoes.sort(key=lambda x: x['confianca'], reverse=True)

        # Remove detecções sobrepostas (non-maximum suppression)
        return self._remover_sobreposicoes(deteccoes)

    def _remover_sobreposicoes(self, deteccoes, limiar_iou=0.5):
        """
        Remove detecções sobrepostas usando non-maximum suppression.

        :param deteccoes: Lista de detecções
        :param limiar_iou: Limiar de IoU para considerar duas detecções como sobrepostas
        :return: Lista filtrada de detecções
        """
        if not deteccoes:
            return []

        # Cria lista de bounding boxes e scores
        boxes = []
        for d in deteccoes:
            x1, y1 = d['posicao']
            x2 = x1 + d['largura']
            y2 = y1 + d['altura']
            boxes.append([x1, y1, x2, y2])

        # Função auxiliar para calcular IoU entre duas caixas
        def calcular_iou(box1, box2):
            x1_1, y1_1, x2_1, y2_1 = box1
            x1_2, y1_2, x2_2, y2_2 = box2

            # Calcula área de interseção
            x_intersect = max(0, min(x2_1, x2_2) - max(x1_1, x1_2))
            y_intersect = max(0, min(y2_1, y2_2) - max(y1_1, y1_2))
            area_intersect = x_intersect * y_intersect

            # Calcula área de união
            area_box1 = (x2_1 - x1_1) * (y2_1 - y1_1)
            area_box2 = (x2_2 - x1_2) * (y2_2 - y1_2)
            area_uniao = area_box1 + area_box2 - area_intersect

            return area_intersect / area_uniao if area_uniao > 0 else 0

        # Aplica non-maximum suppression
        indices_mantidos = []
        for i in range(len(boxes)):
            should_keep = True
            for j in indices_mantidos:
                if calcular_iou(boxes[i], boxes[j]) > limiar_iou:
                    should_keep = False
                    break
            if should_keep:
                indices_mantidos.append(i)

        return [deteccoes[i] for i in indices_mantidos]

    def encontrar_todos_monstros(self, area=None, limite_confianca=0.75):
        """
        Procura por todos os tipos de monstros na tela.

        :param area: Área da tela a ser capturada
        :param limite_confianca: Limiar mínimo de confiança
        :return: Dicionário com detecções para cada tipo de monstro
        """
        tela = self.capturar_tela(area)
        resultados = {}

        for tipo_monstro in self.tipos_monstros:
            if tipo_monstro in self.sprites:
                deteccoes = self.encontrar_monstro(tela, tipo_monstro, limite_confianca)
                if deteccoes:
                    resultados[tipo_monstro] = deteccoes

        return resultados

    def obter_melhor_alvo(self, preferencia_monstro=None, preferencia_estado=None):
        """
        Obtém o melhor alvo para atacar com base nas preferências.

        :param preferencia_monstro: Lista ordenada de tipos de monstros preferenciais
        :param preferencia_estado: Estado preferencial (por exemplo, 'fire' para aquecedores)
        :return: Informação do melhor alvo encontrado
        """
        if preferencia_monstro is None:
            preferencia_monstro = self.tipos_monstros

        alvos = self.encontrar_todos_monstros()
        melhor_alvo = None
        max_prioridade = -1

        for i, tipo in enumerate(preferencia_monstro):
            prioridade = len(preferencia_monstro) - i

            if tipo in alvos:
                for alvo in alvos[tipo]:
                    # Verifica se há preferência de estado (para aquecedor)
                    if tipo == "aquecedor" and preferencia_estado is not None:
                        if alvo['estado_fogo'] == preferencia_estado and prioridade > max_prioridade:
                            melhor_alvo = alvo
                            melhor_alvo['tipo'] = tipo
                            max_prioridade = prioridade
                    elif prioridade > max_prioridade:
                        melhor_alvo = alvo
                        melhor_alvo['tipo'] = tipo
                        max_prioridade = prioridade
                        break

        return melhor_alvo


# Exemplo de uso
if __name__ == "__main__":
    detector = DetectorDeAlvos('assets\\monsters')

    # Encontrar todos os monstros
    alvos = detector.encontrar_todos_monstros()

    if not alvos:
        print("Nenhum monstro encontrado na tela atual.")
    else:
        for tipo_monstro, deteccoes in alvos.items():
            print(f"Encontrados {len(deteccoes)} {tipo_monstro}s:")
            for i, deteccao in enumerate(deteccoes):
                print(f"  {i + 1}. Posição: {deteccao['centro']}, Confiança: {deteccao['confianca']:.2f}, " +
                      f"Direção: {deteccao['direcao_vertical']}_{deteccao['direcao_horizontal']}")
                if tipo_monstro == "aquecedor":
                    print(f"     Estado: {'Em chamas' if deteccao['estado_fogo'] == 'fire' else 'Normal'}")

        # Encontrar o melhor alvo com prioridades
        melhor_alvo = detector.obter_melhor_alvo(
            preferencia_monstro=["aquecedor", "agressor", "batedor", "congelador"],
            preferencia_estado="fire"  # Preferir aquecedores em chamas
        )

        if melhor_alvo:
            print("\nMelhor alvo:")
            print(f"Tipo: {melhor_alvo['tipo']}")
            print(f"Posição: {melhor_alvo['centro']}")
            print(f"Confiança: {melhor_alvo['confianca']:.2f}")
            print(f"Direção: {melhor_alvo['direcao_vertical']}_{melhor_alvo['direcao_horizontal']}")
            if melhor_alvo['tipo'] == "aquecedor":
                print(f"Estado: {'Em chamas' if melhor_alvo['estado_fogo'] == 'fire' else 'Normal'}")
        else:
            print("\nNenhum alvo adequado encontrado.")
