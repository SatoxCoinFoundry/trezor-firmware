use super::ffi;

#[cfg(feature = "button")]
pub use super::ffi::{BTN_EVT_DOWN, BTN_EVT_UP, BTN_LEFT, BTN_RIGHT};

#[cfg(feature = "touch")]
pub fn io_touch_read() -> u32 {
    unsafe { ffi::touch_read() }
}

#[cfg(feature = "button")]
pub fn io_button_read() -> u32 {
    unsafe { ffi::button_read() }
}