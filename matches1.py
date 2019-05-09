import cherrypy
import sys
import time
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
        body = cherrypy.request.json
        jaja = self.Action(body["game"],body["you"],body["players"],body["moves"])
        return jaja
    def Action(self,game,you,players,moves):
        direction = ""
        Myself = 0
        if players[0] == you:
            Myself = 0
        else:
            Myself = 1
        myButtonList = self.convertListButtons(game,Myself)
        iaCmd = utilsQuixo().startIA(myButtonList)
        if iaCmd[1] == True and iaCmd[2] == True:
            direction = "E"
        elif iaCmd[1] == True and iaCmd[2] == False:
            direction = "W"
        elif iaCmd[1] == False and iaCmd[2] == True:
            direction = "S"
        elif iaCmd[1] == False and iaCmd[2] == False:
            direction = "N"
        return {"move" : {"cube" : int(iaCmd[3]), "direction" : str(direction)} , "message": self.returnMessage(iaCmd[0])}
    def convertListButtons(self,moves,myself):
        listbutton = []
        for i in range(25):
            if moves[i] == None:
                btn = Button()
                btn.background_normal = "case2.png"
                btn.background_down = "case2.png"
                btn.guid = str(i)
                listbutton.append(btn)
            elif moves[i] == myself:
                btn = Button()
                btn.background_normal = "casevide2.png"
                btn.background_down = "casevide2.png"
                btn.guid = str(i)
                listbutton.append(btn)
            else:
                btn = Button()
                btn.background_normal = "casevide.png"
                btn.background_down = "casevide.png"
                btn.guid = str(i)
                listbutton.append(btn)
        return listbutton
    beforeWeight = 0
    ennemyName = ""
    def returnMessage(self,weight):
        
        if self.beforeWeight == 0: # on debute la partie
            self.beforeWeight = weight
            return "Debut de la partie, " + self.ennemyName
        elif weight == 1000000000: # on a gagné
            self.beforeWeight = weight
            return "Woow on gagne la partie contre " + self.ennemyName   
        elif weight == -1000000000: # on a perdu
            self.beforeWeight = weight
            return "Woow ca pue tres tres fort pour nous " + self.ennemyName
        elif self.beforeWeight < weight: # on est en position de faiblesse
            self.beforeWeight = weight
            return "Bien joué " + self.ennemyName  
        elif self.beforeWeight > weight: # on est en position de force
            self.beforeWeight = weight
            return "On est chaud chaud balle" 
