import win32gui

# Делает активным окно, которое записывается в WINDOW_SUBSTRINGS

WINDOW_SUBSTRING = 'R2'

def get_window_info():
    # set window info
    window_info = {}
    win32gui.EnumWindows(set_window_coordinates, window_info)
    return window_info

# EnumWindows handler
# sets L2 window coordinates
def set_window_coordinates(hwnd, window_info):
    if win32gui.IsWindowVisible(hwnd):
        if WINDOW_SUBSTRING in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            window_info['x'] = x
            window_info['y'] = y
            window_info['width'] = w
            window_info['height'] = h
            window_info['name'] = win32gui.GetWindowText(hwnd)
            win32gui.SetForegroundWindow(hwnd)

#get_window_info()

