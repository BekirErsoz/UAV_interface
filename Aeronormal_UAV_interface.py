import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, Frame, Label, Button, Scale, HORIZONTAL
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import cv2
from PIL import Image, ImageTk
from tkinter import Tk, Frame
import tkintermapview

# Hız göstergesi fonksiyonu
def draw_speedometer(speed): #bekir
    ax.clear()
    num_segments = 6
    base_width = 0.6
    segment_increments = 0.05
    segment_widths = [base_width + i * segment_increments for i in range(num_segments)]
    segment_colors = ['#0E70A1' if i < int(speed / (100 / num_segments)) else '#2C2C34' for i in range(num_segments)]
    
    for i in range(num_segments):
        start_angle = np.pi - (i * (np.pi / num_segments))
        end_angle = start_angle - (np.pi / num_segments) + 0.05
        theta = np.linspace(end_angle, start_angle, 100)
        r_inner, r_outer = base_width, segment_widths[i]
        x_inner, y_inner = r_inner * np.cos(theta), r_inner * np.sin(theta)
        x_outer, y_outer = r_outer * np.cos(theta), r_outer * np.sin(theta)
        ax.fill(np.concatenate([x_outer, x_inner[::-1]]), np.concatenate([y_outer, y_inner[::-1]]), color=segment_colors[i])

    needle_angle = np.pi - (speed / 100) * np.pi
    needle_length = 0.85
    needle_tip_width = 0.01
    needle_x = [0, needle_length * np.cos(needle_angle) - needle_tip_width * np.sin(needle_angle), needle_length * np.cos(needle_angle) + needle_tip_width * np.sin(needle_angle)]
    needle_y = [0, needle_length * np.sin(needle_angle) + needle_tip_width * np.cos(needle_angle), needle_length * np.sin(needle_angle) - needle_tip_width * np.cos(needle_angle)]
    ax.fill(needle_x, needle_y, color="black")

    base_circle_radius = 0.15
    base_circle = plt.Circle((0, 0), base_circle_radius, color='black', zorder=5)
    ax.add_patch(base_circle)

    ax.text(0.8, -1.1, f"{speed} km/s", horizontalalignment='left', fontsize=15, color="white")
    ax.set_aspect('equal')
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_axis_off()
    canvas.draw()

# Altitude göstergesi fonksiyonu
def draw_altitude_indicator(altitude):
    ax2.clear()
    ax2.add_patch(Rectangle((0.3, 0), 0.4, 1, color='#FFFFFF', zorder=1))
    ax2.add_patch(Rectangle((0.3, 0), 0.4, altitude / 100, color='#3CA4DC', zorder=2))
    arrow_pos = altitude / 100
    ax2.arrow(0.05, arrow_pos, 0.15, 0, head_width=0.1, head_length=0.05, fc='#3CA4DC', ec='#3CA4DC', lw=2)
    ax2.text(1.0, 0.5, f"{altitude} m", va='center', ha='left', fontsize=15, color="white")
    ax2.set_xlim([0, 1.5])
    ax2.set_ylim([0, 1])
    ax2.set_axis_off()
    canvas2.draw()

# Battery göstergesi fonksiyonu
def draw_battery_indicator(battery_level):
    ax3.clear()
    ax3.add_patch(Rectangle((0.2, 0), 0.6, 1, edgecolor='white', fill=False, lw=2, zorder=3))
    ax3.add_patch(Rectangle((0.37, 1.03), 0.26, 0.05, color='white', zorder=4))
    num_segments = 5
    segment_height = 1 / num_segments
    segment_fill = battery_level / 100 * num_segments

    for i in range(num_segments):
        if segment_fill >= (i + 1):
            ax3.add_patch(Rectangle((0.2, i * segment_height), 0.6, segment_height - 0.02, color='#3CA4DC', zorder=2))
        elif segment_fill > i:
            partial_fill = segment_fill - i
            ax3.add_patch(Rectangle((0.2, i * segment_height), 0.6, (segment_height - 0.02) * partial_fill, color='#3CA4DC', zorder=2))

    ax3.text(1.0, 0.5, f"%{battery_level}", va='center', ha='left', fontsize=15, color="white")
    ax3.set_xlim([0, 1.5])
    ax3.set_ylim([0, 1.1])
    ax3.set_axis_off()
    canvas3.draw()

