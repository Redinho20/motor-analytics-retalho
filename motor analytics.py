import time
class Event:
    def __init__(self, event_id, timestamp, zone_id, event_type, duration_s, gender, age_range):
        self.event_id=event_id
        self.timestamp=timestamp
        self.zone_id=zone_id
        self.event_type=event_type
        self.duration_s=duration_s
        self.gender=gender
        self.age_range=age_range


def ler_csv(nome_ficheiro):
    eventos = []

    ficheiro = open(nome_ficheiro, "r", encoding="utf-8")
    linhas = ficheiro.readlines()
    ficheiro.close()

    for i in range(1, len(linhas)):
        linha = linhas[i].strip()
        parte = linha.split(",")
        evento = Event(parte[0], parte[1], parte[2], parte[3], parte[4], parte[5], parte[6])
        eventos.append(evento)

    # ORDENAR ANTES DE RETORNAR
    eventos.sort(key=lambda e: e.timestamp)

    return eventos



# =========================
# ALGORITMOS DE ORDENAÇÃO
# =========================
def ordenar_contagens(contagens):
    n = len(contagens)
    comparacoes = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            comparacoes += 1
            if contagens[j][1] < contagens[j + 1][1]:
                temp = contagens[j]
                contagens[j] = contagens[j + 1]
                contagens[j + 1] = temp

    return contagens, comparacoes

def merge(esq, dir):
    resultado = []
    i = j = 0
    comparacoes = 0

    while i < len(esq) and j < len(dir):
        comparacoes += 1
        if esq[i][1] > dir[j][1]:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1

    resultado.extend(esq[i:])
    resultado.extend(dir[j:])

    return resultado, comparacoes

# =========================
# FUNÇÕES AUXILIARES
# =========================
def contar_entradas_por_zona(eventos):
    tabela = TabelaHash()

    for evento in eventos:
        if evento.event_type == "entry":
            tabela.incrementar(evento.zone_id)

    return tabela.itens()

def contar_entradas_por_zona_intervalo(eventos, inicio, fim):
    tabela = TabelaHash()

    eventos_intervalo = filtrar_eventos_intervalo(eventos, inicio, fim)

    for evento in eventos_intervalo:
        if evento.event_type == "entry":
            tabela.incrementar(evento.zone_id)

    return tabela.itens()

def timestamp_para_segundos(timestamp):
    hora = int(timestamp[11:13])
    minuto = int(timestamp[14:16])
    segundo = int(timestamp[17:19])

    return hora * 3600 + minuto * 60 + segundo

def merge_sort_contagens(lista):
    if len(lista) <= 1:
        return lista, 0

    meio = len(lista) // 2
    esquerda, comp_esq = merge_sort_contagens(lista[:meio])
    direita, comp_dir = merge_sort_contagens(lista[meio:])

    resultado = []
    i = j = 0
    comparacoes = comp_esq + comp_dir

    while i < len(esquerda) and j < len(direita):
        comparacoes += 1
        if esquerda[i][1] > direita[j][1]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado, comparacoes


def juntar_contagens(esquerda, direita):
    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i][1] >= direita[j][1]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado

def comparar_ordenacoes(eventos):
    contagens = contar_entradas_por_zona(eventos)

    lista_original = []
    for item in contagens:
        lista_original.append([item[0], item[1]])

    repeticoes = 1000

    inicio = time.time()
    for _ in range(repeticoes):
        lista_bubble = [x[:] for x in lista_original]
        ordenar_contagens(lista_bubble)
    tempo_bubble = time.time() - inicio

    inicio = time.time()
    for _ in range(repeticoes):
        lista_merge = [x[:] for x in lista_original]
        merge_sort_contagens(lista_merge)
    tempo_merge = time.time() - inicio

    print("\nCOMPARAÇÃO DE ORDENAÇÕES")
    print("Bubble Sort:", round(tempo_bubble, 6), "segundos")
    print("Merge Sort:", round(tempo_merge, 6), "segundos")
    
def busca_binaria_inicio(eventos, alvo):
    esquerda = 0
    direita = len(eventos) - 1
    resultado = len(eventos)

    while esquerda <= direita:
        meio = (esquerda + direita) // 2

        if eventos[meio].timestamp >= alvo:
            resultado = meio
            direita = meio - 1
        else:
            esquerda = meio + 1

    return resultado

