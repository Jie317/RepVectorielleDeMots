## The whole project consists of three parts:
* 1) the computation of the five vector representations (word embeddings) and the evaluation of the models
* 2) the aggregation of model on the term evaluation task
* 3) the aggregation of model on the word similarity task


##To install the whole project and reproduce all the results, please follow the 4 steps below:

###Please note that all the scripts mentioned below are in the folder "src", and whenever giving a directory as an argument please end it with a slash "/", such as "./input_corpora/corpora/".

## Step 1 check system environment and install dependencies
The whole project is developed on Ubuntu 16.04 LTS (64-bit, Kernel: 4.7.1) and Python 2.7.12. Other versions of Ubuntu should work with this project.

To build the project environmemt, firstly run "setup.sh" with root to install all the dependencies and packages. Then extract "tools.tar.gz" in the "src" folder.


## Step 2 perform the computation and evaluation of models
Please run the python script "launch\_computation\_and\_evaluation.py" and then read the explanation of arguments which appears next. The arguments for this script are:

* [1] directory where the corpora locate (One sentence per line)
* [2] directory of the input corpus
* [3] choice of embeddings to compute or directly using existing embeddings
* [4] Input terms/descriptors path
* [5] Prefix of the result directory name

Then run it again with arguments.

* Please note that for the computation of the model TSCCA, the settings are in the buil.xml file in the current folder. All the computations of embeddings have taken the default settings.


## Step 3 perform the aggregation of model on the term evaluation task
Please run the python script "launch\_aggregation\_term\_evaluation.py" and read the explanation of arguments which appears next. 


## Step 4 perform the aggregation of model on the word similarity task
Please run the python script "launch_aggregation_word_similarity.py" and read the explanation of arguments which appears next. 

## Step 5 check the results
All the result files are stored in the folder "results/" in the root directory of the project. For each launching, there will be an independent folder whose name is marked with uique time label (a conbination of the time in the beginning and the time in the end). 



If there is any problem, please contact me (jie.he@mines-ales.org)
