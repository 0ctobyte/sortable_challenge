from fuzzstr import jaro_winkler, fuzzstr
import re

MATCH_THRESHOLD = 0.90
MATCH_THRESHOLD_FUZZY = 0.96

def match(product, listing):
	score = 0.0
	
	try:
		family = product['family'].lower()
		score += fuzzstr.partial_match(family, title)
	except KeyError:
		return False

	title = listing['title'].lower()
	product_name = ' '.join(product['product_name'].lower().split('_'))

	model = product['model'].lower()
	score += fuzzstr.partial_match(model, title)
	
	score += fuzzstr.intersect_match(product_name, title)
	
	return True if score/3.0 > 0.96 else False
	
def match1(product, listing):
	score = 0.0
	title = ''.join(re.split(r'\W+|_', listing['title'].lower()))
	product_name = ''.join(re.split(r'\W+|_', product['product_name'].lower()))

	if title.find(''.join(re.split(r'\W+|_', product['model'].lower()))) == -1:
		return False

	score += fuzzstr.intersect_match(' '.join(product['product_name'].lower.split('_')), listing['title'].lower())

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

	score += fuzzstr.intersect_match(' '.join(product['product_name'].lower.split('_')), listing['title'].lower())

	return True if score >= 0.92 else False

def match3(product, listing):
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
	
	score += fuzzstr.intersect_match(' '.join(product['product_name'].lower.split('_')), listing['title'].lower())

	model = ''.join(re.split(r'\W+|_', product['model'].lower()))
	if re.search(r'\b%s\b' % model, ' '.join(title_list)) is not None:
		score += 1

	return True if score/2.0 >= 0.92 else False
