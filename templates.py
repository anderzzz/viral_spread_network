import pandas as pd
import networkx as nx

from viral_classes import Person, World, Disease

#
# Simple test
#
pp1 = Person('Arnold')
pp1.infect()
pp2 = Person('Lars')
pp3 = Person('Sven')
pp4 = Person('Per')

gg = nx.Graph()
gg.add_node(pp1)
gg.add_node(pp2)
gg.add_node(pp3)
gg.add_node(pp4)
gg.add_edge(pp1, pp2, weight=0.5)
gg.add_edge(pp2, pp3, weight=0.5)
gg.add_edge(pp1, pp4, weight=0.1)

the_world = World('simple test', gg, quarantine_policy='symptomatic')

viral_disease = Disease('contact disease',
                        transmission_base_prob=0.5,
                        activate_mean=4, activate_spread=0.1,
                        reveal_mean=11, reveal_spread=1,
                        survive_mean=24, survive_spread=2,
                        succumb_mean=26, succumb_spread=2,
                        immunization_prob=0.75)

sim_data = []
for k_day in range(30):
    viral_disease.progress_one_more_day(the_world)
    sim_data.append(the_world.report())

df = pd.concat(sim_data)

print (df[:,:,'expectation_meetings_per_day'])
