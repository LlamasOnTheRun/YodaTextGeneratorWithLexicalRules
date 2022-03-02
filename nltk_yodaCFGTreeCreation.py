import nltk

from nltk.tokenize import word_tokenize
from nltk import CFG, Production, nonterminals, Nonterminal
from nltk.parse.generate import generate
from nltk.help import upenn_tagset
from collections import OrderedDict


def getPOSOfSentence(sentence):
    global overallProductionsFound
    print(sentence)
    temp = []
    for word_and_pos in nltk.pos_tag(word_tokenize(sentence)):  # POS -> Part Of Speech
        temp.append(Nonterminal(word_and_pos[1]))
        overallProductionsFound.append(Production(Nonterminal(word_and_pos[1]), [word_and_pos[0]]))

    print("All POS found in sentence: " + temp.__str__())
    return temp

def determineIfNewStartingProductionIsFound(mutatedNonTerminals):
    print("Here are the nonterminals found after mutation")
    print(mutatedNonTerminals)
    isThereANewStart = False

    if len(mutatedNonTerminals) > 1:
        for mutatedNonTerminal in mutatedNonTerminals:
            for startingNonTerminal in overallStartingNonTerminals:
                if mutatedNonTerminal == startingNonTerminal:
                    isThereANewStart = True

    return isThereANewStart

def mutateListWithAlreadyDeclaredProductions(initalNonTerminals):
    global overallProductionsFound
    global overallStartingNonTerminals

    print("-------Starting mutation procedure-------")
    foundExistingProduction = False

    if overallProductionsFound.__len__() != 0:  # [0, 2, 1] index = -1
        index = len(initalNonTerminals) - 1
        print("Starting index: " + index.__str__())
        while index > 0:
            lhs = initalNonTerminals.__getitem__(index - 1)
            rhs = initalNonTerminals.__getitem__(index)

            for production in overallProductionsFound:
                if production.rhs().__eq__((lhs, rhs)):
                    print("Found a match for production!!!!")
                    print("Index we are on: " + index.__str__())
                    print("What we are finding from sentence: " + (lhs, rhs).__str__())
                    print("Existing Production we are checking: " + production.__str__())
                    print("Before mutation: " + initalNonTerminals.__str__())
                    initalNonTerminals.pop(index)
                    initalNonTerminals.pop(index - 1)
                    initalNonTerminals.insert(index-1, production.lhs())
                    foundExistingProduction = True
                    print("After mutation: " + initalNonTerminals.__str__())
                    break
            index -= 2
            if index == 0:
                lhs = initalNonTerminals.__getitem__(index)
                rhs = initalNonTerminals.__getitem__(index+1)
                for production in overallProductionsFound:
                    if production.rhs().__eq__((lhs, rhs)):
                        print("Found a match for production!!!!")
                        print("Index we are on: " + index.__str__())
                        print("What we are finding from sentence: " + (lhs, rhs).__str__())
                        print("Existing Production we are checking: " + production.__str__())
                        print("Before mutation: " + initalNonTerminals.__str__())
                        initalNonTerminals.pop(0)
                        initalNonTerminals.pop(0)
                        initalNonTerminals.insert(0, production.lhs())
                        foundExistingProduction = True
                        print("After mutation: " + initalNonTerminals.__str__())
                        break

    if (foundExistingProduction == True):
        mutateListWithAlreadyDeclaredProductions(initalNonTerminals)

    return initalNonTerminals

def performRightToLeftProductionCreation(unfoundNonTerminals):
    global rollingID
    global overallProductionsFound
    global overallStartingNonTerminals

    index = len(unfoundNonTerminals) - 1
    newNonTerminals = []
    print("-------Starting Left to Right procedure-------")
    print("Displaying unfound nonterminals. On index " + index.__str__() + ": " + unfoundNonTerminals.__str__())
    print("Displaying newly created nonterminals: " + newNonTerminals.__str__())
    while index > 0:
        lhs = unfoundNonTerminals.__getitem__(index - 1)
        rhs = unfoundNonTerminals.__getitem__(index)
        production = Production(Nonterminal(rollingID.__str__()), [lhs, rhs])
        rollingID = rollingID + 1

        overallProductionsFound.insert(0, production)

        unfoundNonTerminals.pop(index)
        unfoundNonTerminals.pop(index-1)
        newNonTerminals.insert(0, production.lhs())

        print("Displaying unfound nonterminals. On index " + index.__str__() + ": " + unfoundNonTerminals.__str__())
        print("Displaying newly created nonterminals: " + newNonTerminals.__str__())
        index -= 2
        if index == 0:
            lhs = unfoundNonTerminals.__getitem__(index)
            production = Production(Nonterminal(rollingID.__str__()), [lhs, production.lhs()])
            overallProductionsFound.insert(0, production)
            unfoundNonTerminals.pop(index)

            newNonTerminals.pop(index)
            newNonTerminals.insert(0, production.lhs())
            rollingID = rollingID + 1
            print("Displaying unfound nonterminals. On index " + index.__str__() + ": " + unfoundNonTerminals.__str__())
            print("Displaying newly created nonterminals: " + newNonTerminals.__str__())

    print("Displaying newly created nonterminals: " + newNonTerminals.__str__() + "\n")
    if newNonTerminals.__len__() > 1: # means I havent found an S canidate
        performRightToLeftProductionCreation(newNonTerminals)
    elif newNonTerminals.__len__() != 0:
        overallStartingNonTerminals.append(newNonTerminals.pop()) # todo make it return "S" on "overallProductionsFound" instead of number
        print("Our new starting nonterminals")
        print(overallStartingNonTerminals)

