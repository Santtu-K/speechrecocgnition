import joblib

joblib.dump(model, 'model.pkl')

# Testi
loaded_model = joblib.load('model.pkl')
demo_y_pred = loaded_model.predict(X_test)
demo_accuracy = accuracy_score(y_test, demo_y_pred)
