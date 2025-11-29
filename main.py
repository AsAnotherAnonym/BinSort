from core.game_manager import GameManager

""" 
List of all libraries used, semua library yang dipakai
"""
import pygame
import cairo
import math
import random
import array
import struct
import json
import os
import sys
from enum import Enum, auto

def main():
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()