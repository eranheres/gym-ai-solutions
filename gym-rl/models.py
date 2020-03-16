from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model, load_model


class DenseModel:
    def build_model(self, observation_space, action_space, num_layers, units_per_layer):
        i = Input(shape=observation_space.shape)
        x = i
        for _ in range(num_layers):
            x = Dense(units=units_per_layer, activation='relu')(x)
        x = Dense(units=action_space.n)(x)
        model = Model(i, x)
        model.compile(loss='mse', optimizer='adam')
        model.summary()
        self._model = model

    def predict_batch(self, states):
        return self._model.predict(states)

    def train_batch(self, x_batch, y_batch):
        return self._model.train_on_batch(x_batch, y_batch)

    def save(self, filename):
        self._model.save(filename)

    def from_file(self, filename):
        self._model = load_model(filename)




