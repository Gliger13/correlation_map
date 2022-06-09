# Correlation Map builder

[![Generic badge](https://img.shields.io/badge/version-1.0.0-green.svg)](https://shields.io/)

## Content

- [Purpose](#purpose)
- [Algorithm](#algorithm)
  - [Images preprocessing](#images-preprocessing)
  - [Correlation Map building](#correlation-map-building)
- [Installation and Launch](#installation-and-launch)
  - [Linux](#linux)
  - [Windows](#windows)
- [Author](#author)
- [License](#license)

## Purpose

Project with a GUI for:
- Preparing digital images for correlation map building
- Creating correlation map of digital images
- Images and correlation map investigations

## Algorithm

To build correlation map we have to prepare digital images. Images requirements:
- same size
- one color chanel
- not rotated relative to each other
- not offset relative to each other
- not scaled relative to each other
- not titled relative to each other
To meet image requirements we use images preprocessing.


### Images preprocessing

The program may:
- Cut out part of the source image to search in the image for comparing
- Rotate the second image relative to the first
- Find a smaller first in the template using chosen correlation and cut
- Present images on a gray scale of intensity

For example, let's take these two images. They have a different position, and 
rotated, on the second there is a difference.

![Arduinos before image preprocessing](/.readme_images/arduinos.png)

After preprocessing, we get two images with the same orientation:

![Arduinos after image preprocessing](/.readme_images/arduinos_after_preprocessor.png)


### Correlation Map building

Divides the two images into identical pieces with the same size. Further, for 
these two pieces, the correlation is calculated and a build 3D plot, the 
correlation map.

Correlation map for Arduinos after image preprocessing using normed covariant and n = 20:

![Correlation map for arduinos after image preprocessing](/.readme_images/cm_cov_20_view.png)

Correlation map helps locate image defects:

![Zoomed arduinos](/.readme_images/zoomed_arduinos.png)

Correlation map for space images using normed Pirson and n = 2

![Space images](/.readme_images/space.png)
![Correlation map for space images](/.readme_images/cm_pirson_2.png)

## Installation and launch

### Linux

1) Clone source code
```bash
git clone https://github.com/Gliger13/correlation_map
```
2) Change current folder to cloned repository
```bash
cd correlation_map
```
3) Create new python virtual environment using Python version >= 3.10
```bash
python3.10 -m venv venv
```
4) Source created virtual environment
```bash
source venv/bin/activate 
```
5) Run setup.py file
```bash
pip install . 
```
6) To launch application run
```bash
MODE=PROD python app.py
```

### Windows

Almost the same process as for Linux or use executable file from [google disk](https://drive.google.com/drive/folders/1XLeWemZJwq4woI-49Tx2lUP7Tc8DpFuL?usp=sharing)

## Author

Made by Andrey Zaneuski (@Gliger13), Belarus
As diploma work for Belarusian State University, faculty of Radiophysics and Computer Technology

## License

[**GNUv3**](LICENSE)