def busca_binaria_fim(eventos, alvo):
    esquerda = 0
    direita = len(eventos) - 1
    resultado = -1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2

        if eventos[meio].timestamp <= alvo:
            resultado = meio
            esquerda = meio + 1
        else:
            direita = meio - 1

    return resultado

def filtrar_eventos_intervalo(eventos, inicio, fim):
    i = busca_binaria_inicio(eventos, inicio)
    j = busca_binaria_fim(eventos, fim)

    if i > j:
        return []

    return eventos[i:j+1]




class MaxHeap:
    def __init__(self):
        self.dados = []

    def insert(self,item):
         self.dados.append(item)
         self.subir(len(self.dados)-1)
         
    def subir (self,indice):
         while indice>0:
              pai=(indice-1)//2
              if self.dados[indice][1]>self.dados[pai][1]:
                   temp = self.dados[indice]
                   self.dados[indice] = self.dados[pai]
                   self.dados[pai] = temp

                   indice = pai
              else:
                   break
              
    def remove_max(self):
         
         if len(self.dados) ==0:
              return None
         if len(self.dados)==1:
              return self.dados.pop()
         
         topo=self.dados[0]
         self.dados[0]=self.dados.pop()
         self.descer(0)

         return topo
    
    def descer(self,indice):
         n=len(self.dados)
         while True:
              maior=indice
              esquerda=2*indice+1
              direita=2*indice+2

              if esquerda < n and self.dados[esquerda][1] > self.dados[maior][1]:
                   maior=esquerda
              if direita < n and self.dados[direita][1] > self.dados[maior][1]:
                   maior=direita

              if maior != indice:
                   temp=self.dados[indice]
                   self.dados[indice]=self.dados[maior]
                   self.dados[maior]=temp
                   indice=maior
              else:
                   break

class TabelaHash:
    def __init__(self, tamanho=101):
        self.tamanho = tamanho
        self.tabela = []

        for i in range(tamanho):
            self.tabela.append([])

    def hash(self, chave):
        soma = 0
        for c in chave:
            soma += ord(c)
        return soma % self.tamanho

    def incrementar(self, chave, valor=1):
        indice = self.hash(chave)

        for par in self.tabela[indice]:
            if par[0] == chave:
                par[1] += valor
                return

        self.tabela[indice].append([chave, valor])

    def itens(self):
        resultado = []

        for balde in self.tabela:
            for par in balde:
                resultado.append(par)

        return resultado
    
    def contar_colisoes(self):
        colisoes = 0

        for balde in self.tabela:
            if len(balde) > 1:
                colisoes += len(balde) - 1

        return colisoes

    def load_factor(self):
        ocupados = 0

        for balde in self.tabela:
            if len(balde) > 0:
                ocupados += 1

        return ocupados / self.tamanho
              
      
# =========================
# QUERIES
# =========================
def query_top_k_zonas(eventos, k):
     resultado = contar_entradas_por_zona(eventos)

     heap = MaxHeap()
     for item in resultado:
          heap.insert(item)

     print(f"\nTOP {k} ZONAS MAIS VISITADAS")
     for i in range(k):
          maior = heap.remove_max()
          if maior is not None:
               print(maior[0], "->", maior[1]) 

def query_ocupacao_por_zona_intervalo(eventos, inicio, fim, tipo_zona):
    tabela = TabelaHash()

    eventos_intervalo = filtrar_eventos_intervalo(eventos, inicio, fim)

    for evento in eventos_intervalo:
        if evento.event_type == "entry":
            if tipo_zona == "" or evento.zone_id.startswith(tipo_zona):
                tabela.incrementar(evento.zone_id)

    contagens = tabela.itens()
    ordenar_contagens(contagens)

    print("\nOCUPAÇÃO POR ZONA")
    print("Intervalo:", inicio, "até", fim)

    if tipo_zona != "":
        print("Filtro tipo de zona:", tipo_zona)

    for item in contagens:
        print(item[0], "->", item[1])

