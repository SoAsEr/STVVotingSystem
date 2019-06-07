class BallotTreeNode:
    def __init__(self, candidateString, candidateDictionary):
        self.votesThatPassHere = 0
        self.candidateString=candidateString
        self.candidateDictionary=candidateDictionary
        self.children={}

    def addBallot(self, remainingBallot):
        self.votesThatPassHere+=1

        #we've gone the ballot as deep as it can go
        if(len(remainingBallot)==0):
            return

        #we check whether we've already had a ballot like this
        if(remainingBallot[0] in self.children):
            #if so, we just recursively add a ballot without our current level
            self.children[remainingBallot[0]].addBallot(remainingBallot[1:])
        else:
            #if not, we first have to add this possible child to our children
            self.children.update({remainingBallot[0] : BallotTreeNode(remainingBallot[0], self.candidateDictionary)})
            #then continue adding
            self.children[remainingBallot[0]].addBallot(remainingBallot[1:])

    def updateCandidates(self, remainder):
        #iterate over all the children
        for candidateStr in self.children:
            #this gets copied over every iteration
            tempRemainder=remainder

            #if the candidate that we're iterating over isn't lost
            if(not self.candidateDictionary[candidateStr].lost):
                #then we add to their votes
                self.candidateDictionary[candidateStr].votes+= tempRemainder * self.candidateDictionary[candidateStr].weight * self.children[candidateStr].votesThatPassHere
                #we have to update the remaining value of the ballot going this way
                tempRemainder*=1-self.candidateDictionary[candidateStr].weight

            #we check whether we're done with this ballot: either this child has no children and the remainder of the ballot is therefore exhausted or the remaining value of this ballot is 0
            if(len(self.children[candidateStr].children)>0 and tempRemainder>0):
                #we continue deeper only if we're not done
                self.children[candidateStr].updateCandidates(tempRemainder)

    def getNumOkay(self):
        #recursibe depth first search on the number of ballots not exhausted (easier than the other way around)
        if(self.candidateDictionary[self.candidateString].lost):
            sum=0
            for child in self.children:
                sum+=self.children[child].getNumOkay()
            return sum
        else:
            return self.votesThatPassHere
