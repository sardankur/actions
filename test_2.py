import dataset
from sklearn.pipeline import Pipeline, FeatureUnion
from preprocess import PreProcess, Strip, RemoveQuestionMark
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB

def test_classify_Q():

    trainFile = "data/illinois/question_train1.txt"
    testFile = "data/illinois/question_test1.txt"

    # 1. detect questions from sentences
    #   a. Get get data

    #       - training data
    train = dataset.get_data(trainFile)
    trainData = dataset.extract_list(train, 3)
    trainTarget = dataset.extract_list(train, 0)

    #       - testing data
    test = dataset.get_data(testFile)
    testData = dataset.extract_list(test, 3)
    testTarget = dataset.extract_list(test, 0)

    #   b. Pre processing data before classification training
    # PreProcess.chain_transform([Strip()], trainData)
    # PreProcess.chain_transform([Strip()], testData)
    PreProcess.chain_transform([Strip(), RemoveQuestionMark()], trainData)
    PreProcess.chain_transform([Strip(), RemoveQuestionMark()], testData)

    #   c. Classification using feature extractions and a classifier
    transformers = [
        ('count', CountVectorizer(ngram_range=(1, 3)), 1)
        # , ('question_mark', features.QuestionMarkVectorizer(), 20)
    ]

    clf = Pipeline([
        ('feature_union', FeatureUnion(transformer_list=dataset.extract_list(transformers, [0, 1]),
                                       transformer_weights=dataset.extract_dict(transformers, 0, 2))),
        ('multinomial', MultinomialNB()
        # ('svm', SVC()
        # ('tree', tree.DecisionTreeClassifier()
         )
    ]).fit(trainData, trainTarget)

    # confusion matrix
    print(metrics.classification_report(testTarget, clf.predict(testData)))

def tests():
    test_classify_Q()

if __name__ == "__main__":
    tests()