## Part 3: Giving the Player Something to Do

In any good game, there needs to be something working against the player. In the case of Asteroids, it's the threat of collision with, well, an asteroid. Collision detection requires a lot of infrastructure in the code, so this section will focus on making it work. We'll also clean up the player class and show some visual feedback for thrusting.

### Simplifying Player Input

Right now, the Player class handles all of its own keyboard events. It spends 13 lines of code doing nothing but setting boolean values in a dictionary. One would think that there would be a better way, and there is: pyglet.window.key.KeyStateHandler. This handy class automatically does what we have been doing manually: it tracks the state of every key on the keyboard.

To start using it, we need to initialize it and push it onto the event stack instead of the Player class. First, let's add it to Player's constructor:

    self.key_handler = key.KeyStateHandler()

We also need to push the key\_handler object onto the event stack. Keep pushing the player\_ship object in addition to its key handler, because we'll need it to keep handling key press and release events later.

    game_window.push_handlers(player_ship.key_handler)

Since Player now relies on key_handler to read the keyboard, we need to change the update() method to use it. The only changes are in the if conditions:

    if self.key_handler[key.LEFT]:
        ...
    if self.key_handler[key.RIGHT]:
        ...
    if self.key_handler[key.UP]:
        ...

Now we can remove the on\_key\_press() and on\_key\_release() methods from the class. It's just that simple. If you need to see a list of key constants, you can check the API documentation under pyglet.window.key.

### Adding an Engine Flame

Without visual feedback, it can be difficult to tell if the ship is actually thrusting forward or not, especially for an observer just watching someone else play the game. One way to provide visual feedback is to show an engine flame behind the player while the player is thrusting.

#### Loading the Flame Image

The player will now be made of two sprites. There's nothing preventing us from letting a Sprite own another Sprite, so we'll just give Player an engine_sprite attribute and update it every frame. For our purposes, this approach will be the simplest and most scalable.

To make the flame draw in the correct position, we could either do some complicated math every frame, or we could just move the image's anchor point. First, load the image in resources.py:

    engine_image = pyglet.resource.image("engine_flame.png")

To get the flame to draw behind the player, we need to move the flame image's center of rotation to the right, past the end of the image. To do that, we just set its anchor\_x and anchor\_y attributes:

    engine_image.anchor_x = engine_image.width * 1.5
    engine_image.anchor_y = engine_image.height / 2

Now the image is ready to be used by the player class. If you're still confused about anchor points, experiment with the values for engine_image's anchor point when you finish this section.

#### Creating and Drawing the Flame

The engine sprite needs to be initialized with all the same arguments as Player, except that it needs a different image and must be initially invisible. The code for creating it belongs in Player.\_\_init\_\_() and is very straightforward:

    self.engine_sprite = pyglet.sprite.Sprite(img=resources.engine_image, 
                                              *args, **kwargs)
    self.engine_sprite.visible = False

To make the engine sprite appear only while the player is thrusting, we need to add some logic to the if self.key_handler[key.UP] block in the update() method.

    if self.key_handler[key.UP]:
        ...
        self.engine_sprite.visible = True
    else:
        self.engine_sprite.visible = False

To make the sprite appear at the player's position, we also need to update its position and rotation attributes:

    if self.key_handler[key.UP]:
        ...
        self.engine_sprite.rotation = self.rotation
        self.engine_sprite.x = self.x
        self.engine_sprite.y = self.y
        self.engine_sprite.visible = True
    else:
        self.engine_sprite.visible = False

#### Cleaning Up After Death

When the player is inevitably smashed to bits by an asteroid, he will disappear from the screen. However, simply removing the Player instance from the game_objects list is not enough for it to be removed from the graphics batch. To do that, we need to call its delete() method. Normally a Sprite's own delete() method will work fine without modifications, but our subclass has its own Sprite which must also be deleted when the Player instance is deleted. To get both to die gracefully, we must write a simple delete() method:

    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()

The Player class is now cleaned up and ready to go.

### Checking For Collisions

To make objects disappear from the screen, we'll need to manipulate the game_objects list. Every object will need to check every other object's position against its own, and each object will have to decide whether or not it should be removed from the list. The game loop will then check for dead objects and remove them from the list.

#### Checking All Object Pairs

We need to check every object against every other object. The simplest method is to use nested loops. This method will be inefficient for a large number of objects, but it will work for our purposes. We can use one easy optimization and avoid checking the same pair of objects twice. Here's the setup for the loops, which belongs in update(). It simply iterates over all object pairs without doing anything.

    for i in xrange(len(game_objects)):
        for j in xrange(i+1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

We'll need a way to check if an object has already been killed. We could go over to PhysicalObject right now and put it in, but let's keep working on the game loop and implement the method later. For now, we'll just assume that everything in game_objects has a dead attribute which will be False until the class sets it to True, at which point it will be ignored and eventually removed from the list.

To perform the actual check, we'll also need to call two more methods that don't exist yet. One method will determine if the two objects actually collide, and the other method will give each object an opportunity to respond to the collision. The checking code itself is easy to understand, so I won't bother you with further explanations:

            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)

Now all that remains is for us to go through the list and remove dead objects:

    ...update game objects...
    
    for to_remove in [obj for obj in game_objects if obj.dead]:
        to_remove.delete()
        game_objects.remove(to_remove)

As you can see, it simply calls the object's delete() method to remove it from any batches, then it removes it from the list. If you haven't used list comprehensions much, the above code might look like it's removing objects from the list while traversing it. Fortunately, the list comprehension is evaluated before the loop actually runs, so there should be no problems.

#### Implementing the Collision Functions

We need to add three things to the PhysicalObject class: the dead attribute, the collides\_with() method, and the handle\_collision\_with() method. The collides\_with() method will need to use the distance() function, so let's start by moving that function into its own submodule of game, called util.py:

    import pyglet, math

    def distance(point_1=(0, 0), point_2=(0, 0)):
        return math.sqrt((point_1[0]-point_2[0])**2+(point_1[1]-point_2[1])**2)

Remember to call from util import distance in load.py. Now we can write PhysicalObject.collides_with() without duplicating code.

Some fancy-pants games use polygon-based or even pixel-perfect collision detection, but this ain't one of those high-falutin' triple-A games, so we'll just pretend everything is shaped like a circle with a radius of half the image width. Circle-to-circle collision detection is very simple: if the centers of the two objects are closer than radius\_1 + radius\_2, then they are overlapping. Knowing this, we can write the collides_with() method:

    def collides_with(self, other_object):
        collision_distance = self.image.width/2 + other_object.image.width/2
        actual_distance = util.distance(self.position, other_object.position)
        
        return (actual_distance <= collision_distance)

The collision handler function is even simpler, since for now we just want every object to die as soon as it touches another object:

    def handle_collision_with(self, other_object):
        self.dead = True

One last thing: set self.dead = False in PhysicalObject.\_\_init\_\_().

And that's it! You should be able to zip around the screen, engine blazing away. If you hit something, both you and the thing you collided with should disappear from the screen. There's still no game, but we are clearly making progress.