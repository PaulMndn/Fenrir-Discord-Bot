

class Cmd:
    def __init__(
        self, 
        execute,
        help_text = "",
        params_required = 0,
        team_required = False,
        admin_required = False
    ):
        self.execute = execute
        self.help_text = help_text
        self.params_required = params_required
        self.team_required = team_required
        self.admin_required = admin_required
    
    def print_help(self):
        if self.help_text == "":
            self.help_text = "No help available for this command yet."
        return self.help_text

