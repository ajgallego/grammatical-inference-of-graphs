#!/usr/bin/python
# -*- coding: utf-8 -*- 
from __future__ import print_function
import networkx as nx


def getInitials(graph):
    initials = []
    for nId in graph.nodes_iter():
        if graph.in_degree(nId) == 0:
            initials.append(nId)
    return initials


def getFinals(graph):
    finals = []
    for nId in graph.nodes_iter():
        if graph.out_degree(nId) == 0:
            finals.append(nId)
    return finals


def numInitials(graph):
    initials = 0
    for nId in graph.nodes_iter():
        if graph.in_degree(nId) == 0:
            initials += 1
    return initials


def numFinals(graph):
    finals = 0
    for nId in graph.nodes_iter():
        if graph.out_degree(nId) == 0:
            finals += 1
    return finals
