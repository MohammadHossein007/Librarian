from . import jalali

def jalali_converter(time):
    jalali_time = jalali.Gregorian(time).persian_tuple()
    output = f'{jalali_time[0]}/{jalali_time[1]}/{jalali_time[2]}'
    return output