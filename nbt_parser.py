from nbtlib import Compound, List, ByteArray, IntArray, LongArray
import sys
from nbt import nbt


def parse_nbt(nbt_file: nbt.NBTFile):
    def nbt_to_dict(tag):
        if isinstance(tag, (Compound, List)):
            return {str(key): nbt_to_dict(value) for key, value in tag.items()}
        elif isinstance(tag, ByteArray):
            return list(tag)
        elif isinstance(tag, IntArray):
            return list(tag)
        elif isinstance(tag, LongArray):
            return list(tag)
        else:
            return tag.value

    try:
        nbt_dict = {}
        print(nbt_file.tags)
        for tag in nbt_file["Chunks"]:
            print(parse_nbt(tag))
        print(nbt_dict)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
