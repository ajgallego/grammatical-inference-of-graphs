#!/usr/bin/python
# -*- coding: utf-8 -*- 
from __future__ import print_function

"""
A transition in graph's n-grams is composed by: an initial state,
a multiset of subgraphs, and a final state (subgraph).
"""
class GraphNGramTransition:
    def __init__(self, initialVertex, numInitialParents, numInitialChildren, multiset, finalState):
        self.initialVertex = initialVertex
        self.numInitialParents = numInitialParents
        self.numInitialChildren = numInitialChildren
        self.multiset = multiset     
        self.finalState = finalState

    def __ne__(self, t2):
        return not self.__eq__(t2)

    def __eq__(self, t2):
        if self.numInitialParents != t2.numInitialParents or self.numInitialChildren != t2.numInitialChildren:
            return False

        if self.finalState != t2.finalState:
            return False

        multisetSize = len(self.multiset)

        if multisetSize != len(t2.multiset):
            return False

        if multisetSize == 0:
            return True

        used = [False] * multisetSize

        for idx1 in xrange(multisetSize):
            isEqual = False
            subG1 = self.multiset[idx1]
            for idx2 in xrange(multisetSize):
                if used[idx2] == True:
                    continue
                
                subG2 = t2.multiset[idx2]

                if subG1 == subG2:  # SubGraphs comparison (__eq__)
                    isEqual = True
                    used[ idx2 ] = True
                    break

            if isEqual == False:
                return False

        return True


    def __str__(self):
        strMultiset = ""
        for m in self.multiset:
            strMultiset += " \t" + str(m) + "\n"

        return "Transition rule: \n" \
                + "- Initial: "+ str(self.initialVertex) \
                +       " [" + str(self.numInitialParents) \
                +       "/"+  str(self.numInitialChildren) +"]\n" \
                + "- Multiset ("+ str(len(self.multiset)) + "):\n" \
                + strMultiset \
                + "- Final: " + str(self.finalState) + "\n"
