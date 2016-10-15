import tflearn as tfl

# Deep neural network implemented by Tflearn
def tflearn_DNN_training(X, Y, mns): # return weights and biases\
	

	# Build network
	net = tfl.input_data(shape=[None, len(X[0])], name='input')
	
	net = tfl.fully_connected(net, 256, name='dense2')
	net = tfl.fully_connected(net, 128, name='dense3')

	net = tfl.fully_connected(net, len(Y[0]), name='dense1',activation='softmax')
	regression = tfl.regression(net, optimizer='sgd',
                                learning_rate=0.005,
                                loss='categorical_crossentropy')

	# Define classifier, with model checkpoint (autosave)
	model = tfl.DNN(regression)

	# Train model, with model checkpoint every epoch and every 200 training steps.
	model.fit(X, Y, n_epoch=5, batch_size=80,run_id='model_and_weights')

	# ------------------
	# Retrieving weights
	# ------------------
	#print("Dense1 layer biases:")
	#print(model.get_weights(tfl.variables.get_layer_variables_by_name('dense2')[1]))


	return model.get_weights(tfl.variables.get_layer_variables_by_name('dense2')[0])