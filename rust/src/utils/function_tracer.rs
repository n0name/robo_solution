use std::time::Instant;
pub struct FunctionTracer {
    start: Instant,
    func_name: &'static str,
    message_postfix: &'static str
}

impl FunctionTracer {
    pub fn new(func_name: &'static str, message_postfix: &'static str) -> Self {
        Self { 
            start: Instant::now(), 
            func_name, message_postfix
        }
    }
}

impl Drop for FunctionTracer {
    fn drop(&mut self) {
        let end = Instant::now();
        let dur = end - self.start;
        println!("{} took {:.3} {}", self.func_name, dur.as_secs_f32(), self.message_postfix);
    }
}

