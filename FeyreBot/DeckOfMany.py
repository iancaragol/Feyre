import random
import os

class DeckOfMany:
    def __init__(self):
        self.default_deck = {
            "balance" : "Your mind suffers a wrenching alteration, causing your Alignment to change. Lawful becomes chaotic, good becomes evil, and vice versa. If you are true neutral or unaligned, this card has no effect on you.",
            "comet" : "If you single-handedly defeat the next Hostile monster or group of Monsters you encounter, you gain Experience Points enough to gain one level. Otherwise, this card has no effect.",
            "donjon" : "You disappear and become entombed in a state of suspended animation in an extradimensional Sphere. Everything you were wearing and carrying stays behind in the space you occupied when you disappeared. You remain imprisoned until you are found and removed from the Sphere. You can't be located by any Divination magic, but a wish spell can reveal the location of your prison. You draw no more cards.",
            "euryale" : "The card's medusa-like visage curses you. You take a -2 penalty on Saving Throws while Cursed in this way. Only a god or the magic of The Fates card can end this curse.",
            "fates" : "Reality's fabric unravels and spins anew, allowing you to avoid or erase one event as if it never happened. You can use the card's magic as soon as you draw the card or at any other time before you die.",
            "flames" : "A powerful devil becomes your enemy. The devil seeks your ruin and plagues your life, savoring your suffering before attempting to slay you. This enmity lasts until either you or the devil dies.",
            "fool" : "You lose 10,000 XP, discard this card, and draw from the deck again, counting both draws as one of your declared draws. If losing that much XP would cause you to lose a level, you instead lose an amount that leaves you with just enough XP to keep your level.",
            "gem" : "Twenty-five pieces of jewelry worth 2,000 gp each or fifty gems worth 1,000 gp each appear at your feet.",
            "idiot" : "Permanently reduce your Intelligence by 1d4 + 1 (to a minimum score of 1). You can draw one additional card beyond your declared draws.",
            "jester" : "You gain 10,000 XP, or you can draw two additional cards beyond your declared draws.",
            "key" : "A rare or rarer Magic Weapon with which you are proficient appears in your hands. The DM chooses the weapon.",
            "knight" : "You gain the service of a 4th-level Fighter who appears in a space you choose within 30 feet of you. The Fighter is of the same race as you and serves you loyally until death, believing the fates have drawn him or her to you. You control this character.",
            "moon" : "You are granted the ability to cast the wish spell 1d3 times.",
            "rogue" : "A nonplayer character of the DM's choice becomes Hostile toward you. The identity of your new enemy isn't known until the NPC or someone else reveals it. Nothing less than a wish spell or Divine Intervention can end the NPC's hostility toward you.",
            "ruin" : " All forms of Wealth that you carry or own, other than Magic Items, are lost to you. Portable property vanishes. Businesses, buildings, and land you own are lost in a way that alters reality the least. Any documentation that proves you should own something lost to this card also disappears.",
            "skull" : "You summon an avatar of death-a ghostly Humanoid Skeleton clad in a tattered black robe and carrying a spectral scythe. It appears in a space of the DM's choice within 10 feet of you and attacks you, warning all others that you must win the battle alone. The avatar fights until you die or it drops to 0 Hit Points, whereupon it disappears. If anyone tries to help you, the helper summons its own Avatar of Death. A creature slain by an Avatar of Death can't be restored to life.",
            "star" : "Increase one of your Ability Scores by 2. The score can exceed 20 but can't exceed 24.",
            "sun" : "You gain 50,000 XP, and a wondrous item (which the DM determines randomly) appears in your hands.",
            "talons" : "Every magic item you wear or carry disintegrates. Artifacts in your possession aren't destroyed but do Vanish.",
            "throne" : "You gain proficiency in the Persuasion skill, and you double your Proficiency Bonus on checks made with that skill. In addition, you gain rightful ownership of a small keep somewhere in the world. However, the keep is currently in the hands of Monsters, which you must clear out before you can claim the keep as. yours.",
            "vizier" : "At any time you choose within one year of drawing this card, you can ask a question in meditation and mentally receive a truthful answer to that question. Besides information, the answer helps you solve a puzzling problem or other dilemma. In other words, the knowledge comes with Wisdom on how to apply it.",
            "void" : "This black card Spells Disaster. Your soul is drawn from your body and contained in an object in a place of the DM's choice. One or more powerful beings guard the place. While your soul is trapped in this way, your body is Incapacitated. A wish spell can't restore your soul, but the spell reveals the location of the object that holds it. You draw no more cards."
        }

        self.default_deck_images = {
            "balance" : "https://i.imgur.com/dlHlMSJ.png",
            "comet" : "https://i.imgur.com/tLWgYA5.png",
            "donjon" : "https://i.imgur.com/Y7zITG4.png",
            "euryale" : "https://i.imgur.com/DxgQ9o1.png",
            "fates" : "https://i.imgur.com/L4ag0fK.png",
            "flames" : "https://i.imgur.com/j7kEK96.png",
            "fool" : "https://i.imgur.com/m7ych8E.png",
            "gem" : "https://i.imgur.com/8TBp17r.png",
            "idiot" : "https://i.imgur.com/4NtUg2g.png",
            "jester" : "https://i.imgur.com/9h9mMaR.png",
            "key" : "https://i.imgur.com/bAfjOyA.png",
            "knight" : "https://i.imgur.com/ZALdmca.png",
            "moon" : "https://i.imgur.com/Bcti8iW.png",
            "rogue" : "https://i.imgur.com/voPBc64.png",
            "ruin" : "https://i.imgur.com/pvMSQTZ.png",
            "skull" : "https://i.imgur.com/bIJZZAR.png",
            "star" : "https://i.imgur.com/zgGikPc.png",
            "sun" : "https://i.imgur.com/zYyIMoe.png",
            "talons" : "https://i.imgur.com/gGStBpn.png",
            "throne" : "https://i.imgur.com/ihUkfzo.png",
            "vizier" : "https://i.imgur.com/8CB1NbW.png",
            "void" : "https://i.imgur.com/45aIClQ.png"
    }

    async def draw(self, deck):
        card, effect = random.choice(list(deck.items()))
        return card, effect

    async def card_to_string(self, card, effect):
        s = f"""```diff
-{card.capitalize()}-
        
{effect}```"""

        return s

    async def get_image(self, card):
        return self.default_deck_images[card]
