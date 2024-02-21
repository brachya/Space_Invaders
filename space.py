import random
from typing import Optional
import pygame
import os
import json

SEP = os.sep

#                HEAD
#  set window in middle of the screen
os.environ["SDL_VIDEO_CENTERED"] = "1"
# pygame initiate
pygame.init()


class HighScore:
    highscore: list[dict[str, int | str | None]] = []
    temp: dict[str, int | str | None] = {}

    @staticmethod
    def add_score():
        HighScore.temp["name"] = actor.get_name()
        HighScore.temp["score"] = actor.get_score()
        HighScore.highscore.append(HighScore.temp.copy())
        if HighScore.highscore:
            HighScore.highscore.sort(key=lambda x: x["score"], reverse=True)  # type: ignore
        HighScore.highscore = HighScore.highscore[:10]

    @staticmethod
    def get_highscore():
        return HighScore.highscore

    @staticmethod
    def set_highscore(high_file: list[dict[str, int | str | None]]):
        HighScore.highscore = high_file

    @staticmethod
    def reset():
        HighScore.highscore = []


class Actor:
    actors: dict[str, dict[str, int]] = {}

    def __init__(self):
        self.new_actor()

    def new_actor(self):
        self.__name: Optional[str] = None
        self.__score: int = 0
        self.__level: int = 1
        self.player_life: int = 3
        self.player_life2: int = 3

    def set_name(self, name: str):
        self.__name = name

    def get_name(self) -> str | None:
        return self.__name

    def hit(self, plane: int):
        if plane == 1:
            self.player_life -= 1
            if not self.player_life:
                return True
        if plane == 2:
            self.player_life2 -= 1
            if not self.player_life2:
                return True

    def cheat(self, plane: int):
        if plane == 1:
            self.player_life += 10
        if plane == 2:
            self.player_life2 += 10

    def health(self, plane: int):
        if plane == 1:
            self.player_life += 1
        if plane == 2:
            self.player_life2 += 1

    def get_players(self, title: str) -> None:
        word(screen, title, "aqua", screen.get_width() // 2, screen.get_height() // 13)
        if self.actors:
            n = 1
            for p in self.actors:
                word(
                    screen,
                    f"{n}.  {p} - {self.actors[p]['level']}",
                    "aqua",
                    screen.get_width() // 2,
                    screen.get_height() // 13 + screen.get_height() // 10 * n,
                )
                n += 1

    def delete_player(self, player_num: int):
        player_num = (player_num - 1) % len(list(self.actors.keys()))
        chosen = list(self.actors.keys())[player_num]
        del self.actors[chosen]

    def load_player(self, player_num: int) -> None:
        player_num = (player_num - 1) % len(list(self.actors.keys()))
        chosen = list(self.actors.keys())[player_num]
        self.__name = chosen
        self.__score = self.actors[chosen]["score"]
        self.__level = self.actors[chosen]["level"]
        self.player_life = self.actors[chosen]["player_life"]
        self.player_life2 = self.actors[chosen]["player_life2"]

    def reset_life(self) -> None:
        self.player_life = 3
        self.player_life2 = 3

    def get_life(self, plane: int) -> int:
        if plane == 1:
            return self.player_life
        elif plane == 2:
            return self.player_life2
        else:
            return 0

    def set_score(self, new_score: int):
        self.__score = new_score

    def more_score(self, more_score: int):
        self.__score += more_score

    def next_level(self):
        self.__level += 1

    def get_level(self) -> int:
        return self.__level

    def reset_level(self):
        self.__level = 1

    def reset(self):
        self.set_score(0)
        self.reset_life()
        self.reset_level()

    def get_score(self):
        return self.__score

    def to_save(self):
        temp = {}
        self.current_actor = {
            "score": self.__score,
            "level": self.__level,
            "player_life": self.player_life,
            "player_life2": self.player_life2,
        }
        if self.actors:
            for player in self.actors:
                temp[player] = self.actors[player]
        temp[self.__name] = self.current_actor
        self.actors = temp

    def save(self):
        self.to_save()
        put = {"players": self.actors, "highscore": HighScore.get_highscore()}
        if not os.path.exists(f"Settings"):
            os.makedirs("Settings")
        with open(f"Settings{SEP}actors.json", "w+") as s:
            json.dump(put, s, indent=2)

    def load(self):
        try:
            with open(f"Settings{SEP}actors.json", "r+") as s:
                a = json.load(s)
                if a["highscore"]:
                    HighScore.set_highscore(a["highscore"])
                if a["players"]:
                    self.actors = a["players"]
        except:
            self.new_actor()


actor = Actor()
actor.load()


class Settings:
    @staticmethod
    def default() -> tuple[
        pygame.Surface,
        tuple[int, int],
        list[pygame.Surface],
        int,
        bool,
        pygame.Surface,
        list[str],
    ]:
        # screen size
        screen: pygame.Surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        # for turning to fullscreen and reverse
        full_scr: bool = False
        pygame.display.set_caption("Space_Ship")
        last_scr: tuple[int, int] = (800, 600)
        bs: list[str] = [
            f"pic{SEP}background.jpg",
            f"pic{SEP}background1.jpg",
            f"pic{SEP}background2.jpg",
            f"pic{SEP}background3.jpg",
        ]
        backgrounds: list[pygame.Surface] = Settings.load_backgrounds(bs)
        # changing backgrounds
        back_place: int = 0
        background: pygame.Surface = pygame.transform.scale(
            backgrounds[back_place], (screen.get_width(), screen.get_height())
        )

        return screen, last_scr, backgrounds, back_place, full_scr, background, bs

    @staticmethod
    def settings_dump():
        global screen
        global last_scr
        global back_place
        global backgrounds
        global full_scr
        global bs
        global actor
        actor.save()
        setting: dict[str, tuple[int, int] | str | int] = {
            "scr": screen.get_size(),
            "last_scr": last_scr,
            "back": bs[back_place],
            "back_place": back_place,
            "full": full_scr,
            "backgrounds": bs,
        }
        if not os.path.exists(f"Settings"):
            os.makedirs("Settings")
        with open(f"Settings{SEP}settings.json", "w+") as s:
            json.dump(setting, s, indent=2)

    @staticmethod
    def settings_load() -> tuple[
        pygame.Surface,
        tuple[int, int],
        list[pygame.Surface],
        int,
        bool,
        pygame.Surface,
        list[str],
    ]:
        try:
            with open(f"Settings{SEP}settings.json", "r") as s:
                se = s.read()
                if se:
                    se = json.loads(se)
                    last_scr: tuple[int, int] = se["last_scr"]
                    if se["full"]:
                        scr: pygame.Surface = pygame.display.set_mode(
                            (0, 0), pygame.FULLSCREEN
                        )
                    else:
                        scr: pygame.Surface = pygame.display.set_mode(
                            (int(se["scr"][0]), int(se["scr"][1])), pygame.RESIZABLE
                        )
                    bs: list[str] = se["backgrounds"]
                    back_place: int = se["back_place"]
                    bls: list[pygame.Surface] = Settings.load_backgrounds(bs)
                    background: pygame.Surface = pygame.transform.scale(
                        bls[back_place], (int(se["scr"][0]), int(se["scr"][1]))
                    )
                    full_scr: bool = se["full"]

        except:
            return Settings.default()
        else:
            return (
                scr,
                last_scr,
                bls,
                back_place,
                full_scr,
                background,
                bs,
            )

    @staticmethod
    def load_backgrounds(list_of_background: list[str]) -> list[pygame.Surface]:
        return [pygame.image.load(b).convert() for b in list_of_background]


(
    screen,
    last_scr,
    backgrounds,
    back_place,
    full_scr,
    background,
    bs,
) = Settings.settings_load()


class Sound:
    sound_on = True
    pf = pygame.mixer.Sound(f"sound{SEP}player_blaster.mp3")
    ef = pygame.mixer.Sound(f"sound{SEP}alien_blaster.mp3")


def new_game():
    actor.reset_level()
    actor.reset_life()
    actor.set_score(0)
    game()


def word(sface: pygame.Surface, word: str, color: str, x: int, y: int, size: int = 60):
    """
    taking text and making a photo that hold the text
    """
    w = pygame.font.SysFont("arial.ttf", size).render(word, True, color)
    p = w.get_rect()
    p.center = (x, y)
    sface.blit(w, p.topleft if x else (x, y))


def en_creator(enemy_group, enemy_object, y_jump: int, en_amount: int, life: int):
    """
    this will create enemies
    enemy_group: this will has the enemies
    enemy_object: enemy class
    y_jump: distance between the raws
    en_amount: num of raws
    """
    for y in range(y_jump - 1, y_jump * en_amount, y_jump):
        for x in range(y_jump + 1, screen.get_width() - 1, screen.get_width() // 4):
            enemy_group.add(enemy_object(x, y, life))


def change_back():
    """
    taking the current background and pulling the next background and changing the screen background
    """
    global back_place
    global background
    global backgrounds
    back_place = (back_place + 1) % len(backgrounds)
    background = pygame.transform.scale(
        backgrounds[back_place], (screen.get_width(), screen.get_height())
    )


def res_change():
    """
    changing the resolution by finding the current and using the next resolutin
    """
    global screen
    global last_scr
    global full_scr
    if not full_scr:
        res = [(800, 600), (960, 700), (1200, 760)]
        p = res.index((screen.get_width(), screen.get_height()))
        new = res[(p + 1) % len(res)]
        last_scr = new
        screen = pygame.display.set_mode(new)
        settings()


def mute():
    Sound.sound_on = not Sound.sound_on
    settings()


def fullscreen():
    global screen
    global full_scr
    global last_scr
    if not full_scr:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        full_scr = True
        settings()
    else:
        screen = pygame.display.set_mode(last_scr, pygame.RESIZABLE)
        full_scr = False
        settings()


def settings():
    global screen
    buttons = pygame.sprite.Group()
    menu = pygame.Rect(
        screen.get_width() // 2 - screen.get_width() // 4,
        screen.get_height() // 2 - screen.get_height() // 4,
        screen.get_width() // 2,
        screen.get_height() // 2,
    )
    b_w = menu.width // 2
    b_h = menu.height // 4
    setting = True
    bcolor = "black"
    buttons.add(
        Click_Button(
            "Background",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            menu.y + menu.height // 3 - (b_h // 2) - b_h * 2,
            b_w,
            b_h,
            bcolor,
            change_back,
        )
    )
    buttons.add(
        Click_Button(
            "Resulotion",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            menu.y + menu.height // 3 - (b_h // 2) - b_h,
            b_w,
            b_h,
            bcolor,
            res_change,
        )
    )
    buttons.add(
        Click_Button(
            "Fullscreen",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            menu.y + menu.height // 3 - (b_h // 2),
            b_w,
            b_h,
            bcolor,
            fullscreen,
        )
    )
    buttons.add(
        Click_Button(
            "Load",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            b_h + menu.y + menu.height // 3 - (b_h // 2),
            b_w,
            b_h,
            bcolor,
            open_screen,
        )
    )
    buttons.add(
        Click_Button(
            "Mute" if Sound.sound_on else "UnMute",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            b_h * 2 + menu.y + menu.height // 3 - (b_h // 2),
            b_w,
            b_h,
            bcolor,
            mute,
        )
    )
    buttons.add(
        Click_Button(
            "Back",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            b_h * 3 + menu.y + menu.height // 3 - (b_h // 2),
            b_w,
            b_h,
            bcolor,
            main,
        )
    )
    while setting:
        screen.blit(
            pygame.transform.scale(
                background, (screen.get_width(), screen.get_height())
            ),
            (0, 0),
        )
        buttons.draw(screen)
        pos = pygame.mouse.get_pos()
        buttons.update(pos, False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Settings.settings_dump()
                quit()
            if event.type == pygame.RESIZABLE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event.pos, True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    setting = False
                    main()
        pygame.display.update()
        pygame.time.Clock().tick(60)


def main():
    global actor
    global screen
    buttons: pygame.sprite.Group[Button] = pygame.sprite.Group()
    menu = pygame.Rect(
        screen.get_width() // 2 - screen.get_width() // 4,
        screen.get_height() // 2 - screen.get_height() // 4,
        screen.get_width() // 2,
        screen.get_height() // 2,
    )
    b_w = menu.width // 2
    b_h = menu.height // 4
    new_check = 0 if actor.get_level() > 1 else b_h
    bcolor = "black"
    if actor.get_level() > 1:
        buttons.add(
            Click_Button(
                "New Game",
                screen,
                menu.x + menu.width // 2 - (b_w // 2),
                menu.y + menu.height // 3 - (b_h // 2) - b_h,
                b_w,
                b_h,
                bcolor,
                new_game,
            )
        )
        buttons.add(
            Click_Button(
                "Continue",
                screen,
                menu.x + menu.width // 2 - (b_w // 2),
                menu.y + menu.height // 3 - (b_h // 2),
                b_w,
                b_h,
                bcolor,
                game,
            )
        )
    else:
        buttons.add(
            Click_Button(
                "New Game",
                screen,
                menu.x + menu.width // 2 - (b_w // 2),
                menu.y + menu.height // 3 - (b_h // 2) - new_check,
                b_w,
                b_h,
                bcolor,
                new_game,
            )
        )
    buttons.add(
        Click_Button(
            "HighScore",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            menu.y + menu.height // 3 - (b_h // 2) + b_h - new_check,
            b_w,
            b_h,
            bcolor,
            score,
        )
    )
    buttons.add(
        Click_Button(
            "Settings",
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            menu.y + menu.height // 3 - (b_h // 2) + b_h * 2 - new_check,
            b_w,
            b_h,
            bcolor,
            settings,
        )
    )
    run = True
    while run:
        screen.blit(
            pygame.transform.scale(
                background, (screen.get_width(), screen.get_height())
            ),
            (0, 0),
        )
        word(screen, f"Hello {actor.get_name()}", "aqua", 0, screen.get_height() // 100)
        word(
            screen,
            f"Your score:{actor.get_score()}",
            "aqua",
            0,
            screen.get_height() - screen.get_height() // 10,
        )
        buttons.draw(screen)
        pos = pygame.mouse.get_pos()
        buttons.update(pos, False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Settings.settings_dump()
                quit()
            if event.type == pygame.RESIZABLE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event.pos, True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if actor.get_level == 1:
                        new_game()
                    else:
                        game()
                    # run = False
                if event.key == pygame.K_ESCAPE:
                    Settings.settings_dump()
                    quit()
        pygame.display.update()
        pygame.time.Clock().tick(60)


def remove_player_screen():
    global actor
    global screen
    run = True
    while run:
        screen.blit(
            pygame.transform.scale(
                background, (screen.get_width(), screen.get_height())
            ),
            (0, 0),
        )
        actor.get_players("Remove player by number:")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Settings.settings_dump()
                quit()
            if event.type == pygame.RESIZABLE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Settings.settings_dump()
                    quit()
                actor.delete_player(int(event.unicode))
                run = False
        pygame.display.update()
        pygame.time.Clock().tick(60)
    open_screen()


def open_screen():
    global actor
    global screen

    buttons = pygame.sprite.Group()
    buttons_to_write = pygame.sprite.Group()
    menu = pygame.Rect(
        screen.get_width() // 2 - screen.get_width() // 4,
        screen.get_height() // 2 - screen.get_height() // 4,
        screen.get_width() // 2,
        screen.get_height() // 2,
    )
    b_w = menu.width // 2
    b_h = menu.height // 4
    run = True
    name = ""
    buttons_to_write.add(
        Write_Button(
            name,
            screen,
            menu.x + menu.width // 2 - (b_w // 2),
            menu.y + menu.height // 3 - (b_h // 2) - b_h,
            b_w,
            b_h,
            "black",
        )
    )
    buttons.add(
        Click_Button(
            "New",
            screen,
            screen.get_width() // 10,
            screen.get_height() - 100,
            screen.get_width() // 6,
            screen.get_height() // 10,
            "black",
            actor.new_actor,
        )
    )
    buttons.add(
        Click_Button(
            "Remove",
            screen,
            screen.get_width() // 10 * 4,
            screen.get_height() - 100,
            screen.get_width() // 6,
            screen.get_height() // 10,
            "black",
            remove_player_screen,
        )
    )
    playing = actor.get_name()
    new = False
    while run:
        screen.blit(
            pygame.transform.scale(
                background, (screen.get_width(), screen.get_height())
            ),
            (0, 0),
        )
        pos = pygame.mouse.get_pos()
        if playing:
            actor.save()
            playing = False
            actor.new_actor()
        if actor.get_name():
            run = False
        if actor.actors and not actor.get_name() and not new:
            actor.get_players("Choose player by number:")
            buttons.draw(screen)
            buttons.update(pos, False)
        if new or not actor.actors and not actor.get_name():
            word(
                screen,
                "Enter your name:",
                "aqua",
                screen.get_width() // 2,
                screen.get_height() // 13,
            )
            buttons_to_write.draw(screen)
            buttons_to_write.update(name)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event.pos, True)
                new = True

            if event.type == pygame.QUIT:
                Settings.settings_dump()
                quit()
            if event.type == pygame.RESIZABLE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Settings.settings_dump()
                    quit()
                if actor.actors and not actor.get_name() and not new:
                    if event.key == pygame.K_RETURN:
                        actor.load_player(1)
                    else:
                        actor.load_player(int(event.unicode))
                else:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                    if event.key == pygame.K_RETURN:
                        actor.set_name(name[:-1])
                        run = False
        pygame.display.update()
        pygame.time.Clock().tick(60)
    main()


def score():
    global actor
    global screen
    buttons = pygame.sprite.Group()
    place_high = screen.get_height() // 10
    buttons.add(
        Click_Button(
            "Reset",
            screen,
            screen.get_width() // 10,
            screen.get_height() - 100,
            screen.get_width() // 6,
            screen.get_height() // 10,
            "black",
            HighScore.reset,
        )
    )
    run = True
    back_main = False
    while run:
        screen.blit(
            pygame.transform.scale(
                background, (screen.get_width(), screen.get_height())
            ),
            (0, 0),
        )
        buttons.draw(screen)
        pos = pygame.mouse.get_pos()
        buttons.update(pos, False)
        n = 1
        word(screen, f"High Score", "aqua", screen.get_width() // 2, place_high - 50)
        for sc in HighScore.highscore:
            word(
                screen,
                f"{n}. {sc['name']} - {sc['score']}",
                "aqua",
                screen.get_width() // 2,
                place_high + 50 * n,
            )
            n += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Settings.settings_dump()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                    back_main = True
                if event.key == pygame.K_ESCAPE:
                    run = False
                    back_main = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(event.pos, True)
        pygame.display.update()
        pygame.time.Clock().tick(60)
    if back_main:
        main()


def pause():
    img = pygame.transform.scale(
        pygame.image.load(f"pic{SEP}button.png"),
        (screen.get_width() // 2, screen.get_height() // 2),
    )
    run = True
    to_main = False
    while run:
        screen.blit(
            img,
            (
                screen.get_width() // 2 - screen.get_width() // 4,
                screen.get_height() // 2 - screen.get_height() // 4,
            ),
        )
        word(
            screen,
            "Pause",
            "black",
            screen.get_width() // 2,
            screen.get_height() // 2 - screen.get_height() // 8,
            80,
        )
        word(
            screen,
            "escape to main",
            "black",
            screen.get_width() // 2,
            screen.get_height() // 2,
            40,
        )
        word(
            screen,
            "enter to return",
            "black",
            screen.get_width() // 2,
            screen.get_height() // 2 + 60,
            40,
        )
        word(
            screen,
            "s to mute" if Sound.sound_on else "s to unmute",
            "black",
            screen.get_width() // 2,
            screen.get_height() // 2 + 120,
            40,
        )
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                Settings.settings_dump()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    run = False
                if e.key == pygame.K_ESCAPE:
                    to_main = True
                    run = False
                if e.key == pygame.K_s:
                    Sound.sound_on = not Sound.sound_on
    return to_main


def game(player2_on: bool = False):
    global actor
    cheat = False
    fires: pygame.sprite.Group[Fire] = pygame.sprite.Group()
    players: pygame.sprite.Group[Player] = pygame.sprite.Group()
    enemies: pygame.sprite.Group[Enemy] = pygame.sprite.Group()
    enfire: pygame.sprite.Group[Fire] = pygame.sprite.Group()
    if actor.get_life(1) > 0:
        pla = Player1(1, f"pic{SEP}space_player1.png")
        players.add(pla)
    pla2_on = player2_on
    if pla2_on:
        if actor.get_life(2) > 0:
            pla2 = Player2(2, f"pic{SEP}2space_player1.png")
            players.add(pla2)
    run = True
    # h = Health((100, 100))
    back_main = False
    next_level = False
    difficult = actor.get_level()
    boss = True if not difficult % 5 else False
    en_creator(
        enemies,
        Enemy,
        int((screen.get_height() // 12) * 1.1),
        difficult // 5 + 1,
        difficult % 5 + 1,
    )
    while run:
        screen.blit(
            pygame.transform.scale(
                background, (screen.get_width(), screen.get_height())
            ),
            (0, 0),
        )
        word(
            screen,
            f"Score {actor.get_score()}",
            "aqua",
            screen.get_width() // 2,
            screen.get_height() - 100,
        )
        word(
            screen,
            f"Level {actor.get_level()}",
            "aqua",
            screen.get_width() // 2,
            screen.get_height() // 20,
        )
        key = pygame.key.get_pressed()
        fires.draw(screen)
        enfire.draw(screen)
        enfire.update()
        players.draw(screen)
        players.update(key, fires, PFire, cheat)
        enemies.draw(screen)
        enemies.update(enfire, EnemyFire)
        fires.update()
        # collisions
        if pygame.sprite.groupcollide(fires, enemies, True, True):
            actor.more_score(1)
        pygame.sprite.groupcollide(enfire, players, True, True)
        pygame.sprite.groupcollide(players, enemies, True, True)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                Settings.settings_dump()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_k:
                    cheat = not cheat
                if e.key == pygame.K_ESCAPE:
                    back_main = pause()
                    run = False if back_main else True
                if e.key == pygame.K_SPACE and not pla2_on:
                    pla2_on = True
                    if actor.get_life(2) > 0:
                        pla2 = Player2(2, f"pic{SEP}2space_player1.png")
                        players.add(pla2)
        if not enemies and boss:
            enemies.add(
                BossEnemy(
                    screen.get_width() // 2,
                    screen.get_width() // 10,
                    random.randint(10, 30),
                )
            )
            boss = False
        if not boss and not len(enemies):
            word(
                screen,
                "NEXT LEVEL",
                "aqua",
                screen.get_width() // 2,
                screen.get_height() // 3,
                screen.get_height() // 4,
            )
            next_level = True
            run = False
            actor.next_level()
            if actor.get_life(1) == 0:
                actor.health(1)
            if actor.get_life(2) == 0:
                actor.health(2)
        if not actor.get_life(1) and (not actor.get_life(2) or not pla2_on):
            HighScore.add_score()
            actor.reset()
            run = False
            score()
        pygame.time.Clock().tick(60)
        pygame.display.flip()
    if back_main:
        main()
    if next_level:
        game(pla2_on)


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        sface: pygame.Surface,
        x: int,
        y: int,
        x_size: int,
        y_size: int,
        color: str,
    ):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(f"pic{SEP}button.png"), (x_size, y_size)
        )
        self.text = pygame.transform.scale(
            pygame.font.SysFont("News706 BT.ttf", y_size).render(text, True, color),
            (x_size, y_size),
        )
        self.text_t = text
        self.y_size = y_size
        self.color_text = color
        self.on_color = "blue"
        self.sface: pygame.Surface = sface
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.center = (x + x_size // 2, y + y_size // 2)

    def update(
        self,
        pos: tuple[float, float] = (0, 0),
        click: bool = False,
        input: str | None = None,
        *args,
        **kwargs,
    ):
        super().update()
        self.sface.blit(self.image, (self.x, self.y))


class Write_Button(Button):
    def __init__(
        self,
        text: str,
        sface: pygame.Surface,
        x: int,
        y: int,
        x_size: int,
        y_size: int,
        color: str,
    ):
        super().__init__(text, sface, x, y, x_size, y_size, color)

    def update(self, input: str, *args: type, **kwargs: type) -> None:
        super().update(input, *args, **kwargs)
        self.w = (
            pygame.font.SysFont("arial.ttf", self.y_size)
            .render(input, True, self.color_text)
            .get_width()
            + 10
        )
        self.sface.blit(
            pygame.transform.scale(
                pygame.font.SysFont("News706 BT.ttf", self.y_size).render(
                    input, True, self.color_text
                ),
                (min(self.w, self.rect.width), self.rect.height),
            ),
            (self.x, self.y),
        )


class Click_Button(Button):
    def __init__(
        self,
        text: str,
        sface: pygame.Surface,
        x: int,
        y: int,
        x_size: int,
        y_size: int,
        color: str,
        des,  # type: ignore
    ):
        super().__init__(text, sface, x, y, x_size, y_size, color)
        self.mission = des

    def update(self, pos: tuple[int, int], click: bool):
        super().update(pos, click)
        self.sface.blit(self.text, (self.x, self.y))
        if self.rect.collidepoint(pos):
            self.sface.blit(
                pygame.transform.scale(
                    pygame.font.SysFont("News706 BT.ttf", self.y_size).render(
                        self.text_t, True, self.on_color
                    ),
                    (self.rect.width, self.rect.height),
                ),
                (self.x, self.y),
            )
            if click:
                self.mission()


class Custom_Button(Button):
    def __init__(
        self,
        text: str,
        sface: pygame.Surface,
        x: int,
        y: int,
        x_size: int,
        y_size: int,
        color: str,
    ):
        super().__init__(text, sface, x, y, x_size, y_size, color)

    def update(self, pos: tuple[int, int], click: bool) -> bool | tuple[bool, bool]:
        super().update(pos, click)
        self.sface.blit(self.text, (self.x, self.y))
        if self.rect.collidepoint(pos):
            self.sface.blit(
                pygame.transform.scale(
                    pygame.font.SysFont("News706 BT.ttf", self.y_size).render(
                        self.text_t, True, self.on_color
                    ),
                    (self.rect.width, self.rect.height),
                ),
                (self.x, self.y),
            )
            if click:
                return False, True
            else:
                return True
        return False


class Player(pygame.sprite.Sprite):
    def __init__(self, num: int, image: str):
        self.plane = num
        super().__init__()
        self.life = actor.get_life(self.plane)
        self.current = image
        self.image = pygame.transform.scale(
            pygame.image.load(self.current),
            (screen.get_width() // 8, screen.get_height() // 6),
        )
        self.rect = self.image.get_rect()
        self.rect.center = (
            screen.get_width() // 2,
            screen.get_height() - self.rect.height,
        )
        self.image_life = pygame.transform.scale(
            pygame.image.load(image),
            (
                screen.get_width() // (screen.get_width() / 20),
                screen.get_height() // (screen.get_height() / 20),
            ),
        )
        self.reload = 0
        self.firing = False
        self.heat = 10

    def shoot(
        self,
        bullets: pygame.sprite.Group,
        bullet: pygame.sprite.Sprite,
        cheat: bool,
    ):
        if (not self.reload and not self.firing and self.heat > 0) or cheat:
            bullets.add(bullet(self.rect.center))
            self.heat -= 1
            self.firing = True

    def update(self, key, fires_group, bullet, cheat):
        super().update()
        self.life = actor.get_life(self.plane)
        self.reload = self.reload + 1 if self.firing else self.reload
        self.heat = self.heat + 0.02 if self.heat < 10 else self.heat
        if self.reload == 15:
            self.reload = 0
            self.firing = False
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width() - 1
        if self.rect.left < 0:
            self.rect.left = 1
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height() - 1
        if self.rect.top < 0:
            self.rect.top = 1

    def position(self):
        return self.rect.center

    def kill(self):
        if actor.hit(self.plane):
            return super().kill()

    def cheat(self, code: str):
        if code == "l":
            actor.cheat(self.plane)


class Player1(Player):
    def __init__(self, num: int, image: str):
        super().__init__(num, image)
        self.images: list[pygame.Surface] = []
        for i in range(4):
            self.images.append(
                pygame.transform.scale(
                    pygame.image.load(f"pic{SEP}space_player{i + 1}.png"),
                    (screen.get_width() // 8, screen.get_height() // 6),
                )
            )
        self.rect.center = (
            screen.get_width() - screen.get_width() // 3,
            screen.get_height() - self.rect.height,
        )
        self.count = 0
        self.poss = 0

    def update(self, key, fires_group, bullet, cheat):
        self.count = self.count + 1 if self.count < 4 else 0
        if self.count == 3:
            self.poss = (self.poss + 1) % 4
            self.image = self.images[self.poss]
        [screen.blit(self.image_life, (15 * int(li), 0)) for li in range(self.life)]
        word(screen, "I" * int(self.heat), "red", 100, 100)
        if key[pygame.K_RETURN]:
            self.shoot(fires_group, bullet, cheat)
        if key[pygame.K_RIGHT]:
            self.rect.x += int(pygame.display.get_window_size()[0] / 100)
        if key[pygame.K_LEFT]:
            self.rect.x -= int(pygame.display.get_window_size()[0] / 100)
        if key[pygame.K_DOWN]:
            self.rect.y += int(pygame.display.get_window_size()[1] / 100)
        if key[pygame.K_UP]:
            self.rect.y -= int(pygame.display.get_window_size()[1] / 100)
        if key[pygame.K_l]:
            self.cheat("l")
        super().update(key, fires_group, bullet, cheat)


class Player2(Player):
    def __init__(self, num, image):
        super().__init__(num, image)
        self.rect.center = (
            0 + screen.get_width() // 3,
            screen.get_height() - self.rect.height,
        )
        self.images: list[pygame.Surface] = []
        for i in range(5):
            self.images.append(
                pygame.transform.scale(
                    pygame.image.load(f"pic{SEP}2space_player{i + 1}.png"),
                    (screen.get_width() // 8, screen.get_height() // 6),
                )
            )
        self.count = 0
        self.poss = 0

    def update(self, key, fires_group, bullet, cheat):
        self.count = self.count + 1 if self.count < 4 else 0
        if self.count == 3:
            self.poss = (self.poss + 1) % 4
            self.image: pygame.Surface = self.images[self.poss]
        [
            screen.blit(self.image_life, ((screen.get_width() - 15) - 15 * int(li), 0))
            for li in range(self.life)
        ]
        word(
            screen,
            "I" * int(self.heat),
            "green",
            screen.get_width() - (screen.get_width() // 5),
            100,
        )
        if key[pygame.K_SPACE]:
            self.shoot(fires_group, bullet, cheat)
        if key[pygame.K_d]:
            self.rect.x += int(pygame.display.get_window_size()[0] / 100)
        if key[pygame.K_a]:
            self.rect.x -= int(pygame.display.get_window_size()[0] / 100)
        if key[pygame.K_s]:
            self.rect.y += int(pygame.display.get_window_size()[1] / 100)
        if key[pygame.K_w]:
            self.rect.y -= int(pygame.display.get_window_size()[1] / 100)
        if key[pygame.K_l]:
            self.cheat("l")
        super().update(key, fires_group, bullet, cheat)


class Fire(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], image: str, speed: float):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image),
            (screen.get_width() // 40, screen.get_height() // 28),
        )
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = int(speed * pygame.display.get_window_size()[1] / 500)

    def update(self, *args: type, **kwargs: type):
        super().update(*args, **kwargs)
        self.rect.y += self.speed
        if self.rect.top < 0 or self.rect.bottom > screen.get_height():
            self.kill()


class PFire(Fire):
    def __init__(
        self,
        position: tuple[int, int],
        image: str = f"pic{SEP}fire.png",
        speed: int = int(pygame.display.get_window_size()[1] / 80 * -1),
    ):
        super().__init__(position, image, speed)
        self.rect.center = (position[0], position[1] - 5)
        self.one_shot = True

    def update(self, *args: type, **kwargs: type):
        super().update(*args, **kwargs)
        if self.one_shot and Sound.sound_on:
            self.one_shot = False
            Sound.pf.play()


class EnemyFire(Fire):
    def __init__(
        self,
        position: tuple[int, int],
        image: str = f"pic{SEP}enfire.png",
        speed: int = int(pygame.display.get_window_size()[1] / 140),
    ):
        super().__init__(position, image, speed)
        self.one_shot = True

    def update(self):
        super().update()
        if self.one_shot and Sound.sound_on:
            Sound.ef.play()
            self.one_shot = False


class Enemy_Base(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, life: int, image: str):
        super().__init__()
        self.image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(image),
            (screen.get_width() // 6, screen.get_height() // 12),
        )
        self.images: list[pygame.Surface] = []
        self.images_non_sizeble = [
            pygame.image.load(image),
            pygame.image.load(f"pic{SEP}enemy2.png"),
            pygame.image.load(f"pic{SEP}enemy3.png"),
        ]
        self.image_shot = pygame.transform.scale(
            pygame.image.load(f"pic{SEP}enemyshot.png"),
            (screen.get_width() // 6, screen.get_height() // 12),
        )
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.got_pos = False
        self.pos_shot = y
        self.life = life
        self.move_x = int(
            random.randint(1, 2) / 4 * pygame.display.get_window_size()[0] / 100
        )
        self.move_y = 0
        self.killed = False
        self.reload_duration = random.randint(50, 200)
        self.reload = random.randint(0, 1)
        self.firing = False if not self.reload else True
        self.call = random.randint(0, 40)
        self.pos1 = 0

    def update(self, bullets: type, bullet: pygame.sprite.Sprite):
        super().update()
        self.call = self.call + 1 if self.call < 20 else 0
        if self.call == 19:
            self.pos1 = (self.pos1 + 1) % 3
            self.image = self.images[self.pos1]
        if not self.killed:
            self.reload = self.reload + 1 if self.firing else self.reload
            if self.reload == self.reload_duration:
                self.reload = 0
                self.firing = False

        if not self.got_pos:
            if self.rect.bottom <= self.y:
                self.rect.bottom += 5
            else:
                if self.rect.x >= self.x:
                    self.rect.x -= 8
                elif self.rect.x <= self.x:
                    self.rect.x += 8
        else:
            if self.rect.right > screen.get_width():
                self.rect.right = screen.get_width() - 1
                self.move_x *= -1
            elif self.rect.left < 0:
                self.rect.left = 1
                self.move_x *= -1
            self.rect.y += self.move_y
            self.rect.x += self.move_x
            if self.rect.bottom > screen.get_height():
                self.kill()
        if (
            self.rect.left <= self.x <= self.rect.right
            and self.rect.top <= self.y <= self.rect.bottom
        ):
            self.got_pos = True

    def died(self):
        return self.life < 0, (self.x, self.y)

    def kill(self) -> None:
        self.image = self.image_shot
        self.life -= 1
        if not self.life:
            self.killed = True
            self.move_y = int(pygame.display.get_window_size()[1] / 200)
        if self.rect.bottom > screen.get_height() or self.life < 0:
            self.died()
            super().kill()


class Enemy(Enemy_Base):
    def __init__(
        self, x: int, y: int, life: int = 5, image: str = f"pic{SEP}enemy.png"
    ):
        super().__init__(x, y, life, image)
        for img in self.images_non_sizeble:
            self.images.append(
                pygame.transform.scale(
                    img, (screen.get_width() // 6, screen.get_height() // 12)
                )
            )

        self.rect.center = (random.randint(1, screen.get_width() - 1), 0)
        self.shot = False

    def update(self, bullets: type, bullet: pygame.sprite.Sprite):
        super().update(bullets, bullet)
        if not self.killed:
            if not self.reload and not self.firing:
                bullets.add(bullet(self.rect.center))
                self.firing = True
        if self.shot == True:
            self.rect.y -= 5
            if (self.pos_shot - self.rect.y) < 5:
                self.rect.y += 5
            self.shot = False

    def kill(self) -> None:
        if not self.shot:
            self.shot = True
        super().kill()


class BossEnemy(Enemy_Base):
    def __init__(self, x: int, y: int, life: int, image: str = f"pic{SEP}enemy.png"):
        super().__init__(x, y, life, image)
        self.image = pygame.transform.scale(
            pygame.image.load(image),
            (screen.get_width() // 2, screen.get_height() // 4),
        )
        for img in self.images_non_sizeble:
            self.images.append(
                pygame.transform.scale(
                    img, (screen.get_width() // 2, screen.get_height() // 4)
                )
            )
        self.image_shot = pygame.transform.scale(
            pygame.image.load(f"pic{SEP}enemyshot.png"),
            (screen.get_width() // 2, screen.get_height() // 4),
        )
        self.rect.center = (screen.get_width() // 2, 0)
        self.rect = self.image.get_rect()
        self.reload_duration = 30

    def update(self, bullets: type, bullet: pygame.sprite.Sprite):
        super().update(bullets, bullet)
        if not self.killed:
            if not self.reload and not self.firing:
                bullets.add(
                    bullet(
                        (
                            random.randint(self.rect.left, self.rect.right),
                            self.rect.centery,
                        )
                    )
                )
                self.firing = True


if __name__ == "__main__":
    open_screen()
