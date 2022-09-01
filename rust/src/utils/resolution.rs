use std::fmt::Display;

#[derive(Debug, PartialEq, Clone, Copy)]
pub struct Resolution {
    width: usize,
    height: usize
}

impl Resolution {
    pub fn new(width: usize, height: usize) -> Self { 
        Self { width, height } 
    }
}

impl Display for Resolution {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.width, self.height)
    }
}
