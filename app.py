from flask import *
import os
import pygal
from werkzeug.utils import secure_filename
from sklearn.metrics import accuracy_score, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
le=preprocessing.LabelEncoder()
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
from sklearn import metrics


app=Flask(__name__)
app.config['SECRET_KEY']='hAcKeR Code'
app.config['upload']='uploadedfile\\foreveralone.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method=='POST':
        name=request.form['admin']
        pwd=request.form['pwd']
        if name=='admin' and pwd=="pwd":
            return render_template('load.html',msg="Admin Log in Successful")
        else:
            return render_template('login.html',msg="Invalid Credentials")
    return render_template('login.html')

@app.route('/loaddataset', methods=['GET', 'POST'])
def loaddataset():
    if request.method == "POST":
        print('1111')
        files = request.files['uploadfile']
        print(files)
        filetype = os.path.splitext(files.filename)[1]
        print(filetype)
        
        # Define the directory for saving uploaded files
        upload_folder = os.path.join(os.getcwd(), 'uploadedfile')
        
        # Create the directory if it doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Define the full path where the file will be saved
        path = os.path.join(upload_folder, secure_filename(files.filename))
        print(path)
        
        # Save the file
        files.save(path)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(path)
        data = df
        print(data.columns)
        print(data['race'].value_counts())
        print('-------------------')
        print(data['sexuallity'].value_counts())
        print(data['income'].value_counts())
        msg = "Dataset uploaded successfully"
        return render_template('process.html', msg=msg, cols=df.columns.values, data=data.values.tolist())
    return render_template('load.html')

@app.route('/preprocessing')
def preprocessing():
    global df
    print('JJJJJJJJJJJJJJJJJJJJJ')
    
    # Use the directory path, not the file path
    upload_dir = os.path.join(os.getcwd(), 'uploadedfile')
    
    # Ensure that the directory exists
    if not os.path.exists(upload_dir):
        print("Error: The upload directory does not exist.")
        return render_template('error.html', msg="Upload directory not found.")
    
    # Get the list of files in the directory
    file_list = os.listdir(upload_dir)
    print(file_list)
    
    if not file_list:
        return render_template('error.html', msg="No files found in the upload directory.")
    
    # Get the path of the uploaded file (assuming it's the first file in the directory)
    file_path = os.path.join(upload_dir, file_list[0])
    print(f"Processing file: {file_path}")
    
    # Now load the file
    try:
        df = pd.read_csv(file_path)
        print("File loaded successfully!")
        
        # Perform preprocessing (dropping columns, label encoding, etc.)
        df.drop(['time', 'prostitution_legal', 'pay_for_sex', 'what_help_from_others', 'employment', 'job_title', 'edu_level', 'improve_yourself_how'], axis=1, inplace=True)
        print('Preprocessing...')
        
        # Apply Label Encoding
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        for column in ['gender', 'sexuallity', 'income', 'race', 'bodyweight', 'virgin', 'social_fear', 'depressed', 'attempt_suicide']:
            df[column] = le.fit_transform(df[column])
        
        # Print some stats
        print("Columns and values after preprocessing:")
        print(df.head())
        
        # Continue with your logic
        msg = "Data Preprocessing Completed Successfully"
        return render_template('processing.html', msg=msg, cols=df.columns.values, data=df.values.tolist())
    
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return render_template('error.html', msg="Error occurred during file processing.")



@app.route('/modeltraining',methods=['GET','POST'])
def modeltraining():
    global x_train,y_train,x_test,y_test
    x = df.drop(['attempt_suicide'], axis=1)
    y = df['attempt_suicide']
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)
    
    if request.method=='POST':
        algo = request.form['algo']

        if algo == "logistic_regression":
            model = LogisticRegression()

        elif algo == "decision_tree":
            model = DecisionTreeClassifier(random_state=42)

        elif algo == "random_forest":
            model = RandomForestClassifier(n_estimators=100, random_state=42)

        elif algo == "adaboost":
            model = AdaBoostClassifier(n_estimators=50, random_state=42)

        elif algo == "gradient_boost":
            model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        elif algo == "gnb":
            model = GaussianNB()
        model.fit(x_train, y_train)
        model_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, model_pred)
        # Generating classification report
        class_report = classification_report(y_test, model_pred, output_dict=True)
        # Rendering the result
        return render_template("model.html", algo=algo, accuracy=accuracy, class_report=class_report)
    return render_template("model.html")