def query_media_permanencia_por_zona(eventos, zona_escolhida):
    horas = []

    for h in range(9, 21):
        horas.append([h, 0, 0])

    for evento in eventos:
        if evento.event_type == "linger" and evento.zone_id == zona_escolhida:
            hora = int(evento.timestamp[11:13])

            if hora >= 9 and hora < 21:
                indice = hora - 9
                horas[indice][1] += int(evento.duration_s)
                horas[indice][2] += 1

    print("\nMÉDIA DE PERMANÊNCIA -", zona_escolhida)

    for item in horas:
        hora = item[0]
        soma = item[1]
        quantidade = item[2]

        if quantidade > 0:
            media = soma / quantidade
        else:
            media = 0

        print(str(hora) + ":00-" + str(hora + 1) + ":00", "->", round(media, 2), "segundos")

def juntar_eventos_temporais(esquerda, direita):
    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i][0] <= direita[j][0]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado

def query_picos_ocupacao(eventos, dia, k):
    eventos_dia = []

    for evento in eventos:
        if evento.timestamp[0:10] == dia:
            if evento.event_type == "entry":
                eventos_dia.append([evento.timestamp, 1])
            elif evento.event_type == "exit":
                eventos_dia.append([evento.timestamp, -1])

    eventos_dia = merge_sort_eventos_temporais(eventos_dia)

    heap = MaxHeap()
    ocupacao = 0

    for item in eventos_dia:
        timestamp = item[0]
        variacao = item[1]

        ocupacao += variacao
        heap.insert([timestamp, ocupacao])

    print(f"\nTOP {k} PICOS DE OCUPAÇÃO - {dia}")

    for i in range(k):
        pico = heap.remove_max()
        if pico is not None:
            print(pico[0], "->", pico[1], "pessoas")
            
def query_top_k_zonas_periodo(eventos, inicio, fim, k):
    tabela = TabelaHash()

    eventos_intervalo = filtrar_eventos_intervalo(eventos, inicio, fim)

    for evento in eventos_intervalo:
        if evento.event_type == "entry":
            tabela.incrementar(evento.zone_id)

    contagens = tabela.itens()

    heap = MaxHeap()

    for item in contagens:
        heap.insert(item)

    print(f"\nTOP {k} ZONAS MAIS VISITADAS ({inicio} até {fim})")

    for i in range(k):
        top = heap.remove_max()
        if top is not None:
            print(top[0], "->", top[1])

def total_visitantes_dia(eventos, dia):
    total = 0

    inicio = dia + " 00:00:00"
    fim = dia + " 23:59:59"
    eventos_dia = filtrar_eventos_intervalo(eventos, inicio, fim)

    for evento in eventos_dia:
        if evento.event_type == "entry":
            total += 1

    return total


def media_permanencia_dia(eventos, dia):
    soma = 0
    quantidade = 0

    inicio = dia + " 00:00:00"
    fim = dia + " 23:59:59"
    eventos_dia = filtrar_eventos_intervalo(eventos, inicio, fim)

    for evento in eventos_dia:
        if evento.event_type == "linger":
            soma += int(evento.duration_s)
            quantidade += 1

    if quantidade == 0:
        return 0

    return soma / quantidade


def zona_mais_visitada_dia(eventos, dia):
    inicio = dia + " 00:00:00"
    fim = dia + " 23:59:59"

    contagens = contar_entradas_por_zona_intervalo(eventos, inicio, fim)

    if len(contagens) == 0:
        return ["Nenhuma", 0]

    contagens, _ = merge_sort_contagens(contagens)

    return contagens[0]

def query_comparacao_entre_dias(eventos, dia1, dia2):
    total1 = total_visitantes_dia(eventos, dia1)
    total2 = total_visitantes_dia(eventos, dia2)

    media1 = media_permanencia_dia(eventos, dia1)
    media2 = media_permanencia_dia(eventos, dia2)

    zona1 = zona_mais_visitada_dia(eventos, dia1)
    zona2 = zona_mais_visitada_dia(eventos, dia2)

    print("\nCOMPARAÇÃO ENTRE DIAS")
    print("Dia 1:", dia1)
    print("Total visitantes:", total1)
    print("Média permanência:", round(media1, 2), "segundos")
    print("Zona mais visitada:", zona1[0], "->", zona1[1])

    print("\nDia 2:", dia2)
    print("Total visitantes:", total2)
    print("Média permanência:", round(media2, 2), "segundos")
    print("Zona mais visitada:", zona2[0], "->", zona2[1])

