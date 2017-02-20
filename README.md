# improvisation
Interactive sound installation using OpenCV and Pure Data

A radio controlled model car can be driven across a wooden platform. A postcard with the image of
Malevich's Black Square is attached to the top of the car. A camera is suspended above the platform.
The camera is connected to a computer. Image recognition software keeps track of the location of
the square in relation to a triangular grid of 12 points. Each point of the grid is marked with a
musical note. A music generating program plays sounds that sound like plucked strings. The notes
that are played correspond to the three points that are closest to the current position of the square.
The frequency of the plucking of each note is relative to the distance of the car to the corresponding
point. This means the music can be changed by driving the car to another position.

In the grid the twelve notes of the octave are laid out in such a way that each triangle forms either a
major or a minor chord. This work is the latest in an occasional series of works that use this grid. 
Another work based on this grid is the [KHL4](https://github.com/muggezifter/khl4express/wiki/KHL4) project.

The image recognition software uses [OpenCV](http://opencv.org).

The sound instrument uses the _karpluck~_ abstraction from [Loomer](http://blog.loomer.co.uk/2010/02/karplus-strong-guitar-string-synthesis.html) and _gpan~_ from the [Pan](https://puredata.info/downloads/pan/?searchterm=pan) library.
