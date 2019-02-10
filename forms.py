# pythonspot.com
import pandas as pd
import utils
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
output = 1
# App config.
DEBUG = True
input_columns = [u'Age', u'Fare', u'Pclass_2', u'Pclass_3', u'Sex_male', u'Embarked_C',
       u'Embarked_Q', u'Embarked_S', u'Parch_1', u'Parch_2', u'Parch_3',
       u'Parch_4', u'Parch_5', u'Parch_6', u'SibSp_1', u'SibSp_2', u'SibSp_3',
       u'SibSp_4', u'SibSp_5', u'SibSp_8']
blank = pd.DataFrame(columns = input_columns)

def preprocessing(data):
    data = pd.DataFrame(data, index = [0])
    data = utils.one_hot_encode(data, cols = ['Pclass', 'Sex', 'Embarked', 'Parch', 'SibSp'])
    data = data.align(blank, axis = 1, join="right", fill_value= 0)[0]
    return data

def predict(data):
    model = pickle.load(open("./model.sav", "rb"))
    output = model.predict(data)
    print output
    return output

app = Flask(__name__)
 
# class ReusableForm(Form):
#     name = TextField('Name:', validators=[validators.required()])
#     Ticket = TextField('Ticket:', validators=[validators.Length(min=6, max=35)])
#     Pclass = TextField('Pclass:', validators=[validators.required(), validators.Length(min=1, max=1), validators.NumberRange(min = 1, max = 3)])
#     Sex = TextField('Sex', validators = [validators.required(), validators.Length(min = 1, max = 1)])
#     Age = DecimalField('Age:', validators=[validators.required(), validators.Length(min=1, max=1), validators.NumberRange(min = 1, max = 3)])
 
 
@app.route("/")
def hello():

    return render_template('index.html')

@app.route("/predict", methods = ["GET", "POST"])
def fetch():
    print request
    print request.form
    if request.method == "POST":
        data = {
        "Age": float(request.form['Age']),
        "Pclass": request.form['Pclass'],
        "Fare": float(request.form['Fare']),
        "Sex": request.form['Sex'],
        "SibSp": request.form['SibSp'],
        "Parch": request.form['Parch'],
        "Embarked": request.form['Embarked']
        }
        data = preprocessing(data)
        output = predict(data)

        return render_template('predict.html', output = output[0])
    else:
        return render_template('predict.html')
 
if __name__ == "__main__":
    app.run(process.env.PORT, 3000)
