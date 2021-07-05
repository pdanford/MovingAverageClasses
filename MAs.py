# version 2.1.0
# requires Python 3.x
# pdanford - April 2021
# MIT License

from collections import deque

class MA:
    """
    base class for specific moving averages (e.g. SMA, EMA)

    actual calculation of MA types should be done in derived classes'
    CalculateNextMA() function
    """

    def __init__(self, legend, ma_period, keep_history):
        """
        legend - a string used to uniquely identify a moving average instance's
        name/purpose

        keep_history - if True, all calculated MA values are kept and can be
        retrieved with GetMAHistory(). Set to False to save memory for
        long-running use where a complete history is not needed.
        """
        self.legend = legend
        self.ma_period = ma_period
        self.keep_history = keep_history

        self.init = True
        self.ma = 0
        self.prev_ma = 0
        self.slope = 0
        self.prev_slope = 0
        self.slope_duration = 0
        self.MA_type = ''
        self.MA_history = []
        self.MA_slope_history = []

    def GetLegend(self):
        """
        returns legend string this instance was created with
        """
        return self.legend

    def GetMAType(self):
        """
        returns string indicating what kind of MA this instance is
        (e.g. SMA or EMA)
        """
        return self.MA_type

    def GetPeriod(self):
        """
        returns MA period for this MA instance
        """
        return self.ma_period

    def GetMA(self):
        """
        returns current calculated MA as of last CalculateNextMA() call
        (this is the same value returned by the last CalculateNextMA() call)
        """
        return self.ma

    def GetMAHistory(self):
        """
        returns all MAs calculated since start as a list
        """
        return self.MA_history

    def GetMA_Slope(self):
        """
        return slope computed from last 2 values of calculated MA
        """
        return self.slope

    def GetMA_SlopeHistory(self):
        """
        returns all MA slopes calculated since start as a list
        """
        return self.MA_slope_history

    def GetMA_SlopeDuration(self):
        """
        returns number of values added by CalculateNextMA() that have had
        the same sign of slope
        """
        return self.slope_duration

    def CalculateNextMA_Slope(self):
        """
        calculates the current slope of the moving average as of last
        CalculateNextMA() call

        this is called by derived classes only at the end of their
        CalculateNextMA() (note that self.prev_ma = self.ma must be done at
        the top of the derived class's CalculateNextMA() also)
        """
        self.prev_slope = self.slope

        x2 = 1
        x1 = 0
        y1 = self.prev_ma
        y2 = self.ma
        self.slope =  (y2 - y1)/(x2 - x1)

        if self.slope * self.prev_slope < 0:
            # sign changed
            self.slope_duration = 1
        else:
            self.slope_duration += 1

        # -- update running history --
        if self.keep_history:
            self.MA_slope_history.append(self.slope)

## ----------------------------------------------------------------------------

class SMA(MA):
    """
    Simple Moving Average

    Computes Simple Moving Average iteratively by calling CalculateNextMA().

    Note: initialization is a bit non-traditional:
    The SMA is initialized progressively using a sample window that grows
    with each new value added until the window is the size the SMA instance
    was created with. This is to provide a reasonable MA approximation during
    initialization instead of returning 0s while the sample window is being
    filled (i.e. shorter period averages are returned while the SMA is
    collecting enough values to return the proper period SMA).
    """

    def __init__(self, legend, ma_period, keep_history = False):
        super().__init__(legend, ma_period, keep_history)
        self.MA_type = 'SMA'
        self.sample_window = deque(maxlen = ma_period)

    def CalculateNextMA(self, new_val):
        """
        Compute Simple Moving Average iteratively

        This uses a progressive formula to build up (i.e. initialize) the SMA
        until enough new values are added to make sample window size match
        ma_period and return the proper period SMA.
        """
        # update for next CalculateNextMA_Slope()
        self.prev_ma = self.ma

        if len(self.sample_window) < self.ma_period:
            # -- progressively establish new sma --
            # (i.e. use a progressive formula until we have ma_period samples)

            # add new value to sample window
            self.sample_window.append(new_val)
            # combine new value (while adjusting for sample size increasing)
            self.ma = self.ma + 1/len(self.sample_window) * (new_val - self.ma)

            if self.init:
                # so slope starts at 0
                self.prev_ma = self.ma
                self.init = False
        else:
            # -- update established SMA --
            # add new value to sma average
            self.ma += (new_val / self.ma_period)
            # subtract leftmost value of sample window from sma
            self.ma -= (self.sample_window[0] / self.ma_period)
            # add new value to sample window
            self.sample_window.append(new_val)

        # -- update slope based on this MA --
        super().CalculateNextMA_Slope()

        # -- update running history --
        if self.keep_history:
            self.MA_history.append(self.ma)

        return self.ma

## ----------------------------------------------------------------------------

class EMA(MA):
    """
    Exponential Moving Average

    Computes Exponential Moving Average iteratively by calling
    CalculateNextMA().

    Note: initialization is a bit non-traditional:
    The EMA is initialized with the first value added to EMA - and will
    converge in 4 or 5 iterations. This is to provide a reasonable MA
    approximation during initialization instead of returning 0s.
    """
    def __init__(self, legend, ma_period, keep_history = False):
        super().__init__(legend, ma_period, keep_history)
        self.MA_type = 'EMA'
        self.alpha = 2/(ma_period + 1)

    def CalculateNextMA(self, new_val):
        """
        Compute Exponential iteratively
        """
        # update for next CalculateNextMA_Slope()
        self.prev_ma = self.ma

        if self.init:
            # initialize with first value added to EMA
            # (EMA will converge in 4 or 5 iterations)
            self.ma = new_val
            # so slope starts at 0
            self.prev_ma = self.ma
            self.init = False
        else:
            self.ma = self.alpha * new_val + (1 - self.alpha) * self.ma

        # -- update slope based on this MA --
        super().CalculateNextMA_Slope()

        # -- update running history --
        if self.keep_history:
            self.MA_history.append(self.ma)

        return self.ma

