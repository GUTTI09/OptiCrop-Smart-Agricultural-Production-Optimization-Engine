import pandas as pd
import numpy as np
pd.set_option('max_colwidth',20)
pd.set_option('display.max_colwidth',None)
pd.set_option('display.max_colwidth',50)
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
plt.rcParams['figure.figsize'] = (12, 8)
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from ipywidgets import interact
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
data=pd.read_csv('Crop_recommendation.csv')
print(data.head())
features = [
    "N", "P", "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]
# Colors
colors = [
    "orange",
    "blue",
    "pink",
    "green",
    "royalblue",
    "red",
    "yellow"
]
# Draw distribution plots
for i, feature in enumerate(features):
    plt.subplot(2,4,i+1)
    sns.histplot(
        data[feature],
        kde=True,
        color=colors[i]
    )
    plt.title(f"Ratio of {feature.capitalize()}")
    plt.xlabel("")
    plt.ylabel("Density")
plt.suptitle(
    "Distribution of agricultural conditions",
    fontsize=18,
    fontweight="bold"
)
plt.tight_layout()
plt.show()
plt.subplot(2,4,7)
sns.scatterplot(x=data['humidity'],y=data['label'])
plt.show()
sns.countplot(data)
plt.show()
print(data.describe())
print(data.isnull().sum())
print(data.shape)
print(data.info())
plt.figure(figsize=(12, 8))
sns.boxplot(data)
plt.show()
Q1=data['P'].quantile(0.25)
Q3=data['P'].quantile(0.75)
IQR=Q3-Q1
filter=(data['P'] >= Q1 - 1.5 * IQR) & (data['P'] <= Q3 + 1.5 * IQR)
data=data.loc[filter]
print("Summer Crops")
print(data[(data['temperature'] > 30) & (data['humidity'] > 50)]['label'].unique())
print("--------------------------------------")
print("Winter Crops")
print(data[(data['temperature'] < 20) & (data['humidity'] > 30)]['label'].unique())
print("--------------------------------------")
print("Rainy Crops")
print(data[(data['rainfall'] > 200) & (data['humidity'] > 50)]['label'].unique())
print("--------------------------------------")
y=data['label']
x=data.drop(['label'],axis=1)
print("Shape of x:",x.shape)
print("Shape of x=y:",y.shape)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
print("The shape of x train:",x_train.shape)
print("The shape of x test:",x_test.shape)
print("The shape of y train:",x_train.shape)
print("The shape of y test:",x_test.shape)  
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 4)
wcss = []
for i in range(1, 11):
    km = KMeans(
        n_clusters=i,
        init='k-means++',
        max_iter=300,
        n_init=10,
        random_state=0
    )
    km.fit(x)
    wcss.append(km.inertia_)
plt.plot(range(1, 11), wcss)
plt.title("The Elbow Method", fontsize=20)
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.show()
km = KMeans(
    n_clusters=4,
    init='k-means++',
    max_iter=300,
    n_init=10,
    random_state=0
)
y_means = km.fit_predict(x)
a = data['label']
y_means = pd.DataFrame(y_means)
z = pd.concat([y_means, a], axis=1)
z = z.rename(columns={0: 'cluster'})
print("lets check the result after applying K-Means clustering analysis \n")
print("Crops in First cluster:",z[z['cluster'] == 0]['label'].unique())
print("______________________________________________________________________")
print("Crops in Second cluster:",z[z['cluster'] == 1]['label'].unique())
print("______________________________________________________________________")
print("Crops in Third cluster:",z[z['cluster'] == 2]['label'].unique())
print("______________________________________________________________________")
print("Crops in Fourth cluster:",z[z['cluster'] == 3]['label'].unique())
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
print(model)
from sklearn.metrics import classification_report
cr = classification_report(y_test, y_pred)
print(cr)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy Score :", accuracy)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix")
print(cm)
from sklearn.metrics import precision_score
precision = precision_score(
    y_test,
    y_pred,
    average='weighted'
)
print("Precision Score :", precision)
from sklearn.metrics import recall_score
recall = recall_score(
    y_test,
    y_pred,
    average='weighted'
)
print("Recall Score :", recall)
from sklearn.metrics import f1_score
f1 = f1_score(
    y_test,
    y_pred,
    average='weighted'
)
print("F1 Score :", f1)
from sklearn.metrics import roc_auc_score
y_prob = model.predict_proba(x_test)
roc_auc = roc_auc_score(
    y_test,
    y_prob,
    multi_class='ovr'
)
print("ROC-AUC Score :", roc_auc)
import pickle
pickle.dump(
    model,
    open("model.pkl", "wb")
)
print("Model Saved Successfully")
prediction = model.predict((np.array([[105,35,40,25,64,7,160]])))
print("The suggested crop for given climatic conditions is :", prediction)
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/findyourcrop")
def findyourcrop():
    return render_template("findyourcrop.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/predict", methods=["POST"])
def predict():
    values = [
        float(request.form["nitrogen"]),
        float(request.form["phosphorous"]),
        float(request.form["potassium"]),
        float(request.form["temperature"]),
        float(request.form["humidity"]),
        float(request.form["ph"]),
        float(request.form["rainfall"])
    ]

    prediction = model.predict([values])[0]

    return render_template("result.html", prediction=prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)