def query_top_k_periodos_afluencia(eventos, inicio, fim, k, zona_filtro):
    blocos = []

    for evento in eventos:
        if inicio <= evento.timestamp <= fim:
            if zona_filtro == "" or evento.zone_id == zona_filtro:
                hora = int(evento.timestamp[11:13])
                minuto = int(evento.timestamp[14:16])

                if minuto < 30:
                    bloco_inicio = evento.timestamp[0:11] + str(hora).zfill(2) + ":00:00"
                    bloco_fim = evento.timestamp[0:11] + str(hora).zfill(2) + ":29:59"
                else:
                    bloco_inicio = evento.timestamp[0:11] + str(hora).zfill(2) + ":30:00"
                    bloco_fim = evento.timestamp[0:11] + str(hora).zfill(2) + ":59:59"

                nome_bloco = bloco_inicio + " até " + bloco_fim
                encontrado = False

                for i in range(len(blocos)):
                    if blocos[i][0] == nome_bloco:
                        blocos[i][1] += 1
                        encontrado = True
                        break

                if not encontrado:
                    blocos.append([nome_bloco, 1])

    heap = MaxHeap()

    for item in blocos:
        heap.insert(item)

    print(f"\nTOP {k} PERÍODOS DE MAIOR AFLUÊNCIA")

    for i in range(k):
        maior = heap.remove_max()
        if maior is not None:
            print(maior[0], "->", maior[1], "eventos")

def query_zonas_maior_permanencia(eventos, k, genero_filtro, idade_filtro):
    zonas = []

    for evento in eventos:
        if evento.event_type == "linger":
            if genero_filtro == "" or evento.gender == genero_filtro:
                if idade_filtro == "" or evento.age_range == idade_filtro:
                    zona = evento.zone_id
                    duracao = int(evento.duration_s)
                    encontrado = False

                    for i in range(len(zonas)):
                        if zonas[i][0] == zona:
                            zonas[i][1] += duracao
                            zonas[i][2] += 1
                            encontrado = True
                            break

                    if not encontrado:
                        zonas.append([zona, duracao, 1])

    heap = MaxHeap()

    for item in zonas:
        zona = item[0]
        soma = item[1]
        quantidade = item[2]

        media = soma / quantidade
        heap.insert([zona, media])

    print(f"\nTOP {k} ZONAS COM MAIOR TEMPO MÉDIO DE PERMANÊNCIA")

    for i in range(k):
        maior = heap.remove_max()
        if maior is not None:
            print(maior[0], "->", round(maior[1], 2), "segundos")
#======12=======
def query_perfil_demografico(eventos, zona, dia_filtro, hora_inicio, hora_fim):
    generos = []
    idades = []

    for evento in eventos:
        if evento.event_type == "entry":

            if zona != "" and evento.zone_id != zona:
                continue

            if dia_filtro != "" and evento.timestamp[0:10] != dia_filtro:
                continue

            hora = int(evento.timestamp[11:13])

            if hora_inicio != "" and hora < int(hora_inicio):
                continue

            if hora_fim != "" and hora >= int(hora_fim):
                continue

            encontrado = False
            for i in range(len(generos)):
                if generos[i][0] == evento.gender:
                    generos[i][1] += 1
                    encontrado = True
                    break
            if not encontrado:
                generos.append([evento.gender, 1])

            encontrado = False
            for i in range(len(idades)):
                if idades[i][0] == evento.age_range:
                    idades[i][1] += 1
                    encontrado = True
                    break
            if not encontrado:
                idades.append([evento.age_range, 1])

    print("\nPERFIL DEMOGRÁFICO")

    if zona != "":
        print("Zona:", zona)
    if dia_filtro != "":
        print("Dia:", dia_filtro)
    if hora_inicio != "" and hora_fim != "":
        print("Faixa horária:", hora_inicio + ":00-" + hora_fim + ":00")

    print("\nPor género:")
    for g in generos:
        print(g[0], "->", g[1])

    print("\nPor faixa etária:")
    for i in idades:
        print(i[0], "->", i[1])
#Fim12

#10
def raiz_quadrada(valor):
    if valor == 0:
        return 0

    tentativa = valor

    for i in range(20):
        tentativa = (tentativa + valor / tentativa) / 2

    return tentativa


