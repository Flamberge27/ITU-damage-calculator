from itu_classes import *
import sys

sys.stdout.reconfigure(encoding='utf-8')

dice_pool_dict = {}

testDicePool = DiePool((1,3,1), dice_pool_dict, ignore_dots=False)

#print(testDicePool.SymbolMultiplicityText())

testKratosPool = KratosPool(brk = 3, fir= 4, hop = 1)

print(testDicePool.SimpleDamageText(testKratosPool))



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