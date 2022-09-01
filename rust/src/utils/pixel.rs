#[derive(Debug, PartialEq)]
pub struct Pixel {
    pub red: u8,
    pub green: u8,
    pub blue: u8,
    pub alpha: u8
}



impl Pixel {
    pub fn new(red: u8, green: u8, blue: u8, alpha: u8) -> Self {
        Self { red, green, blue, alpha }
    }

    pub fn from_int(value: u32) -> Self {
        Self { red: (value >> 24) as u8, 
            green: ((value & 0x00FF0000) >> 16) as u8, 
            blue: ((value & 0x0000FF00) >> 8) as u8, 
            alpha: (value & 0x000000FF) as u8}
    }
}
