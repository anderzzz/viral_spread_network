'''Simulation of people in the world infection and spread

'''
import pandas as pd
import networkx as nx
from numpy import random as rnd
from scipy.stats import norm

class _State():

    def infect(self):

        self.infected = True
        self.days_since_infection = 0

    def reveal(self):

        self.symptomatic = True
        self.days_since_symptomatic = 0

    def activate(self):

        self.contagious = True

    def succumb(self):

        self.dead = True
        self.days_infected_until_dead = self.days_since_infection

    def survive(self):

        self.infected = False
        self.symptomatic = False
        self.contagious = False
        self.quarantined = False
        self.days_infected_until_survive = self.days_since_infection

    def immunize(self):

        self.immune = True

    def quarantine(self):

        self.quarantined = True
        self.days_since_quarantined = 0

    def report(self):
        return pd.Series(data=[self.infected, self.contagious, self.symptomatic,
                               self.immune, self.dead, self.quarantined,
                               self.days_alive, self.days_since_infection,
                               self.days_since_symptomatic],
                         index=['infected', 'contagious', 'symptomatic',
                                'immune', 'dead', 'quarantined',
                                'days_alive', 'days_since_infection',
                                'days_since_symptomatic'])

    def __init__(self, infected=False, contagious=False, symptomatic=False,
                 immune=False, dead=False, quarantined=False):

        self.infected = infected
        self.contagious = contagious
        self.symptomatic = symptomatic
        self.immune = immune
        self.dead = dead
        self.quarantined = quarantined

        self.days_since_infection = None
        self.days_since_symptomatic = None
        self.days_infected_until_dead = None
        self.days_infected_until_survive = None
        self.days_since_quarantined = None
        self.days_alive = 0

class Person():
    '''Person with a state and a predisposition

    '''
    def is_immune(self):
        return self.state.immune

    def is_contagious(self):
        return self.state.contagious

    def is_infected(self):
        return self.state.infected

    def is_dead(self):
        return self.state.dead

    def is_symptomatic(self):
        return self.state.symptomatic

    def is_quarantined(self):
        return self.state.quarantined

    def days_infected(self):
        return self.state.days_since_infection

    def grow_older(self):

        self.state.days_alive += 1
        if self.state.infected:
            self.state.days_since_infection += 1
        if self.state.symptomatic:
            self.state.days_since_symptomatic += 1
        if self.state.quarantined:
            self.state.days_since_quarantined += 1

    def report(self):

        series_person = pd.Series(data=[self.name, self.caution_interaction, self.general_health],
                                  index=['name', 'caution_interaction', 'general_health'])
        series_state = self.state.report()
        return series_person.append(series_state)

    def __init__(self, name, caution_interaction=0.0, general_health=0.0):

        self.name = name

        self.caution_interaction = caution_interaction
        self.general_health = general_health

        self.state = _State()
        self.infect = self.state.infect
        self.succumb = self.state.succumb
        self.activate = self.state.activate
        self.reveal = self.state.reveal
        self.survive = self.state.survive
        self.immunize = self.state.immunize
        self.quarantine = self.state.quarantine

class World():

    def do_they_meet_today(self, p_a, p_b):

        if p_a.is_quarantined() or p_b.is_quarantined():
            they_meet = False

        else:
            try:
                intensity_social_edge = self.network[p_a][p_b]['weight']
                they_meet = rnd.ranf() < intensity_social_edge

            except KeyError:
                they_meet = False

        return they_meet

    def enact_quarantine_policy(self):

        self._q_policy(**self._q_policy_kwargs)

    def _q_policy_none(self):

        pass

    def _q_policy_symptomatic(self):

        for person in self.network.nodes:
            if person.is_symptomatic():
                person.quarantine()

    def _q_policy_symptomatic_with_chance(self, chance):

        for person in self.network.nodes:
            if person.is_symptomatic():
                if rnd.ranf() < chance:
                    person.quarantine()

    def report(self):

        total_df_data = []
        for person in self.network.nodes:

            weight_sum = sum([self.network.edges[ee]['weight'] for ee in self.network.edges(person)])

            person_in_world_series = pd.Series(data=[self.network.degree[person],
                                                     weight_sum],
                                               index=['degree',
                                                      'expectation_meetings_per_day'])

            person_series = person.report()
            person_series = person_series.append(person_in_world_series)
            total_df_data.append(person_series)

        total_df = pd.DataFrame(total_df_data)
        total_df = total_df.set_index(['name', 'days_alive'])
        total_df = total_df.stack()
        new_index = total_df.index.set_names(['name','days_alive','property'])
        total_df.index = new_index

        return total_df

    def __init__(self, name, persons_network,
                 quarantine_policy=None, quarantine_policy_kwargs={}):

        self.name = name
        self.network = persons_network

        self._q_policy_kwargs = quarantine_policy_kwargs
        if quarantine_policy is None:
            self._q_policy = self._q_policy_none

        elif quarantine_policy == 'symptomatic':
            self._q_policy = self._q_policy_symptomatic

        elif quarantine_policy == 'symptomatic with delay':
            self._q_policy = self._q_policy_symptomatic_with_chance

        elif callable(quarantine_policy):
            self._q_policy = quarantine_policy

        else:
            raise ValueError('Unknown quarantine policy: {}'.format(quarantine_policy))

