##

import json

with open("./configure.json", encoding="utf-8") as f:
    mysql_config = json.load(f)["mysql"]
