#!/usr/bin/env python3
"""
Interactive loop for the Haunted Data Center adventure.
"""

from game import Game

def main() -> None:
    game = Game()
    print("Welcome to the Haunted Data Center Adventure!")
    print("Type 'look' to see your surroundings. Type 'quit' to exit.\n")

    while True:
        cmd = input("> ")
        if cmd.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        output = game.process_command(cmd)
        print(output)

if __name__ == "__main__":
    main()

