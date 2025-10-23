import mutagen
from mutagen.id3 import ID3
from pathlib import Path

def _input_music_directory() -> Path | None:
    music_directory: None | Path = None
    while not music_directory:
        input_text = input("Absolute path to the directory where the music files are located: ")
        if Path(input_text).is_dir():
            music_directory = Path(input_text)
            break
        else:
            print("❌ INVALID DIRECTORY")
            continue
    return music_directory


class Music:
    def __init__(self, path: Path) -> None:
        self.path: Path = path
        self.file = mutagen.File(path)
        self.title: str = self.file['TIT2']
        self.artist: str = self.file['TPE1']
        self.album: str = self.file['TALB']
        self.year: str = self.file['TDRC']
        self.length: int = self.file.info.length

class Track_List:
    """
    Represents a track list
    """
    def __init__(self, list_path: Path) -> None:
        self._path: Path = list_path
        self._report_file: Path = self._path / "report.txt"
        self._music_list: list[Music] = []
        self._find_tracks()
        for track in self._music_list:
            print(track.artist, track.title, track.album, track.year, track.length // 60)

    @property
    def length(self) -> int:
        total_length = 0
        for track in self._music_list:
            total_length += track.length
        return total_length


    def _find_tracks(self) -> None:
        if not self._path.glob("*.mp3"):
            raise Exception(f"No .mp3 file found in {self._path}")
        for track_path in self._path.glob("*.mp3"):
            music = Music(track_path)
            self._music_list.append(music)

    def _process_music_file(self, music: Music) -> bool:
        pass


def main():
    music_directory = _input_music_directory()
    track_list = Track_List(music_directory)

if __name__ == "__main__":
    main()




