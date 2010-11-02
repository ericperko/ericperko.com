## Part 1: Basic Graphics

The first version of our Asteroids clone will simply show a score of zero, a label showing the name of the program, three randomly placed asteroids, and the player's ship. Nothing will move.

### Setting Up

#### Installing Pyglet

Download pyglet from http://pyglet.org/download.html and choose the distribution for your platform. The process is different for each platform, but simple on all of them, since pyglet has no external dependencies.

#### Setting Up the Files

Since I wrote this example in stages, I'm putting the folder with the images, called 'resources,' outside the example folders. Each example folder contains a Python file called asteroid.py which runs the game, as well as a game module which contains most of the functionality. Your folder structure should look like this:

    mygame/
        resources/
            (images go here)
        version1/
            asteroids.py
            game/
                __init__.py

#### Getting a Window

To set up a window, simply import pyglet, create a new instance of pyglet.window.Window, and call pyglet.app.run().

    import pyglet
    game_window = pyglet.window.Window(800, 600)

    if __name__ == '__main__':
        pyglet.app.run()

When you run the code above, you should see a window full of junk that goes away when you press Esc.

#### Loading and Displaying an Image

Let's create a separate submodule of game to hold resources, calling it resources.py.

Since our images reside in a directory other than the example's root directory, we need to tell pyglet where to find them:

    import pyglet
    pyglet.resource.path = ['../resources']
    pyglet.resource.reindex()

The resource path starts with '../' because the resources folder is on the same level as the version1 folder. If we left it off, pyglet would look inside version1 for the resources folder.

Now that pyglet's resource module is initialized, we can easily load the images:

    player_image = pyglet.resource.image("player.png")
    bullet_image = pyglet.resource.image("bullet.png")
    asteroid_image = pyglet.resource.image("asteroid.png")

#### Centering the Images

Pyglet will draw all images from their lower left corner by default. We don't want this behavior for our images, which need to rotate around their centers. All we have to do to fix this problem is set their anchor points:

    def center_image(image):
        """Sets an image's anchor point to its center"""
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2

Now we can just call center_image() on all our loaded images:

    center_image(player_image)
    center_image(bullet_image)
    center_image(asteroid_image)

Remember that the center_image() function must be defined before it can be called at the module level. Also, note that zero degrees points directly to the right in pyglet, so the images are all drawn with their front pointing to the right.

To access the images from asteroids.py, we need to use something like from game import resources, which we'll get into in the next section.

### Initializing Objects

We want to put some labels at the top of the window to give the player some information about the score and the current level. Eventually, we will have a score display, the name of the level, and a row of icons representing the number of remaining lives.

#### Making the Labels

To make a text label in pyglet, just initialize a pyglet.text.Label object:

    score_label = pyglet.text.Label(text="Score: 0", x=10, y=575)
    level_label = pyglet.text.Label(text="My Amazing Game", 
                                    x=400, y=575, anchor_x='center')

Notice that the second label is centered using the anchor_x attribute.

#### Drawing the Labels

We want pyglet to call a custom function whenever the window is drawn. To make that happen, we need to either subclass Window and override the on_draw() function, or use the @Window.event decorator on a function with the same name:

    @game_window.event
    def on_draw():
        # draw things here

The @game\_window.event decorator lets the Window instance know that on\_draw() is an event handler. The on\_draw event is fired whenever - you guessed it - the window needs to be redrawn. Other events include on\_mouse\_press and on\_key_press.

Now we can fill the method with the functions necessary to draw our labels. Before we draw anything, we should clear the screen. After that, we can simply call each object's draw() function.

    @game_window.event
    def on_draw():
        game_window.clear()
    
        level_label.draw()
        score_label.draw()

Now when you run asteroids.py, you should get a window with a score of zero in the upper left corner and a centered label reading "Version 1: Static Graphics" at the top of the screen.

#### Making the Player and Asteroid Sprites

The player should be an instance or subclass of pyglet.sprite.Sprite, like so:

    from game import resources
    ...
    player_ship = pyglet.sprite.Sprite(img=resources.player_image, x=400, y=300)

To get the player to draw on the screen, add a line to on_draw():

    @game_window.event
    def on_draw():
        ...
        player_ship.draw()

Loading the asteroids is a little more complicated, since we'll need to place more than one at random locations that don't immediately collide with the player. Let's put the loading code in a new game submodule called load.py:

    import pyglet, random
    import resources

    def asteroids(num_asteroids):
        asteroids = []
        for i in range(num_asteroids):
            asteroid_x = random.randint(0, 800)
            asteroid_y = random.randint(0, 600)
            new_asteroid = pyglet.sprite.Sprite(img=resources.asteroid_image, 
                                                x=asteroid_x, y=asteroid_y)
            new_asteroid.rotation = random.randint(0, 360)
            asteroids.append(new_asteroid)
        return asteroids

All we are doing here is making a few new sprites with random positions. There's still a problem, though: an asteroid might randomly be placed exactly where the player is, causing immediate death. To fix this issue, we'll need to be able to tell how far away new asteroids are from the player. Here is a simple function to calculate that distance:

    import math
    ...
    def distance(point_1=(0, 0), point_2=(0, 0)):
        """Returns the distance between two points"""
        return math.sqrt((point_1[0]-point_2[0])**2+(point_1[1]-point_2[1])**2)

To check new asteroids agains the player's position, we need to pass the player's position into the asteroids() function and keep regenerating new coordinates until the asteroid is far enough away. Pyglet sprites keep track of their position both as a tuple (Sprite.position) and as x and y attributes (Sprite.x and Sprite.y). To keep our code short, we'll just pass the position tuple into the function.

    def asteroids(num_asteroids, player_position):
        asteroids = []
        for i in range(num_asteroids):
            asteroid_x, asteroid_y = player_position
            while distance((asteroid_x, asteroid_y), player_position) < 100:
                asteroid_x = random.randint(0, 800)
                asteroid_y = random.randint(0, 600)
            new_asteroid = pyglet.sprite.Sprite(img=resources.asteroid_image, 
                                                x=asteroid_x, y=asteroid_y)
            new_asteroid.rotation = random.randint(0, 360)
            asteroids.append(new_asteroid)
        return asteroids

For each asteroid, it chooses random positions until it finds one away from the player, creates the sprite, and gives it a random rotation. Each asteroid is appended to a list, which is returned.

Now you can load three asteroids like this:

    from game import resources, load
    ...
    asteroids = load.asteroids(3, player_ship.position)

The asteroids variable now contains a list of sprites. Drawing them on the screen is as simple as it was for the player's ship: just call their draw() methods.

    @game_window.event
    def on_draw():
        ...
        for asteroid in asteroids:
            asteroid.draw()