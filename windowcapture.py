import numpy as np
import win32con
import win32gui
import win32ui


class WindowCapture:
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name=None):
        """
        Initializes the screenshot object.

        Args:
            window_name (str): The name of the window to capture the screenshot from. If None, the screenshot will be taken from the entire desktop.

        Raises:
            Exception: If the specified window cannot be found.

        Returns:
            None
        """
        self.screenshot = None

        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        border_pixels = 0
        titlebar_pixels = 0
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        """
        Get a screenshot of the window.

        Returns:
            numpy.ndarray: The screenshot image as a NumPy array.
        """
        # get the window image data
        w_dc = win32gui.GetWindowDC(self.hwnd)
        dc_obj = win32ui.CreateDCFromHandle(w_dc)
        c_dc = dc_obj.CreateCompatibleDC()
        data_bit_map = win32ui.CreateBitmap()
        data_bit_map.CreateCompatibleBitmap(dc_obj, self.w, self.h)
        c_dc.SelectObject(data_bit_map)
        c_dc.BitBlt((0, 0), (self.w, self.h), dc_obj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        byte_array = data_bit_map.GetBitmapBits(True)
        img = np.frombuffer(byte_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dc_obj.DeleteDC()
        c_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, w_dc)
        win32gui.DeleteObject(data_bit_map.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img

    @staticmethod
    def list_window_names():
        """
        An enumeration handler for Windows.

        Args:
            hwnd (int): The handle of the window.
            ctx: The context.

        Returns:
            None
        """
        def win_enum_handler(hwnd, ctx):
            """
            A function that handles the enumeration of windows.

            Args:
                hwnd (int): The handle to the window being enumerated.
                ctx (object): The context object passed to the enumeration function.

            Returns:
                None
            """
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(win_enum_handler, None)

    def get_screen_position(self, pos):
        """
        Calculates the screen position of a given point.

        Args:
            pos (tuple): The coordinates of the point in the original coordinate system.

        Returns:
            tuple: The screen position of the point, adjusted by the offset.
        """
        return pos[0] + self.offset_x, pos[1] + self.offset_y
