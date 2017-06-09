import os
import tensorflow as tf 
from PIL import Image
import argparse

# Parameters
path_list = ['../X_data', '../T_data']
data_list = ["tfrecords/train.tfrecords", "tfrecords/test.tfrecords"]
age = ['child', 'young', 'adult', 'elder']
gender = ['male', 'female']

#
def _int64_feature(value):
	return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def _bytes_feature(value):
	return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def data_converter(path, tf_data, verbose, split):
	numlist = []
	if not split:
		with tf.python_io.TFRecordWriter(tf_data) as converter:
			for idx_age, itr_age in enumerate(age):
				for idx_gender, itr_gender in enumerate(gender):
					class_label = [idx_age + idx_gender * 4]
					current_path = "{:s}/{:s}/{:s}/".format(path, itr_age, itr_gender)
					
					n_file = sum(os.path.isfile(os.path.join(current_path, itr_dir)) \
								for itr_dir in os.listdir(current_path))
					numlist.append(n_file)
					if verbose:
						print "{:s}: {:4d} files".format(current_path, n_file)
					for itr_file in os.listdir(current_path):
						if itr_file.endswith('.jpg'):
							img_path = current_path + itr_file
							img = Image.open(img_path)
							img_raw = img.tobytes()
							# stream data to the converter
							example = tf.train.Example(features=tf.train.Features(
							feature=
							{ 
								"label"  : _int64_feature(class_label),
								"img_raw": _bytes_feature(img_raw)
							} ))
							converter.write(example.SerializeToString())
						else:
							continue
	else:
		for idx_age, itr_age in enumerate(age):
			for idx_gender, itr_gender in enumerate(gender):
				class_label = [idx_age + idx_gender * 4]
				current_path = "{:s}/{:s}/{:s}/".format(path, itr_age, itr_gender)
				
				n_file = sum(os.path.isfile(os.path.join(current_path, itr_dir)) \
							for itr_dir in os.listdir(current_path))
				numlist.append(n_file)
				if verbose:
					print "{:s}: {:4d} files".format(current_path, n_file)
				tf_name = "tfrecords/{:s}_{:d}.tfrecords".format(tf_data[10:12], class_label[0])
				with tf.python_io.TFRecordWriter(tf_name) as converter:
					for itr_file in os.listdir(current_path):
						if itr_file.endswith('.jpg'):
							img_path = current_path + itr_file
							img = Image.open(img_path)
							img_raw = img.tobytes()
							# stream data to the converter
							example = tf.train.Example(features=tf.train.Features(
							feature=
							{ 
								"label"  : _int64_feature(class_label),
								"img_raw": _bytes_feature(img_raw)
							} ))
							converter.write(example.SerializeToString())
						else:
							continue
	print "{:s}: {:d}".format(path, sum(numlist))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", action="count",
						help="show info in each directory")
	parser.add_argument("-s", "--split", action="count",
						help="split every class to separate files")
	
	args = parser.parse_args()
	if not os.path.isdir('tfrecords'):
		os.makedirs('tfrecords')
	for idx, itr_path in enumerate(path_list):
		data_converter(itr_path, data_list[idx], args.verbosity, args.split)