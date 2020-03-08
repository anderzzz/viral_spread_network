import pandas as pd
import networkx as nx
from numpy import random as rnd

from viral_classes import Person, World, Disease

# Disease constants
DISEASES = {}
DISEASES['Virus X_01'] = {'transmission_base_prob' : 0.25,
                          'activate_mean' : 4.0,
                          'activate_spread' : 2.0,
                          'reveal_mean' : 8.0,
                          'reveal_spread' : 2.0,
                          'survive_mean' : 20.0,
                          'survive_spread' : 3.0,
                          'succumb_mean' : 22.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}

# World constants
WORLDS = {}
WORLDS['World W_01'] = {'quarantine_policy' : 'revealed',
                        'persons_network_func' : 'population_well_mixed',
                        'persons_network_kwargs' : {'n_people' : 5,
                                                    'n_infect_init' : 1,
                                                    'n_avg_meet' : 2}}

# Social network creation methods
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

    return gg

def simulation(disease_name, world_name, n_days_max, report_interval, out_file_name):

    # Instantiate disease and world
    viral_disease = Disease(name=disease_name, **DISEASES[disease_name])
    social_graph = eval(WORLDS[world_name]['persons_network_func'])(**WORLDS[world_name]['persons_network_kwargs'])
    the_world = World(name=world_name,
                      persons_network=social_graph,
                      quarantine_policy=WORLDS[world_name]['quarantine_policy'])

    # Output simulation metadata
    with open(out_file_name + '_sim_data.csv', 'w') as f:
        f.write('World Name, {}\n'.format(world_name))
        f.write('Social Graph Method, {}\n'.format(WORLDS[world_name]['persons_network_func']))
        for key, value in WORLDS[world_name]['persons_network_kwargs'].items():
            f.write('{}, {}\n'.format(key, value))
        f.write('Disease Name, {}\n'.format(disease_name))
        for key, value in DISEASES[disease_name].items():
            f.write('{}, {}\n'.format(key, value))

    # Run the simulation
    for k_day in range(n_days_max):

        print ('Simulate Day: {}'.format(k_day))

        viral_disease.progress_one_more_day(the_world)
        if k_day % report_interval == 0:
            df_report = the_world.report()
            with open(out_file_name + '_data.csv', 'a') as f:
                df_report.to_csv(f, mode='a', header=f.tell() == 0)

        if the_world.is_disease_free():
            break

if __name__ == '__main__':

    simulation('Virus X_01', 'World W_01', 100, 1, 'test_run')
