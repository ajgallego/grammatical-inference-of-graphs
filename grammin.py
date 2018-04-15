#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import gc
import sys
import random
import argparse
import numpy as np
import networkx as nx
import utilGraph, utilGraphIO, utilGraphNGram
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import StratifiedKFold


# Fix seeds ant print options
random.seed(1337)
np.random.seed(1337)                    # for reproducibility
np.set_printoptions(threshold=np.nan)   # Print full np matrix
sys.setrecursionlimit(40000)


#------------------------------------------------------------------------------
def labels_encoder(labels, encoder=None):
    if encoder == None:
        encoder = LabelEncoder()
        encoder.fit(labels)
    y = encoder.transform(labels).astype(np.int32)
    return y, encoder


# ----------------------------------------------------------------------------
def limit_data_to(X, Y, limit):
    if limit is None:
        return
    classes = np.unique(Y)
    nb_classes = len(classes)
    Xaux = []
    Yaux = []
    for c in range(nb_classes):  # iterate by labels
        index = Y == classes[c]    # samples with that label
        X_class = X[index]
        Y_class = Y[index]

        for idx, item in enumerate(X_class):
            if idx >= limit:
                break
            Xaux.append(item)
            Yaux.append(Y_class[idx])

    Xaux, Yaux = shuffle(Xaux, Yaux, random_state=0)

    return np.asarray(Xaux), np.asarray(Yaux)


# ----------------------------------------------------------------------------
def clean_data(X, Y, remove):
    # Remove empty
    Xaux = []
    Yaux = []
    for idx, graph in enumerate(X):
        if graph.number_of_nodes() > 0:
            Xaux.append(graph)
            Yaux.append(Y[idx])
    del X
    del Y
    gc.collect()
    X = Xaux
    Y = Yaux

    # Solve graphs with many initial nodes...
    if remove == False:
        print('Add dummy node strategy...')
        for idx, graph in enumerate(X):
            initials = utilGraph.getInitials(graph)
            if len(initials) > 1:
                #print(graph.adj)
                #assert((graph.number_of_nodes() in graph.node) == False)
                assert((-1 in graph.node) == False)
                rootId = -1 #graph.number_of_nodes()
                graph.add_node( rootId )
                for initialId in initials:
                    graph.add_edge(rootId, initialId)
                X[idx] = nx.convert_node_labels_to_integers( graph )

            elif len(initials) == 0:
                #print(graph.adj)
                #assert((graph.number_of_nodes() in graph.node) == False)
                assert((-1 in graph.node) == False)
                rootId = -1 #graph.number_of_nodes()
                graph.add_node( rootId )
                graph.add_edge(rootId, 0)
                X[idx] = nx.convert_node_labels_to_integers( graph )
        return np.asarray(X), np.asarray(Y)

    else:
        print('Remove graphs with many initial nodes strategy...')
        auxSize = len(X)
        Xaux = []
        Yaux = []
        for idx, graph in enumerate(X):
            if utilGraph.numInitials(graph) == 1:
                Xaux.append(graph)
                Yaux.append(Y[idx])
        del X
        del Y
        gc.collect()

        print('# Total initial files:', auxSize)
        print('# Total files after clean: ', len(Xaux))
        print('# Num removed files:', str(auxSize - len(Xaux)))
        return np.asarray(Xaux), np.asarray(Yaux)


# ----------------------------------------------------------------------------
def run_test(aut, X_test, Y_test, label, kvalue):
    hits = 0
    for idx, graph in enumerate(X_test):
        if aut.isAcceptedGraph(graph) == True and (Y_test[idx] == label or label == -1):
            hits += 1

    acc = float(hits) * 100.0 / float(len(X_test))
    print("%d\t%d\t%d\t%d\t%d\t%d\t%0.4f" % \
            (label, kvalue, aut.numGraphsLoaded, len(X_test), len(aut.transitionList), hits, acc ) )

    return acc
            

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Grammatical inference of directed acyclic graph languages with polynomial time complexity')
parser.add_argument('-path',    required=True,                  help='Path to the dataset')
parser.add_argument('-ftype',   default='grf',   type=str,      help='Input file type: grf, gxl')
parser.add_argument('-nlabel',  default=None,    type=str,      help='Tag used for node labels / only for gxl files')
    # Mutagenicity: chem
    # GREC: type
    # RNA, Fingreprint and Histograph dont have
