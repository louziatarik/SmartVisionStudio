import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import time
from datetime import datetime
import os
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# SMART VISION STUDIO
# Step 4.6C - Premium Product Polish
# ============================================================


# ============================================================
# SETTINGS
# ============================================================

CAPTURE_FOLDER = "captures"
EVENTS_FILE = "vision_events.csv"
SESSION_FILE = "session_history.csv"

os.makedirs(CAPTURE_FOLDER, exist_ok=True)


# ============================================================
# PROFESSIONAL COLOR SYSTEM
# ============================================================

BG_MAIN = "#0B1120"
BG_PANEL = "#111827"
BG_CARD = "#172033"
BG_CARD_LIGHT = "#1D293B"
BG_CAMERA = "#050B14"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#64748B"

ACCENT_BLUE = "#3B82F6"
ACCENT_BLUE_LIGHT = "#60A5FA"

SUCCESS = "#22C55E"
SUCCESS_LIGHT = "#86EFAC"

WARNING = "#F59E0B"
WARNING_LIGHT = "#FCD34D"

DANGER = "#EF4444"

BORDER = "#263449"


# ============================================================
# AI FACE DETECTION
# ============================================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    messagebox.showerror(
        "Camera Error",
        "Could not open the webcam."
    )

    raise SystemExit


# ============================================================
# VARIABLES
# ============================================================

start_time = time.time()

previous_face_count = 0
previous_occupancy = False

detection_events = 0
screenshots_taken = 0
capture_number = 1

peak_occupancy = 0
total_face_samples = 0
face_sample_count = 0
occupied_samples = 0

last_time = time.time()
fps = 0

current_frame = None

chart_times = []
chart_faces = []

temperature = 24.0
humidity = 48


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Smart Vision Studio")
root.geometry("1200x750")

root.configure(
    bg=BG_MAIN
)

root.resizable(
    False,
    False
)


# ============================================================
# HELPER
# ============================================================

def make_label(
    parent,
    text,
    size=10,
    weight="normal",
    color=TEXT_PRIMARY,
    bg=BG_MAIN
):

    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", size, weight),
        fg=color,
        bg=bg
    )


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=BG_MAIN
)

header.pack(
    fill="x",
    padx=28,
    pady=(20, 12)
)


# ------------------------------------------------------------
# HEADER LEFT
# ------------------------------------------------------------

header_left = tk.Frame(
    header,
    bg=BG_MAIN
)

header_left.pack(
    side="left"
)


title = make_label(
    header_left,
    "SMART VISION STUDIO",
    23,
    "bold",
    TEXT_PRIMARY,
    BG_MAIN
)

title.pack(
    anchor="w"
)


subtitle = make_label(
    header_left,
    "AI Visual Perception Platform",
    10,
    "normal",
    TEXT_SECONDARY,
    BG_MAIN
)

subtitle.pack(
    anchor="w",
    pady=(2, 0)
)


# ------------------------------------------------------------
# HEADER RIGHT
# ------------------------------------------------------------

header_status = tk.Frame(
    header,
    bg=BG_CARD,
    padx=13,
    pady=7
)

header_status.pack(
    side="right",
    pady=4
)


status_dot = tk.Label(
    header_status,
    text="●",
    font=("Segoe UI", 10),
    fg=SUCCESS,
    bg=BG_CARD
)

status_dot.pack(
    side="left"
)


status_text = tk.Label(
    header_status,
    text=" SYSTEM ONLINE",
    font=("Segoe UI", 8, "bold"),
    fg=TEXT_PRIMARY,
    bg=BG_CARD
)

status_text.pack(
    side="left"
)


# ============================================================
# MAIN CONTENT
# ============================================================

main = tk.Frame(
    root,
    bg=BG_MAIN
)

main.pack(
    fill="both",
    expand=True,
    padx=28,
    pady=(0, 18)
)


# ============================================================
# LEFT COLUMN
# ============================================================

left_panel = tk.Frame(
    main,
    bg=BG_MAIN,
    width=720
)

left_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 14)
)


# ============================================================
# CAMERA PANEL
# ============================================================

