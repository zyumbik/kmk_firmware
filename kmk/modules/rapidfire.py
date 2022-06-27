from random import randint

from kmk.keys import make_argumented_key
from kmk.modules import Module


class RapidFireMeta:
    def __init__(
        self, kc, repeat=100, wait=200, randomize_repeat=False, randomize_magnitude=15
    ):
        self.kc = kc
        self.repeat = repeat
        self.wait = wait
        self.randomize_repeat = randomize_repeat
        self.randomize_magnitude = randomize_magnitude


class RapidFire(Module):
    _active_keys = {}

    def __init__(self):
        make_argumented_key(
            validator=RapidFireMeta,
            names=('RF',),
            on_press=self._rf_pressed,
            on_release=self._rf_released,
        )

    def _get_repeat(self, key):
        if key.meta.randomize_repeat:
            return key.meta.repeat + randint(
                -key.meta.randomize_magnitude, key.meta.randomize_magnitude
            )
        return key.meta.repeat

    def _on_timer_timeout(self, key, keyboard):
        keyboard.tap_key(key.meta.kc)
        self._active_keys[key] = keyboard.set_timeout(
            self._get_repeat(key), lambda: self._on_timer_timeout(key, keyboard)
        )

    def _rf_pressed(self, key, keyboard, *args, **kwargs):
        keyboard.tap_key(key.meta.kc)
        self._active_keys[key] = keyboard.set_timeout(
            key.meta.wait, lambda: self._on_timer_timeout(key, keyboard)
        )

    def _rf_released(self, key, keyboard, *args, **kwargs):
        if key in self._active_keys:
            keyboard.cancel_timeout(self._active_keys[key])
            self._active_keys.pop(key)

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return
