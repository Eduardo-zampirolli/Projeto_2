from basic_players import Player

# Implemente neste arquivo seus jogadores


#Armazenar todas as peças possíveis
pecas_disp = []
for i in range(10):
    for j in range(10):
        if (j,i) not in pecas_disp:
            pecas_disp.append((i,j))


# Jogador que não faz nada. Subsitua esta classe pela(s) sua(s), ela(s) deve(m) herdar da classe Player
class NonePLayer(Player):

    def __init__(self):
        super().__init__(0, "Ninguém")
        self.num_disp = {i: 11 for i in range(10)}   
        self.valores = {i:0 for i in range(10)}     

    def play(self, board_extremes, play_hist):
        #Criar uma lista que armazena todas peças disponíveis para os demais jogadores
        if len(self._tiles) == 10:
            #num_dispj1 = {i: 11 for i in range(10)}
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
            for k in range(-len(play_hist),0):
                if play_hist[k][3] != None: 
                    self.num_disp[play_hist[k][3][0]] -= 1
                    self.num_disp[play_hist[k][3][1]] -= 1
        
        playable_tiles = self._tiles
        if len(board_extremes) > 0:
            playable_tiles = [tile for tile in self._tiles if tile[0] in board_extremes or tile[1] in board_extremes]
        highest = -1
        tile_sum = -1
        jogada = (-1,-1)
        for i in range(len(playable_tiles)):
            if playable_tiles[i][0] == playable_tiles[i][1] and playable_tiles[i][0] > jogada[0]:
                jogada = playable_tiles[i]
            if jogada[0] != -1:
                return 1, playable_tiles[i]
        for i in range(len(playable_tiles)):
            if playable_tiles[i][0] + playable_tiles[i][1] > tile_sum:
                tile_sum = playable_tiles[i][0] + playable_tiles[i][1]
                highest = i
        if highest >= 0:
            return 1, playable_tiles[highest]
        else:
            return 1, None
        
		
# Função que define o nome da dupla:
def pair_name():
    return "algum nome" # Defina aqui o nome da sua dupla

# Função que cria a dupla:
def create_pair():
    return (NonePLayer(), NonePLayer()) # Defina aqui a dupla de jogadores. Deve ser uma tupla com dois jogadores.	
