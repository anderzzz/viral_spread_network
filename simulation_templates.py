'''Constants and functions to run a simulation of Worlds and Diseases

'''
import networkx as nx
from numpy import random as rnd

from graph_growth_classes import Person, World, Disease

# Disease constants
DISEASES = {}
DISEASES['Virus Y Baseline'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 5.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 1.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y High Base Transmitter'] = {'transmission_base_prob' : 1.0/25.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 5.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 1.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y Early Revealer'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 4.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 1.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y Late Revealer'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 7.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 200.0,
                          'succumb_spread' : 1.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y Imperfect Immunizer'] = {'transmission_base_prob' : 1.0/50.0,
                                'activate_mean' : 2.0,
                                'activate_spread' : 1.0,
                                'reveal_mean' : 5.0,
                                'reveal_spread' : 2.0,
                                'recover_mean' : 15.0,
                                'recover_spread' : 3.0,
                                'succumb_mean' : 200.0,
                                'succumb_spread' : 1.0,
                                'immunization_prob' : 0.80}
DISEASES['Virus Y More Imperfect Immunizer'] = {'transmission_base_prob' : 1.0/50.0,
                                           'activate_mean' : 2.0,
                                           'activate_spread' : 1.0,
                                           'reveal_mean' : 5.0,
                                           'reveal_spread' : 2.0,
                                           'recover_mean' : 15.0,
                                           'recover_spread' : 3.0,
                                           'succumb_mean' : 200.0,
                                           'succumb_spread' : 1.0,
                                           'immunization_prob' : 0.50}

# World constants
WORLDS = {}
WORLDS['World Complete Mix'] = {'quarantine_policy' : None,
                        'social_graph_func' : 'population_well_mixed',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 5,
                                                 'n_avg_meet' : 50}}
WORLDS['World Complete Mix Q'] = {'quarantine_policy' : 'revealed',
                        'social_graph_func' : 'population_well_mixed',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 5,
                                                 'n_avg_meet' : 50}}
WORLDS['World Small World Beta 0'] = {'quarantine_policy' : None,
                        'social_graph_func' : 'population_small_world',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 5,
                                                 'n_avg_meet' : 50,
                                                 'beta' : 0.0}}
WORLDS['World Small World Beta 0 Q'] = {'quarantine_policy' : 'revealed',
                        'social_graph_func' : 'population_small_world',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 5,
                                                 'n_avg_meet' : 50,
                                                 'beta' : 0.0}}
WORLDS['World Small World Beta nn25'] = {'quarantine_policy' : None,
                                      'social_graph_func' : 'population_small_world',
                                      'social_graph_kwargs' : {'n_people' : 1000,
                                                               'n_infect_init' : 5,
                                                               'n_avg_meet' : 50,
                                                               'beta' : 0.025}}
WORLDS['World Small World Beta nn25 Q'] = {'quarantine_policy' : 'revealed',
                                        'social_graph_func' : 'population_small_world',
                                        'social_graph_kwargs' : {'n_people' : 1000,
                                                                 'n_infect_init' : 5,
                                                                 'n_avg_meet' : 50,
                                                                 'beta' : 0.025}}
WORLDS['World Small World Beta n10'] = {'quarantine_policy' : None,
                                         'social_graph_func' : 'population_small_world',
                                         'social_graph_kwargs' : {'n_people' : 1000,
                                                                  'n_infect_init' : 5,
                                                                  'n_avg_meet' : 50,
                                                                  'beta' : 0.10}}
WORLDS['World Small World Beta n10 Q'] = {'quarantine_policy' : 'revealed',
                                           'social_graph_func' : 'population_small_world',
                                           'social_graph_kwargs' : {'n_people' : 1000,
                                                                    'n_infect_init' : 5,
                                                                    'n_avg_meet' : 50,
                                                                    'beta' : 0.10}}
