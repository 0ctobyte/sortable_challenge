from jaro_winkler.jaro_winkler import *
import re

MATCH_THRESHOLD = 0.90
MATCH_THRESHOLD_FUZZY = 0.96

def match(product, listing):
	if listing['manufacturer'].lower().find(
		product['manufacturer'].lower()) == -1:
		return False

	title = ''.join(re.split(r'\W+|_', listing['title'].lower()))
	product_name = ''.join(re.split(r'\W+|_', product['product_name'].lower()))

	if title.find(''.join(re.split(r'\W+|_', product['model'].lower()))) == -1:
		return False

	# Do the jaro-winkler! Sounds like a sweet dance move!
	score = jaro_winkler(title[:len(product_name)], product_name)

	return True if score >= 0.92 else False
