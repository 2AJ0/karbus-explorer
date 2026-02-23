# Wayfare 🚌 

**Wayfare** is a high-performance desktop transit explorer for Karnataka's inter-city bus network. Designed for efficiency, it allows users to navigate complex schedules, compare fares, and find the fastest routes through a clean, native GUI.

## 🛠 Features

* **Intelligent Route Filtering:** Search by source, destination, and specific days of departure.
* **Safety & Quality Indicators:** Visual warnings (⚠) automatically flag low-rated operators or buses with critically low seat availability.
* **One-Touch Optimization:** * **Cheapest:** Instantly isolates the lowest fare for your route.
    * **Fastest:** Calculates and surfaces the shortest travel duration.
* **Advanced Bus Specs:** Toggle filters for AC and Sleeper preferences, or set specific Rating and Fare thresholds.
* **Interactive Data Table:** Sortable results for Timing, Fare, Rating, and Duration.

## 🚀 Getting Started

### Prerequisites
Wayfare is built with **Python 3.x** and requires the **wxPython** toolkit for its graphical interface.

## 📊 Technical Overview
UI Framework: wxPython for a native OS look and feel.

Data Handling: Standard Python csv and datetime libraries for lightweight, database-free performance.

Logic: Custom sorting algorithms for duration parsing (HHh MMm format) and fare optimization.

### 📜 License
Distributed under the MIT License.

### 🤖 AI Attribution
This project was developed with the assistance of Gemini, an AI collaborator by Google. AI was used to help architect the GUI structure, refine the search logic, and generate project documentation.
