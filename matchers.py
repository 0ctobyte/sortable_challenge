from jaro_winkler.jaro_winkler import *
import re

MATCH_THRESHOLD = 0.90
MATCH_THRESHOLD_FUZZY = 0.96

def find_str_in_list(s, strings):
	for index in range(0, len(strings)):
		if strings[index] == s:
			return index
	else:
		return -1

def match(product, listing):
	if listing['manufacturer'].lower().find(
		product['manufacturer'].lower()) == -1:
		return False

	product_name = ''.join(re.split(r'\W+|_', product['product_name'].lower()))

	title_no_syms = ''.join(re.split(r'\W+|_', listing['title'].lower()))
	title_split = listing['title'].lower().split()
	title_list_no_syms = [''.join(re.split(r'\W+|_', x)) for x in title_split]

	model = ''.join(re.split(r'\W+|_', product['model'].lower()))
	if find_str_in_list(model, title_list_no_syms) == -1:
		return False

	divide = 2.0
	score = 0.0
	try:
		family = ''.join(re.split(r'\W+|_', product['family'].lower()))
		if find_str_in_list(family, title_list_no_syms) != -1:
			score += 1.0
	except KeyError:
		divide = 1.0
		score = 0.0

	# Do the jaro-winkler! Sounds like a sweet dance move!
	score += jaro_winkler(title_no_syms[:len(product_name)], product_name)

	return True if score/divide >= 0.92 else False
