#!/bin/python

import sys, math
from decimal import Decimal, InvalidOperation

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

# TARGET_PAIRS = [(27, 917), (27, 484), (31, 923), (31, 904), (13, 891), (27, 923), (13, 982), (19, 484), (19, 917), (4, 195), (3, 797), (19, 294), (27, 294), (1, 801), (18, 801)]
TARGET_PAIRS = [(10, 183), (31, 611), (27, 531), (24, 796), (13, 600), (24, 782), (37, 295), (20, 984), (27, 577), (37, 236), (5, 898)]

#######################################
#              VARIABLES              #
#######################################
curr_video_id = None
curr_noiseme_lines = None
noiseme_succ = False


#######################################
#              MAIN FUNC              #
#######################################

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
                    #sys.stderr.write('No audio labels: %s\n' % video_id)
                    noiseme_succ = False
                    continue 
                except TypeError:
                    #sys.stderr.write('TypeError: %s\n' % video_id)
                    #sys.stderr.write('TypeError: %s\n' % keyframe)
                    noiseme_succ = False
                    continue
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
                pass
                #sys.stderr.write('%s have:%d try:%d\n' % (video_id, len(curr_noiseme_lines), line_num))

            # find positive noiseme labels in target time frame
            labels = set([])
            for i in xrange(NOISEME_LABEL_NUM):
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
                    for noiseme_id in labels:
                        if (noiseme_id, concept_id) in TARGET_PAIRS:
                            print "%s, %s, %s, (%d, %d)" % (video_id, minute, second, noiseme_id, concept_id)
    finally:
        image_label_file.close()
