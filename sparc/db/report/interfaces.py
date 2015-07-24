from zope.interface import Interface, Attribute

class IReportDates(Interface):
    begin = Attribute("Beginning datetime object of report metrics")
    end = Attribute("Ending datetime object of report metrics")

class IReportPublishInfo(Interface):
    name = Attribute("Report name")
    date = Attribute("datetime object of when report was generated")

class IReportCard(IReportDates, IReportPublishInfo):
    """A basic report card
    
    A report card is intended to act as a basic container for reports.  It
    provides a mechanism to gather reports into a logical group.
    """

class IReport(IReportDates, IReportPublishInfo):
    """A basic report
    
    A report is a collection of metrics based on a set of series vs. categories.
    A basic report might look like this:
    
    Example:
                          CATEGORIES
        SERIES | a basic category | another category
        ============================================
        set 1  |        12        |       8
        set 2  |        23        |       16
        set 3  |        220       |       134
        set 4  |        58        |       789
        
    """
    def categories():
        """Return list of categories to be applied to each series (think x)"""
    def series():
        """Return list of individual series to be reported on (think y)"""
    def metric(series, category):
        """Return value for the given metric"""

class ICulmulativeReport(IReport):
    """Report whose unique data points are included exclusively within a single metric.
    
    Example:
                          CATEGORIES
        SERIES        | Internal | External      Sum       Percentage
        ===================================
        Restricted    |   12     |   8           20           1.6
        Confidential  |   23     |   16          39           3.1
        Internal      |   220    |   134         354          28.1
        Public        |   58     |   789         847          67.2
        
        Sum               313        947         1260
        Percentage        24.8       75.2                     100
        
        This report classifies a file based on data sensitivity and location.  
        Each file can only be counted towards a unique/single cell.  If
        we added all the cells together, it would give the total number
        of files included in the report.
    """
    def sum(series = '', category = ''):
        """Return a integer series, category or complete cumulative total number"""
    def percentage(precision = 0, series = '', category = ''):
        """Return float percentage of series/category vs. all other series/categories"""

class ITrendReport(IReport):
    """Report on a set of metrics measured in discrete periods over time
    
    period starts are inclusive, while stops are exclusive (for report)
    """
    period = Attribute("Callable implementing ITrendReportPeriod")

class ITrendReportPeriod(IReportDates):
    """Divide begin/end dates into iterable of tuples of period length
    
    If period is a string, then individual periods will begin/end on midnight 
    (except for bookends which are defined by begin/end properties of the 
    object).  If period is a timedelta, then begin will act as the baseline for 
    all increments which are period in length, except for the end bookend.
    """
    period = Attribute("Valid period string [second, minute, hour, day, week, month, year] or Python timedelta")
    label = Attribute("Callable that accepts (start, stop) and returns a String series (y-axis) label")
    def __len__():
        """Return integer number of increments for the current period setting"""
    def __iter__():
        """Return tuple with begin/end/label (datetime/datetime/string) for each available increment"""