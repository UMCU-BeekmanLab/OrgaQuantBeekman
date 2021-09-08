#Logger: https://docs.python.org/3/howto/logging.html
#Init logger
import logging
import logging.config
logging.config.fileConfig('conf/logging.conf')
logger = logging.getLogger(__file__)

#Import dependencies
import os
import sys 
import json
from pathlib import Path
import re
import time
import datetime
import trackpy as tp
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.client import device_lib
from keras_retinanet import models
from keras_retinanet.utils.gpu import setup_gpu
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image, adjust_contrast
from keras_retinanet.utils.visualization import draw_box
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## Supress TF warnings
#tf.logging.set_verbosity(tf.logging.ERROR)

## Set TF
setup_gpu(0)
logger.info(f'TF version: {tf.__version__}')
logger.info(f'Used Tensorflow backend: {device_lib.list_local_devices()}')

logger.info('Dependecies succesfull loaded!')

##Input variables 
#Input folder
input_dir=sys.argv[1]
if os.path.isdir(input_dir) == False:
            logger.error(f'Incorrect input path specified: {input_dir}')
            exit(0)
else:
    input_dir=os.path.join(input_dir, '')

#Process 
def main():
    
    #Get configuration
    conf = json.load(open(f'{input_dir}config.json'))
    model =  models.load_model(conf['model'], backbone_name='resnet50') 
    image_size = conf['image_size']
    contrast = conf['contrast']
    threshold = conf['threshold']
    regex_string = conf['regex']

    #Make results dir
    results_dir = f'{input_dir}results/'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    ##Build data frame
    results = pd.DataFrame({'x1':  pd.Series([], dtype=np.int16),
                            'y1': pd.Series([], dtype=np.int16), 
                            'x2': pd.Series([], dtype=np.int16), 
                            'y2': pd.Series([], dtype=np.int16),
                            'score': pd.Series([], dtype=np.float32),
                            'diameter_1_in_pixels': pd.Series([], dtype=np.int16),
                            'diameter_2_in_pixels': pd.Series([], dtype=np.int16),
                            'surface': pd.Series([], dtype=np.float32),
                            'image': pd.Series([], dtype='str'),
                            'well': pd.Series([], dtype='str'),
                            't': pd.Series([], dtype=np.int16),
                            'processing_timestamp': pd.Series([], dtype=np.int16)
                            })
    ##Process each image
    exclude_strings = ['_detected']
    imagelist = [i for i in Path(input_dir).glob('**/*.jpg') if not any(x in str(i) for x in exclude_strings)]

    logger.info('Start organoid detection')
    for i, IMAGE_PATH in enumerate(imagelist):
        logger.info(f'Analysing image: {i+1} of {len(imagelist)}')
        # load image
        image = read_image_bgr(IMAGE_PATH)

        # copy to draw on
        draw = image.copy()
        draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

        # preprocess image for network
        image = adjust_contrast(image, contrast)
        image = preprocess_image(image)
        image, scale = resize_image(image, min_side=image_size, max_side=2048)

        # process image
        boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))

        # correct for image scale
        boxes /= scale

        out = np.empty((0,4), dtype=np.float32)
        out_scores = []

        # visualize detections
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
        # scores are sorted so we can break
            if score < threshold:
                break
            out = np.append(out, box.reshape(1,4), axis=0)
            out_scores.append(score)

            b = box.astype(int)
            draw_box(draw, b, color=(255, 0, 255))

        #Save detected image
        plt.imsave(f'{results_dir}{str(IMAGE_PATH.name)}_detected.png', draw)

        ## Get results and append to results table
        output = pd.DataFrame(out,columns=['x1', 'y1', 'x2', 'y2'], dtype=np.int16)
        output['score'] = out_scores
        output['diameter_1_in_pixels'] = output['x2'] - output['x1']
        output['diameter_2_in_pixels'] = output['y2'] - output['y1']
        output['surface'] = (output['diameter_1_in_pixels'] / 2) * (output['diameter_2_in_pixels'] / 2) * np.pi
        output['image'] = str(IMAGE_PATH.name)
        output['well'] = re.search(regex_string, str(IMAGE_PATH.name)).group('WELL')
        output['t'] = re.search(regex_string, str(IMAGE_PATH.name)).group('T')
        output['processing_timestamp'] = int(time.time())
        results = results.append(output)
        
    logger.info('Organoid detection finished')
    logger.info(f'Results head: {results.head()}')
    ## Calculate centers and track organoids over time
    logger.info('Start tracking organoids')

    results['x'] = (results['x2'] + results['x1']) / 2
    results['y'] = (results['y2'] + results['y1']) / 2
    results = results.groupby('well').apply(tp.link, search_range=20, memory=2, t_column='t').reset_index(drop=True)
    
    ## Filter out particles that are seen less than 50% of the time
    results = results[results.groupby(['well','particle'])['t'].transform('count') >= (max(results['t']) / 2)]

    if len(results) == 0:
        logger.warning('Warning: no particles are detected in >= 50% of the time')
    logger.info('Finished tracking organoids')    
    ## Save results to csv
    logger.info('Saving results to csv...')
    results.to_csv(f'{results_dir}results.csv', index=False)

if __name__ == "__main__":
    logger.info('Starting job...')
    start = time.time()
    main()
    end = time.time()
    logger.info(f'Job completed in: {str(datetime.timedelta(seconds=(end-start)))} (HH:MM:SS)')