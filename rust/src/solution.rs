use crate::utils::{
    image::{Image, StrideImage}, 
    function_tracer::FunctionTracer
};

use rayon::prelude::*;

fn compute_image(image: &mut StrideImage) {
    // let res = image.resolution;
    // let pixels = &mut image.pixels_red;
    // for y in 0..res.height {
    //     for x in 0..res.width {
    //         let cur_idx = y * res.width + x;
    //         if pixels[cur_idx] >= 200 {
    //             for pat_y in y..y+5 {
    //                 for pat_x in x..x+5 {
    //                     let pat_idx = pat_y * res.width + pat_x;
    //                     if pixels[pat_idx] >= 200 {
    //                         pixels[pat_idx] -= 150;
    //                     }
    //                 }
    //             }
    //         }
    //     }
    // }

    image.pixels_red.iter_mut().for_each(|pix| {
        if *pix >= 200 {
            *pix -=150;
        }
    })
}

pub fn compute_solution(images: &mut Vec<Image>) {
    let ft = FunctionTracer::new("compute_solution", "seconds");

    images.par_iter_mut().for_each(|img| {
        if let Image::StrideImage(data) = img {
            compute_image(data);
        }
    });

    drop(ft);
}