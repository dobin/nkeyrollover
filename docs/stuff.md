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
        - start timer
        - set state to State.gameover

CharacterAnimationProcessor:
    Handle: EntityDying
        - change texture of player renderable to dying

<advance>

SceneProcessor:
    # move from gameover screen to start of map
    # use state.start to let renderableprocessor do
    # what it should do, then start
    Handle: PlayerKeyPress
        if timer.timeisup:
        - state = state.start
        - emit ClearRenderables

RenderableProcessor:
    Handle: ClearRenderables
        - removeall renderables (including player, enemies)

<advance>

SceneProcessor:
    if state is state.start:
        - state = state.brawl
        - sceneManager.restartScene()
            - reset viewport
            - load map
            - spawnPlayer()
            - spawn enemies
            - ...
```