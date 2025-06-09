


# from pywizlight.discovery import discover_lights
# import asyncio

# async def main():
#     bulbs = await discover_lights(broadcast_space="192.168.0.255")
#     for bulb in bulbs:
#         print(bulb.ip)

# asyncio.run(main())

import asyncio
from dataclasses import dataclass
from typing import Dict, Optional

from pywizlight import wizlight
from pywizlight.discovery import discover_lights


from pywizlight import wizlight, PilotBuilder

@dataclass
class Bulb:
    ip: str
    mac: str
    name: Optional[str] = None
    _wiz: Optional[wizlight] = None

    def __str__(self):
        return f"{self.name or 'Unnamed'} ({self.mac}) at {self.ip}"

    @classmethod
    def from_discovered(cls, d):
        mac = d.mac.lower()
        return cls(ip=d.ip, mac=mac, name=MAC_NAME_MAP.get(mac))

    def _conn(self) -> wizlight:
        if self._wiz is None:
            self._wiz = wizlight(self.ip)
        return self._wiz

    async def turn_on(self):
        await self._conn().turn_on()

    async def turn_off(self):
        await self._conn().turn_off()

    async def set_brightness(self, value: int):
        await self._conn().turn_on(PilotBuilder(brightness=value))

    async def set_colortemp(self, kelvin: int):
        await self._conn().turn_on(PilotBuilder(colortemp=kelvin))

    async def set_rgb(self, r: int, g: int, b: int):
        await self._conn().turn_on(PilotBuilder(rgb=(r, g, b)))

    async def update_state(self):
        state = await self._conn().updateState()
        print(f"Bulb: {self}")
        print(f"  On:         {state.get_is_on()}")
        print(f"  Brightness: {state.get_brightness()}")
        print(f"  Color Temp: {state.get_colortemp()}")
        print(f"  RGB:        {state.get_rgb()}")


async def discover_bulbs():
    print("Discovering bulbs on network...")
    found = await discover_lights(broadcast_space="192.168.0.255")
    bulbs = [Bulb.from_discovered(b) for b in found]
    return bulbs


async def test_control():
    bulbs = await discover_bulbs()
    if not bulbs:
        print("No bulbs found.")
        return

    b = bulbs[0]
    print(f"Controlling: {b}")

    await b.turn_on()
    await asyncio.sleep(1)

    await b.set_brightness(50)
    await asyncio.sleep(1)

    await b.set_colortemp(4000)
    await asyncio.sleep(1)

    await b.set_rgb(255, 100, 0)
    await asyncio.sleep(1)

    await b.update_state()

    await asyncio.sleep(1)
    await b.turn_off()

if __name__ == "__main__":
    asyncio.run(test_control())


# # ----------------------------------------
# # Entrypoint
# async def main():
#     bulbs = await discover_bulbs()
#     if not bulbs:
#         print("No bulbs found.")
#         return
#     for bulb in bulbs:
#         print(bulb)


# if __name__ == "__main__":
#     asyncio.run(main())


