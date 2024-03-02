from imageai.Classification.Custom import CustomImageClassification

import os

execution_path = os.getcwd()

prediction = CustomImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath(os.path.join(execution_path, "resnet50-idenprof-test_acc_0.78200_epoch-91.pt"))
prediction.setJsonPath(os.path.join(execution_path, "idenprof_model_class.json"))
prediction.loadModel(num_objects=10)

predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, "cat.jpg"), result_count=5)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction + " : " + eachProbability)