from itu_classes import *
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Simple damage
# - No rerolls
# - Maximize damage (do not use hopes to protect Fire pool)
def getSimpleDamage(dice_pool_dict, dice_combination, kratos_pool):
	damage_dict = {}
	dicePool = dice_pool_dict[dice_combination]

	for symbol_pool, mult in dicePool.combo_mults.items():
		damage_total = symbol_pool[0]
		breaks = kratos_pool.breaks
		fires = kratos_pool.fires
		hopes = kratos_pool.hopes
		potential = symbol_pool[1]
		dots = symbol_pool[2]
		# use breaks first
		converted = min(breaks, potential)
		damage_total += converted
		breaks -= converted
		potential -= converted
		# use hopes on dots
		converted = min(hopes, dots)
		damage_total += converted
		hopes -= converted
		dots -= converted #technically no longer necessary to keep track of this
		# use remaining hopes and fires
		converted = min(hopes, potential)
		damage_total += converted
		hopes -= converted
		potential -= converted
		converted = min(fires, potential)
		damage_total += converted
		fires -= converted
		potential -= converted
		if damage_total not in damage_dict:
			damage_dict[damage_total] = 0
		damage_dict[damage_total] += mult
	return damage_dict

def SimpleDamageText(dice_pool_dict, dice_combination, kratos_pool):
	dicePool = dice_pool_dict[dice_combination]
	damage_dict = getSimpleDamage(dice_pool_dict, dice_combination, kratos_pool)
	final = "If you roll " + dicePool.DiceText() + ", and your Kratos table is"

	# conditional leading newline. "your Kratos table is empty" does not need a newline
	if not kratos_pool.isEmpty():
		final += "\n  "
	final += kratos_pool.PoolText() + "\nThen you have:\n"
	for damage, mult in sorted(damage_dict.items()):
		perc_str = str(round(mult * 100 / dicePool.total_mult, 1)) + "%"
		# left-pad single-digit percents
		if mult / dicePool.total_mult < 0.1:
			perc_str = " " + perc_str
		dmg_str = str(damage) + chr(int('3031', 16)) + " total"
		if damage < 10:
			dmg_str = " " + dmg_str
		final += " > " + perc_str + " of\t" + dmg_str + "\n"
	return final

dice_pool_dict = {}

testDicePool = DiePool((1,3,1), dice_pool_dict, ignore_dots=False)

#print(testDicePool.SymbolMultiplicityText())

testKratosPool = KratosPool(brk = 3, fir= 4, hop = 1)

print(SimpleDamageText(dice_pool_dict, (1,3,1), testKratosPool))


"""
Kratos Tokens:
	Breaks: Potential -> Power
	Fire: Potential -> Power, use last
	Hope: Dot / Potential > Power
	
	Black: Reroll, +1 Break on this die next roll
	Closing: 1 Precision, 1 reroll
	Openings: +1 Precision

	Diversion: Ignore Fail

	Rouse: +1 Rage

#"""

"""
Relevant keywords (always):
- Attack reroll
- Clutch
- Deadly
- Power Reroll
- Sacrifice
- Spiral
- Spotlight
- Startup
- Taint

Relevant keywords (eventual):
- Armor-Piercing
- Commit
- Heartseeker
- Harpooned
- Precise
#"""