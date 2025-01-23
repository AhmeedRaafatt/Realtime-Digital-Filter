# Realtime Digital Filter Design

![Project Logo](https://via.placeholder.com/1000x200?text=Realtime+Digital+Filter+Design)

## Overview
Realtime Digital Filter Design is an interactive desktop application that allows users to design and visualize digital filters through zero-pole placement on the z-plane. The application supports various customization options, real-time signal processing, and filter realization, making it an invaluable tool for engineers, researchers, and enthusiasts in signal processing.

---

## Features

### 🔐 Z-Plane Visualization and Interaction
- **Interactive Z-Plane Plot**:
  - Unit circle representation.
  - Users can place zeros and poles interactively.
  
![Z-Plane Example](https://via.placeholder.com/800x400?text=Z-Plane+Visualization)

- **Modification Options**:
  - Drag-and-drop functionality for placed zeros/poles.
  - Click-to-delete specific zeros/poles.
  - Clear options: Clear all zeros, all poles, or all elements.
  - Add conjugates for complex elements (optional).
  - Zero-pole swapping feature.
  - Undo/redo for all operations.

### 🏢 Filter Realization and Export
- **Filter Realization**:
  - Direct Form II realization.
  - Cascade form realization.
- **C Code Generation**:
  - Automatically generate C code for the designed filter.

![C Code Example](https://via.placeholder.com/800x400?text=Generated+C+Code+Example)

### 🎥 Frequency Response Visualization
- **Magnitude and Phase Response**:
  - Separate plots for magnitude response and phase response.

![Frequency Response](https://via.placeholder.com/800x400?text=Magnitude+and+Phase+Response)

### 🔒 Built-In Filter Library
- Predefined library of 10+ famous digital filters, including:
  - Low-Pass Filters (LPF)
  - High-Pass Filters (HPF)
  - Band-Pass Filters (BPF)
  - Filter Types: Butterworth, Chebyshev, Inverse Chebyshev, Bessel, and Elliptic.

### ⏱️ Real-Time Filtering
- **Apply Filter to Real-Time Signal**:
  - Process a lengthy signal (minimum 10,000 points) in real-time.
  - Visualize the time progress of both the input and filtered signals.
- **Custom Signal Input**:
  - Generate signals by moving the mouse within a dedicated area.
  - Mouse speed correlates to signal frequency.
- **Control Temporal Resolution**:
  - Adjustable speed via a slider to process points per second.

![Real-Time Processing](https://via.placeholder.com/800x400?text=Real-Time+Signal+Processing)

### ⚖️ Phase Correction with All-Pass Filters
- **All-Pass Filter Library**:
  - Visualize and select from predefined all-pass filters.
  - View zero-pole combinations and phase responses.
- **Custom All-Pass Filter Design**:
  - Define custom “a” coefficients.
  - Integrate custom filters into the library.
- **Enable/Disable All-Pass Filters**:
  - Toggle filters using a drop-down menu or checkbox group.

---

## 💻 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PavlyAwad/Realtime-Digital-Filter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd realtime-digital-filter-design
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

## 🔧 Usage

1. **Designing Filters**:
   - Open the application and use the Z-Plane plot to place zeros and poles.
   - Modify, delete, or clear elements as needed.
2. **Visualizing Responses**:
   - View the magnitude and phase response in real-time.
3. **Filter Realization**:
   - Select the realization form and export the design.
4. **Real-Time Processing**:
   - Apply the designed filter to a signal and visualize the output.
   - Use the slider to adjust processing speed.
5. **Phase Correction**:
   - Add or customize all-pass filters to correct phase distortion.

---

## 🎨 Examples

### Interactive Z-Plane Design
![Interactive Design](https://via.placeholder.com/800x400?text=Interactive+Z-Plane+Design)

### Built-In Filter Library
![Built-In Filters](https://via.placeholder.com/800x400?text=Built-In+Filter+Library)

### Real-Time Signal Processing
![Real-Time Example](https://via.placeholder.com/800x400?text=Real-Time+Signal+Processing)

---

## 🔗 References
- [EarLevel Engineering - Pole-Zero Placement](https://www.earlevel.com/main/2013/10/28/pole-zero-placement-v2/)
- [Filter Frequency Response Grapher](https://www.earlevel.com/main/2016/12/08/filter-frequency-response-grapher/)
- [MicroModeler DSP](https://www.micromodeler.com/dsp)

---

## 🔒 License
This project is licensed under the MIT License. See the LICENSE file for details.

---


## 🌐 Contributors
- [Ziad Mohamed](https://github.com/Ziadmohammed200)  
- [Marcilino Adel](https://github.com/marcilino-adel)  
- [Ahmed Etman](https://github.com/AhmedEtma)  
- [Pavly Awad](https://github.com/PavlyAwad)  
- [Ahmed Rafat](https://github.com/AhmeedRaafatt)  