camera_panel = tk.Frame(
    left_panel,
    bg=BG_PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

camera_panel.pack(
    fill="x"
)

camera_panel.pack_propagate(False)

camera_panel.configure(
    height=365
)


# ============================================================
# CAMERA HEADER
# ============================================================

camera_header = tk.Frame(
    camera_panel,
    bg=BG_PANEL
)

camera_header.pack(
    fill="x",
    padx=16,
    pady=(10, 7)
)


camera_header_left = tk.Frame(
    camera_header,
    bg=BG_PANEL
)

camera_header_left.pack(
    side="left"
)


camera_title = make_label(
    camera_header_left,
    "LIVE CAMERA",
    11,
    "bold",
    TEXT_PRIMARY,
    BG_PANEL
)

camera_title.pack(
    side="left"
)


# AI badge

ai_badge = tk.Label(
    camera_header_left,
    text=" AI VISION ACTIVE ",
    font=("Segoe UI", 7, "bold"),
    fg=ACCENT_BLUE_LIGHT,
    bg="#132B4F",
    padx=5,
    pady=3
)

ai_badge.pack(
    side="left",
    padx=(10, 0)
)


# Camera live indicator

live_container = tk.Frame(
    camera_header,
    bg=BG_PANEL
)

live_container.pack(
    side="right"
)


live_dot = tk.Label(
    live_container,
    text="●",
    font=("Segoe UI", 9),
    fg=SUCCESS,
    bg=BG_PANEL
)

live_dot.pack(
    side="left"
)


live_text = tk.Label(
    live_container,
    text=" LIVE",
    font=("Segoe UI", 8, "bold"),
    fg=SUCCESS_LIGHT,
    bg=BG_PANEL
)

live_text.pack(
    side="left"
)


# ============================================================
# VIDEO CONTAINER
# ============================================================

video_outer = tk.Frame(
    camera_panel,
    bg=BORDER
)

video_outer.pack(
    fill="both",
    expand=True,
    padx=16,
    pady=(0, 15)
)


video_container = tk.Frame(
    video_outer,
    bg=BG_CAMERA
)

video_container.pack(
    fill="both",
    expand=True,
    padx=1,
    pady=1
)


video_label = tk.Label(
    video_container,
    bg=BG_CAMERA
)

video_label.pack(
    fill="both",
    expand=True
)


# ============================================================
# FACE ACTIVITY PANEL
# ============================================================

chart_panel = tk.Frame(
    left_panel,
    bg=BG_PANEL,
    highlightbackground=BORDER,
    highlightthickness=1,
    height=125
)

chart_panel.pack(
    fill="x",
    pady=(10, 0)
)

chart_panel.pack_propagate(False)


# ============================================================
# CHART HEADER
# ============================================================

chart_header = tk.Frame(
    chart_panel,
    bg=BG_PANEL
)

chart_header.pack(
    fill="x",
    padx=15,
    pady=(7, 0)
)


chart_header_left = tk.Frame(
    chart_header,
    bg=BG_PANEL
)

chart_header_left.pack(
    side="left"
)


chart_title = make_label(
    chart_header_left,
    "FACE ACTIVITY",
    9,
    "bold",
    TEXT_PRIMARY,
    BG_PANEL
)

chart_title.pack(
    side="left"
)


chart_indicator = tk.Label(
    chart_header_left,
    text="  LIVE  ",
    font=("Segoe UI", 6, "bold"),
    fg=SUCCESS_LIGHT,
    bg="#12301F",
    padx=3,
    pady=2
)

chart_indicator.pack(
    side="left",
    padx=(7, 0)
)


chart_live = make_label(
    chart_header,
    "LAST 30 SEC",
    7,
    "normal",
    TEXT_MUTED,
    BG_PANEL
)

chart_live.pack(
    side="right"
)


# ============================================================
# CHART
# ============================================================

figure = Figure(
    figsize=(6.5, 1.05),
    dpi=90,
    facecolor=BG_PANEL
)

ax = figure.add_subplot(111)

ax.set_facecolor(
    BG_PANEL
)


# Remove borders

for spine in ax.spines.values():

    spine.set_visible(False)


ax.tick_params(
    colors=TEXT_MUTED,
    labelsize=7,
    length=0
)


ax.grid(
    True,
    axis="y",
    alpha=0.15,
    linewidth=0.6
)


ax.set_ylim(
    0,
    3
)


ax.set_xlim(
    0,
    30
)


ax.set_ylabel(
    "Faces",
    color=TEXT_MUTED,
    fontsize=7
)


ax.set_xlabel(
    "Seconds",
    color=TEXT_MUTED,
    fontsize=7
)


line, = ax.plot(
    [],
    [],
    marker="o",
    markersize=3,
    linewidth=2,
    color=ACCENT_BLUE
)


figure.tight_layout(
    pad=1
)


chart_canvas = FigureCanvasTkAgg(
    figure,
    master=chart_panel
)

chart_canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=10,
    pady=0
)


