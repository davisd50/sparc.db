from datetime import datetime, timedelta
from zope.interface import implements
from zope.component.factory import Factory
from sparc.db.report.interfaces import ITrendReportPeriod

class trendReportPeriod(object):
    """Iterator for time splits between begin/end given a set period
    
    Usage:
        >>> import datetime
        >>> begin = datetime.datetime(2015,1,1)
        >>> end   = datetime.datetime(2015,1,10)
        >>> period = 'day'
        >>> myPeriodIterator = trendReportPeriod(begin=begin,end=end,period=period)
        >>> myPeriodIterator.period
        'day'
        >>> mySplits = list(myPeriodIterator)
        >>> mySplits[0]
        (datetime.datetime(2015,1,1), datetime.datetime(2015,1,2))
        >>> mySplits[1]
        (datetime.datetime(2015,1,2), datetime.datetime(2015,1,3))
        >>> mySplits[9]
        (datetime.datetime(2015,1,9), datetime.datetime(2015,1,10))
    
    """
    implements(ITrendReportPeriod)
        
    def __init__(self, **kwargs):
        self._begin, self._end, self._period, self._label, self._cache = None, None, None, None, {'__iter__':{}, '_steps': {}} # initialize
        if 'begin' in kwargs: self.begin = kwargs['begin']
        if 'end' in kwargs: self.end = kwargs['end']
        if 'period' in kwargs: self.period = kwargs['period']
    
    @property
    def begin(self):
        return getattr(self, '_begin', None)
    @begin.setter
    def begin(self, begin):
        if begin and self._end and begin >= self._end:
            raise ValueError("expected begin datetime to be smaller than end datetime")
        if begin:
            self._begin = begin
    
    @property
    def end(self):
        return getattr(self, '_end', None)
    @end.setter
    def end(self, end):
        if end and self._begin and end <= self._begin:
            raise ValueError("expected end datetime to be larger than begin datetime")
        if end:
            self._end = end
    
    @property
    def period(self):
        return getattr(self, '_period', None)
    @period.setter
    def period(self, period):
        _allowed_strings = ['second', 'minute', 'hour', 'day', 'week', 'month', 'year']
        if isinstance(period, timedelta):
            self._period = period
        else:
            if not period in _allowed_strings:
                raise LookupError("Expected period to be valid string in %s, got: %s", str(_allowed_strings), str(period))
            self._period = period
    
    @property
    def label(self):
        _label = self._label
        if not _label:
            # timedeltas use simple numeric incrementer starting a 1
            if isinstance(self.period, timedelta): # 1, 2, 3...
                _label = lambda start, stop: str(self._steps().index((start, stop)) + 1)
            else:
                if self.period == 'second': _format = '%H:%M:%S' # HH:MM:SS
                if self.period == 'minute': _format = '%H:%M' # HH:MM
                if self.period == 'hour':  _format = '%m - %b %d, %H:%M' # XX - Mon DD, HH:MM (XX is zero-padded month number)
                if self.period == 'day': _format = '%m - %b %d %Y' # XX - Mon DD YYYY (XX is zero-padded month number)
                if self.period == 'week': _format = '%w - %a, %b %d %Y' # X - WDay, Mon DD YYYY (X is 0-6 weekday number, 0 is Sun)
                if self.period == 'month': _format = '%m - %b %Y' # XX - Mon YYYY (XX is zero-padded month number)
                if self.period == 'year': _format = '%Y' # YYYY
                _label = lambda start, stop: start.strftime(_format)
            
        return _label
    
    @label.setter
    def label(self, label):
        """label should be a callable with footprint label(start,stop)"""
        label(datetime(2013,1,1), datetime(2014,1,1), 'month') # simple test...can label be called?
        self._label = label
    
    def _steps(self):
        if (self._begin, self._end, self.period) in self._cache['_steps']:
            return self._cache['_steps'][(self._begin, self._end, self.period)]
        _steps = []
        progress = self.begin
        while progress < self.end:
            _next = self._getNextStep(progress)
            _steps.append((progress, _next))
            progress = _next
        self._cache['_steps'][(self._begin, self._end, self.period)] = _steps
        return _steps
    
    def __len__(self):
        return len(list(self.__iter__()))
    
    def __iter__(self):
        if (self._begin, self._end, self.period) in self._cache['__iter__']:
            return iter(self._cache['__iter__'][(self._begin, self._end, self.period)])
        
        if not self.begin or not self.end or not self.period:
            return iter([])
        _iter = []
        for _begin, _end in self._steps():
            _label = self.label(_begin, _end)
            _iter.append((_begin, _end, _label))
        self._cache['__iter__'][(self._begin, self._end, self.period)] = _iter
        """
        progress = self.begin
        while progress < self.end:
            _next = self._getNextStep(progress)
            _label = self.label(progress, _next)
            _iter.append((progress, _next, _label))
            progress = _next
        self._cache[(self._begin, self._end, self.period)] = _iter
        """
        return iter(_iter)
    
    def _getNextStep(self, progress):
        if not self.begin or not self.end or not self.period:
            return None
        if isinstance(self.period, timedelta):
            _next = progress + self.period
            return _next if _next < self.end else self.end
        
        # normalize the _start based on progress.  This insures next step
        # will land on our desired period increments.
        _start = {'year':progress.year, 'month':progress.month, 'day':progress.day, 'hour':progress.hour, 'minute':progress.minute, 'second':progress.second}
        for _period in ['second', 'minute', 'hour', 'week', 'day', 'month', 'year']: # week is before day intentionally...order matters
            if _period == self.period:
                if self.period in ['second', 'minute', 'hour', 'day', 'week']:
                    _delta = timedelta(**{self.period + 's': 1})
                    if self.period == 'week':
                        _delta_days = 7 - (progress.weekday() % 7) # diff days between next Monday and progress
                        _delta = timedelta(**{'days': _delta_days})
                    _next = datetime(**_start) + _delta
                    return _next if _next < self.end else self.end
                else: # 'month', 'year' are a little tougher
                    if self.period == 'year':
                        _start['year'] += 1
                        _next = datetime(**_start)
                        return _next if _next < self.end else self.end
                    else: # month
                        _start['month'] += 1
                        if _start['month'] <= 12:
                            _next = datetime(**_start)
                        else:
                            _start['month'] = 1
                            _start['year'] += 1
                            _next = datetime(**_start)
                        return _next if _next < self.end else self.end
            else:
                if _period in ['second', 'minute', 'hour']:
                    del _start[_period]
                if _period in ['month','year']:
                    _start['day'] = 1;
                if _period in ['year']:
                    _start['month'] = 1;
            
trendReportPeriodFactory = Factory(trendReportPeriod)
        
            