@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        print('hello')
        gender = request.form['Gender']
        sexuality = request.form['sexuallity']
        age = int(request.form['age'])
        income = request.form['income']
        race = request.form['race']
        weight = request.form['weight']
        virgin = request.form['virgin']
        friends = int(request.form['friends'])
        fear = request.form['fear']
        depression = request.form['depression']
        print(income)
        print(type(income))
        print('=================')
        print('-----------------')

        # Align input data with the training columns
        x = {
            'gender': gender,
            'sexuallity': sexuality,
            'age': age,
            'income': income,
            'race': race,
            'bodyweight': weight,  # Rename 'weight' to 'bodyweight'
            'virgin': virgin,
            'friends': friends,
            'social_fear': fear,  # Rename 'fear' to 'social_fear'
            'depressed': depression  # Rename 'depression' to 'depressed'
        }

        data = pd.DataFrame([x])  # Convert to DataFrame

        # Apply the same preprocessing used during model training (e.g., Label Encoding)
        data['gender'] = data['gender'].replace({'Male': 0, 'Female': 1})  # Replace gender with numeric values
        data['income'] = data['income'].replace({'0': 0, '1 to 10,000': 1, '10,000 to 19,999': 2, 
                                                  '20,000 to 29,999': 3, '30,000 to 39,999': 4, 
                                                  '50,000 to 74,999': 5, '40,000 to 49,999': 6, 
                                                  '75,000 to 99,999': 7, '125,000 to 149,999': 8, 
                                                  '100,000 to 124,999': 9, '150,000 to 174,999': 10, 
                                                  '200,000 or more': 11, '174,999 to 199,999': 12})
        data['sexuallity'] = data['sexuallity'].replace({'Straight': 0, 'Bisexual': 1, 'Gay/Lesbian': 2})
        data['race'] = data['race'].replace({'White non-Hispanic': 0, 'Asian': 1, 'Hispanic (of any race)': 2, 
                                             'Black': 3, 'Mixed': 4, 'Middle Eastern': 5, 'Indian': 6, 
                                             'caucasian': 7, 'Mixed race': 8, 'Pakistani': 9, 'mixed': 10, 
                                             'Turkish': 11, 'Half Asian half white': 12, 'white and asian': 13, 
                                             'North African': 14, 'Native American mix': 15, 'European': 16, 
                                             'First two answers. Gender is androgyne, not male; sexuality is asexual, not bi.': 17, 
                                             'White and Native American': 18, 'Multi': 19, 'Mixed white/asian': 20, 
                                             'Native american': 21, 'helicopterkin': 22, 'half Arab': 23})
        data['bodyweight'] = data['bodyweight'].replace({'Normal weight': 0, 'Overweight': 1, 'Underweight': 2, 'Obese': 3})
        data['virgin'] = data['virgin'].replace({'Yes': 1, 'No': 0})
        data['social_fear'] = data['social_fear'].replace({'Yes': 1, 'No': 0})
        data['depressed'] = data['depressed'].replace({'Yes': 1, 'No': 0})

        # Check data before prediction
        print(data)
        print('---------------------------')

        # Fit the model
        lr = LogisticRegression()
        lr.fit(x_train, y_train)  # Make sure x_train, y_train are defined and preprocessed

        # Predict using the trained model
        lr_pred = lr.predict(data)

        print(lr_pred)
        
        # Based on gender and prediction, form the message
        if gender == 'Female':  # If the gender is female
            if lr_pred == [0]:
                msg = "She will not commit suicide"
            else:
                msg = "She will commit suicide"
        elif gender == 'Male':  # If the gender is male
            if lr_pred == [0]:
                msg = "He will not commit suicide"
            else:
                msg = "He will commit suicide"
        else:
            msg = "Invalid gender input"

        return render_template('ROC.html', msg=msg)

    return render_template('index1.html')







@app.route('/exit')
def exit():
    return redirect(url_for('index'))
# try:
#   models = int(input("Please enter your selection"))
#   while models < 4:
#     option = int(input("Please enter your selection"))
# except ValueError:
#   print("Error!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
