import librosa


class Song:
    def __init__(
            self,
            key: str = None,
            title: str = None,
            album: str = None,
            artist: str = None,
            full_ground_truth_chord_labs_path: str = None,
            full_audio_path: str = None,
            full_segmentation_labs_path: str = None):
        """
        Create a new song. All information we extract from any representation of this song, is added to the Song object

        :param key: Integer key of this song - we use this for matching all representations of the song
        :param title: Title of the song
        :param album: Album on which the song appears
        :param full_ground_truth_chord_labs_path: Path to ground truth chord labels
        :param full_audio_path: Path to the audio file
        :param full_segmentation_labs_path: Path to the segmentation label file
        """
        # Key, title, album and ground truth chord_labs_path are known from the beginning
        self.audio_features_path = None
        self.key = str(key)
        self.tempo = None
        self.beat_times = []
        self.beat_frames = []
        self.chords_order = []
        self.chords_times = []
        self.title = title
        self.album = album
        self.artist = artist
        self.full_ground_truth_chord_labs_path = full_ground_truth_chord_labs_path
        self.full_audio_path = full_audio_path
        self.full_segmentation_labs_path = full_segmentation_labs_path
        self.duration = librosa.get_duration(filename=self.full_audio_path)

        # Tab paths, midi paths and ground truth chord labels are filled by get_all_songs
        self.full_midi_paths = []
        self.full_tab_paths = []
        self.full_chordify_chord_labs_path = ''
        self.full_mirex_chord_lab_paths = dict()

    def __str__(self):
        return 'Song {} ({} from {})'.format(str(self.key), self.title, self.album)

    def add_midi_path(self, full_midi_path):
        self.full_midi_paths.append(full_midi_path)

    def add_tab_path(self, full_tab_path):
        self.full_tab_paths.append(full_tab_path)