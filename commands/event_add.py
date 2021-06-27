import re
import datetime as dt

from commands.base import Cmd
from functions import add_event, get_events


help_text = f'''Add a new event entry to the calendar.

The message needs to include a title in quotes, followed by *on <date> at <time>*.
**British Time** is assumed as timezone.
Is no date parameter given, the current date is assumed.

Examples:
```<PREFIX><COMMAND> 'Scrim against Team' on 22.05.2021 at 07:00pm
<PREFIX><COMMAND> 'Training' at 07:00 pm on 21.12.2012
<PREFIX><COMMAND> 'Foo Bar' at 07:00AM```'''


async def execute(ctx, params):
    string = ctx["params_str"]

    # create regular expression
    time_re = r"at ([01]\d:\d\d) ?(am|AM|pm|PM)"
    date_re = r"on ([0123]\d[.][01]?\d[.](\d\d\d\d))"
    pattern = f"^['\"](.*)['\"] ({date_re} {time_re}|{time_re}( {date_re})?)$"
    p = re.compile(pattern)

    match = re.match(p, string)

    if not match:
        return False, f"Parameters for command `{ctx['prefix']}{ctx['command']}` don't match the format. Please try again or see help."
    
    data = {
        "title": match.group(1),
        "date1": match.group(3),
        "time1": match.group(5),
        "period1": match.group(6),
        "time2": match.group(7),
        "period2": match.group(8),
        "date2": match.group(10)
    }
    title = data["title"]
    date = data["date1"] if data["date1"] else (data["date2"] if data["date2"] else dt.date.today().strftime("%d.%m.%Y"))
    time = data["time1"] if data["time1"] else data["time2"]
    period = data["period1"] if data["period1"] else data["period2"]
    
    date_time = dt.datetime.strptime(f"{date} {time}{period}", "%d.%m.%Y %I:%M%p")

    events = get_events(ctx['guild'])
    if date_time in events:
        return False, f"There is already an event scheduled for that time:\n{events[date_time]}"

    if add_event(ctx["guild"], date_time, title):
        return True, f"Event **{title}** for *{date_time.strftime('%d.%m.%Y at %I:%M%p')}* was added."
    else:
        return False, "Event could not be added."


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=True
)
