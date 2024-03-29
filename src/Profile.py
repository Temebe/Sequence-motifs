import numpy as np

from nucleotide import nucleotide_index, nucleotide_letter


def get_max_probability(probabilities):
    max_value = max(probabilities)
    for i in range(4):
        if probabilities[i] == max_value:
            return nucleotide_letter[i]


class Profile:
    """Class that stores motif and is able to adjust dynamically

    This class is used to store information about given sequences. It knows how often certain nucleotide appeared at
    certain position (self.counts) and based on this it calculates probability of appearing chosen nucleotide on this
    spot. It is later used to calculate matching score, which basically tells us just how it is likely that given
    sequence belongs to motif represented by this profile.
    """

    def __init__(self, seq_size):
        # counts tells us how many times certain nucleotide was in certain spot
        self.counts = np.zeros((seq_size, 4))
        # probabilities are self-explanatory
        self.probabilities = np.zeros((seq_size, 4))
        # seq_amount is amount of sequences used to build profile
        self.seq_amount = 0
        # size determines size of sequences used to build profile
        self.seq_size = seq_size

    def load_sequences(self, sequences):
        for sequence in sequences:
            self.load_sequence(sequence, False)
        self.calculate_probabilities()

    def load_sequence(self, sequence, recalculate=True):
        if len(sequence) != self.seq_size:
            return
        for i, char in enumerate(sequence):
            self.counts[i][nucleotide_index[char]] += 1
        self.seq_amount += 1
        if recalculate:
            self.calculate_probabilities()

    def calculate_probabilities(self):
        for position in range(self.seq_size):
            for nucleotide in range(4):
                count = self.counts[position][nucleotide]
                self.probabilities[position][nucleotide] = count / self.seq_amount if self.seq_amount > 0 else 0

    def calculate_matching(self, sequence):
        if len(sequence) != self.seq_size:
            raise ValueError("Improper length of sequence")
        # If profile doesn't have any sequences loaded than any new sequence is 100% match with this profile
        if self.seq_amount == 0:
            return 1
        match = 0
        for pos, char in enumerate(sequence):
            probability = self.probabilities[pos][nucleotide_index[char]]
            match += probability
        # Scaling score so it is in range from 0 to 1
        match = match / self.seq_size
        return match

    def get_complex_motif(self):
        motif = ""
        for pos in range(self.seq_size):
            tmp = ""
            for char in ['A', 'C', 'G', 'T']:
                if self.counts[pos][nucleotide_index[char]] > 0:
                    tmp += char

            if len(tmp) > 1:
                motif += "[" + tmp + "]"
            else:
                motif += tmp
        return motif

    def get_motif(self):
        motif = ""
        for pos in range(self.seq_size):
            motif += get_max_probability(self.probabilities[pos])
        return motif


if __name__ == "__main__":
    profile = Profile(5)
    example_sequences = ["ATAGT", "ACGGT", "ATAGT", "ATAGT"]
    profile.load_sequences(example_sequences)
    print("Order:\nA\nT\nG\nC")
    print("Probabilities:")
    print(profile.probabilities.transpose())
    print("Score of matching AGATC to profile: " + str(profile.calculate_matching("AGATC")))
    print(profile.get_motif())
