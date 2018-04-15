#!/usr/bin/python
# -*- coding: utf-8 -*- 
from __future__ import print_function
import os, re
import numpy as np
import networkx as nx
import xml.etree.ElementTree as ET


# ----------------------------------------------------------------------------
# Return the list of files in folder
# ext param is optional. For example: 'gxl' or 'gxl|grf'
def list_files(directory, ext=None):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and ( ext==None or re.match('([\w_-]+\.(?:' + ext + '))', f) )]


# ----------------------------------------------------------------------------
def loadGRFfolder(path):
    X = []
    Y = []
    array_of_files = list_files(path, ext='grf')

    for fname in array_of_files:
        G=nx.DiGraph()

        with open(fname) as f:
            lines = f.read().splitlines() 
            if len(lines) == 1:
                continue

            category = lines[0].replace('# ', '')
            
            for idx1, l in enumerate(lines[1:]):
                G.add_node(idx1)                
                
            for idx1, l in enumerate(lines[1:]):
                for idx2, e in enumerate(l):
                    if e == '1':
                        G.add_edge(idx1, idx2)

            G = nx.convert_node_labels_to_integers( G )

            Y.append(category)
            X.append(G)

    return X, Y


# ----------------------------------------------------------------------------
# node_label: attr name to use as nodel labels. Set it to None to not use
# category_regex: contiene una expresión regular a aplicar sobre fname para extraer la categoría
def loadGXLfolder(path, node_label='type', category_regex='image([0-9]+)\_[0-9]+\.gxl'):
    X = []
    Y = []
    array_of_files = list_files(path, ext='gxl')

    compiled_regex = re.compile(category_regex)

    for fname in array_of_files:
        tree = ET.parse(fname)  # load xml from file
        root = tree.getroot()
        graph = root[0]

        # Parse category
        basename = os.path.basename(fname)
        category = compiled_regex.match(basename).group(1)

        # create graph
        G=nx.DiGraph()

        for child in graph.findall('node'):
            nodeId = child.get('id')
            if node_label is None:
                G.add_node(nodeId)
            else:
                aux = '-'  # Search for the node label
                for subNode in child.findall('attr'):
                    if 'name' in subNode.attrib and subNode.attrib['name'] == node_label:
                        aux = subNode[0].text
                G.add_node(nodeId, label=aux)

        for child in graph.findall('edge'):
            G.add_edge(child.get('from'), child.get('to'))

        G = nx.convert_node_labels_to_integers( G )

        Y.append(category)
        X.append(G)
        
    return X, Y

