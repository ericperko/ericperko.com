## Part 2: Basic Motion

In the second version of the example, we'll introduce a simpler, faster way to draw all of the game objects, as well as add row of icons indicating the number of lives left. We'll also write some code to make the player and the asteroids obey the laws of physics.

### More Graphics

#### Drawing with Batches

Calling each object's draw() method manually can become cumbersome and tedious if there are many different kinds of objects. Graphics batches simplify drawing by letting you draw all your objects with a single function call. All you need to do is create a batch, pass it into each object you want to draw, and call the batch's draw() method.

To create a new batch, simply call pyglet.graphics.Batch():

    main_batch = pyglet.graphics.Batch()

To make an object a member of a batch, just pass the batch into its constructor as the batch keyword argument:

    score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)

Add the batch keyword argument to each graphical object created in asteroids.py.

To use the batch with the asteroid sprites, we'll need to pass the batch into the game.load.asteroid() function, then just add it as a keyword argument to each new sprite:

    def asteroids(num_asteroids, player_position, batch=None):
        ...
        new_asteroid = pyglet.sprite.Sprite(img=resources.asteroid_image, 
                                                x=asteroid_x, y=asteroid_y,
                                                batch=batch)

    asteroids = load.asteroids(3, player_ship.position, main_batch)

Now you can replace those five lines of draw() calls with just one:

    main_batch.draw()

Now when you run asteroids.py, it should look exactly the same.

#### Displaying Little Ship Icons

To show how many lives the player has left, we'll need to draw a little row of icons in the upper right corner of the screen. Since we'll be making more than one using the same template, let's create a function called player_lives() in the load module to generate them.

The icons should look the same as the player's ship. We could create a scaled version using an image editor, or we could just let pyglet do the scaling. I don't know about you, but I prefer the option that requires less work.

The function for creating the icons is almost exactly the same as the one for creating asteroids. For each icon we just create a sprite, give it a position and scale, and append it to the return list.

    def player_lives(num_icons, batch=None):
        player_lives = []
        for i in range(num_icons):
            new_sprite = pyglet.sprite.Sprite(img=resources.player_image, 
                                              x=785-i*30, y=585, 
                                              batch=batch)
            new_sprite.scale = 0.5
            player_lives.append(new_sprite)
        return player_lives

The player icon is 50x50 pixels, so half that size will be 25x25. We want to put a little bit of space between each icon, so we create them at 30-pixel intervals starting from the right side of the screen and moving to the left. Note that like the asteroids() function, player_lives() takes a batch argument. A None value specifies no batch.

### Making Things Move

The game would be pretty boring if nothing on the screen ever moved. To achieve motion, we'll need to write our own set of classes to handle frame-by-frame movement calculations. We'll also need to write a Player class to respond to keyboard input.

#### Creating the Basic Motion Class

Since every visible object is represented by at least one Sprite, we may as well make our basic motion class a subclass of pyglet.sprite.Sprite. Another approach would be to have our class inherit from object and have a sprite attribute, but I find that simply subclassing Sprite provides more convenient notation.

Create a new game submodule called physicalobject.py and declare a PhysicalObject class. The only new attributes we'll be adding will store the object's velocity, so the constructor will be simple.

    class PhysicalObject(pyglet.sprite.Sprite):
    
        def __init__(self, *args, **kwargs):
            super(PhysicalObject, self).__init__(*args, **kwargs)
        
            self.velocity_x, self.velocity_y = 0.0, 0.0

Each object will need to be updated every frame, so let's write an update() method.

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

What's dt? It's the time step. Game frames are not instantaneous, and they don't always take equal amounts of time. If you've ever tried to play a modern game on an old machine, you know that frame rates can jump all over the place. There are a number of ways to deal with this problem, the simplest one being to just multiply all time-sensitive operations by dt.

If we give objects a velocity and just let them go, they will fly off the screen before long. Since we're making a version of Asteroids, we would rather they just wrapped around the screen. Here is a simple function that accomplishes this goal:

    def check_bounds(self):
        min_x = -self.image.width/2
        min_y = -self.image.height/2
        max_x = 800 + self.image.width/2
        max_y = 600 + self.image.height/2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

As you can see, it simply checks to see if objects are no longer visible on the screen, and if so, it moves them to the other side of the screen. To make every PhysicalObject use this behavior, add a call to self.check_bounds() at the end of update().

To make the asteroids use our new motion code, just import the physicalobject module and change the "new_asteroid = ..." line to create a new PhysicalObject instead of a Sprite. You'll also want to give them a random initial velocity. Here is the new, improved load.asteroids() function:

    def asteroids(num_asteroids, player_position, batch=None):
        ...
        new_asteroid = physicalobject.PhysicalObject(...)
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x = random.random()*40
        new_asteroid.velocity_y = random.random()*40
        ...

#### Writing the Game Update Function

To call each object's update() method every frame, we first need to have a list of those objects. For now, we can just declare it after setting up all the other objects:

    game_objects = [player_ship] + asteroids

