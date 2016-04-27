from random import *

#common, rare, epic, legendary
cards_nerfed = [2,5,4,0]
card_cap = [2,2,2,1]
classic = [94,81,37,33] #sum = 245
wotog = [50,36,27,21]   
reg_de_amt  =     [5  , 40 , 100 , 400 ]
reg_full_amt =    [40 , 100, 400 , 1600]
golden_de_amt =   [50 , 100, 400 , 1600]
golden_full_amt = [400, 800, 1600, 3200]
num_sims = 1000
sim_granularity = 5
sim_range_start = 0
sim_range_end = 91
def main():
    #start wotog 50 packs sim
    dust_result_accu = 0.0
    for i in range(num_sims):
        dust_ctr = 0.0
        card_collection = []
        for j in range(len(wotog)):
            card_collection.append([])
            for k in range(0, wotog[j]):
                card_collection[j].append([0,0])
        # simulate pack openings
        for j in range(5*50):
            golden, rarity, num = generate_card(wotog)
            card_collection[rarity][num][golden]= card_collection[rarity][num][golden]+1
        for rarity in range(0,4):
            for card_num in range(wotog[rarity]):
                while( card_collection[rarity][card_num][0] + 
                       card_collection[rarity][card_num][1] ) > card_cap[rarity]:
                        if card_collection[rarity][card_num][1] > 0:
                            card_collection[rarity][card_num][1] = card_collection[rarity][card_num][1] - 1
                            dust_ctr = dust_ctr + golden_de_amt[rarity]
                        else:
                            card_collection[rarity][card_num][0] = card_collection[rarity][card_num][0] - 1
                            dust_ctr = dust_ctr + reg_de_amt[rarity]
                dust_ctr = dust_ctr + \
                           card_collection[rarity][card_num][1] * golden_de_amt[rarity] + \
                           card_collection[rarity][card_num][0] * reg_full_amt[rarity]
        dust_result_accu = dust_result_accu + float(dust_ctr)/num_sims
    print("Buying WotoG: " + str(int(dust_result_accu)) + " dust")
    
    
    #Start classic sim
    # number of cards able to be collected from set
    cards_in_set = 0
    working_set = classic
    set_name = "classic"
    cards_in_set = cards_in_set + working_set[0] * 2
    cards_in_set = cards_in_set + working_set[1] * 2
    cards_in_set = cards_in_set + working_set[2] * 2
    cards_in_set = cards_in_set + working_set[3]
    for collection_percent in range(sim_range_start, sim_range_end, sim_granularity):
        dust_result_accu = 0.0
        collection_gen_cond = int(cards_in_set * collection_percent * 0.01)
        for i in range(num_sims):
            nerfdust_ctr = 0.0
            card_collection = []
            prior_card_collection = []
            # generate empty collection buckets
            for j in range(len(working_set)):
                prior_card_collection.append([])
                card_collection.append([])
                for k in range(0, working_set[j]):
                    prior_card_collection[j].append([0,0])
                    card_collection[j].append([0,0])
            # generate a percentage of the user's working_set collection
            # the beforehand collection (prior_card_collection) must be kept separate from the 
            # "opened today" collection (card_collection) because we cannot consider cards that were
            # opened prior to opening our 50 packs.
            completion = 0
            while(completion < collection_gen_cond):
                golden, rarity, num = generate_card(working_set)
                if(prior_card_collection[rarity][num][0] + prior_card_collection[rarity][num][1]) < card_cap[rarity]:
                    prior_card_collection[rarity][num][golden] = prior_card_collection[rarity][num][golden]+1
                    completion = completion + 1
            #simulate the opening of 50 packs
            for j in range(5*50):
                golden, rarity, num = generate_card(working_set)
                card_collection[rarity][num][golden]= card_collection[rarity][num][golden] + 1
            # for cards of all rarity
            for rarity in range(0,4):
                # for each card in each rarity
                for card_num in range(working_set[rarity]):
                    # if this card has been nerfed (first N cards in each rarity are nerfed)
                    if card_num <= (cards_nerfed[rarity]-1):
                        # add full dust value of all opened cards to dust counter
                        nerfdust_ctr =  nerfdust_ctr + \
                                   card_collection[rarity][card_num][1] * golden_full_amt[rarity] + \
                                   card_collection[rarity][card_num][0] * reg_full_amt[rarity]
                    # if this card was not nerfed
                    else:
                        # while we have more than enough of the current card
                        while(  card_collection[rarity][card_num][0] + 
                                card_collection[rarity][card_num][1] +
                                prior_card_collection[rarity][card_num][0] + 
                                prior_card_collection[rarity][card_num][1] ) > card_cap[rarity]:
                            # try to disenchant a golden copy of the card
                            if card_collection[rarity][card_num][1] > 0:
                                card_collection[rarity][card_num][1] = card_collection[rarity][card_num][1] - 1
                                nerfdust_ctr = nerfdust_ctr + golden_de_amt[rarity]
                            # if there are no more golden copies, disenchant a regular one
                            else:
                                card_collection[rarity][card_num][0] = card_collection[rarity][card_num][0] - 1
                                nerfdust_ctr = nerfdust_ctr + reg_de_amt[rarity]
                        # add remaining cards opened in 50 packs
                        nerfdust_ctr = nerfdust_ctr + \
                                   card_collection[rarity][card_num][1] * golden_de_amt[rarity] + \
                                   card_collection[rarity][card_num][0] * reg_full_amt[rarity]
                        
            dust_result_accu = dust_result_accu + float(nerfdust_ctr)/num_sims
        print(str(collection_percent) + "% " + set_name + " cards collected: " + str(int(dust_result_accu)) + " dust")


def generate_card(set):
    ranum = randint(0,10000)
    # GL
    if ranum > (10000 - 7):
        return 1, 3, randint(0,set[3]-1)
    # GE
    elif ranum > (10000 - 7 - 19):
        return 1, 2, randint(0,set[2]-1)
    # RL
    elif ranum > (10000 - 7 - 19 - 94):
        return 0, 3, randint(0,set[3]-1)
    # GR
    elif ranum > (10000 - 7 - 19 - 94 - 127):
        return 1, 1, randint(0,set[1]-1)
    # GC
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148):
        return 1, 0, randint(0,set[0]-1)
    # RE
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148 - 408):
        return 0, 2, randint(0,set[2]-1)
    # RR
    elif ranum > (10000 - 7 - 19 - 94 - 127 - 148 - 408 - 2160):
        return 0, 1, randint(0,set[1]-1)
    # RC
    else:
        return 0, 0, randint(0,set[0]-1)
if __name__ == "__main__":
    main()