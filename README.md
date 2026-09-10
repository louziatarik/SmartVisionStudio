\# 🧠 Smart Vision Studio



> \*\*AI Visual Perception \& Smart Environment Dashboard\*\*



Smart Vision Studio is a Python-based computer vision dashboard that uses a webcam and a pre-trained Haar Cascade classifier to detect faces in real time.



The project combines \*\*computer vision, real-time monitoring, data visualization, and simulated IoT environment responses\*\* into a single desktop dashboard.



It was developed as part of an AI Visual Perception laboratory project and extended into a more complete portfolio project focused on practical AI and IoT concepts.



\---



\## 📸 Dashboard



!\[Smart Vision Studio Dashboard](screenshots/dashboard-main.png)



The dashboard provides a real-time overview of camera activity, detected faces, occupancy, system status, analytics, and simulated environmental conditions.



\---



\## ✨ Features



\### 👁️ Real-Time Face Detection



\* Webcam-based computer vision

\* Pre-trained Haar Cascade face detector

\* Real-time face bounding boxes

\* Face count monitoring

\* Detection status indicators



\### 📊 Live Analytics



\* Current face count

\* Peak occupancy

\* Average detected faces

\* Occupancy percentage

\* Real-time activity graph

\* FPS monitoring

\* Session duration



\### 🏢 Smart Environment Simulation



\* Occupancy status: `IDLE` / `OCCUPIED`

\* Simulated temperature monitoring

\* Simulated humidity monitoring

\* Smart response status

\* Simulated IoT sensor status



\### 📷 Event \& Screenshot System



\* Capture screenshots directly from the dashboard

\* Record vision events

\* Track changes in detected face count

\* Store session history

\* Export monitoring data to CSV files



\### 🎨 Professional Dashboard



\* Dark modern interface

\* Real-time status indicators

\* Camera monitoring panel

\* Analytics cards

\* Activity visualization

\* Smart environment panel

\* Vision event log



\---



\## 🧠 How the Computer Vision Works



Smart Vision Studio uses \*\*OpenCV\*\* together with a pre-trained \*\*Haar Cascade classifier\*\*.



The basic detection pipeline is:



```text

Webcam

&#x20;  ↓

Video Frame

&#x20;  ↓

Grayscale Conversion

&#x20;  ↓

Histogram Equalization

&#x20;  ↓

Haar Cascade Detection

&#x20;  ↓

Face Bounding Boxes

&#x20;  ↓

Dashboard Analytics

&#x20;  ↓

Smart Environment Response

```



For each webcam frame, the system:



1\. Captures the image from the webcam.

2\. Converts the frame to grayscale.

3\. Applies histogram equalization to improve detection under different lighting conditions.

4\. Runs the Haar Cascade face detector.

5\. Identifies detected faces.

6\. Draws bounding boxes around detected faces.

7\. Updates the dashboard statistics.

8\. Records relevant vision events.



> \*\*Note:\*\* The current implementation uses a classical pre-trained Haar Cascade detector. It is designed primarily for frontal face detection and is not a deep-learning face recognition system.



\---



\## 🌐 IoT \& Smart Environment Concept



The project demonstrates how computer vision could interact with a smart environment.



For example:



```text

Face Detected

&#x20;    ↓

Room = OCCUPIED

&#x20;    ↓

Smart Response = LIGHT ACTIVE

```



When no face is detected:



```text

No Face

&#x20;  ↓

Room = IDLE

&#x20;  ↓

Smart Response = STANDBY

```



Temperature and humidity values are currently \*\*simulated\*\* to demonstrate how the computer vision system could eventually communicate with physical IoT sensors.



\---



\## 🛠️ Technologies



| Technology   | Purpose                               |

| ------------ | ------------------------------------- |

| Python       | Main programming language             |

| OpenCV       | Computer vision and webcam processing |

| Tkinter      | Desktop dashboard interface           |

| NumPy        | Numerical processing                  |

| Matplotlib   | Real-time analytics visualization     |

| CSV          | Session and event data storage        |

| Haar Cascade | Pre-trained face detection            |



\---



\## 📁 Project Structure



```text

SmartVisionStudio/

│

├── dashboard.py

├── smart\_vision.py

├── README.md

├── .gitignore

│

└── screenshots/

&#x20;   └── dashboard-main.png

```



Runtime-generated files such as screenshots, session history, and vision event logs are excluded from version control.



\---



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/louziatarik/SmartVisionStudio.git

```



\### 2. Open the project



```bash

cd SmartVisionStudio

```



\### 3. Install the required Python packages



```bash

pip install opencv-python numpy matplotlib

```



Tkinter is normally included with standard Python installations on Windows.



\---



\## ▶️ Running the Application



Run:



```bash

python dashboard.py

```



The Smart Vision Studio dashboard will open.



Make sure your webcam is available and allow camera access if Windows requests permission.



\---



\## 📈 Monitoring Data



During operation, the application can generate runtime data including:



```text

session\_history.csv

vision\_events.csv

detection\_log.txt

```



These files contain information such as:



\* Detection events

\* Face count changes

\* Session information

\* Timestamps

\* Monitoring statistics



They are intentionally excluded from GitHub because they are generated during local application use.



\---



\## 🎯 Project Goals



This project demonstrates practical concepts in:



\* Computer Vision

\* Artificial Intelligence

\* Real-Time Data Processing

\* Human-Computer Interaction

\* Data Visualization

\* IoT Concepts

\* Smart Environment Monitoring



The goal was not only to implement face detection, but also to transform a basic computer vision experiment into a more complete monitoring application.



\---



\## 🔮 Future Improvements



Possible future versions could include:



\* 🤖 Deep-learning-based object detection

\* 📱 Web or mobile dashboard

\* 🌐 Real IoT sensor integration

\* 🗄️ Database integration

\* 👥 Multi-camera monitoring

\* 📊 Advanced historical analytics

\* 🔔 Real-time notifications

\* ☁️ Cloud-based monitoring

\* 🧠 More advanced occupancy intelligence



\---



\## 📚 Academic Context



This project was developed from an \*\*AI Visual Perception — Face Detection with Webcam\*\* laboratory exercise.



The original laboratory objective was to understand how computer vision can detect human faces using a webcam and a pre-trained detection model.



Smart Vision Studio extends this concept into a more complete application with a graphical dashboard, monitoring analytics, event logging, and smart-environment simulation.



\---



\## 👨‍💻 Author



\*\*Tarik Louzia\*\*



Computer Science Student

Dalian Polytechnic University



GitHub:

https://github.com/louziatarik



\---



\## ⭐ Project



If you find this project interesting, feel free to explore the code and follow its development.



\*\*Smart Vision Studio — From Computer Vision Experiment to Smart Monitoring Dashboard.\*\*



