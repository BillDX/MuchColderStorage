#!/usr/bin/env python3
"""
Haunted Data Center – core game engine
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

@dataclass
class Item:
    name: str
    description: str
    takeable: bool = True

@dataclass
class Exit:
    target: str
    locked: bool = False
    condition: Optional[Callable[['Game'], bool]] = None

@dataclass
class Room:
    name: str
    description: str
    exits: Dict[str, Exit] = field(default_factory=dict)
    items: List[Item] = field(default_factory=list)

    def describe(self) -> str:
        txt = f"You are in the {self.name}. {self.description}\n"
        if self.items:
            txt += "You see: " + ", ".join(item.name for item in self.items) + "."
        else:
            txt += "You see nothing of interest."
        return txt

class Game:
    def __init__(self) -> None:
        self.rooms: Dict[str, Room] = {}
        self._build_world()
        self.current_room: str = "Entrance Hall"
        self.inventory: List[Item] = []
        self._patch_cable_used: bool = False

    def _add_room(self, room: Room) -> None:
        self.rooms[room.name] = room

    def _build_world(self) -> None:
        keycard = Item("keycard",
                       "A shimmering keycard that looks like it could open a door.")
        password = Item("password",
                        "A note with the password scribbled: \"Open Sesame 2026!\"")
        patch_cable = Item("patch cable",
                           "A sturdy patch cable, might be useful for powering things.")

        entrance = Room(
            "Entrance Hall",
            "The dimly lit Entrance Hall of the Haunted Data Center. "
            "A flickering sign reads 'Welcome Back'."
        )
        hall = Room(
            "Hallway",
            "A long corridor lined with server racks. Dusty cables glimmer."
        )
        rack_row = Room(
            "Rack Row",
            "Rows of humming servers. One dusty server catches your eye."
        )
        rack_row.items.append(keycard)
        security = Room(
            "Security Office",
            "An office with a desk and a computer. A note with a password scribbled."
        )
        security.items.append(password)
        cooling = Room(
            "Cooling Tower",
            "A massive cooling unit. A patch cable sits on a stand."
        )
        cooling.items.append(patch_cable)
        vault = Room(
            "Data Storage Vault",
            "Rows of encrypted vaults. A terminal flickers in the corner."
        )
        exit_room = Room(
            "Exit",
            "You have escaped the Haunted Data Center! Congratulations!"
        )

        entrance.exits = {"north": Exit(target="Hallway")}

        hall.exits = {
            "south": Exit(target="Cooling Tower",
                          locked=True,
                          condition=lambda g: any(i.name == "password" for i in g.inventory)),
            "east": Exit(target="Rack Row"),
            "west": Exit(target="Security Office"),
            "north": Exit(target="Entrance Hall"),
        }

        rack_row.exits = {"west": Exit(target="Hallway")}

        security.exits = {"east": Exit(target="Hallway"),
                          "north": Exit(target="Vault")}

        cooling.exits = {
            "north": Exit(target="Exit",
                          locked=True,
                          condition=lambda g: any(i.name == "decryption key" for i in g.inventory)),
            "south": Exit(target="Hallway"),
        }

        vault.exits = {"west": Exit(target="Security Office")}

        exit_room.exits = {"south": Exit(target="Cooling Tower")}

        for r in [entrance, hall, rack_row, security, cooling, vault, exit_room]:
            self._add_room(r)

    def process_command(self, cmd: str) -> str:
        cmd = cmd.strip()
        if not cmd:
            return "I don't understand that."

        parts = cmd.split(maxsplit=1)
        verb = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if verb in ("go", "move"):
            return self._cmd_go(arg)
        elif verb == "take":
            return self._cmd_take(arg)
        elif verb == "inventory":
            return self._cmd_inventory()
        elif verb == "look":
            return self._cmd_look()
        elif verb == "use":
            return self._cmd_use(arg)
        elif verb in ("quit", "exit", "q"):
            return "Goodbye!"
        else:
            return "I don't understand that."

    def _cmd_go(self, direction: str) -> str:
        dir_map = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
            "north": "north",
            "south": "south",
            "east": "east",
            "west": "west",
        }
        dir_key = dir_map.get(direction.lower())
        if not dir_key:
            return "I don't know that direction."

        room = self.rooms[self.current_room]
        exit_obj = room.exits.get(dir_key)
        if not exit_obj:
            return f"You can't go {direction} from here."

        if exit_obj.locked:
            if exit_obj.condition and not exit_obj.condition(self):
                return f"The door to the {dir_key} is locked."
        self.current_room = exit_obj.target
        new_room = self.rooms[self.current_room]
        if self.current_room == "Exit":
            return ("You have escaped the Haunted Data Center! "
                    "Congratulations!")
        return f"You move {dir_key} to the {new_room.name}."

    def _cmd_take(self, item_name: str) -> str:
        room = self.rooms[self.current_room]
        for item in room.items:
            if item.name.lower() == item_name.lower() and item.takeable:
                self.inventory.append(item)
                room.items.remove(item)
                return f"You take the {item.name}."
        return f"There is no {item_name} here."

    def _cmd_inventory(self) -> str:
        if not self.inventory:
            return "You are carrying nothing."
        items = ", ".join(item.name for item in self.inventory)
        return f"You are carrying: {items}."

    def _cmd_look(self) -> str:
        room = self.rooms[self.current_room]
        return room.describe()

    def _cmd_use(self, item_name: str) -> str:
        """Handle item usage.

        The tests require a very specific response when the player attempts
        to use the patch cable in the wrong location or without having the
        item.  We therefore handle the patch cable first and then fall back
        to a generic inventory check for other items.
        """

        # Patch cable special handling.
        if item_name.lower() == "patch cable":
            if self.current_room != "Cooling Tower":
                return "You can't use the patch cable here."
            if not any(item.name.lower() == "patch cable" for item in self.inventory):
                return "You don't have a patch cable."
            if self._patch_cable_used:
                return "You have already used the patch cable."
            self._patch_cable_used = True
            decryption_key = Item("decryption key",
                                  "A shiny key that unlocks the Exit door.",
                                  takeable=False)
            self.inventory.append(decryption_key)
            return ("You plug the patch cable into the terminal. A hum fills the air. "
                    "The terminal lights up, reveal a decryption key.")

        # Generic inventory check for other items.
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                break
        else:
            return f"You don't have a {item_name}."
        # For any other item we currently have no special behavior.
        return f"You can't use the {item_name} here."

    def inventory_names(self) -> List[str]:
        return [item.name for item in self.inventory]

