# **Clash Royale Bot (Automated Game Player)**

This project implements an automated bot designed to play Clash Royale on an Android emulator (like BlueStacks) using image recognition and strategic decision-making. The bot leverages ADB (Android Debug Bridge) for screen capture and interaction, OpenCV for visual analysis, and a modular Python framework for its core logic.

## **Features**

* **Real-time Screen Capture:** Captures screenshots from the Android emulator/device using ADB.  
* **Image Preprocessing:** Utilizes OpenCV to preprocess screenshots for better detection.  
* **Game State Detection:** Identifies the current game state (e.g., On Menu, In Battle, Post Game) by detecting key UI elements.  
* **Card Detection:** Detects cards in the player's hand using template matching within a defined Region of Interest (ROI).  
* **Enemy Unit Detection:** Detects opponent units on the battlefield using template matching within a defined ROI.  
* **Basic Strategy Engine:** Makes decisions on which card to play and where to place it, considering the presence and location of enemy units.  
* **Emulator Interaction:** Simulates taps and swipes on the emulator/device via ADB commands.  
* **Debugging Visualizations:** Saves debug images with ROIs and detected elements highlighted to aid in tuning and troubleshooting.

## **Project Structure**

D:.  
├───main.py                     \# Main entry point to run the bot  
├───directory\_structure.txt     \# (Your project structure file)  
├───requirements.txt            \# List of Python dependencies  
│  
├───core  
│   ├───bot\_loop.py             \# The main bot loop and state machine  
│   ├───game\_states.py          \# Enum for different game states  
│   └───\_\_init\_\_.py  
│  
├───emulator  
│   ├───emulator.py             \# Handles interaction with the Android emulator via ADB  
│   └───\_\_init\_\_.py  
│  
├───strategy  
│   ├───strategy\_engine.py      \# Decides actions based on game state and detected objects  
│   └───\_\_init\_\_.py  
│  
└───vision  
    ├───vision\_system.py        \# Orchestrates image processing and detection  
    ├───\_\_init\_\_.py  
    └───templates  
        ├───cards               \# Directory for player's card image templates (e.g., knight.png)  
        ├───enemy\_units         \# Directory for enemy unit image templates (e.g., goblin.png)  
        └───ui\_elements         \# Directory for UI element image templates (e.g., play\_button.png)

## **Setup and Installation**

1. **Python:** Ensure you have Python 3.x installed.  
2. **ADB (Android Debug Bridge):**  
   * Download the [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools).  
   * Extract the contents (which include adb.exe) to a convenient location (e.g., C:\\adb\\platform-tools).  
   * **Add this directory to your system's PATH environment variable.** This allows you to run adb commands from any terminal.  
3. **Android Emulator (e.g., BlueStacks):**  
   * Install and configure an Android emulator (like BlueStacks) and install Clash Royale on it.  
   * **Set the emulator resolution to 720x1280 (width x height)** for compatibility with the current bot's ROI settings.  
   * Ensure the emulator is running and **ADB debugging is enabled** (check emulator settings).  
   * **Verify ADB connection:** Open your terminal and run adb devices. You should see your emulator listed (e.g., emulator-5554 device). If not, you might need to run adb connect localhost:\<port\> (check your emulator's ADB port, often 5555).  
4. **Python Dependencies:**  
   * Navigate to your project's root directory (D:\\bot\_v2\\).  
   * Install the required Python libraries using pip:  
     pip install \-r requirements.txt

     (The requirements.txt file contains numpy, opencv-python, Pillow).  
5. **Image Templates:**  
   * **Crucial Step:** The bot relies heavily on image templates for detection. You *must* create and populate the template directories:  
     * D:\\bot\_v2\\vision\\templates\\cards\\  
     * D:\\bot\_v2\\vision\\templates\\enemy\_units\\  
     * D:\\bot\_v2\\vision\\templates\\ui\_elements\\  
   * **How to get templates:**  
     * Launch Clash Royale in your 720x1280 BlueStacks emulator.  
     * Use adb exec-out screencap \-p \> screenshot.png in your terminal to capture full screenshots of various game states (main menu, in-battle, post-game).  
     * Open these screenshots in an image editor (e.g., Paint, GIMP, Photoshop).  
     * **Carefully crop** small, precise images of:  
       * **Your cards in hand:** (e.g., knight.png, wizard.png). Crop tightly around the card art.  
       * **Enemy units:** (e.g., goblin.png, bomber.png). Crop tightly around the unit model.  
       * **UI elements:**  
         * play\_button.png (the button to start a battle)  
         * battle\_indicator.png (a small, unique, and static part of the in-battle UI, like a corner of the elixir bar or a specific HUD icon)  
         * ok\_button.png (the button to dismiss post-game screens)  
         * home\_button.png (a button to return to the main menu)  
     * Save these cropped images into their respective template folders. The filenames should match the expected names (e.g., play\_button.png for "Play Button").

## **Running the Bot**

1. Ensure your Android emulator (BlueStacks) is running Clash Royale at 720x1280 resolution.  
2. Open your terminal or command prompt.  
3. Navigate to your project's root directory (D:\\bot\_v2\\).  
4. Run the main script:  
   python main.py

5. Observe the logs in your terminal. The bot will start capturing screenshots and attempting to detect game elements and perform actions.

## **Debugging and Tuning**

* debug\_vision\_output **folder:** The bot will create a debug\_vision\_output folder in your project root. This folder will contain images (hand\_roi\_debug\_\*.png, battlefield\_roi\_debug\_\*.png) with colored rectangles drawn around the ROIs and detected elements. Use these images to visually verify if your ROIs and templates are accurate.  
* **Adjusting ROIs:** If the yellow/magenta rectangles in the debug images don't perfectly cover the intended areas, adjust self.hand\_roi and self.battlefield\_roi in vision\_system.py.  
* **Adjusting Thresholds:** If the bot misses detections or has too many false positives, adjust the threshold values in \_find\_template calls within vision\_system.py. Higher thresholds mean stricter matches.  
* **Refining Templates:** The quality and precision of your image templates are paramount. Re-capture and re-crop them if detection is inconsistent.  
* **Strategy Refinement:** Once detection is reliable, focus on expanding \_get\_card\_properties and self.counter\_map in strategy\_engine.py to implement more sophisticated decision-making.

## **License**

MIT License

Copyright (c) 2025 \[Joeri Wijers\]

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.  
