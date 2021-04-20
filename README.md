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

sma = SMA("SMA(5) demo", 5)

print("   SMA   Slope Slope_Duration")
for x in range(-25,25):
    sma.CalculateNextMA(x**2)
    print(f"{sma.GetMA():>7.1f}", end="")
    print(f"{sma.GetMA_Slope():>6.1f}", end="")
    print(f"{sma.GetMA_SlopeDuration():>4}")
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

ema = EMA("EMA(5) demo", 5)

print("   EMA   Slope Slope_Duration")
for x in range(-25,25):
    ema.CalculateNextMA(x**2)
    print(f"{ema.GetMA():>7.1f}", end="")
    print(f"{ema.GetMA_Slope():>6.1f}", end="")
    print(f"{ema.GetMA_SlopeDuration():>4}")
```

### Requirements
- moving average classes require Python 3.x
- f-string in the examples require Python 3.6+


---
:scroll: [MIT License](README.license)

