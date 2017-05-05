import sys
import importlib
from sqlalchemy import create_engine, exists, and_
from models import Cmaq, ExposureType
from flask import jsonify
from configparser import ConfigParser
from controllers import Session

parser = ConfigParser()
parser.read('ini/connexion.ini')
sys.path.append(parser.get('sys-path', 'exposures'))
sys.path.append(parser.get('sys-path', 'controllers'))


def exposures_exposure_type_coordinates_get(exposure_type, latitude = None, longitude = None, radius = None, page = None) -> str:
    session = Session()
    ret = session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                            ExposureType.has_values))).scalar()
    if not session.query(exists().where(ExposureType.exposure_type == exposure_type)).scalar():
        return 'Bad Request', 400, {'x-error': 'Invalid exposure parameters'}
    elif not session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                               and_(ExposureType.has_scores, ExposureType.has_values)))).scalar():
        return 'Not Found', 404, {'x-error': 'Dates not found for exposure type'}
    session.close()
    mod = importlib.import_module(exposure_type)
    kwargs = locals()
    data = mod.get_coordinates(**kwargs)

    return data


def exposures_exposure_type_dates_get(exposure_type) -> str:
    session = Session()
    ret = session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                            ExposureType.has_values))).scalar()
    if not session.query(exists().where(ExposureType.exposure_type == exposure_type)).scalar():
        return 'Bad Request', 400, {'x-error': 'Invalid exposure parameters'}
    elif not session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                               and_(ExposureType.has_scores, ExposureType.has_values)))).scalar():
        return 'Not Found', 404, {'x-error': 'Dates not found for exposure type'}
    session.close()
    mod = importlib.import_module(exposure_type)
    kwargs = locals()
    data = mod.get_dates(**kwargs)

    return data


def exposures_exposure_type_scores_get(exposure_type, start_date, end_date, exposure_point, \
                                       temporal_resolution=None, score_type=None, radius = None, page = None) -> str:
    session = Session()
    ret = session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                            ExposureType.has_values))).scalar()
    if not session.query(exists().where(ExposureType.exposure_type == exposure_type)).scalar():
        return 'Bad Request', 400, {'x-error': 'Invalid exposure parameters'}
    elif not session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                               ExposureType.has_scores))).scalar():
        return 'Not Found', 404, {'x-error': 'Values not found for exposure type'}
    session.close()
    mod = importlib.import_module(exposure_type)
    kwargs = locals()
    data = mod.get_scores(**kwargs)

    return data


def exposures_exposure_type_values_get(exposure_type, start_date, end_date, exposure_point, \
                                       temporal_resolution=None, statistical_type=None, radius = None, page = None) -> str:
    session = Session()
    ret = session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                            ExposureType.has_values))).scalar()
    if not session.query(exists().where(ExposureType.exposure_type == exposure_type)).scalar():
        return 'Bad Request', 400, {'x-error': 'Invalid exposure parameters'}
    elif not session.query(exists().where(and_(ExposureType.exposure_type == exposure_type,
                                            ExposureType.has_values))).scalar():
        return 'Not Found', 404, {'x-error': 'Values not found for exposure type'}
    session.close()
    mod = importlib.import_module(exposure_type)
    kwargs = locals()
    data = mod.get_values(**kwargs)

    return data


def exposures_get() -> str:
    session = Session()
    results = session.query(ExposureType).all()
    session.close()
    data = jsonify([dict(exposure_type=o.exposure_type, description=o.description, units=o.units,
                         has_values=o.has_values, has_scores=o.has_scores, schema_version=o.schema_version)
                    for o in results])

    return data
