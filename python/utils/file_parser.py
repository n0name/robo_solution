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
from utils.pixel import (
    Pixel,
    parse_pixel,
)
from utils.resolution import Resolution
from utils.function_tracer import FunctionTracer
import numpy as np
    
def generate_io_data(input_file_name: str, output_file_name: str, image_type: ImageType) -> \
    Tuple[List[Union[PackedImage, StrideImage]], List[Union[PackedImage, StrideImage]]]:
    ft = FunctionTracer("generate_io_data", "seconds //not included into solution timings")

    input_data = generate_data(input_file_name, image_type)
    output_data = generate_data(output_file_name, image_type) 
    del ft
    
    return input_data, output_data
    

def generate_data(file_name: str, image_type: ImageType) -> List[Union[PackedImage, StrideImage]]:
    images: List[Union[PackedImage, StrideImage]] = []
    with open(file_name) as f:
        images_num: int = int(f.readline())
        
        for _ in range(images_num):
            tokens = f.readline().split()
            width: int = int(tokens[0])
            height: int = int(tokens[1])
            resolution: Resolution = Resolution(width, height)

            num_pixels: int = width*height
            tmp = np.fromstring(f.readline().strip(), dtype=np.uint32, count=num_pixels, sep=' ')
            tmp = tmp.reshape((height, width))
            pixels = np.zeros((height, width, 4), dtype=np.uint8)
            pixels[:, :, 0] = (tmp >> 24).astype(np.uint8)
            pixels[:, :, 1] = (tmp >> 16).astype(np.uint8)
            pixels[:, :, 2] = (tmp >> 8).astype(np.uint8)
            pixels[:, :, 3] = (tmp >> 0).astype(np.uint8)
            
            
            if image_type == ImageType.PackedImageType:
                packed_image: PackedImage = PackedImage(resolution, pixels)
                images.append(packed_image)
            else:
                stride_image: StrideImage = StrideImage(resolution, pixels)
                images.append(stride_image)
                
    return images

def print_images(images: List[Union[PackedImage, StrideImage]]) -> None:
    for index, image in enumerate(images):
        print(f"\n image{index}")
        print(f"{image}")