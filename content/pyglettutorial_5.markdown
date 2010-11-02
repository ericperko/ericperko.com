## Part 4: Collision Response

In this section, we'll add bullets. This new feature will require us to start adding things to the game_objects list during the game, as well as have objects check each others' types to make a decision about whether or not they should die.

### Adding Objects During Play

#### How?

We handled object removal with a boolean flag. Adding objects will be a little bit more complicated. For one thing, an object can't just say "Add me to the list!" It has to come from somewhere. For another thing, an object might want to add more than one other object at a time.

There are a few ways to solve this problem. To avoid circular references, keep our constructors nice and short, and avoid adding extra modules, we'll have each object keep a list of new child objects to be added to game_objects.

#### Tweaking the Game Loop

The simplest way to check objects for children and add those children to the list is to add two lines of code to the game\_objects loop. We haven't implemented the new\_objects attribute yet, but when we do, it will be a list of objects to add.

    for obj in game_objects:
        obj.update(dt)
        game_objects.extend(obj.new_objects)
        obj.new_objects = []

Unfortunately, this simple solution is problematic. It's generally a bad idea to modify a list while iterating over it. The fix is to simply add new objects to a separate list, then add the objects in the separate list to game_objects after we have finished iterating over it.

Declare a to\_add list just below the loop and add new objects to it instead. At the very bottom of update(), after the object removal code, add the objects in to\_add to game_objects.

    ...collision...
    
    to_add = []
    
    for obj in game_objects:
        obj.update(dt)
        to_add.extend(obj.new_objects)
        obj.new_objects = []
    
    ...removal...
    
    game_objects.extend(to_add)

#### Putting the Attribute in PhysicalObject

As mentioned before, all we have to do is declare a new_objects attribute in the PhysicalObject class:

    def __init__(self, *args, **kwargs):
        ....
        self.new_objects = []

To add a new object, all we have to do is put something in new\_objects, and the main loop will see it, add it to the game\_objects list, and clear new_objects.

### Adding Bullets

#### Writing the Bullet Class

For the most part, bullets act like any other PhysicalObject, but they have two differences, at least in this game: they only collide with some objects, and they disappear from the screen after a couple of seconds to prevent the player from flooding the screen with bullets.

First, make a new submodule of game called bullet.py and start a simple subclass of PhysicalObject.

    import pyglet
    import physicalobject, resources

    class Bullet(physicalobject.PhysicalObject):
        """Bullets fired by the player"""
    
        def __init__(self, *args, **kwargs):
            super(Bullet, self).__init__(resources.bullet_image, *args, **kwargs)

To get bullets to disappear after a time, we could keep track of our own age and lifespan attributes, or we could let pyglet do all the work for us. I don't know about you, but I prefer the second option. First, we need to write a function to call at the end of a bullet's life:

    def die(self, dt):
        self.dead = True</pre>

Now we need to tell pyglet to call it after half a second or so. We can do this as soon as the object is initialized by adding a call to pyglet.clock.schedule_once() to the constructor:

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(resources.bullet_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 0.5)

There's still more work to be done on the Bullet class, but before we do any more work on the class itself, let's get them on the screen.

#### Firing Bullets

The Player class will be the only class that fires bullets, so let's open it up, import the bullet module, and add a bullet_speed attribute to its constructor:

    ...
    import bullet

    class Player(physicalobject.PhysicalObject):
        def __init__(self, *args, **kwargs):
            super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
            ....
            self.bullet_speed = 700.0

Now we can write the code to create a new bullet and send it hurling off into space. First, we need to resurrect the on\_key\_press() event handler:

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.fire()

The fire() method itself will be a bit more complicated. Most of the calculations will be very similar to the ones for thrusting, but there will be some differences. We'll need to spawn the bullet out at the nose of the ship, not at its center. We'll also need to add the ship's existing velocity to the bullet's new velocity, or the bullets will end up going slower than the ship if the player gets going fast enough.

As usual, convert to radians and reverse the direction:

    def fire(self):
        angle_radians = -math.radians(self.rotation)

Next, calculate the bullet's position and instantiate it:

        ship_radius = self.image.width/2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = bullet.Bullet(bullet_x, bullet_y, batch=self.batch)

Set its velocity using almost the same equations:

        bullet_vx = self.velocity_x + math.cos(angle_radians) * self.bullet_speed
        bullet_vy = self.velocity_y + math.sin(angle_radians) * self.bullet_speed
        new_bullet.velocity_x, new_bullet.velocity_y = bullet_vx, bullet_vy

Finally, add it to the new\_objects list so that the main loop will pick it up and add it to game\_objects.

    self.new_objects.append(new_bullet)

At this point, you should be able to fire bullets out of the front of your ship. There's just one problem: as soon as you fire, your ship disappears. You may have noticed earlier that asteroids also disappear when they touch each other. To fix this problem, we'll need to start customizing each class's handle\_collision\_with() method.

### Customizing Collision Behavior

