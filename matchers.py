import jaro_winkler.jaro_winkler as jw
import re

MATCH_THRESHOLD = 0.90
MATCH_THRESHOLD_FUZZY = 0.96

def add_result(result, listing):
	result['listings'].append(listing)
	return True

def match_find(title_list, product_attr_list):
	matches = 0
	for item1 in product_attr_list:
		for item2 in title_list:
			if item1.lower() == item2.lower():
				matches += 1
				break
	return (float(matches)/len(product_attr_list))
	
def match_jaro(title_list, product_attr_list):
	matches = 0
	for str1 in product_attr_list:
		distances = []
		for str2 in title_list:
			distances.append(jw.jaro_winklerize_this(str1, str2))
		matches += max(distances)
	return (float(matches)/len(product_attr_list))

def match_det1(product, listing):
	if listing['manufacturer'].find(product['manufacturer']) == -1:
		return False
	
	title_list = listing['title'].lower().split()
	product_attr_list = product['product_name'].lower().split('_')
	
	match_sum = match_find(title_list, product_attr_list)
	
	return True if match_sum >= MATCH_THRESHOLD else False

def match_det2(product, listing):
	if listing['manufacturer'].find(product['manufacturer']) == -1:
		return False
	
	title_list = listing['title'].lower().split()
	product_attr_list = []	
	try:
		product_attr_list.append(''.join(re.split(r'\W+|_', product['manufacturer'].lower())))
		product_attr_list.append(''.join(re.split(r'\W+|_', product['model'].lower())))
		product_attr_list.append(''.join(re.split(r'\W+|_', product['family'].lower())))
	except KeyError:
		return False
	
	match_sum = match_find(title_list, product_attr_list)

	return True if match_sum >= MATCH_THRESHOLD else False

def match_fuzzy(product, listing):
	if listing['manufacturer'].find(product['manufacturer']) == -1:
		return False
	
	title_list = listing['title'].lower().split()
	title = ''.join([''.join(re.split(r'\W+|_', x)) for x in title_list])
	product_name = ''.join(re.split(r'\W+|_', product['product_name']))
	product_attr_list = []	
	try:
		product_attr_list.append(product['manufacturer'].lower())
		product_attr_list.append(product['model'].lower())
		product_attr_list.append(product['family'].lower())
	except KeyError:
		return False
	
	match_sum = jw.jaro_winklerize_this(product_name, title)
	match_sum += match_jaro(title_list, product_attr_list)
		
	return True if match_sum/2.0 >= MATCH_THRESHOLD_FUZZY else False 