# ============================================================
# SMART ENVIRONMENT
# ============================================================

environment_panel = tk.Frame(
    left_panel,
    bg=BG_PANEL,
    highlightbackground=BORDER,
    highlightthickness=1,
    height=105
)

environment_panel.pack(
    fill="x",
    pady=(10, 0)
)

environment_panel.pack_propagate(False)


environment_header = tk.Frame(
    environment_panel,
    bg=BG_PANEL
)

environment_header.pack(
    fill="x",
    padx=15,
    pady=(6, 2)
)


environment_title = make_label(
    environment_header,
    "SMART ENVIRONMENT",
    9,
    "bold",
    TEXT_PRIMARY,
    BG_PANEL
)

environment_title.pack(
    side="left"
)


environment_subtitle = make_label(
    environment_header,
    "IoT MONITORING",
    7,
    "normal",
    TEXT_MUTED,
    BG_PANEL
)

environment_subtitle.pack(
    side="right"
)


environment_content = tk.Frame(
    environment_panel,
    bg=BG_PANEL
)

environment_content.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(2, 8)
)


# ============================================================
# ENVIRONMENT CARD
# ============================================================

def create_environment_card(
    parent,
    label_text,
    value_text
):

    card = tk.Frame(
        parent,
        bg=BG_CARD_LIGHT,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3
    )


    label = tk.Label(
        card,
        text=label_text,
        font=("Segoe UI", 7, "bold"),
        fg=TEXT_MUTED,
        bg=BG_CARD_LIGHT
    )

    label.pack(
        anchor="w",
        padx=10,
        pady=(5, 0)
    )


    value = tk.Label(
        card,
        text=value_text,
        font=("Segoe UI", 11, "bold"),
        fg=TEXT_PRIMARY,
        bg=BG_CARD_LIGHT
    )

    value.pack(
        anchor="w",
        padx=10,
        pady=(1, 0)
    )


    return value


occupancy_value = create_environment_card(
    environment_content,
    "OCCUPANCY",
    "IDLE"
)


temperature_value = create_environment_card(
    environment_content,
    "TEMPERATURE",
    "24.0 °C"
)


humidity_value = create_environment_card(
    environment_content,
    "HUMIDITY",
    "48 %"
)


response_value = create_environment_card(
    environment_content,
    "SMART RESPONSE",
    "STANDBY"
)


# ============================================================
# RIGHT COLUMN
# ============================================================

right_panel = tk.Frame(
    main,
    bg=BG_MAIN,
    width=390
)

right_panel.pack(
    side="right",
    fill="y"
)

right_panel.pack_propagate(False)


# ============================================================
# ANALYTICS HEADER
# ============================================================

analytics_header = tk.Frame(
    right_panel,
    bg=BG_MAIN
)

analytics_header.pack(
    fill="x",
    pady=(0, 8)
)


analytics_title = make_label(
    analytics_header,
    "LIVE ANALYTICS",
    12,
    "bold",
    TEXT_PRIMARY,
    BG_MAIN
)

analytics_title.pack(
    side="left"
)


analytics_status = tk.Label(
    analytics_header,
    text="REAL-TIME",
    font=("Segoe UI", 7, "bold"),
    fg=ACCENT_BLUE_LIGHT,
    bg=BG_MAIN
)

analytics_status.pack(
    side="right",
    pady=3
)


# ============================================================
# PRIMARY METRIC
# ============================================================

primary_card = tk.Frame(
    right_panel,
    bg=BG_CARD,
    height=75,
    highlightbackground=BORDER,
    highlightthickness=1
)

primary_card.pack(
    fill="x",
    pady=(0, 4)
)

primary_card.pack_propagate(False)


