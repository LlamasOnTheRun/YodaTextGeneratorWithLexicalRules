import nltk

from nltk.tokenize import word_tokenize
from nltk import CFG, Production, nonterminals, Nonterminal
from nltk.parse.generate import generate
from nltk.help import upenn_tagset
from collections import OrderedDict

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


def getPOSOfSentence(sentence):
    print(sentence)
    temp = []
    for word_and_pos in nltk.pos_tag(word_tokenize(sentence)):  # POS -> Part Of Speech
        temp.append(Nonterminal(word_and_pos[1]))

    print("All POS found in sentence: " + temp.__str__())
    return temp


def performRightToLeftProductionCreation(unfoundNonTerminals):
    global rollingID
    global overallProductionsFound
    index = len(unfoundNonTerminals) - 1
    while index > 1:
        rhs = unfoundNonTerminals.__getitem__(index)
        lhs = unfoundNonTerminals.__getitem__(index - 1)
        production = Production(Nonterminal(rollingID.__str__()), [lhs, rhs])
        rollingID = rollingID + 1
        overallProductionsFound.insert(0, production)
        index -= 2
        if index == 0:
            lhs = unfoundNonTerminals.__getitem__(index)
            overallProductionsFound.insert(0, Production(Nonterminal(rollingID.__str__()), [lhs, production.lhs()]))
            rollingID = rollingID + 1

    res = list(OrderedDict.fromkeys(overallProductionsFound))
    print("All initial productions found: " + overallProductionsFound.__str__())


posInSentence = []
startingProduction = Production(Nonterminal("S"), [])
overallProductionsFound = []
rollingID = 0

print()
for sentence in quotes:
    posInSentence = getPOSOfSentence(sentence)
    unfoundProductionsForNonTerminals = posInSentence
    # todo add step here for identifying exsiting productions spotted using inital POS
    performRightToLeftProductionCreation(unfoundProductionsForNonTerminals)

    overallProductionsFound.clear()
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
