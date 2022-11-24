from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
import pandas as pd
#import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# Enable auto logging
#mlflow.set_tracking_uri('http://ml.mycompany.com/mlflow')
mlflow.sklearn.autolog()


# Prepare training data
df = pd.read_csv(r"C:\Users\loli\NewDVC\model-template\src\data\iris.csv")
X = df[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
flower_names = {'Setosa': 0, 'Versicolor': 1, 'Virginica': 2}
y = df['variety'].map(flower_names)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#train_data = lgb.Dataset(X_train, label=y_train)
clf=RandomForestClassifier()
def main():
  with mlflow.start_run() as run:
    # Train model
   
    clf=RandomForestClassifier(random_state=42)
    model = clf.fit(X_train,y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test,y_pred)
    flower_name_by_index = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}

    #Log params
   # for key in params.keys(): mlflow.log_param(key, params[key])
    # Log metrics
    mlflow.log_metrics({
      #"log_loss": loss, 
      "accuracy": acc
    })
    # MLFlow Model Registery
    mlflow.sklearn.log_model(model, "model",)

  print("Run ID:", run.info.run_id)
  for i in y_pred:
    print("flower:", flower_name_by_index[i])



    
if __name__ == "__main__":
    main()