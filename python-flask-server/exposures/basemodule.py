import sys
import re
from datetime import datetime, date, timedelta
from configparser import ConfigParser
from flask import jsonify
from controllers import Session

parser = ConfigParser()
parser.read('ini/connexion.ini')
sys.path.append(parser.get('sys-path', 'exposures'))
sys.path.append(parser.get('sys-path', 'controllers'))


class GetExposureData(object):

    def min_date(self, *args):
        session = Session()
        date_table = args[0]
        date_column = args[1]
        sql = ('select min(' + date_column + ') from ' + date_table + ';')
        min_date = datetime.strftime(session.execute(sql).scalar(), '%Y-%m-%d')
        min_date = datetime.strptime(min_date, '%Y-%m-%d')
        return min_date

    def max_date(self, *args):
        session = Session()
        date_table = args[0]
        date_column = args[1]
        sql = ('select max(' + date_column + ') from ' + date_table + ';')
        max_date = datetime.strftime(session.execute(sql).scalar(), '%Y-%m-%d')
        max_date = datetime.strptime(max_date, '%Y-%m-%d')
        session.close()
        return max_date

    def is_before_date_range(self, *args):
        date_to_compare = datetime.strptime(args[2], '%Y-%m-%d')
        min_date = self.min_date(*args)
        if min_date > date_to_compare:
            return True

        return False

    def is_after_date_range(self, *args):
        date_to_compare = datetime.strptime(args[2], '%Y-%m-%d')
        max_date = self.max_date(*args)
        if max_date < date_to_compare:
            return True

        return False

    def is_invalid_date_range(self, *args):
        start_date = datetime.strptime(args[0], '%Y-%m-%d')
        end_date = datetime.strptime(args[1], '%Y-%m-%d')
        if start_date > end_date:
            return True

        return False

    def validate_date_range(self, **args):
        try:
            datetime.strptime(args.get('start_date'), '%Y-%m-%d')
            datetime.strptime(args.get('end_date'), '%Y-%m-%d')
        except ValueError:
            return False, ('Not Found', 400, {'x-error': 'Invalid date range'})
        if self.is_invalid_date_range(args.get('start_date'), args.get('end_date')):
            return False, ('Not Found', 400, {'x-error': 'Invalid date range'})
        if self.is_before_date_range(args.get('date_table'), args.get('date_column'), args.get('end_date')):
            return False, ('Not Found', 404, {'x-error': 'end_date precedes date range'})
        if self.is_after_date_range(args.get('date_table'), args.get('date_column'), args.get('start_date')):
            return False, ('Not Found', 404, {'x-error': 'start_date occurs after date range'})

        return True, ''

    def validate_exposure_point(self, **args):
        weekday_set = {'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'other'}
        start_time_set = {'00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                          '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'}
        end_time_set = {'00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                        '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'}

        points = [p.split(',') for p in args.get('exposure_point').split(';')]
        for p in points:
            if len(p) == 3:
                duration = p[2]
                if len(duration) == 2:
                    if duration[0:2] not in weekday_set:
                        return False, ('Not Found', 400, {'x-error': 'Invalid exposure_point weekday'}), []
                elif len(duration) == 4:
                    if duration[0:2] not in start_time_set or duration[2:4] not in end_time_set \
                            or int(duration[0:2]) >= int(duration[2:4]):
                        return False, ('Not Found', 400, {'x-error': 'Invalid exposure_point '
                                                                     'start_time or end_time'}), []
                elif len(duration) == 5 and duration != 'other':
                    return False, ('Not Found', 400, {'x-error': 'Invalid exposure_point'}), []
                elif len(duration) == 6:
                    if duration[0:2] not in weekday_set or duration[2:4] not in start_time_set \
                            or duration[4:6] not in end_time_set or int(duration[2:4]) >= int(duration[4:6]):
                        return False, ('Not Found', 400, {'x-error': 'Invalid exposure_point weekday or '
                                                                     'start_time or end_time'}), []
                elif len(duration) < 2 or len(duration) > 6:
                    return False, ('Not Found', 400, {'x-error': 'Invalid exposure_point'}), []

        return True, '', points

    def validate_coordinate_point(self, **args):

        lat = args.get('latitude')
        lon = args.get('longitude')
        pt = [lat, lon]

        # if lat is populated - make sure lon is too - and vise versa
        if (lat is None) and (lon is not None) or (lat is not None) and (lon is None):
            return False, ('Not Found', 400, {'x-error': 'Both latitude and longitude must be specified to search for'
                                                         ' a point'}), []
        # check format of coordinates, if provided
        if lat is not None and len is not None:
            # check latitude
            if re.match("^(\+|-)?(?:90(?:(?:\.0{1,})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,})?))$", lat) is None:
                return False, ('Not Found', 400, {'x-error': 'Invalid latitude'}), []

            # check longitude
            if re.match("^(\+|-)?(?:180(?:(?:\.0{1,})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,})?))$", lon) is None:
                return False, ('Not Found', 400, {'x-error': 'Invalid longitude'}), []

        return True, '', pt

    def validate_coordinate_radius(self, **args):

        radius_str = args.get('radius')
        try:
            radius = int(radius_str)
        except ValueError as ex:
            return False, ('Not Found', 400, {'x-error': 'Invalid radius'}), -1

         # set max value to 500 meters for now
        if radius > 500:
            return False, ('Not Found', 400, {'x-error': 'Invalid radius. Must be <= 500'}), -1

        return True, '', radius

    def validate_page(self, **args):
        page_str = args.get('page')
        try:
            page = int(page_str)
        except ValueError as ex:
            return False, ('Invalid page', 400, {'x-error': 'page must be integer > 0'})
        if page < 1:
            return False, ('Invalid page', 400, {'x-error': 'page must be integer > 0'})

        return True, ''

    def get_date_list(self, **kwargs):
        date_list = ([datetime.strftime(datetime.strptime(kwargs.get('start_date'), '%Y-%m-%d').date() + timedelta(days=i), '%Y-%m-%d')] for i in range(((datetime.strptime(kwargs.get('end_date'), '%Y-%m-%d')) - (datetime.strptime(kwargs.get('start_date'), '%Y-%m-%d'))).days + 1))
        return date_list

    def get_coordinates(self, **kwargs):
        raise NotImplemented

    def get_dates(self, **kwargs):
        raise NotImplemented

    def get_values(self, **kwargs):
        raise NotImplemented

    def get_scores(self, **kwargs):
        raise NotImplemented
