import logging
import time
import subprocess  # For running ADB commands
import numpy as np
from PIL import Image  # For converting ADB screenshot output
import io  # NEW: Import the io module for BytesIO

# Configure logging for better visibility of actions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ADBEmulatorInterface:
    """
    An implementation of the emulator interface using ADB (Android Debug Bridge).
    This class executes ADB commands via subprocess to interact with an Android device/emulator.
    """

    def __init__(self, adb_path: str = "adb", device_id: str = None):
        """
        Initializes the ADBEmulatorInterface.

        Args:
            adb_path (str): The path to the adb executable. Defaults to "adb"
                            assuming it's in your system's PATH.
            device_id (str): Optional. The serial number or IP:port of the
                             specific device/emulator to connect to. If None,
                             ADB will connect to the only available device or
                             default emulator.
        """
        self.adb_path = adb_path
        self.device_id = device_id
        self.adb_prefix = [self.adb_path]
        if self.device_id:
            self.adb_prefix.extend(["-s", self.device_id])

        self.vision_system = None  # Will be set by the Emulator during its initialization
        logging.info(
            f"ADBEmulatorInterface initialized. ADB Path: '{self.adb_path}', Device ID: '{self.device_id or 'default'}'")
        self._check_adb_connection()

    def _run_adb_command(self, command: list, capture_output: bool = False, text: bool = False):
        """Helper to run an ADB command."""
        full_command = self.adb_prefix + command
        try:
            result = subprocess.run(
                full_command,
                capture_output=capture_output,
                text=text,
                check=True,  # Raise CalledProcessError for non-zero exit codes
                timeout=10  # Timeout for ADB commands
            )
            if capture_output:
                return result.stdout
            return True
        except FileNotFoundError:
            logging.error(
                f"ADB executable not found at '{self.adb_path}'. Please ensure ADB is installed and in your system's PATH, or provide the correct path.")
            raise
        except subprocess.CalledProcessError as e:
            logging.error(f"ADB command failed: {' '.join(full_command)}\nStderr: {e.stderr.strip()}")
            raise
        except subprocess.TimeoutExpired:
            logging.error(f"ADB command timed out: {' '.join(full_command)}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while running ADB command: {e}")
            raise

    def _check_adb_connection(self):
        """Verifies ADB connection and lists devices."""
        try:
            output = self._run_adb_command(["devices"], capture_output=True, text=True)
            logging.info(f"ADB devices output:\n{output.strip()}")
            if "device" in output:
                logging.info("ADB connection successful.")
            else:
                logging.warning(
                    "No ADB devices found or connected. Please ensure your device/emulator is running and ADB debugging is enabled.")
        except Exception as e:
            logging.error(f"Failed to check ADB connection: {e}")
            # Do not re-raise, allow initialization to complete but warn user

    def set_vision_system(self, vision_system):
        """Sets the VisionSystem instance for this interface to use."""
        self.vision_system = vision_system
        logging.info("ADBEmulatorInterface linked with VisionSystem.")

    def get_screen(self) -> np.ndarray:
        """
        Captures the current screen from the Android device/emulator using ADB
        and returns it as a NumPy array.
        """
        logging.info("ADB: Capturing screen from device.")
        try:
            # Command to capture screenshot and output as PNG to stdout
            png_data = self._run_adb_command(["exec-out", "screencap", "-p"], capture_output=True)

            # Read PNG data into PIL Image using io.BytesIO
            screenshot_pil = Image.open(io.BytesIO(png_data))

            # Convert PIL Image to NumPy array (OpenCV format BGR)
            screen_np = np.array(screenshot_pil)
            # Convert RGB (PIL default) to BGR (OpenCV default)
            screen_np = screen_np[:, :, ::-1].copy()
            return screen_np
        except Exception as e:
            logging.error(f"Failed to capture screen via ADB: {e}")
            # Return a dummy black image on failure to prevent crashes
            return np.zeros((960, 540, 3), dtype=np.uint8)

    def click(self, x: int, y: int):
        """Simulates a tap (click) at the given coordinates using ADB."""
        logging.info(f"ADB: Tapping at ({x}, {y})")
        self._run_adb_command(["shell", "input", "tap", str(x), str(y)])

    def wait(self, duration: float):
        """Waits for a specified duration."""
        logging.info(f"Waiting for {duration} seconds.")
        time.sleep(duration)

    def mouse_down(self, x: int, y: int, button: str = 'left'):
        """
        Simulates a mouse down. For ADB, this is part of a swipe command.
        This method is kept for compatibility but will be primarily used by simulate_click_and_drag.
        """
        logging.debug(f"ADB: Mouse down at ({x}, {y}) is part of a swipe operation.")
        # ADB doesn't have separate mouse_down/mouse_up for touch.
        # This will be handled by the simulate_click_and_drag method using 'swipe'.

    def mouse_move(self, x: int, y: int, duration: float = 0.1):
        """
        Simulates mouse movement. For ADB, this is part of a swipe command.
        This method is kept for compatibility but will be primarily used by simulate_click_and_drag.
        """
        logging.debug(f"ADB: Mouse move to ({x}, {y}) is part of a swipe operation.")
        # ADB doesn't have separate mouse_move for touch.
        # This will be handled by the simulate_click_and_drag method using 'swipe'.

    def mouse_up(self, x: int, y: int, button: str = 'left'):
        """
        Simulates a mouse up. For ADB, this is part of a swipe command.
        This method is kept for compatibility but will be primarily used by simulate_click_and_drag.
        """
        logging.debug(f"ADB: Mouse up at ({x}, {y}) is part of a swipe operation.")
        # ADB doesn't have separate mouse_up for touch.
        # This will be handled by the simulate_click_and_drag method using 'swipe'.

    def get_card_location(self, card_name: str) -> tuple | None:
        """
        Queries the VisionSystem to find the screen coordinates of a specific card in the hand.
        """
        if self.vision_system:
            logging.info(f"ADB: Requesting card location for '{card_name}' from VisionSystem.")
            # This calls a method on the VisionSystem to get the card's coordinates
            return self.vision_system.get_card_coordinates(card_name)
        else:
            logging.error("VisionSystem not set in ADBEmulatorInterface. Cannot get card location.")
            return None


