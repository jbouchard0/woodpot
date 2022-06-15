# Japanese Style 3D Printable Wooden Pots
Generate 3D printable Japanese style wooden pots as seen from the Shinjuku Gyoen in Tokyo with OpenSCAD and Python.

<img src="https://i.imgur.com/hPCAdFn.jpg" height="300"></img>
<img src="https://i.imgur.com/tW1HOD5l.png" height="300"></img>

# Getting Started
<img src="https://i.imgur.com/2a2gdpC.jpg" height="300"></img>
<img src="https://i.imgur.com/2jo0OhYl.png" height="300"></img>

In order to start generating your very own woodpots, you're going to need Python 3, SolidPython and OpenSCAD

In the woodpot.py file, using the Pot() class you can edit your woodpot to your desired specifications.

#### Example
```python
myPot = Pot(radius=20,height=30,wall_thickness=5,sides=4,layers=5)

myPot.exportModel('woodpot')
myPot.exportPieces('woodpot')
```
Here we've created a Pot and exported it in two different ways. 

Pot.exportModel() exports the entire model for 3D printing the model as a whole.
<p align="center">
<img src="https://i.imgur.com/xIB3wp2l.png"></img>
</p>

Pot.exportPieces() exports the model into its individual pieces/planks for CNC machining. 

<p align="center">
<img src="https://media.discordapp.net/attachments/140721676269780992/808934892917489664/unknown.png?width=719&height=453"></img>

<img src="https://media.discordapp.net/attachments/140721676269780992/808850803820331018/unknown.png?width=719&height=334">
</p>
<p align="center">
Example of what a 6 sided pot and a 4 sided pot would look like if it was setup for machining in Fusion 360 using Pot.exportPieces()
</p>


# Parameters
There were many different styles of wooden pots I saw at the Gyoen. So I had a ton of fun implementing parameters to mess around with all based on what I saw.
#### roundEdges
For creating a smoother finish akin to some of the varieties I saw at the gyoen.

By default roundEdges is set to false. Enabling it will change the model from:

<img src="https://i.imgur.com/ReatSBTl.png" width="300"></img>
```python
woodpot = Pot(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=False,overlap=1.0)
```

To this:

<img src="https://i.imgur.com/9AoT4lel.png" width="300"></img>
```python
woodpot = Pot(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=True,overlap=1.0)
```

#### leveledTop
For creating a more flatter lip around the pot by merging the last layer with the second last.

By default it's set to "False":

<img src="https://i.imgur.com/0mODMyZl.png" width="300"></img>
```python
woodpot = Pot(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=True,leveledTop=False,overlap=1.0)
```

Setting it to "True" would result in this:

<img src="https://i.imgur.com/X6Xci1Al.png" width="300"></img>
```python
woodpot = Pot(radius=20,height=30,wall_thickness=5,sides=6,layers=5,roundEdges=True,leveledTop=True,overlap=1.0)
```

# Implementation
Here are my results. I ended up using wood filament (30% wood, 70% PLA):

<img src="https://i.imgur.com/JZg4Sd4.jpg" width="250"></img>   <img src="https://i.imgur.com/F8l19BA.jpg" width="250"></img>   <img src="https://i.imgur.com/GcE4kJn.jpg" width="250"></img><img src="https://media.discordapp.net/attachments/140721676269780992/808853210273677312/IMG_20210209_161220.jpg?width=719&height=539" height="333"></img>


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
* The smooth 2.5hr train ride from Tokyo to Kyoto where I was able to write most of the code for this.
