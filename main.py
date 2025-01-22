from pprint import pprint

import pygame


SRC_PALETTE = (
    0x000000,
    0x353535,
    0x555555,
    0x656565,
    0x8a8a8a,
    0xaaaaaa,
    0xcacaca,
    0xffffff,
)
SRC_MAP = {c: i for i, c in enumerate(SRC_PALETTE)}

PALETTE = (
    0x99ccff,
    0x99ccdd,
    0x99cccc,
    0x99ccaa,
    0x99cc88,
    0x99cc66,
    0x99cc44,
    0x99cc22,
)

CYCLED_PALETTES = tuple(
    PALETTE[-n:] + PALETTE[:-n] for n in range(len(PALETTE))
)

def pixel_map(i, j, palette_cycle, x_cycle, y_cycle, src_pa):
    return PALETTE[(SRC_MAP[src_pa[int(i + x_cycle)%256, int(j + y_cycle)%256]] + palette_cycle) % len(PALETTE)]

def main():
    pygame.init()
    display_flags = pygame.NOFRAME | pygame.SCALED
    display = pygame.display.set_mode((256, 256), display_flags, 32)

    src = pygame.image.load("bg2.png").convert()
    src_pa = pygame.PixelArray(src)

    image = pygame.surface.Surface((256, 256))

    palette_cycle_period = .2
    palette_cycle_t = 0.
    palette_cycle = 0
    x_cycle_period = 5
    y_cycle_period = 11
    x_cycle_t = 0.
    y_cycle_t = 0.
    x_cycle = 0
    y_cycle = 0

    clock = pygame.time.Clock()
    try:
        while True:
            dt = clock.tick(60)/1000.0
            if (palette_cycle_t := palette_cycle_t+dt) > palette_cycle_period:
                palette_cycle_t = 0
                palette_cycle = (palette_cycle + 1) % len(PALETTE)
            x_cycle += dt*256/x_cycle_period
            y_cycle += dt*256/y_cycle_period
            x_cycle %= 256
            y_cycle %= 256
            with pygame.PixelArray(image) as pa:
                for i in range(256):
                    for j in range(256):
                        pa[i,j] = pixel_map(i, j, palette_cycle, x_cycle, y_cycle, src_pa)
            display.blit(image, (0, 0))
            pygame.display.flip()
    except KeyboardInterrupt:
        pass
    pygame.quit()

if __name__ == "__main__":
    main()

