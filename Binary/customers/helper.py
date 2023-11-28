import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from .models import Footprint, Profile, creditscore
from django.core.cache import cache
import time

def prepare_trained_set():
    regressor = cache.get('regressor')
    if not regressor:
        print("calcaulating reg")
        online_footprint_dataset = pd.read_csv(r"D:\UCI_Credit_Card.csv")
        y = online_footprint_dataset['default.payment.next.month'].values.tolist()
        x = online_footprint_dataset.drop(['LIMIT_BAL', 'ID', 'default.payment.next.month'], axis=1).values.tolist()
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=0)
        regressor = RandomForestRegressor(n_estimators=30, random_state=0)
        regressor.fit(X_train, y_train)
        cache.set('regressor', regressor, 86400)
    else:
        print("getting reg from cache")
    return regressor

def prepare_trained_set_for_creditLimit():
    model = cache.get('model')
    if not model:
        print("calcauting model")
        online_footprint_dataset = pd.read_csv(r"D:\UCI_Credit_Card1.csv")
        y = online_footprint_dataset['LIMIT_BAL'].values.tolist()
        x = online_footprint_dataset.drop(['LIMIT_BAL', 'ID', 'default.payment.next.month'], axis=1).values.tolist()
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=0)
        model = KNeighborsClassifier()
        model.fit(X_train, y_train)
        cache.set("model", model, 86400)
    else:
        print("getting model from cache")
    return model

def get_test_set(profile_detail):
    # prepare test_set dict from profile
    footprint = Footprint.objects.filter(profile=profile_detail)
    if footprint.exists():
        footprint = footprint[0]
        dicts = {
            'sex':profile_detail.sex,
            'age':profile_detail.age,
            'is_married': 1 if profile_detail.is_married else 0,
            'no_of_degree':profile_detail.No_of_Degrees,
            'pay_0': footprint.pay_0,
            'pay_1': footprint.pay_1,
            'pay_2': footprint.pay_2,
            'pay_3': footprint.pay_3,
            'pay_4': footprint.pay_4,
            'pay_5': footprint.pay_5,
            'bill_amt1': footprint.bill_amt1,
            'bill_amt2': footprint.bill_amt2,
            'bill_amt3': footprint.bill_amt3,
            'bill_amt4': footprint.bill_amt4,
            'bill_amt5': footprint.bill_amt5,
            'bill_amt6': footprint.bill_amt6,
            'pay_amt1': footprint.pay_amt1,
            'pay_amt2': footprint.pay_amt2,
            'pay_amt3': footprint.pay_amt3,
            'pay_amt4': footprint.pay_amt4,
            'pay_amt5': footprint.pay_amt5,
            'pay_amt6': footprint.pay_amt6,
        }
        return [list(dicts.values())]
    else:
        return None

def calculate_defaulter(regressor, test_set):
    result = regressor.predict(test_set)
    return False if result == 0 else True

def calculate_credit_limit(regressor, test_set):
    result = regressor.predict(test_set)
    return result


def calculate_defaulters_and_creditlimit():
    scores = creditscore.objects.filter(footprint_updated=True)
    if len(scores) > 0:
        defaulter_regressor = prepare_trained_set()
        creditlimit_regressior = prepare_trained_set_for_creditLimit()
    for score in scores:
        save_score_variable = False
        test_set = get_test_set(score.profile)
        if test_set != None:
            try:
                potential_defaulter = calculate_defaulter(defaulter_regressor, test_set)
                score.potential_defaulter = potential_defaulter
                print("dafault value: {}".format(potential_defaulter))
                save_score_variable = True
            except Exception as e:
                print("unable to process for user {} with error {}".format(score.profile.account_number,e))
            try:
                creditlimit = calculate_credit_limit(creditlimit_regressior, test_set)
                score.score = creditlimit
                print("credit limit : {}".format(creditlimit))
                score.footprint_updated =False
                save_score_variable = True
            except Exception as e:
                print("unable to process for user {} with error {}".format(score.profile.account_number, e))
            if save_score_variable:
                score.save()
