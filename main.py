import csv
from BallotTree import BallotTreeNode
from Candidate import Candidate

#How many winners are we looking for?
seats=3

votes=[]
with open('votes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            person = []
            for i in range(0, len(row)):
                person.append(row[i])
            votes.append(person)
            line_count += 1


#check the number of winning candidates
def checkNumWinning(dict):
    numWins=0
    for key in dict:
        if(dict[key].won):
            numWins+=1
    return numWins

def numVotes(candidate):
    return candidate.votes

#return the smallest two candidates
def getSmallestCandidates(candidateDictionary):
    array=[]
    for candStr in candidateDictionary:
        array.append(candidateDictionary[candStr])
    array.sort(key=numVotes)

    index=0
    returnArray=[0,0]

    for cand in array:
        if not cand.lost:
            returnArray[index]=cand
            index+=1
            if(index>=2):
                break
    return returnArray

candidateDictionary={"root": Candidate("root", root=True)}
for row in votes:
    for candidate in row:
        if not candidate in candidateDictionary:
            candidateDictionary[candidate]=Candidate(candidate)

root=BallotTreeNode("root",candidateDictionary)
for voteRow in votes:
    root.addBallot(["root"]+voteRow)

#this is the number of votes counted
print("I have "+str(root.votesThatPassHere)+" votes")

while(checkNumWinning(candidateDictionary)<seats):
    print("New Iteration: ")

    exhausted=root.votesThatPassHere-root.getNumOkay()

    print("At this iteration, a total of "+str(exhausted)+" votes are exhausted")

    quota=(len(votes)-exhausted)//(seats+1)+1

    print("At this iteration , the votes required to be considered winning is "+str(quota))


    #this is the total number of extra votes among all candidates
    sumSurplus=0

    for candStr in candidateDictionary:
        cand=candidateDictionary[candStr]
        if not cand.lost:
            #if they have surplus votes, then we have to adjust their weight to allow them to give those extra votes to other candidates
            if(cand.votes>quota):
                cand.weight*=quota/cand.votes
                cand.won=True
                sumSurplus+=cand.votes-quota

    #we need the difference in the smallest two candidates to determine when to knock out a candidate
    smallestCandidates=getSmallestCandidates(candidateDictionary)

    print("The smallest candidates are:")
    print(smallestCandidates[0].name+ " "+smallestCandidates[1].name)

    #if the difference is bigger than the surplus, then there is no way that the smallest candidate could win, so we knock him out
    if(smallestCandidates[1].votes-smallestCandidates[0].votes>=sumSurplus):
        smallestCandidates[0].lost=True


    #reset all the votes, we have to recount them every time
    for candStr in candidateDictionary:
        cand=candidateDictionary[candStr]
        cand.votes=0

    #recount all the votes with teh updated weights
    root.updateCandidates(1)

    #print all the votes of all hte candidates
    for cand in candidateDictionary:
        print(cand+" "+str(candidateDictionary[cand].votes))

    print("")
    print("")
for cand in candidateDictionary:
    if(candidateDictionary[cand].won):
        print("WINNER:")
        print(cand+" "+str(candidateDictionary[cand].votes))
