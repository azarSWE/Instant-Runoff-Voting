

def read_file():
    """
    read_file - A function to read the data from input file and stores it into a list of lists
    :return: a list of lists which each list represents votes options given by each voter
    """
    file_name = input("Enter the name of the file: ")
    votes_result = []
    with open(file_name, 'r') as fh:
        for line in fh:
            vote = []
            for number in line.strip().split(','):
                try:
                    vote.append(int(number))
                except ValueError:
                    continue
            votes_result.append(vote)
    return votes_result


def get_candidates_id(votes_list):
    """
    get_candidates_id - A function to determine the ID of candidates who are still in competition
    :param votes_list: a list of lists containing votes for each candidate who is still in competition
    :return: a list of candidates' ID
    """
    candidates_id = []
    for i in range(len(votes_list)):
        for j in range(len(votes_list[i])):
            if votes_list[i][j] not in candidates_id:
                candidates_id.append(votes_list[i][j])
    return candidates_id


def get_votes_dict(votes_list):
    """
    get_votes_dict - A function to convert a list of votes to a dictionary structure type
    :param votes_list: a list of votes
    :return: votes_dict a dictionary, key: candidate' ID and value: the number of first place votes
    """
    candidates_id = get_candidates_id(votes_list)
    votes_dict = {}
    for i in range(len(candidates_id)):
        votes_dict[candidates_id[i]] = 0
        for j in range(len(votes_list)):
            if votes_list[j][0] == candidates_id[i]:
                votes_dict[candidates_id[i]] += 1
    return votes_dict


def eliminate_candidate(votes_dict):
    """
    eliminate_candidate - A function to determine which candidate has should be eliminated in a round,
    which incorporates the tie-breaking method for those candidates with equal first place votes
    :param votes_dict: a dictionary of votes, key: candidate's ID and value: the number of first place votes
    :return: a list of candidates which are eliminated
    """
    # calculate sum of first place votes
    sum_votes = 0
    for keys, values in votes_dict.items():
        sum_votes += values

    # determine the candidate with highest first place vote
    highest_votes = 0
    highest_candidate = ''
    for key, value in votes_dict.items():
        if highest_votes < value:
            highest_votes = value
            highest_candidate = key

    # check if candidate with highest first place votes has more than 50% votes and
    # produce an ordered list of eliminated candidates
    elimination_list = []
    if (highest_votes / sum_votes) * 100 > 50:
        for keys in sorted(votes_dict.keys()):
            if keys != highest_candidate:
                elimination_list.append(keys)
        elimination_list.append(highest_candidate)

    # otherwise, determine candidate with the minimum first place votes
    else:
        lowest_votes = highest_votes
        lowest_candidate = highest_candidate
        for keys, values in votes_dict.items():
            if lowest_votes > values:
                lowest_votes = values
                lowest_candidate = keys
            elif lowest_votes == values and lowest_candidate < keys:
                lowest_votes = values
                lowest_candidate = keys
        elimination_list.append(lowest_candidate)
    return elimination_list


def update_votes(votes_list, eliminated_list):
    """
    update_votes - A function to update the votes in the election by eliminating
    candidates with minimum first place vote.
    :param votes_list: a list of votes
    :param eliminated_list: a list of candidates who were eliminated in a round of competition
    :return: an updated list of votes without eliminated candidates
    """
    for i in range(len(votes_list)):
        if eliminated_list[0] in votes_list[i]:
            votes_list[i].remove(eliminated_list[0])
    votes_list = list(filter(None, votes_list))
    return votes_list


def main():
    votes_list = read_file()
    candidates_id = get_candidates_id(votes_list)
    votes_dict = get_votes_dict(votes_list)
    elimination_list = []
    elimination_list.extend(eliminate_candidate(votes_dict))
    while len(elimination_list) < len(candidates_id):
        votes_list = update_votes(votes_list, eliminate_candidate(votes_dict))
        votes_dict = get_votes_dict(votes_list)
        eliminate_candidate(votes_dict)
        elimination_list.extend(eliminate_candidate(votes_dict))

    # print candidates based on the elimination order
    print("Elimination order: ", end='')
    for i in range(len(elimination_list) - 1):
        print(elimination_list[i], end=', ')
    print(elimination_list[len(elimination_list) - 1])


main()
