#!/usr/bin/python
# -*- coding: utf-8 -*- 
from __future__ import print_function
import utilGraph, utilSubGraph, utilGraphNGramTransition


class GraphNGram:
    def __init__(self, k):
        assert(k>=2)
        self.numGraphsLoaded = 0
        self.k = k
        self.transitionList = []


    def _extractTransitionRules_recursive(self, graph, fromNodeId, visitedNodesIds): 
        visitedNodesIds.append(fromNodeId)
        
        children = graph.successors(fromNodeId)
        multiset = []

        # Create multiset of this transition
        for childId in children:
            if childId not in visitedNodesIds:
                subgraph = self._extractTransitionRules_recursive( graph, childId, visitedNodesIds )
            else:
                subgraph = utilSubGraph.SubGraph(graph, childId, self.k - 1)
            
            if subgraph is None:
                continue
            
            multiset.append( subgraph )

        # Calculate the final subGraph
        finalSubgraph = utilSubGraph.SubGraph( graph, fromNodeId, self.k - 1 )

        # Create the new transition
        numInitialParents = graph.in_degree(fromNodeId)
        t = utilGraphNGramTransition.GraphNGramTransition(fromNodeId, 
                                                          numInitialParents,
                                                          len(children), 
                                                          multiset, 
                                                          finalSubgraph)
        if t not in self.transitionList:
            self.transitionList.append(t)

        return finalSubgraph


    def extractTransitionRules(self, graph):
        initials = utilGraph.getInitials(graph)
        assert( len(initials) == 1 )

        visitedNodesIds = []

        self._extractTransitionRules_recursive(graph, initials[0], visitedNodesIds)        

        self.numGraphsLoaded += 1


    def isAcceptedGraph(self, graph):
        if utilGraph.numInitials(graph) == 0:
            return False

        newAutomaton = GraphNGram(self.k)
        newAutomaton.extractTransitionRules(graph)

        for t in newAutomaton.transitionList:
            if t not in self.transitionList:
                return False
            
        return True


    def __str__(self):
        strTransitions = ""
        for t in self.transitionList: 
            strTransitions += "-----\n" + str(t) + "\n"

        return "K value: " + str(self.k) \
             + "\nNum graphs loaded: " + str(self.numGraphsLoaded) \
             + "\nNum transition rules: " + str(len(self.transitionList)) \
             + "\nList of transitions: \n" + strTransitions + "\n"

