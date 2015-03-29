#!/bin/python

import sys, math

#######################################
#              CONSTANTS              #
#######################################
IMAGE_LABEL_FILES = ['/data/MM21/iyu/junk/proto/RESEARCH.koala.1000.shot.predict',
                     '/data/MM21/iyu/junk/proto/PSTRAIN.koala.1000.shot.predict']
AUDIO_LABEL_FOLDER = '/data/VOL2/yipeiw/share/submit2013/noiseme/confidence/2s_100ms_main/'

IMAGE_LABEL_SCORE_THRESHOLD = 0.3
NOISEME_LABEL_SCORE_THRESHOLD = 0.5

IMAGE_LABEL_NUM = 1000
NOISEME_LABEL_NUM = 40


#######################################
#              VARIABLES              #
#######################################
curr_video_id = None
curr_noiseme_lines = None
noiseme_succ = False

noiseme_and_concept_dict = {}
concept_dict = {}
noiseme_not_concept_dict = {}
not_concept_dict = {}


#######################################
#              MAIN FUNC              #
#######################################

# init all the dictionaries
for concept in xrange(1, IMAGE_LABEL_NUM + 1):
    concept_dict[concept] = 0
    not_concept_dict[concept] = 0
    for noiseme in xrange(1, NOISEME_LABEL_NUM + 1):
        noiseme_and_concept_dict[(noiseme, concept)] = 0
        noiseme_not_concept_dict[(noiseme, concept)] = 0

# read keyframe image concepts
for image_label_file_path in IMAGE_LABEL_FILES:
    image_label_file = open(image_label_file_path, 'r')
    try:
        for keyframe in image_label_file:
            str_arr = keyframe.split(' ')
            keyframe_info = str_arr[0].split('_')
            video_id = keyframe_info[0]
            timestamp = keyframe_info[1]

            # update the noiseme cache if necessary
            if curr_video_id != video_id:
                curr_video_id = video_id
                try:
                    f = open(AUDIO_LABEL_FOLDER + video_id + '.txt', 'r')
                except IOError:
                    sys.stderr.write('No audio labels: %s\n' % video_id)
                    noiseme_succ = False
                    continue 
                except TypeError:
                    sys.stderr.write('TypeError: %s\n' % video_id)
                    sys.stderr.write('TypeError: %s\n' % keyframe)
                    return
                else:
                    curr_noiseme_lines = f.readlines()
                    noiseme_succ = True
                    f.close()
            elif not noiseme_succ:
                continue

            # compute the target time frame
            # every 0.1 second is a time frame
            time_arr = timestamp.split('^')
            minute = time_arr[0]
            second = time_arr[1][:-4] # '03.033.jpg'[:-4] = '03.033'
            line_num = int(minute) * 600 + int(float(second) * 10)

            # get noiseme info in that time frame
            try:
                audio_info = curr_noiseme_lines[line_num].split(' ')
            except IndexError:
                sys.stderr.write('%s have:%d try:%d\n' % (video_id, len(curr_noiseme_lines), line_num))

            # find positive noiseme labels in target time frame
            labels = set([])
            for i in xrange(len(audio_info)):
                flag_and_score = audio_info[i].split(':')
                if flag_and_score[0][0] == '1': # '1.0'[0] = '1'
                    if float(flag_and_score[1]) > NOISEME_LABEL_SCORE_THRESHOLD:
                        labels.add(i + 1)

            # for each image concept
            for i in xrange(1, len(str_arr)):
                concept_info = str_arr[i].split(':')
                concept_id = int(concept_info[0])
                concept_conf = float(concept_info[1])
                # if we see some image concept
                if concept_conf > IMAGE_LABEL_SCORE_THRESHOLD:
                    concept_dict[concept_id] += 1
                    for noiseme_id in labels:
                        noiseme_and_concept_dict[(noiseme_id, concept_id)] += 1
                # if we did not see the image concept
                else:
                    not_concept_dict[concept_id] += 1
                    for noiseme_id in labels:
                        noiseme_not_concept_dict[(noiseme_id, concept_id)] += 1
    finally:
        image_label_file.close()

correlation = []
# compute BLRT
for concept in xrange(1, IMAGE_LABEL_NUM + 1):
    for noiseme in xrange(1, NOISEME_LABEL_NUM + 1):
        k1 = noiseme_and_concept_dict[(noiseme, concept)]
        k2 = noiseme_not_concept_dict[(noiseme, concept)]
        n1 = concept_dict[concept]
        n2 = not_concept_dict[concept]
        p = float(k1 + k2) / (n1 + n2)
        p1 = float(k1 / n1)
        p2 = float(k2 / n2)
        L111 = (p1 ** k1) * ((1 - p1) ** (n1 - k1))
        L222 = (p2 ** k2) * ((1 - p2) ** (n2 - k2))
        L_11 = (p ** k1) * ((1 - p) ** (n1 - k1))
        L_22 = (p ** k2) * ((1 - p) ** (n2 - k2))
        BLRT = 2 * math.log((L111 * L222) / (L_11 * L_22))
        correlation.append((noiseme, concept, BLRT))

correlation.sort(key = lambda x: x[2], reverse = True)

for (noiseme, concept, BLRT) in correlation:
    print '%d\t%d\t%f' % (noiseme, concept, BLRT)