class Emulator:
    """
    The Emulator component, responsible for taking actions decided by the
    StrategyEngine and performing them in the game environment.
    """

    def __init__(self, emulator_interface, vision_system):
        """
        Initializes the Emulator with an interface to interact with the actual emulator
        and a reference to the VisionSystem.

        Args:
            emulator_interface: An object that provides methods for interacting
                                with the game emulator (e.g., clicking, dragging, waiting).
                                This is now expected to be an instance of ADBEmulatorInterface.
            vision_system: An instance of the VisionSystem to query for game object locations.
        """
        self.emulator_interface = emulator_interface
        self.vision_system = vision_system
        # Link the vision system to the emulator interface if it supports it
        if hasattr(self.emulator_interface, 'set_vision_system'):
            self.emulator_interface.set_vision_system(self.vision_system)
        logging.info("Emulator initialized.")

    def perform_action(self, action: dict):
        """
        Takes an action dictionary from the StrategyEngine and performs the corresponding
        operation in the emulator.

        Args:
            action (dict): A dictionary specifying the action, e.g.,
                           {'action_type': 'play_card', 'card_name': 'knight', 'position': (250, 600)}
                           or {'action_type': 'wait', 'duration': 1}
        """
        action_type = action.get('action_type')

        if action_type == 'play_card':
            card_name = action.get('card_name')
            position = action.get('position')
            logging.info(f"Emulator: Attempting to play card '{card_name}' at position {position}")
            self.simulate_click_and_drag(card_name, position)

        elif action_type == 'wait':
            duration = action.get('duration', 1)
            logging.info(f"Emulator: Waiting for {duration} seconds.")
            self.emulator_interface.wait(duration)

        elif action_type == 'do_nothing':
            logging.info("Emulator: Performing no action.")
            # No operation needed for 'do_nothing'

        else:
            logging.warning(f"Emulator: Unknown action type received: {action_type}")

    def simulate_click_and_drag(self, card_name: str, position: tuple):
        """
        Simulates the process of clicking a card in the hand and dragging it to a position
        using the provided emulator interface (ADB swipe command).

        Args:
            card_name (str): The name of the card to simulate playing.
            position (tuple): The (x, y) coordinates where the card should be placed.
        """
        logging.info(f"Simulating click on '{card_name}' in hand and dragging to {position}")

        card_hand_location = self.emulator_interface.get_card_location(card_name)
        if card_hand_location:
            start_x, start_y = card_hand_location
            end_x, end_y = position

            # ADB swipe command takes start_x, start_y, end_x, end_y, and optional duration in ms
            # We'll use a duration of 500ms for the swipe
            swipe_duration_ms = 500
            self.emulator_interface._run_adb_command([
                "shell", "input", "swipe",
                str(int(start_x)), str(int(start_y)),
                str(int(end_x)), str(int(end_y)),
                str(swipe_duration_ms)
            ])
            logging.info(f"Successfully simulated playing '{card_name}' to {position} via ADB swipe.")
        else:
            logging.error(f"Could not find card '{card_name}' in hand to simulate drag. Action aborted.")