# Diğer göstergeler için kullanılan fonksiyon
def draw_indicator(ax, value, label_text, unit):
    ax.clear()
    ax.add_patch(Rectangle((0.3, 0), 0.4, 1, color='#FFFFFF', zorder=1))
    ax.add_patch(Rectangle((0.3, 0), 0.4, value / 100, color='#3CA4DC', zorder=2))
    arrow_pos = value / 100
    ax.arrow(0.05, arrow_pos, 0.15, 0, head_width=0.05, head_length=0.02, fc='#3CA4DC', ec='#3CA4DC', lw=1)
    ax.text(0.5, 1.1, label_text, va='center', ha='center', fontsize=8, color="white", transform=ax.transAxes)
    ax.text(0.5, -0.2, f"{value:.2f} {unit}", va='center', ha='center', fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8), transform=ax.transAxes)
    ax.set_xlim([0, 1.5])
    ax.set_ylim([-0.3, 1])
    ax.set_axis_off()

def update_indicators():
    # Her gösterge için 0 ile 100 arasında değerler oluşturuyoruz
    speed = random.randint(0, 100)       # Hız göstergesi
    altitude = random.randint(0, 100)    # İrtifa göstergesi
    battery_level = random.randint(0, 100)  # Batarya seviyesi göstergesi

    # frame1, frame2 ve frame3'teki göstergeleri güncelliyoruz
    draw_speedometer(speed)
    draw_altitude_indicator(altitude)
    draw_battery_indicator(battery_level)

    # Diğer göstergeleri 0 ile 100 arasında değerlerle güncelliyoruz
    for i, ax in enumerate(axes):
        values[i] = random.randint(0, 100)  # Her değeri 0-100 aralığında tutuyoruz
        draw_indicator(ax, values[i], labels[i], units[i])

    # Kanvası yenileyerek güncellenmiş değerleri gösteriyoruz
    canvas4.draw()
    root.after(1000, update_indicators)


def update_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    root.after(10, update_camera)

def update_data():
    global speed, altitude, battery_level, latitude, longitude
    speed = random.randint(0, 150)
    altitude = random.randint(0, 10000)
    battery_level = random.randint(0, 100)
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    root.after(1000, update_data)

def create_button(frame, text):
    return Button(frame, text=text, bg='#B0B0B0', fg='#2E2E2E', bd=2, relief='raised', font=('Arial', 10))

# Ana pencere
root = Tk()
root.title("Flight Indicators with Camera and Map")
root.geometry('1280x720')
root.configure(bg='#1E1F26')

# Kameradan görüntü alımı
cap = cv2.VideoCapture(0)

# Üst panel ve alt çerçeveler
blue_panel = Frame(root, bg='#15141A')
blue_panel.place(relx=0, rely=0, relwidth=1, relheight=0.1)


# frame1 hız göstergesi
frame1 = Frame(blue_panel, bg='#15141A')
frame1.place(relx=0, rely=0, relwidth=0.10, relheight=1)
fig, ax = plt.subplots(figsize=(3, 3), facecolor='#1E1F26')
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.get_tk_widget().pack()

# frame2 altitude göstergesi
frame2 = Frame(blue_panel, bg='#15141A')
frame2.place(relx=0.10, rely=0, relwidth=0.10, relheight=1)
fig2, ax2 = plt.subplots(figsize=(2, 5), facecolor='#1E1F26')
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas2.get_tk_widget().pack()

# frame3 battery göstergesi
frame3 = Frame(blue_panel, bg='#15141A')
frame3.place(relx=0.20, rely=0, relwidth=0.10, relheight=1)
fig3, ax3 = plt.subplots(figsize=(2, 5), facecolor='#1E1F26')
canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
canvas3.get_tk_widget().pack()

# frame4, "Mode: Guided" etiketini burada ekliyoruz
frame4 = Frame(blue_panel, bg='#1E1F26')
frame4.place(relx=0.30, rely=0, relwidth=0.10, relheight=1)
mode_label = Label(frame4, text="Mode: Guided", bg='#1E1F26', fg='white', font=('Arial', 16))
mode_label.pack(expand=True)  # "Mode: Guided" etiketini frame4'e ekleme


