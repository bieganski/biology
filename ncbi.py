#!/usr/bin/env python3

import xmltodict


from Bio import Entrez, SeqIO

Entrez.email = 'niemetin@wp.pl' # provide your email address

entries = open("entries_ncbi").readlines()
entries = list(map(str.strip, entries))
entries = list(filter(lambda x : x != "", entries))

pd = lambda x : print(dir(x))
p = print

from tqdm import tqdm

for e in tqdm(entries):
    # id="145283705"
    handle = Entrez.efetch(db="protein", id=e, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()

    _tax = record.annotations['taxonomy']
    tax = ""
    for s in _tax:
        tax += s
        tax += " "
    tax.strip()
    org = record.annotations['organism']

    print(f"==== {e}:\n{org}\n{tax}")


exit(0)

# initialize some default parameters
Entrez.email = 'niemetin@wp.pl' # provide your email address
db = 'protein'
paramEutils = { 'usehistory':'Y' }

# generate query to Entrez eSearch
# eSearch = Entrez.esearch(db=db, term="ABP51287.1", **paramEutils)
eSearch = Entrez.esearch(db=db, term="145283705", **paramEutils)
# a = eSearch.read()
# print(dir(eSearch))
# print(a)

# get eSearch result as dict object
res = Entrez.read(eSearch)


paramEutils['WebEnv'] = res['WebEnv']         #add WebEnv and query_key to eUtils parameters to request esummary using  
paramEutils['query_key'] = res['QueryKey']    #search history (cache results) instead of using IdList 
paramEutils['rettype'] = 'xml'                #get report as xml
paramEutils['retstart'] = 0                   #get result starting at 0, top of IdList
paramEutils['retmax'] = 10                     #get next five results


# take a peek of what's in the result (ie. WebEnv, Count, etc.)
for k in res:
    print (k, "=",  res[k])

result = Entrez.esummary(db=db, **paramEutils)

xml = result.read()
# take a peek at xml
print(xml)

dsdocs = xmltodict.parse(xml)

#get set of dbVar DocumentSummary (dsdocs) and print report for each (ds)


from pprint import pprint
pprint(dsdocs)

# print(dsdocs ['eSummaryResult'].values())
# for ds in dsdocs ['eSummaryResult']['DocumentSummarySet']['DocumentSummary']: 
#     for p in ds['dbVarPlacementList']['dbVarPlacement']: 
#         print (ds['@uid'], ds['ST'], ds['SV'],p['Chr'], p['Chr_start'], p['Chr_end'], p['Chr_inner_start'], p['Chr_inner_end'])
