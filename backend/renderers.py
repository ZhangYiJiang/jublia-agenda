from icalendar import Calendar
from rest_framework.exceptions import NotFound
from rest_framework.renderers import BaseRenderer


class CalendarRenderer(BaseRenderer):
    media_type = 'text/calendar'
    format = 'ics'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            rendered_data = data.to_ics()
            if not isinstance(rendered_data, Calendar):
                calendar = Calendar()
                calendar.add_component(rendered_data)
                rendered_data = calendar
            return rendered_data.to_ical()
        except ValueError:
            raise NotFound