parser.add_argument('-db',      default=None,    choices=['grec', 'mutagen', 'aids', 'finger', 'histograph', 'rna', 'nist'],  help='Db name')
parser.add_argument('-c',       default=-1,      type=int,      help='Class to validate. -1 to validate all')
parser.add_argument('-values',  default='2,3,4', type=str,      help='List of k values to iterate')
parser.add_argument('-limit',   default=None,    type=int,      help='Limit samples per class to')
parser.add_argument('-step',    default=100,     type=int,      help='Step size between tests. Use -1 to test only at the end')
parser.add_argument('--remove',            action='store_true', help='Remove graphs with more than one initial node')
args = parser.parse_args()


print('Loading data...')
if args.ftype == 'grf':
    X, Y = utilGraphIO.loadGRFfolder(args.path)
elif args.ftype == 'gxl':
    if args.db == 'grec':
        pattern = 'image([0-9]+)\_[0-9]+\.gxl'   # GREC              Example: image1_01.gxl
    elif args.db == 'mutagen' or args.db == 'aids':
        pattern = '[a-z][0-9]+\_([a-z]+)\.gxl'   # Mutagenicity, AIDS      Example: f0000_mutagen.gxl
    elif args.db == 'finger':
        pattern = '[a-z][0-9]+\_([A-Z]+)\.gxl'   # Fingerprint       Example: 'f0000_AT.gxl'
    elif args.db == 'histograph':
        pattern = '[0-9]+\-([0-9]+)\-[0-9]+\.gxl'  # Histograph      Example: '270-01-01.gxl'
    else:
        patter = 'image\_[0-9]+\_([0-9]+)\.gxl'

    X, Y = utilGraphIO.loadGXLfolder(args.path, node_label=args.nlabel, category_regex=pattern)
else:
    raise Exception('Unknown type')


X, Y = shuffle(X, Y, random_state=0)
Y, e = labels_encoder(Y)
X = np.asarray(X)
Y = np.asarray(Y).astype(np.int)

classes = np.unique(Y)
nb_classes = len(classes)


if args.limit != None:
    print('Limit data...')
    X, Y = limit_data_to(X, Y, args.limit)


print('Cleaning data...')
X, Y = clean_data(X, Y, args.remove)
assert(nb_classes == len(np.unique(Y)))


# Divide train / test sets
for train_index, test_index in StratifiedKFold(Y, n_folds=5):
    break;
X_train, X_test = X[train_index], X[test_index]
Y_train, Y_test = Y[train_index], Y[test_index]

assert(nb_classes == len(np.unique(Y_train)))
assert(nb_classes == len(np.unique(Y_test)))



print('# Processing path:', args.path)
print('# Input file type:', args.ftype)
print('# Tag used for node labels:', args.nlabel)
print('# Total train files:', len(X_train))
print('# Total test files:', len(X_test))
print('# Classes:', classes)
print('# Nb classes:', nb_classes)
print('# Class:', args.c)
print('# K values:', args.values)


arrayValues = args.values.split(',')    # Array of values to iterate

for kvalue in arrayValues:
    kvalue = int(kvalue)
    print('Training...')
    print('# K value:', kvalue)

    aut = utilGraphNGram.GraphNGram(k=kvalue)

    if args.c != -1:    # filter by label? train only on those samples
        index = Y_train == args.c
        X_train_aux = X_train[index]
        print('# Total train files of class:', len(X_train_aux))
    else:
        X_train_aux = X_train
        
    print("label\tk\ttrain\ttest\trules\thits\tacc")

    for idx, graph in enumerate(X_train_aux):
        aut.extractTransitionRules(graph)

        if args.step != -1 and idx % args.step == 0:
            acc = run_test(aut, X_test, Y_test, args.c, kvalue)
            if 100.0 - acc < 0.01:
                break

    if args.step == -1 or idx % args.step != 0:  # Final test...
        acc = run_test(aut, X_test, Y_test, args.c, kvalue)

    del aut
    gc.collect()
    print(20*"-")

