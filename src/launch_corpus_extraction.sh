#! /bin/bash


if [ -z "$3" ]; then
	echo "

	A shell to extract the specific sentences or paragrahs from wiki dump html file. Please run this shell with following parameters:

		[1] path of the original downloaded dump file of wikipedia (compressed format)
		put 0 to download the latest enwiki dump online

		[2] path of the result file (clean text, one sentence per line, lowercased, punctuations removed and digits replaced with 0s)

		[3] extract by sentence or by paragraph
		put 0 to extract sentences, put 1 to extract paragraphs

		* Please note that the setting of key words in the filter is available in this script but can not be setted by argument. Please find the line which starts with the variable name FILTER to change the filter words. The backslash and pipe should be kept between two words.

	Version 0.1 by Jie He @LGI2P, EMA

	"
	exit
fi

FILTER='fragrance\|smell\|aroma\|aura\|balm\|bouquet\|essence\|fragrance\|incense\|odorize\|perfume\|pheromone\|redolence\|whiff\|stench\|stink\|deodorize\|doggy\|lemon\|lemony\|lilac\|lime\|mildewed\|mint\|minty\|moldy\|pine\|plastic\|rose\|skunky\|woodsy\|acid\|acrid\|airy\|biting\|clean\|crisp\|dirty\|earthy\|faint\|feminine\|fetid\|fishy\|fresh\|floral\|flowery\|light\|loamy\|masculine\|moist\|musty\|nauseating\|perfumed\|pungent\|putrid\|rancid\|redolent\|repulsive\|rotten\|sharp\|sour\|spicy\|spoiled\|stale\|stinking\|sweaty\|sweet\|tart\|wispy\|taste\|tastes\|odor\|odour\|flavour\|flavor\|osmyl'



init=$1
mid0=pages.xml
mid1=corpus_markupRe.txt
mid1_extra=corpus_markupRe_extra.txt
mid2=corpus_markupRm_spl.txt
mid3=corpus_markupRm_spl_tokenized.txt
mid4=corpus_markupRm_spl_tokenized_punctRm.txt
mid5=corpus_markupRm_spl_tokenized_punctRm_ln.txt
final=$2


echo "Extract the compressed dump file to xml file >>>" 
if [ $1 == 0 ]; then
	wget http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
	python tools_extraction/WikiExtractor.py -cb 250M -o extracted enwiki-latest-pages-articles.xml.bz2
else
	python tools_extraction/WikiExtractor.py -cb 250M -o extracted $init
fi

echo "Concatenate the whole extracted files >>>"
find extracted -name '*bz2' -exec bunzip2 -c {} \; > $mid0
rm -rf extracted

echo "Remove tags in xml file >>>"
sed -e 's/<[^>]*>//g' $mid0 > $mid1
rm $mid0

if [ $3 == 0 ]; then
	echo "Detect sentences (One sentence per line) >>>"
	python tools_extraction/sentenceDetector.py $mid1 $mid2
 	rm $mid1

	echo "Tokenize sentences (separate each token by space) >>>"
	java -cp tools_extraction/stanford-corenlp.jar edu.stanford.nlp.process.PTBTokenizer -preserveLines $mid2 >  $mid3
 	rm $mid2

	echo "Remove punctuations >>>"
	cat $mid3 | tr -d '[:punct:]' > $mid4
 	rm $mid3

	echo "Lowercase words and replace digits with 0s >>>"
	./tools_extraction/preprocess -input-file $mid4 -output-file $mid5 -lower 1 -digit 1 -verbose 1 -threads 8 -gzip 0
 	rm $mid4

	echo "Apply the filter >>>"
	echo -e "The filter is:\n\t"$FILTER
	grep -w "$FILTER"  $mid5 > $final 
 	rm $mid5
fi


if [ $3 == 1 ]; then

	echo "Apply the filter >>>"
	echo -e "The filter is:\n\t"$FILTER
	grep -w "$FILTER"  $mid1 > $mid1_extra 
 	#rm $mid1

	echo "Detect sentences (One sentence per line) >>>"
	python tools_extraction/sentenceDetector.py $mid1_extra $mid2
 	#rm $mid1_extra

	echo "Tokenize sentences >>>"
	java -cp tools_extraction/stanford-corenlp.jar edu.stanford.nlp.process.PTBTokenizer -preserveLines $mid2 >  $mid3
 	#rm $mid2

	echo "Remove punctuations >>>"
	cat $mid3 | tr -d '[:punct:]' > $mid4
 	#rm $mid3

	echo "Lowercase words and replace digits with 0s >>>"
	./tools_extraction/preprocess -input-file $mid4 -output-file $mid5 -lower 1 -digit 1 -verbose 1 -threads 8 -gzip 0
 #rm $mid4

	
fi

exit



