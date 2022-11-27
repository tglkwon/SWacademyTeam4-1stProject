import tensorflow as tf

import numpy as np
import os
import time

from hp_MyModel import MyModel
from hp_OneStep import OneStep

path_to_file = './data/harrypotter/FullBook.txt'

# Read, then decode for py2 compat.
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

# length of text is the number of characters in it
print(f'Length of text: {len(text)} characters')

# The unique characters in the file
vocab = sorted(set(text))
print(f'{len(vocab)} unique characters')

ids_from_chars = tf.keras.layers.StringLookup(
    vocabulary=list(vocab), mask_token=None)

chars_from_ids = tf.keras.layers.StringLookup(
    vocabulary=ids_from_chars.get_vocabulary(), invert=True, mask_token=None)

def text_from_ids(ids):
  return tf.strings.reduce_join(chars_from_ids(ids), axis=-1)

all_ids = ids_from_chars(tf.strings.unicode_split(text, 'UTF-8'))
ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

seq_length = 100
sequences = ids_dataset.batch(seq_length+1, drop_remainder=True)

# for seq in sequences.take(1):
#   print(chars_from_ids(seq))

# for seq in sequences.take(5):
#   print(text_from_ids(seq).numpy())

def split_input_target(sequence):
    input_text = sequence[:-1]
    target_text = sequence[1:]
    return input_text, target_text

dataset = sequences.map(split_input_target)

for input_example, target_example in dataset.take(1):
    print("Input :", text_from_ids(input_example).numpy())
    print("Target:", text_from_ids(target_example).numpy())

# Batch size
BATCH_SIZE = 64

# Buffer size to shuffle the dataset
# (TF data is designed to work with possibly infinite sequences,
# so it doesn't attempt to shuffle the entire sequence in memory. Instead,
# it maintains a buffer in which it shuffles elements).
BUFFER_SIZE = 10000
### 데이터셋을 셔플한다는 게 무슨 뜻인지 잘 모르겠음
### 연속된 텍스트 데이터인데 어떻게 셔플한다는 뜻인지?
### 캐릭터 단위로 잘라놓지 않았나?

dataset = (
    dataset
    .shuffle(BUFFER_SIZE)
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE))


# Length of the vocabulary in StringLookup Layer
vocab_size = len(ids_from_chars.get_vocabulary())
### StringLookup Layer란?

# The embedding dimension
embedding_dim = 256
### 임베딩 차원?

# Number of RNN units
rnn_units = 1024
### 퍼셉트론 개수와 같은 건가?


model = MyModel(
    vocab_size=vocab_size,
    embedding_dim=embedding_dim,
    rnn_units=rnn_units)
    

for input_example_batch, target_example_batch in dataset.take(1):
    example_batch_predictions = model(input_example_batch)
    print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")

model.summary()

sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
sampled_indices = tf.squeeze(sampled_indices, axis=-1).numpy()
### categorical과 squeeze를 쓰는 이유는?

print("Input:\n", text_from_ids(input_example_batch[0]).numpy())
print("Next Char Predictions:\n", text_from_ids(sampled_indices).numpy())

loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True)
### 다른 에러를 써보고 싶은데 파라미터 조정을 어떻게 해야 하는지 잘 모르겠다.
### from_logits 파라미터는 뭐하는 친구

example_batch_mean_loss = loss(target_example_batch, example_batch_predictions)
print("Prediction shape: ", example_batch_predictions.shape, " # (batch_size, sequence_length, vocab_size)")
print("Mean loss:        ", example_batch_mean_loss)

# tf.exp(example_batch_mean_loss).numpy()
### exp를 사용하는 이유는?

model.compile(optimizer='adam', loss=loss)


# ------------------------------------------------------------------------
# Directory where the checkpoints will be saved
checkpoint_dir = './training_checkpoints_hp'
# Name of the checkpoint files
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True)

# 저장된 ckpt 읽어서 이어서 학습하기
latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)

# history = model.fit(dataset, epochs=1, callbacks=[checkpoint_callback])

# ------------------------------------------------------------------------

one_step_model = OneStep(model, chars_from_ids, ids_from_chars)

start = time.time()
states = None
next_char = tf.constant(['Harry,'])
result = [next_char]

for n in range(1000):
  next_char, states = one_step_model.generate_one_step(next_char, states=states)
  result.append(next_char)

result = tf.strings.join(result)
end = time.time()
print(result[0].numpy().decode('utf-8'), '\n\n' + '_'*80)
print('\nRun time:', end - start)

# tf.saved_model.save(one_step_model, 'one_step')
# one_step_reloaded = tf.saved_model.load('one_step')

# states = None
# next_char = tf.constant(['ROMEO:'])
# result = [next_char]

# for n in range(100):
#   next_char, states = one_step_reloaded.generate_one_step(next_char, states=states)
#   result.append(next_char)

# print(tf.strings.join(result)[0].numpy().decode("utf-8"))