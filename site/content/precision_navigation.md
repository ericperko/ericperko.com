+++
title = "Precision Navigation for Indoor Mobile Robots"
date = "2021-08-14"
tags = ["thesis", "mobile robots", "indoor navigation", "robotics", "motion planning", "precision navigation"]
+++

#### Source code: [ericperko/precision_navigation](https://github.com/ericperko/precision_navigation)

#### Thesis Latex source code: [ericperko/cwru_ms_thesis](https://github.com/ericperko/cwru_ms_thesis)

#### Thesis PDF version: [Precision Navigation for Indoor Mobile Robots](http://dl.dropbox.com/u/1970299/EricPerkoCwruMsThesis.pdf)

#### Thesis Defense Slides: [Precision Navigation for Indoor Mobile Robots](https://docs.google.com/presentation/d/1lY0TqNb_-ygW2uUKvOQE4UTBd5OgHlRafy4pJYUcWg4/edit)

**Abstract:**
This thesis describes a precision navigation system for indoor mobile robots, developed to address deficiencies in the ROS navigation stack when used for precision navigation. It includes a precision localization subsystem, based on a planar laser scanner, wheel encoders, a gyroscope and an *a priori* map, and a precision path execution system made up of a steering algorithm, a trajectory generator and a simplistic path planner. A 3D octree costmap based on the OctoMap library was also developed for collision detection. Geometric parameterizations for path segments were developed for use by those components. The precision navigation system was evaluated using a physical robot, CWRU's HARLIE, as well as in a Gazebo simulation. This precision navigation system allowed HARLIE to precisely navigate indoors, following paths made up of straight lines, constant curvature arcs and spin-in-place segments with as little as just over three centimeters of RMS lateral offset error.
