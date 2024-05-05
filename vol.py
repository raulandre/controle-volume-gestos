import win32api

VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE

def send_key(vk):
    hwcode = win32api.MapVirtualKey(vk, 0)
    win32api.keybd_event(vk, hwcode)