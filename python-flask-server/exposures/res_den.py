from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from basemodule import GetExposureData
from configparser import ConfigParser
from flask import jsonify
import requests
from requests.auth import HTTPBasicAuth
import sys

parser = ConfigParser()
parser.read('ini/connexion.ini')
POSTGRES_ENGINE = 'postgres://' + parser.get('postgres', 'username') + ':' + parser.get('postgres', 'password') \
                  + '@' + parser.get('postgres', 'host') + ':' + parser.get('postgres', 'port') \
                  + '/' + parser.get('postgres', 'database')
sys.path.append(parser.get('sys-path', 'exposures'))
engine = create_engine(POSTGRES_ENGINE)
Session = sessionmaker(bind=engine)

class GetResDenExposureData(GetExposureData):
    # radius used to give some leeway to finding the specified lat lon
    # radius doesn't seem to really apply since values for a census tract will be returned
    # radius_meters = "2"

    apikey = "d31f54f88a96c3f21c9629d6c3e5601494a02e22"
    request_url = "http://citysdk.commerce.gov"

    # example request:
    # request_obj = {
    # 'lat': '35.9131996',
    # 'lng': '-79.0558445',
    # 'level': 'tract',
    # 'sublevel': False,
    # 'api': 'acs5',
    # 'year': 2010,
    # 'variables': ['POP', 'DENSITY']
}

response = requests.post(request_url, auth=HTTPBasicAuth(apikey, None), json=request_obj)

    def get_values(self, **kwargs):
        # {'kwargs': {'statistical_type': 'max', 'temporal_resolution': 'day', 'exposure_point': 'alkd',\
        #  'end_date': '2001-02-01', 'start_date': '2001-01-02', 'exposure_type': 'res_den'}}
        session = Session()
        (valid_points, message, point_list) = GetExposureData.validate_exposure_point(self, **kwargs)
        if not valid_points:
            return message
        date_list = GetExposureData.get_date_list(self, **kwargs)

        # retrieve the temporal resolution and the statistical type
        # only yearly applies for residential density
        # tres = kwargs.get('temporal_resolution')
        # stype = kwargs.get('statistical_type')

        sql_array = []

        for dt in date_list:
            for pt in point_list:
                x=0

        session.close()
        data = "[]"
        # data = jsonify([{'end_time': o[1], 'exposure_type': 'o3', 'latitude': o[2], 'longitude': o[3],
                         # 'start_time': o[0], 'units': 'ppm', 'value': o[4]
                         # } for o in sql_array])

        return data

    # 1 = Urbanized Areas (UAs) of 50,000 or more people
    # 2 = Urban Clusters (UCs) of at least 2,500 and less than 50,000 people
    # 3 = Rural (not UA or UC)

    def get_scores(self, **kwargs):
        # {'kwargs': {'temporal_resolution': 'day', 'exposure_point': 'alkd', 'score_type': '7dayrisk',\
        #  'end_date': '2001-02-01', 'start_date': '2001-01-02', 'exposure_type': 'res_den'}}
        session = Session()
        (valid_points, message, point_list) = GetExposureData.validate_exposure_point(self, **kwargs)
        if not valid_points:
            return message
        date_list = GetExposureData.get_date_list(self, **kwargs)
        sql_array = []

        # only yearly applies for residential density
        for dt in date_list:
            for pt in point_list:

                x=0
                # sql_array.append([datetime.strptime(dt[0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                    # datetime.strptime(dt[0] + ' 23:00:00', '%Y-%m-%d %H:%M:%S'),
                                    # pt[0], pt[1], str(risk)])

        session.close()
        data = "[]"
        # data = jsonify([{'end_time': o[1], 'exposure_type': 'res_den', 'latitude': o[2], 'longitude': o[3],
                        # 'start_time': o[0], 'units': score_type, 'value': o[4]
                         # } for o in sql_array])

        return data

# Define valid parameter sets
temporal_resolution_set = {'hour', 'day'}
score_type_set = {'UA', 'UC', 'rural'}
statistical_type_set = {'max', 'mean', 'median'}

exp = GetResDenExposureData()

def get_coordinates(**kwargs):

    (valid_points, message, pt) = exp.validate_coordinate_point(**kwargs)
    if not valid_points:
        return message

    (valid_radius, message, radius) = exp.validate_coordinate_radius(**kwargs)
    if not valid_radius:
        return message

    if pt[0] is None:
        sql = "select distinct latitude, longitude from cmaq order by latitude;"
    else:
        sql = "select distinct latitude, longitude from cmaq where ST_DWithin(ST_GeographyFromText('POINT("\
              + pt[1] + " " + pt[0] + ")'), location," + str(radius) + ")"

    session = Session()

    results = session.execute(sql)
    session.close()
    data = jsonify([dict(latitude=str(o.latitude), longitude=str(o.longitude))
                    for o in results])
    return data

def get_dates(**kwargs):
    min_date = exp.min_date('Cmaq', 'utc_date_time')
    max_date = exp.max_date('Cmaq', 'utc_date_time')
    data = jsonify({'start_date': min_date, 'end_date': max_date})
    return data

def get_values(**kwargs):
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
