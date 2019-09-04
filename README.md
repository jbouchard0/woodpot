# Japanese Style 3D Printable Wooden Pots
Generate 3D printable Japanese style wooden pots as seen from the Shinjuku Gyoen in Tokyo with OpenSCAD and Python.

<img src="https://i.imgur.com/hPCAdFn.jpg" height="300"></img>
<img src="https://i.imgur.com/tW1HOD5l.png" height="300"></img>

# Getting Started
<img src="https://i.imgur.com/2a2gdpC.jpg" height="300"></img>
<img src="https://i.imgur.com/2jo0OhYl.png" height="300"></img>

In order to start generating your very own woodpots, you're going to need Python 3, SolidPython and OpenSCAD

In the woodpot.py file, using the calcDimensions() function you can edit your woodpot to your desired properties

#### Example
```python
woodpot = calcDimensions(radius=20,height=30,wall_thickness=5,sides=4,layers=5)
```
Would generate a scad file named "woodpot.scad" with a 4 sides, a radius of 20mm, a height of 30mm, a plank/wall thickness of 5mm. Once opened in openscad, the pot should look like this:

![alt text](https://i.imgur.com/xIB3wp2l.png)

# Parameters
There were many different styles of wooden pots I saw at the Gyoen. So I had a ton of fun implementing parameters to mess around with all based on what I saw.
#### roundEdges
For creating a smoother finish akin to some of the varieties I saw at the gyoen.

By default roundEdges is set to false. Enabling it will change the model from:

<img src="https://i.imgur.com/ReatSBTl.png" width="300"></img>
```python
woodpot = calcDimensions(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=False,overlap=1.0)
```

To this:

<img src="https://i.imgur.com/9AoT4lel.png" width="300"></img>
```python
woodpot = calcDimensions(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=True,overlap=1.0)
```

#### leveledTop
For creating a more flatter lip around the pot by merging the last layer with the second last.

By default it's set to "False":

<img src="https://i.imgur.com/0mODMyZl.png" width="300"></img>
```python
woodpot = calcDimensions(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=True, leveledTop=False,overlap=1.0)
```

Setting it to "True" would result in this:

<img src="https://i.imgur.com/X6Xci1Al.png" width="300"></img>
```python
woodpot = calcDimensions(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=True, leveledTop=True,overlap=1.0)
```

# Implementation
Here are my results:

<img src="https://i.imgur.com/JZg4Sd4.jpg" width="250"></img>   <img src="https://i.imgur.com/F8l19BA.jpg" width="250"></img>   <img src="https://i.imgur.com/GcE4kJn.jpg" width="250"></img>

(1) Printing in progress. Using a roll of wood filament from amazon. Seller said it was 30% wood and 70% PLA. It semlls just like real wood as it prints.

(2) After removing all the supports, I started to apply the wood filler to any print imperfections I had. Totally not necessary, I just didnt have my print settings all dialled in for wood filament at the time.

(3) After a light wood stain. The stain looks a whole lot better in real life for some reason. Overall however, pretty happy with this project and what I ended up with.

# Known Bugs
When I originally wrote this code, I was one my way to Kyoto from Tokyo, about a 2.5 hour trip on the Shinkasen. I wasn't planning on releasing it as it was just for my own personal use to generated maybe 3 or 4 pots that I could print. Because of this, there are many bugs with this program that I will eventually work out.

* Floor generation code for pots with 8 or more sides isn't inline with the walls
* Large overlaps > 3 will often break the model
* 3 sided triangular shaped pots don't generate a proper floor
* Many more

As it is, I recommend that if you're going to use this program, stick to 4-8 sided pots and you won't have any issues.

## Built With

* [Python 3](https://www.python.org/downloads/)
* [SolidPython](https://github.com/SolidCode/SolidPython/)
* [OpenSCAD](https://www.openscad.org/)

## Authors

* **Justin Bouchard** - *Initial code* - [shamans10](https://github.com/shamans10/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thank you to SolidPython for their awesome library
* Shinjuku Gyoen and their handmade wooden pots that inspired me to make this.
* The smooth 2.5hr train ride from Tokyo to Kyoto
