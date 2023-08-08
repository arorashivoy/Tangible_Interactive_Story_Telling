import pygame
import kavaad
import os


################################################################################
# Golbal Variables
################################################################################
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1840
FRAME_RATE = 24
BACKGROUND_COLOR = (51, 34, 28)


################################################################################
# Helper Functions
################################################################################


################################################################################
# Screens Class
################################################################################
class Screen:
    def __init__(self, app, screenIndex, text, img, narrator):
        self._app = app
        self._screenIndex = screenIndex
        self._textName = text
        self._imgName = img
        self._imgIndex = 0
        self._time = 0
        self._isClicking = False
        self._narrator = narrator

    def on_init(self):
        current_path = os.path.dirname(__file__)
        self._assetLoc = os.path.join(current_path, "assets")
        self._imgLoc = os.path.join(self._assetLoc, "img")
        self._textLoc = os.path.join(self._assetLoc, "text")
        self._text = pygame.image.load(os.path.join(self._textLoc, self._textName))
        self._img = []
        for i in self._imgName:
            self._img.append(pygame.image.load(os.path.join(self._imgLoc, i)))

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            return self._screenIndex + 1
        return self._screenIndex

    def on_loop(self):
        self._time += 1

        kavaad.speaking(self._narrator)
        if (self._time % FRAME_RATE == 0):
            self._imgIndex = (self._imgIndex + 1) % len(self._img)

        # if (self._time % (FRAME_RATE // 2) == 0):

    def on_render(self):
        self._app.win.fill(BACKGROUND_COLOR)
        self._app.win.blit(self._text, (50, 1030))
        self._app.win.blit(self._img[self._imgIndex], (50, 50))

        pygame.display.update()


class ScreenBut(Screen):
    def __init__(self, win, screenIndex, text, img, narrator):
        super().__init__(win, screenIndex, text, img, narrator)

    def on_init(self):
        super().on_init()

    def on_loop(self):
        if kavaad.check_next_botton(self._screenIndex):
            self._isClicking = True
        elif self._isClicking:
            self._isClicking = False
            return self._screenIndex + 1

        super().on_loop()

        return self._screenIndex


class ScreenNFC(Screen):
    def __init__(self, win, screenIndex, text, img, narrator):
        super().__init__(win, screenIndex, text, img, narrator)

    def on_init(self):
        super().on_init()

        kavaad.flush_nfc()

    def on_loop(self):
        if kavaad.check_next_botton(self._screenIndex):
            return self._screenIndex + 1

        super().on_loop()

        return self._screenIndex


class ScreenAud(Screen):
    def __init__(self, win, screenIndex, text, img, audio, narrator):
        super().__init__(win, screenIndex, text, img, narrator)
        self._loopTime = 0
        self._audioName = audio

    def on_init(self):
        super().on_init()
        self._audioLoc = os.path.join(self._assetLoc, "audio")

        pygame.mixer.music.load(os.path.join(self._audioLoc, self._audioName))
        pygame.mixer.music.play()

    def on_loop(self):
        self._loopTime += 1
        super().on_loop()
        if (not pygame.mixer.music.get_busy()):
            return self._screenIndex + 1

        return self._screenIndex


class ScreenMor(Screen):
    def __init__(self, win, screenIndex, text, img, audio, narrator):
        super().__init__(win, screenIndex, text, img, narrator)
        self._loopTime = 0
        self._audioName = audio

    def on_init(self):
        super().on_init()
        self._audioLoc = os.path.join(self._assetLoc, "audio")

        pygame.mixer.music.load(os.path.join(self._audioLoc, self._audioName))
        pygame.mixer.music.play()

    def on_loop(self):
        self._loopTime += 1
        super().on_loop()
        if (not pygame.mixer.music.get_busy()):
            return 100

        return self._screenIndex


class ScreenCho(Screen):
    def __init__(self, win, screenIndex, text, img, leftChoice, rightChoice, narrator):
        super().__init__(win, screenIndex, text, img, narrator)
        self._nextIndex = self._screenIndex
        self._leftChoice = leftChoice
        self._rightChoice = rightChoice

    def on_init(self):
        super().on_init()

    def on_loop(self):
        if kavaad.check_next_botton(self._screenIndex) == -1:
            self._isClicking = True
            self._nextIndex = self._leftChoice
        elif kavaad.check_next_botton(self._screenIndex) == 1:
            self._isClicking = True
            self._nextIndex = self._rightChoice
        elif self._isClicking:
            self._isClicking = False
            return self._nextIndex

        super().on_loop()

        return self._screenIndex


