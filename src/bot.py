# load_and_use_model.py
import pickle

# Load the model
with open('my_bot.pkl', 'rb') as f:
    model = pickle.load(f)
    
sample = [[5.1, 3.5, 1.4, 0.2]]  
prediction = model.predict(sample)

print("Prediction:", prediction)
