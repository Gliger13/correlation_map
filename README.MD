# Correlation Map

Correlation Map - project with a GUI for creating correlation maps of two images.

### Preprocess:
Before building a map, the program may:
- Cut out part of the first image to search in the second
- Rotate the second image relative to the first
- Find a smaller first in the second using correlation

### Process:
The program divides the two images into identical pieces of the size that was set. Further, for these two pieces, the correlation is calculated and a build 3D plot, the correlation map.

#### Available types of correlation:
- SQDIFF - square difference
- SQDIFF_NORMED - square diffrenece normed
- CCORR - covariance
- CCORR_NORMED - covariance normed
- CCOEFF - correlation coefficient Pirson
- CCOEFF_NORMED - correlation coefficient Pirson normed

# Author
Made by:
Andrey Zanevskiy (@Gliger13), Belarus
As course work for Belarusian State University faculty of Radiophysics and Computer Technology
