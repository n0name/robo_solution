#!/usr/bin/env python3

from typing import List
from utils.resolution import Resolution
from enum import Enum
import numpy as np


class ImageType(Enum):
    PackedImageType = 0
    StrideImageType = 1

class PackedImage:
    def __init__(self, resolution: Resolution, pixels: np.ndarray):
        self.resolution: Resolution = resolution
        self.pixels: np.ndarray = pixels
    
    def __str__ (self):
        return str(self.resolution) + '\n' + ' '.join(str(p) for p in self.pixels[:, :])

    def __eq__(self, other):
        return self.resolution == other.resolution and np.all(self.pixels == other.pixels)

class StrideImage:
    def __init__(self, resolution: Resolution, pixels: np.ndarray):
        self.resolution: Resolution = resolution
        self.pixels_red: np.ndarray = np.zeros((resolution.height, resolution.width))
        self.pixels_green: np.ndarray = np.zeros((resolution.height, resolution.width))
        self.pixels_blue: np.ndarray = np.zeros((resolution.height, resolution.width))
        self.pixels_alpha: np.ndarray = np.zeros((resolution.height, resolution.width))
        
        self.__split_pixel_components(pixels)

    def merge_pixel_components(self) -> np.ndarray:
        pixels = np.zeros((self.resolution.height, self.resolution.width, 4))
        pixels[:, :, 0] = self.pixels_red
        pixels[:, :, 1] = self.pixels_green
        pixels[:, :, 2] = self.pixels_blue
        pixels[:, :, 3] = self.pixels_alpha
        return pixels
    
    def __split_pixel_components(self, pixels: np.ndarray):
        self.pixels_red   = pixels[:, :, 0]
        self.pixels_green = pixels[:, :, 1]
        self.pixels_blue  = pixels[:, :, 2]
        self.pixels_alpha = pixels[:, :, 3]
    
    def __str__ (self):
        return str(self.resolution) + '\n' + \
            ' '.join(str(p) for p in self.pixels_red[:, :]) + \
            ' '.join(str(p) for p in self.pixels_green[:, :]) + \
            ' '.join(str(p) for p in self.pixels_blue[:, :]) + \
            ' '.join(str(p) for p in self.pixels_alpha[:, :])

    def __eq__(self, other):
        return self.resolution == other.resolution and \
            np.all(self.pixels_red == other.pixels_red) and \
            np.all(self.pixels_green == other.pixels_green) and \
            np.all(self.pixels_blue == other.pixels_blue) and \
            np.all(self.pixels_alpha == other.pixels_alpha)

def to_stride_image(image: PackedImage) -> StrideImage:
    return StrideImage(image.resolution, image.pixels)

def to_image(stride_image: StrideImage) -> PackedImage:
    return PackedImage(stride_image.resolution, stride_image.merge_pixel_components())