################################################################################
# App Class
################################################################################
class App:
    def __init__(self):
        self._running = True
        self.size = self.weight, self.height = SCREEN_WIDTH, SCREEN_HEIGHT

        self.win = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self._screenIndex = 0

    def on_init(self):
        global screens

        kavaad.led_on(0, 0, 0)

        pygame.init()
        pygame.display.set_caption("Kaavad Bits")

        self._running = True

        self._screens = screens
        self._screens[self._screenIndex].on_init()

    def on_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            self._running = False

        _screenIndex = self._screens[self._screenIndex].on_event(event)

        if _screenIndex != self._screenIndex:
            if (_screenIndex >= len(self._screens)):
                self._running = False
                return
            self._screenIndex = _screenIndex
            self._screens[self._screenIndex].on_init()

    def on_loop(self):
        _screenIndex = self._screens[self._screenIndex].on_loop()
        if _screenIndex != self._screenIndex:
            if (_screenIndex >= len(self._screens)):
                self._running = False
                return

            ####################################################################
            # Lights
            ####################################################################
            if _screenIndex == 3:
                kavaad.led_on(1, 0, 0)
            elif _screenIndex == 9:
                kavaad.led_on(2, 0, 0)
            elif _screenIndex == 19:
                kavaad.led_on(3, 0, 0)
            elif _screenIndex == 24:
                kavaad.led_on(4, 0, 0)
            elif _screenIndex == 26:
                kavaad.led_on(5, 0, 0)
            elif _screenIndex == 30:
                kavaad.led_on(6, 0, 0)
            elif _screenIndex == 32:
                kavaad.led_on(7, 0, 0)
            elif _screenIndex == 34:
                kavaad.led_on(8, 0, 0)
            elif _screenIndex == 44:
                kavaad.led_on(9, 0, 0)
            elif _screenIndex == 58:
                kavaad.led_on(1, 1, 1)
            elif _screenIndex == 59:
                kavaad.led_on(8, 0, 1)
            elif _screenIndex == 65:
                kavaad.led_on(9, 0, 1)
            elif _screenIndex == 67:
                kavaad.led_on(1, 1, 1)
            elif _screenIndex == 68:
                kavaad.led_on(5, 1, 0)
            elif _screenIndex == 73:
                kavaad.led_on(6, 1, 0)
            elif _screenIndex == 76:
                kavaad.led_on(7, 1, 0)
            elif _screenIndex == 79:
                kavaad.led_on(8, 1, 0)
            elif _screenIndex == 84:
                kavaad.led_on(9, 1, 0)
            elif _screenIndex == 90:
                kavaad.led_on(1, 1, 1)
            elif _screenIndex == 92:
                kavaad.led_on(8, 1, 1)
            elif _screenIndex == 94:
                kavaad.led_on(9, 1, 1)
            elif _screenIndex == 99:
                kavaad.led_on(1, 1, 1)

            self._screenIndex = _screenIndex
            self._screens[self._screenIndex].on_init()

    def on_render(self):
        self._screens[self._screenIndex].on_render()

    def on_cleanup(self):
        kavaad.cleanup()
        pygame.quit()

    def on_execute(self):
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