class utilsQuixo:
    def startIA(self,listebtn):
        simplelist = self.convertToSimpleList(listebtn)
        
        listWeight = self.getTheBestWeight(simplelist,True,True) # liste de liste de tuple = [[(valueWeight,horizontale,droitebas,cell),...]]
        result = self.anticipationBlow(listWeight,simplelist)
        return result
    def anticipationBlow(self,listWeight,simplelist):
        # mode anticipation du tour suivant : on check le poid qu 'on obtient dans le prochain coups
        listWeightTurnTwo = []
        if len(listWeight) > 0:
            for i in range(len(listWeight)):
                for y in range(len(listWeight[i])): # on parcourt toutes les possibilités pour obtenir le meilleur poids a notre tour
                    if listWeight[i][y][0] == 1000000000:
                        return listWeight[i][y]
                    if listWeight[i][y][0] != -1000000000:
                        myliste = self.getFutureBlow(listWeight[i][y][1],listWeight[i][y][2],listWeight[i][y][3],simplelist,True)
                        ennemy = self.getTheBestWeight(myliste,False,False)
                        if ennemy[0] != 1000000000:
                            mynewliste = self.getFutureBlow(ennemy[1],ennemy[2],ennemy[3],myliste,False)
                            listWeightTurnTwo.append((self.getTheBestWeight(mynewliste,True,False),listWeight[i][y]))
            if len(listWeightTurnTwo) > 0:
                BestWeight2 = listWeightTurnTwo[0]
            for i in listWeightTurnTwo:
                if BestWeight2[0][0] < i[0][0]:  
                    BestWeight2 = i
            
            return BestWeight2[1] # meilleur lancé possible
    def getTheBestWeight(self,simplelist,round,returnlist = False):
        cellReachable = self.getReachableCells(simplelist,round)
        listWeight = [] # liste de tuple = [(valueWeight,horizontale,droitebas,cell)]
        for i in cellReachable:
            listWeight.append(self.evaluateAllAction(i,simplelist,round,returnlist))
        if returnlist == True:
            return listWeight
        #mode 1 analyse du jeu
        if len(listWeight) > 0:
            BestWeight = listWeight[0]
            for i in listWeight:
                if BestWeight[0] < i[0]:  
                    BestWeight = i
            return BestWeight # meilleur lancé possible 
    def evaluateAllAction(self,cell,mylist,round,returnlist = False):
        listWeight = [] # list of tuple
        if int(cell) == 0:
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
        elif int(cell) == 20:
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
        elif int(cell) == 4:      
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))      
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
        elif int(cell) == 24:
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
            listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
        else: 
            if int(cell) == 5 or int(cell) == 10 or int(cell) == 15:
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
            if int(cell) == 9 or int(cell) == 14 or int(cell) == 19:
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
            if int(cell) == 1 or int(cell) == 2 or int(cell) == 3:
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
            if int(cell) == 21 or int(cell) == 22 or int(cell) == 23:
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
                listWeight.append((self.generateWeightSpell(cell,self.getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
        if returnlist == True:
            return listWeight
        if len(listWeight) > 0:
            BestWeight = listWeight[0]
            for i in listWeight:
                if BestWeight[0] < i[0]: 
                    BestWeight = i
            return BestWeight
    def generateWeightSpell(self,cell,listebtn,round):
        agressif = 0
        defensif = 0
        if round == True:
            agressif = self.generateWeightMyself(listebtn)
            defensif  = self.generateWeightEnnemy(listebtn) 
        else:
            agressif = self.generateWeightEnnemy(listebtn)
            defensif  = self.generateWeightMyself(listebtn)
        if agressif == 1000000000:
            return agressif # si la possibilité de gagner, on gagne la partie
        if defensif == 1000000000:
            return -1000000000 # si le coups est perdant, on annule le coups
        ratio = agressif - defensif
        return ratio
    def generateWeightMyself(self,mylist):
        #Calcul du nombre de rond aligné on possede
        weight = 0
        indexes = self.getMyselfCells(mylist)
        ## Horizontalement
        for t in range(5):
            num = 0
            for i in range((t * 5) ,(5 * t) + 5):
                if i in indexes:
                    num += 1
            for i in range(num):
                weight += (i + 1)**2 
            if num == 5:
                return 1000000000         
        ## Verticalement
        for t in range(5):
            num = 0
            for i in range(t,t+21,5):
                if i in indexes:
                    num += 1
            for i in range(num):
                weight += (i + 1)**2 
            if num == 5:
                return 1000000000
        ## Diagonale 0,0 -> 4,4
        num = 0
        for i in range(5):
            if self.convertMatrix(i,i) in indexes:
                num += 1
        for i in range(num):
            weight += (i + 1)**2 
        if num == 5:
            return 1000000000
        ## Diagonale 4,0 -> 0,4
        num = 0
        for i in range(5):
            if self.convertMatrix(4-i,i) in indexes:
                num += 1
        for i in range(num):
            weight += (i + 1)**2 
        if num == 5:
            return 1000000000
        return weight
    def generateWeightEnnemy(self,mylist):
        #Calcul du nombre de rond aligné on possede
        weight = 0
        indexes = self.getEnemyCells(mylist)
        ## Horizontalement
        for t in range(5):
            num = 0
            for i in range((t * 5) ,(5 * t) + 5):
                if i in indexes:
                    num += 1
            for i in range(num):
                weight += (i + 1)**2 
            if num == 5:
                return 1000000000     
        ## Verticalement
        for t in range(5):
            num = 0
            for i in range(t,t+21,5):
                if i in indexes:
                    num += 1
            for i in range(num):
                weight += (i + 1)**2 
            if num == 5:
                return 1000000000
        ## Diagonale 0,0 -> 4,4
        num = 0
        for i in range(5):
            if self.convertMatrix(i,i) in indexes:
                num += 1
        for i in range(num):
            weight += (i + 1)**2 
        if num == 5:
            return 1000000000
        ## Diagonale 4,0 -> 0,4
        num = 0
        for i in range(5):
            if self.convertMatrix(4-i,i) in indexes:
                num += 1
        for i in range(num):
            weight += (i + 1)**2 
        if num == 5:
            return 1000000000
        return weight
    def convertToSimpleList(self,listbtn):
        mines = []
        for i in range(len(listbtn)):
            mines.append(listbtn[i].background_normal)
        return mines
    def getFutureBlow(self,horizontale,droitebas,index,mylist,round):
        mines = [] # list 
        mylist2 = [] # list saveCode
        for i in range(len(mylist)):
            mines.append(mylist[i])
            mylist2.append(mylist[i])
        #### Gestion du haut et du bas horizontalement
        if horizontale == True and droitebas == False:
            if int(index) > -1 and int(index) < 5:
                for i in range(int(index)):
                    self.addpictureotherbtn(i+1,i,mylist2,mines)
                self.Addpicture(mines,0,round)
            elif int(index) > 19 and int(index) < 25:
                for i in range(20,int(index)):
                    self.addpictureotherbtn(i+1,i,mylist2,mines)
                self.Addpicture(mines,20,round)
        elif horizontale == True and droitebas == True:
            if int(index) > -1 and int(index) < 5:
                for i in range(4,int(index),-1):
                    self.addpictureotherbtn(i-1,i,mylist2,mines)
                self.Addpicture(mines,4,round)
            elif int(index) > 19 and int(index) < 25:
                for i in range(24,int(index),-1):
                    self.addpictureotherbtn(i-1,i,mylist2,mines)
                self.Addpicture(mines,24,round)
        #### Gestion du haut et du bas verticalement
        if horizontale == False:
            if int(index) > -1 and int(index) < 5:
                for i in range(int(index) + 20,int(index),-5):
                    self.addpictureotherbtn(i-5,i,mylist2,mines)
                self.Addpicture(mines,int(index) + 20,round)
            elif int(index) > 19 and int(index) < 25:
                for i in range(int(index)-20 ,int(index) ,5):
                    self.addpictureotherbtn(i+5,i,mylist2,mines)
                self.Addpicture(mines,int(index) - 20,round)
        ##### Gestion du droite et gauche horizontalement
        if horizontale == True:
            if int(index) == 5 or int(index) == 10 or int(index) == 15:
                for i in range(int(index) + 4,int(index),-1):
                    self.addpictureotherbtn(i-1,i,mylist2,mines)
                self.Addpicture(mines,int(index)+4,round)
            elif int(index) == 9 or int(index) == 14 or int(index) == 19:
                for i in range(int(index)-4,int(index)):
                    self.addpictureotherbtn(i+1,i,mylist2,mines)
                self.Addpicture(mines,int(index)-4,round)
        ##### Gestion du droite et gauche verticalement
        if horizontale == False and droitebas == False:
            if int(index) == 5 or int(index) == 10 or int(index) == 15:
                for i in range(0 ,int(index) ,5):
                    self.addpictureotherbtn(i+5,i,mylist2,mines)
                self.Addpicture(mines,0,round)
            elif int(index) == 9 or int(index) == 14 or int(index) == 19:
                for i in range(4 ,int(index) ,5):
                    self.addpictureotherbtn(i+5,i,mylist2,mines)
                self.Addpicture(mines,4,round)
        elif horizontale == False and droitebas == True:
            if int(index) == 5 or int(index) == 10 or int(index) == 15:
                for i in range(20,int(index),-5):
                    self.addpictureotherbtn(i-5,i,mylist2,mines)
                self.Addpicture(mines,20,round)
            elif int(index) == 9 or int(index) == 14 or int(index) == 19:
                for i in range(24,int(index),-5):
                    self.addpictureotherbtn(i-5,i,mylist2,mines)
                self.Addpicture(mines,24,round)
        return mines
    def Addpicture(self,instance,index,round):
        if round == True:
            instance[index] = "casevide2.png"
        else:
            instance[index] = "casevide.png"
    def addpictureotherbtn(self,index1,index2,savecode,listref):
        listref[index1] = savecode[index2]
        listref[index1] = savecode[index2] 
    def getEnemyCells(self,listebtn):
        # return list of index Enemy Cells 
        mylist = []
        for i in range(len(listebtn)):
            if self.checkIfValueX(listebtn[i]) == True:
                mylist.append(i)
        return mylist
    def getMyselfCells(self,listebtn):
        # return list of index Myself Cells 
        mylist = []
        for i in range(len(listebtn)):
            if self.checkIfValueO(listebtn[i]) == True:
                mylist.append(i)
        return mylist
    def getReachableCells(self,listebtn,round):
        # return list of index Reachable Cells
        mylist = []
        for i in range(len(listebtn)):
            if self.canLaunchSpell(listebtn[i],i,round) == True:
                mylist.append(i)
        return mylist
    def canLaunchSpell(self,btn,index,round):
        if round == True:
            if self.checkIfValueO(btn) == True or self.checkIfValueNothing(btn) == True:
                for i in range(5):
                    if self.convertMatrix(0,i) == index:
                        return True
                for i in range(5):
                    if self.convertMatrix(i,0) == index:
                        return True
                for i in range(5):
                    if self.convertMatrix(4,i) == index:
                        return True
                for i in range(5):
                    if self.convertMatrix(i,4) == index:
                        return True
        if round == False:
            if self.checkIfValueX(btn) == True or self.checkIfValueNothing(btn) == True:
                for i in range(5):
                    if self.convertMatrix(0,i) == index:
                        return True
                for i in range(5):
                    if self.convertMatrix(i,0) == index:
                        return True
                for i in range(5):
                    if self.convertMatrix(4,i) == index:
                        return True
                for i in range(5):
                    if self.convertMatrix(i,4) == index:
                        return True
        return False
    def convertMatrix(self,columns,rows):
        return columns + rows * 5
    def checkIfValueX(self,btn):
        if btn == "casevide.png":
            return True
        return False
    def checkIfValueO(self,btn):
        if btn == "casevide2.png":
            return True
        return False
    def checkIfValueNothing(self,btn):
        if btn == "case2.png":
            return True
        return False
class Button:
    background_normal = ""
    background_down = ""
    guid = ""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080
    cherrypy.config.update({'server.socket_port': port})
    cherrypy.quickstart(Server())