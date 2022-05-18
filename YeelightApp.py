import tkinter as tk
import tkinter.messagebox
from yeelight import Bulb, BulbException, flows

global bulb


def activate_controls():
    bulb_bright_lbl.config(fg='black')
    bulb_temp_lbl.config(fg='black')
    bulb_saturation_lbl.config(fg='black')
    bulb_hue_lbl.config(fg='black')
    bulb_bright_sld.config(state='normal', troughcolor='gray', fg='black')
    bulb_temp_sld.config(state='normal', troughcolor='gray', fg='black')
    bulb_saturation_sld.config(state='normal', troughcolor='gray', fg='black')
    bulb_hue_sld.config(state='normal', troughcolor='gray', fg='black')
    bulb_color_image.config(state='normal')
    scene_lbl.config(fg='black')
    scene_home_btn.config(state='normal')
    scene_movie_btn.config(state='normal')
    scene_romance_btn.config(state='normal')
    scene_candle_btn.config(state='normal')
    scene_sunrise_btn.config(state='normal')
    scene_sunset_btn.config(state='normal')
    scene_rgb_btn.config(state='normal')
    scene_police_btn.config(state='normal')


def deactivate_controls():
    bulb_bright_lbl.config(fg='gray')
    bulb_temp_lbl.config(fg='gray')
    bulb_saturation_lbl.config(fg='gray')
    bulb_hue_lbl.config(fg='gray')
    bulb_bright_sld.config(state='disabled', troughcolor='lightgray', fg='gray')
    bulb_temp_sld.config(state='disabled', troughcolor='lightgray', fg='gray')
    bulb_saturation_sld.config(state='disabled', troughcolor='lightgray', fg='gray')
    bulb_hue_sld.config(state='disabled', troughcolor='lightgray', fg='gray')
    bulb_color_image.config(state='disabled')
    scene_lbl.config(fg='gray')
    scene_home_btn.config(state='disabled')
    scene_movie_btn.config(state='disabled')
    scene_romance_btn.config(state='disabled')
    scene_candle_btn.config(state='disabled')
    scene_sunrise_btn.config(state='disabled')
    scene_sunset_btn.config(state='disabled')
    scene_rgb_btn.config(state='disabled')
    scene_police_btn.config(state='disabled')


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
        connect_status_lbl.config(text=f'Connected to: {bulb_ip}')
        bulb_toggle_btn.config(state='normal', image=button_on_image)
        activate_controls()

    except BulbException as ex:
        error_msg = str(ex) + '\n-Make sure the bulb is on and has enabled Lan Control.\n-Check if you are using the ' \
                              'correct bulb ip address.\n-Ensure that the program is in the firewall exceptions list.'
        tk.messagebox.showerror('Error', error_msg)
        connect_status_lbl.config(text='Not connected to a bulb')
        bulb_toggle_btn.config(state='disabled')
        deactivate_controls()

    finally:
        ip_entry.delete(0, tk.END)


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


def hue_saturation_slider_changed(event):
    saturation = bulb_saturation_sld.get()
    hue = bulb_hue_sld.get()
    try:
        bulb.set_hsv(hue, saturation)
    except BulbException as ex:
        tk.messagebox.showerror('error', str(ex))


def get_scene(scene_type):
    match scene_type:
        case 'home':
            return flows.home()
        case 'movie':
            return flows.movie(500, 50)
        case 'romance':
            return flows.romance()
        case 'candle':
            return flows.candle_flicker()
        case 'sunrise':
            return flows.sunrise()
        case 'sunset':
            return flows.sunset()
        case 'rgb':
            return flows.random_loop(750, 100, 9)
        case 'police':
            return flows.police2(250, 100)


def set_scene(scene_name):
    scene = get_scene(scene_name)
    try:
        bulb.start_flow(scene)
    except BulbException as ex:
        tk.messagebox.showerror('error', str(ex))


def on_closing():
    if tk.messagebox.askokcancel('Quit', 'Do you want to quit ?'):
        root.destroy()


root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', on_closing)

root.title('Yeelight bulb control')
root.geometry('600x680')

background_image = tk.PhotoImage(file=r'pictures\background.png')
tk.Label(root, image=background_image).place(x=0, y=0)


ip_lbl = tk.Label(root, width=15, text='Bulb ip address ->', relief='groove')
ip_lbl.grid(column=1, row=2, padx=(25, 10), pady=20)

ip_entry = tk.Entry(root, width=20, justify='center', bg='gray95')
ip_entry.grid(column=2, row=2, padx=10)

connect_btn = tk.Button(root, width=15, text='Connect', command=connect_to_bulb)
connect_btn.grid(column=3, row=2, padx=10)

connect_status_lbl = tk.Label(root, text='Not connected to a bulb', width='20')
connect_status_lbl.grid(column=4, row=2, padx=10)