class Disease():

    def progress_one_more_day(self, world):
        '''Make disease progress one more day in the world'''

        for pp_interaction in world.network.edges:

            person_a = pp_interaction[0]
            person_b = pp_interaction[1]

            if world.do_they_meet_today(person_a, person_b):

                self._progression_edge(person_a, person_b)

        persons_dead = []
        for person in world.network.nodes:
            self._progression_node(person)
            if person.is_dead():
                persons_dead.append(person)
        world.network.remove_nodes_from(persons_dead)

        world.enact_quarantine_policy()

        self.day_counter += 1

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

        transition_performed = False
        if rnd.ranf() < transition_cdf(n_days, **transition_cdf_kwargs):
            person_transition_func()
            transition_performed = True

        return transition_performed

    def _progression_edge(self, person_a, person_b):
        '''Make disease progress as far as given network edge is concerned. Only event is transmission, which requires
        one contagious individual and one uninfected individual.'''

        if person_a.is_contagious() and (not person_b.is_infected()):
            self._try_transmission(person_a, person_b)

        elif person_b.is_contagious() and (not person_a.is_infected()):
            self._try_transmission(person_b, person_a)

    def _progression_node(self, person):
        '''Make disease progress as far as a given network node is concerned. Number of events possible as the
        single individual deals with the disease.'''

        # If person displays symptoms, possible transition: survive or succumb
        if person.is_symptomatic():
            if person.general_health >= 0.0:
                survive_mean_actual = self.survive_mean + person.general_health * \
                                      (self.activate_mean - self.survive_mean)
            else:
                survive_mean_actual = self.survive_mean - person.general_health * \
                                      (self.succumb_mean + self.succumb_spread - self.survive_mean)

            survived = self._trial(person.survive, person.days_infected(), norm.cdf,
                                   {'loc' : survive_mean_actual,
                                    'scale' : self.survive_spread})

            # If no survival today, do trial if they succumb
            if not survived:
                self._trial(person.succumb, person.days_infected(), norm.cdf,
                            {'loc' : self.succumb_mean,
                             'scale' : self.succumb_spread})

            # If there was survival, do trial if they immunize
            else:
                self._trial(person.immunize, None, lambda _ : self.immunization_prob)

        # If instead person is infected, not yet symptomatic, they can become activated and/or become symptomatic
        elif person.is_infected():
            self._trial(person.activate, person.days_infected(), norm.cdf,
                        {'loc' : self.activate_mean,
                         'scale' : self.activate_spread})

            self._trial(person.reveal, person.days_infected(), norm.cdf,
                        {'loc' : self.reveal_mean,
                         'scale' : self.reveal_spread})

        person.grow_older()

    def __init__(self, name, transmission_base_prob,
                       activate_mean, activate_spread,
                       reveal_mean, reveal_spread,
                       survive_mean, survive_spread,
                       succumb_mean, succumb_spread,
                       immunization_prob):

        self.name = name
        self.day_counter = 0

        self.transmission_base_prob = transmission_base_prob
        self.activate_mean = activate_mean
        self.activate_spread = activate_spread
        self.reveal_mean = reveal_mean
        self.reveal_spread = reveal_spread
        self.survive_mean = survive_mean
        self.survive_spread = survive_spread
        self.succumb_mean = succumb_mean
        self.succumb_spread = succumb_spread
        self.immunization_prob = immunization_prob

