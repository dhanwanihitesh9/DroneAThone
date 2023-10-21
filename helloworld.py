import numpy as np

# Define two coordinates
x = 3.0
y = 4.0

# Calculate the arctangent (angle) between the two coordinates
angle = np.arctan2(y, x)

# Calculate the cosine of the angle
cosine = np.cos(angle)

print("Angle (radians):", angle)
print("Angle (degrees):", np.degrees(angle))
print("Cosine of the angle:", cosine)