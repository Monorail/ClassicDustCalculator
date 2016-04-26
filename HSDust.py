from random import *

#common, rare, epic, legendary
card_cap = [2,2,2,1]
classic = [94,81,37,33] #sum = 245
wotog = [50,36,27,21]   
reg_de_amt  =     [5  , 40 , 100 , 400 ]
reg_full_amt =    [40 , 100, 400 , 1600]
golden_de_amt =   [50 , 100, 400 , 1600]
golden_full_amt = [400, 800, 1600, 3200]
cards_nerfed = [2,5,4,0]

def main():
    num_sims = 1000
    dust_result_accu = 0
    for i in range(num_sims):
        dust_ctr = 0.0
        card_list = []
        for j in range(len(wotog)):
            card_list.append([])
            for k in range(0, wotog[j]):
                card_list[j].append([0,0])
        # simulate pack openings
        for j in range(5*50):
            golden, rarity, num = generate_wotog_card()
            card_list[rarity][num][golden]= card_list[rarity][num][golden]+1
        for rarity in range(0,4):
            for card_num in range(wotog[rarity]):
                while( card_list[rarity][card_num][0] + 
                       card_list[rarity][card_num][1] ) > card_cap[rarity]:
                        if card_list[rarity][card_num][1] > 0:
                            card_list[rarity][card_num][1] = card_list[rarity][card_num][1] - 1
                            dust_ctr = dust_ctr + golden_de_amt[rarity]
                        else:
                            card_list[rarity][card_num][0] = card_list[rarity][card_num][0] - 1
                            dust_ctr = dust_ctr + reg_de_amt[rarity]
                dust_ctr = dust_ctr + \
                           card_list[rarity][card_num][1] * golden_de_amt[rarity] + \
                           card_list[rarity][card_num][0] * reg_full_amt[rarity]
        dust_result_accu = dust_result_accu + float(dust_ctr)/num_sims
    print("Waiting for wotog: " + str(int(dust_result_accu)) + " dust")
    for collectionperc in range(0,20):
        dust_result_accu = 0.0
        for i in range(num_sims):
            nerfdust_ctr = 0.0
            card_list = []
            prior_card_list = []
            # generate empty collection buckets
            for j in range(len(classic)):
                prior_card_list.append([])
                card_list.append([])
                for k in range(0, classic[j]):
                    prior_card_list[j].append([0,0])
                    card_list[j].append([0,0])
            # generate a percentage of the user's classic collection
            # the beforehand collection (prior_card_list) must be kept separate from the 
            # "opened today" collection (card_list) because we cannot consider cards that were
            # opened prior to opening our 50 packs.
            completion = 0
            while_cond = int(.05 * collectionperc * 2 * 245)
            while(completion < while_cond):
                golden, rarity, num = generate_classic_card()
                if(prior_card_list[rarity][num][0] + prior_card_list[rarity][num][1]) < card_cap[rarity]:
                    prior_card_list[rarity][num][golden] = prior_card_list[rarity][num][golden]+1
                    completion = completion + 1
            #simulate the opening of 50 packs
            for j in range(5*50):
                golden, rarity, num = generate_classic_card()
                card_list[rarity][num][golden]= card_list[rarity][num][golden]+1
            # for cards of all rarity
            for rarity in range(0,4):
                # for each card in each rarity
                for card_num in range(classic[rarity]):
                    # if this card has been nerfed (first N cards in each rarity are nerfed)
                    if card_num <= (cards_nerfed[rarity]-1):
                        # add full dust value of all opened cards to dust counter
                        nerfdust_ctr =  nerfdust_ctr + \
                                   card_list[rarity][card_num][1] * golden_full_amt[rarity] + \
                                   card_list[rarity][card_num][0] * reg_full_amt[rarity]
                    # if this card was not nerfed
                    else:
                        # while we have more than enough of the current card
                        while(  card_list[rarity][card_num][0] + 
                                card_list[rarity][card_num][1] +
                                prior_card_list[rarity][card_num][0] + 
                                prior_card_list[rarity][card_num][1] ) > card_cap[rarity]:
                            # try to disenchant a golden copy of the card
                            if card_list[rarity][card_num][1] > 0:
                                card_list[rarity][card_num][1] = card_list[rarity][card_num][1] - 1
                                nerfdust_ctr = nerfdust_ctr + golden_de_amt[rarity]
                            # if there are no more golden copies, disenchant a regular one
                            else:
                                card_list[rarity][card_num][0] = card_list[rarity][card_num][0] - 1
                                nerfdust_ctr = nerfdust_ctr + reg_de_amt[rarity]
                        # add remaining cards opened in 50 packs
                        nerfdust_ctr = nerfdust_ctr + \
                                   card_list[rarity][card_num][1] * golden_de_amt[rarity] + \
                                   card_list[rarity][card_num][0] * reg_full_amt[rarity]
                        
            dust_result_accu = dust_result_accu + float(nerfdust_ctr)/num_sims
        print(str(collectionperc*5) + "% classic cards collected: " + str(int(dust_result_accu)) + " dust")


def generate_classic_card():
    ranum = randint(0,10000)
    # 7 GL
    if ranum > (10000 - 7):
        return 1, 3, randint(0,classic[3]-1)
    # 19 GE
    elif ranum > (10000 - 7 - 19):
        return 1, 2, randint(0,classic[2]-1)
    # 94 RL
    elif ranum > (10000 - 7 - 19 - 94):
        return 0, 3, randint(0,classic[3]-1)
    # 127 GR
    elif ranum > (10000 - 7 - 19 - 94 - 127):
        return 1, 1, randint(0,classic[1]-1)
    # 148 GC
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148):
        return 1, 0, randint(0,classic[0]-1)
    # 408 RE
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148 - 408):
        return 0, 2, randint(0,classic[2]-1)
    # 2160 RR
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148 - 408 - 2160):
        return 0, 1, randint(0,classic[1]-1)
    # 7036 RC
    else:
        return 0, 0, randint(0,classic[0]-1)
def generate_wotog_card():
    ranum = randint(0,10000)
    # 7 GL
    if ranum > (10000 - 7):
        return 1, 3, randint(0,wotog[3]-1)
    # 19 GE
    elif ranum > (10000 - 7 - 19):
        return 1, 2, randint(0,wotog[2]-1)
    # 94 RL
    elif ranum > (10000 - 7 - 19 - 94):
        return 0, 3, randint(0,wotog[3]-1)
    # 127 GR
    elif ranum > (10000 - 7 - 19 - 94 - 127):
        return 1, 1, randint(0,wotog[1]-1)
    # 148 GC
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148):
        return 1, 0, randint(0,wotog[0]-1)
    # 408 RE
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148 - 408):
        return 0, 2, randint(0,wotog[2]-1)
    # 2160 RR
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148 - 408 - 2160):
        return 0, 1, randint(0,wotog[1]-1)
    # 7036 RC
    else:
        return 0, 0, randint(0,wotog[0]-1)

if __name__ == "__main__":
    main()