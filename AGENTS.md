数据集说明页: https://github.com/UCF-SST-Lab/UCF-SST-CitySim1-Dataset/wiki

Trajectory
The UCF SST CitySim dataset contains vehicle trajectories captured using drone videos. The videos were captured at 30 frames per second. Each row in the trajectory dataset represents a vehicle waypoint at a single frame in the video. Additionally, the dataset describes the rotation-aware vehicle bounding box in each row.

The following table describes the trajectory CSV columns and states their respective units.

Name	Description	Unit
frameNum	Frame number of the vehicle waypoint captured at 30 frames per second	-
carId	Vehicle unique identifier that remains consistent for all vehicle waypoints across the entire video	-
carCenterX	Pixel x-coordinate of vehicle bounding box center point	Pixel
carCenterY	Pixel y-coordinate of vehicle bounding box center point	Pixel
headX	Pixel x-coordinate of vehicle bounding box front center point	Pixel
headY	Pixel y-coordinate of vehicle bounding box front center point	Pixel
tailX	Pixel x-coordinate of vehicle bounding box rear center point	Pixel
tailY	Pixel y-coordinate of vehicle bounding box rear center point	Pixel
boundingBox1X	Pixel x-coordinate of vehicle bounding box vertex 1	Pixel
boundingBox1Y	Pixel y-coordinate of vehicle bounding box vertex 1	Pixel
boundingBox2X	Pixel x-coordinate of vehicle bounding box vertex 2	Pixel
boundingBox2Y	Pixel y-coordinate of vehicle bounding box vertex 2	Pixel
boundingBox3X	Pixel x-coordinate of vehicle bounding box vertex 3	Pixel
boundingBox3Y	Pixel y-coordinate of vehicle bounding box vertex 3	Pixel
boundingBox4X	Pixel x-coordinate of vehicle bounding box vertex 4	Pixel
boundingBox4Y	Pixel y-coordinate of vehicle bounding box vertex 4	Pixel
carCenterXft	X-coordinate of vehicle bounding box center point in feet	Feet
carCenterYft	Y-coordinate of vehicle bounding box center point in feet	Feet
headXft	X-coordinate of vehicle bounding box front center point in feet	Feet
headYft	Y-coordinate of vehicle bounding box front center point in feet	Feet
tailXft	X-coordinate of vehicle bounding box rear center point in feet	Feet
tailYft	Y-coordinate of vehicle bounding box rear center point in feet	Feet
boundingBox1Xft	X -coordinate of vehicle bounding box vertex 1 in feet	Feet
boundingBox1Yft	Y -coordinate of vehicle bounding box vertex 1 in feet	Feet
boundingBox2Xft	X -coordinate of vehicle bounding box vertex 2 in feet	Feet
boundingBox2Yft	Y -coordinate of vehicle bounding box vertex 2 in feet	Feet
boundingBox3Xft	X -coordinate of vehicle bounding box vertex 3 in feet	Feet
boundingBox3Yft	Y -coordinate of vehicle bounding box vertex 3 in feet	Feet
boundingBox4Xft	X-coordinate of vehicle bounding box vertex 4 in feet	Feet
boundingBox4Yft	Y -coordinate of vehicle bounding box vertex 4 in feet	Feet
carCenterLat*	Global latitude of vehicle bounding box center point	Degrees
carCenterLon*	Global longitude of vehicle bounding box center point	Degrees
headLat*	Global latitude of vehicle bounding box front center point	Degrees
headLon*	Global longitude of vehicle bounding box front center point	Degrees
tailLat*	Global latitude of vehicle bounding box rear center point	Degrees
tailLon*	Global longitude of vehicle bounding box rear center point	Degrees
boundingBox1Lat*	Global latitude of vehicle bounding box vertex 1	Degrees
boundingBox1Lon*	Global longitude of vehicle bounding box vertex 1	Degrees
boundingBox2Lat*	Global latitude of vehicle bounding box vertex 1	Degrees
boundingBox2Lon*	Global longitude of vehicle bounding box vertex 1	Degrees
boundingBox3Lat*	Global latitude of vehicle bounding box vertex 1	Degrees
boundingBox3Lon*	Global longitude of vehicle bounding box vertex 1	Degrees
boundingBox4Lat*	Global latitude of vehicle bounding box vertex 1	Degrees
boundingBox4Lon*	Global longitude of vehicle bounding box vertex 1	Degrees
speed	Vehicle waypoint speed	Miles per Hour
heading	Vehicle waypoint heading relative to the global North	Degrees
course	Vehicle waypoint heading relative to the image coordinate X-axis	Degrees
laneId	Waypoint lane number according to the supplementary lane map	-
*Only provided for US-based locations

Vehicle Point Features
The vehicle center, head, tail, and bounding box vertices locations are described in figure below.

Bounding box point 1 describes the front right vehicle corner
Bounding box point 2 describes the rear right vehicle corner
Bounding box point 3 describes the rear left vehicle corner
Bounding box point 4 describes the front left vehicle corner