def query_anomalias(eventos):
    dados = []

    for evento in eventos:
        if evento.event_type == "entry":
            zona = evento.zone_id
            dia = evento.timestamp[0:10]
            hora = evento.timestamp[11:13] + ":00-" + str(int(evento.timestamp[11:13]) + 1) + ":00"
            bloco = dia + " " + hora

            encontrado = False

            for i in range(len(dados)):
                if dados[i][0] == zona and dados[i][1] == bloco:
                    dados[i][2] += 1
                    encontrado = True
                    break

            if not encontrado:
                dados.append([zona, bloco, 1])

    zonas = []

    for item in dados:
        zona = item[0]

        if zona not in zonas:
            zonas.append(zona)

    print("\nANOMALIAS POR ZONA")

    for zona in zonas:
        valores = []

        for item in dados:
            if item[0] == zona:
                valores.append(item[2])

        soma = 0
        for valor in valores:
            soma += valor

        media = soma / len(valores)

        soma_desvios = 0
        for valor in valores:
            diferenca = valor - media
            soma_desvios += diferenca * diferenca

        variancia = soma_desvios / len(valores)
        desvio = raiz_quadrada(variancia)

        print("\nZona:", zona)
        encontrou = False

        for item in dados:
            if item[0] == zona:
                contagem = item[2]

                if contagem > media + 2 * desvio or contagem < media - 2 * desvio:
                    print(item[1], "->", contagem, "entradas")
                    encontrou = True

        if not encontrou:
            print("Sem anomalias")
#11
def query_composta(eventos, inicio, fim, zona_filtro, genero_filtro, idade_filtro):
    total_eventos = 0
    soma_permanencia = 0
    quantidade_linger = 0

    distribuicao_horas = []

    for h in range(9, 21):
        distribuicao_horas.append([h, 0])

    for evento in eventos:
        if inicio <= evento.timestamp <= fim:

            if zona_filtro == "" or evento.zone_id == zona_filtro:
                if genero_filtro == "" or evento.gender == genero_filtro:
                    if idade_filtro == "" or evento.age_range == idade_filtro:

                        total_eventos += 1

                        hora = int(evento.timestamp[11:13])
                        if hora >= 9 and hora < 21:
                            indice = hora - 9
                            distribuicao_horas[indice][1] += 1

                        if evento.event_type == "linger":
                            soma_permanencia += int(evento.duration_s)
                            quantidade_linger += 1

    if quantidade_linger > 0:
        media = soma_permanencia / quantidade_linger
    else:
        media = 0

    print("\nQUERY COMPOSTA")
    print("Total de eventos:", total_eventos)
    print("Tempo médio de permanência:", round(media, 2), "segundos")

    print("\nDistribuição por hora:")
    for item in distribuicao_horas:
        print(str(item[0]) + ":00-" + str(item[0] + 1) + ":00", "->", item[1], "eventos")

def query_fluxo_entre_zonas(eventos, threshold, n):
    transicoes = []

    for i in range(len(eventos)):
        evento_saida = eventos[i]

        if evento_saida.event_type == "exit":
            for j in range(i + 1, len(eventos)):
                evento_entrada = eventos[j]

                if evento_entrada.timestamp[0:10] != evento_saida.timestamp[0:10]:
                    break

                if evento_entrada.event_type == "entry":
                    mesma_pessoa = (
                        evento_saida.gender == evento_entrada.gender and
                        evento_saida.age_range == evento_entrada.age_range
                    )

                    if mesma_pessoa:
                        tempo_saida = timestamp_para_segundos(evento_saida.timestamp)
                        tempo_entrada = timestamp_para_segundos(evento_entrada.timestamp)
                        diferenca = tempo_entrada - tempo_saida

                        if diferenca >= 0 and diferenca <= threshold:
                            origem = evento_saida.zone_id
                            destino = evento_entrada.zone_id

                            if origem != destino:
                                encontrado = False

                                for k in range(len(transicoes)):
                                    if transicoes[k][0] == origem and transicoes[k][1] == destino:
                                        transicoes[k][2] += 1
                                        encontrado = True
                                        break

                                if not encontrado:
                                    transicoes.append([origem, destino, 1])

                            break

    heap = MaxHeap()

    for item in transicoes:
        heap.insert([[item[0], item[1]], item[2]])

    print(f"\nTOP {n} TRANSIÇÕES ENTRE ZONAS")

    for i in range(n):
        maior = heap.remove_max()
        if maior is not None:
            origem = maior[0][0]
            destino = maior[0][1]
            quantidade = maior[1]
            print(origem, "->", destino, ":", quantidade)
