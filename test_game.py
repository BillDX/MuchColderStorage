#!/usr/bin/env python3
"""
Red/green style tests for the Haunted Data Center game.
"""

import unittest
from game import Game

class TestHauntedDataCenter(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initial_room(self):
        self.assertEqual(self.game.current_room, "Entrance Hall")

    def test_look_description(self):
        out = self.game.process_command("look")
        self.assertIn("Entrance Hall", out)
        self.assertIn("dimly lit", out)

    def test_go_north(self):
        out = self.game.process_command("go north")
        self.assertIn("Hallway", out)
        self.assertEqual(self.game.current_room, "Hallway")

    def test_go_south_locked_before_password(self):
        self.game.process_command("go north")   # to Hallway
        out = self.game.process_command("go south")
        self.assertIn("locked", out)
        self.assertEqual(self.game.current_room, "Hallway")

    def test_take_keycard(self):
        self.game.process_command("go north")   # Hallway
        self.game.process_command("go east")    # Rack Row
        out = self.game.process_command("take keycard")
        self.assertIn("take the keycard", out.lower())
        self.assertIn("keycard", [i.name for i in self.game.inventory])

    def test_inventory_list(self):
        self.game.process_command("go north")
        self.game.process_command("go east")
        self.game.process_command("take keycard")
        out = self.game.process_command("inventory")
        self.assertIn("keycard", out.lower())

    def test_take_password(self):
        self.game.process_command("go north")   # Hallway
        self.game.process_command("go west")    # Security Office
        out = self.game.process_command("take password")
        self.assertIn("take the password", out.lower())
        self.assertIn("password", [i.name for i in self.game.inventory])

    def test_use_patch_cable_before_cooling(self):
        # Ensure patch cable can't be used outside Cooling Tower
        self.game.process_command("go north")
        self.game.process_command("go east")
        self.game.process_command("take keycard")
        self.game.process_command("go west")
        self.game.process_command("go west")
        self.game.process_command("take password")
        self.game.process_command("go east")
        out = self.game.process_command("use patch cable")
        self.assertIn("can't use the patch cable here", out.lower())

    def test_patch_cable_use(self):
        # Full path to patch cable
        self.game.process_command("go north")   # Hallway
        self.game.process_command("go east")    # Rack Row
        self.game.process_command("take keycard")
        self.game.process_command("go west")    # Hallway
        self.game.process_command("go west")    # Security Office
        self.game.process_command("take password")
        self.game.process_command("go east")    # Hallway
        self.game.process_command("go south")   # Cooling Tower
        self.game.process_command("take patch cable")
        out = self.game.process_command("use patch cable")
        self.assertIn("reveal a decryption key", out.lower())
        self.assertIn("decryption key", [i.name for i in self.game.inventory])

    def test_unlock_exit_and_escape(self):
        # Go through all puzzles and escape
        self.game.process_command("go north")
        self.game.process_command("go east")
        self.game.process_command("take keycard")
        self.game.process_command("go west")
        self.game.process_command("go west")
        self.game.process_command("take password")
        self.game.process_command("go east")
        self.game.process_command("go south")
        self.game.process_command("take patch cable")
        self.game.process_command("use patch cable")
        # Attempt to exit (north from Cooling Tower)
        out = self.game.process_command("go north")
        self.assertIn("escaped", out.lower())
        self.assertEqual(self.game.current_room, "Exit")

    def test_full_playthrough(self):
        """Integration test that plays the entire game to victory."""
        commands = [
            "look",
            "go north",
            "go east",
            "take keycard",
            "go west",
            "go west",
            "take password",
            "go east",
            "go south",
            "take patch cable",
            "use patch cable",
            "go north",
            "look"
        ]
        for cmd in commands:
            out = self.game.process_command(cmd)
            # Just ensure we don't get errors
            self.assertNotIn("I don't understand", out)
        final_desc = self.game.process_command("look")
        # The final look will be the exit message, so just check that we’re in the exit
        self.assertIn("escaped", final_desc.lower() if "escaped" in final_desc.lower() else "")

if __name__ == "__main__":
    unittest.main()

