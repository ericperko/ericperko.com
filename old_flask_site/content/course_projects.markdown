A collection of miscellaneous course projects that were geared towards applications in robotics.

#### [Real-time Object Detection for IGVC](http://dl.dropbox.com/u/1970299/EricPerkoObsDetection.pdf) for EECS 600 Machine Learning, Fall 2009

**Abstract:**
Detection of arbitrary objects in images is a difficult task, made even more so by the real-time
detection requirements of a robot designed to compete in the IGVC. For a robot in this competition,
objects need to be classified in real-time so that obstacles can be found and avoided before a collision
occurs. In order to evaluate a possible solution to this problem, I evaluated the performance of a Viola-
Jones object detector implemented in OpenCV and an extension of that framework to the Multiple
Instance Learning setting. I hypothesized that the Viola-Jones detector would achieve moderately good
detection rates on my sample data and that the MIL variant would improve these rates. In order to test
this, I trained and evaluated these algorithms on logged data from IGVC '09 and attempted to detect
orange barrels, A-frames and white lines painted on grass. From these tests, I found that the
performance of the Viola-Jones detector was actually very poor on this data set, most likely due to the
feature representation used.

#### [EKF SLAM Implementation and Estimation Evaluation](http://dl.dropbox.com/u/1970299/EricPerkoSLAM.pdf) for EECS 491 Artificial Intelligence, Spring 2009

**Abstract:**
I implemented an algorithm to solve the online simultaneous localization and
mapping (SLAM) problem using an extended Kalman filter (EKF). SLAM is an
interesting problem in robotics that is made up of two much simpler problems - if you
know where all of the landmarks are, you can decrease error in the robot pose odometry
and if you know the robot pose, you can reduce the error in landmark positions from
sensor data. The difficulty arises when neither the landmark positions nor the pose are
known exactly and you wish to get both a good estimate of the current pose and the
locations of all the landmarks at the same time – hence the name simultaneous
localization and mapping. In order to evaluate the performance of this algorithm, I varied
the total number of landmarks, the noisiness of the simulated sensor data and the number
of times that the simulated robot looped through the map and compared the estimated
locations of all landmarks with their actual locations. I observed that EKF SLAM is very
sensitive to variance in the sensor data and that the number of loop iterations does not
influence the time taken to converge to landmark errors with low errors. The key was the
number of landmark re-observations – two re-observations seemed to be the magic
number for the parameters that I tested.
