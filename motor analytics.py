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
        eventos=[]

        ficheiro=open(nome_ficheiro, "r", encoding="utf-8")
        linhas=ficheiro.readlines()
        ficheiro.close

        for i in range(1, len(linhas)):
            linha=linhas[i].strip()
            parte=linha.split(",")
            evento=Event(parte[0],parte[1],parte[2],parte[3],parte[4],parte[5],parte[6])
            eventos.append(evento)

        return eventos

def contar_entradas_por_zona(eventos):
     contagens=[]

     for evento in eventos:
          if evento.event_type == "entry":
               zona=evento.zone_id
               encontrado=False

               for i in range(len(contagens)):
                    if contagens[i][0]==zona:
                         contagens[i][1]+=1
                         encontrado=True
                         break
                    
               if not encontrado:
                    contagens.append([zona,1])
     return contagens

def ordenar_contagens(contagens):
     n=len(contagens)

     for i in range(n):
          for j in range(0, n-i-1):
               if contagens[j][1]<contagens[j+1][1]:
                    temp=contagens[j]
                    contagens[j]=contagens[j+1]
                    contagens[j+1]=temp

     return contagens

class MaxHeap:
    def __init__(self):
        self.dados = []

def top_k_zonas(contagens, k):
    top = []
    for i in range(k):
        top.append(contagens[i])

    return top


eventos=ler_csv("events.csv")
print("TOTAL DE EVENTOS:", len(eventos))
print(eventos[0].event_id)
print(eventos[1].zone_id)
print(eventos[2].event_type)

resultado=contar_entradas_por_zona(eventos)
ordenado=ordenar_contagens(resultado)
top3 = top_k_zonas(ordenado, 3)
for item in top3:
     print(item[0], "->",item[1])



        
