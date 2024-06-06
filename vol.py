from sys import platform
import pynput

VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE

keyboard = pynput.keyboard.Controller()

def send_key(vk):
    if vk == VK_MEDIA_PLAY_PAUSE:
        keyboard.press(pynput.keyboard.Key.media_play_pause)
        keyboard.release(pynput.keyboard.Key.media_play_pause)

    if vk == VK_MEDIA_NEXT_TRACK:
        keyboard.press(pynput.keyboard.Key.media_next)
        keyboard.release(pynput.keyboard.Key.media_next)

    if vk == VK_MEDIA_NEXT_TRACK:
        keyboard.press(pynput.keyboard.Key.media_previous)
        keyboard.release(pynput.keyboard.Key.media_previous)

    if vk == VK_VOLUME_UP:
        keyboard.press(pynput.keyboard.Key.media_volume_up)
        keyboard.release(pynput.keyboard.Key.media_volume_up)

    if vk == VK_VOLUME_DOWN:
        keyboard.press(pynput.keyboard.Key.media_volume_down)
        keyboard.release(pynput.keyboard.Key.media_volume_down)