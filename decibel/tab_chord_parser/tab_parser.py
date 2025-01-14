import decibel.music_objects.untimed_chord_sequence
from decibel.import_export.untimed_chord_sequence_io import write_untimed_chord_sequence
from decibel.music_objects.song import Song
from decibel.music_objects.untimed_chord_sequence import UntimedChordSequence
from decibel.music_objects.untimed_chord_sequence_item import UntimedChordSequenceItem
from decibel.tab_chord_parser.tab_line_classifier import classify_lines
from decibel.tab_chord_parser.tab_segmenter import segment_line_list


def classify_tabs_from_file(tab_path: str) -> UntimedChordSequence:
    # Find all line types for this tab
    classified_lines = classify_lines(tab_path)
    # Segment them (by empty LineTypes)
    segments = segment_line_list(classified_lines)

    untimed_chord_sequence = UntimedChordSequence()
    # Start with No chord symbol
    untimed_chord_sequence.add_untimed_chord_sequence_item(UntimedChordSequenceItem.no_chord_symbol(0))
    line_nr = 1
    for segment in segments:
        for system in segment.systems:
            chords = system.chords
            for chord_x, chord in chords:
                # Add each chord line from each system in each segment
                untimed_chord_sequence.add_untimed_chord_sequence_item(
                    UntimedChordSequenceItem(line_nr, segment.segment_nr, system.system_nr, chord_x, str(chord)))
            line_nr += 1
    # End with No chord symbol
    untimed_chord_sequence.add_untimed_chord_sequence_item(UntimedChordSequenceItem.no_chord_symbol(line_nr))

    return untimed_chord_sequence


def classify_all_tabs_of_song(
        song: Song,
        intermediate_parsed_chords_path: str = None,
        input_song_tab_path: str = None) -> decibel.music_objects.untimed_chord_sequence.UntimedChordSequence:
    """
    Classify all tabs of a song, by (1) LineType classification; (2) Segmenting lines; (3) System and Chord extraction.
    
    :param song: A Song in our data set, for which we want to parse all tabs
    :param intermediate_parsed_chords_path: The path to where the internally used chords path file should be written to
    :param input_song_tab_path: The path of the input song tab .txt file
    """
    write_path = ""
    file_exists = True
    tab_path = None
    if intermediate_parsed_chords_path is not None:
        write_path = intermediate_parsed_chords_path
        tab_path = input_song_tab_path
    else:
        from decibel.import_export import filehandler
        for tab_path in song.full_tab_paths:
            write_path = filehandler.get_chords_from_tab_filename(tab_path)
        file_exists = filehandler.file_exists(write_path)
    if file_exists:
        untimed_chord_sequence = classify_tabs_from_file(tab_path)
        write_untimed_chord_sequence(write_path, untimed_chord_sequence)
        return untimed_chord_sequence

