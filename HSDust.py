from random import *

classic = [94,81,37,33] #sum = 245

def main():
	numsims = 1000
	dustresultaccu = 0
	for i in range(numsims):
		# print(i)
		dustctr = 0
		cardlist = []
		for j in range(len(classic)):
			cardlist.append([])
			for k in range(0, classic[j]):
				cardlist[j].append(0)
		for j in range(5*50):
			rarity, num = get_card_rarity()
			if(cardlist[rarity][num] >= 2):
				if(rarity is 3):
					dustctr = dustctr + 400
				elif(rarity is 2):
					dustctr = dustctr + 100
				elif(rarity is 1):
					dustctr = dustctr + 20
				else:
					dustctr = dustctr + 5
			else:
				cardlist[rarity][num] = cardlist[rarity][num] + 1
				if(rarity is 3):
					dustctr = dustctr + 1600
				elif(rarity is 2):
					dustctr = dustctr + 400
				elif(rarity is 1):
					dustctr = dustctr + 100
				else:
					dustctr = dustctr + 40
		dustresultaccu = dustresultaccu + float(dustctr)/numsims
	print("Waiting for wotog: " + str(int(dustresultaccu)) + " dust")
	for collectionperc in range(0,10):
		dustresultaccu = 0
		for i in range(numsims):
			nerfdustctr = 0
			cardlist = []
			# print(range(100))
			for j in range(len(classic)):
				cardlist.append([])
				for k in range(0, classic[j]):
					cardlist[j].append(0)
			completion = 0
			while(completion < int(.1 * collectionperc * 2 * 245)):
				rarity, num = get_card_rarity()
				if(cardlist[rarity][num] < 2):
					cardlist[rarity][num] = cardlist[rarity][num] + 1
					completion = completion + 1
			for j in range(5*50):
				rarity, num = get_card_rarity()
				if(cardlist[rarity][num] >= 2 and randint(0,100)>8):
					if(rarity is 3):
						nerfdustctr = nerfdustctr + 400
					elif(rarity is 2):
						nerfdustctr = nerfdustctr + 100
					elif(rarity is 1):
						nerfdustctr = nerfdustctr + 20
					else:
						nerfdustctr = nerfdustctr + 5
				else:
					cardlist[rarity][num] = cardlist[rarity][num] + 1
					if(rarity is 3):
						nerfdustctr = nerfdustctr + 1600
					elif(rarity is 2):
						nerfdustctr = nerfdustctr + 400
					elif(rarity is 1):
						nerfdustctr = nerfdustctr + 100
					else:
						nerfdustctr = nerfdustctr + 40
			dustresultaccu = dustresultaccu + float(nerfdustctr)/numsims
		print(str(collectionperc*10) + "% classic cards collected: " + str(int(dustresultaccu)) + " dust")


def get_card_rarity():
	ranum = randint(0,10000)
	if ranum > (10000 - 110):
		return 3, randint(0,classic[3]-1)
	elif ranum > (10000 - 110 - 442):
		return 2, randint(0,classic[2]-1)
	elif ranum > (10000 - 110 - 442 - 2284):
		return 1, randint(0,classic[1]-1)
	else:
		return 0, randint(0,classic[0]-1)

if __name__ == "__main__":
    main()