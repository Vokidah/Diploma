__author__ = 'vokidah'
import random


class Machine:

    # Initialization of new automata
    def __init__(self, inputs):
        self.inputs = inputs
        self.i = 0
        self.transfers = {}
        for each in self.inputs:
            self.transfers[each] = {"Gb": "Gb"}
        self.first_state = str(self.i);
        self.i += 1
        self.final_states = []
        self.states = [self.first_state, "Gb"]

    # printing
    def show(self):
        print ''
        print len(self.states)
        print self.transfers
        print self.states
        print self.final_states
        print ''
        return

    # creation of new transfer or transfer if it exists
    def new_transfer(self, state, letter, new_state=None):
        if not self.get_transition(state, letter):
            new_state = str(self.i)
            self.i += 1
            self.states.append(new_state)
            if letter in self.transfers:
                self.transfers[letter][state] = new_state
            else:
                self.transfers[letter] = {state: new_state}
            return new_state
        else:
            return self.get_transition(state, letter)

    # transfer from current state to another
    def get_transition(self, state, letter):
        if state not in self.transfers[letter]:
            return None
        return self.transfers[letter][state]

    # transfer from current state to the garbage state
    def move_to_garbage(self, state, letter):
        self.transfers[letter][state] = "Gb"
        return "Gb"

    # process of creating our automata
    def build(self, words, state=None):
        if not state:
            state = self.first_state
        words_hash = {}
        for word in words:
            if word != '':
                head = word[0]
                tail = word[1:]
                if head in self.inputs:
                    if head not in words_hash:
                        words_hash[head] = [tail]
                    else:
                        words_hash[head].append(tail)
            elif state not in self.final_states:
                self.final_states.append(state)

        for letter in self.inputs:
            if letter in words_hash:
                next_state = self.new_transfer(state, letter)
                self.build(words_hash[letter], next_state)
            else:
                self.move_to_garbage(state, letter)

    #  checking word for correctness
    def check(self, word):
        state = self.first_state
        path = [state]
        for letter in word:
            if letter not in self.inputs:
                return False
            state = self.get_transition(state, letter)
            path.append(state)
        if state in self.final_states:
            return True
        return False

    # creation of the hash that will have new states as a key and list of old_states as a value
    def create_new_transfers_hash(self, all_states):
        new_hash = {}
        new_states = []
        new_final_states = []
        first_state = self.first_state
        all_old_states = []
        for array in all_states:
            new_state = "q%s"%self.i
            self.i += 1
            new_hash[new_state] = array
            all_old_states.append(array)
            new_states.append(new_state)
            if array[0] in self.final_states:
                new_final_states.append(new_state)
            if self.first_state in array:
                self.first_state = new_state
        self.states = new_states
        self.final_states = new_final_states

        return new_hash

    # X contains in Y
    def contains(self, X, Y):
        what_contains = []
        for x in X:
            if x in Y:
                return True
        return False

    def create_new_transfers(self, new_hash):
        garbage_state = None
        new_transfers = {}
        for letter in self.inputs:
            new_transfers[letter] = {}
        for state in self.states:
            if 'Gb' in new_hash[state]:
                garbage_state = state
            for letter in self.inputs:
                X = []
                for each in new_hash[state]:
                    new_state = self.get_transition(each, letter)
                    if new_state not in X:
                        X.append(new_state)
                for another in self.states:
                    if self.contains(X, new_hash[another]):
                        new_transfers[letter][state] = another
        self.transfers = new_transfers
        return garbage_state

    # redirection of all states that lead to the garbage state to another random state
    def make_new_transfers(self, garbage_state):
        if garbage_state in self.states:
            self.states.remove(garbage_state)
        for letter in self.inputs:
            if garbage_state in self.transfers[letter]:
                del self.transfers[letter][garbage_state]
            for state in self.states:
                if state == garbage_state:
                    del self.transfers[letter][state]
                to_state = self.get_transition(state, letter)
                if to_state == garbage_state:
                    id = random.randint(0, len(self.states)-1)
                    self.transfers[letter][state] = self.states[id]

    def uncheck_wrong(self, words, state=None):
        if not state:
            state = self.first_state
        words_hash = {}
        for word in words:
            if word != '':
                head = word[0]
                tail = word[1:]
                if head in self.inputs:
                    if head not in words_hash:
                        words_hash[head] = [tail]
                    else:
                        words_hash[head].append(tail)
            elif state in self.final_states:
                    self.final_states.remove(state)
        for letter in self.inputs:
            if letter in words_hash:
                next_state = self.get_transition(state, letter)
                self.uncheck_wrong(words_hash[letter], next_state)
            else:
                return

    # minimizing our automata
    def hopcroft_minimization(self):
        W  = [[x for x in self.final_states]]
        P = [[x for x in self.final_states], [x for x in self.states if x not in self.final_states]]
        while W:
            A = W[0]
            W.remove(W[0])
            for letter in self.inputs:
                X = []
                for each in self.states:
                    new_state = self.get_transition(each, letter)
                    if new_state in A and each not in X:
                        X.append(each)
                if X:
                    for Y in P:
                        result = self.split(X, Y)
                        if result:
                            P.remove(Y)
                            P.append(result[0])
                            P.append(result[1])
                            if Y in W:
                                W.remove(Y)
                                W.append(result[0])
                                W.append(result[1])
                            else:
                                if len(result[0]) <= len(result[1]):
                                    W.append(result[0])
                                else:
                                    W.append(result[1])
        new_hash = self.create_new_transfers_hash(P)
        garbage_state = self.create_new_transfers(new_hash)
        self.make_new_transfers(garbage_state)

    def split(self, X, Y):
        intersection = []
        subtraction = [y for y in Y]
        for x in X:
            if x in Y:
                intersection.append(x)
                subtraction.remove(x)
        if intersection and subtraction:
            return [intersection, subtraction]
        return None