primary_accent = tk.Frame(
    primary_card,
    bg=SUCCESS,
    width=4
)

primary_accent.pack(
    side="left",
    fill="y"
)


primary_content = tk.Frame(
    primary_card,
    bg=BG_CARD
)

primary_content.pack(
    fill="both",
    expand=True,
    padx=14
)


primary_top = tk.Frame(
    primary_content,
    bg=BG_CARD
)

primary_top.pack(
    fill="x",
    pady=(7, 0)
)


primary_label = tk.Label(
    primary_top,
    text="CURRENT FACES",
    font=("Segoe UI", 7, "bold"),
    fg=TEXT_MUTED,
    bg=BG_CARD
)

primary_label.pack(
    side="left"
)


primary_state = tk.Label(
    primary_top,
    text="LIVE",
    font=("Segoe UI", 6, "bold"),
    fg=SUCCESS_LIGHT,
    bg="#12301F",
    padx=5,
    pady=2
)

primary_state.pack(
    side="right"
)


faces_value = tk.Label(
    primary_content,
    text="0",
    font=("Segoe UI", 22, "bold"),
    fg=TEXT_PRIMARY,
    bg=BG_CARD
)

faces_value.pack(
    anchor="w"
)


# ============================================================
# SECONDARY ANALYTICS CARD
# ============================================================

def create_card(
    parent,
    label_text,
    value_text,
    accent=ACCENT_BLUE
):

    card = tk.Frame(
        parent,
        bg=BG_CARD,
        height=53,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        fill="x",
        pady=2
    )

    card.pack_propagate(False)


    accent_line = tk.Frame(
        card,
        bg=accent,
        width=3
    )

    accent_line.pack(
        side="left",
        fill="y"
    )


    content = tk.Frame(
        card,
        bg=BG_CARD
    )

    content.pack(
        fill="both",
        expand=True,
        padx=12
    )


    label = tk.Label(
        content,
        text=label_text,
        font=("Segoe UI", 7, "bold"),
        fg=TEXT_MUTED,
        bg=BG_CARD
    )

    label.pack(
        anchor="w",
        pady=(5, 0)
    )


    value = tk.Label(
        content,
        text=value_text,
        font=("Segoe UI", 14, "bold"),
        fg=TEXT_PRIMARY,
        bg=BG_CARD
    )

    value.pack(
        anchor="w"
    )


    return value


# ============================================================
# ANALYTICS
# ============================================================

events_value = create_card(
    right_panel,
    "DETECTION EVENTS",
    "0",
    ACCENT_BLUE
)


screenshots_value = create_card(
    right_panel,
    "SCREENSHOTS",
    "0",
    ACCENT_BLUE
)


session_value = create_card(
    right_panel,
    "SESSION TIME",
    "00:00",
    TEXT_MUTED
)


fps_value = create_card(
    right_panel,
    "FPS",
    "0",
    SUCCESS
)


peak_value = create_card(
    right_panel,
    "PEAK OCCUPANCY",
    "0",
    WARNING
)


average_value = create_card(
    right_panel,
    "AVG FACES",
    "0.0",
    ACCENT_BLUE
)


occupancy_percentage_value = create_card(
    right_panel,
    "OCCUPANCY",
    "0%",
    SUCCESS
)


# ============================================================
# SYSTEM STATUS
# ============================================================

status_frame = tk.Frame(
    right_panel,
    bg=BG_CARD,
    height=46,
    highlightbackground=BORDER,
    highlightthickness=1
)

status_frame.pack(
    fill="x",
    pady=(6, 2)
)

status_frame.pack_propagate(False)


status_left = tk.Frame(
    status_frame,
    bg=BG_CARD
)

status_left.pack(
    side="left",
    padx=12
)


status_title = tk.Label(
    status_left,
    text="SYSTEM STATUS",
    font=("Segoe UI", 7, "bold"),
    fg=TEXT_MUTED,
    bg=BG_CARD
)

status_title.pack(
    anchor="w",
    pady=(4, 0)
)


status_value = tk.Label(
    status_left,
    text="●  CAMERA ONLINE",
    font=("Segoe UI", 8, "bold"),
    fg=SUCCESS_LIGHT,
    bg=BG_CARD
)

status_value.pack(
    anchor="w"
)


# ============================================================
# IoT SENSOR STATUS
# ============================================================

