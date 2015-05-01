#!/bin/python

import sys

#######################################
#              CONSTANTS              #
#######################################
IMAGE_LABEL_FILES = ['/data/MM21/iyu/junk/proto/RESEARCH.koala.1000.shot.predict',
                     '/data/MM21/iyu/junk/proto/PSTRAIN.koala.1000.shot.predict']
AUDIO_LABEL_FOLDER = '/data/VOL2/yipeiw/share/submit2013/noiseme/confidence/2s_100ms_main/'
FEATURE_FOLDER = '/data/VOL2/yipeiw/share/submit2013/noiseme/LS_2s_100ms/scale_mergeANDmfcc/'

IMAGE_LABEL_SCORE_THRESHOLD = 0.3


#######################################
#              VARIABLES              #
#######################################
curr_video_id = None
curr_noiseme_lines = None
curr_feature_lines = None
noiseme_succ = False
corr_set = set([])

#######################################
#              MAIN FUNC              #
#######################################

# check for console parameters
if (len(sys.argv) < 3):
    print('Usage: %s refined_correlations output_file' % sys.argv[0])

# read correlation set
f = open(sys.argv[1], 'r')
for line in f:
    line_arr = line.split()
    corr_set.add((int(line_arr[0]), int(line_arr[1])))
f.close()
# print corr_set

out_file = open(sys.argv[2], 'w+')
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
                    g = open(FEATURE_FOLDER + video_id + '.mat', 'r')
                except IOError:
                    sys.stderr.write('No audio labels: %s\n' % video_id)
                    noiseme_succ = False
                    continue
                except TypeError:
                    sys.stderr.write('Type error: %s\n' % video_id)
                    noiseme_succ = False
                    continue
                else:
                    curr_noiseme_lines = f.readlines()
                    curr_feature_lines = g.readlines()
                    noiseme_succ = True
                    f.close()
                    g.close()
            elif not noiseme_succ:
                continue

            # compute the target time frame
            # every 0.1 second is a time frame
            time_arr = timestamp.split('^')
            minute = time_arr[0]
            second = time_arr[1][:-4] # '03.033.jpg'[:-4] = '03.033'
            line_num = int(minute) * 600 + int(float(second) * 10)

            # expand from a 0.1s window to the whole second
            end_idx = min(len(curr_feature_lines), line_num + 10)

            # get noiseme info in that time frame
            try:
                audio_info = curr_noiseme_lines[line_num].split(' ')
            except IndexError:
                sys.stderr.write('%s have:%d try:%d\n' % (video_id, len(curr_noiseme_lines), line_num))
                continue

            # find positive noiseme labels in target time frame
            labels = {}
            for i in xrange(len(audio_info)):
                noiseme_and_score = audio_info[i].split(':')
                if noiseme_and_score[0][0] == '1': # '1.0'[0] = '1'
                    labels[i + 1] = float(noiseme_and_score[1])

            for i in xrange(1, len(str_arr)):
                concept_info = str_arr[i].split(':')
                concept_id = int(concept_info[0])
                concept_conf = float(concept_info[1])
                # if we see some image concept
                if concept_conf >= IMAGE_LABEL_SCORE_THRESHOLD:
                    for label, noiseme_score in labels.items():
                        # print (label, concept_id)
                        # if the correlation is in the "target correlations"
                        if (label, concept_id) in corr_set:
                            for idx in xrange(line_num, end_idx):
                                out_file.write('%d %s' % (label, curr_feature_lines[idx]))
    finally:
        image_label_file.close()
out_file.close()
