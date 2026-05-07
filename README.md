# 🖐️ Hand-Gesture Tic-Tac-Toe with Arduino LED Integration

An interactive, computer-vision-based Tic-Tac-Toe game that you play using hand gestures via your webcam. The game tracks your hands to place 'X's and 'O's on a virtual board, and communicates with an Arduino in real-time to control a physical LED strip based on the game's progress and win states.

## ✨ Features
* **Computer Vision:** Uses OpenCV and MediaPipe to draw a virtual 3x3 grid and track hand movements.
* **Hand Recognition:** The game assigns the Left Hand as 'X' and the Right Hand as 'O'.
* **Gesture Controls:** Hover your index finger over an empty circle to make a move.
* **Hardware Integration:** Communicates with an Arduino via Serial to trigger physical lighting effects when a move is made or a game is won.
* **Auto-Reset:** Automatically detects winning combinations, updates the score, and resets the board for seamless gameplay.

---

## 🛠️ How It Was Built

### Phase 1: Building from Scratch (The Software)
The project started as a pure Python computer vision script. 
1. **The Board:** OpenCV is used to draw a 3x3 grid of circles on the webcam feed.
2. **Hand Tracking:** Using the `cvzone` wrapper for MediaPipe, the script detects up to two hands. It specifically tracks landmark #8 (the tip of the index finger).
3. **Game Logic:** The script enforces alternating turns (Left hand vs. Right hand). When the index finger hovers over a circle's coordinates, it claims that space for the respective player. An array of 9 slots continually checks against 8 possible winning combinations (rows, columns, diagonals).

### Phase 2: The Hardware Update (Arduino Integration)
To bring the game into the physical world, hardware communication was added.
1. **Serial Communication:** Added the `pyserial` library to open a line of communication (`COM6` at 9600 baud) between the Python script and an Arduino.
2. **Move Signals:** When a player makes a move, Python sends a byte (`b'X'` or `b'O'`) to the Arduino, triggering the LED strip to flash Red or Blue.
3. **Endgame Signals:** The `check_winner` logic was updated. When 'X' wins, it sends a `b'W'` signal. When 'O' wins, it sends a `b'L'` signal. Both signals trigger the Arduino to light the entire LED strip Green, celebrating the end of the round before the board resets.

---

## 📋 Requirements

### Software
* Python 3.x
* A webcam

### Hardware
* Arduino (Uno, Nano, or similar)
* Addressable LED Strip (e.g., WS2812B / NeoPixels) connected to Pin 6.

---

## 🚀 Installation & Setup

### 1. Arduino Setup
1. Open the Arduino IDE.
2. Install the **FastLED** library via the Library Manager.
3. Upload the provided C++ code to your Arduino.
4. Note the COM port your Arduino is connected to (e.g., `COM6`).

### 2. Python Setup
1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/Ammushama/tictactoe.git](https://github.com/Ammushama/tictactoe.git)
   cd tictactoe
