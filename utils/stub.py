# Measurement generator to demo or development without attached arduino
import random


def mock_read(self, plug_count=5):
    serial_str = ""
    for id in range(1, plug_count + 1):
        voltage = random.randint(210, 240)
        current = random.randint(0, 10)
        power = voltage * current
        # TODO currently active status is applied by default because not returned by arduino
        # active = True
        serial_str += f"{id},{voltage},{current},{power};"

    time = random.randint(3700, 4100)
    serial_str += f"t{time}"

    print(serial_str)
    return serial_str