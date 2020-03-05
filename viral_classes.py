'''Simulation of people in the world infection and spread

'''
import networkx as nx
from numpy import random as rnd
from scipy.stats import norm

class _State():

    def infect(self):

        self.infected = True
        self.days_since_infection = 0

    def reveal(self):

        self.symptomatic = True

    def activate(self):

        self.contagious = True

    def succumb(self):

        self.dead = True
        self.days_since_start = self.days_since_infection

    def survive(self):

        self.infected = False
        self.symptomatic = False
        self.contagious = False
        self.days_since_start = self.days_since_infection

    def immunize(self):

        self.immune = True

    def __init__(self, infected=False, contagious=False, symptomatic=False,
                       immune=False, dead=False, days_since_infection=None,
                       days_alive = 0):

        self.infected = infected
        self.contagious = contagious
        self.symptomatic = symptomatic
        self.immune = immune
        self.dead = dead

        self.days_since_infection = days_since_infection
        self.days_alive = days_alive

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

    def grow_older(self):

        self.state.days_alive += 1
        if self.state.infected:
            self.state.days_since_infection += 1

    def __init__(self, name, caution_interaction=0.0, general_health=1.0):

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

class World():

    def do_they_meet_today(self, p_a, p_b):

        try:
            intensity_social_edge = self.network[p_a][p_b]['weight']
            they_meet = rnd.ranf() < intensity_social_edge

        except KeyError:
            they_meet = False

        return they_meet

    def __init__(self, name, persons_network):

        self.name = name
        self.network = persons_network

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

            survived = self._trial(person.survive, person.days_since_infection, norm.cdf,
                                   {'loc' : survive_mean_actual,
                                    'scale' : self.survive_spread})

            # If no survival today, do trial if they succumb
            if not survived:
                self._trial(person.succumb, person.days_since_infection, norm.cdf,
                            {'loc' : self.succumb_mean,
                             'scale' : self.succumb_spread})

            # If there was survival, do trial if they immunize
            else:
                self._trial(person.immunize, None, lambda _ : self.immunization_prob)

        # If instead person is infected, not yet symptomatic, they can become activated and/or become symptomatic
        elif person.is_infected():
            self._trial(person.activate, person.days_since_infection, norm.cdf,
                        {'loc' : self.activate_mean,
                         'scale' : self.activate_spread})

            self._trial(person.reveal, person.days_since_infection, norm.cdf,
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

#
# Simple test
#
pp1 = Person('Arnold')
pp2 = Person('Lars')
pp3 = Person('Sven')

gg = nx.Graph()
gg.add_node(pp1)
gg.add_node(pp2)
gg.add_node(pp3)
gg.add_edge(pp1, pp2, weight=0.5)
gg.add_edge(pp2, pp3, weight=0.5)

the_world = World('simple test', gg)

viral_disease = Disease('contact disease')

viral_disease.one_more_day(the_world)
