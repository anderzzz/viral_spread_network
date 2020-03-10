'''Classes for persons in a social graph in the world in which a disease is spreading

'''
import pandas as pd
import networkx as nx
from numpy import random as rnd
from scipy.stats import norm

class _State():
    '''State of disease for a person and the state transition methods'''

    def infect(self):
        self.infected = True

    def reveal(self):
        self.revealed = True

    def activate(self):
        self.contagious = True

    def succumb(self):
        self.dead = True
        self.reset()

    def recover(self):
        self.reset()

    def immunize(self):
        self.immune = True

    def quarantine(self):
        self.quarantined = True

    def reset(self):
        self.infected = False
        self.revealed = False
        self.contagious = False
        self.quarantined = False

    def report(self):
        '''Report current state'''
        return pd.Series(data=[self.infected, self.contagious, self.revealed,
                               self.immune, self.dead, self.quarantined],
                         index=self.state_labels)

    def __init__(self, infected=False, contagious=False, revealed=False,
                 immune=False, dead=False, quarantined=False):

        self.state_labels = ['infected', 'contagious', 'revealed', 'immune', 'dead', 'quarantined']
        self.infected = infected
        self.contagious = contagious
        self.revealed = revealed
        self.immune = immune
        self.dead = dead
        self.quarantined = quarantined


class Person():
    '''Person with a disease state and a predisposition, plus methods to query the person's current disease state

    '''
    def is_immune(self):
        return self.state.immune

    def is_contagious(self):
        return self.state.contagious

    def is_infected(self):
        return self.state.infected

    def is_dead(self):
        return self.state.dead

    def is_revealed(self):
        return self.state.revealed

    def is_quarantined(self):
        return self.state.quarantined

    def _time_diff(self, label):
        '''Create function to evaluate difference between current time and time of a given state transition'''

        def mapper():
            if self.time_stamp[label] is None:
                return None
            else:
                return self.time_coordinate - self.time_stamp[label]

        return mapper

    def _decorate_time_stamp(self, func, label):
        '''Decorate the state change function with the recording of a time stamp'''

        def mapper():
            self.time_stamp[label] = self.time_coordinate
            func()

        return mapper

    def report(self):
        '''Report personal data, including disease state of person, at current time'''
        series_person = pd.Series(data=[self.name, self.time_coordinate,
                                        self.caution_interaction, self.general_health],
                                  index=['name', 'time_coordinate',
                                         'caution_interaction', 'general_health'])
        series_time = pd.Series(dict([('time_' + label, value) for label, value in self.time_stamp.items()]))
        series_state = self.state.report()

        return pd.concat([series_person, series_state, series_time])

    def __init__(self, name, caution_interaction=0.0, general_health=0.0):

        self.name = name
        self.time_coordinate = 0

        self.caution_interaction = caution_interaction
        self.general_health = general_health

        self.state = _State()
        self.time_stamp = dict([(label, None) for label in self.state.state_labels])

        self.infect = self._decorate_time_stamp(self.state.infect, 'infect')
        self.succumb = self._decorate_time_stamp(self.state.succumb, 'succumb')
        self.activate = self._decorate_time_stamp(self.state.activate, 'activate')
        self.reveal = self._decorate_time_stamp(self.state.reveal, 'reveal')
        self.recover = self._decorate_time_stamp(self.state.recover, 'recover')
        self.immunize = self._decorate_time_stamp(self.state.immunize, 'immunize')
        self.quarantine = self._decorate_time_stamp(self.state.quarantine, 'quarantine')

        self.days_infected = self._time_diff('infect')
        self.days_revealed = self._time_diff('reveal')
        self.days_quarantined = self._time_diff('quarantine')
        self.days_immunized = self._time_diff('immunize')
        self.days_succumbed = self._time_diff('succumb')
        self.days_recovered = self._time_diff('recover')


