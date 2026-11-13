# The start file of the web version.
# pygbag (the tool that turns the game into a website) always starts a file
# called main.py, so this file only starts the 2D game.
# asyncio.run starts main() from game_2d.py, which is an "async" function:
# that lets the browser draw the page between two frames of the game.
# (pygbag looks for exactly the line asyncio.run(main()), so main is
# imported by its own name.)

import asyncio
# pygbag only looks at the imports in this file to decide which packages
# the browser must load, so pygame is imported here too.
import pygame
from game_2d import main

asyncio.run(main())
