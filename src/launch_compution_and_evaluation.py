#!/usr/bin/python

import os
import sys
import time
import shutil
import itertools
import gensim, logging #CBOW
import numpy as np #Sparse random projection
from sklearn import random_projection #Sparse random projection
from gensim import utils, corpora, matutils, models #Random projection




help_s = '''

This script performs two proocedures: computating the word embeddings of the five models: CBOW, HPCA, TSCCA, Random Projection, GloVe, and evaluating the terms based on the existing models or the models generated during the former procudure.

Inputs:

		Attention: One of the following first two arguments must be "1" to avoid repeated input! 

		[1] directory where the corpora locate (Plain text and one sentence per line)
		put 0 to apply the default setting: "../input_corpora/"

		[2] choice of embeddings to compute or directly using existing embeddings:
		put 0 for all the five models
		put 1 for CBOW
		put 2 for GloVe
		put 3 for HPCA
		put 4 for Random Projections (must be run later than HPCA)
		put 5 for TSCCA
		put existing embeddings directory to skip this procedure (terminated with "/")
		put 00 to use Schnabel Embeddings ("../schnabel_embeddings/")
		Attention: only when all the five models are available that the evaluation procedure will perform
		
		[3] input terms/descriptors path
		put 0 for default setting: "../input_terms_descriptors/terme_au_concepts_merged_cleaned.tsv"
				
		[4] prefix of the result directory name
		which together with the timestamp serves as the name of the result directory
			


Version 0.1 by Jie He @LGI2P, EMA

'''



class Sentences_flow(object):  # a memory-friendly iterator for multi-corpus (corpora)
	def __init__(self, filepath): self.filepath = filepath
	def __iter__(self):
		for line in open(self.filepath):
			yield line.split()
			
def concatenate_corpora(corpora_dir, corpus_path):
	with open(corpus_path, 'w+') as outfile:
		for fname in os.listdir(corpora_dir):
			with open(corpora_dir+'/'+fname) as infile:
				for line in infile: outfile.write(line)
	return corpus_path
				
def process_matrix_chunk_random_projections(Matrix, output_vec_chunk):
	global Matrix_reduced
	Matrix_reduced = transformer.fit_transform(Matrix)
	# Store the reduced matrix chunk
	np.savetxt(output_vec_chunk, Matrix_reduced, fmt = '%.5f')


def creat_new_result_folder():
	if not os.path.exists('../results/'): os.makedirs('../results/')
	timestr = time.strftime("%m%d%H%M%S") 
	global timestamped_results_dir
	timestamped_results_dir=results_dir+prefix_of_timestamped_results_dir+timestr+"/"
	os.makedirs(timestamped_results_dir)



if(len(sys.argv) < 5):
	print help_s
	exit()
# Parameters and inputs
NUM_THREADS=" -threads 8"
corpora_dir = "../input_corpora/"
corpus_concatenated_path = "../metadata/corpus_concatenated.txt"
terms_descriptors_path = "../input_terms_descriptors/terme_au_concepts_merged_cleaned.tsv"
embeddings_dir = '../schnabel_embeddings/'
results_dir = "../results/"

if sys.argv[1] != '0': corpora_dir = sys.argv[1]
if sys.argv[2][-1] == '/': embeddings_dir = sys.argv[2]
if sys.argv[3] != '0': terms_descriptors_path = sys.argv[3] 
prefix_of_timestamped_results_dir = sys.argv[4]+'_'


print "\n>>>>>>>>>>>> Starting the project >>>>>>>>>>>>>\n\t"
creat_new_result_folder()
print "\n>>>>>>>>>>>> Creating new result folder for this launching >>>>>>>>>>>>>\n\t"+timestamped_results_dir
	