sensor_frame = tk.Frame(
    right_panel,
    bg=BG_CARD,
    height=46,
    highlightbackground=BORDER,
    highlightthickness=1
)

sensor_frame.pack(
    fill="x",
    pady=2
)

sensor_frame.pack_propagate(False)


sensor_left = tk.Frame(
    sensor_frame,
    bg=BG_CARD
)

sensor_left.pack(
    side="left",
    padx=12
)


sensor_title = tk.Label(
    sensor_left,
    text="IoT SENSOR STATUS",
    font=("Segoe UI", 7, "bold"),
    fg=TEXT_MUTED,
    bg=BG_CARD
)

sensor_title.pack(
    anchor="w",
    pady=(4, 0)
)


sensor_value = tk.Label(
    sensor_left,
    text="●  SIMULATED SENSORS ACTIVE",
    font=("Segoe UI", 8, "bold"),
    fg=WARNING_LIGHT,
    bg=BG_CARD
)

sensor_value.pack(
    anchor="w"
)


# ============================================================
# CAPTURE FUNCTION
# ============================================================

def capture_image():

    global screenshots_taken
    global capture_number

    if current_frame is None:

        return


    filename = (
        f"detection_{capture_number:03d}.jpg"
    )


    path = os.path.join(
        CAPTURE_FOLDER,
        filename
    )


    cv2.imwrite(
        path,
        current_frame
    )


    screenshots_taken += 1

    capture_number += 1


    screenshots_value.config(
        text=str(
            screenshots_taken
        )
    )


    add_event(
        f"Screenshot captured · {filename}"
    )


# ============================================================
# CAPTURE BUTTON
# ============================================================

capture_button = tk.Button(
    right_panel,
    text="CAPTURE SCREENSHOT",
    font=("Segoe UI", 8, "bold"),
    fg=TEXT_PRIMARY,
    bg=ACCENT_BLUE,
    activebackground=ACCENT_BLUE_LIGHT,
    activeforeground=TEXT_PRIMARY,
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    command=capture_image
)

capture_button.pack(
    fill="x",
    pady=(7, 5),
    ipady=7
)


# ============================================================
# BUTTON HOVER
# ============================================================

def button_enter(event):

    capture_button.config(
        bg=ACCENT_BLUE_LIGHT
    )


def button_leave(event):

    capture_button.config(
        bg=ACCENT_BLUE
    )


capture_button.bind(
    "<Enter>",
    button_enter
)

capture_button.bind(
    "<Leave>",
    button_leave
)


# ============================================================
# VISION EVENTS HEADER
# ============================================================

events_header = tk.Frame(
    right_panel,
    bg=BG_MAIN
)

events_header.pack(
    fill="x",
    pady=(4, 4)
)


events_header_left = tk.Frame(
    events_header,
    bg=BG_MAIN
)

events_header_left.pack(
    side="left"
)


events_title = make_label(
    events_header_left,
    "VISION EVENTS",
    9,
    "bold",
    TEXT_PRIMARY,
    BG_MAIN
)

events_title.pack(
    side="left"
)


events_indicator = tk.Label(
    events_header_left,
    text="  ACTIVITY  ",
    font=("Segoe UI", 6, "bold"),
    fg=TEXT_SECONDARY,
    bg=BG_CARD,
    padx=3,
    pady=2
)

events_indicator.pack(
    side="left",
    padx=(7, 0)
)


events_live = make_label(
    events_header,
    "LIVE LOG",
    7,
    "normal",
    TEXT_MUTED,
    BG_MAIN
)

events_live.pack(
    side="right"
)


# ============================================================
# EVENT LOG
# ============================================================

event_list = tk.Listbox(
    right_panel,
    height=5,
    bg=BG_CARD,
    fg="#CBD5E1",
    font=("Consolas", 8),
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    selectbackground="#243B5A",
    selectforeground=TEXT_PRIMARY,
    activestyle="none"
)

event_list.pack(
    fill="both",
    expand=True
)


# ============================================================
# EVENT FUNCTION
# ============================================================

