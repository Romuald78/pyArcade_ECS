from ecs.core.components.gfx import GfxAnimatedSprite, GfxAnimSpriteList, GfxMultiSprite
from ecs.core.main.entity import Entity
from shmup.common.constants import SCREEN_HEIGHT, ZIDX_HUD, SCREEN_WIDTH, MAX_PLAYERS
from shmup.scripts.hudLife import HudLife
from shmup.scripts.updatescores import UpdateScores


class HudFactory():


    def __init__(self):
        pass


    def create(self, playerNum, playerColor, lifeComp, scoreComp):
        # Create HUD Entity
        hudEntity = Entity()

        # Create borders
        w = 672
        wbar = w
        h = 64
        hbar = h
        d = 20
        ratio = ((SCREEN_WIDTH-((MAX_PLAYERS+1)*d))/MAX_PLAYERS)/w
        refX = (w*ratio//2) + d + (playerNum-1)*((w*ratio)+d)
        refY = (h*ratio//2) + d
        params = {
            "filePath": "resources/images/hud/bar.png",
            "textureName": f"hudBar{playerNum}",
            "spriteBox": (1, 1, w, h),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 10,
            "size": (int(w*ratio),int(h*ratio)),
            "position": (refX,refY),
            "filterColor": playerColor
        }
        barGfx = GfxAnimatedSprite(params, ZIDX_HUD, "barGfx")
        hudEntity.addComponent(barGfx)

        # Add bar element sprites
        w = 30
        h = 40
        d = 1
        gfxList = []
        for i in range(-10,11):
            red   = 255
            green = 255
            alpha = 160
            if i>=0:
                red = int(255*(10-i)/10)
            if i<=0:
                green = int(255*(10+i)/10)
            params = {
                "filePath": "resources/images/hud/barElt.png",
                "textureName": f"hudElt{playerNum}{i+10}",
                "spriteBox": (1, 1, w, h),
                "startIndex": 0,
                "endIndex": 0,
                "frameDuration": 1 / 10,
                "size": (int(w * ratio), int(h * ratio)),
                "position": (refX+i*(w+d)*ratio, refY),
                "filterColor": (red, green, 0, 160)
            }
            eltGfx = GfxAnimatedSprite(params, ZIDX_HUD, "eltGfx")
            hudEntity.addComponent(eltGfx)
            gfxList.append(eltGfx)


        d = 20
        refX += (-wbar/2+d)*ratio
        refY += hbar*ratio/2
        w = 80
        h = 128
        ratio *= 0.5
        params = {
            "filePath": "resources/images/hud/numbers.png",
            "textureName": f"hudNum{playerNum}hundred",
            "spriteBox": (10, 1, w, h),
            "startIndex": 0,
            "endIndex": 9,
            "frameDuration": 1 / 10,
            "size": (int(w*ratio),int(h*ratio)),
            "position": (refX,refY)
        }
        hundredGfx = GfxMultiSprite(params, ZIDX_HUD-1, "hundredGfx")
        refX += (w)*ratio
        refY += 0
        params = {
            "filePath": "resources/images/hud/numbers.png",
            "textureName": f"hudNum{playerNum}decade",
            "spriteBox": (10, 1, w, h),
            "startIndex": 0,
            "endIndex": 9,
            "frameDuration": 1 / 10,
            "size": (int(w*ratio),int(h*ratio)),
            "position": (refX,refY)
        }
        decadeGfx = GfxMultiSprite(params, ZIDX_HUD-1, "decadeGfx")
        refX += (w)*ratio
        refY += 0
        params = {
            "filePath": "resources/images/hud/numbers.png",
            "textureName": f"hudNum{playerNum}unit",
            "spriteBox": (10, 1, w, h),
            "startIndex": 0,
            "endIndex": 9,
            "frameDuration": 1 / 10,
            "size": (int(w*ratio),int(h*ratio)),
            "position": (refX,refY)
        }
        unitGfx = GfxMultiSprite(params, ZIDX_HUD-1, "unitGfx")


        # Add numbers
        hudEntity.addComponent(unitGfx)
        hudEntity.addComponent(decadeGfx)
        hudEntity.addComponent(hundredGfx)

        unitGfx.setTexture(1)
        decadeGfx.setTexture(4)
        hundredGfx.setTexture(8)

        # Create score update script
        scrUpdate = UpdateScores(scoreComp,unitGfx, decadeGfx, hundredGfx)
        hudEntity.addComponent(scrUpdate)

        # Create hudlife script
        life = HudLife(lifeComp, gfxList)
        hudEntity.addComponent(life)

        # Return entity
        return hudEntity