if sys.argv[2] != '00' and sys.argv[2][-1] != '/':
	if not os.path.exists('../metadata/'): os.makedirs('../metadata/')
	embeddings_dir = timestamped_results_dir+'embeddings/'
	print "\n\n>>>>>>>>>>>> Creating result folder for Embeddings Computation >>>>>>>>>>>>>\n\t"+embeddings_dir
	os.makedirs(embeddings_dir)
	
	# 1 Get sentences from corpora using a memory-friendly iterator (only applicable for cbow at present)
	corpus_list = os.listdir(corpora_dir)
	if len(corpus_list) == 1: corpus_path = corpora_dir + corpus_list[0]
	if len(corpus_list) > 1: corpus_path = concatenate_corpora(corpora_dir, corpus_concatenated_path)
	print "\nInput corpora:\n\t", corpus_list
	
	# 2 Compute the models (embeddings)
	print "\n>>>>>>>>>>>> Starting embeddings computation >>>>>>>>>>>>>\n"
	print "Local time: "+time.strftime("%c")

	# 2.1 CBOW (Prediction-based model)
	if sys.argv[2] == "1" or sys.argv[2] == "0":
		print "\n>>>>>>>>>>>> Starting model 1 CBOW >>>>>>>>>>>>>\n"
		embeddings_dir_cbow = embeddings_dir+"cbow/"
	
		logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
		sentences = Sentences_flow(corpus_path)
		model_CBOW = gensim.models.Word2Vec(sentences,size=50, window=15, min_count=5, workers=4)
	
		cbow_result_path = embeddings_dir_cbow+'cbow_size_50.embeddings.vec'
		model_CBOW.save_word2vec_format(cbow_result_path, binary=0)
		with open(cbow_result_path, 'r') as vec_file:
			with open(embeddings_dir_cbow+'cbow_size_50.embeddings.voc',"w+") as voc:
				for line in vec_file: voc.write(line.split()[0]+'\n')
		print "\n<<<<<<<<<<<< Ended model 1 CBOW <<<<<<<<<<<<<<<\n"
		print "Local time: "+time.strftime("%c")
	

	# 2.2 GloVe (Count-based model)
	if sys.argv[2] == "2" or sys.argv[2] == "0":
		print "\n>>>>>>>>>>>> Starting model 2 GloVe >>>>>>>>>>>>>\n"
		embeddings_dir_glove = embeddings_dir+"glove/"
		if not os.path.exists(embeddings_dir_glove): os.makedirs('../metadata/glove/')
		CORPUS= " < "+corpus_path+" >"
		VOCAB_FILE = "../metadata/glove/glove_size_50.embeddings.vocc"
		VOCAB_FILE_refined = embeddings_dir_glove+"glove_size_50.embeddings.voc"
		BUILDDIR = "./tools/GloVe_1.2/build/"
		COOCCURRENCE_FILE=" ../metadata/glove/glove_cooccurrence.bin"
		COOCCURRENCE_SHUF_FILE=" ../metadata/glove/glove_cooccurrence.shuf.bin"
		SAVE_FILE=" -save-file "+embeddings_dir_glove+"glove_size_50.embeddings.vec"
		VERBOSE=" -verbose 2"
		MEMORY=" -memory 4.0"
		VOCAB_MIN_COUNT=" -min-count 5"
		VECTOR_SIZE=" -vector-size 50"
		MAX_ITER=" -iter 15"
		WINDOW_SIZE=" -window-size 15"
		BINARY=" -binary 0"
		X_MAX=" -x-max 10"
	
		cmd1_vocab_count = BUILDDIR +"vocab_count" + VOCAB_MIN_COUNT + VERBOSE + CORPUS + VOCAB_FILE
		cmd2_cooccurence = BUILDDIR +"cooccur" + MEMORY + " -vocab-file "+VOCAB_FILE + VERBOSE + WINDOW_SIZE + CORPUS + COOCCURRENCE_FILE
		cmd3_shuffle = BUILDDIR+"shuffle " + MEMORY + VERBOSE +" <"+ COOCCURRENCE_FILE +" >" + COOCCURRENCE_SHUF_FILE
		cmd4_glove = BUILDDIR +"glove" + SAVE_FILE + NUM_THREADS + " -input-file"+COOCCURRENCE_SHUF_FILE + X_MAX + MAX_ITER + VECTOR_SIZE + BINARY +  " -vocab-file "+VOCAB_FILE + VERBOSE
	
		print ">>>>>>>>>>"+cmd1_vocab_count
		os.system(cmd1_vocab_count)
		print ">>>>>>>>>>"+cmd2_cooccurence
		os.system(cmd2_cooccurence)
		print ">>>>>>>>>>"+cmd3_shuffle
		os.system(cmd3_shuffle)
		print ">>>>>>>>>>"+cmd4_glove
		os.system(cmd4_glove)
	
		# Evaluation based on build-in references
		#cmd5_glove_matlab = "matlab -nodisplay -nodesktop -nojvm -nosplash < ./tools/GloVe_1.2/eval/matlab/read_and_evaluate.m 1>&2"
		#cmd6_glove_octave = "octave < ./tools/GloVe_1.2/eval/octave/read_and_evaluate_octave.m 1>&2"
		#cmd7_glove_python = "python ./tools/GloVe_1.2/eval/python/evaluate.py --vocab_file "+VOCAB_FILE + " --vectors_file "+embeddings_dir_glove+"glove_size_50.embeddings.vec.txt" + " --eva_dir ./tools/GloVe_1.2/"
		#os.system(cmd5_glove_matlab)
		#os.system(cmd6_glove_octave)
		#os.system(cmd7_glove_python)
	
		# Refine the voc file
		with open(VOCAB_FILE,'r') as vocc, open(VOCAB_FILE_refined,'w+') as voc:
			for l in vocc: voc.write(l.split()[0]+'\n')
		print "\n<<<<<<<<<<<< Ended model 2 GloVe <<<<<<<<<<<<<<<\n"
		print "Local time: "+time.strftime("%c")
	

	# 2.3 HPCA (Count-based model)
	if sys.argv[2] == "3" or sys.argv[2] == "0":
		print "\n>>>>>>>>>>>> Starting model 3 HPCA >>>>>>>>>>>>>\n"
		embeddings_dir_hpca = embeddings_dir+"hpca/"
		if not os.path.exists(embeddings_dir_hpca): os.makedirs('../metadata/hpca/')
		HPCA_VOC_Path = " -vocab-file ../metadata/hpca/hpca_general.voc"
		VERBOSE_hpca = " -verbose 1"
		EMB_path = "../metadata/hpca/hpca_size_50.embeddings.vecc"
		
		# Deprecated becasue the preprocess has already been done
		#print "\n>>>>>>>>>>>>>>> HPCA 1 preprocessing >>>>>>>>>>>>\n"
		#cmd1_preprocess = "./tools/hpca-master/bin/preprocess -input-file "+corpus_path+" -output-file ../metadata/hpca/hpca_corpus_clean.txt -lower 1 -digit 1 -verbose 1"+ NUM_THREADS
		#print cmd1_preprocess
		#os.system(cmd1_preprocess)
	
		print "\n>>>>>>>>>>>>>>> HPCA 1 get vocabulary from cleaned corpus >>>>>>>>>>>>>>>>>>\n"
		cmd1_get_vocabulary = "./tools/hpca-master/bin/vocab -input-file " + corpus_path + HPCA_VOC_Path + VERBOSE_hpca + NUM_THREADS
		print cmd1_get_vocabulary
		os.system(cmd1_get_vocabulary)
	
		print "\n>>>>>>>>>>>>>> HPCA 2 get cooccurrence statistics <<<<<<<<<<<<<<<<\n"
		cmd2_cooccurence = "./tools/hpca-master/bin/cooccurrence -input-file "+ corpus_path + HPCA_VOC_Path +" -output-dir ../metadata/hpca/ -min-freq 50 -cxt-size 5 -dyn-cxt 0 -upper-bound 1.0 -lower-bound 0.00001 -memory 4.0"+ VERBOSE_hpca + NUM_THREADS
		print cmd2_cooccurence
		os.system(cmd2_cooccurence)
	
		print "\n>>>>>>>>>>>>>> HPCA 3 perform Hellinger PCA <<<<<<<<<<<<<<<<\n"
		cmd3_hpca = "./tools/hpca-master/bin/pca -input-dir ../metadata/hpca -rank 300" + NUM_THREADS + VERBOSE_hpca
		print cmd3_hpca
		os.system(cmd3_hpca)
	
		print "\n>>>>>>>>>>>>>> HPCA 4 compute word embeddings <<<<<<<<<<<<<<<<\n"
		cmd4_computeembeddings = "./tools/hpca-master/bin/embeddings -input-dir ../metadata/hpca -output-path " + EMB_path + " -dim 50 -eig 0 -norm 0 " + VERBOSE_hpca + NUM_THREADS
		print cmd4_computeembeddings
		os.system(cmd4_computeembeddings)
	
		# Refine the results
		shutil.copyfile('../metadata/hpca/target_words.txt',embeddings_dir_hpca+'hpca_size_50.embeddings.voc')
		with open(EMB_path,'r') as vecc, open('../metadata/hpca/target_words.txt','r') as voc, open(embeddings_dir_hpca+'hpca_size_50.embeddings.vec','w+') as vec:
			for l_vecc, l_voc in itertools.izip(vecc,voc): vec.write(l_voc.strip()+'\t'+l_vecc.strip()+'\n') 
	
		print "\n<<<<<<<<<<<< Ended model 3 HPCA <<<<<<<<<<<<<<<\n"
		print "Local time: "+time.strftime("%c")
	

	# 2.4 Random Projection (Count-based model)
	if sys.argv[2] == "4" or sys.argv[2] == "0":
		print "\n>>>>>>>>>>>> Starting model 4 Sparse Random Projection >>>>>>>>>>>>>\n"
		embeddings_dir_random_projection = embeddings_dir+"random_projection/"
		if not os.path.exists(embeddings_dir_random_projection): os.makedirs('../metadata/random_projection/')
		# Load the co-occurrence matrix
		transformer = random_projection.SparseRandomProjection(n_components=50, density='auto', eps=0.1, dense_output=False, random_state=None)# n_components is the dimension of the reduced matrix
		with open('../metadata/hpca/cooccurrence_matrix.txt','r') as mat,  open("../metadata/random_projection/embeddings.vecc",'w+') as output_vec_chunk:
			i = 0
			rows = sum(1 for line in mat) # count rows
			mat.seek(0,0)
			columns = len(mat.readline().split()) # count columns
			mat.seek(0,0)
			print 'Original co-occurrence matrix dimension: ', rows, ' * ', columns
			print '\nStarting chunking the matrix and applying the sparse random projections ...'
			chunk_row_num = 1000	# define chunk matrix row number
			Matrix = np.zeros(shape=(chunk_row_num, columns)) # initiate a zero chunk matrix
			for line in mat:
				Matrix[i] = line.split()
				i += 1
				if i == chunk_row_num:
					process_matrix_chunk_random_projections(Matrix, output_vec_chunk)	 # apply the sparse random projections to the chunk matrix and store it in temporal file
					i = 0  # reset the load pointer
			Matrix_strip = Matrix[: (rows % chunk_row_num )] # copy the last chunk which is stored in the Matrix variable when it leaves the "for" loop
			process_matrix_chunk_random_projections(Matrix_strip, output_vec_chunk)	 # apply the sparse random projections to the chunk matrix and store it in temporal file
			
		print "\nThe last chunk of co-occurence matrix is reduced to " + str(Matrix_reduced.shape)
		
		# Store the reduced matrix
		with open(embeddings_dir_random_projection+"/random_projection_size_50.embeddings.vec",'w+') as output_vec, open ('../metadata/hpca/target_words.txt') as voc, open('../metadata/random_projection/embeddings.vecc','r') as vecc:
			for l_vecc, l_voc in itertools.izip(vecc, voc):
				output_vec.write(l_voc.strip() + '\t' + l_vecc)
				
		# Copy vocabulary file from HPCA
		shutil.copyfile('../metadata/hpca/target_words.txt',embeddings_dir_random_projection+'random_projection_size_50.embeddings.voc')
		print "\n<<<<<<<<<<<< Ended model 4 Sparse Random Projection <<<<<<<<<<<<<<<\n"
		print "Local time: "+time.strftime("%c")
	
	
	# 2.5 TSCCA
	if sys.argv[2] == "5" or sys.argv[2] == "0":
		print "\n>>>>>>>>>>>> Starting model 5 TSCCA >>>>>>>>>>>>>\n"
		embeddings_dir_tscca = embeddings_dir+"tscca/"
		if not os.path.exists(embeddings_dir_tscca): os.makedirs('../metadata/tscca/')
	
		tscca_emb_path = embeddings_dir_tscca+'tscca_size_50.embeddings.vec'
		cmd_tscca = 'ant -Dcorpus_path='+corpus_path+' CCAVariantsTSCCA '
		print cmd_tscca
		os.system(cmd_tscca)
		shutil.copyfile('../metadata/tscca/eigenDictCCARunningTextTwoStepLRvsW',tscca_emb_path)
	
		# Move the vectors file and extract the vocabulary file
		with open(embeddings_dir_tscca+'tscca_size_50.embeddings.voc','w+') as voc, open(tscca_emb_path,'r') as vec:
			for l_vec in vec: voc.write(l_vec.split()[0]+'\n')
	
		print "\n<<<<<<<<<<<< Ended model 5 TSCCA <<<<<<<<<<<<<<<\n"
		print "Local time: "+time.strftime("%c")
	
	
	print "\n<<<<<<<<<<<< End of calculation <<<<<<<<<<<<<<<\n"

# Evaluation (perform conditionally)
if sys.argv[2] == "0" or sys.argv[2][-1] == "/"  or sys.argv[2] == "00":
	print "\n>>>>>>>>>>>> Starting evaluation >>>>>>>>>>>>>>>\n"
	print "Local time: "+time.strftime("%c")+"\n"

	evaluation_dir = timestamped_results_dir+'evaluation/'
	print 'Making result directory:\n\t', evaluation_dir
	os.makedirs(evaluation_dir)
	cmd_evaluation = "./tools/models_evaluation.py "+terms_descriptors_path+' '+embeddings_dir+" "+evaluation_dir+" 0 "+ prefix_of_timestamped_results_dir
	print '\n'+cmd_evaluation
	os.system(cmd_evaluation)
	
	print "\n<<<<<<<<<<<< Evaluation Ended <<<<<<<<<<<<<<<\n"
	print "Local time: "+time.strftime("%c")
	
os.rename(timestamped_results_dir, timestamped_results_dir[:-1]+time.strftime("__%m%d%H%M%S_complete"))
print "\n<<<<<<<<<<<<  Project Ended  <<<<<<<<<<<<<<<\n"



















