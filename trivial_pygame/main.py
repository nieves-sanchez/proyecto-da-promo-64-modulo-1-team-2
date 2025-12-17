import sys
import random
import pygame

from preguntas import preguntas
from ui_utils import dibujar_texto_multilinea, dibujar_texto_multilinea_centrado, dibujar_texto_en_rect, texto_vidas

# -------------------------
# CONFIGURACIÓN PYGAME
# -------------------------
pygame.init()
ANCHO = 900
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))

# ✅ Título del juego (sin “frase.”)
pygame.display.set_caption("Películas y series que dejan huella")

# Colores estilo Netflix
NEGRO = (0, 0, 0)
ROJO_NETFLIX = (229, 9, 20)
GRIS_OSCURO = (15, 15, 15)
GRIS_BOTON = (40, 40, 40)
GRIS_BOTON_HOVER = (80, 80, 80)
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)

# ✅ Colores para mensajes
ROJO = (200, 0, 0)        # incorrecta / perder
VERDE = (0, 200, 0)       # correcta / ganar

# Fuentes
FUENTE_TITULO = pygame.font.SysFont("arial", 40, bold=True)
FUENTE_TEXTO = pygame.font.SysFont("arial", 24)
FUENTE_PEQUE = pygame.font.SysFont("arial", 18)

# ✅ Mensajes “un poco más grandes”
FUENTE_FEEDBACK = pygame.font.SysFont("arial", 34, bold=True)
FUENTE_FEEDBACK_PEQUE = pygame.font.SysFont("arial", 22)


NOMBRE_JUEGO = "PELÍCULAS Y SERIES QUE DEJAN HUELLA"


def crear_botones_opciones():
    """Crea 4 botones para A, B, C, D."""
    botones = []
    ancho_boton = 380
    alto_boton = 80  # más alto para varias líneas
    margen_x = 60
    margen_y_inicial = 260
    separacion_y = 100

    for fila in range(2):  # 2 filas
        for col in range(2):  # 2 columnas
            x = margen_x + col * (ancho_boton + 40)
            y = margen_y_inicial + fila * separacion_y
            rect = pygame.Rect(x, y, ancho_boton, alto_boton)
            botones.append(rect)

    return botones


