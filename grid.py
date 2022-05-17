

def construct_grid(gui):
    # BORDER
    gui.border_label.grid(column=1, row=0)
    gui.border_slider.grid(column=0, row=1)

    gui.dir_label.grid(column=0, row=2)
    gui.dir_button.grid(column=1, row=2)
    gui.dir_entry.grid(column=2, row=2)

    gui.color_label.grid(column=0, row=3)
    gui.red_label.grid(column=0, row=4)
    gui.green_label.grid(column=0, row=5)
    gui.blue_label.grid(column=0, row=6)
    gui.red_slider.grid(column=1, row=4)
    gui.green_slider.grid(column=1, row=5)
    gui.blue_slider.grid(column=1, row=6)
    gui.rgb_label.grid(column=0, row=7)
    gui.hue_label.grid(column=0, row=8)
    gui.rgb_entry.grid(column=1, row=7)
    gui.hue_entry.grid(column=1, row=8)

    # SPLIT
    gui.split_lable.grid(column=1, row=9)
    gui.split_H_label.grid(column=0, row=10)
    gui.split_V_label.grid(column=0, row=11)
    gui.split_H_slider.grid(column=1, row=10)
    gui.split_V_slider.grid(column=1, row=11)

    # PREVIEW
    gui.preview.grid(column=3, row=0)

    # PROCESSING
    gui.text_field.grid(column=3, row=8)
    gui.confirm_button.grid(column=3, row=11)
