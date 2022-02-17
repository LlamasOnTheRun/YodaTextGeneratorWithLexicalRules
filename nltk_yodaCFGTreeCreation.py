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


def mutateListWithAlreadyDeclaredNonTerminals(initalNonTerminals):
    global overallProductionsFound
    global startingProduction
    unfoundNonTerminsals = []

    if overallProductionsFound.__len__() != 0:
        index = len(initalNonTerminals) - 1
        while index > 0:
            lhs = initalNonTerminals.__getitem__(index - 1)
            rhs = initalNonTerminals.__getitem__(index)
            print("What we are finding: " + (lhs, rhs).__str__())

            for production in overallProductionsFound:
                print("Production we are checking: " + production.lhs().__str__() + " -> " + production.rhs().__str__())
                if production.rhs().__eq__((lhs, rhs)):
                    print("Found a match!!!!")
            index = 0

    return initalNonTerminals

def performRightToLeftProductionCreation(unfoundNonTerminals):
    global rollingID
    global overallProductionsFound
    global startingProduction
    index = len(unfoundNonTerminals) - 1
    newNonTerminals = []
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


    print("Overall productions found thus far: " + overallProductionsFound.__str__())
    print("Displaying newly created nonterminals: " + newNonTerminals.__str__() + "\n")
    if newNonTerminals.__len__() > 1: # means I havent found an S canidate
        performRightToLeftProductionCreation(newNonTerminals)
    else:
        startingProduction.append(newNonTerminals.pop())
        print(startingProduction)

quotes = [
    "Agree with you, the council does. Your apprentice, Skywalker will be.",
    "Always two there are, no more, no less: a master and an apprentice.",
    "Fear is the path to the Dark Side. Fear leads to anger, anger leads to hate; hate leads to suffering. I sense much fear in you.",
    "Qui-Gon's defiance I sense in you.",
    "Truly wonderful the mind of a child is.",
    "Around the survivors a perimeter create.",
    "Lost a planet Master Obi-Wan has. How embarrassing. how embarrassing.",
    "Victory, you say? Master Obi-Wan, not victory. The shroud of the Dark Side has fallen. Begun the Clone War has.",
    "Much to learn you still have...my old padawan... This is just the beginning!",
    "Twisted by the Dark Side young Skywalker has become.",
    "The boy you trained, gone he is, consumed by Darth Vader.",
    "The fear of loss is a path to the Dark Side.",
    "If into the security recordings you go, only pain will you find.",
    "Not if anything to say about it I have.",
    "Great warrior, hmm? Wars not make one great.",
    "Do or do not; there is no try.",
    "Size matters not. Look at me. Judge me by my size, do you?",
    "That is why you fail.",
    "No! No different. Only different in your mind. You must unlearn what you have learned.",
    "Always in motion the future is.",
    "Reckless he is. Matters are worse.",
    "When nine hundred years old you reach, look as good, you will not.",
    "No. There is... another... Sky... walker..."
]
posInSentence = []
startingProduction = []
overallProductionsFound = []
rollingID = 0

print()
for sentence in quotes:
    posInSentence = getPOSOfSentence(sentence)
    #unfoundProductionsForNonTerminals = posInSentence
    unfoundProductionsForNonTerminals = mutateListWithAlreadyDeclaredNonTerminals(posInSentence)
    # todo add step here for identifying exsiting productions spotted using inital POS
    performRightToLeftProductionCreation(unfoundProductionsForNonTerminals)

    #overallProductionsFound.clear()
    posInSentence.clear()
    print()

# grammar = CFG.fromstring("""
# S -> RTO SHR
# RTO -> DIR SUM
# DIR -> vb in
# SUM -> dt MWSO
# MWSO -> nnp nnp
# SHR -> DSO GDA
# DSO -> jj nnp
# GDA -> vbz vbn
# vb -> 'twisted'
# in -> 'by'
# dt -> 'the'
# nnp -> 'dark' | 'side' | 'skywalker'
# jj -> 'young'
# vbz -> 'has'
# vbn -> 'become'
# """)
#
# print("A Grammar:", repr(grammar))
# print("    grammar.start()       =>", repr(grammar.start()))
# print("    grammar.productions() =>", end=" ")
# # Use string.replace(...) is to line-wrap the output.
# print(repr(grammar.productions()).replace(",", ",\n" + " " * 25))
# print()
#
# print(list(generate(grammar)))
#
# #nltk.parse_cfg("Twisted by the Dark Side young Skywalker has become")
