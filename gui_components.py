from gui_func import GUIFunc

import tkinter as tk


class Components(GUIFunc):
    def __init__(self, window):
        # Load preview into the buffer
        self.preview_img = super().get_default_preview()

        # BORDER settings
        self.border_label = tk.Label(window, text='BORDER')
        self.border_slider = tk.Scale(window, from_=0, to=100, orient='horizontal', command=lambda x: self.preprocess(self.preview_img))
        self.border_slider.set(20)

        # DIRECTORY settings
        self.dir_label = tk.Label(window, text='Select working directory:')
        self.dir_entry = tk.Entry(window)
        self.dir_button = tk.Button(window, text='select', command=lambda: [self.preprocess(self.preview_img), self.chose_dir()])

        # COLOR settings
        self.color_label = tk.Label(window, text='COLOR:')
        self.red_label = tk.Label(window, text='red:')
        self.green_label = tk.Label(window, text='green:')
        self.blue_label = tk.Label(window, text='blue:')
        self.rgb_entry_content = tk.StringVar()
        self.rgb_entry_content.trace("w", lambda name, index, mode, rgb_entry_content=self.rgb_entry_content: self.set_rgb_sliders(self.rgb_entry.get()))
        self.rgb_entry = tk.Entry(window, textvariable=self.rgb_entry_content)
        self.red_slider = tk.Scale(window, from_=0, to=255, orient='horizontal', command=lambda x: [self.set_rgb_entry(), self.preprocess(self.preview_img)])
        self.green_slider = tk.Scale(window, from_=0, to=255, orient='horizontal', command=lambda x: [self.set_rgb_entry(), self.preprocess(self.preview_img)])
        self.blue_slider = tk.Scale(window, from_=0, to=255, orient='horizontal', command=lambda x: [self.set_rgb_entry(), self.preprocess(self.preview_img)])
        self.rgb_label = tk.Label(window, text='RGB')
        self.hue_label = tk.Label(window, text='HUE')
        self.hue_entry = tk.Entry(window)

        # SPLIT settings
        self.split_lable = tk.Label(window, text='SPLIT')
        self.split_H_label = tk.Label(window, text='Horizontally:')
        self.split_V_label = tk.Label(window, text='Vertically:')
        self.split_H_slider = tk.Scale(window, from_=1, to=10, orient='horizontal', command=lambda x: self.preprocess(self.preview_img))
        self.split_V_slider = tk.Scale(window, from_=1, to=10, orient='horizontal', command=lambda x: self.preprocess(self.preview_img))

        # OTHER
        self.preview = tk.Label(window)
        self.text_field = tk.Text(window, height=10, width=45)
        self.confirm_button = tk.Button(window, text='Process', width=25, command=lambda:self.process(self.border_slider.get(), self.get_RGB(), self.get_split() ))

    def get_RGB(self):
        return [self.blue_slider.get(), self.green_slider.get(), self.red_slider.get()]

    def get_split(self):
        return [self.split_H_slider.get(), self.split_V_slider.get()]