There are five kinds of collisions in the current version of the game: bullet-asteroid, bullet-player, asteroid-player, bullet-bullet, and asteroid-asteroid. There would be many more in a more complex game.

In general, objects of the same type should not be destroyed when they collide, so we can generalize that behavior in PhysicalObject. Other interactions will require a little more work.

#### Letting Twins Ignore Each Other

To let two asteroids or two bullets pass each other by without a word of acknowledgement (or a dramatic explosion), we just need to check if their classes are equal in the PhysicalObject.handle\_collision\_with() method:

    def handle_collision_with(self, other_object):
        if other_object.__class__ == self.__class__:
            self.dead = False
        else:
            self.dead = True

#### Customizing Bullet Collisions

Since bullet collision behavior can vary so wildly across objects, let's add a reacts\_to\_bullets attribute to PhysicalObjects which the Bullet class can check to determine if it should register a collision or not. We should also add an is_bullet attribute so we can check the collision properly from both objects.

First, initialize the reacts\_to\_bullets attribute to True in the PhysicalObject constructor.

    class PhysicalObject(pyglet.sprite.Sprite):
        def __init__(self, *args, **kwargs):
            ...
            self.reacts_to_bullets = True
            self.is_bullet = False
            ...

    class Bullet(physicalobject.PhysicalObject):
        def __init__(self, *args, **kwargs):
            ...
            self.is_bullet = True

Then, insert a bit of code in PhysicalObject.collides_with() to ignore bullets under the right circumstances:

        def collides_with(self, other_object):
            if not self.reacts_to_bullets and other_object.is_bullet:
                return False
            if self.is_bullet and not other_object.reacts_to_bullets:
                return False
            ...

Finally, set self.reacts\_to\_bullets = False in Player.\_\_init\_\_(). The Bullet class is completely finished! Now let's make something happen when a bullet hits an asteroid.

### Making Asteroids Explode

Asteroids is challenging to players because every time you shoot an asteroid, it turns into more asteroids. We need to mimic that behavior if we want our game to be any fun. We've already done most of the hard parts. All that remains is to make another subclass of PhysicalObject and write a custom handle\_collision\_with() method, along with a couple of maintenance tweaks.

#### Writing the Asteroid Class

Create a new submodule of game called asteroid.py. Write the usual constructor to pass a specific image to the superclass, passing along any other parameters.

    import pyglet
    import resources, physicalobject

    class Asteroid(physicalobject.PhysicalObject):
        def __init__(self, *args, **kwargs):
            super(Asteroid, self).__init__(resources.asteroid_image, *args, **kwargs)

Now we need to write a new handle\_collision\_with() method. It should create a random number of new, smaller asteroids with random velocities. However, it should only do that if it's big enough. An asteroid should divide at most twice, and if we scale it down by half each time, then an asteroid should stop dividing when it's 1/4 the size of a new asteroid.

We want to keep the old behavior of ignoring other asteroids, so start the method with a call to the superclass's method:

        def handle_collision_with(self, other_object):
            super(Asteroid, self).handle_collision_with(other_object)

Now we can say that if it's supposed to die, and it's big enough, then we should create two or three new asteroids with random rotations and velocities. We should add the old asteroid's velocity to the new ones to make it look like they come from the same object.

    import random
    ...
    class Asteroid...
        def handle_collision_with(self, other_object):
            super(Asteroid, self).handle_collision_with(other_object)
            if self.dead and self.scale > 0.25:
                num_asteroids = random.randint(2, 3)
                for i in xrange(num_asteroids):
                    new_asteroid = Asteroid(x=self.x, y=self.y, batch=self.batch)
                    new_asteroid.rotation = random.randint(0, 360)
                    new_asteroid.velocity_x = random.random()*70 + self.velocity_x
                    new_asteroid.velocity_y = random.random()*70 + self.velocity_y
                    new_asteroid.scale = self.scale * 0.5
                    self.new_objects.append(new_asteroid)

While we're here, let's add a small graphical touch to the asteroids by making them rotate a little. To do that, we'll add a rotate_speed attribute and give it a random value. Then we'll write an update() method to apply that rotation every frame.

Add the attribute in the constructor:

        def __init__(self, *args, **kwargs):
            super(Asteroid, self).__init__(resources.asteroid_image, *args, **kwargs)
            self.rotate_speed = random.random() * 100.0 - 50.0

Then write the update() method:

        def update(self, dt):
            super(Asteroid, self).update(dt)
            self.rotation += self.rotate_speed * dt

The last thing we need to do is go over to load.py and have the asteroid() method create a new Asteroid instead of a PhysicalObject.

    import asteroid

    def asteroids(num_asteroids, player_position, batch=None):
        ...
        for i in range(num_asteroids):
            ...
            new_asteroid = asteroid.Asteroid(x=asteroid_x, y=asteroid_y, batch=batch)
            ...
        return asteroids

Now we're looking at something resembling a game. There are just a few more things left to do before we can pat ourselves on the back.
