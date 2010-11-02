Writing programs in [Python][1] is fun. Writing games is fun. **Writing games in Python** is fun! Unfortunately, tutorials to help people get started are spread pretty thin. I wanted to help correct the situation, so I wrote this tutorial.

The [pyglet programming guide][2] is a great resource, but it won't really help you if you've never written a game before. This tutorial will walk you through the steps of writing a simple Asteroids clone. This tutorial was also presented as a talk at [PyOhio][3]. If you just want a broad overview, you can watch the talk, which lasts about 40 minutes. Otherwise, you can read the text version, which is much more in-depth.

<embed src="http://blip.tv/play/AYGa8XAC" type="application/x-shockwave-flash" width="480" height="350" allowscriptaccess="always" allowfullscreen="true">
</embed>

<hr class="space" />

## Table of Contents

*   Introduction
*   [Part 1: Basic Graphics][4]
*   [Part 2: Basic Motion][5]
*   [Part 3: Giving the Player Something to Do][6]
*   [Part 4: Collision Response][7]
*   [Part 5: Next Steps][8]

## Introduction

### Who is this document for?

This document was written for people who know how to write simple Python programs and run them. That should be all you need. If that's all you have and this document confuses you, then you should [email me][9] and I'll try to fix it. 
### Why use Python for games?

The same reason you use Python for anything else. It's easy, it makes sense, and there are great libraries available.

### Speaking of libraries, what's available?

*   [PyGame][10]
*   [pyglet][11]
*   [Panda3D][12]

### Which one should I use?

My personal opinion is that pyglet is the cleanest and fastest, but PyGame has also been used to do some cool things. Panda3D is more sophisticated, geared toward 3D, and has a much higher learning curve. This tutorial will use pyglet. I'm trying to teach you, not convert you.

To get you familiar with pyglet, I'll walk you through the process of creating a simple version of the classic game Asteroids. If you ever get stuck, you can look at the project in various stages of completion on [its Github page][13].

 [1]: http://www.python.org/
 [2]: http://pyglet.org/doc/programming_guide
 [3]: http://www.pyohio.org/
 [4]: /pyglettutorial/2
 [5]: /pyglettutorial/3
 [6]: /pyglettutorial/4
 [7]: /pyglettutorial/5
 [8]: /pyglettutorial/6
 [9]: mailto:steve.johnson.public@gmail.com
 [10]: http://www.pygame.org/
 [11]: http://www.pyglet.org/
 [12]: http://www.panda3d.org/
 [13]: http://github.com/irskep/pyglettutorial
