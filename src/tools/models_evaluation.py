#!/usr/bin/python

import os
import time
import shutil
import sys



help_s = '''

This script is used to compute the performance of all the models (vector representations).
The evaluation is based on the same level for all models, which means it takes intersection pairs of each model 
for the same level.

You can run this script anywhere with the following four arguments:

	[1] test data path where the terms-descriptors file locates 
	put 0 if using the default test data: "./test_data/terme_au_concepts_merged_cleaned.tsv" 
	
	[2] directory where all the models locate (where the folders "tscca phca ..." locate) 
	put 0 if using the default directory: "./"
	
	[3] result directory: chose where to store the evaluation result (which consists of a file and a folder), 
	put 0 if using the default path: "./results/"
	
	[4] vector format of models
	put 0 if uncompressed, 1 if compressed
	
	[5] prefix of the result file name
	
	
Version 0.1 by Jie He @LGI2P, EMA

'''

def make_result_file(prefix):
	global result_file
	result_file = results_path+prefix+"evaluation_result"+".csv"
	with open("./tools/template_evaluation_result.csv", 'r') as template, open( result_file, 'w+') as result:
		result.write(prefix+template.readline())
		for line in template:
			result.write(line)

		

if(len(sys.argv) < 6):
	print help_s
	exit()


approaches = next(os.walk(sys.argv[2]))[1]

test_data_path = "./test_data/"
results_path = "../results/"
vectors_directory = "./"
prefix = ''
iteration_times = 5000
k_fold =3

if (sys.argv[1] != '0'): test_data_path = sys.argv[1]
if (sys.argv[2] != '0'): vectors_directory = sys.argv[2]
if (sys.argv[3] != '0'): results_path = sys.argv[3]
prefix = sys.argv[5]
	
vector_format = sys.argv[4]

make_result_file(prefix)

print "\n\n\n---------------------------------------------------------"
print "---------------------------------------------------------"
print 'Models: ', approaches[:]
print "\nEstablishing result report (csv file):\n\t"+result_file
print "\nMaking  result directory for this evaluation:\n\t"+results_path


for level in range(1,5):
	
	sub_results_path = results_path+"details/Level_"+str(level)+"/"
	os.makedirs(sub_results_path)
	fnames_to_intersection = []
	
	print "\nMaking sub-directory for each level:\n\t "+sub_results_path
	print "\nEvaluating level", level
	print "\n >>>>>>>>>>>>>>>>>>>>>>>>> "

	with open(result_file,'a') as fa:
		fa.write("\n")
			
			
	
	for approach in approaches:
		
		inputData_vector_voc = (vectors_directory
							+approach+"/"
							+approach+"_size_50.embeddings.voc")
		inputData_vector = (vectors_directory
							+approach+"/"
							+approach+"_size_50.embeddings.vec")
		outputFile_voc = "voc_"+approach+".voc"
		outputFile_valid_pairs = "valid_pairs_"+approach+".pair"
		outputFile_vec_extracted = "vectors_extracted_"+approach+".vec"
		outputFile_performance_result = "performance_result_"+approach+".rank"
		
		log_file = "level_%d.log" % level
		
		
	
		# Command 1: generate_benchmark.py	
		print "\nGenerating valid pairs according to model: "+approach+" >>>>>>>>>>"
		cmd1_generate_benchmark = ("./tools/generate_benchmark.py "
								+ test_data_path + " "
								+ str(level) + " "
								+ inputData_vector_voc + " "
								+ sub_results_path + outputFile_voc + " "
								+ sub_results_path + outputFile_valid_pairs + " "
								+ "0" + " "
								+ " > " + sub_results_path + log_file)
		os.system(cmd1_generate_benchmark)
		
		fnames_to_intersection.append(sub_results_path + outputFile_valid_pairs)
		
		
		
	print "\nStarting the intersection >>>>>>>>>>>>>>>>>>"	
	# Command: find_intersection.py
	cmd_find_intersection = ("./tools/find_intersection.py "
							+ str(fnames_to_intersection).replace('\'','\\\'').replace(' ', '') + " "
							+ sub_results_path + "intersection.pair" + " "
							+ sub_results_path + "intersection_pair.voc" + " "
							+ ">> " + sub_results_path + log_file)
		
	print "\n\tExecuting command: python " + cmd_find_intersection
	os.system(cmd_find_intersection)	
		
	print "\nEnded intersection >>>>>>>>>>>>>>>>>>"	
		
		
	for approach in approaches:	
		
		inputData_vector_voc = (vectors_directory
							+approach+"/"
							+approach+"_size_50.embeddings.voc")
		inputData_vector = ( vectors_directory
							+approach+"/"
							+approach+"_size_50.embeddings.vec")
		outputFile_voc = "voc_"+approach+".voc"
		outputFile_valid_pairs = "valid_pairs_"+approach+".pair"
		outputFile_vec_extracted = "vectors_extracted_"+approach+".vec"
		outputFile_performance_result = "performance_result_"+approach+".rank"
		
		log_file = "level_%d.log" % level
		
		
		print "\n\tEvaluating level", level, "  Model", approach, "  >>>>>>>>>>>>>>>>>>>>"
		
		with open(result_file,'a') as fa:
			fa.write("Level%s,%s " % (level, approach))
			
		# Command 1: generate_benchmark.py	
		# Just for recording data
		cmd1_generate_benchmark = ("./tools/generate_benchmark.py "
								+ test_data_path + " "
								+ str(level) + " "
								+ inputData_vector_voc + " "
								+ sub_results_path + outputFile_voc + " "
								+ sub_results_path + outputFile_valid_pairs + " "
								+ result_file + " "
								+ " >> " + sub_results_path + log_file)
		os.system(cmd1_generate_benchmark)
		
		
		# Command 2: extract_vectors.py
		cmd2_extract_vectors = ("./tools/extract_vectors.py "
								+ sub_results_path + "intersection_pair.voc" + " "
								+ inputData_vector + " "
								+ sub_results_path + outputFile_vec_extracted + " "
								+ result_file+ " "
								+ sub_results_path + "intersection.pair"+ " "
								+ ">> " + sub_results_path + log_file)
		
		print "\n\tExecuting command_2: python " + cmd2_extract_vectors
		os.system(cmd2_extract_vectors)	
		
		# Command 3: compute_performance.py
		cmd3_compute_performance =( "./tools/compute_performance.py "
								+ vector_format + " "
								+ sub_results_path + outputFile_vec_extracted + " "
								+ sub_results_path + "intersection.pair" + " "
								+ sub_results_path + outputFile_performance_result + " "
								+ result_file+ " "
								+ approach+ " "
								+ ">> "+sub_results_path + log_file)
		
		print "\n\tExecuting command_3: python " + cmd3_compute_performance
		os.system(cmd3_compute_performance)
		
	# Calculate the average
	with open(result_file,'a') as fa:
		fa.write("Average,")
		for c in  ('C','D','E','F','G','H','I','J','K','L','M'):
			fa.write(",=AVERAGE(%s%d:%s%d)" % (c, (len(approaches)+2)*level-4, c, (len(approaches)+2)*level-5+len(approaches)))
		fa.write("\n")

# the following is kept in case of the need to concatenate the two procedures
# command_aggregation
#cmd_agg = './tools/single_neuron_aggregation_tc.py %s' % results_path+'details/'
#print '\n\ncmd_agg: %s' % cmd_agg
#os.system(cmd_agg)

# appending "complete" in the result folder's name to indicate the completion of this launching
os.rename(results_path, results_path[:-1]+'_complete/')







































	
