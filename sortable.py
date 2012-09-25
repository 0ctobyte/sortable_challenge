import json, sys
from datetime import datetime
from matchers import *

print str(datetime.now())

products_f, listings_f = 'products.txt', 'listings.txt'
results_f = 'results.txt'

# This script will take products and listings files specified in the command
# line
if len(sys.argv) >= 3:
	products_f, listings_f = sys.argv[1], sys.argv[2]

# Load products into an array of dicts
products = []
with open(products_f, 'r') as file:
	for line in file:
		products.append(json.loads(line))

# Load listings into an array of dicts
listings = []
with open(listings_f, 'r') as file:
	for line in file:
		listings.append(json.loads(line))

print '# of products: ' + str(len(products))
print '# of listings: ' + str(len(listings))

results = []

print 'Matching (This may take a while)'

# Now we match products to listings
for product in products:
	results.append({'product_name': product['product_name'], 'listings': []})

	# Here we remove listings that have been matched to a product, thus
	# the listings list becomes smaller as more listings get matched.
	# Why listings[:] instead of just listings? To modify the list in place
	# instead of creating a new reference of course!
	listings[:] = [listing for listing in listings 
		if not (match_det1(product, listing) and add_result(results[len(results)-1:][0], listing))]

	# Some very cool effects so the user knows the program is still alive
	sys.stdout.write('.')

print '\nMatch2'
print '# of listings: ' + str(len(listings))

i = 0
for product in products:
	listings[:] = [listing for listing in listings 
		if not (match_det2(product, listing) and add_result(results[i], listing))]
	sys.stdout.write('.')
	i += 1
	
print '\nMatch3'
print '# of listings: ' + str(len(listings))

i = 0
for product in products:
	listings[:] = [listing for listing in listings 
		if not (match_fuzzy(product, listing) and add_result(results[i], listing))]
	sys.stdout.write('.')
	i += 1

print '\nMatching complete!'
print '# of leftover listings: ' + str(len(listings))

# Write the results to a file, one result per line
# Remove the commas!
with open(results_f, 'w') as file:
	for result in results:
		file.write(json.dumps(result) + ',\n')

# Write the leftover listings to a file
with open('leftovers.txt', 'w') as file:
	for listing in listings:
		file.write(json.dumps(listing) + ',\n')

print str(datetime.now())