class World():
    '''The world within which persons exist and interact and can be infected with the disease, wherein the world can
    be comprised of heterogenous interactions between persons as defined by a social graph'''

    def do_they_meet_today(self, p_a, p_b):
        '''Evaluate if two persons in the world meet. If meeting takes place is an outcome of a Bernoulli trial
        with a probability proportional to the weight of the corresponding edge

        '''

        # Quarantined and dead people meet nobody
        if p_a.is_quarantined() or p_b.is_quarantined() or p_a.is_dead() or p_b.is_dead():
            they_meet = False

        # Trial for meeting, probability set by corresponding social graph edge weight
        else:
            try:
                intensity_social_edge = self.social_graph[p_a][p_b]['weight']
                they_meet = rnd.ranf() < intensity_social_edge

            except KeyError:
                they_meet = False

        return they_meet

    def enact_quarantine_policy(self):
        self._q_policy(**self._q_policy_kwargs)

    def _q_policy_none(self):
        '''No quarantine is done under any condition'''
        pass

    def _q_policy_revealed(self):
        '''Person is quarantined if their disease is revealed'''
        for person in self.social_graph.nodes:
            if person.is_revealed():
                person.quarantine()

    def _q_policy_revealed_with_chance(self, chance):
        '''Person is quarantined with some probability if their disease is revealed'''
        for person in self.social_graph.nodes:
            if person.is_revealed():
                if rnd.ranf() < chance:
                    person.quarantine()

    def is_disease_free(self):
        '''If no person in the world is infected, return True, which implies by the disease spreading mechanism that
        no person can become infected, hence a stable state has been attained.'''
        return not any([person.is_infected() for person in self.social_graph.nodes])

    def report(self):
        '''Report data about the world, including its persons and their disease state at current time'''
        total_df_data = []
        for person in self.social_graph.nodes:

            weight_sum = sum([self.social_graph.edges[ee]['weight'] for ee in self.social_graph.edges(person)])

            person_in_world_series = pd.Series(data=[self.social_graph.degree[person],
                                                     weight_sum],
                                               index=['degree',
                                                      'expectation_meetings_per_day'])

            person_series = person.report()
            person_series = person_series.append(person_in_world_series)
            total_df_data.append(person_series)

        total_df = pd.DataFrame(total_df_data)
        total_df = total_df.set_index(['name', 'time_coordinate'])
        total_df = total_df.stack()
        new_index = total_df.index.set_names(['name','time_coordinate','property'])
        total_df.index = new_index

        return total_df

    def __init__(self, name, social_graph, delete_dead_from_social_graph=False,
                 quarantine_policy=None, quarantine_policy_kwargs={}):

        self.name = name
        self.social_graph = social_graph
        self.delete_dead_from_social_graph = delete_dead_from_social_graph

        self._q_policy_kwargs = quarantine_policy_kwargs
        if quarantine_policy is None:
            self._q_policy = self._q_policy_none

        elif quarantine_policy == 'revealed':
            self._q_policy = self._q_policy_revealed

        elif quarantine_policy == 'revealed with chance':
            self._q_policy = self._q_policy_revealed_with_chance

        elif callable(quarantine_policy):
            self._q_policy = quarantine_policy

        else:
            raise ValueError('Unknown quarantine policy: {}'.format(quarantine_policy))

