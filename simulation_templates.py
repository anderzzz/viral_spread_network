'''Constants and functions to run a simulation of Worlds and Diseases

'''
import networkx as nx
from numpy import random as rnd

from graph_growth_classes import Person, World, Disease

# Disease constants
DISEASES = {}
DISEASES['Virus X_01'] = {'transmission_base_prob' : 1.0/30.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 10.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 20.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 22.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus X_02'] = {'transmission_base_prob' : 1.0/10.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 10.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 20.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 22.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus X_03'] = {'transmission_base_prob' : 1.0/30.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 10.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 22.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus X_04'] = {'transmission_base_prob' : 1.0/30.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 7.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 20.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 22.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y_01'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 5.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 20.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y_02'] = {'transmission_base_prob' : 1.0/25.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 5.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 20.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y_03'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 4.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 20.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y_04'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 7.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 20.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y_05'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 5.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 25.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}
DISEASES['Virus Y_06'] = {'transmission_base_prob' : 1.0/50.0,
                          'activate_mean' : 2.0,
                          'activate_spread' : 1.0,
                          'reveal_mean' : 5.0,
                          'reveal_spread' : 2.0,
                          'recover_mean' : 15.0,
                          'recover_spread' : 3.0,
                          'succumb_mean' : 15.0,
                          'succumb_spread' : 3.0,
                          'immunization_prob' : 1.00}

# World constants
WORLDS = {}
WORLDS['World W_01'] = {'quarantine_policy' : None,
                        'social_graph_func' : 'population_well_mixed',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 4,
                                                 'n_avg_meet' : 60}}
WORLDS['World W_02'] = {'quarantine_policy' : 'revealed',
                        'social_graph_func' : 'population_well_mixed',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 4,
                                                 'n_avg_meet' : 60}}
WORLDS['World W_03'] = {'quarantine_policy' : 'revealed',
                        'social_graph_func' : 'population_well_mixed',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 4,
                                                 'n_avg_meet' : 30}}
WORLDS['World W_04'] = {'quarantine_policy' : None,
                        'social_graph_func' : 'population_small_world',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 4,
                                                 'n_avg_meet' : 60}}
WORLDS['World W_05'] = {'quarantine_policy' : 'revealed',
                        'social_graph_func' : 'population_small_world',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 4,
                                                 'n_avg_meet' : 60}}
WORLDS['World W_06'] = {'quarantine_policy' : 'revealed',
                        'social_graph_func' : 'population_small_world',
                        'social_graph_kwargs' : {'n_people' : 1000,
                                                 'n_infect_init' : 4,
                                                 'n_avg_meet' : 30}}

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
    f_weight = float(n_avg_meet) * n_nodes / n_edges
    nx.set_edge_attributes(gg, f_weight, 'weight')

    return gg

def population_well_mixed(n_people, n_infect_init, n_avg_meet):

    # Generate people in population and seed with a few infected ones
    people = _make_persons(n_people, n_infect_init)

    # Disperse population in a social network
    gg = nx.complete_graph(n_people)
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))
    nx.readwrite.write_gml(gg, 'complete_graph.gml')

    # Put weight on social connections
    gg = _make_edge_weights(gg, n_avg_meet)

    return gg

def population_small_world(n_people, n_infect_init, n_avg_meet):

    # Generate people in population and seed with a few infected ones
    people = _make_persons(n_people, n_infect_init)

    # Disperse population in a social network
    gg = nx.connected_watts_strogatz_graph(n_people, int(n_people / 10), 1.0/3.0, seed=42)
    gg = nx.relabel_nodes(gg, dict([(k, p) for k, p in enumerate(people)]))
    nx.readwrite.write_gml(gg, 'small_world_graph.gml')

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

    simulation('Virus Y_01', 'World W_01', 120, 1, 'test_run_y_1_1')
    simulation('Virus Y_02', 'World W_01', 120, 1, 'test_run_y_2_1')
    simulation('Virus Y_03', 'World W_01', 120, 1, 'test_run_y_3_1')
    simulation('Virus Y_04', 'World W_01', 120, 1, 'test_run_y_4_1')
    simulation('Virus Y_05', 'World W_01', 120, 1, 'test_run_y_5_1')
    simulation('Virus Y_06', 'World W_01', 120, 1, 'test_run_y_6_1')
   # simulation('Virus Y_01', 'World W_02', 120, 1, 'test_run_y_1_2')
   # simulation('Virus Y_02', 'World W_02', 120, 1, 'test_run_y_2_2')
   # simulation('Virus Y_03', 'World W_02', 120, 1, 'test_run_y_3_2')
   # simulation('Virus Y_04', 'World W_02', 120, 1, 'test_run_y_4_2')
   # simulation('Virus Y_05', 'World W_02', 120, 1, 'test_run_y_5_2')
   # simulation('Virus Y_06', 'World W_02', 120, 1, 'test_run_y_6_2')
   # simulation('Virus Y_01', 'World W_03', 120, 1, 'test_run_y_1_3')
   # simulation('Virus Y_02', 'World W_03', 120, 1, 'test_run_y_2_3')
   # simulation('Virus Y_03', 'World W_03', 120, 1, 'test_run_y_3_3')
   # simulation('Virus Y_04', 'World W_03', 120, 1, 'test_run_y_4_3')
   # simulation('Virus Y_05', 'World W_03', 120, 1, 'test_run_y_5_3')
   # simulation('Virus Y_06', 'World W_03', 120, 1, 'test_run_y_6_3')
   # simulation('Virus Y_01', 'World W_04', 120, 1, 'test_run_y_1_4')
   # simulation('Virus Y_02', 'World W_04', 120, 1, 'test_run_y_2_4')
   # simulation('Virus Y_03', 'World W_04', 120, 1, 'test_run_y_3_4')
   # simulation('Virus Y_04', 'World W_04', 120, 1, 'test_run_y_4_4')
   # simulation('Virus Y_05', 'World W_04', 120, 1, 'test_run_y_5_4')
   # simulation('Virus Y_06', 'World W_04', 120, 1, 'test_run_y_6_4')
   # simulation('Virus Y_01', 'World W_05', 120, 1, 'test_run_y_1_5')
   # simulation('Virus Y_02', 'World W_05', 120, 1, 'test_run_y_2_5')
   # simulation('Virus Y_03', 'World W_05', 120, 1, 'test_run_y_3_5')
   # simulation('Virus Y_04', 'World W_05', 120, 1, 'test_run_y_4_5')
   # simulation('Virus Y_05', 'World W_05', 120, 1, 'test_run_y_5_5')
   # simulation('Virus Y_06', 'World W_05', 120, 1, 'test_run_y_6_5')
   # simulation('Virus Y_01', 'World W_06', 120, 1, 'test_run_y_1_6')
   # simulation('Virus Y_02', 'World W_06', 120, 1, 'test_run_y_2_6')
   # simulation('Virus Y_03', 'World W_06', 120, 1, 'test_run_y_3_6')
   # simulation('Virus Y_04', 'World W_06', 120, 1, 'test_run_y_4_6')
   # simulation('Virus Y_05', 'World W_06', 120, 1, 'test_run_y_5_6')
   # simulation('Virus Y_06', 'World W_06', 120, 1, 'test_run_y_6_6')
