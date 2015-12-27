__author__ = 'vokidah'
import random
import itertools


class Machine:

    # Initialization of new automata
    def __init__(self):
        self.inputs = ["a", "b"]
        self.i = 0
        self.transfers = {}
        for each in self.inputs:
            self.transfers[each] = {"Gb": "Gb"}
        self.first_state = str(self.i);
        self.i += 1
        self.final_states = []
        self.states = [self.first_state, "Gb"]

    # printint
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
        if not self.transfer_move(state, letter):
            new_state = str(self.i)
            self.i+=1
            self.states.append(new_state)
            if letter in self.transfers:
                self.transfers[letter][state] = new_state
            else:
                self.transfers[letter] = {state: new_state}
            return new_state
        else:
            return self.transfer_move(state, letter)

    # transfer from current state to another
    def transfer_move(self, state, letter):
        if state not in self.transfers[letter]:
            return None
        return self.transfers[letter][state]

    # transfer from current state to the garbage state
    def move_to_garbage(self, state, letter):
        self.transfers[letter][state] = "Gb"
        return "Gb"

    # process of creating our automata
    def build(self, words, state=None):
        if not state or state == "Gb":
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
            else:
                if state not in self.final_states:
                    self.final_states.append(state)
        for letter in self.inputs:
            if letter in words_hash:
                next_state = self.new_transfer(state, letter)
                if '' in words_hash[letter]:
                    if next_state not in self.final_states:
                        self.final_states.append(next_state)
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
            state = self.transfer_move(state, letter)
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
                    new_state = self.transfer_move(each, letter)
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
                to_state = self.transfer_move(state, letter)
                if to_state == garbage_state:
                    id = random.randint(0, len(self.states)-1)
                    self.transfers[letter][state] = self.states[id]

    # joining two states
    def combine(self, a, b):
        return (a, b)

    # minimizing our automata
    def minimization(self):
        F = self.final_states
        NF = [x for x in self.states if x not in self.final_states]
        all_states = [x for x in self.states]
        marked = list(itertools.product(F, NF))
        unmarked = [self.combine(i, j) for i in F for j in F] + [self.combine(i, j) for i in NF for j in NF]
        while True:
            len_for_check = len(marked)
            for each in unmarked:
                for letter in self.inputs:
                    first_state = self.transfer_move(each[0], letter)
                    second_state = self.transfer_move(each[1], letter)
                    if (first_state, second_state) in marked or (second_state, first_state) in marked:
                        marked.append(each)
                        unmarked.remove(each)
                        break
            if len_for_check == len(marked):
                break

        new_states = []
        while unmarked:
            pair = unmarked[0]
            unmarked.remove(pair)
            if not new_states:
                new_states.append([pair[0], pair[1]])
                if pair[0] == pair[1]:
                    all_states.remove(pair[0])
                else:
                    all_states.remove(pair[0])
                    all_states.remove(pair[1])
            else:
                check = False
                for each in new_states:
                    if pair[0] in each:
                        check = True
                        if pair[1] not in each:
                            each.append(pair[1])
                            all_states.remove(pair[1])
                    elif pair[1] in each:
                        check = True
                        if pair[0] not in each:
                            each.append(pair[0])
                            all_states.remove(pair[0])
                if not check:
                    new_states.append([pair[0], pair[1]])
                    if pair[0] == pair[1]:
                        all_states.remove(pair[0])
                    else:
                        all_states.remove(pair[0])
                        all_states.remove(pair[1])
        for each in all_states:
            new_states.append([each])
        new_hash = self.create_new_transfers_hash(new_states)
        garbage_state = self.create_new_transfers(new_hash)
        self.make_new_transfers(garbage_state)



'''


    def split(self, X, Y):
        intersection = []
        subtraction = []
        for y in Y:
            for x in X:
                if x == y:
                    intersection.append(x)
        for each in Y:
            if each not in intersection:
                subtraction.append(each)
        if intersection == [] or subtraction == []:
            if Y:
                if isinstance(Y[-1], list):
                    result = self.split(X, Y[-1])
                    if result:
                        for each in Y[:-1]:
                            result.append(each)
                    return result

            return None
        else:
            return [intersection, subtraction]

    def separate_equiv(self, all_states):

        for letter in self.inputs:
            new_hash = {}
            i = 0
            for each in all_states:
                new_hash[i] = each
                i+=1
            whole_seperations = []
            for states in all_states:
                my_hash = {}
                for each in states:
                    new_state = self.transfer_move(each, letter)
                    for key in new_hash.keys():
                        if new_state in new_hash[key]:
                            if key not in my_hash:
                                my_hash[key] = [each]
                            else:
                                my_hash[key].append(each)
                to_seperate = []
                for each in my_hash.keys():
                    if my_hash[each] not in to_seperate:
                        to_seperate.append(my_hash[each])
                if len(to_seperate)>1:
                    whole_seperations.append((states, to_seperate))
            for states,seperation in whole_seperations:
                all_states.remove(states)
                for each in seperation:
                    all_states.append(each)
        return all_states


def minimize(self):
        P = [[], []]
        W = [[], []]
        for each in self.states:
            if each in self.final_states:
               W[0].append(each)
               P[0].append(each)
            else:
                W[1].append(each)
                P[1].append(each)
        while len(W) != 0:
            S = W[0]
            W.remove(S)
            for letter in self.inputs:
                L = []
                for each in self.states:
                    state = self.transfer_move(each, letter)
                    if state not in L and state in S:
                        L.append(each)
                if L:
                    for i, R in enumerate(P):
                        result = self.split(L, R)
                        if result:
                            P[i] = result
                            if R in W:
                                W.remove(R)
                                W.append(result)
                            else:
                                if len(result[0]) <= len(result[1]):
                                    W.append(result[0])
                                else:
                                    W.append(result[1])
        all_states = []
        for i in range(0,len(P)):
            if isinstance(P[i][0], list):
                for each in P[i]:
                    all_states.append(each)
            else:
                all_states.append(P[i])
        all_states = self.separate_equiv(all_states)
        new_hash = self.create_new_transfers_hash(all_states)
        garbage_state = self.create_new_transfers(new_hash)
        self.make_new_transfers(garbage_state)
'''