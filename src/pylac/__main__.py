from .containers import Container, VStack, HStack, Grid
import pygame


def draw(screen, layout):
    for id, child in layout.items():
        match id:
            case 'children': [ draw(screen, c) for c in child ]
            case 'back': pass
            case 'controllers': pass
            case 'states': pass
            case 'plots': pass
            case 'motors': pass
            case 'header': pass
            case _:
                pygame.draw.rect(
                    screen,
                    (255, 28, 28),
                    pygame.Rect(
                        child[0],
                        child[1],
                        child[2],
                        child[3],
                    )
                )

def generate_layout():
    back = VStack("back")
    back.set_padding(20.0)
    back.set_gap(20.0)

    header = HStack("header")
    header.set_gap(20.0)
    header.set_padding(10.0)
    header.add(Container("label1"))
    header.add(Container("label2"))
    header.add(Container("label3"))
    header.add(Container("label4"))

    plots = Grid("plots", 2, 2)
    plots.set_gaps(20.0, 20.0)
    plots.add(Container("p1"))
    plots.add(Container("p2"))
    plots.add(Container("p3"))
    plots.add(Container("p4"))

    controllers = HStack("controllers")
    controllers.set_gap(20.0)

    motors = VStack("motors")
    motors.set_gap(20.0)
    motors.add(Container("m1"))
    motors.add(Container("m2"))

    states = Grid("states", 4, 3)
    states.set_gaps(20.0, 20.0)
    states.fill_row_first(False)
    states.add(Container("s1"))
    states.add(Container("s2"))
    states.add(Container("s3"))
    states.add(Container("s4"))

    controllers.add(motors)
    controllers.add(states)

    back.add(header, 1)
    back.add(controllers, 4)
    back.add(plots, 10)
    return back
    


def main():
    back = generate_layout()
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            back.set_dim(screen.get_width(), screen.get_height())
            back.update()
            layout = back.get_layout()
            draw(screen, layout)
            pygame.display.flip()
            clock.tick(120)
        print("Quitting...")
    except KeyboardInterrupt:
        print("Quitting...")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
