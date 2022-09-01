use crate::utils::{image::Image, function_tracer::FunctionTracer};

pub fn compute_solution(images: &mut Vec<Image>) {
    let ft = FunctionTracer::new("compute_solution", "seconds");

    images.iter_mut().for_each(|img| {
        if let Image::StrideImage(data) = img {
            data.pixels_red.iter_mut().for_each(|pix| {
                if *pix >= 200 {
                    *pix -= 150;
                }
            })
        }
    });

    drop(ft);
}