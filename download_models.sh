#!/bin/bash
mkdir -p models/detect
cd models/detect
echo "Downloading detection models..."
curl -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5 \
	-O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5 \
	-O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo-tiny.h5
cd -
mkdir models/classify
cd models/classify
echo "Downloading classification models..."
curl -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/mobilenet_v2.h5 \
	  -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_imagenet_tf.2.0.h5 \
	  -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/inception_v3_weights_tf_dim_ordering_tf_kernels.h5 \
	  -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/DenseNet-BC-121-32.h5
echo "Checking hashes for classification model files..."
sha256sum -c ../../checksums --check --strict
if [ $? -eq 0 ]
then
    echo "Success. Checksums match!"
else
    echo "Failure. Checksums don't match! Verify the download links are still correct."
    echo "Removing classification models."
    rm *.h5
fi
mkdir ~/.keras/models
cd ~/.keras/models
curl -O -L https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json
