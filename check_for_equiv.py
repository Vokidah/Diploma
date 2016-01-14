__author__ = 'vokidah'

from main_machine import Automata
from new_machine import Machine
import random
import decimal
import json


# loading data from JSON file
def readJSON(json_path):
    return json.loads(open(json_path).read())


# getting data from text file
def get_words(words_path):
    f = open(words_path, 'r')
    words = f.read().split(" ")
    return words


path = "/home/vokidah/Documents/Diploma/automata.json"
Json_path = readJSON(path)
automata = Automata(Json_path)
for i in range(1, 10000):
    string = ''.join(random.choice("".join(automata.inputs)) for x in range(random.randint(1, 2*len(automata.states))))
    automata.check(string)

automata.set_words()
iterations = 0
result = None

while result != 1:
    mac = Machine(automata.inputs)
    mac.build(get_words("correct_words")[:-1])
    mac.hopcroft_minimization()
    n = 100
    count = 0
    for i in range(0, n):
        string = ''.join(random.choice("".join(automata.inputs)) for x in range(random.randint(16, 21)))
        if mac.check(string) == automata.check(string):
            count += 1
    result = decimal.Decimal(count) / decimal.Decimal(n)
    print result
    iterations += 1
print ''
print "Iterations %s"%iterations
print ''
mac.hopcroft_minimization()
print "Origin %s / Made %s"%(len(automata.states),len(mac.states))
mac.show()
