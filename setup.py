from Functions import Functions
import math

f = Functions()


def set_units(unit_type='km'):
    """
    changes units type for distances
    :param unit_type: sting 'km' or 'nm'
    :return: void
    """
    if unit_type == 'km':
        f.a_e = 6371.0
    elif unit_type == 'nm':
        f.a_e = 3443.9


def direct(lat, lon, distance, azimuth):
    """
    solves direct geodesic issue
    :param lat: float between -90 and 90
    :param lon: float between -180 and 180
    :param distance: float
    :param azimuth: float between 0 and 359
    :return: tuple(lat,lon,reverse azimuth)
    """
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    azi = math.radians(azimuth)
    dist = distance / f.a_e
    lat2, lon2 = f.direct(lat1, lon1, dist, azi)
    dist, azi2 = f.inverse(lat2, lon2, lat1, lon1)
    return math.degrees(lat2), math.degrees(lon2), math.degrees(azi2)


def inverse(lat1, lon1, lat2, lon2):
    """
    solves inverse geodesic issue
    :param lat1: float between -90 and 90
    :param lon1: float between -180 and 180
    :param lat2: float between -90 and 90
    :param lon2: float between -180 and 180
    :return: tuple(azimuth, reverse azimuth, distance)
    """
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dist, azi2 = f.inverse(lat2, lon2, lat1, lon1)
    dist, azi1 = f.inverse(lat1, lon1, lat2, lon2)
    return math.degrees(azi1), math.degrees(azi2), dist * f.a_e


def angular(lat1, lon1, lat2, lon2, az13, az23):
    """
    solves angular issue: return coordinates of third point of spherical triangle by given coordinates of two points
    and azimuths to third point from each of two points
    :param lat1: float - latitude of first point
    :param lon1: float - longitude of first point
    :param lat2: float - latitude of second point
    :param lon2: float - longitude of second point
    :param az13: float - azimuth from first to third point
    :param az23: float - azimuth from second to third point
    :return: tuple of coordinates for third point, or "Azimuths has no intersection" if error.
    """
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    azi13 = math.radians(az13)
    azi23 = math.radians(az23)
    errflag, lat3, lon3 = f.angular(lat1, lon1, lat2, lon2, azi13, azi23)
    if errflag or (lat3 == 0. and lon3 == 0.):
        return "Azimuths has no intersection"
    else:
        return math.degrees(lat3), math.degrees(lon3)


def linear(lat1, lon1, lat2, lon2, dist13, dist23, cc):
    """
    solves linear issue: return coordinates of third point of spherical triangle by given coordinates of two points
     and distances to third point from each of two points
    :param lat1: float - latitude of first point
    :param lon1: float - longitude of first point
    :param lat2: float - latitude of second point
    :param lon2: float - longitude of second point
    :param dist13: float - distance from first to third point in selected units
    :param dist23: float - distance from second to third point in selected units
    :param cc: enum(0,1) - flag for placing third point:
                            0 - on the left from Q1-Q2 line (counterclockwise), 1 - on the right of those line (clockwise)
    :return: tuple of coordinates for third point, or "Vectors has no intersection" if error.
    """
    c = (cc != 0.)
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dist13 = dist13 / f.a_e
    dist23 = dist23 / f.a_e
    errflag, lat3, lon3 = f.linear(lat1, lon1, lat2, lon2, dist13, dist23, c)
    if errflag or (lat3 == 0. and lon3 == 0.):
        return "Vectors has no intersection"
    else:
        return math.degrees(lat3), math.degrees(lon3)


def distance(lat1, lon1, lat2, lon2):
    da = inverse(lat1, lon1, lat2, lon2)
    return da[2]


def azimuth(lat1, lon1, lat2, lon2):
    da = inverse(lat1, lon1, lat2, lon2)
    return da[0]


def bearing(lat1, lon1, lat2, lon2):
    da = inverse(lat1, lon1, lat2, lon2)
    return da[1]


def to_ivac(crd_decimal, crd_type='lat'):
    """
    converts decimal to ivac2
    :param crd_decimal: float
    :param crd_type: string 'lat' or 'lon', default 'lat'
    :return: string in ivac2 format
    """
    prefix = ["N", "S"] if crd_type == 'lat' else ["E", "W"]
    degrees = int(math.floor(abs(crd_decimal)))
    minutes = math.floor(float(abs(crd_decimal)-degrees)*60)
    seconds_list = str((float(abs(crd_decimal)-degrees)*60 - minutes)*60).split(".")
    seconds = "%02d" % int(seconds_list[0])+str(int(round(float("0."+seconds_list[1]), 2)*100))
    string_prefix = prefix[0] if crd_decimal > 0 else prefix[1]
    if crd_type == 'lat':
        return "%s%02d%02d%s" % (string_prefix, degrees, minutes, seconds)
    return "%s%03d%02d%s" % (string_prefix, degrees, minutes, seconds)


def from_ivac(string_coord):
    """
    converts ivac2 format to decimal
    :param string_coord: string in ivac2 format
    :return: float
    """
    numdeg = 4
    if string_coord[0] in ["N", "S"]:
        numdeg = 3
    prfx = string_coord[0]
    degrees = int(string_coord[1:numdeg])
    minutes = int(string_coord[numdeg:numdeg+2])
    seconds = string_coord[numdeg+2:numdeg+4]
    decimals = string_coord[numdeg+4:]
    seconds = float("%s.%s" % (seconds, decimals))
    crd_decimal = degrees + (minutes/60.0) + (seconds/3600.0)
    if prfx not in ["N", "E"]:
        crd_decimal *= -1
    return crd_decimal



