#! /usr/bin/python
import sys
import time
import random
import tensorflow as tf
import numpy as np
from tools.neural_network import cosine_similarity, end_mark, get_model_names, creat_result_folder

help_s = '''

A script to cluster the descriptors of the scent of wine products. The algorithm used here is K-means clustering and was implemented on Tensorflow.

Inputs:

	[1] sample data path (one term and its frequency per line and separated by comma)
	put 0 if using the default test data: "../input_terms_for_clustering/terms_wines_frequences.csv" 
	
	[2] directory where all the models locate (where the folders "tscca phca ..." locate) 
	put 0 if using the default directory: "../schnabel_embeddings/"
	
	[3] number of centers
	put 0 for default value: 5
	
	[4] max iterations in the K means clustering procedure
	put 0 for default value: 1000

	[5] prefix of the result folder name
	any string you like to mark the folder

	
Version 0.1 by Jie He @LGI2P, EMA

'''

def tensorflow_k_means_cluatering(points_list, init_cs, K, MAX_ITERS): # return clustering centers and point assignments
	start = time.time()
	N = len(points_list)
	dims = len(points_list[0])
	points = tf.constant(points_list)
	cluster_assignments = tf.Variable(tf.zeros([N], dtype=tf.int64))
	#  Initialization of the centroids (Potential problem here about chosing the initial centroids!!!)
	centroids = tf.Variable(init_cs)
	# Replicate to N copies of each centroid and K copies of each
	# point, then subtract and compute the sum of squared distances.
	rep_centroids = tf.reshape(tf.tile(centroids, [N, 1]), [N, K, dims])
	rep_points = tf.reshape(tf.tile(points, [1, K]), [N, K, dims])
	sum_squares = tf.reduce_sum(tf.square(rep_points - rep_centroids),reduction_indices=2)
	# Use argmin to select the lowest-distance point
	best_centroids = tf.argmin(sum_squares, 1)
	did_assignments_change = tf.reduce_any(tf.not_equal(best_centroids, cluster_assignments))
	def bucket_mean(data, bucket_ids, num_buckets): # return the centroids
		total = tf.unsorted_segment_sum(data, bucket_ids, num_buckets)
		count = tf.unsorted_segment_sum(tf.ones_like(data), bucket_ids, num_buckets)
		return total / count
	means = bucket_mean(points, best_centroids, K)
	# Do not write to the assigned clusters variable until after
	# computing whether the assignments have changed - hence with_dependencies
	with tf.control_dependencies([did_assignments_change]):
		do_updates = tf.group(centroids.assign(means), cluster_assignments.assign(best_centroids))
	init = tf.initialize_all_variables()
	sess = tf.Session()
	sess.run(init)
	changed = True
	iters = 0
	while changed and iters < MAX_ITERS:
		iters += 1
		[changed, _] = sess.run([did_assignments_change, do_updates])
	[centers, assignments] = sess.run([centroids, cluster_assignments])
	end = time.time()
	return [centers, assignments, iters, end-start]

def get_term_frequency(terms_path):
	print '\nRetrieving terms and frequencies >>>>>>'
	t_f = {} # terms are keys and frequencies are values
	with open(terms_path) as term_f:
		term_f.readline()
		for l in term_f: t_f[l.split(',')[0]] = int(l.split(',')[1])
	print 'Total terms:',sum(t_f.itervalues()),'Unique terms:',len(t_f)
	return t_f

def get_points_and_init_centroids(models_dir, m, t_f, K):
	print '\nRetrieving points(vectors) and initial random centroids >>>>>>'
	init_cs = []
	ps = []
	t_vs ={}
	t_f_rep = t_f.copy()
	with open('%s%s/%s_size_50.embeddings.vec' % (models_dir, m, m)) as vec:
		for l in vec:
			t = l.split()[0]
			vec = [float(v) for v in l.split()[1:]]
			if t in t_f:
				t_vs[t] = vec
				ps += [vec]*t_f[t]
				del t_f_rep[t]
	ts_valid = t_vs.keys()
	random.shuffle(ts_valid)
	init_c_terms = ts_valid[:K]
	for ct in init_c_terms: init_cs.append(t_vs[ct])
	print 'Total points(vectors):', len(ps), ' Vector dimension:', len(ps[0])
	print '\nTerms not found:\n', t_f_rep, '\n\nInitial random centroids:', init_c_terms
	return [len(ps), len(ps[0]), ps, init_cs, init_c_terms]

