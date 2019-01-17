import pynk
from pynk.nkpygame import NkPygame


class InputBox:
    def __init__(self, max_len):
        # self.max_len = pynk.ffi.new("int *", max_len)
        self.len = pynk.ffi.new("int *", 0)
        self.max_len = max_len
        # self.len = 0
        self.cur_text = pynk.ffi.new("char[{}]".format(max_len))

    def show(self, nkpy: NkPygame):
        pynk.lib.nk_edit_string(nkpy.ctx, pynk.lib.NK_EDIT_SIMPLE,
                                self.cur_text, self.len, self.max_len, pynk.ffi.addressof(
                                    pynk.lib, "nk_filter_default"))
