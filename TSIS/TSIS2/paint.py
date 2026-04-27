import os
from datetime import datetime

import pygame

pygame.init()

WIDTH, HEIGHT = 1100, 700
TOOLBAR_W = 280
CANVAS = pygame.Rect(300, 20, 780, 660)

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (220, 220, 220)

COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 120, 255),
    (0, 170, 0),
    (255, 140, 0),
    (160, 0, 200),
    (255, 255, 0),
    (255, 255, 255),
]

TOOLS = [
    "pencil",
    "line",
    "rect",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
    "eraser",
    "fill",
    "text",
]

BRUSH = {"small": 2, "medium": 5, "large": 10}


def in_canvas(pos):
    return CANVAS.collidepoint(pos)


def local(pos):
    return pos[0] - CANVAS.x, pos[1] - CANVAS.y


def save_canvas(canvas):
    name = f"paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    out = os.path.join(os.path.dirname(__file__), name)
    pygame.image.save(canvas, out)


def flood_fill(surface, start, color):
    w, h = surface.get_size()
    x, y = start
    if x < 0 or y < 0 or x >= w or y >= h:
        return
    target = surface.get_at((x, y))
    if target == pygame.Color(*color):
        return
    stack = [(x, y)]
    while stack:
        px, py = stack.pop()
        if px < 0 or py < 0 or px >= w or py >= h:
            continue
        if surface.get_at((px, py)) != target:
            continue
        surface.set_at((px, py), color)
        stack.extend([(px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)])


