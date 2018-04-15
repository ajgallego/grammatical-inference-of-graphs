#!/usr/bin/python
# -*- coding: utf-8 -*- 
from __future__ import print_function
import utilGraph
import networkx as nx
import signal, time
from contextlib import contextmanager


class SubGraph:
    def __init__(self, fromGraph, fromNodeId, k):
        self.maxLevel = -1;
        self.isFinal = False
        self.graph = nx.DiGraph()

        # Extract subGraph...
        visitedNodesIds = []

        # Add first node
        self._copyNode(fromGraph, fromNodeId, visitedNodesIds)
        
        # Add the rest of nodes recursively...
        level = 0
        self.maxLevel = self._copyNodesRecursive(level, fromGraph, fromNodeId, k, visitedNodesIds)
        
        # Copy edges
        self._copyEdges(fromGraph)
        
        self.graph = nx.convert_node_labels_to_integers( self.graph )
        
        
    def _copyNodesRecursive(self, level, fromGraph, fromNodeId, k, visitedNodesIds):
        level += 1
        maxLevel = -1        
        children = fromGraph.successors(fromNodeId)
        
        if len(children) == 0:
            self.isFinal = True
        if level == k:
            return level

        for childId in children:
            if childId not in visitedNodesIds:
                self._copyNode(fromGraph, childId, visitedNodesIds)
                childLevel = self._copyNodesRecursive(level, fromGraph, childId, k, visitedNodesIds)
                maxLevel = max(maxLevel, childLevel)

        return maxLevel


    def _copyNode(self, fromGraph, nodeId, visitedNodesIds):
        visitedNodesIds.append(nodeId)
        label = fromGraph.node[nodeId]['label'] if 'label' in fromGraph.node[nodeId] else '-'
        labelIn = fromGraph.in_degree(nodeId)
        labelOut = fromGraph.out_degree(nodeId)
        return self.graph.add_node(nodeId, label=str(label), In=str(labelIn), Out=str(labelOut))
        
        
    def _copyEdges(self, fromGraph):
        for nodeId in self.graph.nodes_iter():
            children = fromGraph.successors(nodeId)
            for childId in children:
                if childId in self.graph.node:
                    self.graph.add_edge(nodeId, childId)


    def getNodeLabels(self, nId):
        return self.graph.node[nId]['label'], self.graph.node[nId]['In'], self.graph.node[nId]['Out']
    
    
    def length(self):
        return self.maxLevel
    
    
    def isFinal(self):
        return self.isFinal
    
    
    def numNodes(self):
        return self.graph.number_of_nodes()
    
    
    def numEdges(self):
        return self.graph.number_of_edges()
        
        
    def _node_match_function(graph, att1, att2):
        return att1['label']==att2['label'] and att1['In']==att2['In'] and att1['Out']==att2['Out']


    def __ne__(self, g2):        
        return not self.__eq__(g2)


    def __eq__(self, g2):
        if self.isFinal != g2.isFinal or \
           self.maxLevel != g2.maxLevel or \
           self.graph.number_of_nodes() != g2.graph.number_of_nodes() or \
           self.graph.number_of_edges() != g2.graph.number_of_edges() or \
           utilGraph.numInitials(self.graph) != utilGraph.numInitials(g2.graph) or \
           utilGraph.numFinals(self.graph) != utilGraph.numFinals(g2.graph):
            return False

        if nx.faster_could_be_isomorphic(self.graph, g2.graph) == False:
            return False
       
        return nx.is_isomorphic(self.graph, g2.graph, node_match=self._node_match_function)


    def __str__(self):
        return str(self.graph.nodes(data=True)) \
               + "\n" + str(self.graph.adj) \
               + "\nMax level: " + str(self.maxLevel) \
               + "\nIs final: " + str(self.isFinal) + "\n"

  