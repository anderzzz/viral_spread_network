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
DISEASES['Virus Y Delayed Recovery'] = \
                         {'transmission_base_prob': 1.0 / 80.0,
                          'activate_mean': 3.0,
                          'activate_spread': 1.0,
                          'reveal_mean': 8.0,
                          'reveal_spread': 2.0,
                          'recover_mean': 16.0,
                          'recover_spread': 3.0,
                          'succumb_mean': 200.0,
                          'succumb_spread': 1.0,
                          'immunization_prob': 1.00}
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
#
# Complete mix graph, no reactive quarantine, no cautious behaviours
WORLDS['Complete Mix'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.complete_graph,
                            'social_graph_creator_kwargs': {'n': 1000}}}
#
# Complete mix graph, no reactive quarantine, 20% of people 50% more cautious
WORLDS['Complete Mix Cautious 50_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level' : 0.5,
                            'cautious_size' : 200,
                            'social_graph_creator': nx.complete_graph,
                            'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, no reactive quarantine, 10% of people 50% more cautious
WORLDS['Complete Mix Cautious 50_100'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level' : 0.5,
                      'cautious_size' : 100,
                      'social_graph_creator': nx.complete_graph,
                      'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, no reactive quarantine, 20% of people 25% more cautious
WORLDS['Complete Mix Cautious 25_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level' : 0.25,
                      'cautious_size' : 200,
                      'social_graph_creator': nx.complete_graph,
                      'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, no reactive quarantine, 10% of people 25% more cautious
WORLDS['Complete Mix Cautious 25_100'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level' : 0.25,
                      'cautious_size' : 100,
                      'social_graph_creator': nx.complete_graph,
                      'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, with reactive quarantine, no cautious behaviours
WORLDS['Complete Mix Q'] = \
    {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.complete_graph,
                            'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, with reactive quarantine, 20% of people 50% more cautious
WORLDS['Complete Mix Q Cautious 50_200'] = \
    {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level' : 0.5,
                            'cautious_size' : 200,
                            'social_graph_creator': nx.complete_graph,
                            'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, with reactive quarantine, 10% of people 50% more cautious
WORLDS['Complete Mix Q Cautious 50_100'] = \
    {'quarantine_policy' : 'revealed',
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level' : 0.5,
                      'cautious_size' : 100,
                      'social_graph_creator': nx.complete_graph,
                      'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, with reactive quarantine, 20% of people 25% more cautious
WORLDS['Complete Mix Q Cautious 25_200'] = \
    {'quarantine_policy' : 'revealed',
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level' : 0.25,
                      'cautious_size' : 200,
                      'social_graph_creator': nx.complete_graph,
                      'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, with reactive quarantine, 10% of people 25% more cautious
WORLDS['Complete Mix Q Cautious 25_100'] = \
    {'quarantine_policy' : 'revealed',
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level' : 0.25,
                      'cautious_size' : 100,
                      'social_graph_creator': nx.complete_graph,
                      'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Complete mix graph, with reactive quarantine, across the board 25% fewer meetings
WORLDS['Complete Mix Q 50p Less Meet'] = \
    {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 38,
                            'social_graph_creator': nx.complete_graph,
                            'social_graph_creator_kwargs' : {'n' : 1000}}}
#
# Ring lattice graph 100 neighbours, no reactive quarantine, no cautious behaviours
WORLDS['Small World Beta 0'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.0,
                                                             'seed' : 42}}}
#
# Ring lattice graph 100 neighbours, no reactive quarantine, 20% of people 50% more cautious
WORLDS['Small World Beta 0 Cautious 50_200'] = \
    {'quarantine_policy' : None,
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level': 0.5,
                      'cautious_size': 200,
                      'social_graph_creator': nx.connected_watts_strogatz_graph,
                      'social_graph_creator_kwargs' : {'k' : 100,
                                                       'n' : 1000,
                                                       'p' : 0.0,
                                                       'seed' : 42}}}
#
# Ring lattice graph 100 neighbours, no reactive quarantine, 10% of people 50% more cautious
WORLDS['Small World Beta 0 Cautious 50_100'] = \
    {'quarantine_policy' : None,
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level': 0.5,
                      'cautious_size': 100,
                      'social_graph_creator': nx.connected_watts_strogatz_graph,
                      'social_graph_creator_kwargs' : {'k' : 100,
                                                       'n' : 1000,
                                                       'p' : 0.0,
                                                       'seed' : 42}}}
#
# Ring lattice graph 100 neighbours, reactive quarantine, no cautious behaviours
WORLDS['Small World Beta 0 Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.0,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 1%, no reactive quarantine, no cautious behaviours
WORLDS['Small World Beta 1p'] = \
    {'quarantine_policy' : None,
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'social_graph_creator': nx.connected_watts_strogatz_graph,
                      'social_graph_creator_kwargs' : {'k' : 100,
                                                       'n' : 1000,
                                                       'p' : 0.01,
                                                       'seed' : 42}}}
#
# Small world graph 100 neighbours beta 1%, no reactive quarantine, 20% of people 50% more cautious
WORLDS['Small World Beta 1p Cautious 50_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.5,
                            'cautious_size': 200,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 1%, no reactive quarantine, 10% of people 50% more cautious
WORLDS['Small World Beta 1p Cautious 50_100'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.5,
                            'cautious_size': 100,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 1%, no reactive quarantine, 20% of people 25% more cautious
WORLDS['Small World Beta 1p Cautious 25_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.25,
                            'cautious_size': 200,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 1%, no reactive quarantine, 10% of people 25% more cautious
WORLDS['Small World Beta 1p Cautious 25_100'] = \
    {'quarantine_policy' : None,
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level': 0.25,
                      'cautious_size': 100,
                      'social_graph_creator': nx.connected_watts_strogatz_graph,
                      'social_graph_creator_kwargs' : {'k' : 100,
                                                       'n' : 1000,
                                                       'p' : 0.01,
                                                       'seed' : 42}}}
#
# Small world graph 100 neighbours beta 1%, with reactive quarantine, no cautious behaviour
WORLDS['Small World Beta 1p Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 10%, no reactive quarantine, no cautious behaviours
WORLDS['Small World Beta 10p'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.1,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 10%, with reactive quarantine, no cautious behaviours
WORLDS['Small World Beta 10p Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.1,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 10%, no reactive quarantine, 20% of people 50% more cautious
WORLDS['Small World Beta 10p Cautious 50_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.5,
                            'cautious_size': 200,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.1,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 10%, no reactive quarantine, 10% of people 50% more cautious
WORLDS['Small World Beta 10p Cautious 50_100'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.5,
                            'cautious_size': 100,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.1,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 10%, no reactive quarantine, 20% of people 25% more cautious
WORLDS['Small World Beta 10p Cautious 25_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.25,
                            'cautious_size': 200,
                            'social_graph_creator': nx.connected_watts_strogatz_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'n' : 1000,
                                                             'p' : 0.1,
                                                             'seed' : 42}}}
#
# Small world graph 100 neighbours beta 10%, no reactive quarantine, 10% of people 25% more cautious
WORLDS['Small World Beta 10p Cautious 25_100'] = \
    {'quarantine_policy' : None,
     'social_graph': {'n_people': 1000,
                      'n_infect_init': 5,
                      'n_avg_meet': 50,
                      'caution_level': 0.25,
                      'cautious_size': 100,
                      'social_graph_creator': nx.connected_watts_strogatz_graph,
                      'social_graph_creator_kwargs' : {'k' : 100,
                                                       'n' : 1000,
                                                       'p' : 0.1,
                                                       'seed' : 42}}}
#
# Relaxed caveman graph 10 cliques 100 nodes each 1% edge between cliques,
# no reactive quarantine, no cautious behaviours
WORLDS['Relaxed Caveman'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.relaxed_caveman_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'l' : 10,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Relaxed caveman graph 10 cliques 100 nodes each 1% edge between cliques,
# no reactive quarantine, 20% of people 50% more cautious
WORLDS['Relaxed Caveman Cautious 50_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.50,
                            'cautious_size': 200,
                            'social_graph_creator': nx.relaxed_caveman_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'l' : 10,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Relaxed caveman graph 10 cliques 100 nodes each 1% edge between cliques,
# no reactive quarantine, 10% of people 50% more cautious
WORLDS['Relaxed Caveman Cautious 50_100'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.50,
                            'cautious_size': 100,
                            'social_graph_creator': nx.relaxed_caveman_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'l' : 10,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Relaxed caveman graph 10 cliques 100 nodes each 1% edge between cliques,
# no reactive quarantine, 20% of people 25% more cautious
WORLDS['Relaxed Caveman Cautious 25_200'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.25,
                            'cautious_size': 200,
                            'social_graph_creator': nx.relaxed_caveman_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'l' : 10,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Relaxed caveman graph 10 cliques 100 nodes each 1% edge between cliques,
# no reactive quarantine, 10% of people 25% more cautious
WORLDS['Relaxed Caveman Cautious 25_100'] = \
          {'quarantine_policy' : None,
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'caution_level': 0.25,
                            'cautious_size': 100,
                            'social_graph_creator': nx.relaxed_caveman_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'l' : 10,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}
#
# Relaxed caveman graph 10 cliques 100 nodes each 1% edge between cliques,
# with reactive quarantine, no cautious behaviours
WORLDS['Relaxed Caveman Q'] = \
          {'quarantine_policy' : 'revealed',
           'social_graph': {'n_people': 1000,
                            'n_infect_init': 5,
                            'n_avg_meet': 50,
                            'social_graph_creator': nx.relaxed_caveman_graph,
                            'social_graph_creator_kwargs' : {'k' : 100,
                                                             'l' : 10,
                                                             'p' : 0.01,
                                                             'seed' : 42}}}

def make_persons(n_people, n_infect_init=1, caution_level=0.0, cautious_size=0):
    '''Create persons to simulate and infected subset

    '''
    if cautious_size > n_people:
        raise ValueError('Number of cautious persons must be less than total')

    people = [Person('Person {}'.format(k)) for k in range(n_people)]

    if cautious_size > 0:
        inds = list(range(n_people))
        rnd.shuffle(inds)
        for ind_more_cautious in inds[0:cautious_size]:
            people[ind_more_cautious].caution_interaction = caution_level

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
                      caution_level=0.0, cautious_size=0,
                      social_graph_creator = None,
                      social_graph_creator_kwargs = {}):
    '''Create population of people in a social graph

    '''
    people = make_persons(n_people, n_infect_init, caution_level, cautious_size)

    if not callable(social_graph_creator):
        raise ValueError('Social graph creator required to be executable')

    social_graph = social_graph_creator(**social_graph_creator_kwargs)
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

    disease_sim = ['Virus Y Baseline']
#    world_sim = ['Complete Mix', 'Complete Mix Cautious 50_200', 'Complete Mix Cautious 50_100',
#                 'Complete Mix Cautious 25_200', 'Complete Mix Cautious 25_100']
    world_sim = ['Complete Mix Q', 'Complete Mix Q Cautious 50_200', 'Complete Mix Q Cautious 50_100',
                 'Complete Mix Q Cautious 25_200', 'Complete Mix Q Cautious 25_100']
    short_label = {'Virus Y Baseline' : 'baseline',
                   'Complete Mix Q' : 'completeQ',
                   'Complete Mix Q Cautious 50_200' : 'completeQC50200',
                   'Complete Mix Q Cautious 50_100' : 'completeQC50100',
                   'Complete Mix Q Cautious 25_200' : 'completeQC25200',
                   'Complete Mix Q Cautious 25_100' : 'completeQC25100'}

    sim_repeater = 5
    sim_max_steps = 120
    sim_reporter_interval = 1

    for dd in disease_sim:
        if not dd in DISEASES.keys():
            raise ValueError('Disease label {} not in DISEASES'.format(dd))
    for ww in world_sim:
        if not ww in WORLDS.keys():
            raise ValueError('World label {} not in WORLDS'.format(ww))

    for repeat_index in range(sim_repeater):
        for disease in disease_sim:
            for world in world_sim:
                out_name_prefix = 'simfile_{}_{}_{}'.format(short_label[disease], short_label[world], repeat_index)
                simulation(disease, world, sim_max_steps, sim_reporter_interval, out_name_prefix)
