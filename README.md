# MovieBarcode with Python 3 and OpenCV 3.4
Create a MovieBarcode for any video file. It generates a colored bar by picking the most dominant color for every second of the video file

## Example
![Westworld S02E01](https://raw.githubusercontent.com/primus852/python-movie-barcode/master/pmb/result/westworld_s02e01.jpg)
*Westworld Season 02 - Episode 01*

## Installation
- Clone the repository, go to folder
- First install SciPy: `sudo apt install python-scipy`
- Run `pip install -r requirements.txt`
- Install OpenCV Python
  - Ubuntu: `sudo apt install python-opencv`
  - Windows: https://www.codeprimus.de/opencv-python3-a-love-story-based-on-windows-10/

## Rendering time
- ~~The above image took about 3 hours with an i5 and four cores~~
- Changed the `KMean` Algorithm to `MiniBatchKMeans` and got it down to 1 hour 20 mins. 

### Bugs
- When running daemonized on windows, there is an error with arguments in "" or ''
