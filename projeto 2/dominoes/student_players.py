from basic_players import Player

# Implemente neste arquivo seus jogadores


#Armazenar todas as peças possíveis
pecas_disp = []
for i in range(10):
    for j in range(10):
        if (j,i) not in pecas_disp:
            pecas_disp.append((i,j))


# Jogador que não faz nada. Subsitua esta classe pela(s) sua(s), ela(s) deve(m) herdar da classe Player
class AnalystPlayer(Player):

    def __init__(self):
        super().__init__(0, "Analisador")
        self.num_disp = {i: 11 for i in range(10)} #Frequência de cada número disponível para os outros jogadores
        self.valores = {i:0 for i in range(10)} #Frequência de cada número para o jogador
        self.prox_sem = set() #Valores que o proximo não tem (jogar para bloquear)
        self.dupla_sem = set() #Valores que a dupla não tem (evitar jogar se for tentar bloquear)
        
    
    def analise_freq(self, pecas_jogaveis, extremos):
        """Escolhe a peça maior e de maior frequencia"""

        pecas_bloqueadoras = []
        melhor_peca = (0, 0) #Peça de maior frequência e/ou maior
        peca_mais_alta = (0, 0)
        melhor_freq = 0
        mais_rara = None
        melhor_dupla = None

        if len(pecas_jogaveis) > 0:
            
            melhor_peca = pecas_jogaveis[0]
            melhor_freq = self.valores[pecas_jogaveis[0][0]] + self.valores[pecas_jogaveis[0][1]]
        
        #Escolhe dupla (as duplas recebem prioridade)
        for peca in pecas_jogaveis:
            if peca[0] == peca[1]:
                if melhor_dupla == None:
                    melhor_dupla = peca
                else:
                    if peca[0] * 2 > melhor_dupla[0] * 2:
                        melhor_dupla = peca
            
            
            #Ver peças de bloqueio
            if len(extremos) > 0:
                if self.check_sem(peca, extremos[1]) != None:
                    pecas_bloqueadoras.append([peca,extremos[1]])
                    
                    
                elif self.check_sem(peca, extremos[0]) != None:
                    pecas_bloqueadoras.append([peca,extremos[0]])
                    
            #Escolhe peça de maior frequencia de números (manter variedade de números)    
            if self.valores[peca[0]] + self.valores[peca[1]] > melhor_freq and self.valores[peca[0]] > 1 and self.valores[peca[1]] > 1:
                melhor_peca = peca
                melhor_freq = self.valores[peca[0]] + self.valores[peca[1]]
            
            if peca[0] + peca[1] > peca_mais_alta[0] + peca_mais_alta[1]:
                peca_mais_alta = peca

            #Escolher peça mais rara
            if mais_rara == None:
                if peca[0] in extremos:
                    mais_rara = [peca,peca[1]]
                else:
                    mais_rara = [peca,peca[0]]
            else:
                raridade = self.chances()
                if  peca[0] in extremos:
                    if raridade.index(peca[1]) < raridade.index(mais_rara[1]):
                        mais_rara = [peca,peca[1]]
                else:
                    if raridade.index(peca[0]) < raridade.index(mais_rara[1]):
                        mais_rara = [peca,peca[0]]

        #Escolhe a melhor peça bloqueadora
        if len(pecas_bloqueadoras) > 0:
            melhor = [(0,0),0]
            for peca in pecas_bloqueadoras:
                if peca[0][0] + peca[0][1] > melhor[0][0] + melhor[0][1]:
                    melhor = peca
            self.valores[melhor[0][0]] -= 1
            self.valores[melhor[0][1]] -= 1
            

            return melhor[1], melhor[0]
        
        #Se as frequencias não forem altas o bastante, escolhe entre a peça mais alta e a mais rara
        if melhor_freq < 4:
            #Caso a mais rara tenha uma quantidade menor de 3 e o seu amigo tem essa peça faltante
            if mais_rara != None and self.num_disp[mais_rara[1]] < 3 and mais_rara[1] not in self.dupla_sem:
                melhor_peca = mais_rara[0]
            #Ao contrário, escolher a peça com valor mais alto
            else:
                melhor_peca = peca_mais_alta
        
        #Duplas recebem prioridade
        if melhor_dupla != None:
            melhor_peca = melhor_dupla
                
        self.valores[melhor_peca[0]] -= 1
        self.valores[melhor_peca[1]] -= 1
        
        
        return 0, melhor_peca


    def play(self, board_extremes, play_hist):

        #Armazena a frequencia dos números que os outros jogadores podem ter e a frequencia dos que o jogador tem
        if len(self._tiles) == 10:
            self.num_disp = {i: 11 for i in range(10)} #Frequência de cada número disponível para os outros jogadores
            self.valores = {i:0 for i in range(10)} #Frequência de cada número para o jogador
            self.prox_sem = set() #Valores que o proximo não tem (jogar para bloquear)
            self.dupla_sem = set()
            for peca in self._tiles:
                self.num_disp[peca[0]] -= 1
                self.num_disp[peca[1]] -= 1
                self.valores[peca[0]] += 1
                self.valores[peca[1]] += 1
            

        if len(play_hist) > 2:
            
            for k in range(-3,0):
                if play_hist[k][3] != None: 
                    self.num_disp[play_hist[k][3][0]] -= 1
                    self.num_disp[play_hist[k][3][1]] -= 1
                else:
                    #Vê se o próximo ou a dupla não jogaram para saber as peças que eles não tem
                    if k == -3:
                        self.prox_sem.add(play_hist[k][1][0])  
                        self.prox_sem.add(play_hist[k][1][1])
                    elif k == -2:
                        self.dupla_sem.add(play_hist[k][1][0])  
                        self.dupla_sem.add(play_hist[k][1][1])
        else:
            for k in range(-len(play_hist),0):
                if play_hist[k][3] != None: 
                    self.num_disp[play_hist[k][3][0]] -= 1
                    self.num_disp[play_hist[k][3][1]] -= 1
        
        playable_tiles = self._tiles
        #Estabelecer quas são as peças jogáveis
        if len(board_extremes) > 0:
            playable_tiles = [tile for tile in self._tiles if tile[0] in board_extremes or tile[1] in board_extremes]
        #Retornar a peça que foi escolhida por meio da função de análise
        if playable_tiles != None:
            peca_e_extremo = self.analise_freq(playable_tiles, board_extremes)
            return peca_e_extremo[0], peca_e_extremo[1]
        else:
            return 1, None
   
    def check_sem(self, tile, extremo):
        """Recebe uma peça e uma extremidade e verifica se ela deve ser colocada baseado no que o amigo e o proximo têm"""

        if tile[0] == extremo and extremo not in self.prox_sem and tile[1] in self.prox_sem:
            if tile[1] not in self.dupla_sem:
                return tile
        if tile[1] == extremo and extremo not in self.prox_sem and tile[0] in self.prox_sem:
            if tile[0] not in self.dupla_sem:
                return tile
        return None
    
    
    def chances(self):
        '''Função que retorna a lista odenada dos valores mais raros até os mais comuns'''

        aux = self.num_disp
        ordenado = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}
        lista = []
        for i in ordenado:
            lista.append(i)

        return lista
            

# Função que define o nome da dupla:
def pair_name():
    return "Dupla Analista" # Defina aqui o nome da sua dupla

# Função que cria a dupla:
def create_pair():
    return (AnalystPlayer(), AnalystPlayer()) # Defina aqui a dupla de jogadores. Deve ser uma tupla com dois jogadores.	
