from decibel.music_objects.chord import Chord
from decibel.music_objects.chord_vocabulary import ChordVocabulary
from decibel.music_objects.interval import Interval
from decibel.music_objects.pitch_class import PitchClass


class ChordAlphabet:
    def __init__(self, chord_vocabulary: ChordVocabulary):
        self.alphabet_list = ['N'] + [str(PitchClass(chord_template.key)) + chord_template.mode
                                      for chord_template in chord_vocabulary.chord_templates]
        self.chord_vocabulary_name = chord_vocabulary.name

    def _chord_to_str(self, chord: Chord) -> str:
        if chord is None:
            return 'N'
        intervals = chord.semitone_intervals_array
        if self.chord_vocabulary_name == 'MajorMinor' or self.chord_vocabulary_name == 'MajorMinorSevenths':
            # MAJOR and MINOR
            if intervals == [3, 7]:
                return str(chord.root_note) + 'm'
            elif self.chord_vocabulary_name == 'MajorMinor':
                return str(chord.root_note)
            # SEVENTHS
            elif intervals == [4, 7, 10]:
                return str(chord.root_note) + '7'
            elif intervals == [4, 7, 11]:
                return str(chord.root_note) + 'maj7'
            elif intervals == [3, 7, 10]:
                return str(chord.root_note) + 'm7'
            # OTHERS (not implemented yet)
            else:
                return str(chord.root_note)

        # TODO Implement for other chord vocabularies (e.g. augmented, diminished, suspended ...)

    def __len__(self):
        return len(self.alphabet_list)

    def __getitem__(self, item):
        return self.alphabet_list.__getitem__(item)

    def get_index_of_chord_in_alphabet(self, chord: Chord):
        """
        Given a Chord object, retrieve the index in the chord alphabet

        :param chord: Chord object for which we want to find the index
        :return: Index of this chord in the alphabet
        """
        chord_str = self._chord_to_str(chord)
        if chord_str not in self.alphabet_list:
            raise KeyError('Chord "{}" not in "{}" vocabulary.'.format(chord_str, self.chord_vocabulary_name))
        return self.alphabet_list.index(chord_str)
