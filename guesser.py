import random

class WordleGuesser:
    def __init__(self):
        self.words = self.get_words()
        self.guesses = []
        self.correct = []
        self.present = []
        self.absent = []

    def get_words(self):
        with open('words.txt') as word_file:
            words = word_file.readlines()
            words = [word.replace('\n', '') for word in words]

        return words

    def guess_word(self):
        guess = random.choice(self.words)
        self.guesses.append(guess)

        return guess

    # result is a list like this: ['absent', 'present', 'correct', 'absent', 'absent']
    def set_guess_result(self, result: list):
        last_guess = self.guesses[-1]

        for i, res in enumerate(result):
            if res == 'absent':
                self.absent.append(last_guess[i])
            elif res == 'present':
                self.present.append(
                    {
                        'index': i,
                        'letter': last_guess[i]
                    }
                )
            else:
                self.correct.append(
                    {
                        'index': i,
                        'letter': last_guess[i]
                    }
                )

        self.update_word_list()

    # update words available based on results of guesses
    def update_word_list(self):
        updated_words = []

        for word in self.words:
            # ignore words from previous guesses
            if word not in self.guesses:
                # check correct, present and absent and find words that are possible
                is_word_possible = True

                for c in self.correct:
                    if word[c['index']] != c['letter']:
                        is_word_possible = False

                for p in self.present:
                    if p['letter'] not in word or word[p['index']] == p['letter']:
                        is_word_possible = False

                for a in self.absent:
                    if a in word:
                        is_word_possible = False

                if is_word_possible:
                    updated_words.append(word)

        self.words = updated_words
