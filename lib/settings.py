import discord
import json
from cfg import DATA_DIR
import utils

class GuildSettings(dict):
    #implemented as dict-alike oder von Dict ableiten --> init von super(), __setitem__ macht super().setitem und store
    def __init__(self, guild):
        # read file fill dict with correct
        if isinstance(guild, discord.Guild):
            self.guild_id = guild.id
        elif isinstance(guild, int):
            self.guild_id = guild
        else:
            raise ValueError("Guild must be a `discord.Guild` object or integer.")
        
        self.path = DATA_DIR / str(self.guild_id) / "settings.json"
        
        self._read()
        super().__init__(self.items())


    def reset(self):
        self.clear()
        self.update(utils.get_default_settings())
        self._write()


    def _read(self):
        self.clear()
        self.update(utils.get_default_settings())
        if self.path.exists():
            with open(str(self.path)) as f:
                self.update(json.load(f).items())


    def _write(self):
        with open(str(self.path), "w") as f:
            json.dump(self, f)


    def __setitem__(self, k, v):
        super().__setitem__(k,v)
        self._write()

    
    def __delitem__(self, k):
        self[k] = utils.get_default_settings()[k]
    

    def __str__(self):
        name_col_width = max(len(k) for k in self.keys()) + 3
        return "\n".join(f"{s:<{name_col_width}}{v}" for s,v in self.items())
