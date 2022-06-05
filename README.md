# Correlation Map building

[![Generic badge](https://img.shields.io/badge/version-1.0.0-green.svg)](https://shields.io/)

Correlation Map - project with a GUI for creating correlation maps of two digital images.

### Image preprocessing:
Before building correlation map, the program may:
- Cut out part of the source image to search in the image for comparing
- Rotate the second image relative to the first
- Find a smaller first in the second using correlation

For example, let's take these two images. They have a different position, and 
rotated, on the second there is a difference

![Arduinos before image preprocessing](/.readme_images/arduinos.png)

After preprocessing, we get two images with the same orientation

![Arduinos after image preprocessing](/.readme_images/arduinos_after_preprocessor.png)


### Process:
The program divides the two images into identical pieces of the size that was 
set. Further, for these two pieces, the correlation is calculated and a build 
3D plot, the correlation map.

Correlation map for arduinos after image preprocessing using normed covariant and n = 20

![Correlation map for arduinos after image preprocessing](/.readme_images/cm_cov_20_view.png)

Correlation map helps locate image defects

![Zoomed arduinos](/.readme_images/zoomed_arduinos.png)

Correlation map for space images using normed Pirson and n = 2

![Space images](/.readme_images/space.png)
![Correlation map for space images](/.readme_images/cm_pirson_2.png)

# Author
Made by:
Andrey Zaneuski (@Gliger13), Belarus
As diploma work for Belarusian State University faculty of Radiophysics and Computer Technology
