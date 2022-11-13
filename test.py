
from toolkit import Image

ret = Image.load(rf'image/3440.1440/weapon.attachment')
for name, img in ret:
    print(f"'{name}': '{name}',")