def main():
    reloj = pygame.time.Clock()
    botones = crear_botones_opciones()

    # Estados: "INICIO", "INTRO_NOMBRE", "INTRO_NUM", "PREGUNTA", "FEEDBACK", "GAME_OVER"
    estado = "INICIO"

    nombre_jugador = ""
    texto_input = ""
    mensaje_error = ""
    num_preguntas = 0

    mazo = []
    indice_pregunta = 0
    puntuacion = 0
    vidas = 3

    # Datos para FEEDBACK
    ultima_correcta = None
    letra_correcta = ""
    texto_correcto = ""
    vidas_mostradas = 0
    fin_por_vidas = False  # True si pierdes por quedarte sin vidas

    def avanzar_pregunta():
        nonlocal indice_pregunta, estado
        # Si llegamos aquí con fin_por_vidas=True, vamos directo al final
        if fin_por_vidas:
            estado = "GAME_OVER"
            return

        # Si no hay más preguntas, fin
        if indice_pregunta >= len(mazo) - 1:
            estado = "GAME_OVER"
        else:
            indice_pregunta += 1
            estado = "PREGUNTA"

    en_ejecucion = True
    while en_ejecucion:
        reloj.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_ejecucion = False

            # --------- TECLADO ----------
            if evento.type == pygame.KEYDOWN:
                if estado == "INICIO":
                    if evento.key == pygame.K_RETURN:
                        estado = "INTRO_NOMBRE"

                elif estado in ["INTRO_NOMBRE", "INTRO_NUM"]:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_input = texto_input[:-1]
                    elif evento.key == pygame.K_RETURN:
                        if estado == "INTRO_NOMBRE":
                            # input("Nombre del jugador")
                            if texto_input.strip() == "":
                                mensaje_error = "Introduce un nombre:"
                            else:
                                nombre_jugador = texto_input.strip().title()
                                texto_input = ""
                                mensaje_error = ""
                                estado = "INTRO_NUM"
                        else:
                            # ¿Cuántas preguntas quieres hacer? Elige al menos 5
                            if texto_input.strip() == "" or not texto_input.isdigit():
                                mensaje_error = f"Entrada no válida. Introduce un número del 5 al {len(preguntas)}."
                            else:
                                num = int(texto_input)
                                if num < 5 or num > len(preguntas):
                                    mensaje_error = f"Por favor, introduce un número entre 5 y {len(preguntas)}."
                                else:
                                    num_preguntas = num
                                    mazo = random.sample(preguntas, num_preguntas)
                                    indice_pregunta = 0
                                    puntuacion = 0
                                    vidas = 3
                                    fin_por_vidas = False
                                    texto_input = ""
                                    mensaje_error = ""
                                    estado = "PREGUNTA"
                    else:
                        if len(texto_input) < 20:
                            texto_input += evento.unicode

                elif estado == "FEEDBACK":
                    # Cualquier tecla → siguiente pregunta o final
                    avanzar_pregunta()

                elif estado == "GAME_OVER":
                    if evento.key == pygame.K_RETURN:
                        # Volver a elegir número de preguntas, manteniendo nombre
                        texto_input = ""
                        mensaje_error = ""
                        estado = "INTRO_NUM"

            # --------- RATÓN ----------
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado == "PREGUNTA":
                    pos = evento.pos
                    for idx, boton in enumerate(botones):
                        if boton.collidepoint(pos):
                            letras = ["A", "B", "C", "D"]
                            letra_elegida = letras[idx]
                            pregunta_actual = mazo[indice_pregunta]
                            opciones = pregunta_actual["opciones"]
                            correcta = pregunta_actual["respuesta_correcta"]

                            ultima_correcta = (letra_elegida == correcta)
                            letra_correcta = correcta
                            texto_correcto = opciones[correcta]

                            if ultima_correcta:
                                # ¡Respuesta correcta!
                                puntuacion += 1
                                estado = "FEEDBACK"
                                break
                            else:
                                # Fallo: restamos vida y comprobamos si se queda sin vidas
                                vidas -= 1
                                vidas_mostradas = vidas
                                if vidas == 0:
                                    # ✅ Si se queda sin vidas, vamos DIRECTO a GAME_OVER (sin pantalla intermedia)
                                    fin_por_vidas = True
                                    estado = "GAME_OVER"
                                else:
                                    estado = "FEEDBACK"
                                break

                elif estado == "FEEDBACK":
                    avanzar_pregunta()

        # -------------------------
        # DIBUJO
        # -------------------------
        VENTANA.fill(GRIS_OSCURO)

        if estado == "INICIO":
            titulo = FUENTE_TITULO.render(NOMBRE_JUEGO, True, ROJO_NETFLIX)
            VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))

            # ✅ sin “frase.”
            subtitulo = FUENTE_TEXTO.render("Adivina la serie o película.", True, BLANCO)
            VENTANA.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 230))

            texto_inicio = FUENTE_TEXTO.render("Pulsa ENTER para empezar", True, GRIS_CLARO)
            VENTANA.blit(texto_inicio, (ANCHO // 2 - texto_inicio.get_width() // 2, 320))

        elif estado == "INTRO_NOMBRE":
            titulo = FUENTE_TITULO.render(NOMBRE_JUEGO, True, ROJO_NETFLIX)
            VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 60))

            etiqueta = FUENTE_TEXTO.render("Nombre del jugador", True, BLANCO)
            VENTANA.blit(etiqueta, (80, 160))

            subtitulo = FUENTE_TEXTO.render("Introduce tu nombre y pulsa ENTER:", True, BLANCO)
            VENTANA.blit(subtitulo, (80, 200))

            caja = pygame.Rect(80, 240, 400, 40)
            pygame.draw.rect(VENTANA, BLANCO, caja, border_radius=5)
            texto_render = FUENTE_TEXTO.render(texto_input, True, NEGRO)
            VENTANA.blit(texto_render, (caja.x + 10, caja.y + 8))

            if mensaje_error:
                error_render = FUENTE_PEQUE.render(mensaje_error, True, ROJO)
                VENTANA.blit(error_render, (80, 300))

        elif estado == "INTRO_NUM":
            titulo = FUENTE_TITULO.render(f"¡Bienvenida al juego, {nombre_jugador}!", True, ROJO_NETFLIX)
            VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 60))

            subtitulo = FUENTE_TEXTO.render("¿Cuántas preguntas quieres hacer? (mínimo 5)", True, BLANCO)
            VENTANA.blit(subtitulo, (80, 180))

            caja = pygame.Rect(80, 230, 200, 40)
            pygame.draw.rect(VENTANA, BLANCO, caja, border_radius=5)
            texto_render = FUENTE_TEXTO.render(texto_input, True, NEGRO)
            VENTANA.blit(texto_render, (caja.x + 10, caja.y + 8))

            if mensaje_error:
                error_render = FUENTE_PEQUE.render(mensaje_error, True, ROJO)
                VENTANA.blit(error_render, (80, 290))

        elif estado == "PREGUNTA":
            pregunta_actual = mazo[indice_pregunta]
            texto_pregunta = pregunta_actual["pregunta"]
            opciones = pregunta_actual["opciones"]

            titulo = FUENTE_TITULO.render(NOMBRE_JUEGO, True, ROJO_NETFLIX)
            VENTANA.blit(titulo, (20, 20))

            # Quitamos el texto "¡Que comience el juego!" para evitar solaparlo con el título.

            info_jugador = FUENTE_PEQUE.render(
                f"Jugador: {nombre_jugador}  |  Puntuación: {puntuacion}  |  {texto_vidas(vidas)}",
                True,
                BLANCO,
            )
            VENTANA.blit(info_jugador, (20, 80))

            num_preg_text = FUENTE_PEQUE.render(
                f"Pregunta {indice_pregunta + 1}:",
                True,
                BLANCO,
            )
            VENTANA.blit(num_preg_text, (60, 120))

            # Pregunta multilínea
            dibujar_texto_multilinea(
                VENTANA,
                texto_pregunta,
                FUENTE_TEXTO,
                BLANCO,
                60,
                150,
                max_ancho=ANCHO - 120,
            )

            pos_raton = pygame.mouse.get_pos()
            for idx, (letra, opcion) in enumerate(opciones.items()):
                boton = botones[idx]
                color = GRIS_BOTON_HOVER if boton.collidepoint(pos_raton) else GRIS_BOTON
                pygame.draw.rect(VENTANA, color, boton, border_radius=8)
                pygame.draw.rect(VENTANA, ROJO_NETFLIX, boton, 2, border_radius=8)

                texto_opcion = f"{letra} {opcion}"
                dibujar_texto_en_rect(VENTANA, texto_opcion, FUENTE_TEXTO, BLANCO, boton)

            ayuda = FUENTE_PEQUE.render("Haz clic en una opción (A, B, C o D)", True, GRIS_CLARO)
            VENTANA.blit(ayuda, (60, ALTO - 40))

        elif estado == "FEEDBACK":
            VENTANA.fill(NEGRO)

            if ultima_correcta:
                # ✅ Correcta en verde y más grande
                linea1 = "¡Respuesta correcta!"
                render1 = FUENTE_FEEDBACK.render(linea1, True, VERDE)
                VENTANA.blit(render1, (ANCHO // 2 - render1.get_width() // 2, 200))
            else:
                # ✅ Incorrecta en rojo y más grande
                # Formato más claro: "Respuesta incorrecta. La respuesta correcta era A) Título"
                linea1 = f"Respuesta incorrecta. La respuesta correcta era {letra_correcta}) {texto_correcto}"
                linea2 = texto_vidas(vidas_mostradas)  # ✅ singular/plural

                # ✅ Ajuste a pantalla: partimos el texto en varias líneas centradas
                dibujar_texto_multilinea_centrado(
                    VENTANA,
                    linea1,
                    FUENTE_FEEDBACK,
                    ROJO,
                    ANCHO // 2,
                    160,
                    max_ancho=ANCHO - 120,
                    interlineado=8,
                )

                render2 = FUENTE_FEEDBACK_PEQUE.render(linea2, True, BLANCO)
                VENTANA.blit(render2, (ANCHO // 2 - render2.get_width() // 2, 300))

            texto_cont = FUENTE_PEQUE.render(
                "Pulsa cualquier tecla o haz clic para continuar",
                True,
                GRIS_CLARO,
            )
            VENTANA.blit(
                texto_cont,
                (ANCHO // 2 - texto_cont.get_width() // 2, 380),
            )

        elif estado == "GAME_OVER":
            VENTANA.fill(NEGRO)
            y = 120

            if fin_por_vidas:
                # ✅ Has perdido en rojo y más grande
                linea = "Has perdido. ¡Te has quedado sin vidas!"
                render_err = FUENTE_FEEDBACK.render(linea, True, ROJO)
                VENTANA.blit(render_err, (ANCHO // 2 - render_err.get_width() // 2, y))
                y += 70

                linea1 = f"¡Juego terminado, {nombre_jugador}!"
                render1 = FUENTE_TEXTO.render(linea1, True, BLANCO)
                VENTANA.blit(render1, (ANCHO // 2 - render1.get_width() // 2, y))
                y += 45

                linea3 = f"Tu puntuación fue: {puntuacion}/{num_preguntas}"
                render3 = FUENTE_TEXTO.render(linea3, True, BLANCO)
                VENTANA.blit(render3, (ANCHO // 2 - render3.get_width() // 2, y))

            else:
                # ✅ Enhorabuena en verde y más grande
                linea1 = f"¡Juego terminado, {nombre_jugador}!"
                render1 = FUENTE_TEXTO.render(linea1, True, BLANCO)
                VENTANA.blit(render1, (ANCHO // 2 - render1.get_width() // 2, y))
                y += 50

                linea2 = "¡Enhorabuena, has ganado!"
                render2 = FUENTE_FEEDBACK.render(linea2, True, VERDE)
                VENTANA.blit(render2, (ANCHO // 2 - render2.get_width() // 2, y))
                y += 60

                linea3 = f"Tu puntuación fue: {puntuacion}/{num_preguntas}"
                render3 = FUENTE_TEXTO.render(linea3, True, BLANCO)
                VENTANA.blit(render3, (ANCHO // 2 - render3.get_width() // 2, y))

            texto4 = FUENTE_PEQUE.render(
                "Pulsa ENTER para volver a jugar con el mismo nombre.",
                True,
                GRIS_CLARO,
            )
            VENTANA.blit(texto4, (ANCHO // 2 - texto4.get_width() // 2, ALTO - 80))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
