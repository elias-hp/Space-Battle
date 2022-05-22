# ASSET FILE, ALL PRELOADED ASSETS HERE

import pygame as pg
from game_lib import Asset, AnimatedAsset, Background

# ITEMS
asset_coin = AnimatedAsset(img_fold=r'./assets/ani_coin', size_factor=1.75)
asset_medkit = Asset(img_dir=r'./assets/item_heart.png', size_factor=3)
asset_shield = Asset(img_dir=r'./assets/item_shield.png', size_factor=5)

sound_coin = pg.mixer.Sound(rf'./assets/sound/coin.wav')
sound_medkit = pg.mixer.Sound(rf'./assets/sound/medkit.wav')
sound_shield = pg.mixer.Sound(rf'./assets/sound/shield.wav')

# PLAYER
asset_space_ship = Asset(img_dir=r'assets/player_SpaceShip.png', size_factor=1.25)
asset_laser_bullet = Asset(img_dir=r'assets/player_LaserBullet.png', size_factor=0.035)

sound_warp = pg.mixer.Sound(rf'./assets/sound/warp.wav')
sound_warp.set_volume(0.75)

sound_laser_shot = pg.mixer.Sound(rf'./assets/sound/laser_shot.wav')
sound_laser_shot.set_volume(0.5)

# GUI
sound_click = pg.mixer.Sound(r'./assets/sound/click.wav')
sound_menu = pg.mixer.Sound(r'./assets/sound/menu.mp3')
sound_menu.set_volume(0.5)

background_menu = Background(image_dir=r'assets/back_BeautifulCosmosDawn_bottom.png')

# ENEMIES
asset_astroid = Asset(img_dir=r'./assets/asteroid.png', size_factor=0.50)
asset_astroid.add_alter(size_factor=1, nmb=1)
asset_astroid.add_alter(size_factor=1.75, nmb=2)
asset_astroid.add_alter(size_factor=4, nmb=3)

asset_explosion = AnimatedAsset(img_fold=r'./assets/ast_explosion', size_factor=4)
asset_explosion.add_alter(size_factor=8, nmb=1)
asset_explosion.add_alter(size_factor=10, nmb=2)
asset_explosion.add_alter(size_factor=20, nmb=3)

# GENERAL
sound_explosion = pg.mixer.Sound(rf'./assets/sound/mixkit-arcade-game-explosion-2759.wav')

# DEATH SCREEN
sound_death_screen = pg.mixer.Sound('./assets/sound/dark-souls-_you-died_-sound-effect-from-youtube.mp3')
sound_death_screen.set_volume(2.0)

# WIN SCREEN
sound_win_screen = pg.mixer.Sound('./assets/sound/win+misson_passed.wav')
sound_win_screen.set_volume(2.0)

# LEVELS
sound_level_up = pg.mixer.Sound(rf'./assets/sound/level_cleared.wav')
sound_level_up.set_volume(0.70)

level_1_background = Background(image_dir=r'./assets/back_NebulaBirth.png')
level_1_music = pg.mixer.Sound('./assets/sound/soundtrack_level01.wav')
level_1_music.set_volume(1)

level_2_background = Background(image_dir=r'assets/back_UnviersalDeath_dust.png')
level_2_music = pg.mixer.Sound('./assets/sound/soundtrack_level02.wav')
level_2_music.set_volume(0.5)

level_3_background = Background(image_dir=r'assets/back_NewPlanetaryAge.png')
level_3_music = pg.mixer.Sound('./assets/sound/soundtrack_level03.wav')
level_3_music.set_volume(0.75)
