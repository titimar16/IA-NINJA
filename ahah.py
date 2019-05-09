import cherrypy
import sys
import random
from easyAI import TwoPlayersGame, AI_Player, Negamax,Human_Player


class Match(TwoPlayersGame):
    def __init__(self, players, body, indice):
        self.players = players

        self.board = body["game"]
        self.transform()
        self.nplayer = 1  # player 1 starts.

        self.forbidden = {'E': [4, 9, 14, 19, 24], 'W': [0, 5, 10, 15, 20], 'N': [0, 1, 2, 3, 4], 'S': [20, 21, 22, 23, 24]}
        self.increments = {'N': -5, 'S': 5, 'E': 1, 'W': -1}
        self.reverseDir = {"N": "S", "S": "N", "E": "W", "W": "E"}
        self.poss = [[0, 1, 2, 3, 4],
                     [5, 6, 7, 8, 9],
                     [10, 11, 12, 13, 14],
                     [15, 16, 17, 18, 19],
                     [20, 21, 22, 23, 24],
                     [0, 5, 10, 15, 20],
                     [1, 6, 11, 16, 21],
                     [2, 7, 12, 17, 22],
                     [3, 8, 13, 18, 23],
                     [4, 9, 14, 19, 24],
                     [0, 6, 12, 18, 24],
                     [4, 8, 12, 16, 20]]

        self.history = [[0],[0]]

    def transform(self):
        print(self.board)
        for i,x in enumerate(self.board):
            if x != None:
                self.board[i]= x+1
            else:
                self.board[i] = 0
        print(self.board)
    def possible_moves(self):

        dic = {'E': [4, 9, 14, 19, 24], 'W': [0, 5, 10, 15, 20], 'N': [0, 1, 2, 3, 4], 'S': [20, 21, 22, 23, 24]}

        indices = [i for i, x in enumerate(self.board) if x == 0] + [i for i, x in
                                                                               enumerate(self.board) if
                                                                               x == 1]

        to_remove = [6, 7, 8, 11, 12, 13, 16, 17, 18]
        for i in to_remove:  # enleve les cases du milieux
            if i in indices:
                indices.remove(i)
        G = ['W', 'S','E', 'N' ]
        possibleMov = []
        for dir in G:
            for elem in indices:
                if elem not in dic[dir]:
                    possibleMov.append(str(elem) + " "+ dir)

        return  possibleMov

    def scoring(self):
        if self.lose() :
            return -100
        else:
            return 0
    def lose(self):
        return any([all([(self.board[c ] == self.nopponent)
                         for c in line])
                    for line in self.poss])  # diagonal

    def is_over(self):
        return self.lose()

    def make_move(self,move) :
        a = move.split()
        dir = a[1]
        cube = int(a[0])
        pos = cube


        if self.board[cube] != 0:
            self.history[self.nplayer - 1 ].append(self.nplayer)
        else:
            self.history[self.nplayer - 1 ].append(0)


        while pos not in self.forbidden[dir]:
            self.board[pos] = self.board[pos + self.increments[dir]]
            pos += self.increments[dir]
        self.board[pos] = self.nplayer
      #  print("move make" + " " + str(self.nplayer) + " "+ move)
      #  self.show()


    def unmake_move(self,move):
        a = move.split() #3E
        dir = a[1]  #E
        dirOppose = self.reverseDir[dir] #W
        cube = int(a[0]) #3
        pos = cube #3
        while pos not in self.forbidden[dir]:
            pos += self.increments[dir]

        while pos !=  cube   :
            self.board[pos] = self.board[pos + self.increments[dirOppose]]
            pos += self.increments[dirOppose]


        length = len(self.history[self.nplayer-1])
        self.board[pos] = self.history[self.nplayer - 1][length-1]
        del self.history[self.nplayer-1][length-1]


    #    print("move unmake" + " "+ str(self.nplayer)+ " "+ move)
    #    self.show()


    def show(self):
        print('\n' + '\n'.join([
            ' '.join([['.', 'O', 'X'][self.board[5 * j + i]]
                      for i in range(5)])
            for j in range(5)]))



class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''

        self.body = cherrypy.request.json
        if self.body["players"][0] == self.body["you"]:
            self.couleur = 0
        else:
            self.couleur = 1
        match = Match([AI_Player(Negamax(4)),Human_Player()], self.body, self.couleur)
        nextMove = match.get_move()
        a = nextMove.split()

        return {"move": {"cube": int(a[0]),
                         "direction": a[1]}}  # Trouver algorithme #Nique la police #Les poulets faut les fumer

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8081

    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())