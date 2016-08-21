#!/usr/bin/python
import os
import sys


help_s = '''
Script used to generate intersection of the input pairs and the existing pairs.

Parameters:
    [1] paths of the vaild pair files
    [2] path of intersection pairs
    [3] path of intersection pairs vocabulary

'''

print ">>>>>>>>>>>>           >>>>>>>>>>>>>>>>>>          >>>>>>>>>>"
print "\n>>>>>>>>>> starting intersection >>>>>>>>>>>\n"
if(len(sys.argv) < 4):
    print help_s
    exit()

pair_paths = sys.argv[1]
    
first_pairs_file = pair_paths[1]
second_pairs_file = pair_paths[2]


host_set = set()
guest_set = set()
intersection_pairs_voc = set()

for i in sys.argv:
	print i+'\n'


with open(eval(sys.argv[1])[0]) as input1:
    for l in input1: host_set.add(l)

for i in eval(sys.argv[1])[1:]:
    with open(i) as input2:
        for ll in input2: guest_set.add(ll)
        host_set.intersection_update(guest_set)
        guest_set = set() # Reinitialization !!!
        
print "Output pairs file: "+sys.argv[2]     
with open(sys.argv[2],'w+') as outp_pair:
    for pairs in host_set: outp_pair.write(pairs)
        
voc = set()        
for pairs in host_set:
    for word in pairs.split(): voc.add(word+"\n")
        
print "Output vocabulary file: "+sys.argv[3]
with open(sys.argv[3],'w+') as outp_voc:
    for w in voc: outp_voc.write(w)
        
print "\n>>>>>>>>>> intersection ended >>>>>>>>>>>\n"
print ">>>>>>>>>>>>           >>>>>>>>>>>>>>>>>>          >>>>>>>>>>"

