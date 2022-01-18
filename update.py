import shelve
import json
from cfg import DATA_DIR


guild_dirs = [d for d in DATA_DIR.iterdir() if d.is_dir()]
print("\n".join(str(i) for i in guild_dirs))


for dir in guild_dirs:
    with shelve.open(str(dir/"settings")) as s:
        with open(str(dir/"settings.json"), "w") as f:
            json.dump(dict(s), f)
    
    to_del = [d for d in dir.glob("settings*") if d.is_file() and not str(d).endswith(".json")]
    for d in to_del:
        d.unlink()