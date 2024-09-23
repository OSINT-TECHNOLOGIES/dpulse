import socket

def time_processing(end):
    if end < 60:
        endtime = round(end)
        endtime_string = f'approximately {endtime} seconds'
    else:
        time_minutes = round(end / 60)
        if time_minutes == 1:
            endtime_string = f'approximately {time_minutes} minute'
        else:
            endtime_string = f'approximately {time_minutes} minutes'
    return endtime_string

def domain_precheck(domain):
    try:
        socket.create_connection((domain, 80), timeout=5)
        return True
    except OSError:
        return False