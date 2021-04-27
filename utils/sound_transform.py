import os
from pydub import AudioSegment


def transform(path, new_format, replace=False):
    audio = AudioSegment.from_file(path)
    name = os.path.basename(path).split('.')[0] + '.' + new_format
    new_path = os.path.join(os.path.dirname(path), name)
    audio.export(new_path, new_format)
    if replace:
        os.remove(path)
