"""
The main Strategy Engine, responsible for making all in-game decisions.
"""
import logging
import numpy as np


class StrategyEngine:
    """
    Analyzes the game state and decides the best action to take.
    """

    def __init__(self):
        """Initializes the strategy engine."""
        logging.info("Strategy Engine initialized.")
        # Define general defensive and offensive positions for fallback
        # These are tuned for a 720x1280 resolution, more central.
        self.general_defensive_position = (360, 900) # Centered horizontally, on our side (lower half)
        self.general_offensive_position = (360, 450) # Centered horizontally, at the bridge or opponent's side (upper half)

        # Define specific counter-placement zones (illustrative, needs tuning)
        # These are relative to the battlefield or specific lanes.
        # For simplicity, we'll use a few fixed points for now.
        # In a real game, these would be dynamic based on enemy unit positions.
        self.left_lane_defensive = (200, 900)
        self.right_lane_defensive = (520, 900)
        self.middle_defensive = (360, 800) # Slightly more forward than general defensive

        self.left_lane_offensive = (200, 450)
        self.right_lane_offensive = (520, 450)
        self.middle_offensive = (360, 500) # Slightly behind bridge for pushes


    def _assess_threat(self, game_info: dict) -> list:
        """
        Assesses immediate threats on the field.
        
        Args:
            game_info: The dictionary of game objects from the VisionSystem.
            
        Returns:
            list: A list of detected opponent units.
        """
        return game_info.get("opponent_units", [])

    def _get_card_properties(self, card_name: str) -> dict:
        """
        Placeholder: In a real system, this would fetch detailed properties
        (elixir cost, type, attack range, etc.) for a given card.
        For now, we return dummy properties.
        """
        # This would ideally come from a separate data file or database
        card_data = {
            "Knight": {"elixir_cost": 3, "type": "tank", "target": "ground"},
            "Archers": {"elixir_cost": 3, "type": "ranged", "target": "ground_air"},
            "Fireball": {"elixir_cost": 4, "type": "spell", "target": "area"},
            "Mini Pekka": {"elixir_cost": 4, "type": "damage", "target": "ground"},
            "Barbarians": {"elixir_cost": 5, "type": "swarm", "target": "ground"},
            "Giant": {"elixir_cost": 5, "type": "tank", "target": "buildings"},
            "Musketeer": {"elixir_cost": 4, "type": "ranged", "target": "ground_air"},
            "Spear Goblins": {"elixir_cost": 2, "type": "swarm", "target": "ground_air"},
            "Tombstone": {"elixir_cost": 3, "type": "building", "target": "spawner"},
            "Valkyrie": {"elixir_cost": 4, "type": "splash", "target": "ground"},
            "Wizard": {"elixir_cost": 5, "type": "splash_ranged", "target": "ground_air"},
            # Add more cards as you define them in your VisionSystem
        }
        return card_data.get(card_name, {"elixir_cost": 99, "type": "unknown", "target": "unknown"})


    def decide_action(self, game_info: dict):
        """
        Takes the current game info and returns the best action.
        This version implements smarter placement based on detected enemy units.

        Args:
            game_info (dict): A dictionary of all detected game objects from
                              the VisionSystem.

        Returns:
            A dictionary representing the chosen action (e.g.,
            {'action_type': 'play_card', 'card_name': 'knight',
             'position': (x, y)}), or None if no action is to be taken.
        """
        cards_in_hand = game_info.get("cards_in_hand", [])
        current_elixir = game_info.get("current_elixir", 0) # Assuming this is detected by VisionSystem
        opponent_units = self._assess_threat(game_info) # Get actual detected enemy units

        if not cards_in_hand:
            logging.info("No cards in hand. No action taken.")
            return None

        # Sort cards by elixir cost (cheapest first, for simple play logic)
        # In a real bot, you'd sort by strategic value.
        playable_cards = sorted([
            card for card in cards_in_hand 
            if self._get_card_properties(card.get("name")).get("elixir_cost", 99) <= current_elixir
        ], key=lambda c: self._get_card_properties(c.get("name")).get("elixir_cost", 99))

        if not playable_cards:
            logging.info(f"Not enough elixir ({current_elixir}) to play any available cards. No action taken.")
            return None

        card_to_play_info = playable_cards[0] # For now, still play the cheapest playable card
        card_name = card_to_play_info.get("name")
        card_properties = self._get_card_properties(card_name)
        
        placement_position = None

        if opponent_units:
            logging.info(f"Threat detected! Opponent units: {[u['name'] for u in opponent_units]}. Deciding defensive placement.")
            # Simple defensive logic: place unit near the first detected enemy unit
            # This is a very basic counter. More advanced logic would consider unit types, ranges, etc.
            first_enemy_unit = opponent_units[0]
            enemy_x, enemy_y = first_enemy_unit["position"]

            # Decide lane based on enemy X position (illustrative for 720 width)
            if enemy_x < 720 / 3: # Left third of the screen
                logging.info(f"Enemy in left lane. Considering left defensive placement for {card_name}.")
                placement_position = self.left_lane_defensive
            elif enemy_x > (720 / 3) * 2: # Right third of the screen
                logging.info(f"Enemy in right lane. Considering right defensive placement for {card_name}.")
                placement_position = self.right_lane_defensive
            else: # Middle lane
                logging.info(f"Enemy in middle lane. Considering middle defensive placement for {card_name}.")
                placement_position = self.middle_defensive
            
            # Further refinement: adjust Y position slightly based on enemy Y
            # E.g., place behind your tower if enemy is pushing tower.
            # For now, we stick to predefined defensive positions.

        else:
            logging.info("No immediate threat detected. Deciding offensive placement.")
            # Simple offensive logic: push a lane.
            # For now, always push middle offensively if no threat.
            placement_position = self.middle_offensive

            # More complex offensive logic could randomly choose a lane,
            # or choose based on opponent tower health, or cycle.
            # if np.random.rand() < 0.5:
            #     placement_position = self.left_lane_offensive
            # else:
            #     placement_position = self.right_lane_offensive


        if placement_position:
            action = {
                "action_type": "play_card",
                "card_name": card_name,
                "position": placement_position
            }
            logging.info(f"Strategy decided to play '{action['card_name']}' at {action['position']}.")
            return action
        else:
            logging.warning("Strategy failed to determine a placement position. No action taken.")
            return None

