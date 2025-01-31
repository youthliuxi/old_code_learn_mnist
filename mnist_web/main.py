import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request

from mnist import model

MODEL_SAVE_PATH = "./mnist/data/"

x = tf.placeholder("float", [None, 784])
sess = tf.Session()

with tf.variable_scope("regression"):
	y1, variables = model.regression(x)
saver = tf.train.Saver(variables)
saver.restore(sess, MODEL_SAVE_PATH + "regression.ckpt")

with tf.variable_scope("convolutional"):
	keep_prob = tf.placeholder("float")
	y2, variables = model.convolutional(x, keep_prob)
saver = tf.train.Saver(variables)
saver.restore(sess, MODEL_SAVE_PATH + "convolutional.ckpt")

def regression(input):
	return sess.run(y1, feed_dict = {x: input}).flatten().tolist()

def convolutional(input):
	return sess.run(y2, feed_dict = {x:input, keep_prob:1.0}).flatten().tolist()

app = Flask(__name__)

@app.route('api/mnist', methods=['post'])
def mnist():
	input = ((255 - np.array(request.json, dtype = np.uint8)) / 255.0).reshape(1, 784)
	output1 = regression(input)
	output2 = convolutional(input)
	return jsonify(results = [output1, output2])

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