Now we can write a simple function to iterate over the list:

    def update(dt):
        for obj in game_objects:
            obj.update(dt)

The update() function takes a dt parameter because it is still not the source of the actual time step.

#### Calling the Update Function

We need to update the objects at least once per frame. What's a frame? Well, most screens have a maximum refresh rate of 60 hertz. If we set our loop to run at exactly 60 hertz, though, the motion will look a little jerky because it won't match the screen exactly. Instead, we should have it update twice as fast, 120 times per second, to get smooth animation.

Instead of using an actual loop to update the game every frame, we let pyglet call the function at a specified interval, using no more resources than are necessary. The pyglet.clock module contains a number of ways to call functions periodically or at some specified time in the future. The one we want is pyglet.clock.schedule_interval():

pyglet.clock.schedule_interval(update, 1/120.0)

Putting this line above pyglet.app.run() in the if \_\_name\_\_ == '\_\_main\_\_' block tells pyglet to call update() 120 times per second. Pyglet will pass in the elapsed time, i.e. dt, as the only parameter.

Now when you run asteroids.py, you should see your formerly static asteroids drifting serenely across the screen, reappearing on the other side when they slide off the edge.

#### Writing the Player Class

In addition to obeying the basic laws of physics, the player object needs to respond to keyboard input. Start by creating a game.player module, importing the appropriate modules, and subclassing PhysicalObject:

    import physicalobject, resources

    class Player(physicalobject.PhysicalObject):
    
        def __init__(self, *args, **kwargs):
            super(Player, self).__init__(img=resources.player_image, 
                                         *args, **kwargs)

So far, the only difference between a Player and a PhysicalObject is that a Player will always have the same image. But Player objects need a couple more attributes. Since the ship will always thrust with the same force in whatever direction it points, we'll need to define a constant for the magnitude of that force. We should also define a constant for the ship's rotation speed.

                self.thrust = 300.0
                self.rotate_speed = 200.0

Now we need to get the class to respond to user input. Pyglet uses a polling approach to input, sending key press and key release events to registered event handlers. We will need to constantly check if a key is down, and one way to accomplish that is to maintain a dictionary of keys. First, we need to initialize the dictionary in the constructor:

                self.keys = dict(left=False, right=False, up=False)

Then we need to write two methods, on\_key\_press() and on\_key\_release(). When pyglet checks a new event handler, it looks for these two methods, among others.

    import math
    from pyglet.window import key
    import physicalobject, resources
    ...
    class Player(physicalobject.PhysicalObject)
        ...
        def on_key_press(self, symbol, modifiers):    
            if symbol == key.UP:
                self.keys['up'] = True
            elif symbol == key.LEFT:
                self.keys['left'] = True
            elif symbol == key.RIGHT:
                self.keys['right'] = True

        def on_key_release(self, symbol, modifiers):
            if symbol == key.UP:
                self.keys['up'] = False
            elif symbol == key.LEFT:
                self.keys['left'] = False
            elif symbol == key.RIGHT:
                self.keys['right'] = False

That looks pretty cumbersome. There's a better way to do it which we'll see later, but for now, this version serves as a good demonstration of pyglet's event system.

The last thing we need to do is write the update() method. It follows the same behavior as a PhysicalObject plus a little extra, so we'll need to call PhysicalObject's update() method and then respond to input.

        def update(self, dt):
            super(Player, self).update(dt)
        
            if self.keys['left']:
                self.rotation -= self.rotate_speed * dt
            if self.keys['right']:
                self.rotation += self.rotate_speed * dt

Pretty simple so far. To rotate the player, we just add the rotation speed to the angle, multiplied by dt to account for time. Note that Sprite objects' rotation attributes are in degrees, with clockwise as the positive direction. This means that you need to call math.degrees() or math.radians() and make the result negative whenever you use Python's built-in math functions with the Sprite class, since those functions use radians instead of degrees, and their positive direction is counter-clockwise. The code to make the ship thrust forward uses an example of such a conversion:

            if self.keys['up']:
                angle_radians = -math.radians(self.rotation)
                force_x = math.cos(angle_radians) * self.thrust * dt
                force_y = math.sin(angle_radians) * self.thrust * dt
                self.velocity_x += force_x
                self.velocity_y += force_y

First, we convert the angle to radians so that math.cos() and math.sin() will get the correct values. Then we apply some simple physics to modify the ship's X and Y velocity components and push the ship in the right direction.

We now have a complete Player class. If we add it to the game and tell pyglet that it's an event handler, we should be good to go.

#### Integrating the Player Class

The first thing we need to do is make player_ship an instance of Player:

    from game import player
    ...
    player_ship = player.Player(x=400, y=300, batch=main_batch)

Now we need to tell pyglet that player\_ship is an event handler. To do that, we need to push it onto the event stack with game\_window.push_handlers():

    game_window.push_handlers(player_ship)

That's it! Now you should be able to run the game and move the player with the arrow keys.
