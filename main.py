import tkinter as tk
import tkinter.messagebox
from yeelight import Bulb, BulbException

global bulb


def activate_controls():
    bulb_bright_lbl.config(fg='black')
    bulb_temp_lbl.config(fg='black')
    bulb_bright_sld.config(state='normal', troughcolor='white', fg='black')
    bulb_temp_sld.config(state='normal', troughcolor='white', fg='black')


def deactivate_controls():
    bulb_bright_lbl.config(fg='gray')
    bulb_temp_lbl.config(fg='gray')
    bulb_bright_sld.config(state='disabled', troughcolor='lightgray', fg='gray')
    bulb_temp_sld.config(state='disabled', troughcolor='lightgray', fg='gray')


def bulb_is_on():
    bulb_state = bulb.get_properties()['power']
    if bulb_state == 'on':
        return True
    elif bulb_state == 'off':
        return False


def connect_to_bulb():
    global bulb
    bulb_ip = ip_entry.get()
    bulb = Bulb(bulb_ip)

    try:
        bulb.turn_on()
        bulb.get_capabilities()
        bulb.start_music()
        tk.messagebox.showinfo('Connected', f'Successfully connected to model: {bulb.model} on {bulb_ip}')
        connect_status_lbl.config(text=f'Currently connected to: {bulb_ip}')
        bulb_toggle_btn.config(state='normal', image=button_on_image)
        activate_controls()

    except BulbException as ex:
        error_msg = str(ex) + '\n-Make sure the bulb is on.\n-Check if you are using the correct bulb ip address.'
        tk.messagebox.showerror('error', error_msg)
        connect_status_lbl.config(text='Not connected to a bulb')
        bulb_toggle_btn.config(state='disabled')
        deactivate_controls()


def bulb_toggle():
    try:
        if bulb_is_on():
            bulb.turn_off()
            bulb_toggle_btn.config(image=button_off_image)
            deactivate_controls()
        else:
            bulb.turn_on()
            bulb_toggle_btn.config(image=button_on_image)
            activate_controls()
    except BulbException as ex:
        tk.messagebox.showerror('error', str(ex))


def bright_slider_changed(event):
    brightness = bulb_bright_sld.get()
    try:
        bulb.set_brightness(brightness)
    except BulbException as ex:
        tk.messagebox.showerror('error', str(ex))


def temp_slider_changed(event):
    temperature = bulb_temp_sld.get()
    try:
        bulb.set_color_temp(temperature)
    except BulbException as ex:
        tk.messagebox.showerror('error', str(ex))


def on_closing():
    if tk.messagebox.askokcancel('Quit', 'Do you want to quit ?'):
        root.destroy()


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.title('Yeelight bulb control')
root.geometry('600x500')

# TODO: make background
# BG IMAGE
# background_image = tk.PhotoImage(file='yl_bg.png')
# label = tk.Label(root, image=background_image).place(x=0, y=0)


ip_lbl = tk.Label(root, text="Bulb ip address ->", relief="groove")
ip_lbl.grid(column=1, row=2, padx=10, pady=20)

ip_entry = tk.Entry(root, width=16, justify='center')
ip_entry.grid(column=2, row=2, padx=10)

connect_btn = tk.Button(root, text='Connect', command=connect_to_bulb)
connect_btn.grid(column=3, row=2, padx=10)

connect_status_lbl = tk.Label(root, text="Not connected to a bulb")
connect_status_lbl.grid(column=4, row=2, padx=10)

button_on_image = tk.PhotoImage(file=r'pictures\on.png')
button_off_image = tk.PhotoImage(file=r'pictures\off.png')

bulb_toggle_btn = tk.Button(root, image=button_on_image, width='35', height='48', state='disabled', command=bulb_toggle)
bulb_toggle_btn.grid(column=1, row=4, rowspan=2, pady=(30, 0))

bulb_bright_lbl = tk.Label(root, text="Brightness", fg='gray')
bulb_bright_lbl.grid(column=2, row=4, pady=(30, 0))

bulb_bright_sld = tk.Scale(root, from_=0, to=100, state='disabled', fg='gray', orient='horizontal', command=bright_slider_changed)
bulb_bright_sld.grid(column=2, row=5)

bulb_temp_lbl = tk.Label(root, text="Color temperature", fg='gray')
bulb_temp_lbl.grid(column=3, row=4, pady=(30, 0))

bulb_temp_sld = tk.Scale(root, from_=1700, to=6500, state='disabled', fg='gray', orient='horizontal', command=temp_slider_changed)
bulb_temp_sld.grid(column=3, row=5)


root.mainloop()

# TODO: check for model and give appropriate functions
