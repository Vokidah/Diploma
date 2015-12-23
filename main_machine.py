__author__ = 'vokidah'

class Automata():
    def __init__(self,dict):
        self.states = dict['states']
        self.inputs = dict['inputs']
        self.transfers_dict = dict['transfers']
        self.final_states = dict['final_states']
        self.first_state = self.states[0]
        self.correct_words = []
        self.incorrect_words = []

    def get_transition(self, curr_state, input_symbol):
        trans_list = self.transfers_dict[input_symbol]
        if curr_state in trans_list:
            return trans_list[curr_state]
        return None

    def get_words(self):
        f_c = open("correct_words", 'w')
        for word in self.correct_words:
            f_c.write(word+" ")
        f_c.close()
        f_i = open("incorrect_words","w")
        for word in self.incorrect_words:
            f_i.write(word+" ")
        f_i.close()

    def check(self, word):
        state = self.first_state
        for letter in word:
            if letter not in self.inputs:
                return False
            state = self.get_transition(state, letter)
        if state in self.final_states:
            self.correct_words.append(word)
            return True
        self.incorrect_words.append(word)
        return False
