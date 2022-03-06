# pano2equi360
Convert 360 degree panoramic photos to equirectangular 360 photos 

This is another one of script I created to convert the one pano photo I had to a 360 equirectangular image

Edit this line to set the width and height of your output

fbo = ctx.simple_framebuffer((4096,2048))

The first value is the width, second the height.

A requirement.txt file is included so you can build a python environment using pip install -r requirements.txt

to run use

python3 pano2equi360.py input_image output_image
