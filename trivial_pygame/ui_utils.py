import pygame


def texto_vidas(vidas: int) -> str:
    """Devuelve el texto de vidas con singular/plural correcto."""
    return "Te queda 1 vida" if vidas == 1 else f"Te quedan {vidas} vidas"


def dibujar_texto_multilinea(superficie, texto, fuente, color, x, y, max_ancho, interlineado=5):
    """Dibuja texto multilinea ajustándolo a max_ancho (anclado en x, y)."""
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba = (linea_actual + " " + palabra).strip()
        if fuente.size(prueba)[0] <= max_ancho:
            linea_actual = prueba
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = palabra

    if linea_actual:
        lineas.append(linea_actual)

    for linea in lineas:
        render = fuente.render(linea, True, color)
        superficie.blit(render, (x, y))
        y += render.get_height() + interlineado


def dibujar_texto_multilinea_centrado(superficie, texto, fuente, color, x_centro, y, max_ancho, interlineado=5):
    """Dibuja texto multilinea centrando cada línea en x_centro."""
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba = (linea_actual + " " + palabra).strip()
        if fuente.size(prueba)[0] <= max_ancho:
            linea_actual = prueba
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = palabra

    if linea_actual:
        lineas.append(linea_actual)

    for linea in lineas:
        render = fuente.render(linea, True, color)
        rect = render.get_rect(center=(x_centro, y))
        superficie.blit(render, rect)
        y += render.get_height() + interlineado


def dibujar_texto_en_rect(superficie, texto, fuente, color, rect, margen=10, interlineado=5):
    """Dibuja texto dentro de un rectángulo, con salto de línea automático."""
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    max_ancho = rect.width - 2 * margen

    for palabra in palabras:
        prueba = (linea_actual + " " + palabra).strip()
        if fuente.size(prueba)[0] <= max_ancho:
            linea_actual = prueba
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = palabra

    if linea_actual:
        lineas.append(linea_actual)

    y = rect.y + margen
    for linea in lineas:
        render = fuente.render(linea, True, color)
        superficie.blit(render, (rect.x + margen, y))
        y += render.get_height() + interlineado
