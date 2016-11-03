from icalendar import Calendar
from rest_framework.exceptions import NotFound
from rest_framework.renderers import BaseRenderer

from backend.helper import calendar


class CalendarRenderer(BaseRenderer):
    media_type = 'text/calendar'
    format = 'ics'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            rendered_data = data.to_ical()
            if not isinstance(rendered_data, Calendar):
                cal = calendar()
                cal.add_component(rendered_data)
                rendered_data = cal
            return rendered_data.to_ical()
        except AttributeError:
            raise NotFound
