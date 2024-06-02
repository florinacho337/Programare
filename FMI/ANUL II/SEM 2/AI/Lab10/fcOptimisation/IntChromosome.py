import random
from fcOptimisation.utils import generateNewValue

class Chromosome:
    def __init__(self, problParam):
        self.__problParam = problParam
        self.__repres = self.initialize(problParam)
        self.__fitness = 0.0

    def initialize(self, problParam):
        mat = self.__problParam['mat']
        degrees = self.__problParam['degrees']
        node_count = self.__problParam['noNodes']

        sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
        community_assignments = [-1] * node_count
        current_community = 0
        degerees_keys = list(degrees.keys())
        degerees_keys.sort()
        start = degerees_keys[0]

        for node in sorted_nodes:
            idx = node - start
            if community_assignments[idx] == -1:  
                community_assignments[idx] = current_community
                for neighbor in range(node_count):
                    if mat[idx][neighbor] == 1 and community_assignments[neighbor] == -1:
                        community_assignments[neighbor] = current_community
                current_community += 1

        return community_assignments
        
    
    @property
    def repres(self):
        return self.__repres 
    
    @property
    def fitness(self):
        return self.__fitness 
    
    @repres.setter
    def repres(self, l=[]):
        self.__repres = l 
    
    @fitness.setter 
    def fitness(self, fit=0.0):
        self.__fitness = fit 
    
    def crossover(self, c):
        newrepres = [self.__repres[i] if random.random() < 0.5 else c.__repres[i] for i in range(len(self.__repres))]
        offspring = Chromosome(self.__problParam)
        offspring.repres = newrepres
        return offspring
    
    def mutation(self):
        idx = generateNewValue(0, len(self.__repres) - 1)
        self.__repres[idx] = generateNewValue(0, max(self.__repres))
        
    def __str__(self):
        return '\nChromo: ' + str(self.__repres) + ' has fit: ' + str(self.__fitness)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness

