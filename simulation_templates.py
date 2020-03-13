'''Constants and functions to set up and run a simulation of Worlds and Diseases

'''
import networkx as nx
from numpy import random as rnd

from graph_growth_classes import Person, World, Disease

#
# Template disease parameter sets
DISEASES = {}
DISEASES['Virus Y Baseline'] = \
                         {'transmission_base_prob' : 1.0/80.0,
                          'activate_mean' : 3.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 8.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 13.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 0.01,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y High Base Transmitter'] = \
                         {'transmission_base_prob' : 1.0/40.0,
                          'activate_mean' : 3.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 8.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 13.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 1.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y Early Revealer'] = \
                         {'transmission_base_prob' : 1.0/80.0,
                          'activate_mean' : 3.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 6.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 13.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 1.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y Late Revealer'] = \
                         {'transmission_base_prob' : 1.0/80.0,
                          'activate_mean' : 3.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 10.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 13.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 1.0,
                          'immunization_prob' : 1.00}

#
# Template world parameter sets
WORLDS = {}
WORLDS['Complete Mix'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.complete_graph}}
WORLDS['Complete Mix Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.complete_graph}}
WORLDS['Small World Beta 0'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.0,
                                                             'seed' : 42}}}
WORLDS['Small World Beta 0 Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.0,
                                                             'seed' : 42}}}
WORLDS['Small World Beta 1p'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
WORLDS['Small World Beta 1p Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
WORLDS['Small World Beta 10p'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.1,
                                                             'seed' : 42}}}
WORLDS['Small World Beta 10p Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.1,
                                                             'seed' : 42}}}
WORLDS['Relaxed Caveman'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.relaxed_caveman_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
WORLDS['Relaxed Caveman Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}

def make_persons(n_people, n_infect_init=1):
    '''Create persons to simulate and infected subset

    '''
    people = [Person('Person {}'.format(k)) for k in range(n_people)]
    for k_infect in rnd.randint(0, n_people, n_infect_init):
        people[k_infect].infect()

    return people

def make_edge_weights(graph, n_avg_meet):
    '''Compute weights for graph

    '''
    n_edges = graph.size()
    n_nodes = len(graph)
    f_weight = 0.5 * float(n_avg_meet) * n_nodes / n_edges
    if f_weight > 1.0:
        raise ValueError('Too great weight: {}. Reduce average meetings or increase density of edges'.format(f_weight))
    nx.set_edge_attributes(graph, f_weight, 'weight')

    return graph

def create_population(n_people, n_infect_init, n_avg_meet,
                      social_graph_creator = None,
                      social_graph_creator_kwargs = {}):
    '''Create population of people in a social graph

    '''
    people = make_persons(n_people, n_infect_init)

    if not callable(social_graph_creator):
        raise ValueError('Social graph creator required to be executable')

    social_graph = social_graph_creator(n_people, **social_graph_creator_kwargs)
    social_graph = nx.relabel_nodes(social_graph, dict([(k, p) for k, p in enumerate(people)]))

    social_graph = make_edge_weights(social_graph, n_avg_meet)

    return social_graph

def simulation(disease_name, world_name, n_days_max, report_interval, out_file_name):
    '''Set up world and disease and run the simulation for a set number of days or until
    no infections remain

    '''
    viral_disease = Disease(name=disease_name,
                            transmit_trajectory_file='{}_traj.csv'.format(out_file_name),
                            **DISEASES[disease_name])

    w_params = WORLDS[world_name]
    social_graph = create_population(**w_params['social_graph'])
    the_world = World(name=world_name,
                      social_graph=social_graph,
                      quarantine_policy=w_params['quarantine_policy'])
    nx.write_gml(nx.convert_node_labels_to_integers(social_graph), '{}_social_graph.gml'.format(out_file_name))

    # Simulation metadata
    with open(out_file_name + '_sim_data.csv', 'w') as fout:
        print ('World Name, {}'.format(world_name), file=fout)
        print ('Number of Persons, {}'.format(w_params['social_graph']['n_people']), file=fout)
        print ('Number of Initially Infected Persons, {}'.format(w_params['social_graph']['n_infect_init']), file=fout)
        print ('Number of Average Daily Meetings Per Person, {}'.format(w_params['social_graph']['n_avg_meet']), file=fout)
        print ('Graph Generator, {}'.format(w_params['social_graph']['social_graph_creator']), file=fout)
        if 'social_graph_creator_kwargs' in w_params['social_graph']:
            for key, value in w_params['social_graph']['social_graph_creator_kwargs'].items():
                print ('Generator Argument {}, {}'.format(key, value), file=fout)

        print ('Disease Name, {}'.format(disease_name), file=fout)
        for key, value in DISEASES[disease_name].items():
            print('Disease Argument {}, {}'.format(key, value), file=fout)

    # Run the simulation
    open(out_file_name + '_data.csv', 'w').close()
    for k_day in range(n_days_max):

        print ('Simulate Day: {}'.format(k_day + 1))

        viral_disease.progress_one_more_day(the_world)
        if k_day % report_interval == 0:
            df_report = the_world.report()
            with open(out_file_name + '_data.csv', 'a') as f:
                df_report.to_csv(f, mode='a', header=f.tell() == 0)

        if the_world.is_disease_free():
            break

if __name__ == '__main__':

    simulation('Virus Y Baseline', 'Complete Mix Q', 120, 1, 'test0')
    simulation('Virus Y Baseline', 'Relaxed Caveman', 120, 1, 'test1')
    simulation('Virus Y Baseline', 'Small World Beta 1p', 120, 1, 'test2')
