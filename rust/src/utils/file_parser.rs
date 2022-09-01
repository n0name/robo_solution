use std::{path::Path, io::BufRead};
use std::fs::File;
use std::io::BufReader;

use crate::utils::image::{ImageType, Image, PackedImage, StrideImage};
use crate::utils::pixel::Pixel;
use crate::utils::resolution::Resolution;

use super::function_tracer::FunctionTracer;


pub fn generate_data<S: AsRef<Path>>(file_name: S, image_type: ImageType) -> std::io::Result<Vec<Image>> {
    let mut reader = BufReader::new(File::open(file_name)?);
    let mut buf = String::new();

    reader.read_line(&mut buf);
    let images_num = buf.replace("\n", "").parse::<usize>().unwrap();

    let mut res = Vec::new();
    for _ in 0..images_num {
        buf.clear();
        reader.read_line(&mut buf);
        let tokens: Vec<usize> = buf.replace("\n", "").split(" ").map(|t| t.parse::<usize>().unwrap()).collect();
        assert_eq!(tokens.len(), 2);
        let width = tokens[0];
        let height = tokens[1];
        let resolution = Resolution::new(width, height);

        buf.clear();
        reader.read_line(&mut buf);
        let pixels: Vec<Pixel> = buf.replace("\n", "").split(" ")
            .filter_map(|t| {
                t.parse::<u32>().ok()
            }).map(|val| {
                Pixel::from_int(val)
            }).collect();
        match image_type {
            ImageType::PackedImage => {
                res.push(Image::PackedImage(PackedImage::new(resolution, pixels)))
            },
            ImageType::StrideImage => {
                res.push(Image::StrideImage(StrideImage::new(resolution, pixels)))
            },
        }
    }

    Ok(res)
}

pub fn generate_io_data<S: AsRef<Path>>(input_file_name: S, output_file_name: S, image_type: ImageType) -> std::io::Result<(Vec<Image>, Vec<Image>)> {
    let ft = FunctionTracer::new("generate_io_data", "seconds //not included into solution timings");
    
    let input_data = generate_data(input_file_name, image_type)?;
    let output_data = generate_data(output_file_name, image_type)?;

    drop(ft);
    Ok((input_data, output_data))
}