WORLDS['World Small World Beta n50'] = {'quarantine_policy' : None,
                                        'social_graph_func' : 'population_small_world',
                                        'social_graph_kwargs' : {'n_people' : 1000,
                                                                 'n_infect_init' : 5,
                                                                 'n_avg_meet' : 50,
                                                                 'beta' : 0.50}}
WORLDS['World Small World Beta n50 Q'] = {'quarantine_policy' : 'revealed',
                                          'social_graph_func' : 'population_small_world',
                                          'social_graph_kwargs' : {'n_people' : 1000,
                                                                   'n_infect_init' : 5,
                                                                   'n_avg_meet' : 50,
                                                                   'beta' : 0.50}}
WORLDS['World Small World Low K Beta n50'] = {'quarantine_policy' : None,
                                        'social_graph_func' : 'population_small_world',
                                        'social_graph_kwargs' : {'n_people' : 1000,
                                                                 'n_infect_init' : 5,
                                                                 'n_avg_meet' : 50,
                                                                 'k_avg_degree' : 51,
                                                                 'beta' : 0.50}}
WORLDS['World Small World Low K Beta n50 Q'] = {'quarantine_policy' : 'revealed',
                                          'social_graph_func' : 'population_small_world',
                                          'social_graph_kwargs' : {'n_people' : 1000,
                                                                   'n_infect_init' : 5,
                                                                   'n_avg_meet' : 50,
                                                                   'k_avg_degree': 51,
                                                                   'beta' : 0.50}}
WORLDS['World Caveman'] = {'quarantine_policy' : None,
                        'social_graph_func' : 'population_caveman',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 5,
                                                 'n_avg_meet' : 50}}
WORLDS['World Caveman Q'] = {'quarantine_policy' : 'revealed',
                        'social_graph_func' : 'population_caveman',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 5,
                                                 'n_avg_meet' : 50}}
WORLDS['World Relaxed Caveman'] = {'quarantine_policy' : None,
                           'social_graph_func' : 'population_relaxed_caveman',
                           'social_graph_kwargs' : {'n_people' : 1000,
                                                    'n_infect_init' : 5,
                                                    'n_avg_meet' : 50}}
WORLDS['World Relaxed Caveman Q'] = {'quarantine_policy' : 'revealed',
                             'social_graph_func' : 'population_relaxed_caveman',
                             'social_graph_kwargs' : {'n_people' : 1000,
                                                      'n_infect_init' : 5,
                                                      'n_avg_meet' : 50}}
WORLDS['World ScaleFree'] = {'quarantine_policy' : None,
                                   'social_graph_func' : 'population_barabasi_albert',
                                   'social_graph_kwargs' : {'n_people' : 1000,
                                                            'n_infect_init' : 5,
                                                            'n_avg_meet' : 50}}
WORLDS['World ScaleFree Q'] = {'quarantine_policy' : 'revealed',
                                     'social_graph_func' : 'population_barabasi_albert',
                                     'social_graph_kwargs' : {'n_people' : 1000,
                                                              'n_infect_init' : 5,
                                                              'n_avg_meet' : 50}}

# Social network creation methods
def _make_persons(n_people, n_infect_init):

    people = [Person('A Name {}'.format(k)) for k in range(n_people)]
    rnd_inds = rnd.randint(0, n_people, n_infect_init)
    for k_infect in rnd_inds:
        people[k_infect].infect()

    return people

def _make_edge_weights(gg, n_avg_meet):

    n_edges = gg.size()
    n_nodes = len(gg)
    f_weight = 0.5 * float(n_avg_meet) * n_nodes / n_edges
    if f_weight > 1.0:
        raise ValueError('Too great weight: {}. Reduce average meetings or increase density of edges'.format(f_weight))
    nx.set_edge_attributes(gg, f_weight, 'weight')

    return gg

def population_well_mixed(n_people, n_infect_init, n_avg_meet):

    # Generate people in population and seed with a few infected ones
    people = _make_persons(n_people, n_infect_init)

    # Disperse population in a social network
    gg = nx.complete_graph(n_people)
    nx.readwrite.write_gml(gg, 'complete_graph.gml')
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))

    # Put weight on social connections
    gg = _make_edge_weights(gg, n_avg_meet)

    return gg

