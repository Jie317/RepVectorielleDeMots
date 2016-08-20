#!/usr/bin/python
import glob, time, sys, os
import numpy as np
from sklearn.cross_validation import KFold
from tools.neural_network import simple_neural_network

help_s = '''

A script to aggregate the models by applying a set of weights to each model. The weights are trained by a single neuron model which consists of an input layer and an output layer. The results is given by mean squared error, which are stored in the global result csv file besides the folder "details".

Inputs:
	
	[1] directory of "details" which locates in the subdirectory of the timestamped folder under the "result" folder
	For example, "../results/sch_single_neuron_0811211927__0811212032_complete/evaluation_complete/details/"
	Attentioon: run "launch_computation_and_evaluation.py" first to generate this directory

	[2] iteration number during the training
	put 0 to apply the default value: 100000

	[3] learning rate during the training
	put 0 to apply the default value: 0.05

Version 0.1 by Jie He @LGI2P, EMA

'''


		
def get_sm(level): # return sample matrix and concepts number
	# extract the vocabularies (terms and concepts)	
	voc_concepts = set()
	voc_terms = set()
	pairs_dict = {}
	with open(details_dir + 'Level_%d/intersection.pair' % level) as com_pairs:
		for l in com_pairs:
			voc_terms.add(l.split()[0])
			voc_concepts.add(l.split()[1])
			pairs_dict[l.split()[0]] = l.split()[1]
	print '\n\n>>>>>>>>>>Level %d\nvoc terms: %d\n' % (level,len(voc_terms)), voc_terms
	print '\nvoc cncepts: %d\n' % len(voc_concepts), voc_concepts,'\n'
	# extract all the original pair sims from all the models in this level
	sims_all_models = {} # key is the model name, to store all the sim info for all the terms in all the models
	for m in mns:
		model_sims = {} # key is the pairs, value is the sims, for each model
		with open(details_dir + 'Level_%d/%s_term_concepts.sims' % (level, m),'r') as f:
			for line in f: model_sims[line.split('\t')[0]] = float(line.split('\t')[1])
			sims_all_models[m] = model_sims
	# extract sample items
	sample_items = [] # matrix where the sample items are stored (pair, input and output)
	for term in voc_terms:
		for concept in voc_concepts:
			# generate samples (the last element is output)
			sample_unit = []
			sample_unit = [term, concept, pairs_dict[term]] + [sims_all_models[m][term+' '+concept] for m in mns] # the order of values remains the same as that of model_names
			# add the classification label(output)
			if pairs_dict[term] == concept: sample_unit.append(1)
			else: sample_unit.append(0)
			sample_items.append(sample_unit)
	# get sample matrix
	sm = [r[3:] for r in sample_items] 
	return sm, len(voc_concepts)

def write_sample_items_to_file(cn, sample_items): # return none	
	fpa = details_dir+'Level_%d/samples.item' % level
	with open(fpa,'w+') as output_samples:
		output_samples.write('Term\tConcepts\tCorrect Concept\t')
		for mn in mns: output_samples.write(mn+'\t')
		output_samples.write('%d\n' % cn)
		for l in sample_items:
			for value in l: output_samples.write('%s\t' % value)
			output_samples.write('\n')

def start_training_kfCV_for_TC_evalutation(level,k=3): # return weights matrix
	kv = KFold(len(sm)/cn, n_folds=k, shuffle=True, random_state=None)
	count = 0
	test = [] 
	test_w = []
	test_m = {}
	ws = []
	for n in mns: test_m[n] = []
	for tr_index, te_index in kv:
		count += 1
		print '\nLevel %d, K_fold %d\ntrain index:\n' % (level,count),tr_index, '\ntest index: \n', te_index
		train_set = [] 
		test_set = [] 
		for tr in tr_index:
			train_set += sm[tr*cn : (tr+1)*cn]
		for te in te_index:
			test_set += sm[te*cn : (te+1)*cn]
		X = np.array(train_set, dtype='|S4').astype(np.float)[:, :-1]
		y = np.array(train_set, dtype='|S4').astype(np.float)[:, -1:]
		
		X_t = np.array(test_set, dtype='|S4').astype(np.float)[:, :-1]
		y_t = np.array(test_set, dtype='|S4').astype(np.float)[:, -1:]	

 		weights, ph0, ph1, ph2, ph3, ph4 = simple_neural_network(X, y, X_t, y_t, mns, it=it, alpha=alpha, hd=HIDDEN_DIM) ###### train the model and get the weights
 		print "weights:\n",weights
 		weights = normalize(weights) # rescale the weights by Frobenius Norm to make them comparable between the 4 levels
 		print "weights rescaled:\n",weights
 		ws.append(weights.T[0].tolist()) # add "[0]" to convert the 2-d array into a 1-d array

 		# test with and without the trained weights
 		test.append(test_TC_evaluation(X_t, y_t))
 		for i,n in enumerate(mns):
 			test_m[n].append(test_TC_evaluation(np.array(X_t[:,i]).reshape((len(X_t),1)),y_t))
 		test_w.append(test_TC_evaluation(X_t, y_t, w=weights))

 	return ws, test, test_w, test_m
		
