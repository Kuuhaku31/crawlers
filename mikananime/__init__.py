##

import json

with open("./configure.json", encoding="utf-8") as f:
    mode_mikan_config = json.load(f)["modes"]["mikan"]
