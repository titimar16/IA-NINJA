# utilsQuixo.py
# IA library
# Author: Soffie Quentin - Thibaut Maringer
# Version: February 20, 2019

def startIA(listebtn):
    simplelist = convertToSimpleList(listebtn)
    
    listWeight = getTheBestWeight(simplelist,True,True) # liste de liste de tuple = [[(valueWeight,horizontale,droitebas,cell),...]]
    result = anticipationBlow(listWeight,simplelist)
    return result
    

    
                    

def anticipationBlow(listWeight,simplelist):
    # mode anticipation du tour suivant : on check le poid qu 'on obtient dans le prochain coups
    listWeightTurnTwo = []
    if len(listWeight) > 0:
        for i in range(len(listWeight)):
            for y in range(len(listWeight[i])): # on parcourt toutes les possibilités pour obtenir le meilleur poids a notre tour
                if listWeight[i][y][0] == 1000000000:
                    return listWeight[i][y]
                if listWeight[i][y][0] != -1000000000:
                    myliste = getFutureBlow(listWeight[i][y][1],listWeight[i][y][2],listWeight[i][y][3],simplelist,True)
                    ennemy = getTheBestWeight(myliste,False,False)
                    if ennemy[0] != 1000000000:
                        mynewliste = getFutureBlow(ennemy[1],ennemy[2],ennemy[3],myliste,False)
                        listWeightTurnTwo.append((getTheBestWeight(mynewliste,True,False),listWeight[i][y]))


        if len(listWeightTurnTwo) > 0:
            BestWeight2 = listWeightTurnTwo[0]
        for i in listWeightTurnTwo:
            if BestWeight2[0][0] < i[0][0]:  
                BestWeight2 = i
        
        return BestWeight2[1] # meilleur lancé possible


def getTheBestWeight(simplelist,round,returnlist = False):
    cellReachable = getReachableCells(simplelist,round)
    listWeight = [] # liste de tuple = [(valueWeight,horizontale,droitebas,cell)]
    for i in cellReachable:
        listWeight.append(evaluateAllAction(i,simplelist,round,returnlist))

    if returnlist == True:
        return listWeight

      #mode 1 analyse du jeu
    if len(listWeight) > 0:
        BestWeight = listWeight[0]
        for i in listWeight:
            if BestWeight[0] < i[0]:  
                BestWeight = i
        
        return BestWeight # meilleur lancé possible 
    



