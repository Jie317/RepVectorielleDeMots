#! usr/bin/python
import sys
import time
import glob
import tensorflow as tf
import numpy as np

help_s = '''

A script to 
Inputs:

	[1] sample data path (one term and its frequency per line and separated by comma)
	put 0 if using the default test data: "../input_terms_for_clustering/terms_wines_frequences.csv" 
	
	[2] directory where all the models locate (where the folders "tscca phca ..." locate) 
	put 0 if using the default directory: "../schnabel_embeddings/"
	
	[3] number of centers
	put 0 for default value: 5
	
	[4] max iterations in the K means clustering procedure
	put 0 for default value: 1000

	
Version 0.1 by Jie He @LGI2P, EMA

'''

def tensorflow_k_means_cluatering(points_list, K, MAX_ITERS): # return clustering centers and point assignments
	start = time.time()
	N = len(points_list)
	dims = len(points_list[0])
	points = tf.constant(points_list)
	cluster_assignments = tf.Variable(tf.zeros([N], dtype=tf.int64))
	#  Initialization of the centroids (could)
	centroids = tf.Variable(tf.slice(points, [1,0], [K,dims]))
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

def get_model_names(sup_dir):
	print '\nRetrieving model names >>>>>>'
	mns = []
	m_dirs = glob.glob('%s*/' % sup_dir)
	for n in m_dirs: mns.append(n.replace(sup_dir,'')[:-1])
	print 'Model names:', mns
	return mns

def get_term_frequency(terms_path):
	print '\nRetrieving terms and frequencies >>>>>>'
	t_f = {} # terms are keys and frequencies are values
	with open(terms_path) as term_f:
		term_f.readline()
		for l in term_f: 
			t_f[l.split(',')[0]] = int(l.split(',')[1])
	print 'Total terms:',sum(t_f.itervalues()),'Unique terms:',len(t_f)
	return t_f


def get_points(models_dir, m, t_f):
	print '\nRetrieving points(vectors) >>>>>>'

	ps = []
	with open('%s%s/%s_size_50.embeddings.vec' % (models_dir, m, m)) as vec:
		for l in vec:
			if l.split()[0] in t_f:
				ps += [[float(v) for v in l.split()[1:]]]*t_f[l.split()[0]]
				del t_f[l.split()[0]]
	print 'Total points(vectors):', len(ps), ' Vector dimension:', len(ps[0]), '\nTerms not found:', t_f 
	return [len(ps), len(ps[0]), ps]

def find_concepts(vecs):
	for vec in vecs:
		pass # calculate sims and sort then get the biggest one



def main(args):
	if len(args) < 5:
		print help_s
		exit()

	terms_path = '../input_terms_for_clustering/terms_wines_frequences.csv'
	models_dir = '../schnabel_embeddings/'
	K = 5
	MAX_ITERS = 1000

	if args[1] != '0': terms_path = args[1]
	if args[2] != '0': models_dir = args[2]
	if args[3] != '0': K = int(args[3])
	if args[4] != '0': MAX_ITERS = int(args[4])

	mns = get_model_names(models_dir)
	t_f = get_term_frequency(terms_path)

	for m in mns:
		print '\n\n>>>>> Starting model ', m
		[N, dims, points] = get_points(models_dir, m, t_f)
		[centers, assignments, iters, time] = tensorflow_k_means_cluatering(points, K, MAX_ITERS)
		print ('\nFor model:%s\nFound in %.2f seconds' % (m, time)), iters, 'iterations'
		print 'Centroids:\n', centers
		print '\n>>>>> Starting model ', m
		[N, dims, points] = get_points(models_dir, m, t_f)
		[centers, assignments, iters, time] = tensorflow_k_means_cluatering(points, K, MAX_ITERS)
		print ('For model:%s\nFound in %.2f seconds' % (m, time)), iters, 'iterations'
		print 'Centroids:', centers
		#print 'Cluster assignments:', assignments

if __name__ == '__main__':
	args = sys.argv
	main(args)