def find_max_sim(m_dir, m, vecs):
	print '\nFinding terms with maximal similarity in model %s >>>>>>' % m
	max_sim_terms = []
	max_sims = []
	with open('%s%s/%s_size_50.embeddings.vec' % (m_dir, m, m)) as in_vec:
		for i,vec_a in enumerate(vecs):
			print 'Processing point', (i+1)
			similarities = {} # the key is vec_b and the value is its sim with current vec_a
			best_sim = 0
			best_sim_label = None
			in_vec.seek(0) 
			for l in in_vec: 
				similarities[l.split()[0]] = cosine_similarity(vec_a, [float(v) for v in l.split()[1:]])
			max_sim_term = (sorted(similarities, key=similarities.get, reverse=True))[0]
			max_sim_terms.append(max_sim_term)
			max_sims.append(similarities[max_sim_term])
	return [max_sim_terms, max_sims]


def main(args):


	if len(args) < 6:
		print help_s
		exit()

	# 0 define parameters
	terms_path = '../input_terms_for_clustering/terms_wines_frequences.csv'
	models_dir = '../schnabel_embeddings/'
	K = 5
	MAX_ITERS = 1000

	if args[1] != '0': terms_path = args[1]
	if args[2] != '0': models_dir = args[2]
	if args[3] != '0': K = int(args[3])
	if args[4] != '0': MAX_ITERS = int(args[4])
	prefix_dir_name = args[5]


	print '\n>>>>>>>>>>>> K-means clustering >>>>>>>>>>>'
	print "Local time:", time.strftime("%c")
	print '\nInput benchmark file:\n', terms_path

	# 1 retrieve the centers (the centroid points given by vectors)
	mns = get_model_names(models_dir)
	t_f = get_term_frequency(terms_path)
	results_dir = creat_result_folder(prefix_dir_name)

	ms_cs = {} # the keys are model names and the values are the centers
	init_c_terms_ms = [] # initial center terms for each model
	iters_ms = [['Iterations']] # iterations to cluster
	for i,m in enumerate(mns):
		print '\n\n>>>>> Starting model %d: %s' % (i, m)
		[N, dims, points, init_c_points, init_c_terms] = get_points_and_init_centroids(models_dir, m, t_f, K)
		[centers, assignments, iters, runtime] = tensorflow_k_means_cluatering(points, init_c_points, K, MAX_ITERS)
		print ('\Starting K-means clustering for model: %s\nFound in %.2f seconds' % (m, runtime)), iters, 'iterations'
		print 'Centroid matrix size and type:', centers.shape, type(centers)
		ms_cs[m] = centers
		init_c_terms_ms.append(init_c_terms)
		iters_ms.append([iters])
		#print 'Cluster assignments:', assignments

		# save center matrix
		fname = results_dir+'centers.mat'
		np.savetxt(fname, centers, delimiter='\t', comments='Centers for %s' % m, fmt='%.5f')


	# 2 find the terms which have the maximal similatrities with these centroid points
	clustering_result = [] # store the center terms and their maximal similarities
	for m in ms_cs:
		clustering_result.append(find_max_sim(models_dir, m, ms_cs[m]))


	# 3 establish conclusion table
	label = ['Model'] + ['Center %d' % (i+1) for i in xrange(K)] + ['Avg.']
	row_label = [[m] for m in mns] + [['Avg.']]
	center_terms = [row[0] for row in clustering_result]
	term_sims = [row[1] for row in clustering_result]
	term_sims_1 = np.hstack((term_sims, np.mean(term_sims, axis=1,keepdims=True)))
	term_sims_mean = np.vstack((term_sims_1, np.mean(term_sims_1,axis=0, keepdims=True)))
	table_clustered_terms = np.hstack((np.vstack((label[:-1], np.hstack((row_label[:-1], center_terms)))), iters_ms))
	table_sims = np.vstack((label, np.hstack((row_label, term_sims_mean))))
	table_init_c_terms_ms = np.vstack((label[:-1], np.hstack((row_label[:-1], init_c_terms_ms))))


	# 4 save to csv result file
	with open(results_dir+'terms_clustering_results.csv', 'a+') as re_p:
		np.savetxt(re_p, np.array(table_clustered_terms), delimiter='\t', header='\n>>>>>>>>\nNew launching local time %s\nCenters' % time.strftime('%c'), fmt='%s')
		np.savetxt(re_p, np.array(table_sims), delimiter='\t', header='\nSimilarities', fmt='%s')
		np.savetxt(re_p, np.array(table_init_c_terms_ms), delimiter='\t', header='\nInitial center terms', fmt='%s')


	# end
	end_mark(results_dir)
	print "\n\nLocal time: "+time.strftime("%c")
	print '<<<<<<<<<<<< Ended terms clustering task <<<<<<<<<<<<<\n'



if __name__ == '__main__':
	args = sys.argv
	main(args)


