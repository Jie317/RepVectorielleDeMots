#! /usr/bin/python
import os
import time
import sys
import glob
import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from tools.neural_network import start_training_kfCV,write_matrix_to_file



help_s = '''

A script to aggregate the models to perform the word similarity task. The weight matrices are trained by a single neuron model or a 3-layer neural network model. The results is given by mean squared error, which are stored in the global result csv file besides the folder "details".

Inputs:

	[1]* sample data path (pairs and their human-evaluated similarities)
	put 0 if using the default test data: "../input_sim_benchmarks/wordsim_combined.tab" 
	
	[2] directory where all the models locate (where the folders "tscca phca ..." locate) 
	put 0 if using the default directory: "../schnabel_embeddings/"
	
	[3] use or not the existing sample matrix generated by previous launching
	put 0 not to use
	put the directory of the file "sample.mat" to apply existing sample matrix
	
	[4] prefix of the result file name

	[5] iteration number during the training
	put 0 to apply the default value: 2000

	[6] learning rate during the training
	put 0 to apply the default value: 0.02

	[7] dimensions in the hidden layer
	put 0 to apply the default value: 3
	if setted to 1, the model will degrade to single neuron from 3-layer neural network

	
	* for the sample data file, the template is fixed as: the first line is the header line and from second line the first three strings must be word_1, word_2, and human mean rating(range of 10). It doesn't matter if each line contains more than 3 strings. The delimiter can only be space or table.

Version 0.1 by Jie He @LGI2P, EMA

'''

def get_sample_matrix(results_dir, prefix_dir, sample_data_path, embeddings_dir, rescaling_1abel=0.1): # return new output directory
	print '\n\nStep 1: Getting sample matrix >>>>>>'
	print '\n\nCreating new output directory >>>>>>'
	timestr = time.strftime("%d%H%M%S_") 
	timestamped_output_dir = results_dir+prefix_dir+timestr+"/"
	detail_dir = timestamped_output_dir+'details/'
	os.makedirs(timestamped_output_dir)
	os.makedirs(detail_dir)
	print 'New output directory:',timestamped_output_dir

	print '\n\nRetrieving model names >>>>>>'
	mns = []
	model_dirs = glob.glob('%s*/' % embeddings_dir)
	for n in model_dirs: mns.append(n.replace(embeddings_dir,'')[:-1])
	print 'Model names:', mns

	print '\n\nReading original pairs >>>>>>'
	pairs_sims = {}
	pairs = []
	with open(sample_data_path) as inP:
		inP.readline() # remove the header line
		for l in inP: 
			l = l.lower()
			p = l.split()[0]+' '+l.split()[1]
			pairs_sims[p] = float(l.split()[2])
			pairs.append(p.split())
	print 'Original pairs size: ', len(pairs)

	print '\n\nFinding common pairs >>>>>>'
	cpairs_set = set()
	cpairs = []
	model_vocs_paths = glob.glob('%s*/*.voc' % embeddings_dir)
	for n in mns:
		pairs_tem = []
		ws = []
		voc_p = '%s%s/%s_size_50.embeddings.voc' % (embeddings_dir, n, n)
		with open(voc_p) as voc: 
			for l in voc: ws.append(l.strip())
		for pair in pairs: 
			if (pair[0] in ws and pair[1] in ws): pairs_tem.append(pair[0]+' '+pair[1])
			else: print 'Pair not found: ', pair, ' in model: ', n
		if len(cpairs_set) == 0: cpairs_set = set(pairs_tem)
		else: cpairs_set.intersection_update(pairs_tem)
	for p in cpairs_set: cpairs.append(p.split())
	write_matrix_to_file(detail_dir+'common.pair', cpairs, paraSpace=0)
	print 'Common pairs size:', len(cpairs)

	print '\n\nExtracting vectors >>>>>>'
	paths = []
	cps_voc = set()
	for p in cpairs: 
		for w in p: cps_voc.add(w)
	for n in mns:
		print 'Extracting model: ', n
		output_path = '%s%s_extracted.vec' % (detail_dir, n)
		paths.append(output_path)
		with open('%s%s/%s_size_50.embeddings.vec' % (embeddings_dir, n, n)) as vf, open(output_path, 'w+') as out:
			for vec in vf: 
				if vec.split()[0] in cps_voc: out.write(vec)
	print 'Extracted vectors: vocabulary size:%d' % len(cps_voc)
	
	print '\n\nCalculating similarities >>>>>>'
	sample_matrix = [[0.]*(len(mns)+1) for i in range(len(cpairs))]
	for j,m in enumerate(mns): 
		fp = '%s%s_extracted.vec' % (detail_dir, m)
		with open(fp) as inm:
			vec_m = {}
			for l in inm: vec_m[l.split()[0]] = [float(i) for i in l.split()[1:]]
			print '%s, size: %d' % (fp, len(vec_m))
			for i,cp in enumerate(cpairs):
				v_word_a = vec_m[cp[0]]
				v_word_b = vec_m[cp[1]]
				sim = cosine_similarity(v_word_a, v_word_b)
				sample_matrix[i][j] = sim
	for i,cp in enumerate(cpairs): # write the human-measured sim scores
		sample_matrix[i][len(mns)] = rescaling_1abel*pairs_sims[cp[0]+' '+cp[1]]
	print 'Calculated sims:\nSample matrix size: ', len(sample_matrix)
	write_matrix_to_file(timestamped_output_dir+'sample.mat', mns, mode='w+', paraSpace = 0, dimension=1, oneLine=True)
	write_matrix_to_file(timestamped_output_dir+'sample.mat', sample_matrix, mode='a+', paraSpace = -1)
	return timestamped_output_dir

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    den = math.sqrt(sumxx*sumyy)
    if(den == 0): return 0
    return sumxy/den			
				
def end_mark(dirName):
	timestr = time.strftime("%d%H%M%S") 
	os.rename(dirName, dirName[:-1]+timestr+'_complete/')


def main(args): 
	if(len(args) < 8):
		print help_s
		exit()

	sample_data_path = '../input_sim_benchmarks/wordsim_combined.tab'	
	embeddings_dir = '../schnabel_embeddings/'	
	results_dir = '../results/'
	skip = False 
	mode = 'w+'
	it = 2000
	alpha = 0.02
	hidden_dim = 3

	if args[1] != '0': sample_data_path = args[1]
	if args[2] != '0': embeddings_dir = args[2]
	if args[3] != '0': 
		timestamped_results_dir = args[3]
		mode = "a+"
		skip_step_1 = True
	prefix_dir = args[4]+'_'
	if args[5] != '0': it = int(args[5])
	if args[6] != '0': alpha = float(args[6])
	if args[7] != '0': hidden_dim = int(args[7])

	print '\n>>>>>>>>>>>> Starting training and test >>>>>>>>>>>'
	print "Local time: "+time.strftime("%c")
	print '\nInput benchmark file:\n', sample_data_path
	if not os.path.exists('../results/'): os.makedir('../results/')

	if not skip: timestamped_results_dir = get_sample_matrix(results_dir, prefix_dir, sample_data_path, embeddings_dir)

	start_training_kfCV(timestamped_results_dir, it=it, alpha=alpha, hidden_dim=hidden_dim)

	if not skip: end_mark(timestamped_results_dir)

	print "\n\nLocal time: "+time.strftime("%c")
	print '<<<<<<<<<<<< Ended neuron unit training and test <<<<<<<<<<<<<\n'

if __name__ == '__main__':
	args = sys.argv
	main(args)
