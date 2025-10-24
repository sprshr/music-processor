from pathlib import Path

import mutagen


def _input_music_directory() -> Path:
    """
    Inputs an absolute path containing the mp3 files.
    Returns a Path or keeps asking until a valid path is presented
    :return:
    """
    music_directory: None | Path = None
    while not music_directory:
        input_text = input(
            "Absolute path to the directory where the music files are located: ")
        if Path(input_text).is_dir():
            music_directory = Path(input_text)
            break
        else:
            print("❌ INVALID DIRECTORY")
            continue
    return music_directory


class Music:
    """
    Represents a music file
    """

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

    def _rename_music(self, music: Music, new_title: str) -> Path:
        target = self._path / f"{new_title}.mp3"
        music.path.rename(target)
        music.path = target
        return target

    def process_music_files(self) -> None:
        """Renames music files and orders music files"""
        for n in range(len(self._music_list)):
            music = self._music_list[n]
            new_title: str = f'{n + 1}. {music.title} - {music.album} - {music.year}'
            self._rename_music(music, new_title)

    def generate_report(self):
        with open(self._path / "track-list.txt", "w") as file:
            file.write('Track List\n')
            file.write('Author: Sepehr Sahraian\n')
            file.write(f'Total Length: {self.length // 60}\n')
            file.write(f'Number of Tracks: {len(self._music_list)}\n')
            file.write('---***---***---***---')
            file.write('\n')
            file.write('\n')
            for n in range(len(self._music_list)):
                music = self._music_list[n]
                file.write(f'{n + 1}. {music.title}\n')
                file.write(f'  Artist: {music.artist}\n')
                file.write(f'  Album: {music.album}\n')
                file.write(f'  Year: {music.year}\n')
                file.write(f'  Length: {music.length // 60} min\n\n')


def main():
    music_directory = _input_music_directory()
    track_list = Track_List(music_directory)
    track_list.process_music_files()
    track_list.generate_report()


if __name__ == "__main__":
    main()
