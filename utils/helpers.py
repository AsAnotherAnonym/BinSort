
def rgb_to_cairo(color_rgb):
    """Convert RGB tuple (0-255) to Cairo format (0-1)"""
    return tuple(c / 255.0 for c in color_rgb)


def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))