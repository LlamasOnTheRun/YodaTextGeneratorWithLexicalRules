import nltk

from nltk.tokenize import word_tokenize
from nltk import CFG, Production, nonterminals, Nonterminal
from nltk.parse.generate import generate
from nltk.help import upenn_tagset
from collections import OrderedDict


def getPOSOfSentence(sentence):
    print(sentence)
    temp = []
    for word_and_pos in nltk.pos_tag(word_tokenize(sentence)):  # POS -> Part Of Speech
        temp.append(Nonterminal(word_and_pos[1]))

    print("All POS found in sentence: " + temp.__str__())
    return temp


def mutateListWithAlreadyDeclaredProductions(initalNonTerminals):
    global overallProductionsFound
    global overallStartingNonTerminals

    print("-------Starting mutation procedure-------")

    if overallProductionsFound.__len__() != 0:
        index = len(initalNonTerminals) - 1
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
                    index = len(initalNonTerminals)
                    print("After mutation: " + initalNonTerminals.__str__())
            index = index - 1

    # for startingNonTerminal in overallStartingNonTerminals: # A -> generator -> B then i need B -> parser -> A
    #     for foundNonTerminal in initalNonTerminals: # todo this was my orginal way to find S, but i plan on moving this to a seperate method later on
    #         if startingNonTerminal.__eq__(foundNonTerminal):
    #             print("Found a match for starting production "+foundNonTerminal.__str__()+"!!!!")
    #             if initalNonTerminals.__len__() == 1:
    #                 print("We matched up with a expected starting non-terminal. Look for Production " + initalNonTerminals.__str__())
    #                 initalNonTerminals.remove(foundNonTerminal)
    #             else:
    #                 print("We found a new starting symbol. Look for Production " + initalNonTerminals.__str__())

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
        print(overallStartingNonTerminals)

quotes = [
    "Yes, No different I.",
    "No different I.",
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
    # todo add method here to check if an S was found and unfoundProductionsForNonTerminals == length of 1. If a S was found and unfoundProductionsForNonTerminals != length of 1, there is a new S
    performRightToLeftProductionCreation(unfoundProductionsForNonTerminals)
    posInSentence.clear()
    print()
    print("Overall productions found thus far: " + overallProductionsFound.__str__())