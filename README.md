# bHaptics Python Library
## Prerequisite
* bHaptics Player has to be installed (Windows)
   * The app can be found in
   bHaptics webpage: [http://www.bhaptics.com](http://bhaptics.com/)
* To play predefined haptic patterns [bHaptics Designer](https://designer1.bhaptics.com/)
## Quick Start

```python
from bhaptics import better_haptic_player as player
from bhaptics.better_haptic_player import BhapticsPosition
from time import sleep

# Initialize the haptic player
player.initialize()

# Register tact files (exported from bHaptics Designer - https://designer1.bhaptics.com/)
player.register("CenterX", "CenterX.tact")
player.register("Circle", "Circle.tact")

# Play a registered pattern
player.submit_registered("CenterX")

# Play with options (rotation, intensity)
player.submit_registered_with_option("Circle", "alt",
                                    scale_option={"intensity": 1, "duration": 1},
                                    rotation_option={"offsetAngleX": 180, "offsetY": 0})
```

## Core Functions

### Initialization

```python
player.initialize()
```

### Pattern Registration

```python
# Register tact files (exported from bHaptics Designer)
player.register("effect_name", "effect_file.tact")
```

### Playing Effects

```python
# Play a registered effect
player.submit_registered("effect_name")

# Play with options (alternate key, scale, rotation)
player.submit_registered_with_option("effect_name", "alternate_key",
                                    scale_option={"intensity": 1, "duration": 1},
                                    rotation_option={"offsetAngleX": 180, "offsetY": 0})

## Direct Device Control

### Submit Dot Pattern

Play haptic feedback by specifying dot indices:

```python
# Play pattern on vest back (dots are indexed 0-19)
player.submit_dot("feedback_id", BhapticsPosition.VestBack.value, 
                 [{"index": 0, "intensity": 100}], duration_millis=100)
```

## Direct Device Control

### Submit Dot Pattern

Play haptic feedback by specifying dot indices:

```python
# Play pattern on vest back (dots are indexed 0-19)
player.submit_dot("feedback_id", BhapticsPosition.VestBack.value, 
                 [{"index": 0, "intensity": 100}], duration_millis=100)
```

### Submit Path Pattern

Play haptic feedback by specifying exact positions:

```python
# Path on the vest front using coordinates (x, y from 0-1)
player.submit_path("feedback_id", BhapticsPosition.VestFront.value, [
    {"x": 0.5, "y": 0.5, "intensity": 100},  # Center
    {"x": 0.7, "y": 0.7, "intensity": 100},  # Upper right
], duration_millis=1000)
```

## Device Positions

The library supports the following device positions:

- `BhapticsPosition.Vest`
- `BhapticsPosition.VestFront`
- `BhapticsPosition.VestBack`
- `BhapticsPosition.ForearmL`
- `BhapticsPosition.ForearmR`
- `BhapticsPosition.GloveL`
- `BhapticsPosition.GloveR`


## Dependencies
* websocket-client