def add_event(message):

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )


    event_text = (
        f"{current_time}   {message}"
    )


    event_list.insert(
        0,
        event_text
    )


    while event_list.size() > 7:

        event_list.delete(7)


    file_exists = os.path.exists(
        EVENTS_FILE
    )


    with open(
        EVENTS_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )


        if not file_exists:

            writer.writerow([
                "Time",
                "Event"
            ])


        writer.writerow([
            current_time,
            message
        ])


# ============================================================
# UPDATE CHART
# ============================================================

def update_chart(face_count):

    elapsed = (
        time.time() -
        start_time
    )


    chart_times.append(
        elapsed
    )


    chart_faces.append(
        face_count
    )


    while (
        chart_times and
        elapsed - chart_times[0] > 30
    ):

        chart_times.pop(0)

        chart_faces.pop(0)


    if chart_times:

        line.set_data(
            chart_times,
            chart_faces
        )


        left_limit = max(
            0,
            elapsed - 30
        )


        right_limit = max(
            30,
            elapsed
        )


        ax.set_xlim(
            left_limit,
            right_limit
        )


        maximum_faces = max(
            max(chart_faces),
            1
        )


        ax.set_ylim(
            0,
            maximum_faces + 1
        )


    chart_canvas.draw_idle()


# ============================================================
# UPDATE SMART ENVIRONMENT
# ============================================================

def update_environment(face_count):

    global previous_occupancy


    occupied = (
        face_count > 0
    )


    if occupied:

        occupancy_value.config(
            text="OCCUPIED",
            fg=SUCCESS_LIGHT
        )


        response_value.config(
            text="LIGHT ACTIVE",
            fg=WARNING_LIGHT
        )

    else:

        occupancy_value.config(
            text="IDLE",
            fg=TEXT_SECONDARY
        )


        response_value.config(
            text="STANDBY",
            fg=TEXT_SECONDARY
        )


    temperature_value.config(
        text=f"{temperature:.1f} °C"
    )


    humidity_value.config(
        text=f"{humidity} %"
    )


    if occupied != previous_occupancy:

        if occupied:

            add_event(
                "Room occupied"
            )

        else:

            add_event(
                "Room idle"
            )


        previous_occupancy = occupied


# ============================================================
# SAVE SESSION HISTORY
# ============================================================

def save_session_history():

    session_seconds = int(
        time.time() -
        start_time
    )


    minutes = (
        session_seconds //
        60
    )


    seconds = (
        session_seconds %
        60
    )


    if face_sample_count > 0:

        average_faces = (
            total_face_samples /
            face_sample_count
        )


        occupancy_percentage = (
            occupied_samples /
            face_sample_count
        ) * 100

    else:

        average_faces = 0

        occupancy_percentage = 0


    file_exists = os.path.exists(
        SESSION_FILE
    )


    with open(
        SESSION_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )


        if not file_exists:

            writer.writerow([
                "Date",
                "Duration",
                "Peak Occupancy",
                "Average Faces",
                "Occupancy Percentage",
                "Detection Events",
                "Screenshots"
            ])


        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            f"{minutes:02d}:{seconds:02d}",
            peak_occupancy,
            f"{average_faces:.1f}",
            f"{occupancy_percentage:.0f}%",
            detection_events,
            screenshots_taken
        ])


# ============================================================
# CAMERA UPDATE
# ============================================================

