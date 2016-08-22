 #! usr/bin/bash
 
 if [ -z "$1" ]; then
 	echo "A shell to extract the specific sentences or paragrahs from wiki dump html file. Please run this shell with following parameters:
 
 	[1] path of the original dump file of wikipedia
 	[2] path of the result file ()
 	[3] extract by sentence or by paragraph?
 	put 0 to extract sentences, put 1 to extract paragraphs
 	
 	* Please note that the parameters of filter are available in the following line which starts with the variable FILTER. The bacslash and pipe should be kept between two words.
 "
 	exit
 fi
 
 FILTER='fragrance\|smell\|aroma\|aura\|balm\|bouquet\|essence\|fragrance\|incense\|odorize\|perfume\|pheromone\|redolence\|whiff\|stench\|stink\|deodorize\|doggy\|lemon\|lemony\|lilac\|lime\|mildewed\|mint\|minty\|moldy\|pine\|plastic\|rose\|skunky\|woodsy\|acid\|acrid\|airy\|biting\|clean\|crisp\|dirty\|earthy\|faint\|feminine\|fetid\|fishy\|fresh\|floral\|flowery\|light\|loamy\|masculine\|moist\|musty\|nauseating\|perfumed\|pungent\|putrid\|rancid\|redolent\|repulsive\|rotten\|sharp\|sour\|spicy\|spoiled\|stale\|stinking\|sweaty\|sweet\|tart\|wispy\|taste\|tastes\|odor\|odour\|flavour\|flavor\|osmyl'
 

 
 init=$1
 mid1=corpus_markupRe.txt
 mid2=corpus_markupRm_spl.txt
 mid3=corpus_markupRm_spl_tokenized.txt
 mid4=corpus_markupRm_spl_tokenized_punct_Rm.txt
 mid5=corpus_markupRm_spl_tokenized_punct_Rm_ln.txt
 final=$2
 
 
 echo "Extract the compressed dump file >>>" 
 python tools_extraction/WikiExtractor.py -cb 250K -o extracted $init
 
 echo "Remove tags in xml file >>>"
 sed -e 's/<[^>]*>//g' $init > $mid1
 
 if [ $3 -eq 0 ]; then
 	echo "Detect sentences (One sentence per line) >>>"
 	python tools_extraction/sentenceDetector.py $mid1 $mid2
 	rm $mid1
 	
 	echo "Tokenize sentences >>>"
 	java -cp tools_extraction/stanford-corenlp.jar edu.stanford.nlp.process.PTBTokenizer -preserveLines $mid2 >  $mid3
 	rm $mid2
 	
 	echo "Remove punctuations >>>"
 	cat $mid3 | tr -d '[:punct:]' > $mid4
 	rm $mid3
 	
 	echo "Lowcase words replace numbers with 0s >>>"
 	./tools_extraction/preprocess -input-file $mid4 -output-file $mid5 -lower 1 -digit 1 -verbose 1 -threads 8 -gzip 0
 	rm $mid4
 	
 	echo "Apply the filter >>>"
	echo -e "The filter is:\n\t"$FILTER
	grep -w "$FILTER"  $mid5 > $final 
	rm $mid5
fi



exit



