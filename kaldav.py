import logging

import datetime
import time
import locale
import pytz

import caldav
from caldav.elements import dav, cdav

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Kaldav (NeuronModule):
    def __init__(self, **kwargs):
        super(Kaldav, self).__init__(**kwargs)

        # get parameters form the neuron
        self.configuration = {
            'url': kwargs.get('url', None),
            'action': kwargs.get('action', None),
            'max_results': kwargs.get('max_results', 1),
            'name': kwargs.get('name', None),
            'start_date': kwargs.get('start_date', None),
            'end_date': kwargs.get('end_date', None),
            'date_format': kwargs.get('date_format', '%b %d %Y %I:%M%p'),
            'timezone': kwargs.get('timezone', None)
        }

        # check parameters
        if self._is_parameters_ok():
            self.response = {
                'action': self.configuration['action']
            }
            if self.configuration['action'] == "search":
                events = self.search_event(self.configuration['start'], self.configuration['end'])
                if events is not False:
                    self.response['events'] = events
            elif self.configuration['action'] == "create":
                self.create_event()
            elif self.configuration['action'] == 'delete':
                pass

            self.say(self.response)

    def get_calendars(self):
        client = caldav.DAVClient(self.configuration['url'])
        principal = client.principal()
        calendars = principal.calendars()
        return calendars

    def create_event(self):
        logger.debug('Creating an event')
        calendars = self.get_calendars()
        calendar = calendars[0]
        logger.debug("Using calendar %s" % calendar)

        if len(calendars) > 0:
            calendar = calendars[0]

            start = datetime.datetime.strptime(
                self.configuration['start_date'],
                self.configuration['date_format'])

            end = datetime.datetime.strptime(
                self.configuration['end_date'],
                self.configuration['date_format'])

            logger.debug("Start date: %s" % start)
            logger.debug("End date: %s" % end)

            # Manage locales.
            if self.configuration['timezone'] is not None:
                logger.debug('Timezone set to %s, converting.' % self.configuration['timezone'])
                local = pytz.timezone(self.configuration['timezone'])
                # Start date:
                start_local = local.localize(start, is_dst=None)
                # Override start with utc time.
                start = start_local.astimezone(pytz.utc)

                # End date:
                end_local = local.localize(end, is_dst=None)
                # Override end with utc time.
                end = end_local.astimezone(pytz.utc)

                # Debug
                logger.debug("start date local time: %s start date utc: %s "% (start_local, start))
                logger.debug("end date local time: %s end date utc: %s "% (end_local, end))

            start_str = start.strftime("%Y%m%dT%H%M00Z")
            end_str = end.strftime("%Y%m%dT%H%M00Z")
            # 20180528T180000Z
            # 20180528T190000Z

            vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Sabre//Sabre VObject 4.1.2//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
SUMMARY:""" + self.configuration['name'] + """
DTSTART:""" + start_str + """
DTEND:""" + end_str + """
END:VEVENT
END:VCALENDAR
"""
        logger.debug(vcal)
        event = calendar.add_event(vcal)
        # event = self.configuration['name']
        logger.debug("Event %s created" % event)

    def search_event(self, start, end=None):
        logger.debug('Searching event')
        calendars = self.get_calendars()

        if len(calendars) > 0:
            calendar = calendars[0]
            logger.debug("Using calendar %s" % calendar)

            if start is None:
                start = datetime.datetime.today()
            else:
                # TODO: transform in datetime
                pass
            if end is not None:
                # TODO: transform in datetime
                pass
            logger.debug("Looking for events between %s and %s" % (start, end))
            results = calendar.date_search(start, end)

            events = []
            for event in results:
                e = Kvevent(event.data)
                logger.debug("Found event: %s" % e)
                #logger.debug(e.get_property('DTSTART'))
                #logger.debug(e.get_property('DTEND'))
                events.append({
                    'start': e.get_property('DTSTART'),
                    'end': e.get_property('DTEND'),
                    'name': e.get_property('SUMMARY')
                })

            logger.debug(events)
            return events
        return False

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.configuration['url'] is None:
            raise InvalidParameterException("CalDav requires an URL.")

        if self.configuration['action'] is None:
            raise InvalidParameterException("CalDav requires an action.")

        return True


class Kvevent():
    def __init__(self, vevent_string):
        logger.debug("Creating Kvevent:\n %s" % vevent_string)
        self.properties = {}
        # Properties can be there twice like "END".
        self.properties = vevent_string.splitlines()

    def get_property(self, name):
        logger.debug('looking for property %s' % name)
        results = []
        for line in self.properties:
            items = line.split(':')
            # logger.debug('name = %s - items0 = %s' % (name, items[0]))
            if name == items[0]:
                logger.debug('found property %s: %s - %s' % (name, items[0], items[1]))
                results.append(items[1])
        return results
