# NKeyRollover Design

## Main Loop

Note that drawing the map is not being done with a system (for performance reasons).

* Draw1 (draw map)
* Advance (let all systems/processors run)
* Draw2 (draw some overlays)

## Z Order 

In advance():
* all RenderableMinimal
* all Renderable
    * y-value is basically Z order
    * plus optional Z in renderable
* particles

## ECS

State in components, code in systems. Systems which need state have singletons. 

Components:
* Renderable (position, texture)
* GroupId (a unique id for an entity)
* Player (some player related data)
* Enemy (enemy specific cooldowns)
* Ai (behaviour of enemies)
* Attackable (health)
* OffensiveAttack (can select and use attacks)
* OffensiveSkill (can use skills)

Entities: 
* Player
* Enemy
* GFX
    * based on RenderableMinimal:
        * TextureMinimal (with 1 char big texture)
        * Effect
    * based on Renderable:
        * SpeechBubble
        * ActionAttack

Other GFX:
* Particle (managed via ParticleProcessor)
* Map (managed via MapProcessor)

Textures:
* Action: Used for attacks (e.g. swords attacks)
* Character: player, enemy models
* Phenomena: Static things (e.g. trees, roflcopter)
* Speech: Speech bubble


## Attacks vs. Skills

Similar to Leage of Legends. Attacks are space (or autoattacks in LoL, left mouse 
button), selected by key 1-4. Skills are keys QWER.

* Attacks: Use ActionTexture
* Skills: Use Particles


## File System

* data/
  * enemies/: Enemy Definition (cooldowns, health, texture type)
  * map/: Map in XP format
  * textures/: Stored ASCII textures (loaded via FileTextureLoader)
    * Action/: for attacks
    * Character/: Character animations (stickfigure, cow, dragon)
    * Phenomena/: Static stuff (logo, roflcopter, trees)
  * weapons/: Information about Attacks
    * .ascii: Hit detection texture (for enemies, AI)
    * .yaml: Some information (damage, Texture)


## Pipeline

The current pipeline, as of writing this document, looks like the following. It 
is a list of systems, executed every game loop, from top to bottom.

Note that all messages get removed at the end of the pipeline (after DamageProcessor).
Messages can therefor only flow "down", as indicated by the order of the processors
in the source code. 

If it is necessary to make a message survive a loop, use DirectMessage (uses a GroupId
to identify a component. Message can be read exactly once). 

* p: Player
* e: Enemy
* x: Both, other

```python
        self.world.add_processor(gametimeProcessor)

        # KeyboardInput:getInput()
        # p generate: Message            PlayerKeypress

        # p handle:   Message            PlayerKeyPress (movement)
        # p generate: DirectMessage      movePlayer
        self.world.add_processor(inputProcessor)

        # p handle:   DirectMessage      movePlayer
        # e handle:   DirectMessage      moveEnemy
        # p generate: Message            PlayerLocation
        # x generate: Message            EntityMoved
        self.world.add_processor(movementProcessor)

        # p handle:   Message            PlayerLocation
        # e generate: Message            EnemyAttack
        # e generate: DirectMessage      moveEnemy
        # x generate: Message            EmitTextureMinimal
        self.world.add_processor(aiProcessor)

        # e handle:   DirectMessage      moveEnemy
        # p handle:   Message            PlayerKeyPress (space/attack, weaponselect)
        # p generate: Message            PlayerAttack (via OffensiveAttack)
        self.world.add_processor(offensiveAttackProcessor)

        # p handle:   Message            PlayerKeyPress (skill activate)
        # x generate: Message            EmitParticleEffect (skill)
        # x generate: DirectMessage      activateSpeechBubble
        self.world.add_processor(offensiveSkillProcessor)

        # x handle:   DirectMessage      receiveDamage
        # x generate: Message            EntityStun
        # x generate: Message            EntityDying
        # x generate: Message            EmitTexture
        self.world.add_processor(attackableProcessor)

        # p handle:   Message            PlayerLocation
        # x handle:   Message            EntityDying
        # p handle:   Message            PlayerKeypress
        # e generate: Message            SpawnEnemy
        # p generate: Message            SpawnPlayer
        # x generate: DirectMessage      activateSpeechBubble
        self.world.add_processor(sceneProcessor)

        # x generate: Message            EntityDead
        # e handle:   Message            SpawnEnemy
        self.world.add_processor(enemyProcessor)

        # p handle.   Message            SpawnPlayer
        self.world.add_processor(playerProcessor)

        # x handle:   Message            EmitTextureMinimal
        # x handle:   Message            EmitTexture
        # x generate: Message            AttackAt (via TextureEmiter, ActionTexture)
        self.world.add_processor(renderableMinimalProcessor)

        # e handle:   Message            EntityDying
        # p handle:   Message            PlayerAttack (change animation)
        # x handle:   Message            AttackWindup
        # x handle:   Message            EntityAttack
        # x handle:   Message            EntityMoved
        # x handle:   Message            EntityStun
        self.world.add_processor(characterAnimationProcessor)

        # x handle:   DirectMessage      activateSpeechBubble (emit)
        # p handle:   Message            PlayerAttack (CD, convert to damage)
        # e handle:   Message            EnemyAttack
        # x generate: Message            AttackAt
        # x generate: DirectMessage      activateSpeechBubble (because of damage)
        self.world.add_processor(renderableProcessor)

        # x handle:   Message            EmitParticleEffect
        # x generate: Message            AttackAt
        self.world.add_processor(particleProcessor)

        # x handle:   Message            AttackAt
        # x generate: DirectMessage      receiveDamage
        self.world.add_processor(damageProcessor)
```
