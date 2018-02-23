
# .............................................................................
def TimeScaleTitle(range):
    range = range / 60
    if range <= 120:
        return '{} minutes'.format(int(range))
    
    range = range / 60
    if range <= 48:
        return '{} hours'.format(int(range))
    
    range = range / 24
    if range <= 7:
        return '{} days'.format(int(range))
    
    range = range / 7
    return '{} weeks'.format(int(range))
