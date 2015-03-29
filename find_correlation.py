#!/bin/python

import sys

#######################################
#              CONSTANTS              #
#######################################
IMAGE_LABEL_FILES = ['/data/MM21/iyu/junk/proto/RESEARCH.koala.1000.shot.predict',
                     '/data/MM21/iyu/junk/proto/PSTRAIN.koala.1000.shot.predict']
AUDIO_LABEL_FOLDER = '/data/VOL2/yipeiw/share/submit2013/noiseme/confidence/2s_100ms_main/'

IMAGE_LABEL_SCORE_THRESHOLD = 0.1


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
                    sys.stderr.write('No audio labels: %s\n' % video_id)
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
                sys.stderr.write('%s have:%d try:%d\n' % (video_id, len(curr_noiseme_lines), line_num))

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
                        print '%d:%d\t%f' % (concept_id, label, noiseme_score * concept_conf)
    finally:
        image_label_file.close()
