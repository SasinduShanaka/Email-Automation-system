import pickle

with open("models/email_classifier.pkl", "rb") as f:
    model = pickle.load(f)

test_email = "I want to book a honeymoon tour in Sri Lanka"
prediction = model.predict([test_email])

print("Predicted category:", prediction[0])
