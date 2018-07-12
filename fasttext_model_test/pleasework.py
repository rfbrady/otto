#!/usr/bin/env python

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division, absolute_import, print_function

import os
import csv
from fastText import train_supervised



def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

if __name__ == "__main__":
    text_list = []
<<<<<<< HEAD
    ofp = os.getcwd() + '/model_statistics_truncated_3.csv'
=======
    ofp = os.getcwd() + '/model_statistics_truncated_2.csv'
>>>>>>> 2e61322c3a135bf5cfb4dac034896842d90dc93b

    with open(ofp, 'w') as csvfile:
        fieldnames = ['Epoch','LR','P1','R1','P2','R2']
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldnames)
        train_data = os.path.join(os.getcwd(), 'truncated.train')
        valid_data = os.path.join(os.getcwd(), 'truncated.valid')
<<<<<<< HEAD
        #lr_range = [.1, .2, .3, .4, .5, .6, .7, .8, .9]
        #epoch_range = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        lr_range = [.3]
        epoch_range = [25]
=======
        lr_range = [.1, .2, .3, .4, .5, .6, .7, .8, .9]
        epoch_range = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

        epoch = 10
>>>>>>> 2e61322c3a135bf5cfb4dac034896842d90dc93b
        for lr in lr_range:
            print(lr)
            for epoch in epoch_range:
                print(epoch)
                # train_supervised uses the same arguments and defaults as the fastText cli
                model = train_supervised(
                    input=train_data, epoch=epoch, lr=lr, wordNgrams=2, verbose=1, minCount=1, bucket=500000
                )
<<<<<<< HEAD

                model.save_model('truncated_model')
=======
>>>>>>> 2e61322c3a135bf5cfb4dac034896842d90dc93b
                #print_results(*model.test(valid_data))
                p1 = str(round(model.test(valid_data)[1], 3))
                r1 = str(round(model.test(valid_data)[2], 3))

                p2 = str(round(model.test(valid_data, 2)[1], 3))
                r2 = str(round(model.test(valid_data, 2)[1], 3))

                p3 = str(round(model.test(valid_data, 3)[1], 3))
                r3 = str(round(model.test(valid_data, 3)[1], 3))

                print("{}{}".format(p1, r1))
                print("{}{}".format(p2, r2))
                print("{}{}".format(p3, r3))
                writer.writerow([epoch, lr, p1, r1, p2, r2])


                
                #model = train_supervised(
                #   input=train_data, epoch=40, lr=.4, wordNgrams=2, verbose=1, minCount=1, bucket=500000,
                #    loss="hs"
                #)
                #print_results(*model.test(valid_data))

                #model.quantize(input=train_data, qnorm=True, retrain=True, cutoff=100000)
                #print_results(*model.test(valid_data))
                #model.save_model("cooking.ftz")
