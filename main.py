import csv
from BallotTree import BallotTreeNode
from Candidate import Candidate
votes=[]
seats=3
exhausted=0
with open('votes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            person = [row[2], row[3], row[4], row[5], row[6]]
            votes.append(person)
            line_count += 1

def checkNumWinning(dict):
    numWins=0
    for key in dict:
        if(dict[key].won):
            numWins+=1
    return numWins


candidateDictionary={
    "root": Candidate("root", root=True),
    "Lucynda Amo" : Candidate("Lucynda Amo"),
    "Alessandro Maioli": Candidate("Alessandro Maioli"),
    "Auguste Pfeiffer": Candidate("Auguste Pfeiffer"),
    "Carson Giles" : Candidate("Carson Giles"),
    "Daniel Lin" : Candidate("Daniel Lin"),
    "Eli Wasserman" : Candidate("Eli Wasserman"),
    "Jackson McCarthy" : Candidate("Jackson McCarthy"),
    "Janki Raythattha" : Candidate("Janki Raythattha"),
    "Julia Brown" : Candidate("Julia Brown"),
    "Khadeeja Qureshi" : Candidate("Khadeeja Qureshi"),
    "Kira Sehgal" : Candidate("Kira Sehgal"),
    "Liam Massey" : Candidate("Liam Massey"),
    "Roei Zakut" : Candidate("Roei Zakut"),
    "Sam Bezilla" : Candidate("Sam Bezilla"),
    "Sam Harshbarger" : Candidate("Sam Harshbarger"),
    "Saumya Malik" : Candidate("Saumya Malik"),
    "Stosh Omiecinski" : Candidate("Stosh Omiecinski"),
    "Talia Fiester" : Candidate("Talia Fiester")
}

root=BallotTreeNode("root",candidateDictionary)
for voteRow in votes:
    root.addBallot(["root"]+voteRow)

print(root.votesThatPassHere)


seats=3


while(checkNumWinning(candidateDictionary)<seats):

    exhausted=root.votesThatPassHere-root.getNumOkay()
    print(exhausted)

    quota=(len(votes)-exhausted)//(seats+1)+1
    print(quota)

    sumSurplus=0

    #smallest, second smallest
    for candStr in candidateDictionary :
        if(not candidateDictionary[candStr].lost):
            smallestCandidates=[candidateDictionary[candStr], candidateDictionary[candStr]]
            break

    for candStr in candidateDictionary:
        cand=candidateDictionary[candStr]
        if not cand.lost:
            if(cand.votes>quota):
                cand.weight*=quota/cand.votes
                cand.won=True
                sumSurplus+=cand.votes-quota
            if(cand.votes<smallestCandidates[0].votes):
                smallestCandidates[0]=cand
            elif(cand.votes<smallestCandidates[1].votes):
                smallestCandidates[1]=cand

    print(smallestCandidates[0].name+ " "+smallestCandidates[1].name)

    if(smallestCandidates[1].votes-smallestCandidates[0].votes>=sumSurplus):
        smallestCandidates[0].lost=True

    for candStr in candidateDictionary:
        cand=candidateDictionary[candStr]
        cand.votes=0

    root.updateCandidates(1)

    for cand in candidateDictionary:
        print(cand+" "+str(candidateDictionary[cand].votes))
for cand in candidateDictionary:
    if(candidateDictionary[cand].won):
        print("WINNER:")
        print(cand+" "+str(candidateDictionary[cand].votes))
