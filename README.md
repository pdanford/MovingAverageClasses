Python 3 Classes to Calculate Moving Averages Iteratively
-------------------------------------------------------------------------------
### Simple Moving Average
Computes Simple Moving Average iteratively by calling CalculateNextMA().

##### Initialization is a bit non-traditional:  
The SMA is initialized progressively using a sample window that grows
with each new value added until the window is the size the SMA instance
was created with. This is to provide a reasonable MA approximation during
initialization instead of returning 0s while the sample window is being
filled (i.e. shorter period averages are returned while the SMA is
collecting enough values to return the proper period SMA).

##### Example Use:
```
from MAs import SMA

sma = SMA("SMA_demo", 5)

print(f"{sma.GetLegend()}  Slope  Slope_Duration")
for x in range(-25,25):
    sma.CalculateNextMA(x**2)
    print(f"{sma.GetMA():>9.1f}", end="")
    print(f"{sma.GetMASlope():>12.1f}", end="")
    print(f"{sma.GetMASlopeDuration():>8}")
```

### Exponential Moving Average
Computes Exponential Moving Average iteratively by calling CalculateNextMA().

##### Initialization is a bit non-traditional:  
The EMA is initialized with the first value added to EMA - and will
converge in 4 or 5 iterations. This is to provide a reasonable MA
approximation during initialization instead of returning 0s.

##### Example Use:
```
from MAs import EMA

ema = EMA("EMA_demo", 5)

print(f"{ema.GetLegend()}  Slope  Slope_Duration")
for x in range(-25,25):
    ema.CalculateNextMA(x**2)
    print(f"{ema.GetMA():>9.1f}", end="")
    print(f"{ema.GetMASlope():>12.1f}", end="")
    print(f"{ema.GetMASlopeDuration():>8}")
```

### History
If `keep_history` is  True at instantiation, all calculated MA values and their slopes are kept and can be retrieved as a list with GetMAHistory() and GetMASlopeHistory(). Defaults to False to save memory for long-running use where a complete history is not needed.

### Requirements
- Python 3.6+

---

:scroll: [MIT License](README.license)