################################################################################
# Main Function
################################################################################
if __name__ == "__main__":
    kavaad.init()
    app = App()

    screens = [
        ScreenAud(app, 0, "kaav/K1.png", ["kaav.png"], "kaav/K1.mp3", 1),
        ScreenAud(app, 1, "kaav/K2.png", ["kaav.png"], "kaav/K2.mp3", 1),
        ScreenNFC(app, 2, "trans/T1.png", ["kaav.png"], 0),
        ScreenAud(app, 3, "kaav/K3.png", ["kaav.png"], "kaav/K3.mp3", 1),
        ScreenNFC(app, 4, "trans/T2.png", ["kaav.png"], 0),
        ScreenAud(app, 5, "kaav/K4.png", ["kaav.png"], "kaav/K4.mp3", 1),
        ScreenNFC(app, 6, "trans/T3.png", ["kaav.png"], 0),
        ScreenAud(app, 7, "kaav/K5.png", ["kaav.png"], "kaav/K5.mp3", 1),
        ScreenNFC(app, 8, "trans/T4.png", ["kaav.png"], 0),
        ScreenAud(app, 9, "kaav/K6.png", ["kaav.png"], "kaav/K6.mp3", 1),
        ScreenAud(app, 10, "kaav/K7.png", ["kaav.png"], "kaav/K7.mp3", 1),
        ScreenNFC(app, 11, "trans/T3.png", ["kaav.png"], 0),
        ScreenAud(app, 12, "croc/C1.png", ["croc.png"], "croc/C1.mp3", 2),
        ScreenAud(app, 13, "kaav/K8.png", ["kaav.png"], "kaav/K8.mp3", 1),
        ScreenAud(app, 14, "croc/C2.png", ["croc.png"], "croc/C2.mp3", 2),
        ScreenAud(app, 15, "kaav/K9.png", ["kaav.png"], "kaav/K9.mp3", 1),
        ScreenNFC(app, 16, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 17, "monke/M1.png", ["monke.png"], "monke/M1.mp3", 2),
        ScreenNFC(app, 18, "trans/T5.png", ["kaav.png"], 0),
        ScreenAud(app, 19, "kaav/K10.png", ["kaav.png"], "kaav/K10.mp3", 1),
        ScreenNFC(app, 20, "trans/T3.png", ["kaav.png"], 0),
        ScreenAud(app, 21, "kaav/K11.png", ["kaav.png"], "kaav/K11.mp3", 1),
        ScreenAud(app, 22, "kaav/K12.png", ["kaav.png"], "kaav/K12.mp3", 1),
        ScreenAud(app, 23, "crocwife/W1.png", ["crocwife.png"], "crocwife/W1.mp3", 0),
        ScreenAud(app, 24, "kaav/K13.png", ["kaav.png"], "kaav/K13.mp3", 1),
        ScreenCho(app, 25, "trans/T10.png", ["kaav.png"], 26, 68, 0),
        ScreenAud(app, 26, "kaav/K14.png", ["kaav.png"], "kaav/K14.mp3", 1),
        ScreenAud(app, 27, "croc/C3.png", ["croc.png"], "croc/C3.mp3", 2),
        ScreenAud(app, 28, "crocwife/W2.png", ["crocwife.png"], "crocwife/W2.mp3", 0),
        ScreenAud(app, 29, "kaav/K15.png", ["kaav.png"], "kaav/K15.mp3", 1),
        ScreenAud(app, 30, "croc/C4.png", ["croc.png"], "croc/C4.mp3", 2),
        ScreenAud(app, 31, "crocwife/W3.png", ["crocwife.png"], "crocwife/W3.mp3", 0),
        ScreenAud(app, 32, "kaav/K16.png", ["kaav.png"], "kaav/K16.mp3", 1),
        ScreenCho(app, 33, "trans/T11.png", ["kaav.png"], 34, 59, 0),
        ScreenAud(app, 34, "kaav/K17.png", ["kaav.png"], "kaav/K17.mp3", 1),
        ScreenNFC(app, 35, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 36, "monke/M2.png", ["monke.png"], "monke/M2.mp3", 2),
        ScreenNFC(app, 37, "trans/T8.png", ["kaav.png"], 0),
        ScreenAud(app, 38, "croc/C5.png", ["croc.png"], "croc/C5.mp3", 2),
        ScreenNFC(app, 39, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 40, "monke/M3.png", ["monke.png"], "monke/M3.mp3", 2),
        ScreenAud(app, 41, "kaav/K18.png", ["kaav.png"], "kaav/K18.mp3", 1),
        ScreenAud(app, 42, "monke/M4.png", ["monke.png"], "monke/M4.mp3", 2),
        ScreenNFC(app, 43, "trans/T8.png", ["kaav.png"], 0),
        ScreenAud(app, 44, "croc/C6.png", ["croc.png"], "croc/C6.mp3", 2),
        ScreenAud(app, 45, "kaav/K19.png", ["kaav.png"], "kaav/K19.mp3", 1),
        ScreenAud(app, 46, "croc/C7.png", ["croc.png"], "croc/C7.mp3", 2),
        ScreenAud(app, 47, "kaav/K20.png", ["kaav.png"], "kaav/K20.mp3", 1),
        ScreenNFC(app, 48, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 49, "monke/M5.png", ["monke.png"], "monke/M5.mp3", 2),
        ScreenAud(app, 50, "kaav/K21.png", ["kaav.png"], "kaav/K21.mp3", 1),
        ScreenAud(app, 51, "monke/M6.png", ["monke.png"], "monke/M6.mp3", 2),
        ScreenAud(app, 52, "kaav/K22.png", ["kaav.png"], "kaav/K22.mp3", 1),
        ScreenNFC(app, 53, "trans/T8.png", ["kaav.png"], 0),
        ScreenAud(app, 54, "croc/C8.png", ["croc.png"], "croc/C8.mp3", 2),
        ScreenAud(app, 55, "kaav/K23.png", ["kaav.png"], "kaav/K23.mp3", 1),
        ScreenNFC(app, 56, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 57, "monke/M7.png", ["monke.png"], "monke/M7.mp3", 2),
        ScreenMor(app, 58, "mor/MoA.png", ["kaav.png"], "mor/MoA.mp3", 0),
        ScreenAud(app, 59, "kaav/K24.png", ["kaav.png"], "kaav/K24.mp3", 1),
        ScreenNFC(app, 60, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 61, "monke/M8.png", ["monke.png"], "monke/M8.mp3", 2),
        ScreenNFC(app, 62, "trans/T8.png", ["kaav.png"], 0),
        ScreenAud(app, 63, "croc/C9.png", ["croc.png"], "croc/C9.mp3", 2),
        ScreenNFC(app, 64, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 65, "monke/M9.png", ["monke.png"], "monke/M9.mp3", 2),
        ScreenAud(app, 66, "kaav/K25.png", ["kaav.png"], "kaav/K25.mp3", 1),
        ScreenMor(app, 67, "mor/MoB.png", ["kaav.png"], "mor/MoB.mp3", 0),
        ScreenAud(app, 68, "kaav/K26.png", ["kaav.png"], "kaav/K26.mp3", 1),
        ScreenAud(app, 69, "croc/C10.png", ["croc.png"], "croc/C10.mp3", 2),
        ScreenAud(app, 70, "crocwife/W4.png", ["crocwife.png"], "crocwife/W4.mp3", 0),
        ScreenAud(app, 71, "kaav/K27.png", ["kaav.png"], "kaav/K27.mp3", 1),
        ScreenNFC(app, 72, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 73, "monke/M10.png", ["monke.png"], "monke/M10.mp3", 2),
        ScreenNFC(app, 74, "trans/T8.png", ["kaav.png"], 0),
        ScreenAud(app, 75, "croc/C5.png", ["croc.png"], "croc/C5.mp3", 2),
        ScreenAud(app, 76, "kaav/K28.png", ["kaav.png"], "kaav/K28.mp3", 1),
        ScreenCho(app, 77, "trans/T12.png", ["kaav.png"], 78, 91, 0),
        ScreenNFC(app, 78, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 79, "monke/M11.png", ["monke.png"], "monke/M11.mp3", 2),
        ScreenNFC(app, 80, "trans/T8.png", ["kaav.png"], 0),
        ScreenAud(app, 81, "croc/C6.png", ["croc.png"], "croc/C6.mp3", 2),
        ScreenAud(app, 82, "kaav/K29.png", ["kaav.png"], "kaav/K29.mp3", 1),
        ScreenNFC(app, 83, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 84, "monke/M12.png", ["monke.png"], "monke/M12.mp3", 2),
        ScreenAud(app, 85, "kaav/K30.png", ["kaav.png"], "kaav/K30.mp3", 1),
        ScreenAud(app, 86, "monke/M13.png", ["monke.png"], "monke/M13.mp3", 2),
        ScreenAud(app, 87, "crocwife/W5.png", ["crocwife.png"], "crocwife/W5.mp3", 0),
        ScreenAud(app, 88, "monke/M14.png", ["monke.png"], "monke/M14.mp3", 2),
        ScreenAud(app, 89, "kaav/K31.png", ["kaav.png"], "kaav/K31.mp3", 1),
        ScreenMor(app, 90, "mor/MoC.png", ["kaav.png"], "mor/MoC.mp3", 0),
        ScreenNFC(app, 91, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 92, "monke/M15.png", ["monke.png"], "monke/M15.mp3", 2),
        ScreenNFC(app, 93, "trans/T8.png", ["kaav.png"], 0),
        ScreenAud(app, 94, "croc/C6.png", ["croc.png"], "croc/C6.mp3", 2),
        ScreenAud(app, 95, "kaav/K32.png", ["kaav.png"], "kaav/K32.mp3", 1),
        ScreenNFC(app, 96, "trans/T9.png", ["kaav.png"], 0),
        ScreenAud(app, 97, "monke/M16.png", ["monke.png"], "monke/M16.mp3", 2),
        ScreenAud(app, 98, "kaav/K33.png", ["kaav.png"], "kaav/K33.mp3", 1),
        ScreenMor(app, 99, "mor/MoD.png", ["kaav.png"], "mor/MoD.mp3", 0),
        ScreenNFC(app, 100, "end/end.png", ["kaav.png"], 0),
        ScreenAud(app, 101, "end/ask.png", ["kaav.png"], "end/ask.mp3", 0),
        ScreenAud(app, 102, "end/EM.png", ["kaav.png"], "end/EM.mp3", 0),
        ScreenNFC(app, 103, "end/end.png", ["kaav.png"], 0),
        ScreenAud(app, 104, "end/ask.png", ["kaav.png"], "end/ask.mp3", 0),
        ScreenAud(app, 105, "end/EC.png", ["kaav.png"], "end/EC.mp3", 0),
        ScreenNFC(app, 106, "end/end.png", ["kaav.png"], 0),
        ScreenAud(app, 107, "end/ask.png", ["kaav.png"], "end/ask.mp3", 0),
        ScreenAud(app, 108, "end/EK.png", ["kaav.png"], "end/EK.mp3", 0),






    ]

    app.on_init()

    try:
        app.on_execute()
    except KeyboardInterrupt:
        app.on_cleanup()
