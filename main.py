# -*- coding:utf-8 -*-
import argparse
import csv

def createParser ():
    parser = argparse.ArgumentParser(description='Process some value\'s')
    parser.add_argument('-j', '--j' , help = 'journals',dest='journal')
    parser.add_argument ('-mr', '--mr', help='most request',dest='mr')
    return parser

def mostrequest(journal,mr):
    with open(journal, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        k = []
        for row in reader:
            val = row['input_byte']
            k.append(val)
        j = set(k)
        res = sorted(j,reverse=True)
        print(res)
        
        


if __name__ == "__main__":
    parser = createParser()
    data = parser.parse_args()
    print(data.journal)
    mostrequest(data.journal, data.mr)