def update_camera():

    global current_frame
    global previous_face_count
    global detection_events
    global last_time
    global fps
    global peak_occupancy
    global total_face_samples
    global face_sample_count
    global occupied_samples


    success, frame = camera.read()


    if not success:

        status_value.config(
            text="●  CAMERA ERROR",
            fg=DANGER
        )


        live_dot.config(
            fg=DANGER
        )


        live_text.config(
            text=" ERROR",
            fg=DANGER
        )


        root.after(
            30,
            update_camera
        )


        return


    current_frame = frame.copy()


    # ========================================================
    # FACE DETECTION
    # ========================================================

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # Improve image contrast

    gray = cv2.equalizeHist(
        gray
    )


    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=4,
        minSize=(35, 35)
    )


    face_count = len(
        faces
    )


    # ========================================================
    # SESSION STATISTICS
    # ========================================================

    total_face_samples += face_count

    face_sample_count += 1


    if face_count > 0:

        occupied_samples += 1


    if face_count > peak_occupancy:

        peak_occupancy = face_count


    average_faces = (
        total_face_samples /
        face_sample_count
    )


    occupancy_percentage = (
        occupied_samples /
        face_sample_count
    ) * 100


    peak_value.config(
        text=str(
            peak_occupancy
        )
    )


    average_value.config(
        text=f"{average_faces:.1f}"
    )


    occupancy_percentage_value.config(
        text=f"{occupancy_percentage:.0f}%"
    )


    # ========================================================
    # DRAW FACE DETECTION
    # ========================================================

    for (x, y, w, h) in faces:

        # Outer detection box

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )


        # FACE label

        cv2.rectangle(
            frame,
            (x, y - 27),
            (x + 70, y),
            (0, 255, 0),
            -1
        )


        cv2.putText(
            frame,
            "FACE",
            (x + 7, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA
        )


    # ========================================================
    # FPS
    # ========================================================

    current_time = time.time()


    elapsed = (
        current_time -
        last_time
    )


    if elapsed > 0:

        fps = 1 / elapsed


    last_time = current_time


    # ========================================================
    # ANALYTICS
    # ========================================================

    faces_value.config(
        text=str(
            face_count
        )
    )


    fps_value.config(
        text=f"{fps:.1f}"
    )


    # ========================================================
    # DETECTION EVENTS
    # ========================================================

    if face_count != previous_face_count:

        detection_events += 1


        events_value.config(
            text=str(
                detection_events
            )
        )


        if face_count == 0:

            add_event(
                "No face detected"
            )


        elif face_count == 1:

            add_event(
                "1 face detected"
            )


        else:

            add_event(
                f"{face_count} faces detected"
            )


        previous_face_count = face_count


    # ========================================================
    # SMART ENVIRONMENT
    # ========================================================

    update_environment(
        face_count
    )


    # ========================================================
    # SESSION TIME
    # ========================================================

    session_seconds = int(
        time.time() -
        start_time
    )


    minutes = (
        session_seconds //
        60
    )


    seconds = (
        session_seconds %
        60
    )


    session_value.config(
        text=f"{minutes:02d}:{seconds:02d}"
    )


    # ========================================================
    # UPDATE CHART
    # ========================================================

    update_chart(
        face_count
    )


    # ========================================================
    # CAMERA STATUS
    # ========================================================

    status_value.config(
        text="●  CAMERA ONLINE",
        fg=SUCCESS_LIGHT
    )


    live_dot.config(
        fg=SUCCESS
    )


    live_text.config(
        text=" LIVE",
        fg=SUCCESS_LIGHT
    )


    # ========================================================
    # CAMERA OVERLAY
    # ========================================================

    timestamp = datetime.now().strftime(
        "%Y-%m-%d  %H:%M:%S"
    )


    # Timestamp

    cv2.putText(
        frame,
        timestamp,
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # Occupancy

    if face_count > 0:

        occupancy_text = (
            "ROOM: OCCUPIED"
        )

        occupancy_color = (
            0,
            255,
            0
        )

    else:

        occupancy_text = (
            "ROOM: IDLE"
        )

        occupancy_color = (
            180,
            180,
            180
        )


    cv2.putText(
        frame,
        occupancy_text,
        (15, 57),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        occupancy_color,
        2,
        cv2.LINE_AA
    )


    # AI status

    cv2.putText(
        frame,
        "AI VISION",
        (15, 82),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # Face counter

    cv2.putText(
        frame,
        f"FACES: {face_count}",
        (540, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # ========================================================
    # DISPLAY VIDEO
    # ========================================================

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    image = Image.fromarray(
        frame_rgb
    )


    image = image.resize(
        (660, 315)
    )


    photo = ImageTk.PhotoImage(
        image=image
    )


    video_label.config(
        image=photo
    )


    video_label.image = photo


    # ========================================================
    # NEXT FRAME
    # ========================================================

    root.after(
        30,
        update_camera
    )


# ============================================================
# CLOSE APPLICATION
# ============================================================

def close_application():

    save_session_history()

    camera.release()

    cv2.destroyAllWindows()

    root.destroy()


# ============================================================
# WINDOW CLOSE EVENT
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ============================================================
# START APPLICATION
# ============================================================

add_event(
    "Smart Vision Studio started"
)

add_event(
    "IoT sensors running in simulation mode"
)


update_camera()

root.mainloop()