def test_TC_evaluation(X_t, y_t, w=None): # return test result (prediction ratio, or evaluation performance)
	if w is None: w = [[1.] for n in range(len(X_t[0]))]
	w_array = np.array(w)
	correct_count = 0
	print 'Weights in test:\n',w_array
	#print 'X_t:\n',X_t
	sum_sims = X_t.dot(w_array)
	#print 'Sum_sims:\n',sum_sims

	for i in range(len(X_t)/cn):
		t_tem = sum_sims[i*cn:(i+1)*cn]
		c_tem = y_t[i*cn:(i+1)*cn]
		#print np.argmax(t_tem)

		if c_tem[np.argmax(t_tem)] == 1: 
			correct_count += 1
	return [correct_count, len(X_t)/cn, float(correct_count)/(len(X_t)/cn)] 

def normalize(v): # apply Frobenius Norm
    norm=np.linalg.norm(v)
    if norm==0: return v
    return v/norm	

def save_oprms():
	g_re.write('\n>>>>Model Prediction Accuracy\n')
	for e in head_pr_m: g_re.write(e+'\t')
	g_re.write('\n')
	for l in range(1,5):
		h_row0 = [['Level %d' % l] for n in mns] + [['Average']]
		h_row1 = [[n] for n in mns] + [['-']]
		#print 'oprms:\n',oprms
		oprms[l] = np.hstack((np.hstack((h_row0, h_row1)), np.vstack((oprms[l], np.mean(oprms[l],axis=0)))))
		np.savetxt(g_re, oprms[l], delimiter='\t', fmt='%s')

def save_fold_details():
	np.savetxt(g_re, np.array(ws), delimiter='\t', header='\n>>>>>>>>K-fold details: Level %d\nWeight matrix (K=3)' % level, fmt='%.5f')
	np.savetxt(g_re, np.array(test), delimiter='\t', header='Test without weights', fmt='%.3f')
	np.savetxt(g_re, np.array(test_w), delimiter='\t', header='Test with weights', fmt='%.3f')
	for n in mns: np.savetxt(g_re, np.array(test_m[n]), delimiter='\t', header='Test for model %s' % n, fmt='%.3f')


if len(sys.argv) != 4:
	print help_s
	exit()

# parameters
it = 100000 # iterationn number to update the weights
alpha = 0.05 # learning rate to rescale the update value
HIDDEN_DIM = 1 # fixed to 1 to degrade the neural model to single neuron model
details_dir = sys.argv[1]
if sys.argv[2] != '0': it = int(sys.argv[2])
if sys.argv[3] != '0': alpha = float(sys.argv[3])

global_result_path = glob.glob(details_dir[:-8]+'*evaluation_result.csv')[0]


print '\n---------------- Starting aggregation --------------\n'

# get model names (and fix their order by setting the variable type as list)
mns = []
for fpath in glob.glob(details_dir + 'Level_1/*term_concepts.sims'):
	model_name = fpath.replace(details_dir + 'Level_1/', '').replace('_term_concepts.sims', '')
	mns.append(model_name)

wm = [] # weights matrix (4 levels)
oprs = [] # original prediction accuracies (4 levels)
prs = [] # prediction accuracies when applying trained weights (4 levels)
oprms = {} # original prediction accuracies for each model (4 levels)

g_re = open(global_result_path,'a+')
for level in range(1,5):
	sm, cn = get_sm(level) # get sample matrix and concepts number in current level
	ws, test, test_w, test_m = start_training_kfCV_for_TC_evalutation(level)
	#print 'ws:\n',ws,type(ws)

	wm.append(np.mean(ws,axis=0).tolist())
	oprs.append(np.mean(test,axis=0).tolist())
	prs.append(np.mean(test_w,axis=0).tolist())

	oprms[level] = []
	for n in mns: oprms[level].append(np.mean(test_m[n],axis=0).tolist())

	#save_fold_details() # save the details of each fold in K-fold Cross Validation

# write conclusion tables to the result file
# make headers and titles to establish the table
h_wm = ['Model Name'] + mns
h_pr = ['Concept Level','Correct Prediction','Pairs Number','Prediction Accuracy']
h_pr_m = ['Concept Level','Model Name','Correct Prediction','Pairs Number','Prediction Accuracy']
h_row_pr = [['Level %d' % l] for l in range(1,5)]+[['Average']]
h_row = [['Level %d' % l] for l in range(1,5)]
h_row_pr_m = [[n] for n in mns]+[['Average']]
# calculate the averages and add headers and other infos to complete the table (to facilitate the write process)
wm_output = np.vstack((h_wm, np.hstack((h_row,wm))))
oprs_output = np.vstack((h_pr, np.hstack((h_row_pr,np.vstack((oprs,np.mean(oprs,axis=0)))))))
prs_output = np.vstack((h_pr, np.hstack((h_row_pr,np.vstack((prs,np.mean(prs,axis=0)))))))
g_re.write('\n>>>>>>>>>>>>>>>>\nTC evaluation task: local time %s\n' % time.strftime("%d%H%M%S"))
np.savetxt(g_re, wm_output, delimiter='\t', header='>>>>>>>>Conclusion (it=%d,alpha=%.2f)\n>>>>Weight matrix (K=3)' % (it,alpha), fmt='%s')
np.savetxt(g_re, oprs_output, delimiter='\t', header='\n>>>>Original Prediction Accuracy', fmt='%s')
np.savetxt(g_re, prs_output, delimiter='\t', header='\n>>>>Prediction Accuracy With Trained Weights', fmt='%s')
#save_oprms() # no need to run it every time unless the original data(samples) are changed

g_re.close()

print '\n---------------- Aggregation ended --------------\n'



