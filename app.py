from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# model = pickle.load(open('random_model.pkl', 'rb'))
model = joblib.load('random_model.sav')

standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = request.form.get('on_year', False)
        Present_Price = request.form.get('Present_Price', False)
        Kms_Driven = request.form.get('Kms_Driven', False)
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = request.form.get('Owner', False)
        Fuel_Type_Petrol = request.form.get('Fuel_Type', False)
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Year = 2020-Year
        Seller_Type_Individual = request.form.get(
            'Seller_Type', False)
        if(Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = request.form.get('Transmission', False)
        if(Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0

        df = pd.DataFrame([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]],
                          columns=['Present_Price', 'Kms_Driven', 'Owner', 'on_year', 'Fuel_Type', 'Seller_Type', 'Transmission'])
        # df = standard_to.transform(df)
        prediction = model.predict(df)
        output = round(prediction[0], 2)

        # prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel,
        #                            Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]]

    else:
        return jsonify({'Alert': 'You can not sell a car'})
    return jsonify({"Car Price": output})


if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 33507))
    app.run(debug=True)
