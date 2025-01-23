import argparse
import math

import pygame


def read_palette(filepath):
    with open(filepath, "r") as f:
        palette = tuple(map(lambda p: int(p, 16), f.readlines()))
    return palette

def pixel_map(i, j, src_map, palette, palette_cycle, dx, dy, x_osc_mag, y_osc_mag, x_osc_period, y_osc_period, src_pa, src_width, src_height):
    i = i + dx + x_osc_mag*math.sin(2*math.pi*i/x_osc_period)
    j = j + dy + y_osc_mag*math.sin(2*math.pi*j/y_osc_period)
    return palette[(src_map[src_pa[int(i)%src_width, int(j)%src_height]] + palette_cycle) % len(palette)]

def draw_image(image, src_pa, src_width, src_height, src_map, palette, palette_cycle, dx, dy, x_osc_mag, y_osc_mag, x_osc_period, y_osc_period):
    w, h = image.get_size()
    with pygame.PixelArray(image) as pa:
        for i in range(w):
            for j in range(h):
                pa[i,j] = pixel_map(i, j, src_map, palette, palette_cycle, dx, dy, x_osc_mag, y_osc_mag, x_osc_period, y_osc_period, src_pa, src_width, src_height)

def main(source_image, source_palette, palette, num_images, cycle_period, x_vel, y_vel, x_osc_mag, y_osc_mag, x_osc_period, y_osc_period, width, height):
    source_palette = read_palette(source_palette)
    palette = read_palette(palette)
    cycled_palettes = (palette,) if cycle_period is None else tuple(
        palette[-n:] + palette[:-n] for n in range(len(palette))
    )

    src_map = {c: i for i, c in enumerate(source_palette)}

    cycle_period = cycle_period or [float("inf")]
    x_vel = x_vel or [0.]
    y_vel = y_vel or [0.]
    x_osc_mag = x_osc_mag or [0.]
    y_osc_mag = y_osc_mag or [0.]
    x_osc_period = x_osc_period or [float("inf")]
    y_osc_period = y_osc_period or [float("inf")]

    for thing in (cycle_period, x_vel, y_vel, x_osc_mag, y_osc_mag, x_osc_period, y_osc_period):
        while len(thing) < num_images:
            thing.extend(thing)

    pygame.init()
    display_flags = pygame.SCALED
    #display_flags |= pygame.NOFRAME
    display = pygame.display.set_mode((width, height), display_flags, 32)

    src = pygame.image.load(source_image).convert()
    src_pa = pygame.PixelArray(src)
    src_width, src_height = src.get_size()

    images = [pygame.surface.Surface((width, height)) for _ in range(num_images)]
    alpha = 255./num_images

    palette_cycle_t = [0. for _ in range(num_images)]
    palette_cycle = [0 for _ in range(num_images)]

    clock = pygame.time.Clock()
    t = 0.
    pt = 1.5
    frames = 0
    try:
        while True:
            dt = clock.tick(90)/1000.0
            t += dt
            for n, image in enumerate(images):
                palette_cycle_t[n] += dt
                if palette_cycle_t[n] > cycle_period[n%len(cycle_period)]:
                    palette_cycle_t[n] = 0
                    palette_cycle[n] = (palette_cycle[n] + 1) % len(palette)
                dx = (x_vel[n] * t) % src_width
                dy = (y_vel[n] * t) % src_height
                draw_image(image, src_pa, src_width, src_height, src_map, palette, palette_cycle[n], dx, dy, x_osc_mag[n], y_osc_mag[n], x_osc_period[n], y_osc_period[n])
                image.set_alpha(alpha)
                display.blit(image, (0, 0))
            pygame.display.flip()
            frames += 1
    except KeyboardInterrupt:
        pass
    pygame.quit()
    print(f"\nAvg. FPS: {frames/t}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="motherly", description="Create Earthbound-esque backgrounds")
    parser.add_argument("source_image")
    parser.add_argument("source_palette")
    parser.add_argument("palette")
    parser.add_argument("num_images", type=int)
    parser.add_argument("--cycle-period", action="append", type=float)
    parser.add_argument("--x-vel", action="append", type=float)
    parser.add_argument("--y-vel", action="append", type=float)
    parser.add_argument("--x-osc-mag", action="append", type=float)
    parser.add_argument("--y-osc-mag", action="append", type=float)
    parser.add_argument("--x-osc-period", action="append", type=float)
    parser.add_argument("--y-osc-period", action="append", type=float)
    parser.add_argument("--width", default=160, type=int)
    parser.add_argument("--height", default=160, type=int)
    args = parser.parse_args()
    main(**vars(args))

