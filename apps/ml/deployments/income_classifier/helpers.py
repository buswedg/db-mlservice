import pandas as pd


class Helpers:
    values_fill_missing = None
    encoders = None
    model = None

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data.fillna(self.values_fill_missing)

        encode_cols = [
            'workclass',
            'education',
            'marital-status',
            'occupation',
            'relationship',
            'race',
            'sex',
            'native-country'
        ]

        for column in encode_cols:
            categorical_convert = self.encoders[column]
            input_data[column] = categorical_convert.transform(input_data[column])

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def process_prediction(self, input_data):
        label = "<=50K"
        if input_data[1] > 0.5:
            label = ">50K"

        pred_data = {
            'probability': input_data[1],
            'label': label,
            'status': 'OK'
        }

        return pred_data

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]  # one sample
            pred_data = self.process_prediction(prediction)
        except Exception as e:
            return {'status': 'Error', 'message': str(e)}

        return pred_data
