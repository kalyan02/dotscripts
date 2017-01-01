# dotscripts

Tools and Scripts that I use to make life easier. This repo is called dotscripts because I place these in `~/.scripts` folder and set my `$PATH` to include this.

## resize.py

Script resizes JPG files to be super compact using python PIL library

     ~$ ./resize.py -h
    Usage: resize.py [options]

    Options:
      -h, --help            show this help message and exit
      -o OUTPUT, --output=OUTPUT
      -s SIZE, --size=SIZE  
      -i IE, --ignore-existing=IE

Example Usage:

     ~$ resize.py -s 1600 -o r/ *.jpg

## combine.py

A python script to combine 2 or more photos into a single one and place them side by side, resizing them proportionally to be of same height.

     ~$ ./combine.py -h
    Usage: combine.py [options]

    Options:
      -h, --help            show this help message and exit
      -o OUTPUT, --output=OUTPUT
      -s SIZE, --size=SIZE  
      -d, --debug           
      -m, --move            
      -r, --reverse         

Example Usage:

     ~$ combine.py -s 1600 -o r/ 20161218-IMG_2414.jpg 20161218-IMG_2418.jpg -r

Example Output:

![link](http://blog.fuss.in/wp/wp-content/uploads/2016/12/img_857_1_5.jpg)

## requirements

- Python 2.x
- PIL - Python Imaging Library
  
        pip install pillow
      
  Note: `pillow` is the package name. `pil`/`image` packages are depricated.
  
## License

  BSD