## This project has come out as an implementation of several methods to evaluate the performance of word vector representations during the internship at LGI2P, EMA (Mentors: [Sébastien Harispe](http://dblp.uni-trier.de/pers/hd/h/Harispe:S=eacute=bastien.html) and [Jacky Montmain](https://www.researchgate.net/profile/Jacky_Montmain)), which consists of four parts:
* 1) the computation of the five vector representations (word embeddings) and the evaluation of the models
* 2) the aggregation of model on the term evaluation task
* 3) the aggregation of model on the word similarity task
* 4) the clustering of terms by K-means


## Introduction to install the whole project and reproduce all the results

### Please note that:
* All the scripts mentioned below are in the folder `src`.
* All the scripts should be run under the directory of the folder `src`. 
* Whenever giving a directory as an argument, please try to use relative directory and end it with a slash `/`, such as `../input_corpora/corpora/`.
* All the output files and statistic tables (CSV files) are stored in the folder named `results` under the root directory after any launching.
* The start time and end time of a launching is concatenated to the folder name to distinguish every launching result.

## Step 0: check system environment and install dependencies
The whole project is developed on Ubuntu 16.04 LTS (64-bit, Kernel: 4.7.1) and Python 2.7.12. Other versions of Ubuntu should work with this project but Python should be the version 2.7.

To build the project environmemt, run with root the shell script `setup.sh` to install a set of dependencies and packages.  If there is any error during the installation, please find in the shell script the name of the package and install it manually.

### Before continuing, several datasets should be prepared:
* Corpus/corpora to computate the vector representations of words (a.k.a word embeddings), in plain text format. You can extract the corpus from wikipedia dump file using the shell script `launch\_corpus_extraction.sh`.
* Existing word embeddings to evaluate (For all the embeddings, please concatenate the model's name as prefix with the name of its vocabulary file and vector file, for example, change the file name `size\_50.embeddings.voc` to `hpca\_size_50.embeddings.voc` ).
* Term-discriptor file to evaluate the embeddings, tsv format. The built-in dataset already exists in the default input folder `input\_terms_discriptors`. Please keep the same form if you want to replace the file with another one.
* Benchmarks of word similarity. Already exsist in the default input folder  `input_sim\_benchmarks`. Please keep the same form if you want to replace the file with another one.
* Descriptor file of wine products for clustering task. Already exsists in the default input folder  `input\_terms\_for_clustering`.  Please keep the same form if you want to replace the file with another one.

If you need these files, you can also find some of them at my [google drive](https://drive.google.com/open?id=0B-TRyz0akbbaeHpaUk5SN1cybW8 ). 

## Step 1: perform the computation and evaluation of models
The arguments for this script are:
* [1] directory where the corpora locate (Plain text and one sentence per line)
* [2] choice of embeddings to compute or directly using existing embeddings
* [3] input terms/descriptors path
* [4] prefix of the result directory name
* Please note that for the computation of the model TSCCA, the settings are in the buil.xml file in the current folder. All the computations of embeddings have taken the default settings.

Please run firstly the python script `launch\_computation\_and\_evaluation.py` without argument and then read the specific explanation of these arguments which appears next. Default arguments are provided to give examples about the format. Then run it again with arguments and check the results in the folder `results`. The computation of models can last a long time, for example, training a corpus with 400Mb cost 2 hours on a physical machine with `Intel® Core™ i5-4210M CPU @ 2.60GHz × 4`.


## Step 2: perform the aggregation of model on the term evaluation task
The arguments for this script are:
* [1] directory of `details` which locates in the subdirectory of the timestamped folder under the `result` folder
* [2] iteration number during the training
* [3] learning rate during the training

Please run firstly the python script `launch\_aggregation\_term_evaluation.py` without argument and then read the specific explanation of these arguments which appears next. Default arguments are available as examples but you can take them if you've checked their values. Then run it again with arguments and check the results in the folder `results`.


## Step 3: perform the aggregation of model on the word similarity task
The arguments for this script are:
* [1] sample data path (pairs and their human-evaluated similarities)
* [2] directory where all the models locate
* [3] use or not the existing sample matrix generated by previous launching
* [4] prefix of the result file name
* [5] iteration number during the training
* [6] learning rate during the 
* [7] dimensions in the hidden layer

Please run firstly the python script `launch\_aggregation\_word_similarity.py` without argument and then read the specific explanation of these arguments which appears next. Default arguments are provided to give examples about the form. Then run it again with arguments and check the results in the folder `results`.

## Step 4: perform the terms clustering task
The arguments for this script are:
* [1] sample data path (one term and its frequency per line and separated by comma)
* [2] directory where all the models locate (where the folders `tscca phca ...` locate)
* [3] number of centers
* [4] max iterations in the K means clustering procedure
* [5] prefix of the result folder name

Please run firstly the python script `launch\_terms_clustering.py` without argument and then read the specific explanation of these arguments which appears next. Default arguments are provided to give examples about the form. Then run it again with arguments and check the results in the folder `results`.

End of the documentation. If there is any problem, please contact me (jie.he@mines-ales.org).
