#!/bin/bash 
mkdir -p models/detect
cd models/detect
curl -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5 \
	-O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5 \
	-O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo-tiny.h5
cd -
mkdir models/classify
cd models/classify
curl -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/mobilenet_v2.h5 \
	  -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_imagenet_tf.2.0.h5 \
	  -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/inception_v3_weights_tf_dim_ordering_tf_kernels.h5 \
	  -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/DenseNet-BC-121-32.h5
cd -
