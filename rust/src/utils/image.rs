use std::fmt::Display;

use crate::utils::resolution::Resolution;

use super::pixel::Pixel;

#[derive(Debug, Clone, Copy)]
pub enum ImageType {
    PackedImage,
    StrideImage
}

#[derive(Debug, PartialEq)]
pub enum Image {
    PackedImage(PackedImage),
    StrideImage(StrideImage)
}

#[derive(Debug, PartialEq)]
pub struct PackedImage {
    resolution: Resolution,
    pixels: Vec<Pixel>
}

impl PackedImage {
    pub fn new(resolution: Resolution, pixels: Vec<Pixel>) -> Self { 
        Self { resolution, pixels } 
    }
}

impl Display for PackedImage {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}\n{:?}", self.resolution, self.pixels)
    }
}

#[derive(Debug, PartialEq)]
pub struct StrideImage {
    pub resolution: Resolution,
    pub pixels_red: Vec<u8>,
    pub pixels_green: Vec<u8>,
    pub pixels_blue: Vec<u8>,
    pub pixels_alpha: Vec<u8>,
}

impl StrideImage {
    pub fn new(resolution: Resolution, pixels: Vec<Pixel>) -> Self {
        let mut res = Self {
            resolution,
            pixels_red: Vec::new(),
            pixels_green: Vec::new(),
            pixels_blue: Vec::new(),
            pixels_alpha: Vec::new(),
        };
        res.split_pixel_components(pixels);
        res
    }

    fn split_pixel_components(&mut self, pixels: Vec<Pixel>) {
        pixels.into_iter().for_each(|p| {
            self.pixels_red.push(p.red);
            self.pixels_green.push(p.green);
            self.pixels_blue.push(p.blue);
            self.pixels_alpha.push(p.alpha);
        })
    }

    pub fn merge_pixel_components(&self) -> Vec<Pixel> {
        self.pixels_red.iter()
            .zip(self.pixels_green.iter())
            .zip(self.pixels_blue.iter())
            .zip(self.pixels_alpha.iter())
            .map(|(((&r, &g), &b), &a)| {
                Pixel::new(r, g, b, a)
            }).collect()
    }
}


impl Into<StrideImage> for PackedImage {
    fn into(self) -> StrideImage {
        StrideImage::new(self.resolution, self.pixels)
    }
}

impl Into<PackedImage> for StrideImage {
    fn into(self) -> PackedImage {
        PackedImage::new(self.resolution, self.merge_pixel_components())
    }
}