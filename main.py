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

PALETTE = (
    0x99ccff,
    0x99cccc,
    0x99ff00,
    0x99cc99,
    0x99cc66,
    0x99ff66,
    0x99cc33,
    0x99cc00,
)

CYCLED_PALETTES = tuple(
    PALETTE[-n:] + PALETTE[:-n] for n in range(len(PALETTE))
)

def palette_swapped(src, cycle=0):
    image = src.copy()
    with pygame.PixelArray(image) as pa:
        for src_c, plt_c in zip(SRC_PALETTE, CYCLED_PALETTES[cycle]):
            pa.replace(src_c, plt_c)
    return image

def main():
    pygame.init()
    display_flags = pygame.NOFRAME | pygame.SCALED
    display = pygame.display.set_mode((256, 256), display_flags, 32)

    cycle_period = .2
    cycle_t = 0.
    cycle = 0
    src = pygame.image.load("bg.png").convert()

    clock = pygame.time.Clock()
    try:
        while True:
            dt = clock.tick(60)/1000.0
            if (cycle_t := cycle_t+dt) > cycle_period:
                cycle_t = 0
                cycle = (cycle + 1) % len(PALETTE)
            image = palette_swapped(src, cycle)
            display.blit(image, (0, 0))
            pygame.display.flip()
    except KeyboardInterrupt:
        pass
    pygame.quit()

if __name__ == "__main__":
    main()

