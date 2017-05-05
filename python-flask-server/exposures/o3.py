from basemodule import GetExposureData
from configparser import ConfigParser
from flask import jsonify
from datetime import datetime, timedelta
from controllers import Session

parser = ConfigParser()
parser.read('ini/connexion.ini')

limit = 100
offset = 0


class GetO3ExposureData(GetExposureData):
    # radius used to give some leeway to finding the specified lat lon
    radius_meters = "2"

    # this might move up to parent class if it is generic for all
    def create_values_query(self, dt, pt, radius, stat_type, temp_res):

        date_loc_where = "where cast(utc_date_time as date) = cast('" + dt[0] + "' as date) " \
                            "and ST_DWithin(ST_GeographyFromText('POINT(" + \
                            pt[1] + " " + pt[0] + ")'),location," + radius + ")"

        if temp_res == "hour":
            # for hourly - ignore temporal resolution and just return all hours
            sql = "select utc_date_time, coalesce(ozone ,0) as o3_total " \
                  "from cmaq " + \
                  date_loc_where

        else:  # assume default - temp_res == "day":
            if stat_type == "max":
                sql = "select max(coalesce(ozone,0)) " \
                     "from cmaq " + \
                     date_loc_where

            elif stat_type == "median":
                sql = "with date_loc_query as (select (coalesce(ozone,0)) " \
                     "as o3_total " \
                    "from cmaq " + \
                    date_loc_where + ") select percentile_cont(0.5) within group(order by o3_total) from date_loc_query"

            elif stat_type == "mean":
                sql = "select avg(coalesce(ozone,0)) " \
                    "from cmaq " + \
                    date_loc_where

        return sql

    def get_values(self, **kwargs):
        # kwargs: exposure_type, start_date, end_date, exposure_point, temporal_resolution=None,
        #         statistical_type=None, radius = None, page = None
        (valid_page, message) = GetExposureData.validate_page(self, **kwargs)
        if not valid_page:
            return message

        (valid_points, message, point_list) = GetExposureData.validate_exposure_point(self, **kwargs)
        if not valid_points:
            return message

        (valid_radius, message, radius) = GetExposureData.validate_coordinate_radius(self, **kwargs)
        if not valid_radius:
            return message

        date_list = GetExposureData.get_date_list(self, **kwargs)

        # retrieve the temporal resolution and the statistical type
        tres = kwargs.get('temporal_resolution')
        stype = kwargs.get('statistical_type')
        self.radius_meters = kwargs.get('radius')

        sql_array = []
        session = Session()
        for dt in date_list:
            for pt in point_list:
                sql = self.create_values_query(dt, pt, self.radius_meters, stype, tres)

                if tres == "hour":
                    result = session.execute(sql)
                else:
                    result = session.execute(sql).scalar()
                # return empty string "" if data is not available
                if not result:
                    result = ''

                if tres == "hour":
                 for row in result:
                    sql_array.append([row['utc_date_time'], row['utc_date_time'],
                                    pt[0], pt[1], str(row['o3_total'])])
                else:
                    sql_array.append([datetime.strptime(dt[0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                    datetime.strptime(dt[0] + ' 23:00:00', '%Y-%m-%d %H:%M:%S'),
                                    pt[0], pt[1], str(result)])

        session.close()
        page = int(kwargs.get('page'))
        offset = (page - 1) * limit
        data = jsonify([{'end_time': o[1], 'exposure_type': 'o3', 'latitude': o[2], 'longitude': o[3],
                         'start_time': o[0], 'units': 'ppm', 'value': o[4]
                         } for o in sql_array[offset:(offset + limit)]])

        return data, 200, {'page': page, 'per_page': limit}

    # supports 7dayrisk and 14dayrisk total scores
    # applies to 7 or 14 days, previous to dates provided (including date provided)
    # if a full set of data is not available for 7dayrisk - 7 rows returned,
    # or 14dayrisk - 14 rows returned, the empty string "" will be returned
    def get_scores(self, **kwargs):
        # kwargs: exposure_type, start_date, end_date, exposure_point, temporal_resolution=None,
        #         score_type=None, radius = None, page = None
        (valid_page, message) = GetExposureData.validate_page(self, **kwargs)
        if not valid_page:
            return message

        (valid_points, message, point_list) = GetExposureData.validate_exposure_point(self, **kwargs)
        if not valid_points:
            return message

        (valid_radius, message, radius) = GetExposureData.validate_coordinate_radius(self, **kwargs)
        if not valid_radius:
            return message

        date_list = GetExposureData.get_date_list(self, **kwargs)
        self.radius_meters = kwargs.get('radius')
        sql_array = []
        session = Session()
        for dt in date_list:
            for pt in point_list:

                # set date range for 7 or 14 day risk
                score_type = kwargs.get('score_type')
                date_range = int(score_type[:len(score_type) - len("dayrisk")])

                d = datetime.strptime(dt[0], '%Y-%m-%d') - timedelta(days=date_range-1)  # change this to 6 or 13
                end_date = datetime.strptime(dt[0], '%Y-%m-%d')
                delta = timedelta(days=1)
                scores = 0


                while d <= end_date:
                    d_as_str = d.strftime("%Y-%m-%d")

                    sql = "select max(coalesce(ozone,0)) from cmaq " \
                            "where cast(utc_date_time as date) = cast('" + d_as_str + "' as date) " \
                            "and ST_DWithin(ST_GeographyFromText('POINT(" + pt[1] + " " + pt[0] + ")'), location, " + \
                            self.radius_meters + ")"

                    result = session.execute(sql).scalar()

                    # DESo = 1 if 24h max ozone ≤ 0.050 ppm
                    # DESo = 2 if 24h max ozone 0.051 – 0.075 ppm
                    # DESo = 3 if 24h max ozone 0.076-0.100 ppm
                    # DESo = 4 if 24h max ozone 0.101-0.125 ppm
                    # DESo = 5 if 24h max ozone > 0.125 ppm

                    if not result:
                        scores = ''
                        break
                    elif result <= 0.050:
                        result = 1
                    elif 0.050 < result <= 0.075:
                        result = 2
                    elif 0.075 < result <= 0.100:
                        result = 3
                    elif 0.100 < result <= 0.125:
                        result = 4
                    elif result > 0.125:
                        result = 5

                    scores += result

                    # iterate to next day
                    d += delta

                if scores == '':
                    risk = scores
                else:
                    risk = scores / date_range
                sql_array.append([datetime.strptime(dt[0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                    datetime.strptime(dt[0] + ' 23:00:00', '%Y-%m-%d %H:%M:%S'),
                                    pt[0], pt[1], str(risk)])

        session.close()
        page = int(kwargs.get('page'))
        offset = (page - 1) * limit
        data = jsonify([{'end_time': o[1], 'exposure_type': 'o3', 'latitude': o[2], 'longitude': o[3],
                         'start_time': o[0], 'units': score_type, 'value': o[4]
                         } for o in sql_array[offset:(offset + limit)]])

        return data, 200, {'page': page, 'per_page': limit}

# Define valid parameter sets
temporal_resolution_set = {'hour', 'day'}
score_type_set = {'7dayrisk', '14dayrisk'}
statistical_type_set = {'max', 'mean', 'median'}

exp = GetO3ExposureData()

def get_coordinates(**kwargs):
    # kwargs: exposure_type, latitude = None, longitude = None, radius = None, page = None

    (valid_page, message) = exp.validate_page(**kwargs)
    if not valid_page:
        return message

    (valid_points, message, pt) = exp.validate_coordinate_point(**kwargs)
    if not valid_points:
        return message

    (valid_radius, message, radius) = exp.validate_coordinate_radius(**kwargs)
    if not valid_radius:
        return message

    page = int(kwargs.get('page'))
    offset = (page - 1) * limit

    if pt[0] is None:
        sql = "select distinct latitude, longitude from cmaq order by latitude limit %s offset %s ;" % (limit, offset)
    else:
        sql = "select distinct latitude, longitude from cmaq where ST_DWithin(ST_GeographyFromText('POINT("\
              + pt[1] + " " + pt[0] + ")'), location," + str(radius) + ") limit %s offset %s ;" % (limit, offset)

    session = Session()

    results = session.execute(sql)
    session.close()
    data = jsonify([dict(latitude=str(o.latitude), longitude=str(o.longitude))
                    for o in results])
    return data, 200, {'page': page, 'per_page': limit}

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
