#!/bin/bash

FILTER='fragrance\|smell\|aroma\|aura\|balm\|bouquet\|essence\|fragrance\|incense\|odorize\|perfume\|pheromone\|redolence\|whiff\|stench\|stink\|deodorize\|doggy\|lemon\|lemony\|lilac\|lime\|mildewed\|mint\|minty\|moldy\|pine\|plastic\|rose\|skunky\|woodsy\|acid\|acrid\|airy\|biting\|clean\|crisp\|dirty\|earthy\|faint\|feminine\|fetid\|fishy\|fresh\|floral\|flowery\|light\|loamy\|masculine\|moist\|musty\|nauseating\|perfumed\|pungent\|putrid\|rancid\|redolent\|repulsive\|rotten\|sharp\|sour\|spicy\|spoiled\|stale\|stinking\|sweaty\|sweet\|tart\|wispy\|taste\|tastes\|odor\|odour\|flavour\|flavor\|osmyl'



echo -e "The filter is:\n\t"$FILTER
 
grep -w "$FILTER" ./original_corpus/corpus_clean.txt > $1

exit
