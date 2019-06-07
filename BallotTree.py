class BallotTreeNode:
    def __init__(self, candidateString, candidateDictionary):
        self.votesThatPassHere = 0
        self.candidateString=candidateString
        self.candidateDictionary=candidateDictionary
        self.children={}

    def addBallot(self, remainingBallot):
        self.votesThatPassHere+=1
        if(len(remainingBallot)==0):
            return
        if(remainingBallot[0] in self.children):
            self.children[remainingBallot[0]].addBallot(remainingBallot[1:])
        else:
            self.children.update({remainingBallot[0] : BallotTreeNode(remainingBallot[0], self.candidateDictionary)})
            self.children[remainingBallot[0]].addBallot(remainingBallot[1:])

    def getVoteValue():
        voteValue=self.votesThatPassHere
        for child in self.children:
            voteValue+=(1-self.candidateDictionary[child].weight)*child.getVoteValue()
        voteValue*=self.candidateDictionary[self.candidateString].weight

    def updateCandidates(self, remainder):
        for candidateStr in self.children:
            #this gets copied over every iteration
            tempRemainder=remainder
            if(not self.candidateDictionary[candidateStr].lost):
                self.candidateDictionary[candidateStr].votes+= tempRemainder * self.candidateDictionary[candidateStr].weight * self.children[candidateStr].votesThatPassHere
                tempRemainder*=1-self.candidateDictionary[candidateStr].weight
            if(len(self.children[candidateStr].children)>0 and tempRemainder>0):
                self.children[candidateStr].updateCandidates(tempRemainder)

    def getNumOkay(self):
        if(self.candidateDictionary[self.candidateString].lost):
            sum=0
            for child in self.children:
                sum+=self.children[child].getNumOkay()
            return sum
        else:
            return self.votesThatPassHere
