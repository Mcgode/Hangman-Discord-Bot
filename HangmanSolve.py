
class HangmanSolve:
    number_of_letters = 0
    selection = []
    used_letters = []
    last_input = ''

    def __init__(self, number_of_letters):
        self.number_of_letters = number_of_letters
        with open('./List.txt', 'r') as f:
            for line in f:
                self.selection.append(line.rstrip('\n').upper())
        self.remove_by_letter_amount()
        self.last_input = "◯" * number_of_letters
        self.used_letters = []
        self.last_input = ''

    def remove_by_letter_amount(self):
        i = 0
        while i < len(self.selection):
            if len(self.selection[i].replace(' ', '').replace('-', '').replace('.', '')) == self.number_of_letters:
                i += 1
            else:
                self.selection.pop(i)

    def next_discriminative_letter(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        repartitions = []

        for letter in alphabet:
            repartition = [0, 0]
            for e in self.selection:
                if letter in e:
                    repartition[0] += 1
                else:
                    repartition[1] += 1
            repartitions.append(repartition)

        ranking = {}
        for i, e in enumerate(repartitions):
            diff = abs(e[0] - e[1])
            if diff not in ranking and alphabet[i] not in self.used_letters:
                ranking[diff] = i

        return alphabet[ranking[min(ranking.keys())]]

    def parse_input(self, input_str, last_letter):
        self.used_letters.append(last_letter)
        indexes = [i for i, e in enumerate(input_str) if e == last_letter]
        i = 0
        while i < len(self.selection):
            if indexes == [
                i
                for i, e in enumerate(self.selection[i].replace(' ', '').replace('-', '').replace('.', ''))
                if e == last_letter
            ]:
                i += 1
            else:
                self.selection.pop(i)
        print("{0} possibilities: {1}".format(len(self.selection), self.selection))
        print("{0} used letters: {1}".format(len(self.used_letters), self.used_letters))
        print('----------------------')
