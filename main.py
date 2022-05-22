# MAIN FILE, RUN THIS FILE TO START THE GAME
import pygame as pg
import pygame.event


# initialise pygame functionality
pg.init()
pg.font.init()
pg.mixer.init()


# game-program runs
def main():

    print("GAME INITIALIZING ...")

    # import custom libraries and assets
    from level_manager import LEVEL_MANAGER
    from player_lib import space_ship
    from game_lib import GROUP_ENEMY, GROUP_PLAYER, GROUP_ITEM, GROUP_GAME_SPRITES, \
        SCREEN, CLOCK, FPS, end_game, reset_game
    import item_lib
    from gui_lib import GUI, MENU, DEATH_SCREEN, WIN_SCREEN

    # -------- DEVELOPMENT --------------------------
    # from dev import DeveloperManager
    # global fps_list
    # global time_list
    # dev_manager = DeveloperManager()
    # -------- DEVELOPMENT --------------------------

    # different modes program switch between
    MODE_MENU = True
    MODE_GAME = False
    MODE_DEATH = False
    MODE_WIN = False

    GAME_SETUP = True

    # managers control what's show on screen & functionality
    MANAGER_MENU = MENU()
    MANAGER_DEATH_SCREEN = DEATH_SCREEN()
    MANAGER_WIN_SCREEN = WIN_SCREEN()

    MANAGER_GUI = GUI()

    # GAME-PROGRAM LOOP
    while True:

        # CONTROL FPS
        CLOCK.tick(FPS)

        # CHECK FOR CLOSING WINDOW
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                end_game()

        # GAME SCREEN
        if MODE_GAME:
            
            # setup game, restart from beginning
            if GAME_SETUP:
                # clear all sprites / remove from groups
                reset_game()
                # spawn player
                player = space_ship()
                # initialise level_manager, controls levels, waves, environment and progression
                MANAGER_LEVEL = LEVEL_MANAGER()
                # setup done
                GAME_SETUP = False
            
            # update level mechanics, if all levels complete end game
            if MANAGER_LEVEL.update():
                MODE_GAME = False
                MODE_WIN = True

            # collisions: enemies & player + player attacks
            collisions = pg.sprite.groupcollide(GROUP_ENEMY, GROUP_PLAYER, dokilla=False, dokillb=False)
            if collisions:  # go through all collisions 'on screen'
                for enemy in collisions:  # every enemy affected
                    for target in collisions[enemy]:  # all attacks on enemy
                        if pg.sprite.collide_mask(enemy, target):  # actually collides with sprite mask, deal damages
                            enemy.health -= target.attack   # damage enemy sprite

                            if target.__class__ == space_ship:
                                if target.shield != True:   # only damage player if shield isn't activated
                                    target.health -= enemy.attack
                            else:
                                target.health -= enemy.attack   # damage everything else

            # collisions: items & player
            collisions = pg.sprite.spritecollide(player, GROUP_ITEM, dokill=False)
            if collisions:  # go through all collisions 'on screen'
                for item in collisions:  # every item affected
                    if pg.sprite.collide_mask(item, player):  # actually collides with sprite mask, apply effect
                        item.health -= player.attack    # damage / remove item

                        # apply effect to player
                        if item.__class__ == item_lib.coin:
                            player.score += 1
                        elif item.__class__ == item_lib.medkit:
                            player.health += 400
                        elif item.__class__ == item_lib.shield:
                            player.activate_shield(time=10)

            # update all sprites
            GROUP_GAME_SPRITES.update()

            # draw all sprites
            GROUP_GAME_SPRITES.draw(SCREEN)

            # update & pass GUI manager current variables
            MANAGER_GUI.update(score=player.score, health=player.health, health_max=player.health_max,
                               warp_max=player.warp_max, warp_avl=player.warp_avl,
                               current_warp_intervall_fps=player.current_warp_intervall_fps,
                               warp_intervall_fps=player.warp_intervall_fps,
                               shield_time=player.shield_time, shield_time_current=player.shield_time_current,
                               level_time=MANAGER_LEVEL.level.level_time,
                               current_level_time=MANAGER_LEVEL.level.time_passed,
                               level_stop_time=MANAGER_LEVEL.level.level_stop)

            # switch to death screen upon player death
            if player.health <= 0:
                MODE_GAME = False
                MODE_DEATH = True

        # MENU SCREEN
        elif MODE_MENU:

            # receives positiv signal, switch mode to game, while updating
            if MANAGER_MENU.update():
                MODE_MENU = False
                MODE_GAME = True
                GAME_SETUP = True

        # PLAYER WIN SCREEN
        elif MODE_WIN:

            # receives positiv signal, switch mode to menu, while updating
            if MANAGER_WIN_SCREEN.update():
                MODE_WIN = False
                MODE_DEATH = False
                MODE_MENU = True

        # PLAYER DEATH SCREEN
        elif MODE_DEATH:

            # receives positiv signal, switch mode to menu, while updating
            if MANAGER_DEATH_SCREEN.update():
                MODE_DEATH = False
                MODE_MENU = True

        # -------- DEVELOPMENT --------------------------
        # dev_manager.update(FPS=CLOCK.get_fps())
        # -------- DEVELOPMENT --------------------------

        # UPDATE SCREEN
        pg.display.update()


# run main function upon script run
if __name__ == "__main__":
    main()