button_on_image = tk.PhotoImage(file=r'pictures\on.png')
button_off_image = tk.PhotoImage(file=r'pictures\off.png')

bulb_toggle_btn = tk.Button(root, image=button_on_image, width='35', height='48', state='disabled', command=bulb_toggle)
bulb_toggle_btn.grid(column=1, row=4, rowspan=2, pady=(30, 0))

bulb_bright_lbl = tk.Label(root, text='Brightness', fg='gray', bg='white')
bulb_bright_lbl.grid(column=2, row=4, pady=(30, 0))

bulb_bright_sld = tk.Scale(root, length=111, from_=0, to=100, state='disabled', fg='gray', bg='white', orient='horizontal', command=bright_slider_changed)
bulb_bright_sld.grid(column=2, row=5)

bulb_temp_lbl = tk.Label(root, text='Color temperature', fg='gray', bg='white')
bulb_temp_lbl.grid(column=3, row=4, pady=(30, 0))

bulb_temp_sld = tk.Scale(root, length=111, from_=1700, to=6500, state='disabled', fg='gray', bg='white', orient='horizontal', command=temp_slider_changed)
bulb_temp_sld.grid(column=3, row=5)


color_img = tk.PhotoImage(file=r'pictures\color.png')

bulb_color_image = tk.Label(root, state='disabled', image=color_img)
bulb_color_image.grid(column=2, row=7, columnspan=2, pady=(25, 2), padx=(3, 0))

bulb_saturation_lbl = tk.Label(root, text='Saturation', wraplength=1, fg='gray', bg='white')
bulb_saturation_lbl.grid(column=1, row=7, padx=(50, 0), pady=(25, 2))

bulb_saturation_sld = tk.Scale(root, length=160, from_=100, to=0, state='disabled', fg='gray', bg='white', command=hue_saturation_slider_changed)
bulb_saturation_sld.grid(column=1, row=7, pady=(25, 2), sticky='E')

bulb_hue_lbl = tk.Label(root, text='Hue', fg='gray', bg='white')
bulb_hue_lbl.grid(column=2, row=9, columnspan=2, padx=(15, 0))

bulb_hue_sld = tk.Scale(root, length=250, from_=0, to=359, state='disabled', fg='gray', bg='white', orient='horizontal', command=hue_saturation_slider_changed)
bulb_hue_sld.grid(column=2, row=8, columnspan=2, padx=(3, 0))


scene_lbl = tk.Label(root, text='Scenes', width='8', justify='center', relief='groove', fg='gray')
scene_lbl.grid(column=1, row=10, pady=(15, 0), columnspan=4)

scene_home_img = tk.PhotoImage(file=r'pictures\scene_home.png')
scene_home_btn = tk.Button(root, state='disabled', image=scene_home_img, command=lambda: set_scene('home'))
scene_home_btn.grid(column=1, row=11, pady=15)

scene_movie_img = tk.PhotoImage(file=r'pictures\scene_movie.png')
scene_movie_btn = tk.Button(root, state='disabled', image=scene_movie_img, command=lambda: set_scene('movie'))
scene_movie_btn.grid(column=2, row=11)

scene_romance_img = tk.PhotoImage(file=r'pictures\scene_romance.png')
scene_romance_btn = tk.Button(root, state='disabled', image=scene_romance_img, command=lambda: set_scene('romance'))
scene_romance_btn.grid(column=3, row=11, padx=(10, 0))

scene_candle_img = tk.PhotoImage(file=r'pictures\scene_candle.png')
scene_candle_btn = tk.Button(root, state='disabled', image=scene_candle_img, command=lambda: set_scene('candle'))
scene_candle_btn.grid(column=4, row=11)

scene_sunrise_img = tk.PhotoImage(file=r'pictures\scene_sunrise.png')
scene_sunrise_btn = tk.Button(root, state='disabled', image=scene_sunrise_img, command=lambda: set_scene('sunrise'))
scene_sunrise_btn.grid(column=1, row=12, pady=20)

scene_sunset_img = tk.PhotoImage(file=r'pictures\scene_sunset.png')
scene_sunset_btn = tk.Button(root, state='disabled', image=scene_sunset_img, command=lambda: set_scene('sunset'))
scene_sunset_btn.grid(column=2, row=12)

scene_rgb_img = tk.PhotoImage(file=r'pictures\scene_rgb.png')
scene_rgb_btn = tk.Button(root, state='disabled', image=scene_rgb_img, command=lambda: set_scene('rgb'))
scene_rgb_btn.grid(column=3, row=12, padx=(10, 0))

scene_police_img = tk.PhotoImage(file=r'pictures\scene_police.png')
scene_police_btn = tk.Button(root, state='disabled', image=scene_police_img, command=lambda: set_scene('police'))
scene_police_btn.grid(column=4, row=12)


root.mainloop()

# TODO: check for model and give appropriate functions