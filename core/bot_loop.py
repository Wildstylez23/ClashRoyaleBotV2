"""
The main bot loop, which acts as a state machine to handle different
phases of the game.
"""
import logging
import time
import numpy as np

from core.game_states import GameState
from vision.vision_system import VisionSystem
from strategy.strategy_engine import StrategyEngine
from emulator.emulator import Emulator, ADBEmulatorInterface # Corrected: Changed PyAutoGUIEmulatorInterface to ADBEmulatorInterface

# Configure logging for better visibility of actions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BotLoop:
    """
    The core state machine for the bot.
    """

    def __init__(self):
        """Initializes the main bot loop and its components."""
        self.current_state = GameState.INITIALIZING
        self.running = False

        # Initialize the VisionSystem
        self.vision = VisionSystem()

        # Initialize ADBEmulatorInterface
        # You can specify adb_path and device_id here if needed, e.g.:
        # self.emulator_interface = ADBEmulatorInterface(adb_path="C:\\adb\\adb.exe", device_id="emulator-5554")
        self.emulator_interface = ADBEmulatorInterface() # Uses default "adb" path and auto-detects device

        # Initialize the Emulator with the ADB interface and VisionSystem
        self.emulator = Emulator(emulator_interface=self.emulator_interface, vision_system=self.vision)

        # Initialize the StrategyEngine
        self.strategy = StrategyEngine()

        logging.info("New bot framework initialized.")

    def start(self):
        """Starts the main bot loop."""
        self.running = True
        logging.info("Bot loop started.")
        self.run()

    def stop(self):
        """Stops the main bot loop."""
        self.running = False
        logging.info("Bot loop stopped.")

    def run(self):
        """
        The main state machine loop. It continuously checks the game state
        and calls the appropriate handler.
        """
        while self.running:
            # Get a screenshot from the emulator interface and pass it to the vision system.
            screen_image = self.emulator_interface.get_screen()
            self.current_state = self.vision.get_current_game_state(screen_image)

            if self.current_state == GameState.INITIALIZING:
                self._handle_initializing_state()
            elif self.current_state == GameState.ON_MENU:
                self._handle_menu_state()
            elif self.current_state == GameState.IN_BATTLE:
                self._handle_battle_state()
            elif self.current_state == GameState.POST_GAME:
                self._handle_post_game_state()
            elif self.current_state == GameState.STOPPED:
                self.running = False

            time.sleep(1) # Main loop delay

    def _handle_initializing_state(self):
        """Handles the bot's startup logic."""
        logging.info("Bot is initializing... looking for game screen.")
        # We'll transition directly to the menu for simulation.
        # In a real scenario, VisionSystem would detect the actual state.
        # For now, we rely on VisionSystem's internal state counter.
        pass # VisionSystem.get_current_game_state will handle the transition

    def _handle_menu_state(self):
        """Handles logic for when the bot is on the main menu."""
        logging.info("On main menu. Attempting to start a battle.")
        # In a real scenario, you'd click a "Battle" or "Play" button here.
        # Example: self.emulator.click(x_coord_of_battle_button, y_coord_of_battle_button)
        # For simulation, we rely on VisionSystem's internal state counter to transition.
        pass # VisionSystem.get_current_game_state will handle the transition

    def _handle_battle_state(self):
        """Handles the core in-battle logic."""
        logging.info("In battle. Analyzing game state...")

        # Use the vision system to analyze the battlefield.
        # The screen_image is already captured in the run loop.
        game_info = self.vision.analyze_battlefield(self.emulator_interface.get_screen())

        # Use strategy engine to decide action
        action = self.strategy.decide_action(game_info)

        # Perform action using emulator if an action was decided
        if action:
            self.emulator.perform_action(action)
        else:
            logging.info("Strategy decided no action for this turn.")

        # Simulate the end of a battle
        if np.random.rand() < 0.1: # 10% chance to end battle
            self.current_state = GameState.POST_GAME

    def _handle_post_game_state(self):
        """Handles logic for the post-game screen."""
        logging.info("Post-game screen detected. Returning to menu.")
        # In a real scenario, you'd click an "OK" or "Return to Menu" button here.
        # Example: self.emulator.click(x_coord_of_ok_button, y_coord_of_ok_button)
        # For simulation, we directly transition to ON_MENU
        self.current_state = GameState.ON_MENU
