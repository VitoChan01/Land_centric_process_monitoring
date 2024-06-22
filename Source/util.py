import sys
def case_selection(cmdin):
    if cmdin=='ID':
        Case='Idaho'
    elif cmdin=='CO':
        Case='Colorado'
    elif cmdin=='ND':
        Case='NorthDakota'
    elif cmdin=='WA':
        Case='Washington'
    elif cmdin=='WI':
        Case='Wisconsin'

    else:
        Case='All'
    return Case