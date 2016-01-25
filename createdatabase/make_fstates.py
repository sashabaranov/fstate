from operator import mul
from copy import deepcopy
from datetime import datetime
from multiprocessing import Pool, cpu_count

from weight_split import get_jobs
from database import *

import pickle

db = {}

with open('../decaydecparser/parsed_decays.pkl', 'r') as basket:
    test_set = pickle.load(basket)

for father in test_set['decays']:
    if not father in db:
            db[father] = []

    for d in test_set['decays'][father]:
        if d['braching'] < 1E-30:
            continue    
        if d['braching'] >= 1:
            continue    
        db[father].append({
            'branching': d['braching'],
            'father': father,
            'products': d['daughters']
        })


def do_work(fathers):
    for father in fathers:
        start = datetime.now()

        for decay in db[father]:
            work_copy = deepcopy(decay)
            work_copy['history'] = "{} --> {}".format(
                father, ' '.join(decay['products']))

            get_fstates(work_copy)

        end = datetime.now()

        print "{}\t{}".format(father, end-start)


if __name__ == "__main__":
    from fstate import get_fstates

    fstates.drop()
    fstates.create_index("fstate")
    fstates.create_index("scheme", unique=True)


    #do_work(test_set['decays'].keys())

    print "DB build started on {}.".format(datetime.now())

    start = datetime.now()

    workers  = cpu_count()
    p = Pool(processes=workers)
    p.map(do_work, get_jobs(workers))


    end = datetime.now()

    print "Took {} to build!".format(end - start)