def population_small_world(n_people, n_infect_init, n_avg_meet, k_avg_degree=100, beta=(1.0/25.0)):

    # Generate people in population and seed with a few infected ones
    people = _make_persons(n_people, n_infect_init)

    # Disperse population in a social network
    gg = nx.connected_watts_strogatz_graph(n_people, k_avg_degree, beta, seed=42)
    nx.readwrite.write_gml(gg, 'small_world_graph_{}_{}.gml'.format(k_avg_degree, int(100.0 * beta)))
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))

    # Put weight on social connections
    gg = _make_edge_weights(gg, n_avg_meet)

    return gg

def population_caveman(n_people, n_infect_init, n_avg_meet):

    # Generate people in population and seed with a few infected ones
    people = _make_persons(n_people, n_infect_init)

    # Disperse population in a social network
    gg = nx.connected_caveman_graph(10, int(n_people / 10))
    nx.readwrite.write_gml(gg, 'caveman_graph.gml')
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))

    # Put weight on social connections
    gg = _make_edge_weights(gg, n_avg_meet)

    return gg

def population_relaxed_caveman(n_people, n_infect_init, n_avg_meet):

    # Generate people in population and seed with a few infected ones
    people = _make_persons(n_people, n_infect_init)

    # Disperse population in a social network
    gg = nx.relaxed_caveman_graph(10, int(n_people / 10), 0.01, seed=42)
    nx.readwrite.write_gml(gg, 'relaxed_caveman_graph.gml')
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))

    # Put weight on social connections
    gg = _make_edge_weights(gg, n_avg_meet)

    return gg

def population_barabasi_albert(n_people, n_infect_init, n_avg_meet):

    # Generate people in population and seed with a few infected ones
    people = _make_persons(n_people, n_infect_init)

    # Disperse population in a social network
    gg = nx.barabasi_albert_graph(n_people, 60, seed=42)
    nx.readwrite.write_gml(gg, 'barabasi_albert_graph.gml')
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))

    # Put weight on social connections
    gg = _make_edge_weights(gg, n_avg_meet)

    return gg

def simulation(disease_name, world_name, n_days_max, report_interval, out_file_name):

    # Instantiate disease and world
    viral_disease = Disease(name=disease_name, **DISEASES[disease_name])
    social_graph = eval(WORLDS[world_name]['social_graph_func'])(**WORLDS[world_name]['social_graph_kwargs'])
    the_world = World(name=world_name,
                      social_graph=social_graph,
                      quarantine_policy=WORLDS[world_name]['quarantine_policy'])

    # Output simulation metadata
    with open(out_file_name + '_sim_data.csv', 'w') as f:
        f.write('World Name, {}\n'.format(world_name))
        f.write('Social Graph Method, {}\n'.format(WORLDS[world_name]['social_graph_func']))
        for key, value in WORLDS[world_name]['social_graph_kwargs'].items():
            f.write('{}, {}\n'.format(key, value))
        f.write('Disease Name, {}\n'.format(disease_name))
        for key, value in DISEASES[disease_name].items():
            f.write('{}, {}\n'.format(key, value))

    # Run the simulation
    open(out_file_name + '_data.csv', 'w').close()
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

    #counter_1 = 0
    #for virus, v_kwargs in DISEASES.items():
    #    counter_2 = 0
    #    for world, w_kwargs in WORLDS.items():
    #        simulation(virus, world, 120, 1, 'sim_out_{}_{}'.format(counter_1, counter_2))
    #        counter_2 += 1
    #    counter_1 += 1
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_00')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_01')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_02')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_03')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_04')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_05')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_06')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_07')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_08')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix Q', 120, 1, 'impimmun_complete_q_09')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_00')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_01')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_02')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_03')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_04')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_05')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_06')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_07')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_08')
    simulation('Virus Y More Imperfect Immunizer', 'World Complete Mix', 120, 1, 'impimmun_complete_09')
