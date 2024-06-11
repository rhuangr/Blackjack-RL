import numpy as np
import random

POSSIBLE_SUM = [12,13,14,15,16,17,18,19,20,21]
DEALER_CARD = [1,2,3,4,5,6,7,8,9,10]
USEABLE_ACE = [0,1]
POSSIBLE_ACTIONS = ["Hit", "Stick"]
ALL_CARDS = [1,2,3,4,5,6,7,8,9,10,10,10,10]
STEP_SIZE = 0.001

#Action-State value table
SAV = np.zeros((len(POSSIBLE_SUM), len(DEALER_CARD), len(USEABLE_ACE), len(POSSIBLE_ACTIONS)))

#Action-State amount of times visited
SAvisits = np.zeros_like(SAV)


def returnIndex(sum, dealerCard):
    return sum - 12, dealerCard - 1


def agentPlays( agentSum, dealerCard, hasUseableAce): #returns whether has received reward 
    action = None

    # a list containing all states visisted during the episode, used for calculating values
    statesList = [] 
    epsilon = 0.1
    while True:

        i,j = returnIndex(agentSum, dealerCard)

        # Inital policy: stick if 20 or 21, else: hit
        if SAvisits[i ,j, hasUseableAce, 0] == 0 and SAvisits[i ,j, hasUseableAce, 1] == 0:
            action = "Stick" if agentSum > 19 else "Hit"
        
        else:
            epsilonCheck = random.random()
            bestAction = SAV[i, j, hasUseableAce, :].argmax()
            if epsilon > epsilonCheck:
                action = POSSIBLE_ACTIONS[1] if bestAction == 0 else POSSIBLE_ACTIONS[0]
            else:
                action = POSSIBLE_ACTIONS[bestAction]
        if action == "Stick":
            statesList.append([i,j,hasUseableAce, 1])
            return agentSum, statesList

        agentSum += drawCard()

        if agentSum > 21: 
            if hasUseableAce == 0:
                statesList.append([i,j,0,0])
                setAllSAInEpisode(statesList, -1)
                return 0, statesList
            else:
                statesList.append([i, j ,1, 0])
                hasUseableAce = 0
                agentSum -= 10
        else:
            if agentSum == 21:
                statesList.append([i, j ,hasUseableAce, 0])
                return 21, statesList #Pass to next function to check dealerSum
            statesList.append([i,j, hasUseableAce, 0])
            
def getDealerSumWithAce(sum):
    sum1 = sum
    sum2 = sum + 10

    if sum2 > 21:
        return sum1, False
    else:
        return sum2, True

def dealerPlays(dealerCard, agentSum, statesList):
    dealerAction = None
    dealerSum = dealerCard
    dealerHasAce = False
    if dealerCard == 1:
        dealerHasAce = True
    while True:
        dealerSum += drawCard()
        if dealerHasAce:
            dealerSum, dealerHasAce = getDealerSumWithAce(dealerSum)
        if dealerSum > 16:
            dealerAction = "Stick"
        else:
            dealerAction = "Hit"

        if dealerAction == "Stick":

            if dealerSum == agentSum:   
                setAllSAInEpisode(statesList, 0)         
                return "Draw"  
            if agentSum > dealerSum or dealerSum > 21:
                setAllSAInEpisode(statesList, 1)
                return "Win"
            else:
                setAllSAInEpisode(statesList, -1)
                return "Loss"
            
def setAllSAInEpisode(statesList, reward):
    for i in range(len(statesList)):
        setSAFunction(statesList[i][0], statesList[i][1],statesList[i][2],statesList[i][3], reward)

def setSAFunction(sumIndex, dealerCardIndex, hasUseableAce, action, reward):

    SAvisits[sumIndex, dealerCardIndex, hasUseableAce, action] += 1
    visits = SAvisits[sumIndex, dealerCardIndex, hasUseableAce, action]
    stateActionValue = SAV[sumIndex, dealerCardIndex, hasUseableAce, action]
    newValue = stateActionValue + (reward - stateActionValue)/visits
    SAV[sumIndex, dealerCardIndex, hasUseableAce, action] = newValue

def drawCard():
    return ALL_CARDS[random.randint(0,len(ALL_CARDS) - 1)]

def findOptimalPolicy(n):
    totalWins = 0
    totalLosses = 0
    totalDraws = 0
    i = 0
    while (i < n):
        agentSum = random.randint(12,21)
        dealerCard = random.randint(1,10)
        hasUseableAce = random.randint(0,1)
        WL = None

        agentSum, statesList = agentPlays(agentSum, dealerCard, hasUseableAce)
        if agentSum != 0:
            WL = dealerPlays(dealerCard, agentSum, statesList)

        i+=1
        if WL == None:
            WL = "Loss"
        
        if WL == "Loss":
            totalLosses += 1
        elif WL == "Win":
            totalWins += 1
        elif WL == "Draw":
            totalDraws += 1
            
    print(f"Wins: {totalWins}, Draws: {totalDraws}, Losses: {totalLosses}")
    print(f"W% : {totalWins/i}, D%: {totalDraws/i}, L%: {totalLosses/i}")

def printAllActionValues():
    for i in range(10):
        # if i == 8:
            for j in range(10):
                for k in range(2):
                    for l in range(2):
                        action = "Hit" if l==0 else "Stick"
                        value = SAV[i,j,k,l]
                        print(f"AgentSum = {i + 12}, dealerCard = {j+1}, hasAce = {k}, action = {action}")
                        print(f"Value : {value}, Visits: {SAvisits[i,j,k,l]}")
                        print()

def printBestActions():
    for i in range(10):
    # if i == 7:
        for j in range(10):
            for k in range(2):
                bestAction = np.argmax(SAV[i,j,k,:])
                action = "Hit" if bestAction==0 else "Stick"
                print(f"AgentSum = {i + 12}, dealerCard = {j+1}, hasAce = {k}, action = {action}")
                print(f"Visits: {SAvisits[i,j,k,bestAction]}, Values: {SAV[i,j,k,bestAction]}")
                print()
   
findOptimalPolicy(5000000)
printBestActions()
# printAllActionValues()


