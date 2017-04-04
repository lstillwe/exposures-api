from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from basemodule import GetExposureData
from configparser import ConfigParser
from flask import jsonify
from datetime import datetime
import sys

parser = ConfigParser()
parser.read('ini/connexion.ini')
POSTGRES_ENGINE = 'postgres://' + parser.get('postgres', 'username') + ':' + parser.get('postgres', 'password') \
                  + '@' + parser.get('postgres', 'host') + ':' + parser.get('postgres', 'port') \
                  + '/' + parser.get('postgres', 'database')
sys.path.append(parser.get('sys-path', 'exposures'))
engine = create_engine(POSTGRES_ENGINE)
Session = sessionmaker(bind=engine)

class GetPm25ExposureData(GetExposureData):

    def get_values(self, **kwargs):
        # print(kwargs)
        # {'kwargs': {'statistical_type': 'max', 'temporal_resolution': 'day', 'exposure_point': 'alkd',\
        #  'end_date': '2001-02-01', 'start_date': '2001-01-02', 'exposure_type': 'pm25'}}
        session = Session()
        (valid_points, message, point_list) = GetExposureData.validate_exposure_point(self, **kwargs)
        if not valid_points:
            return message
        date_list = GetExposureData.get_date_list(self, **kwargs)
        sql_array = []
        for dt in date_list:
            for pt in point_list:
                sql = "select max(coalesce(pm25_primary,0) + coalesce(pm25_secondary,0)) from cmaq " \
                      "where cast(utc_date_time as date) = cast('" + \
                      dt[0] + "' as date) and latitude = " + pt[0] + " and longitude = " + pt[1] + ";"
                result = session.execute(sql).scalar()
                if not result:
                    result = 'Not Available'
                sql_array.append([datetime.strptime(dt[0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                  datetime.strptime(dt[0] + ' 23:00:00', '%Y-%m-%d %H:%M:%S'),
                                  pt[0], pt[1], str(result)])
        session.close()
        data = jsonify([{'end_time': o[1], 'exposure_type': 'pm25', 'latitude': o[2], 'longitude': o[3],
                         'start_time': o[0], 'units': 'ugm3', 'value': o[4]
                         } for o in sql_array])

        return data

    def get_scores(self, **kwargs):
        # {'kwargs': {'statistical_type': 'max', 'temporal_resolution': 'day', 'exposure_point': 'alkd',\
        #  'end_date': '2001-02-01', 'start_date': '2001-01-02', 'exposure_type': 'pm25'}}
        session = Session()
        (valid_points, message, point_list) = GetExposureData.validate_exposure_point(self, **kwargs)
        if not valid_points:
            return message
        date_list = GetExposureData.get_date_list(self, **kwargs)
        sql_array = []
        for dt in date_list:
            for pt in point_list:
                sql = "select max(coalesce(pm25_primary,0) + coalesce(pm25_secondary,0)) from cmaq " \
                      "where cast(utc_date_time as date) = cast('" + \
                      dt[0] + "' as date) and latitude = " + pt[0] + " and longitude = " + pt[1] + ";"
                result = session.execute(sql).scalar()
                # 1: 24h max PM2.5 < 4.0 μg/m3
                # 2: 24h max PM2.5 4.0-7.06 μg/m3
                # 3: 24h max PM2.5 7.007-8.97 μg/m3
                # 4: 24h max PM 2.5 8.98-11.36 μg/m3
                # 5: 24h max PM2.5 > 11.37 μg/m3
                if not result:
                    result = 'Not Available'
                elif result < 4.0:
                    result = 1
                elif 4.0 <= result < 7.06:
                    result = 2
                elif 7.06 <= result < 8.97:
                    result = 3
                elif 8.97 <= result < 11.36:
                    result = 4
                elif result >= 11.36:
                    result = 5

                sql_array.append([datetime.strptime(dt[0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                  datetime.strptime(dt[0] + ' 23:00:00', '%Y-%m-%d %H:%M:%S'),
                                  pt[0], pt[1], str(result)])
        session.close()
        data = jsonify([{'end_time': o[1], 'exposure_type': 'pm25', 'latitude': o[2], 'longitude': o[3],
                         'start_time': o[0], 'units': kwargs.get('score_type'), 'value': o[4]
                         } for o in sql_array])

        return data

# Define valid parameter sets
temporal_resolution_set = {'hour', 'day'}
score_type_set = {'7dayrisk', '14dayrisk'}
statistical_type_set = {'max', 'mean', 'median'}

exp = GetPm25ExposureData()


def get_values(**kwargs):
    # print(kwargs)
    date_args = {'date_table': 'cmaq', 'date_column': 'utc_date_time', 'start_date': kwargs.get('start_date'),
            'end_date': kwargs.get('end_date')}
    (valid_date, message) = exp.validate_date_range(**date_args)
    if not valid_date:
        return message
    if kwargs.get('temporal_resolution') not in temporal_resolution_set:
        return 'Not Found', 400, {'x-error': 'Invalid temporal_resolution'}
    if kwargs.get('statistical_type') not in statistical_type_set:
        return 'Not Found', 400, {'x-error': 'Invalid statistical_type'}

    return exp.get_values(**kwargs)


def get_scores(**kwargs):
    print(kwargs)
    date_args = {'date_table': 'cmaq', 'date_column': 'utc_date_time', 'start_date': kwargs.get('start_date'),
            'end_date': kwargs.get('end_date')}
    (valid_date, message) = exp.validate_date_range(**date_args)
    if not valid_date:
        return message
    if kwargs.get('temporal_resolution') not in temporal_resolution_set:
        return 'Not Found', 400, {'x-error': 'Invalid temporal_resolution'}
    if kwargs.get('score_type') not in score_type_set:
        return 'Not Found', 400, {'x-error': 'Invalid score_type'}

    return exp.get_scores(**kwargs)