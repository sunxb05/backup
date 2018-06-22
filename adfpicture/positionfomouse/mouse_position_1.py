#!/usr/bin/env python

"""Get the current mouse position."""

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def get_mouse_position():
    """
    Get the current position of the mouse.

    Returns
    -------
    dict :
        With keys 'x' and 'y'
    """
    mouse_position = None
    import sys
    if sys.platform in ['linux', 'linux2']:
        pass
    elif sys.platform == 'Windows':
        try:
            import win32api
        except ImportError:
            logging.info("win32api not installed")
            win32api = None
        if win32api is not None:
            x, y = win32api.GetCursorPos()
            mouse_position = {'x': x, 'y': y}
    elif sys.platform == 'Mac':
        pass
    else:
        try:
            import Tkinter  # Tkinter could be supported by all systems
        except ImportError:
            logging.info("Tkinter not installed")
            Tkinter = None
        if Tkinter is not None:
            p = Tkinter.Tk()
            x, y = p.winfo_pointerxy()
            mouse_position = {'x': x, 'y': y}
        print("sys.platform={platform} is unknown. Please report."
              .format(platform=sys.platform))
        print(sys.version)
    return mouse_position

print(get_mouse_position())
