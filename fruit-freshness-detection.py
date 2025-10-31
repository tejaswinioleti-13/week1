# fruit_freshness_detection.py
# CNN model setup - dataset not trained yet

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Create a Sequential model
model = Sequential()

# Add convolutional + pooling layers
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

# Add fully connected layers
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))  # To reduce overfitting
model.add(Dense(3, activation='softmax'))  # 3 output classes: Fresh, Rotten, Overripe

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Display the model structure
model.summary()

print("\n✅ CNN model created successfully!")
print("⚠ Dataset not loaded or trained yet. Please extract and prepare dataset folders before training.")