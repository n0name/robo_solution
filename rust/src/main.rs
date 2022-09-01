#![allow(unused)]
mod utils;
mod solution;

use std::env;

use utils::{file_parser::generate_io_data, image::ImageType};

use crate::solution::compute_solution;


fn main() -> std::io::Result<()> {
    let path = env::current_dir()?;
    println!("The current directory is {}", path.display());

    let input_file_name = "input.bin";
    let output_file_name = "output.bin";

    let (mut input_images, output_images) = generate_io_data(input_file_name, output_file_name, ImageType::StrideImage)?;

    compute_solution(&mut input_images);

    let success = input_images.iter().zip(output_images.iter()).all(|(i, o)| {
        i == o
    });

    if success {
        println!("Solution status - [SUCCESS]\n");
    } else {
        println!("Solution status - [FAIL]\n");
    }

    Ok(())
}
