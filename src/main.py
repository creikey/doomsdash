#!/usr/bin/env python

"""
Shows networktable data
"""

import pygame
import pynk
import pynk.nkpygame
import coloredlogs
import logging
from inputbox import InputBox
from networktables import NetworkTables

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

WIDTH = 1024
HEIGHT = 768
FONT_NAME = "Arial"
FONT_SIZE = 36
WIN_CAPTION = "Doomsdash"
SERVER_URL = "127.0.0.1"
conn_status = b"NOT CONNECTED"
conn_color = pynk.lib.nk_rgb(255, 0, 0)

tb = NetworkTables.initialize(server=SERVER_URL)
#NetworkTables.enableVerboseLogging()
d_width = WIDTH
d_height = HEIGHT
data_box = InputBox(128)


def make_screen():
    return pygame.display.set_mode((d_width, d_height), pygame.RESIZABLE)


def connectionListener(connected, info):
    logging.info(str(info) + ": Connected={}".format(connected))
    if connected:
        global conn_status
        global conn_color
        conn_status = b"CONNECTED"
        conn_color = pynk.lib.nk_rgb(0, 255, 0)

def drawValues(ctx, inValues):
    for k in inValues.keys():
        pynk.lib.nk_layout_row_dynamic(ctx, 0, 2)
        pynk.lib.nk_label(ctx, k.encode('utf-8'), pynk.lib.NK_TEXT_LEFT)
        pynk.lib.nk_label(ctx, str(inValues[k]).encode('utf-8'), pynk.lib.NK_TEXT_RIGHT)

values = {}

def entryListener(key, value, isNew): # isNew is if new entry
    values[key] = value

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
NetworkTables.addEntryListener(entryListener)

if __name__ == '__main__':

    # Initialise pygame.
    pygame.init()
    screen = make_screen()
    pygame.display.set_caption(WIN_CAPTION)

    running = True
    # Initialise nuklear
    font = pynk.nkpygame.NkPygameFont(
        pygame.font.SysFont(FONT_NAME, FONT_SIZE))
    with pynk.nkpygame.NkPygame(font) as nkpy:
        text_color = pynk.lib.nk_rgb(
            nkpy.ctx.style.text.color.r, nkpy.ctx.style.text.color.g, nkpy.ctx.style.text.color.b)
        while running:
            # Handle input.
            events = []
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.VIDEORESIZE:
                    d_width = e.w
                    d_height = e.h
                    screen = make_screen()
                else:
                    events.append(e)
            nkpy.handle_events(events)

            # Show the demo GUI.
            if pynk.lib.nk_begin(nkpy.ctx, WIN_CAPTION.encode('utf-8'), pynk.lib.nk_rect(0, 0, d_width, d_height), 0):
                pynk.lib.nk_layout_row_dynamic(nkpy.ctx, 0, 2)
                pynk.lib.nk_label(
                    nkpy.ctx, b"Connection Status", pynk.lib.NK_TEXT_LEFT)
                nkpy.ctx.style.text.color = conn_color
                pynk.lib.nk_label(nkpy.ctx, conn_status,
                                  pynk.lib.NK_TEXT_RIGHT)
                nkpy.ctx.style.text.color = text_color

                pynk.lib.nk_layout_row_dynamic(nkpy.ctx, 0, 2)
                data_box.show(nkpy)

                drawValues(nkpy.ctx, values)
            pynk.lib.nk_end(nkpy.ctx)

            # Draw
            screen.fill((0, 0, 0))
            nkpy.render_to_surface(screen)
            pygame.display.update()

            # Clear the context for the next pass.
            pynk.lib.nk_clear(nkpy.ctx)

    # Shutdown.
    pygame.quit()