frame5 = Frame(blue_panel, bg='#1E1F26')
frame5.place(relx=0.40, rely=0, relwidth=0.15, relheight=1)
# Logo resmini yükleyin
logo_image = Image.open("gallery/logo.png")  # 'gallery' klasöründeki 'logo.png' dosyasını açar
logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)  # Boyutlandırma
logo_photo = ImageTk.PhotoImage(logo_image)

# Label widget ile logo resmini frame5 içine ekleyin
logo_label = Label(frame5, image=logo_photo, bg='#1E1F26')
logo_label.image = logo_photo  # Referansı saklayın
logo_label.pack(expand=True)


# frame6, "Mode: Guided" etiketini burada ekliyoruz
frame6 = Frame(blue_panel, bg='#1E1F26')
frame6.place(relx=0.55, rely=0, relwidth=0.25, relheight=1)
mode_label = Label(frame6, text="Enlem ve Boylam: 41.0054K, 28.972836D", bg='#1E1F26', fg='white', font=('Arial', 18))
mode_label.pack(expand=True)  

# frame7 içinde küçük bölümler oluşturma
frame7 = Frame(blue_panel, bg='#15141A')
frame7.place(relx=0.80, rely=0, relwidth=0.20, relheight=1)
left_frame = Frame(frame7, bg='#2C2C34', bd=1, relief='solid')
left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

right_frame = Frame(frame7, bg='#2C2C34', bd=1, relief='solid')
right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)


# frame_map tanımı
frame_map = Frame(root, bg='#2C2C34')  # Arka plan rengini isteğinize göre ayarlayın
frame_map.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)
# tkintermapview ile harita ekleme
map_widget = tkintermapview.TkinterMapView(frame_map, width=800, height=600)
map_widget.pack(fill="both", expand=True)

# Başlangıçta belirli bir konumu ayarlama (örneğin, İstanbul)
map_widget.set_position(41.015137, 28.979530)  # Enlem ve boylam değerleri
map_widget.set_zoom(10)  # Yakınlaştırma seviyesi


# Sol taraftaki RTL ve Acil Mod butonları için üst ve alt çerçeveler
rtl_button = Button(left_frame, text="RTL", bg='#2C2C34', fg='white', font=('Arial', 10), bd=1, relief='solid')
rtl_button.pack(fill='both', expand=True, padx=1, pady=1, side='top')

emergency_button = Button(left_frame, text="Acil Mod", bg='#2C2C34', fg='white', font=('Arial', 10), bd=1, relief='solid')
emergency_button.pack(fill='both', expand=True, padx=1, pady=1, side='bottom')

# Sağ tarafta Ayarlar butonu
settings_button = Button(right_frame, text="Ayarlar", bg='#2C2C34', fg='white', font=('Arial', 10), bd=1, relief='solid')
settings_button.pack(fill='both', expand=True, padx=1, pady=1)


camera_frame = Frame(root, bg='white', bd=0, relief='flat')
camera_frame.place(relx=0, rely=0.1, relwidth=0.3, relheight=0.5)
camera_label = Label(camera_frame)
camera_label.pack(fill='both', expand=True)

button_frame = Frame(root, bg='white', bd=0)
button_frame.place(relx=0, rely=0.6, relwidth=0.3, relheight=0.05)
button_labels = ["Kontrol", "Komut", "Mesaj", "Sayaç", "Durum", "Servo", "Veri K.", "Veri K. Hafızası"]
buttons = [create_button(button_frame, label) for label in button_labels]
for i, button in enumerate(buttons):
    button.pack(side='left', fill='both', expand=True)

indicator_frame = Frame(root, bg='white', bd=1, relief='flat')
indicator_frame.place(relx=0, rely=0.65, relwidth=0.3, relheight=0.35)
fig4, axes = plt.subplots(1, 8, figsize=(8, 4), facecolor='#1E1F26')
canvas4 = FigureCanvasTkAgg(fig4, master=indicator_frame)
canvas4.get_tk_widget().pack(side='top', fill='both', expand=True)

labels = ["Airspeed", "Vertical\nSpeed", "Heading", "Altitude", "Turn Rate", "Balance", "Roll", "Pitch"]
units = ["knots", "fpm", "deg", "m", "deg/s", "deg", "deg", "deg"]
values = [random.randint(0, 100) for _ in range(8)]

# Başlangıç güncellemeleri
update_camera()
update_data()
update_indicators()

# Tkinter ana döngüsü
root.mainloop()
cap.release()
