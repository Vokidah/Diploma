__author__ = 'vokidah'

'''
    original automata with help of it we generate correct/incorrect words
     that we'll use to teach our new automata
'''


class Automata():
    # Set our data from JSON file
    def __init__(self, dict):
        self.states = dict['states']
        self.inputs = dict['inputs']
        self.transfers_dict = dict['transfers']
        self.final_states = dict['final_states']
        self.first_state = self.states[0]
        self.correct_words = []
        self.incorrect_words = []

    # transfer from current state to another
    def get_transition(self, curr_state, input_symbol):
        trans_list = self.transfers_dict[input_symbol]
        if curr_state in trans_list:
            return trans_list[curr_state]
        return None

    # separating words in 2 categories
    def set_words(self):
        f_c = open("correct_words", 'w')
        for word in self.correct_words:
            f_c.write(word + " ")
        f_c.close()
        f_i = open("incorrect_words", "w")
        for word in self.incorrect_words:
            f_i.write(word + " ")
        f_i.close()

    #  checking word for correctness
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
