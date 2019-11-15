# !/user/bin/python
# coding: utf-8

import random
import numpy as np
import itertools
import matplotlib.pyplot as plt


NUM_ATTRIBUTES = 4
NUM_TOPS = 1
GROUP_SIZE = 20
UNIT_SIZE = 0.2
NUM_TRIALS = 100

class Person:
    def __init__(self, attr_list = None, random_func=np.random.rand):
        if attr_list == None:
            self.attr_list = random_func(NUM_ATTRIBUTES)
        else:
            self.attr_list = attr_list

        self.accumulated_rank_score = 0
        self.total_match_cntr = 0
        self.cntr_per_rank = [0 for i in range(NUM_TOPS + 1)]


def get_shuffled_member_ids_per_group (num_members, group_size):
    shuffled_member_ids = range(num_members)
    random.shuffle(shuffled_member_ids)
    member_ids_per_group = devide_list2group(shuffled_member_ids, group_size)
    return member_ids_per_group

def devide_list2group(list, group_size):
    num_groups = int(len(list) / group_size)
    groups = [list[i * group_size : (i + 1) * group_size] for i in range (num_groups)]
    groups[-1] = groups[-1] + list[num_groups * group_size : len(list)]
    return groups

def test_devide_list2group():
    l = range(11)
    group_size = 3
    actual = devide_list2group(l, group_size)
    expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9, 10]]
    show_test_result("devide_list2group()", actual, expected)

    l = range(20)
    group_size = 4
    actual = devide_list2group(l, group_size)
    expected = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]]
    show_test_result("devide_list2group()", actual, expected)
    

def trial (all_men_members, num_attributes, unit_size, group_size):
    num_members = len(all_men_members)
    for member_ids in get_shuffled_member_ids_per_group(num_members, group_size):
        men_group = [all_men_members[member_id] for member_id in member_ids]
        num_men_group = len(men_group)
        women_group = [Person() for i in range(group_size)]
        meetup(men_group, women_group)

def test_trial():
    num_attributes = 3
    unit_size = 0.1
    group_size = 6
    all_men_members = create_all_men(num_attributes, unit_size)
    trial(all_men_members, num_attributes, unit_size, group_size)
    trial(all_men_members, num_attributes, unit_size, group_size)

    for index, member in enumerate(all_men_members):
        if member.total_match_cntr != group_size * 2:
            print "Test of trial() failed ! index:", index, "member.total_match_cntr", member.total_match_cntr

    print "Test of trial() passed !"

def create_all_men(num_attributes, unit_size):
    all_men = []
    all_attr_comb_list = get_all_attr_comb_list(num_attributes, unit_size)
    for attrs in all_attr_comb_list:
        all_men.append(Person(attr_list = list(attrs)))
    return all_men

def meetup(men_group, women_group):
    for woman in women_group:
        score_list = [match(man, woman) for man in men_group]
        rank_per_id_list = get_top_ranked_id_list (score_list, NUM_TOPS)
        for man, rank in zip(men_group, rank_per_id_list):
            man.accumulated_rank_score += rank
            man.cntr_per_rank[rank] += 1

def test_meet_up ():
    man1 = Person(attr_list = [1, 1, 1])
    man2 = Person(attr_list = [0.5, 0.5, 0.5])
    man3 = Person(attr_list = [0.5, 0.5, 0.5])
    man4 = Person(attr_list = [0, 0, 0])
    woman1 = Person(attr_list = [1, 1, 1])
    woman2 = Person(attr_list = [1, 1, 1])
    woman3 = Person(attr_list = [1, 1, 1])
    men_group = [man1, man2, man3, man4]
    women_group = [woman1, woman2, woman3]
    meetup(men_group, women_group)
    print "man1.total_match_cntr", man1.total_match_cntr
    print "man2.total_match_cntr", man2.total_match_cntr
    print "man3.total_match_cntr", man3.total_match_cntr
    print "man4.total_match_cntr", man4.total_match_cntr
    print "man1.accumulated_rank_score", man1.accumulated_rank_score
    print "man2.accumulated_rank_score", man2.accumulated_rank_score
    print "man3.accumulated_rank_score", man3.accumulated_rank_score
    print "man4.accumulated_rank_score", man4.accumulated_rank_score

def get_all_attr_comb_list(num_attributes, unit_size):
    if (1 / unit_size) % 1 > 0.0001:
        print "[ERROR] this unit_size is unacceptable !"
        return -1

    magnif = int(1 / unit_size)
    l = [float(i) / magnif for i in range(1, int(1 / unit_size) + 1)]
    all_attr_comb_list = list(itertools.product(l, repeat=num_attributes))

    if magnif ** num_attributes != len(all_attr_comb_list):
        print "[ERROR] the combination size is wrong !"
        return -1

    return all_attr_comb_list

def test_get_all_attr_comb_list(num_attributes, unit_size):
    print "--<test_get_all_attr_comb_list>--"
    print get_all_attr_comb_list(num_attributes, unit_size)
    print "**<test_get_all_attr_comb_list>**"

def get_top_ranked_id_list (score_list, num_tops):
    if (len(score_list) < num_tops):
        print "[WARN] num_tops overnumbers score_list"

    top_ranked_id_list = [0 for i in range(len(score_list))]
    sorted_id_list = np.argsort(np.array(score_list))[::-1]
    for id, rank in zip(sorted_id_list [:num_tops], range(num_tops, -1, -1)):
        top_ranked_id_list[id] = rank
    return top_ranked_id_list

def test_get_top_ranked_id_list():
    score_list = [1, 4, 3, 0, 2]
    num_tops = 2
    actual = get_top_ranked_id_list (score_list, num_tops)
    expected = [0, 2, 1, 0, 0]
    show_test_result("get_top_ranked_id_list()", actual, expected)
    

def match(man, woman):
    score = 0
    man.total_match_cntr += 1
    for i, j in zip(man.attr_list, woman.attr_list):
        score = score + i * j
    return score

def test_match():
    man = Person(attr_list = [1, 1, 1])
    woman = Person(attr_list = [0.5, 0.5, 0.5])
    actual = match(man, woman)
    expected = 1.5
    show_test_result("match()", actual, expected)

def show_test_result(func_name, actual, expected):
    if actual == expected:
        print "Test of", func_name ,"passed!"
    else:
        print "Test of", func_name ,"failed! : the actual value was", actual, "but it supposed to be", expected

def main():
    all_men_members = create_all_men(NUM_ATTRIBUTES, UNIT_SIZE)
    for i in range(NUM_TRIALS):
        trial(all_men_members, NUM_ATTRIBUTES, UNIT_SIZE, GROUP_SIZE)

    d1, d2 = dict(), dict()
    for man in all_men_members:
        summed_attr = sum(man.attr_list)
        if summed_attr in d1.keys():
            d1[summed_attr] = [d1[summed_attr][0] + man.accumulated_rank_score, d1[summed_attr][1] + 1]
        else:
            d1[summed_attr] = [man.accumulated_rank_score, 1]

    for k, v in d1.items():
        average = (float(v[0])/v[1]) / (NUM_TRIALS * GROUP_SIZE * NUM_TOPS)
        plt.plot(k, average, marker = 'o', color = "blue")

    plt.show()

if __name__ == '__main__':
    main()
