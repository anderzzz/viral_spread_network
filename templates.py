import pandas as pd
import networkx as nx
from numpy import random as rnd

from viral_classes import Person, World, Disease

def population_well_mixed(n_people, n_infect_init, n_avg_meet):

    # Generate people in population and seed with a few infected ones
    people = [Person('A Name {}'.format(k)) for k in range(n_people)]
    rnd_inds = rnd.randint(0, n_people, n_infect_init)
    for k_infect in rnd_inds:
        people[k_infect].infect()

    # Disperse population in a social network
    gg = nx.complete_graph(n_people)
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))

    # Put weight on social connections
    f_weight = float(n_avg_meet) / float(n_people)
    nx.set_edge_attributes(gg, f_weight, 'weight')

    print (gg)

    return gg

viral_disease_1 = Disease('viral X',
                          transmission_base_prob=0.1,
                          activate_mean=4, activate_spread=2,
                          reveal_mean=8, reveal_spread=2,
                          survive_mean=20, survive_spread=3,
                          succumb_mean=22, succumb_spread=3,
                          immunization_prob=1.00)

gg = population_well_mixed(5000, 1, 10)
the_world = World('simple test', gg, quarantine_policy=None)

sim_data = []
for k_day in range(100):
    print (k_day)
    viral_disease_1.progress_one_more_day(the_world)
    sim_data.append(the_world.report())
    if the_world.is_disease_free():
        break

df = pd.DataFrame(pd.concat(sim_data), columns=['value'])
df.to_csv('dummy3.csv')
