from PIL import ImageColor

# colores
WARM_RED = '#FF462D'
DEEP_FOREST = '#042315'
WHITE = '#FFFFFF'
SPRUCE = '#2A494C'
CLOUD = '#f2f1ee'
SAGE = '#8D978B'
SPRING_GREEN = '#4CDD84'
EARTH = '#9E9287'
STONE = '#BBBBBB'
DIGITAL_DARK_SPRING_GREEN = '#187E3F'
DIGITAL_DARK_EARTH = '#565049'
DIGITAL_DARK_STONE = '#3D3C3C'


def rgba_to_rgb(base_color, background='black'):
    try:
        r, g, b, a = ImageColor.getrgb(base_color)
        R, G, B = ImageColor.getrgb(background)
    except ValueError:
        raise ValueError("Valores suministrados para los colores no son correctos")
    a = a / 255.0
    r = int(r * a + (1.0 - a) * R)
    g = int(g * a + (1.0 - a) * G)
    b = int(b * a + (1.0 - a) * B)
    return f'#{r:02x}{g:02x}{b:02x}'


if __name__ == '__main__':
    print(rgba_to_rgb(SPRUCE+'cc'))
