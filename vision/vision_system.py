"""
The main Vision System, responsible for orchestrating all detectors
and interpreting the game screen.
"""
import logging
import numpy as np
import cv2 # Import OpenCV for image processing
from PIL import Image # For handling image data, e.g., from pyautogui screenshots
import os # For path manipulation and file listing
import time # Import the time module for timestamps

from core.game_states import GameState

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class VisionSystem:
    """
    Manages all detection-related tasks.
    """

    def __init__(self):
        """Initializes the vision system and its detectors."""
        logging.info("Vision System initialized (real image processing framework).")
        
        # Store the latest captured screenshot for detection methods
        self.latest_screenshot = None 

        # Dictionaries to store pre-loaded templates for template matching
        self.card_templates = {}
        self.ui_templates = {} # For UI elements like buttons
        self.enemy_unit_templates = {} # NEW: For enemy unit templates

        # Load templates at initialization
        self._load_templates()
        
        # Counter for simulated data (will be replaced by real detection over time)
        self._battle_analysis_counter = 0

        # Define the Region of Interest (ROI) for the player's hand (720x1280)
        self.hand_roi = (50, 1050, 670, 1230) # (left, top, right, bottom)

        # Define the Region of Interest (ROI) for the main battlefield (720x1280)
        # This area covers where units typically move and engage.
        # Tune these coordinates based on your game's actual battlefield area.
        self.battlefield_roi = (0, 150, 720, 1000) # (left, top, right, bottom)
                                                  # Example: from top of screen (0) down to just above hand (1000)
                                                  # and full width (0 to 720)

        # NEW: Define the Region of Interest (ROI) for the enemy's side of the battlefield (720x1280)
        # This is typically the upper half of the battlefield.
        # Assuming battlefield_roi starts at y=150 and ends at y=1000 (height 850 pixels)
        # The enemy's side would be roughly from y=150 to y=575 (mid-point of battlefield_roi + a bit)
        self.enemy_field_roi = (self.battlefield_roi[0], self.battlefield_roi[1], 
                                self.battlefield_roi[2], self.battlefield_roi[1] + (self.battlefield_roi[3] - self.battlefield_roi[1]) // 2 + 50) 
                                # (left, top, right, middle_y_plus_offset)
                                # Adjusted to take the upper half of battlefield_roi plus 50 pixels down for overlap.
                                # This would be approx (0, 150, 720, 575) if battlefield_roi is (0,150,720,1000)

        # Debugging flag and output directory for visualizations
        self.debug_visualizations = True # Set to False to disable saving images
        self.debug_output_dir = "debug_vision_output"
        if self.debug_visualizations and not os.path.exists(self.debug_output_dir):
            os.makedirs(self.debug_output_dir)
            logging.info(f"Created debug output directory: {self.debug_output_dir}")


    def _load_templates(self):
        """
        Loads all image templates (cards, UI elements, and enemy units) from their respective directories.
        Assumes templates are organized under D:/bot_v2/vision/templates/
        """
        # Determine the path to the 'vision' directory
        vision_dir = os.path.dirname(os.path.abspath(__file__)) # D:/bot_v2/vision
        templates_base_dir = os.path.join(vision_dir, "templates")

        self._load_card_templates(os.path.join(templates_base_dir, "cards"))
        self._load_ui_templates(os.path.join(templates_base_dir, "ui_elements"))
        self._load_enemy_unit_templates(os.path.join(templates_base_dir, "enemy_units")) # NEW


    def _load_card_templates(self, cards_dir: str):
        """
        Loads card images from the specified directory and stores them as grayscale templates.
        """
        if not os.path.isdir(cards_dir):
            logging.error(f"Card templates directory not found: {cards_dir}. Please create it and add card images.")
            return

        logging.info(f"Loading card templates from: {cards_dir}")
        for filename in os.listdir(cards_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Convert filename to a standardized card name (e.g., "knight.jpg" -> "Knight")
                card_name = os.path.splitext(filename)[0].replace('_', ' ').title() 
                filepath = os.path.join(cards_dir, filename)
                
                # Load image in grayscale
                template = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                
                if template is not None:
                    self.card_templates[card_name] = template
                    logging.debug(f"Loaded template for '{card_name}' from {filename}")
                else:
                    logging.warning(f"Could not load image file: {filename}")
        logging.info(f"Finished loading {len(self.card_templates)} card templates.")

    def _load_ui_templates(self, ui_elements_dir: str):
        """
        Loads UI element images from the specified directory and stores them as grayscale templates.
        It expects specific filenames for key UI elements.
        """
        # Define the expected UI elements and their corresponding filenames (case-insensitive, no spaces for files)
        expected_ui_elements = {
            "Play Button": "play_button.png",
            "Battle Indicator": "battle_indicator.png", # A unique element present only during battle
            "OK Button": "ok_button.png",               # Common button after a match
            "Home Button": "home_button.png",           # Button to return to main menu
            "Settings Icon": "settings_icon.png",       # Example of another common UI element
            # Add more UI elements as needed for your game
        }

        if not os.path.isdir(ui_elements_dir):
            logging.warning(f"UI elements directory not found: {ui_elements_dir}. UI state detection will be severely limited.")
            return

        logging.info(f"Loading UI element templates from: {ui_elements_dir}")
        loaded_count = 0
        for ui_element_name, filename in expected_ui_elements.items():
            filepath = os.path.join(ui_elements_dir, filename)
            
            if os.path.exists(filepath):
                template = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE) 
                
                if template is not None:
                    self.ui_templates[ui_element_name] = template
                    logging.debug(f"Loaded template for '{ui_element_name}' from {filename}")
                    loaded_count += 1
                else:
                    logging.warning(f"Could not load image file: {filename} (check file corruption).")
            else:
                logging.warning(f"Expected UI template '{filename}' for '{ui_element_name}' not found at {filepath}.")

        logging.info(f"Finished loading {loaded_count} UI element templates out of {len(expected_ui_elements)} expected.")
        if loaded_count < len(expected_ui_elements):
            logging.warning("Some expected UI templates were not loaded. Game state detection might be less accurate.")

    def _load_enemy_unit_templates(self, enemy_units_dir: str): # NEW METHOD
        """
        Loads enemy unit images from the specified directory and stores them as grayscale templates.
        """
        if not os.path.isdir(enemy_units_dir):
            logging.warning(f"Enemy unit templates directory not found: {enemy_units_dir}. Enemy unit detection will be limited.")
            return

        logging.info(f"Loading enemy unit templates from: {enemy_units_dir}")
        loaded_count = 0
        for filename in os.listdir(enemy_units_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                unit_name = os.path.splitext(filename)[0].replace('_', ' ').title() 
                filepath = os.path.join(enemy_units_dir, filename)
                
                template = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                
                if template is not None:
                    self.enemy_unit_templates[unit_name] = template
                    logging.debug(f"Loaded template for '{unit_name}' from {filename}")
                    loaded_count += 1
                else:
                    logging.warning(f"Could not load enemy unit image file: {filename}")
        logging.info(f"Finished loading {loaded_count} enemy unit templates.")
        if loaded_count == 0:
            logging.warning("No enemy unit templates loaded. Opponent unit detection will be simulated.")


    def _preprocess_image(self, image_np: np.ndarray) -> np.ndarray:
        """
        Performs basic preprocessing on the image (e.g., grayscale, blur).
        
        Args:
            image_np: The current screen image as a NumPy array (BGR format).
            
        Returns:
            np.ndarray: The preprocessed image.
        """
        # Convert to grayscale
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        # Apply a Gaussian blur to reduce noise (optional, but often helpful)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        logging.debug("Image preprocessed: converted to grayscale and blurred.")
        return blurred_image

    def _find_template(self, screen_image_gray: np.ndarray, template: np.ndarray, threshold: float = 0.8) -> tuple | None:
        """
        Performs template matching to find a template in the screen image.
        
        Args:
            screen_image_gray: The grayscale screen image.
            template: The grayscale template to find.
            threshold: The confidence threshold for a positive match.
            
        Returns:
            tuple: (x, y) coordinates of the card's center, or None if not found.
        """
        if template is None or screen_image_gray is None:
            logging.debug("Template or screen image is None for _find_template.")
            return None
        
        # Ensure template is smaller than the search image
        if template.shape[0] > screen_image_gray.shape[0] or \
           template.shape[1] > screen_image_gray.shape[1]:
            logging.warning("Template is larger than screen image. Cannot perform template matching.")
            return None

        res = cv2.matchTemplate(screen_image_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            template_width, template_height = template.shape[::-1]
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            return (center_x, center_y)
        return None


    def get_current_game_state(self, image_np: np.ndarray) -> GameState:
        """
        Analyzes the screen to determine the overall game state using template matching.
        
        Args:
            image_np: The current screen image as a NumPy array (BGR format).
            
        Returns:
            GameState: The detected game state (e.g., ON_MENU, IN_BATTLE).
        """
        self.latest_screenshot = image_np # Store the latest screenshot
        processed_screen = self._preprocess_image(image_np)

        # Try to detect UI elements to determine the state
        # Order matters here: check for specific states first.
        
        # Check for IN_BATTLE state (e.g., by detecting an in-game HUD element)
        battle_indicator_template = self.ui_templates.get("Battle Indicator")
        if battle_indicator_template is not None:
            battle_indicator_pos = self._find_template(processed_screen, battle_indicator_template, threshold=0.7)
            if battle_indicator_pos:
                logging.info(f"VisionSystem: Detected 'Battle Indicator' at {battle_indicator_pos}. State: IN_BATTLE.")
                return GameState.IN_BATTLE

        # Check for ON_MENU state (e.g., by detecting a "Play" button)
        play_button_template = self.ui_templates.get("Play Button")
        if play_button_template is not None:
            play_button_pos = self._find_template(processed_screen, play_button_template, threshold=0.7)
            if play_button_pos:
                logging.info(f"VisionSystem: Detected 'Play Button' at {play_button_pos}. State: ON_MENU.")
                return GameState.ON_MENU

        # Check for POST_GAME state (e.g., by detecting an "OK" or "Home" button after a match)
        ok_button_template = self.ui_templates.get("OK Button")
        if ok_button_template is not None:
            ok_button_pos = self._find_template(processed_screen, ok_button_template, threshold=0.7)
            if ok_button_pos:
                logging.info(f"VisionSystem: Detected 'OK Button' at {ok_button_pos}. State: POST_GAME.")
                return GameState.POST_GAME
        
        home_button_template = self.ui_templates.get("Home Button")
        if home_button_template is not None:
            home_button_pos = self._find_template(processed_screen, home_button_template, threshold=0.7)
            if home_button_pos:
                logging.info(f"VisionSystem: Detected 'Home Button' at {home_button_pos}. State: ON_MENU (returning from post-game).")
                return GameState.ON_MENU # Assuming Home Button leads to menu

        # Fallback if no specific UI element is confidently detected
        logging.warning("VisionSystem: Could not confidently determine game state based on UI templates. Defaulting to IN_BATTLE for simulation.")
        return GameState.IN_BATTLE


    def analyze_battlefield(self, image_np: np.ndarray) -> dict:
        """
        Performs a detailed analysis of the battlefield, detecting units,
        cards, elixir, etc.
        
        Args:
            image_np: The current screen image as a NumPy array.
            
        Returns:
            A dictionary containing all detected game objects.
        """
        self.latest_screenshot = image_np # Store the latest screenshot
        processed_image = self._preprocess_image(image_np)

        detected_cards_in_hand = []
        # Define the ROI for the hand (y_start:y_end, x_start:x_end)
        # Ensure these coordinates are valid for your screenshot resolution
        hand_x_start, hand_y_start, hand_x_end, hand_y_end = self.hand_roi 
        
        # Crop the processed image to the hand ROI
        # Ensure slicing is safe, handle cases where ROI might be out of bounds
        roi_image_hand = processed_image[max(0, hand_y_start):min(processed_image.shape[0], hand_y_end), 
                                         max(0, hand_x_start):min(processed_image.shape[1], hand_x_end)]

        # --- Debug Visualization for Hand ROI ---
        debug_hand_image = image_np.copy() # Use original image for visualization
        cv2.rectangle(debug_hand_image, (hand_x_start, hand_y_start), (hand_x_end, hand_y_end), (0, 255, 255), 2) # Yellow rectangle for ROI


        if roi_image_hand.size == 0: # Check if ROI is empty due to invalid coordinates
            logging.warning("Hand ROI is empty or invalid. Cannot detect cards in hand.")
        else:
            # Iterate through all loaded card templates
            for card_name, template in self.card_templates.items():
                # Try to find the card template within the hand ROI
                # Adjust threshold as needed for card detection
                found_pos_in_roi = self._find_template(roi_image_hand, template, threshold=0.85) # Higher threshold for cards
                
                if found_pos_in_roi:
                    # Convert coordinates from ROI-relative to full-screen-relative
                    full_screen_x = found_pos_in_roi[0] + hand_x_start
                    full_screen_y = found_pos_in_roi[1] + hand_y_start
                    
                    # Add detected card to the list
                    detected_cards_in_hand.append({
                        "name": card_name,
                        "position": (full_screen_x, full_screen_y),
                        "elixir_cost": 3, # Placeholder
                        "type": "unit" # Placeholder
                    })
                    # Removed redundant logging here, will log the full list later
                    # logging.info(f"VisionSystem: Detected card '{card_name}' in hand at ({full_screen_x}, {full_screen_y}).")

                    # Draw rectangle on debug image for detected card
                    template_height, template_width = template.shape
                    top_left = (full_screen_x - template_width // 2, full_screen_y - template_height // 2)
                    bottom_right = (full_screen_x + template_width // 2, full_screen_y + template_height // 2)
                    cv2.rectangle(debug_hand_image, top_left, bottom_right, (0, 255, 0), 2) # Green rectangle
                    cv2.putText(debug_hand_image, card_name, (top_left[0], top_left[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Save the debug image of the hand ROI
        if self.debug_visualizations:
            timestamp = int(time.time() * 1000)
            debug_path = os.path.join(self.debug_output_dir, f"hand_roi_debug_{timestamp}.png")
            cv2.imwrite(debug_path, debug_hand_image)
            logging.info(f"Saved hand ROI debug image to: {debug_path}")


        # NEW: Detect player and opponent units on the battlefield
        detected_opponent_units = []
        
        # Use the more specific enemy_field_roi for detecting opponent units
        enemy_field_x_start, enemy_field_y_start, enemy_field_x_end, enemy_field_y_end = self.enemy_field_roi
        
        # Crop the processed image to the enemy field ROI
        roi_image_enemy_field = processed_image[max(0, enemy_field_y_start):min(processed_image.shape[0], enemy_field_y_end), 
                                                max(0, enemy_field_x_start):min(processed_image.shape[1], enemy_field_x_end)]

        # --- Debug Visualization for Enemy Field ROI ---
        debug_enemy_field_image = image_np.copy() # Use original image for visualization
        cv2.rectangle(debug_enemy_field_image, (enemy_field_x_start, enemy_field_y_start), 
                      (enemy_field_x_end, enemy_field_y_end), (255, 165, 0), 2) # Orange rectangle for Enemy Field ROI


        if roi_image_enemy_field.size == 0:
            logging.warning("Enemy field ROI is empty or invalid. Cannot detect units.")
        else:
            for unit_name, template in self.enemy_unit_templates.items():
                # For multiple instances of the same unit, you might need multi-scale template matching
                # or find all matches above a certain threshold. For simplicity, we find the first one.
                found_pos_in_roi = self._find_template(roi_image_enemy_field, template, threshold=0.85) # Lower threshold for units
                
                if found_pos_in_roi:
                    full_screen_x = found_pos_in_roi[0] + enemy_field_x_start
                    full_screen_y = found_pos_in_roi[1] + enemy_field_y_start
                    
                    detected_opponent_units.append({
                        "name": unit_name,
                        "position": (full_screen_x, full_screen_y),
                        "health": 100, # Placeholder
                        "type": "unit" # Placeholder
                    })
                    logging.info(f"VisionSystem: Detected enemy unit '{unit_name}' at ({full_screen_x}, {full_screen_y}).")

                    # Draw rectangle on debug image for detected unit
                    template_height, template_width = template.shape
                    top_left = (full_screen_x - template_width // 2, full_screen_y - template_height // 2)
                    bottom_right = (full_screen_x + template_width // 2, full_screen_y + template_height // 2)
                    cv2.rectangle(debug_enemy_field_image, top_left, bottom_right, (0, 0, 255), 2) # Red rectangle
                    cv2.putText(debug_enemy_field_image, unit_name, (top_left[0], top_left[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        # Save the debug image of the enemy field ROI
        if self.debug_visualizations:
            timestamp = int(time.time() * 1000)
            debug_path = os.path.join(self.debug_output_dir, f"enemy_field_roi_debug_{timestamp}.png")
            cv2.imwrite(debug_path, debug_enemy_field_image)
            logging.info(f"Saved enemy field ROI debug image to: {debug_path}")

        # --- Other Real Detection Concepts (to be implemented here) ---
        # 3. Read elixir: This would involve OCR (Optical Character Recognition)
        #    on the elixir bar region, or template matching for elixir drops.
        # 4. Read tower healths: Similar to elixir, often requires OCR or number detection.
        # 5. Read game time: Also requires OCR.

        # For now, we'll provide simulated data for other game_info elements,
        # but the framework for real image processing is in place.
        
        game_info = {
            "player_units": [], # Will be populated by real detection (future)
            "opponent_units": detected_opponent_units, # Now populated by real detection
            "cards_in_hand": detected_cards_in_hand, # Now populated by real detection
            "current_elixir": 10.0, # Will be read by OCR/detection (future)
            "player_tower_health": {"king": 3000, "left": 2000, "right": 2000}, # Will be read by OCR/detection (future)
            "opponent_tower_health": {"king": 3000, "left": 2000, "right": 2000}, # Will be read by OCR/detection (future)
            "game_time_seconds": 60 # Will be read by OCR/detection (future)
        }
        logging.info("Vision System: Battlefield analysis complete (partially real, partially simulated).")
        # Log the detected cards in hand for debugging purposes
        logging.info(f"Vision System: Cards in hand for StrategyEngine: {[card['name'] for card in detected_cards_in_hand]}")
        return game_info

    def get_card_coordinates(self, card_name: str) -> tuple | None:
        """
        Returns the screen coordinates (x, y) of a specific card in the hand
        by performing template matching on the latest screenshot.

        Args:
            card_name (str): The name of the card to find (e.g., "Knight", "Fireball").

        Returns:
            tuple: (x, y) coordinates of the card's center, or None if not found.
        """
        if self.latest_screenshot is None:
            logging.error("VisionSystem: No screenshot available for card detection.")
            return None

        template_key = card_name.replace('_', ' ').title()
        card_template = self.card_templates.get(template_key)

        if card_template is None:
            logging.warning(f"VisionSystem: Template for card '{card_name}' not loaded or found.")
            return None

        screen_gray = self._preprocess_image(self.latest_screenshot)

        # Perform template matching using the helper function
        # This will search the entire screen. For cards in hand, analyze_battlefield's
        # detection within ROI is more appropriate.
        # This method is primarily used by the Emulator.
        found_location = self._find_template(screen_gray, card_template, threshold=0.8)

        if found_location:
            logging.info(f"VisionSystem: Found '{card_name}' at {found_location} with confidence (threshold 0.8).")
            return found_location
        else:
            logging.info(f"VisionSystem: Card '{card_name}' not found on screen (below threshold 0.8).")
            return None
