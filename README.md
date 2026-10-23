

**Created a self-driving car simulation in Webots R2025a, using Python.** 

**What the car does:**

1. Pedestrian aware: slows down to 20 **km/h** within 30 m of a zebra crossing, and completely stops if an obstacle is detected **in its lane** within 12 m in front, **such as a pedestrian on the crossing. It drives on once the lane has been clear for a second.**
2. Keeps its lane by following the yellow centre line.
3. Feedback control: **steers itself back towards the centre of its lane whenever it drifts.**
4. **Speed control: 30 km/h in the city, 20 km/h near crossings, 0 to stop.**
5. GPS and compass **navigation through places where yellow markings are absent.**

**How it works:**

1. Uses computer vision with OpenCV and NumPy: the camera on the vehicle takes a picture of the road and analyses it every 10 ms. OpenCV and NumPy then use HSV colour segmentation to identify the yellow **centre line** ahead.
2. The steering is turned in the required direction based on feedback **from the camera: the further the yellow line is from where it should be, the harder it steers (proportional control).**
3. Works on the standard sense > think > act loop, **repeated** every 10 ms (100 times in 1 second).
4. Lidar for obstacle detection, **counting only what is in the car's own lane.**
5. GPS **and compass** for navigating through **junctions,** where yellow markings are absent.

The project still needs major updates! The vehicle still cannot detect and react to traffic signals **or other cars**. Still working on it, but thought this was worth sharing!
