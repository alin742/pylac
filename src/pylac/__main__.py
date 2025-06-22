from .containers import Container, VStack, HStack, Grid
import pygame


def draw(screen, layout):
    for id, child in layout.items():
        match id:
            case 'back':
                pygame.draw.rect(
                    screen,
                    (18, 18, 18),
                    pygame.Rect(
                        child['dim'][0],
                        child['dim'][1],
                        child['dim'][2],
                        child['dim'][3],
                    )
                )
            case _:
                pygame.draw.rect(
                    screen,
                    (255, 28, 28),
                    pygame.Rect(
                        child['dim'][0],
                        child['dim'][1],
                        child['dim'][2],
                        child['dim'][3],
                    )
                )

def generate_layout(pad, gap):
    back = VStack("back", padding = [pad, pad, pad, pad], gap = gap)

    header = HStack("header", gap=gap)
    header.add(Container("label1"))
    header.add(Container("label2"))
    header.add(Container("label3"))
    header.add(Container("label4"))

    plots = Grid("plots", 2, 2, gap = gap)
    plots.set_gaps(gap, gap)
    plots.add(Container("p1"))
    plots.add(Container("p2"))
    plots.add(Container("p3"))
    plots.add(Container("p4"))

    controllers = HStack("controllers", gap = gap)

    motors = VStack("motors", gap = gap)
    motors.add(Container("m1"))
    motors.add(Container("m2"))

    states = Grid("states", 4, 3, gap = gap, row_first = False)
    states.add(Container("s1"))
    states.add(Container("s2"))
    states.add(Container("s3"))
    states.add(Container("s4"))

    controllers.add(motors)
    controllers.add(states)

    back.add(header, 1)
    back.add(controllers, 4)
    back.add(plots, 10)
    return [back, plots, header, controllers, motors, states]
    


def main():
    containers = generate_layout(20.0, 20.0)
    pygame.init()
    screen = pygame.display.set_mode((1200, 900), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            containers[0].set_dim(screen.get_width(), screen.get_height())
            [container.set_gap(0.02*screen.get_width()) for container in containers]
            containers[0].update()
            layout = containers[0].get_layout()
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