class Disease():
    '''Disease that can spread between persons in the world according to a stochastic mechanism and which progress
    within a person according to a stochastic mechanism'''

    def progress_one_more_day(self, world):
        '''Make disease progress one more day in the world'''

        self.day_counter += 1

        # Transmit disease between people
        for pp_interaction in world.social_graph.edges:
            person_a = pp_interaction[0]
            person_b = pp_interaction[1]

            if world.do_they_meet_today(person_a, person_b):
                self._progression_edge(person_a, person_b)

        # Evolve disease state within people
        persons_dead = []
        for person in world.social_graph.nodes:
            self._progression_node(person)
            if person.is_dead():
                persons_dead.append(person)

        # Update social graph on basis of rules as policy
        if world.delete_dead_from_social_graph:
            world.social_graph.remove_nodes_from(persons_dead)
        world.enact_quarantine_policy()

    def _try_transmission(self, transmitter, receiver):
        '''Attempt transmission of disease between a contagious transmitter and a healthy receiver'''

        transmission_made = False
        if not receiver.is_immune():
            caution = min(transmitter.caution_interaction,
                          receiver.caution_interaction)
            thrs_transmission = self.transmission_base_prob * (1.0 - caution)
            transmission_made = self._trial(receiver.infect, None, lambda _: thrs_transmission)

        return transmission_made

    def _trial(self, person_transition_func, n_days, transition_cdf, transition_cdf_kwargs={}):
        '''Generic trial function of event to create a state transition'''

        transition_performed = False
        if rnd.ranf() < transition_cdf(n_days, **transition_cdf_kwargs):
            person_transition_func()
            transition_performed = True

        return transition_performed

    def _progression_edge(self, person_a, person_b):
        '''Make disease progress as far as given social graph edge is concerned. Only event is transmission, which requires
        one contagious individual and one uninfected individual.'''

        outcome = False
        if person_a.is_contagious() and (not person_b.is_infected()):
            outcome = self._try_transmission(person_a, person_b)

        elif person_b.is_contagious() and (not person_a.is_infected()):
            outcome = self._try_transmission(person_b, person_a)

        return outcome

    def _progression_node(self, person):
        '''Make disease progress as far as a given social graph node is concerned. Number of events possible as the
        single individual deals with the disease.'''

        # A dead person is in terminal state, no transitions to be made
        if person.is_dead():
            pass

        # If person is contagious, possible next transition: reveal or recover or succumb
        elif person.is_contagious():

            # Attempt to reveal
            if not person.is_revealed():
                self._trial(person.reveal, person.days_infected(), norm.cdf,
                            {'loc' : self.reveal_mean,
                             'scale' : self.reveal_spread})

            # Scale recovery parameter by general health of person
            if person.general_health >= 0.0:
                recover_mean_actual = self.recover_mean + person.general_health * \
                                      (self.activate_mean - self.recover_mean)
            else:
                recover_mean_actual = self.recover_mean - person.general_health * \
                                      (self.succumb_mean - self.recover_mean)

            # Because recover and succumb are mutually exclusive, an unbiased trial of either transition requires
            # the first trial to be selected at random and evenly between recover and succumb
            event_first = rnd.choice(['recover', 'succumb'])
            if event_first == 'recover':
                first_func = person.recover
                first_func_mean = recover_mean_actual
                first_func_spread = self.recover_spread
                second_func = person.succumb
                second_func_mean = self.succumb_mean
                second_func_spread = self.succumb_spread

            else:
                first_func = person.succumb
                first_func_mean = self.succumb_mean
                first_func_spread = self.succumb_spread
                second_func = person.recover
                second_func_mean = recover_mean_actual
                second_func_spread = self.recover_spread

            # TODO: generalize to non-normal transition probabilities
            first_outcome = self._trial(first_func, person.days_infected(), norm.cdf,
                                        {'loc' : first_func_mean,
                                         'scale' : first_func_spread})
            if not first_outcome:
                second_outcome = self._trial(second_func, person.days_infected(), norm.cdf,
                                             {'loc' : second_func_mean,
                                              'scale' : second_func_spread})
            else:
                second_outcome = False

            # If recover (or succumb) try event to immunize
            if (first_outcome and event_first == 'recover') or (second_outcome and event_first == 'succumb'):
                self._trial(person.immunize, None, lambda _ : self.immunization_prob)

        # If instead person is infected but not contagious, attempt to activate disease
        elif person.is_infected():
            self._trial(person.activate, person.days_infected(), norm.cdf,
                        {'loc' : self.activate_mean,
                         'scale' : self.activate_spread})

        person.time_coordinate = self.day_counter

    def __init__(self, name, transmission_base_prob,
                       activate_mean, activate_spread,
                       reveal_mean, reveal_spread,
                       recover_mean, recover_spread,
                       succumb_mean, succumb_spread,
                       immunization_prob):

        self.name = name
        self.day_counter = 0

        self.transmission_base_prob = transmission_base_prob
        self.activate_mean = activate_mean
        self.activate_spread = activate_spread
        self.reveal_mean = reveal_mean
        self.reveal_spread = reveal_spread
        self.recover_mean = recover_mean
        self.recover_spread = recover_spread
        self.succumb_mean = succumb_mean
        self.succumb_spread = succumb_spread
        self.immunization_prob = immunization_prob
