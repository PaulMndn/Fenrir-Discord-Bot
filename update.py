import shelve
import json
from cfg import DATA_DIR

def migrate_guild_settings():
    print("Migration of guild settings\n")
    guild_dirs = [d for d in DATA_DIR.iterdir() if d.is_dir()]
    print("Guild data directories to iterate over:")
    print("\n".join(str(i) for i in guild_dirs))
    if not input("\nIs this correct, do you want to continue? (Y/n) ").lower() == "y":
        print("\nMigration of guild settings cancelled.\n")
        return

    print()
    for dir in guild_dirs:
        print(f"Migrating settings for {dir}.")
        with shelve.open(str(dir/"settings")) as s:
            with open(str(dir/"settings.json"), "w") as f:
                json.dump(dict(s), f)
        
        to_del = [d for d in dir.glob("settings*") if d.is_file() and not str(d).endswith(".json")]
        for d in to_del:
            d.unlink()
    print("\nMigration of guild settings completed.\n")


if __name__ == "__main__":
    migrate_guild_settings()