import discord
import datetime as dt


class Event:
    def __init__(self, title: str, date_time: dt.datetime, event_channel_id: int = None, msg_id: int = None):
        self.title = title
        self.date_time = date_time
        self.event_channel_id = event_channel_id
        self.msg_id = msg_id
    
    def __str__(self):
        return f"**{self.title}** {self.date_time.strftime('%d.%m.%Y at %I:%M%p')}"
    
    def __lt__(self, other):
        if isinstance(other, Event):
            return self.date_time < other.date_time
        elif isinstance(other, dt.datetime):
            return self.date_time < other
        elif isinstance(other, dt.date):
            return self.date_time.date() < other
        else:
            raise NotImplementedError(f"Can't compare type '{type(self)}'v to type '{type(other)}'.")

    def __le__(self, other):
        if isinstance(other, Event):
            return self.date_time <= other.date_time
        elif isinstance(other, dt.datetime):
            return self.date_time <= other
        elif isinstance(other, dt.date):
            return self.date_time.date() <= other
        else:
            raise NotImplementedError(f"Can't compare type '{type(self)}' to type '{type(other)}'.")
    
    def __ge__(self, other):
        if isinstance(other, Event):
            return self.date_time >= other.date_time
        elif isinstance(other, dt.datetime):
            return self.date_time >= other
        elif isinstance(other, dt.date):
            return self.date_time.date() >= other
        else:
            raise NotImplementedError(f"Can't compare type '{type(self)}' to type '{type(other)}'.")
    
    def __eq__(self, other):
        if isinstance(other, Event):
            return self.date_time == other.date_time
        elif isinstance(other, dt.datetime):
            return self.date_time == other
        elif isinstance(other, dt.date):
            return self.date_time.date() == other
        else:
            raise NotImplementedError(f"Can't compare type '{type(self)}' to type '{type(other)}'.")
    
    @property
    def key(self):
        '''Message ID if it exists. Otherwise the datetime in iso-format.'''
        return str(self.msg_id) if self.msg_id is not None else self.date_time.isoformat()
    
    def add_message(self, msg:discord.Message):
        self.event_channel_id = msg.channel.id
        self.msg_id = msg.id





if __name__ == "__main__":
    pass