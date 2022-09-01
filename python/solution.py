#!/usr/bin/env python3

from typing import (
    List,
    Tuple,
    Union
)

from utils.image import (
    ImageType,
    PackedImage,
    StrideImage,
)

from utils.function_tracer import FunctionTracer

def fix_image(image: StrideImage):
    """
    Levaraging the fact that all patterns are 5x5 squares and are not intersecting or partial
    And the fact that we don't have pixels with values above 200 that do not belong to the pattern
    We can scan the image to find the upper left pixel of each pattern occurance and then just 
    subtract 150 from each pixel with value above 200 in 5x5 block
    """
    res = image.resolution

    def to_image_idx(x, y):
        return y * res.width + x

    for y in range(res.height):
        for x in range(res.width):
            idx = to_image_idx(x, y)
            pix = image.pixels_red[idx]
            if pix >= 200:
                for py in range(5):
                    for px in range(5):
                        tmp_idx = to_image_idx(x + px, y + py)
                        tmp = image.pixels_red[tmp_idx]
                        if tmp >= 200:
                            image.pixels_red[tmp_idx] = tmp - 150

def fix_image2(image: StrideImage):
    """
    Optimization of fix_image() by removing the direct indexing of pixels and replacing
    it with list slices
    """
    res = image.resolution

    def get_row(row_idx: int):
        return image.pixels_red[row_idx*res.width:(row_idx+1)*res.width]

    def write_row(row_idx: int, data: List[int]):
        image.pixels_red[row_idx*res.width:(row_idx+1)*res.width] = data

    for ri in range(res.height):
        row = get_row(ri)
        for pi, pix in enumerate(row):
            if pix >= 200:
                for pat_ri in range(ri,ri+5):
                    pattern_row = get_row(pat_ri)
                    pattern_row[pi:pi+5] = (p if p < 200 else p - 150 for p in pattern_row[pi:pi+5])
                    write_row(pat_ri, pattern_row)

def fix_image3(image: StrideImage):
    """ really !?! """
    image.pixels_red = list(p if p < 200 else p - 150 for p in image.pixels_red)

def compute_solution(images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    for img in images:
        fix_image2(img)

    del ft
            