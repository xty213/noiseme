###############################
#        NOISEME INFO         #
###############################
NOISEME_SEGMENT_NUM = [11, 64, 20, 20, 28, 113, 9, 72, 35, 195, 
                       216, 42, 115, 26, 12, 34, 55, 18, 138, 86, 
                       36, 295, 57, 47, 10, 32, 168, 65, 41, 16, 
                       1181, 121, 26, 65, 5, 97, 69, 2, 111, 25]
NOISEME_DURATION = [0.22, 4.14, 0.17, 1.0, 2.92, 0.95, 0.08, 4.85, 0.56, 2.98, 
                    8.35, 0.23, 11.15, 5.68, 0.37, 4.07, 2.71, 0.12, 0.96, 2.11, 
                    1.43, 8.01, 35.34, 36.6, 2.26, 5.77, 8.14, 3.56, 1.09, 1.34, 
                    42.75, 4.02, 0.75, 0.27, 0.96, 3.44, 3.66, 0.02, 5.57, 4.54]

###############################
#          FILE PATH          #
###############################
IMAGE_HIERARCHY_PATH = "/Users/tianyux/Documents/775/project/repo/image_concepts/koala_concept_categories.csv"
IMAGE_RELIABILITY_PATH = "/Users/tianyux/Documents/775/project/repo/image_concepts/koala_concept_reliability.csv"
INPUT_PATH = "/Users/tianyux/Documents/775/project/repo/result/weighted_sum.txt"

###############################
#          PARAMETER          #
###############################
NOISEME_DURATION_THRESHOLD = 1.0
IMAGE_RELIABILITY_THRESHOLD = 3

def noiseme_duration_filter(data):
    return filter(lambda x: NOISEME_DURATION[x[0] - 1] >= NOISEME_DURATION_THRESHOLD, data)

def image_reliability_filter(data):
    reliabilities = {}
    with open(IMAGE_RELIABILITY_PATH, 'r') as f:
        for line in f:
            line_arr = line.split(",")
            reliabilities[int(line_arr[0])] = int(line_arr[-3])

    return filter(lambda x: reliabilities[x[1]] >= IMAGE_RELIABILITY_THRESHOLD, data)

def merge_image_hierarchy(data):
    hierarchy = []
    with open(IMAGE_HIERARCHY_PATH, 'r') as f:
        for line in f:
            hierarchy.append(line.strip().split(",")[-1])
    
    score_dict = {}
    for (nid, cid, score) in data:
        new_key = (nid, hierarchy[cid - 1])
        if new_key not in score_dict:
            score_dict[new_key] = 0
        score_dict[new_key] += score

    nids = map(lambda x: x[0], score_dict.keys())
    concepts = map(lambda x: x[1], score_dict.keys())
    new_data = zip(nids, concepts, score_dict.values())
    new_data.sort(key=lambda x: x[2], reverse=True)
    return new_data

def print_data(data):
    for n, c, s in data:
        print "%d\t%s\t%f" % (n, str(c), s)

if __name__ == "__main__":
    # read-in original weighted sum data
    data = []
    with open(INPUT_PATH, 'r') as f:
        for line in f:
            line_arr = line.split()
            data.append((int(line_arr[0]), int(line_arr[1]), float(line_arr[2])))

    data = noiseme_duration_filter(data)
    data = image_reliability_filter(data)
    # data = merge_image_hierarchy(data)
    print_data(data)
