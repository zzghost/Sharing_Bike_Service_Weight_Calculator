import csv
import time
import json
import numpy as np
import lightgbm as lgb
import pandas as pd
from sklearn.metrics import mean_squared_error


#train_file = "data/google.train"
#test_file = "data/google.test"
train_file = "data/train.3.csv"
test_file = "/home/caoxingchao/ffz_nlp/ccir_2018/ranking/data/NYC_taxi/test_14w.csv"

df_train = pd.read_csv(train_file, header=None, sep='\t')
df_test = pd.read_csv(test_file, header=None, sep='\t')

y_train = df_train[0].values
y_test = df_test[0].values
X_train = df_train.drop(0, axis=1).values
X_test = df_test.drop(0, axis=1).values

num_train, num_feature = X_train.shape

lgb_train = lgb.Dataset(X_train, y_train, free_raw_data=False)
lgb_eval = lgb.Dataset(X_test, y_test, free_raw_data=False)


def rmsle(preds, y_data):
    y_data = np.array(y_data.get_label())
    return 'error', np.sqrt(np.mean((np.log(1 + preds) - np.log(1 + y_data)) ** 2)), False


params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'l2',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

feature_name = ['feature_' + str(col) for col in range(num_feature)]

print("Start training...")

gbm = lgb.train(params, lgb_train, num_boost_round=100, feval=rmsle, valid_sets=lgb_eval, feature_name=feature_name, categorical_feature=[0, 1, 2, 4, 5, 11], early_stopping_rounds=10)


# Save model to file
print("Saving model...")
gbm.save_model("models/model.txt", num_iteration=gbm.best_iteration)

# dump model to JSON
# model_json = gbm.dump_model()

# with open("models/model.json", 'w+') as f:
#     json.dump(model_json, f, indent=4)

print("Fearure names: ", gbm.feature_name())

print("feature importances: ", list(gbm.feature_importance()))

#print("Load model...")
#gbm = lgb.Booster(model_file='models/model.txt')
# predict
y_pred = gbm.predict(X_test)
# eval
#print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)
print('The rmsle of prediction is:', np.sqrt(np.mean((np.log(1 + y_test) - np.log(1 + y_pred)) ** 2)))

timestamp = int(time.time())
print(timestamp)
with open('results/train_{}.res'.format(timestamp), 'w') as f:
    for res in y_pred:
        f.write('{}'.format(res) + '\n')
print("over")

