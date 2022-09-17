#!/usr/bin/env python3
from typing import (
    List,
    Tuple,
    Union
)

from utils.eye_pattern import (
    EyePattern,
    EYE_PATTERN_1, 
    EYE_PATTERN_2, 
    EYE_PATTERN_3, 
    EYE_PATTERN_4
)

from utils.image import (
    ImageType,
    PackedImage,
    StrideImage,
)

from utils.function_tracer import FunctionTracer
import numpy as np

def convert_pattern(pattern: EyePattern) -> np.ndarray:
    """ Converts a pattern from tuple of strings to np.ndarray """

    res = np.zeros((5, 5), dtype=np.uint8)
    for ri, row in enumerate(pattern):
        elemets = np.array([e != ' ' for e in row])
        res[ri, :] = elemets.astype(np.uint8)
    return res

def calc_visual_hash(array: np.ndarray, start_x: int = 0, start_y:int = 0, *, thres:int = 199) -> int:
    """
    Calculates a hash function over a 5x5 grid of pixels with values grater than 'thres'

    hash = 0
    for y in range(start_y, start_y + 5):
        for x in range(start_x, start_x + 5):
            if array[y, x] > thres:
                _x = x - start_x
                _y = y - start_y
                hash += (_x + _y * _y)
    """

    assert start_y + 4 < array.shape[0] and start_x + 4 < array.shape[1]
    tmp = (array[start_y:start_y+5, start_x:start_x+5] > thres).nonzero()
    hash = np.sum(tmp[0] * tmp[0] + tmp[1])
    return hash

patterns = [convert_pattern(p) for p in [EYE_PATTERN_1, EYE_PATTERN_2, EYE_PATTERN_3, EYE_PATTERN_4]]
hashes = [calc_visual_hash(p, thres=0) for p in patterns]
pattern_dict = dict(zip(hashes, patterns))

def fix_red_eyes(image: StrideImage) -> np.ndarray:
    res = image.resolution
    pixels_red = image.pixels_red.copy()
    for y in range(res.height - 5):
        for x in range(res.width - 5):
            if pixels_red[y, x] >= 200 and pixels_red[y, x+4] >= 200:
                hash = calc_visual_hash(pixels_red, x, y)
                if hash in pattern_dict:
                    pat = pattern_dict[hash]
                    pixels_red[y:y+5, x:x+5] = pixels_red[y:y+5, x:x+5] - 150 * pat

    return pixels_red

def compute_solution(images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    from multiprocessing import Pool, cpu_count

    with Pool(cpu_count()) as p:
        results = []
        for img in images:
            results.append(p.apply_async(fix_red_eyes, (img, )))

        for r, i in zip(results, images):
            i.pixels_red = r.get()

    del ft