quotes = [
    "No different I.",
    "Yes, No different I.",
    "Agree with you, the council does.",
    "Your apprentice, Skywalker will be.",
    "Always two there are, no more, no less: a master and an apprentice.",
    "Fear is the path to the Dark Side.",
    "Fear leads to anger, anger leads to hate; hate leads to suffering.",
    "I sense much fear in you.",
    "Qui-Gon's defiance I sense in you.",
    "Truly wonderful the mind of a child is.",
    "Around the survivors a perimeter create.",
    "Lost a planet Master Obi-Wan has.",
    "How embarrassing...How embarrassing.",
    "Victory, you say?",
    "Master Obi-Wan, not victory.",
    "The shroud of the Dark Side has fallen.",
    "Begun the Clone War has.",
    "Much to learn you still have... my old padawan... this is just the beginning!",
    "Twisted by the Dark Side young Skywalker has become.",
    "The boy you trained, gone he is, consumed by Darth Vader.",
    "The fear of loss is a path to the Dark Side.",
    "If into the security recordings you go, only pain will you find.",
    "Not if anything to say about it I have.",
    "Great warrior, hmm?",
    "Wars not make one great.",
    "Do or do not; there is no try.",
    "Size matters not.",
    "Look at me.",
    "Judge me by my size, do you?",
    "That is why you fail.",
    "No!",
    "No similar.",
    "You must unlearn what you have learned.",
    "Only different in your mind.",
    "Always in motion the future is.",
    "Reckless he is.",
    "Matters are worse.",
    "When nine hundred years old you reach, look as good, you will not.",
    "No.",
    "There is... another... Sky... walker..."
]

posInSentence = []
overallStartingNonTerminals = []
overallProductionsFound = []
rollingID = 0

print()
for sentence in quotes:
    posInSentence = getPOSOfSentence(sentence)
    unfoundProductionsForNonTerminals = mutateListWithAlreadyDeclaredProductions(posInSentence)
    # newStartDetected = determineIfNewStartingProductionIsFound(unfoundProductionsForNonTerminals)
    performRightToLeftProductionCreation(unfoundProductionsForNonTerminals)

    posInSentence.clear()
    print()
    print("Overall productions found thus far: " + overallProductionsFound.__str__())

print("We made our tree, lets see if this is in chomsky normal form")

for production in overallProductionsFound:
    for startingNonTerminal in overallStartingNonTerminals:
        if(production.lhs() == startingNonTerminal):
            overallProductionsFound.append(Production(Nonterminal("S"), production.rhs()))
            overallProductionsFound.remove(production)

print("New productions found after adding S: " + overallProductionsFound.__str__())

overallProductionsFound.append(Production(Nonterminal("S"), production.rhs()))
customCFG = CFG(Nonterminal("S"), overallProductionsFound)

print("Is this in chomsky normal form: ")
print(customCFG.is_chomsky_normal_form())
print("That is what we like to see")
#That is why you fail.

sent = ['No', 'different', 'I', '.']
parser = nltk.ChartParser(customCFG)
trees = list(parser.parse(sent))
print(trees.__str__())

for sentence in quotes:
    sent = word_tokenize(sentence)
    parser = nltk.ChartParser(customCFG)
    trees = list(parser.parse(sent))
    print(trees[0])

#[4, 11, 17, 31, 39, 52, 57, 61, 65, 69, 73, 77, 80, 84, 90, 91, 104, 108, 119, 123, 133, 139, 142, 147, 154, 157, 158, 163, 166, 167, 168, 173, 177, 180, 181, 184, 196, 202]
#[2, 4, 11, 17, 31, 39, 52, 57, 61, 65, 69, 73, 77, 80, 84, 90, 91, 104, 108, 119, 123, 133, 139, 142, 147, 154, 157, 158, 163, 166, 167, 168, 173, 177, 180, 181, 184, 196, 202]