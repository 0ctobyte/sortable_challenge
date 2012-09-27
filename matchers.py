from fuzzstr import jaro_winkler
import re

MATCH_THRESHOLD = 0.90
MATCH_THRESHOLD_FUZZY = 0.96

# PARTIAL_RATIO:
# ratios = []
# i = title.find(model[0])
# while i != -1:
# 	ratios.append(jaro_winkle(model, title[i: i+len(model)]))
# 	i = title[i+1:].find(model[0])
# max(ratios)

def match1(product, listing):
	title = ''.join(re.split(r'\W+|_', listing['title'].lower()))
	product_name = ''.join(re.split(r'\W+|_', product['product_name'].lower()))

	if title.find(''.join(re.split(r'\W+|_', product['model'].lower()))) == -1:
		return False

	# Do the jaro-winkler! Sounds like a sweet dance move!
	score = jaro_winkler.distance(title[:len(product_name)], product_name)

	return True if score >= 0.92 else False
	
def match2(product, listing):
	title = ''.join(re.split(r'\W+|_', listing['title'].lower()))
	product_name = ''.join(re.split(r'\W+|_', product['product_name'].lower()))
	
	score = 0.0
	
	try:
		family = ''.join(re.split(r'\W+|_', product['family'].lower()))
		if title.find(family) == -1:
			return False
	except KeyError:
		pass

	model = ''.join(re.split(r'\W+|_', product['model'].lower()))
	if title.find(model) == -1:
		return False

	# Do the jaro-winkler! Sounds like a sweet dance move!
	score += jaro_winkler.distance(title[:len(product_name)], product_name)

	return True if score >= 0.92 else False

def match(product, listing):
	title = listing['title'].lower()
	product_name = ''.join(re.split(r'\W+|_', product['product_name'].lower()))
	
	try:
		family = ''.join(re.split(r'\W+|_', product['family'].lower()))
		if title.find(family) == -1:
			return False
	except KeyError:
		pass
	
	title_list = [''.join(re.split(r'\W+|_', x)) for x in title.split()]
	title_no_syms = ''.join(title_list)
	
	score = 0.0
	
	# Do the jaro-winkler! Sounds like a sweet dance move!
	score += jaro_winkler.distance(title_no_syms[:len(product_name)], product_name)

	model = ''.join(re.split(r'\W+|_', product['model'].lower()))
	if re.search(r'\b%s\b' % model, ' '.join(title_list)) is not None:
		score += 1

	return True if score/2.0 >= 0.92 else False