#8
def construir_sequencia_zonas(eventos):
    entradas = []

    for evento in eventos:
        if evento.event_type == "entry":
            entradas.append([evento.timestamp, evento.zone_id])

    entradas = merge_sort_eventos_temporais(entradas)

    sequencia = ""

    for i in range(len(entradas)):
        sequencia += entradas[i][1]

        if i < len(entradas) - 1:
            sequencia += "-"

    return sequencia


def calcular_prefixos_kmp(padrao):
    prefixos = []
    for i in range(len(padrao)):
        prefixos.append(0)

    tamanho = 0
    i = 1

    while i < len(padrao):
        if padrao[i] == padrao[tamanho]:
            tamanho += 1
            prefixos[i] = tamanho
            i += 1
        else:
            if tamanho != 0:
                tamanho = prefixos[tamanho - 1]
            else:
                prefixos[i] = 0
                i += 1

    return prefixos


def kmp_procurar(texto, padrao):
    if padrao == "":
        return 0

    prefixos = calcular_prefixos_kmp(padrao)

    i = 0
    j = 0
    ocorrencias = 0

    while i < len(texto):
        if texto[i] == padrao[j]:
            i += 1
            j += 1

        if j == len(padrao):
            ocorrencias += 1
            j = prefixos[j - 1]

        elif i < len(texto) and texto[i] != padrao[j]:
            if j != 0:
                j = prefixos[j - 1]
            else:
                i += 1

    return ocorrencias


def query_pesquisa_sequencia(eventos, padrao):
    sequencia = construir_sequencia_zonas(eventos)

    ocorrencias = kmp_procurar(sequencia, padrao)

    print("\nPESQUISA DE SEQUÊNCIA DE ZONAS")
    print("Padrão:", padrao)
    print("Ocorrências encontradas:", ocorrencias)

lista_zonas = ["Z_E1", "Z_E2", "Z_X1", "Z_CK", "Z_C1", "Z_C2", "Z_C3",
               "Z_S1", "Z_S2", "Z_S3", "Z_S4", "Z_S5", "Z_S6", "Z_S7",
               "Z_N1", "Z_N2", "Z_N3", "Z_N4", "Z_N5", "Z_N6", "Z_N7",
               "Z_N8", "Z_N9", "Z_N10"]
