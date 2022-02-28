#!/usr/bin/python3

#
# Copyright: Pierre.Flener@it.uu.se and his teaching assistants, 2022.
#
# This file is part of course 1DL481 at Uppsala University, Sweden.
#
# Permission is hereby granted only to the registered students of that
# course to use this file, for a homework assignment.
#
# The copyright notice and permission notice above shall be included in
# all copies and extensions of this file, and those are not allowed to
# appear publicly on the internet, both during a course instance and
# forever after.
#

# Team: 9    # fill in your team number
# Authors: Deng Mingwei # fill in your names

# To run this file, you may need to make it executable. On Linux that can be
# done with: chmod +x cruDes

from typing import List, Tuple
import sys

NVAR = 1   #The number of variables

def at_most(k: int, x: List[int]) -> List[List[int]]:
    n = len(x) - 1
    clauses = []

    # TODO: Return 2nk+n-3k-1 clauses that are satisfiable iff at most k
    # of the n variables x[i] are True

    s = [[] for i in range(n+1)]

    #add !x1|s1,1
    global NVAR

    for i in range(1, n):
        s[i].append(0)
        for j in range(1, k+1):
            s[i].append(NVAR)
            NVAR = NVAR + 1

    a = 1

    firstCla = [-x[1], s[1][1]]
    clauses.append(firstCla)


    #add !s1,j where 1 < j <= k
    for j in range(2, k+1):
        clauses.append([-s[1][j]])

    #add third part
    for i in range(2, n):
        clauses.append([-x[i], s[i][1]])
        clauses.append([-s[i-1][1], s[i][1]])
        for j in range(2,k + 1):
            clauses.append([-x[i], -s[i-1][j-1], s[i][j]])
            clauses.append([-s[i-1][j], s[i][j]])
        clauses.append([-x[i], -s[i-1][k]])

    #add last part
    clauses.append([-x[n], -s[n-1][k]])

    #print(clauses)
    assert len(clauses) == 2 * n * k + n - 3 * k - 1
    return clauses

# <=k(x1,...,xn) <--> >=(n-k)(!x1,...,xn)
def at_least(k: int, x: List[int]) -> List[List[int]]:
    n = len(x) - 1
    clauses = []
    for i in range(len(x)):
        x[i] = -x[i]
    clauses = at_most(n-k, x)

    return clauses




def and_imply(x: List[int], b: int) -> List[List[int]]:
    # TODO: Return a set of clauses that encodes (x[0] /\ ... /\  x[n-1]) -> b
    clause = []
   # if b == 1:
        #clause.


    return None


def or_imply(x: List[int], b: int) -> List[List[int]]:
    # TODO: Return a set of clauses that encodes (x[0] \/ ... \/  x[n-1]) -> b
    clause = []
    clauses = []
    if b == 1:
        for i in range(len(x)):
            clause.append(x[i])
        clauses.append(clause)
    elif b == 0:
        for j in x:
            clauses.append(-x[j])
   # print(clauses)
    return clauses


def gen_cnf(d: int, c: int, e: int) -> Tuple[int, List[List[int]]]:
    nvar = 0  # the number of boolean variables (required by DIMACS CNF)
    cnf = []  # a list of clauses

    # TODO: Generate and add clauses to cnf, by calls to at_most, and_imply,
    # and or_imply.  Also set nvar accordingly.
    t = int(d / c)
    global  NVAR

    #variable list: list[i][j][k] means wether the ith diner eat at kth table in jth evening
    varList = [[[] for j in range(e)] for i in range(d)]
    for i in range(d):
        for j in range(e):
            for k in range(t):
                varList[i][j].append(NVAR)
                NVAR = NVAR + 1



    #Constraint 1: every diner can only eat in one table in each evening
    for i in range(d):
        for j in range(e):
            oneTable = []
            oneTable.append(0)
            for k in range(t):
                #find all varibales that tell whether a fixed diner eats at kth table in a fixed evening,
                oneTable.append(varList[i][j][k])
            #he must eat at most one table
            clauses = at_most(1, oneTable)
            for c1 in range(len(clauses)):
                cnf.append(clauses[c1])
            oneTable.remove(0)

            #he must eat at least one table (x1\/x2...\/xn)
            clauses = or_imply(oneTable, 1)
            for c2 in range(len(clauses)):
                cnf.append(clauses[c2])

    #Constraint 2: there are exactly c diners eat at each table in each evening
    for j in range(e):
        for k in range(t):
            cDiners = []
            cDiners.append(0)
            for i in range(d):
                #find all variables that tell whether ith diner eats at a fixed table in a fixed evening
                cDiners.append(varList[i][j][k])
            #the table must serve exactly c people = at_most c /\ at_least_c
            clauses1 = at_most(c, cDiners)
            for c3 in range(len(clauses1)):
                cnf.append(clauses1[c3])
            clauses2 = at_least(c, cDiners)
            for c4 in range(len(clauses2)):
                cnf.append(clauses2[c4])

    #Constraint 3: diner can only eat with people who have not dined yet
    constraint2 = constrint2(varList, d, e, t)
    for i in range(len(constraint2)):
        cnf.append(constraint2[i])
    nvar = NVAR
    return nvar, cnf


def constrint2(varList , d: int, e: int, t: int):

    clauses = []
    #x1 /\ x2 ==> !(x3/\x4) =  !x1\/!x2\/!x3!\/x4
    for i in range(d):
        for j in range(i+1, d):
            for x1 in range(e):
                for y1 in range(t):
                    twoDiner = []
                    twoDiner.append(-varList[i][x1][y1])
                    twoDiner.append(-varList[j][x1][y1])
                    for x2 in range(e):
                        if x1 != x2:
                            for y2 in range(t):
                                    noTogether = []
                                    noTogether.append(twoDiner[0])
                                    noTogether.append(twoDiner[1])
                                    noTogether.append(-varList[i][x2][y2])
                                    noTogether.append(-varList[j][x2][y2])
                                    clause = or_imply(noTogether, 1)
                                    clauses.append(clause[0])

    return clauses



if __name__ == "__main__":


    try:
        d = int(sys.argv[1])
        c = int(sys.argv[2])
        e = int(sys.argv[3])
    except IndexError:
         print('Usage: cruDes d c e')


    nvar, cnf = gen_cnf(d, c, e)

    # Output to stdout in DIMACS CNF format
    with open('in.dimacs', 'w') as f:
        f.write(f'p cnf {nvar} {len(cnf)}')
        f.write('\n')
        for clause in cnf:
            f.write(f'{" ".join([str(var) for var in clause])} 0')
            f.write('\n')
    print("CNF generate successfully")