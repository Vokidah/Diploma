__author__ = 'vokidah'
from main_machine import Automata
from new_machine import Machine
import random
import decimal
import json

def readJSON(path):
    return json.loads(open(path).read())


def get_words(path):
    f = open(path, 'r')
    words = f.read().split(" ")
    return words


path = "/home/vokidah/Documents/Diploma/automata.json"
json_path = readJSON(path)
automata = Automata(json_path)
for i in range(1, 10000):
    string = ''.join(random.choice("ab") for x in range(random.randint(1, 6)))
    automata.check(string)

automata.get_words()
print "LET'S GET IT"
iterations = 0
result = None

while result != 1:
    mac = Machine()
    mac.build(get_words("correct_words")[:-1])
    mac.minimization()
    n = 100
    count = 0
    for i in range(0, n):
        string = ''.join(random.choice("ab") for x in range(random.randint(9, 11)))
        if mac.check(string) == automata.check(string):
            count+=1
    result = decimal.Decimal(count)/decimal.Decimal(n)
    print result
    iterations += 1
mac.minimization()
print ''
print iterations
print ''

print automata.transfers_dict
print automata.first_state
print automata.states
print ''
print mac.transfers
print mac.first_state
print mac.states
