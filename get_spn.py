def get_spn(toponym):
    toponym_bounded = toponym['boundedBy']['Envelope']
    lower_corner = list(map(float, toponym_bounded['lowerCorner'].split(' ')))
    upper_corner = list(map(float, toponym_bounded['upperCorner'].split(' ')))
    delta_lat = str(abs(lower_corner[1] - upper_corner[1]))
    delta_long = str(abs(lower_corner[0] - upper_corner[0]))
    return delta_long, delta_lat
