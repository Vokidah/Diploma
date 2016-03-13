__author__ = 'vokidah'

from main_machine import Automata
from new_machine import Machine
import random
import decimal
import json


# loading data from JSON file
def read_json(json_path):
    return json.loads(open(json_path).read())


def create_hash(machine):
    hash = {}
    for input in machine.inputs:
        hash[input] = {}
        for state in machine.states:
            hash[input][state] = False
    return hash


def compare(machine1, machine2, state1, state2, hash1, hash2):
    if len(machine1.states)==len(machine2.states):
        if (state1 in machine1.final_states and state2 in machine2.final_states) or (state1 not in machine1.final_states and state2 not in machine2.final_states):
            for input in machine1.inputs:
                if hash1[input][state1] == False and hash2[input][state2] == False:
                    next_state1 = machine1.get_transition(state1, input)
                    next_state2 = machine2.get_transition(state2, input)
                    hash1[input][state1] = True
                    hash1[input][state2] = True
                    if not compare(machine1, machine2, next_state1, next_state2, hash1, hash2):
                        return False
            return True
    return False


# getting data from text file
def get_words(words_path):
    f = open(words_path, 'r')
    words = f.read().split(" ")
    return words




path = "./Data/automata2.json"
json_path = read_json(path)
automata = Automata(json_path)

for i in range(1, 100000):
    string = ''.join(random.choice("".join(automata.inputs)) for x in range(random.randint(1, 2*len(automata.states))))
    automata.check(string)
automata.set_words()

iterations = 0
while True:
    mac = Machine(automata.inputs)
    mac.build(get_words("./Data/correct_words")[:-1])
    mac.hopcroft_minimization()
    mac. uncheck_wrong(get_words("./Data/incorrect_words")[:-1], mac.first_state)
    mac.hopcroft_minimization()
    iterations += 1
    if compare(automata, mac, automata.first_state, mac.first_state, create_hash(automata), create_hash(mac)):
        break
print(automata.transfers)
print(mac.transfers)
print "Iterations %s"%iterations