def evaluateAllAction(cell,mylist,round,returnlist = False):
    listWeight = [] # list of tuple
    if int(cell) == 0:
        listWeight.append((generateWeightSpell(cell,getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
        listWeight.append((generateWeightSpell(cell,getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
    elif int(cell) == 20:
        listWeight.append((generateWeightSpell(cell,getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
        listWeight.append((generateWeightSpell(cell,getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
    elif int(cell) == 4:      
        listWeight.append((generateWeightSpell(cell,getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))      
        listWeight.append((generateWeightSpell(cell,getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
    elif int(cell) == 24:
        listWeight.append((generateWeightSpell(cell,getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
        listWeight.append((generateWeightSpell(cell,getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
    else: 
        if int(cell) == 5 or int(cell) == 10 or int(cell) == 15:
            listWeight.append((generateWeightSpell(cell,getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
        if int(cell) == 9 or int(cell) == 14 or int(cell) == 19:
            listWeight.append((generateWeightSpell(cell,getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
        if int(cell) == 1 or int(cell) == 2 or int(cell) == 3:
            listWeight.append((generateWeightSpell(cell,getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(False,True,cell,mylist,round),round),False,True,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
        if int(cell) == 21 or int(cell) == 22 or int(cell) == 23:
            listWeight.append((generateWeightSpell(cell,getFutureBlow(True,False,cell,mylist,round),round),True,False,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(False,False,cell,mylist,round),round),False,False,cell))
            listWeight.append((generateWeightSpell(cell,getFutureBlow(True,True,cell,mylist,round),round),True,True,cell))
    if returnlist == True:
        return listWeight

    
    if len(listWeight) > 0:
        BestWeight = listWeight[0]
        for i in listWeight:
            if BestWeight[0] < i[0]: 
                BestWeight = i
        return BestWeight


 

def generateWeightSpell(cell,listebtn,round):
    agressif = 0
    defensif = 0

    if round == True:
        agressif = generateWeightMyself(listebtn)
        defensif  = generateWeightEnnemy(listebtn) 
    else:
        agressif = generateWeightEnnemy(listebtn)
        defensif  = generateWeightMyself(listebtn)
    
    if agressif == 1000000000:
        return agressif # si la possibilité de gagner, on gagne la partie
    if defensif == 1000000000:
        return -1000000000 # si le coups est perdant, on annule le coups
    ratio = agressif - defensif
    return ratio
    
    
    
    

def generateWeightMyself(mylist):
    #Calcul du nombre de rond aligné on possede
    weight = 0
    
    indexes = getMyselfCells(mylist)
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
        if convertMatrix(i,i) in indexes:
            num += 1
    for i in range(num):
        weight += (i + 1)**2 
    if num == 5:
        return 1000000000

    ## Diagonale 4,0 -> 0,4
    
    num = 0
    for i in range(5):
        if convertMatrix(4-i,i) in indexes:
            num += 1
    for i in range(num):
        weight += (i + 1)**2 
    if num == 5:
        return 1000000000
    return weight

def generateWeightEnnemy(mylist):
    #Calcul du nombre de rond aligné on possede
    weight = 0
    
    indexes = getEnemyCells(mylist)
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
        if convertMatrix(i,i) in indexes:
            num += 1
    for i in range(num):
        weight += (i + 1)**2 
    if num == 5:
        return 1000000000

    ## Diagonale 4,0 -> 0,4
    
    num = 0
    for i in range(5):
        if convertMatrix(4-i,i) in indexes:
            num += 1
    for i in range(num):
        weight += (i + 1)**2 
    if num == 5:
        return 1000000000
    return weight

    


def convertToSimpleList(listbtn):
    mines = []
    for i in range(len(listbtn)):
        mines.append(listbtn[i].background_normal)
    return mines

def getFutureBlow(horizontale,droitebas,index,mylist,round):
    mines = [] # list 
    mylist2 = [] # list saveCode
    for i in range(len(mylist)):
        mines.append(mylist[i])
        mylist2.append(mylist[i])
    

    #### Gestion du haut et du bas horizontalement
    if horizontale == True and droitebas == False:
        if int(index) > -1 and int(index) < 5:
            for i in range(int(index)):
                addpictureotherbtn(i+1,i,mylist2,mines)
            Addpicture(mines,0,round)
        elif int(index) > 19 and int(index) < 25:
            for i in range(20,int(index)):
                addpictureotherbtn(i+1,i,mylist2,mines)
            Addpicture(mines,20,round)
    elif horizontale == True and droitebas == True:
        if int(index) > -1 and int(index) < 5:
            for i in range(4,int(index),-1):
                addpictureotherbtn(i-1,i,mylist2,mines)
            Addpicture(mines,4,round)
        elif int(index) > 19 and int(index) < 25:
            for i in range(24,int(index),-1):
                addpictureotherbtn(i-1,i,mylist2,mines)
            Addpicture(mines,24,round)
    #### Gestion du haut et du bas verticalement

    if horizontale == False:
        if int(index) > -1 and int(index) < 5:
            for i in range(int(index) + 20,int(index),-5):
                addpictureotherbtn(i-5,i,mylist2,mines)
            Addpicture(mines,int(index) + 20,round)
        elif int(index) > 19 and int(index) < 25:
            for i in range(int(index)-20 ,int(index) ,5):
                addpictureotherbtn(i+5,i,mylist2,mines)
            Addpicture(mines,int(index) - 20,round)
    ##### Gestion du droite et gauche horizontalement
    if horizontale == True:
        if int(index) == 5 or int(index) == 10 or int(index) == 15:
            for i in range(int(index) + 4,int(index),-1):
                addpictureotherbtn(i-1,i,mylist2,mines)
            Addpicture(mines,int(index)+4,round)
        elif int(index) == 9 or int(index) == 14 or int(index) == 19:
            for i in range(int(index)-4,int(index)):
                addpictureotherbtn(i+1,i,mylist2,mines)
            Addpicture(mines,int(index)-4,round)
    ##### Gestion du droite et gauche verticalement

    if horizontale == False and droitebas == False:
        if int(index) == 5 or int(index) == 10 or int(index) == 15:
            for i in range(0 ,int(index) ,5):
                addpictureotherbtn(i+5,i,mylist2,mines)
            Addpicture(mines,0,round)
        elif int(index) == 9 or int(index) == 14 or int(index) == 19:
            for i in range(4 ,int(index) ,5):
                addpictureotherbtn(i+5,i,mylist2,mines)
            Addpicture(mines,4,round)
    elif horizontale == False and droitebas == True:
        if int(index) == 5 or int(index) == 10 or int(index) == 15:
            for i in range(20,int(index),-5):
                addpictureotherbtn(i-5,i,mylist2,mines)
            Addpicture(mines,20,round)
        elif int(index) == 9 or int(index) == 14 or int(index) == 19:
            for i in range(24,int(index),-5):
                addpictureotherbtn(i-5,i,mylist2,mines)
            Addpicture(mines,24,round)
    return mines

def Addpicture(instance,index,round):
    if round == True:
        instance[index] = "casevide2.png"
    else:
        instance[index] = "casevide.png"

def addpictureotherbtn(index1,index2,savecode,listref):
    listref[index1] = savecode[index2]
    listref[index1] = savecode[index2]
        
def getEnemyCells(listebtn):
    # return list of index Enemy Cells 
    mylist = []
    for i in range(len(listebtn)):
        if checkIfValueX(listebtn[i]) == True:
            mylist.append(i)
    return mylist

def getMyselfCells(listebtn):
    # return list of index Myself Cells 
    mylist = []
    for i in range(len(listebtn)):
        if checkIfValueO(listebtn[i]) == True:
            mylist.append(i)
    return mylist

def getReachableCells(listebtn,round):
    # return list of index Reachable Cells
    mylist = []
    for i in range(len(listebtn)):
        if canLaunchSpell(listebtn[i],i,round) == True:
            mylist.append(i)
    return mylist

def canLaunchSpell(btn,index,round):
    if round == True:
        if checkIfValueO(btn) == True or checkIfValueNothing(btn) == True:
            for i in range(5):
                if convertMatrix(0,i) == index:
                    return True
            for i in range(5):
                if convertMatrix(i,0) == index:
                    return True
            for i in range(5):
                if convertMatrix(4,i) == index:
                    return True
            for i in range(5):
                if convertMatrix(i,4) == index:
                    return True
    if round == False:
        if checkIfValueX(btn) == True or checkIfValueNothing(btn) == True:
            for i in range(5):
                if convertMatrix(0,i) == index:
                    return True
            for i in range(5):
                if convertMatrix(i,0) == index:
                    return True
            for i in range(5):
                if convertMatrix(4,i) == index:
                    return True
            for i in range(5):
                if convertMatrix(i,4) == index:
                    return True
    return False

def convertMatrix(columns,rows):
    return columns + rows * 5



def checkIfValueX(btn):
    if btn == "casevide.png":
        return True
    return False

def checkIfValueO(btn):
    if btn == "casevide2.png":
        return True
    return False

def checkIfValueNothing(btn):
    if btn == "case2.png":
        return True
    return False

