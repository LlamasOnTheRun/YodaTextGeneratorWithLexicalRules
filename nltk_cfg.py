def cfg_demo():
    """
    A demonstration showing how ``CFGs`` can be created and used.
    """

    from nltk import CFG, Production, nonterminals

    # Create some nonterminals
    S, NP, VP, PP = nonterminals("S, NP, VP, PP")
    N, V, P, Det = nonterminals("N, V, P, Det")
    VP_slash_NP = VP / NP

    print("Some nonterminals:", [S, NP, VP, PP, N, V, P, Det, VP / NP])
    print("    S.symbol() =>", repr(S.symbol()))
    print()

    print(Production(S, [NP]))

    # Create some Grammar Productions
    grammar = CFG.fromstring(
        """
      S -> NP VP
      PP -> P NP
      NP -> Det N | NP PP
      VP -> V NP | VP PP
      Det -> 'a' | 'the'
      N -> 'dog' | 'cat'
      V -> 'chased' | 'sat'
      P -> 'on' | 'in'
    """
    )

    print("A Grammar:", repr(grammar))
    print("    grammar.start()       =>", repr(grammar.start()))
    print("    grammar.productions() =>", end=" ")
    # Use string.replace(...) is to line-wrap the output.
    print(repr(grammar.productions()).replace(",", ",\n" + " " * 25))
    print()

cfg_demo()