# =========================
# MENU
# =========================
def menu(eventos,lista_zonas):
    while True:
        print("\n===== MOTOR DE ANALYTICS =====")
        print("1 - Top-K zonas mais visitadas")
        print("2 - Ocupação por zona num intervalo")
        print("3 - Média de permanência por zona")
        print("4 - Picos de ocupação")
        print("5 - Top-K zonas num intervalo")
        print("6 - Comparação entre dias")
        print("7 - Top-K períodos de maior afluência")
        print("8 - Zonas com maior tempo médio de permanência")
        print("9 - Perfil demográfico por zona")
        print("10 - Deteção de anomalias")
        print("11 - Query composta")
        print("12 - Fluxo entre zonas")
        print("13 - Pesquisa de sequência de zonas")
        print("14 - Comparar algoritmos de ordenação")
        print("15 - Estatísticas da Hash Table")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                k = int(input("Quantas zonas quer ver? "))
            except:
                 print("Valor Invalido")
                 continue
            inicio_tempo = time.time()

            query_top_k_zonas(eventos, k)

            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")        
        
        elif opcao == "2":
             inicio = input("Data/hora início (YYYY-MM-DD HH:MM:SS): ")
             fim = input("Data/hora fim (YYYY-MM-DD HH:MM:SS): ")
             if inicio > fim:
                 print("Intervalo inválido: início maior que fim")
                 continue
             tipo_zona = input("Tipo de zona para filtrar (ex: Z_C, Z_E ou enter para todas): ")
             inicio_tempo = time.time()
             query_ocupacao_por_zona_intervalo(eventos, inicio, fim, tipo_zona)
             fim_tempo = time.time()

             print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "3":
             zona = input("Digite a zona (ex: Z_C2): ")
             if zona not in lista_zonas:
                  print("Zona inválida")
             else:
                  inicio_tempo = time.time()

                  query_media_permanencia_por_zona(eventos, zona)

                  fim_tempo = time.time()
                  print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos") 

        elif opcao == "4":
            dia = input("Digite o dia (YYYY-MM-DD): ")
            k = int(input("Quantos picos quer ver? "))
            inicio_tempo = time.time()
            query_picos_ocupacao(eventos, dia, k)
            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos") 
          
        elif opcao == "5":
            inicio = input("Data/hora início (YYYY-MM-DD HH:MM:SS): ")
            fim = input("Data/hora fim (YYYY-MM-DD HH:MM:SS): ")

            try:
                k = int(input("Quantas zonas quer ver? "))
            except:
                print("Valor inválido")
                continue

            inicio_tempo = time.time()
            query_top_k_zonas_periodo(eventos, inicio, fim, k)
            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "6":
            dia1 = input("Digite o primeiro dia (YYYY-MM-DD): ")
            dia2 = input("Digite o segundo dia (YYYY-MM-DD): ")
            inicio_tempo = time.time()
            query_comparacao_entre_dias(eventos, dia1, dia2)
            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "7":
            inicio = input("Data/hora início (YYYY-MM-DD HH:MM:SS): ")
            fim = input("Data/hora fim (YYYY-MM-DD HH:MM:SS): ")
            zona = input("Zona para filtrar (enter para todas): ")

            try:
                k = int(input("Quantos períodos quer ver? "))
            except:
                print("Valor inválido")
                continue

            inicio_tempo = time.time()
            query_top_k_periodos_afluencia(eventos, inicio, fim, k, zona)
            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "8":
            genero = input("Filtrar género (M/F ou enter para todos): ")
            idade = input("Filtrar faixa etária (ex: adult ou enter para todas): ")

            try:
                k = int(input("Quantas zonas quer ver? "))
            except:
                print("Valor inválido")
                continue

            inicio_tempo = time.time()
            query_zonas_maior_permanencia(eventos, k, genero, idade)
            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "9":
            zona = input("Digite a zona (enter para todas): ")
            dia = input("Digite o dia (YYYY-MM-DD ou enter para todos): ")
            hora_inicio = input("Hora início (ex: 9 ou enter): ")
            hora_fim = input("Hora fim (ex: 12 ou enter): ")

            inicio_tempo = time.time()
            query_perfil_demografico(eventos, zona, dia, hora_inicio, hora_fim)
            fim_tempo = time.time()

            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "10":
            inicio_tempo = time.time()

            query_anomalias(eventos)

            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "11":
            inicio = input("Data/hora início (YYYY-MM-DD HH:MM:SS): ")
            fim = input("Data/hora fim (YYYY-MM-DD HH:MM:SS): ")
            zona = input("Zona (enter para todas): ")
            genero = input("Género M/F (enter para todos): ")
            idade = input("Faixa etária (enter para todas): ")

            inicio_tempo = time.time()
            query_composta(eventos, inicio, fim, zona, genero, idade)
            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")  

        elif opcao == "12":
            threshold = int(input("Threshold em segundos: "))
            n = int(input("Quantas transições quer ver? "))
            inicio_tempo = time.time()
            query_fluxo_entre_zonas(eventos, threshold, n)
            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")

        elif opcao == "13":
            padrao = input("Digite a sequência (ex: Z_E1-Z_C1-Z_S3): ")
            inicio_tempo = time.time()

            query_pesquisa_sequencia(eventos, padrao)

            fim_tempo = time.time()
            print("Tempo de execução:", round(fim_tempo - inicio_tempo, 4), "segundos")  

        elif opcao == "14":
             comparar_ordenacoes(eventos)
             
       
        elif opcao == "15":
             tabela = TabelaHash()

             for evento in eventos:
                 if evento.event_type == "entry":
                    tabela.incrementar(evento.zone_id)

             print("\nESTATÍSTICAS DA HASH TABLE")
             print("Tamanho da tabela:", tabela.tamanho)
             print("Load factor:", round(tabela.load_factor(), 4))
             print("Colisões:", tabela.contar_colisoes())

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("Opção inválida.")
# =========================
# PROGRAMA PRINCIPAL
# =========================
eventos = ler_csv("events.csv")
menu(eventos,lista_zonas)


        
