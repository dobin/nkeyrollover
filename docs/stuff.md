# Keys

In-game: 

* F1: Show some stats
* F2: Show log
* p: Pause


# Playground

Empty map. 

* Key "k": Kill all enemies in current Akt
* Key "n": Go to next scene


# On Death

Order of actions when player health reaches below 0:

```
AttackableProcessor:
    if player.isAlive and playerAttackable.isActive and playerAttackable.health <= 0:
        - player.isAlive = False
        - playerAttackable.isActive = False
        - Emit: Gameover
        - Emit: EntityDying
        

SceneProcessor:
    Handle: Gameover
        - show gameover texture

CharacterAnimationProcessor:
    Handle: EntityDying
        - change texture of player renderable to dying

<advance>

InputProcessor:
    # continue when key is pressed on gameover screen / texture
    Handle: PlayerKeyPress
        if not player.isAlive:
            - Emit: GameRestart

RenderableProcessor:
    Handle: GameRestart
        - removeall renderables (including player, enemies)
    Emit: GameStart

<advance>

SceneProcessor:
    Handle: GameStart
        - sceneManager.restartScene()
            - reset viewport
            - load map
            - spawnPlayer()
            - spawn enemies
            - ...
```