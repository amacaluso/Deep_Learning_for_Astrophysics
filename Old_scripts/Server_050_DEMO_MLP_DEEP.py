import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split

raw_data = pd.read_csv('DATA/df_ML.csv')  # Open raw .csv

# kilgharrah.iasfbo.inaf.it
# ------------------------------------------------------------------------------

## Variabili
Y_LABEL = 'Y'
KEYS = [i for i in raw_data.keys().tolist() if i != Y_LABEL]
N_INSTANCES = raw_data.shape[ 0 ]
N_INPUT = raw_data.shape[ 1 ] - 1
N_CLASSES = raw_data[ Y_LABEL ].unique().shape[ 0 ]
TEST_SIZE = 0.2
TRAIN_SIZE = int(N_INSTANCES * (1 - TEST_SIZE))
LEARNING_RATE = 0.001
TRAINING_EPOCHS = 200
BATCH_SIZE = 100
DISPLAY_STEP = 20


TEMP_HIDDEN_SIZE = range( 100, 500, 100 )
HIDDEN_SIZE = TEMP_HIDDEN_SIZE + sorted( TEMP_HIDDEN_SIZE, reverse = True)

ACTIVATION_FUNCTION_OUT = tf.nn.tanh
STDDEV = 0.1 # density function inizializzazione pesi
RANDOM_STATE = 1050  # Splitting


# ------------------------------------------------------------------------------
# Loading data
# randomizzazione
raw_data = raw_data.sample( frac = 1 )
data = raw_data[KEYS].get_values()  # X data
labels = raw_data[Y_LABEL].get_values()  # y data

# One hot encoding for labels
labels_ = np.zeros((N_INSTANCES, N_CLASSES))
labels_[np.arange(N_INSTANCES), labels] = 1

# Train-test split
data_train, data_test, labels_train, labels_test = train_test_split(data,
                                                                    labels_,
                                                                    test_size = TEST_SIZE,
                                                                    random_state = RANDOM_STATE)

# ------------------------------------------------------------------------------
# Neural net

# Parameters
n_input = N_INPUT  # input n labels
n_hidden_1 = HIDDEN_SIZE[ 0 ]
n_hidden_2 = HIDDEN_SIZE[ 1 ]
n_hidden_3 = HIDDEN_SIZE[ 2 ]
n_hidden_4 = HIDDEN_SIZE[ 3 ]
n_hidden_5 = HIDDEN_SIZE[ 4 ]
n_hidden_6 = HIDDEN_SIZE[ 5 ]
n_hidden_7 = HIDDEN_SIZE[ 6 ]
n_hidden_8 = HIDDEN_SIZE[ 7 ]
n_classes = N_CLASSES  # output m classes

# Tf placeholders
X = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
dropout_keep_prob = tf.placeholder(tf.float32)



def mlp(_X, _weights, _biases, dropout_keep_prob):
    layer1 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(_X, _weights['h1']), _biases['b1'])), dropout_keep_prob)
    layer2 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(layer1, _weights['h2']), _biases['b2'])), dropout_keep_prob)
    layer3 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(layer2, _weights['h3']), _biases['b3'])), dropout_keep_prob)
    layer4 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(layer3, _weights['h4']), _biases['b4'])), dropout_keep_prob)
    layer5 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(layer4, _weights['h5']), _biases['b5'])), dropout_keep_prob)
    layer6 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(layer5, _weights['h6']), _biases['b6'])), dropout_keep_prob)
    layer7 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(layer6, _weights['h7']), _biases['b7'])), dropout_keep_prob)
    layer8 = tf.nn.dropout(tf.nn.tanh(tf.add(tf.matmul(layer7, _weights['h8']), _biases['b8'])), dropout_keep_prob)
    out = ACTIVATION_FUNCTION_OUT(tf.add(tf.matmul(layer8, _weights['out']), _biases['out']))
    return out

weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1], stddev=STDDEV)),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2], stddev=STDDEV)),
    'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3], stddev=STDDEV)),
    'h4': tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4], stddev=STDDEV)),
    'h5': tf.Variable(tf.random_normal([n_hidden_4, n_hidden_5], stddev=STDDEV)),
    'h6': tf.Variable(tf.random_normal([n_hidden_5, n_hidden_6], stddev=STDDEV)),
    'h7': tf.Variable(tf.random_normal([n_hidden_6, n_hidden_7], stddev=STDDEV)),
    'h8': tf.Variable(tf.random_normal([n_hidden_7, n_hidden_8], stddev=STDDEV)),
    'out': tf.Variable(tf.random_normal([n_hidden_8, n_classes], stddev=STDDEV)),
}




biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'b3': tf.Variable(tf.random_normal([n_hidden_3])),
    'b4': tf.Variable(tf.random_normal([n_hidden_4])),
    'b5': tf.Variable(tf.random_normal([n_hidden_5])),
    'b6': tf.Variable(tf.random_normal([n_hidden_6])),
    'b7': tf.Variable(tf.random_normal([n_hidden_7])),
    'b8': tf.Variable(tf.random_normal([n_hidden_8])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Build model
pred = mlp(X, weights, biases, dropout_keep_prob)


# Loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = pred, labels = y))  # softmax loss
#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=yhat))

optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE).minimize(cost)

# Accuracy
correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


# ------------------------------------------------------------------------------
# Training

# Initializzazione
init_all = tf.initialize_all_variables()

# Launch session
sess = tf.Session()
sess.run(init_all)

# Training loop
for epoch in range(TRAINING_EPOCHS):
    avg_cost = 0.
    total_batch = int(data_train.shape[0] / BATCH_SIZE)
    for i in range(total_batch):
        randidx = np.random.randint(int(TRAIN_SIZE), size=BATCH_SIZE)
        batch_xs = data_train[randidx, :]
        batch_ys = labels_train[randidx, :]
        sess.run(optimizer, feed_dict={X: batch_xs, y: batch_ys, dropout_keep_prob: 0.9})
        avg_cost += sess.run(cost, feed_dict={X: batch_xs, y: batch_ys, dropout_keep_prob: 1.}) / total_batch
    # Display progress
    if epoch % DISPLAY_STEP == 0:
        print ("Epoch: %03d/%03d cost: %.9f" % (epoch, TRAINING_EPOCHS, avg_cost))
        train_acc = sess.run(accuracy, feed_dict={X: batch_xs, y: batch_ys, dropout_keep_prob: 1.})
        print ("Training accuracy: %.3f" % (train_acc))

------------------------------------------------
# Testing

test_acc = sess.run(accuracy, feed_dict={X: data_test, y: labels_test, dropout_keep_prob: 1.})
print ("Test accuracy: %.3f" % (test_acc))

sess.close()
print("Session closed!")