![pylac](resources/pylac.tif)
pylac [_pˈa͡ɪlak_] is a simple GUI layout calculator that can be used with anything. 

The idea is that it calculatest the x and y coordinates as well as the width and height of your elements, and you do whatever you want with that.

## Installation

The library can be easily installed using `pip` in your virtual environment

```bash
pip install git+https://github.com/alin742/pylac.git
```

to use the library, it is as simple as setting up your layout, updating the screen width and height of your root element, and getting the layout coordinates.
You use these coordinates however you want.

Here is a simple pygame example:
```python
import pygame
from pygame import draw, Rect
import pylac

def main():
    W = 800
    H = 600
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    ### LAYOUT SETUP ###
    root = pylac.VStack('root')
    root.set_padding(20.0)
    root.add(Container('box'))
    root.add(Container('box'))
    root.add(Container('box'))
    ####################
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('#181818')
        W = screen.get_width()
        H = screen.get_height()
    ### LAYOUT UPDATE ###
        root.set_dim(W, H)
        root.update()
    #####################
    ### OUTPUT COORDS ###
        layout = root.get_layout()
        draw.rect(
          screen, (28, 255, 28),
          Rect(
              layout['root'][0], layout['root'][1],
              layout['root'][2], latout['root'][3]
          )
        )
        for child in layout['children']:
            # Here all the children have the same name
            # but we can also do something different
            # based on the id of the child
            draw.rect(
              screen, (28, 255, 28),
              Rect(
                  layout['box'][0], layout['box'][1],
                  layout['box'][2], latout['box'][3]
              )
            )
    #####################
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()

```

This might have been a bit of code but when you break it down, Its super simple.