def draw_shape(surface, tool, color, a, b, width):
    x1, y1 = a
    x2, y2 = b
    left, top = min(x1, x2), min(y1, y2)
    w, h = abs(x2 - x1), abs(y2 - y1)

    if tool == "line":
        pygame.draw.line(surface, color, a, b, width)
    elif tool == "rect":
        pygame.draw.rect(surface, color, pygame.Rect(left, top, w, h), width)
    elif tool == "circle":
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        r = max(1, int((((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) / 2))
        pygame.draw.circle(surface, color, center, r, width)
    elif tool == "square":
        side = min(w, h)
        sx = x1 if x2 >= x1 else x1 - side
        sy = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, color, pygame.Rect(sx, sy, side, side), width)
    elif tool == "right_triangle":
        pts = [(left, top + h), (left, top), (left + w, top + h)]
        pygame.draw.polygon(surface, color, pts, width)
    elif tool == "equilateral_triangle":
        pts = [(left + w // 2, top), (left, top + h), (left + w, top + h)]
        pygame.draw.polygon(surface, color, pts, width)
    elif tool == "rhombus":
        pts = [(left + w // 2, top), (left + w, top + h // 2), (left + w // 2, top + h), (left, top + h // 2)]
        pygame.draw.polygon(surface, color, pts, width)


def draw_toolbar(screen, font, small, tool, color, size):
    pygame.draw.rect(screen, GRAY, (0, 0, TOOLBAR_W, HEIGHT))
    buttons = []
    y = 20
    title = font.render("Mini Paint", True, BLACK)
    screen.blit(title, (20, y))
    y += 40

    for i, t in enumerate(TOOLS):
        r = pygame.Rect(20 + (i % 2) * 120, y + (i // 2) * 34, 110, 28)
        pygame.draw.rect(screen, (180, 220, 255) if t == tool else WHITE, r)
        pygame.draw.rect(screen, BLACK, r, 1)
        screen.blit(small.render(t.replace("_", " "), True, BLACK), (r.x + 4, r.y + 6))
        buttons.append((r, "tool", t))

    y = y + ((len(TOOLS) + 1) // 2) * 34 + 18
    for i, c in enumerate(COLORS):
        r = pygame.Rect(20 + (i % 4) * 58, y + (i // 4) * 36, 40, 24)
        pygame.draw.rect(screen, c, r)
        pygame.draw.rect(screen, (0, 120, 255) if c == color else BLACK, r, 2 if c == color else 1)
        buttons.append((r, "color", c))

    y += 84
    for i, k in enumerate(["small", "medium", "large"]):
        r = pygame.Rect(20 + i * 84, y, 76, 28)
        pygame.draw.rect(screen, (180, 220, 255) if k == size else WHITE, r)
        pygame.draw.rect(screen, BLACK, r, 1)
        screen.blit(small.render(k, True, BLACK), (r.x + 14, r.y + 6))
        buttons.append((r, "size", k))

    hint = ["1/2/3 size", "Ctrl+S save", "Text: Enter/Esc"]
    y += 44
    for h in hint:
        screen.blit(small.render(h, True, BLACK), (20, y))
        y += 22

    return buttons


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Mini Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28)
    small = pygame.font.SysFont("arial", 18)
    text_font = pygame.font.SysFont("arial", 24)

    canvas = pygame.Surface(CANVAS.size)
    canvas.fill(WHITE)

    tool = "pencil"
    color = COLORS[0]
    size = "medium"
    drawing = False
    start = None
    current = None
    prev = None

    text_mode = False
    text_pos = (0, 0)
    text_buf = ""

    run = True
    while run:
        buttons = draw_toolbar(screen, font, small, tool, color, size)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    size = "small"
                elif e.key == pygame.K_2:
                    size = "medium"
                elif e.key == pygame.K_3:
                    size = "large"
                elif e.key == pygame.K_s and (e.mod & pygame.KMOD_CTRL):
                    save_canvas(canvas)
                elif text_mode:
                    if e.key == pygame.K_RETURN:
                        if text_buf:
                            canvas.blit(text_font.render(text_buf, True, color), text_pos)
                        text_mode = False
                        text_buf = ""
                    elif e.key == pygame.K_ESCAPE:
                        text_mode = False
                        text_buf = ""
                    elif e.key == pygame.K_BACKSPACE:
                        text_buf = text_buf[:-1]
                    elif e.unicode.isprintable():
                        text_buf += e.unicode

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if e.pos[0] < TOOLBAR_W:
                    for rect, kind, val in buttons:
                        if rect.collidepoint(e.pos):
                            if kind == "tool":
                                tool = val
                                if tool != "text":
                                    text_mode = False
                                    text_buf = ""
                            elif kind == "color":
                                color = val
                            elif kind == "size":
                                size = val
                            break
                elif in_canvas(e.pos):
                    p = local(e.pos)
                    if tool == "fill":
                        flood_fill(canvas, p, color)
                    elif tool == "text":
                        text_mode = True
                        text_pos = p
                        text_buf = ""
                    else:
                        drawing = True
                        start = p
                        current = p
                        prev = p
                        w = BRUSH[size]
                        if tool == "pencil":
                            pygame.draw.circle(canvas, color, p, max(1, w // 2))
                        elif tool == "eraser":
                            pygame.draw.circle(canvas, WHITE, p, max(1, w // 2))

            elif e.type == pygame.MOUSEMOTION and drawing and in_canvas(e.pos):
                p = local(e.pos)
                current = p
                w = BRUSH[size]
                if tool == "pencil":
                    pygame.draw.line(canvas, color, prev, p, w)
                    prev = p
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, prev, p, w)
                    prev = p

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and drawing:
                end = local(e.pos) if in_canvas(e.pos) else (current or start)
                if tool in {"line", "rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"}:
                    draw_shape(canvas, tool, color, start, end, BRUSH[size])
                drawing = False
                start = None
                current = None
                prev = None

        screen.fill((245, 245, 245))
        draw_toolbar(screen, font, small, tool, color, size)
        pygame.draw.rect(screen, BLACK, CANVAS, 2)
        screen.blit(canvas, CANVAS.topleft)

        if drawing and tool in {"line", "rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"} and start and current:
            preview = canvas.copy()
            draw_shape(preview, tool, color, start, current, BRUSH[size])
            screen.blit(preview, CANVAS.topleft)

        if text_mode:
            blink = "|" if (pygame.time.get_ticks() // 350) % 2 == 0 else ""
            screen.blit(text_font.render(text_buf + blink, True, color), (CANVAS.x + text_pos[0], CANVAS.y + text_pos[1]))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
