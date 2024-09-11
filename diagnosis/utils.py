import os
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array



model_path = './ai_weights'

# 안구 질환별 모델 파일 경로
eye_model_paths = {
    'e1': 'E1_CNN_model.keras',
    'e2': 'E2_CNN_model.keras',
    'e3': 'E3_CNN_model.keras',
    'e4': 'E4_CNN_model.keras',
    'e5': 'E5_CNN_model.keras',
    'e6': 'E6_CNN_model.keras',
    'e7': 'E7_CNN_model.keras',
    'e8': 'E8_CNN_model.keras',
    'e9': 'E9_CNN_model.keras',
    'e10': 'E10_CNN_model.keras'
}

# 피부 질환별 모델 파일 경로
skin_model_paths = {
    's1': 'A1_cnn_model.keras',
    's2': 'A2_cnn_model.keras',
    's3': 'A3_cnn_model.keras',
    's4': 'A4_cnn_model.keras',
    's5': 'A5_cnn_model.keras',
    's6': 'A6_cnn_model.keras'
}

# 모델 로드 (서버 시작 시 한 번만 로드)
eye_models = {disease: load_model(os.path.join(model_path, path)) for disease, path in eye_model_paths.items()}
skin_models = {disease: load_model(os.path.join(model_path, path)) for disease, path in skin_model_paths.items()}

def preprocess_image(image_path, target_size):
    """이미지를 Keras 모델에 맞게 전처리하는 함수"""
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # 이미지 정규화
    return img_array

def predict_eye_diseases(image_path):
    """안구 질환 예측을 수행하는 함수"""
    results = {}
    target_size = (224, 224)
    img_array = preprocess_image(image_path, target_size)

    # 각 안구 질환에 대한 확률 계산
    probabilities = []
    for disease, model in eye_models.items():
        prediction = model.predict(img_array)
        probability = prediction[0][0]  # 이진 분류의 경우
        probabilities.append(probability)
        results[disease] = probability

    # 확률 정규화
    total_probability = sum(probabilities)
    normalized_results = {disease: (prob / total_probability) * 100 for disease, prob in results.items()}

    return normalized_results

def predict_skin_diseases(image_path):
    """피부 질환 예측을 수행하는 함수"""
    results = {}
    target_size = (224, 224)
    img_array = preprocess_image(image_path, target_size)

    # 각 피부 질환에 대한 확률 계산
    probabilities = []
    for disease, model in skin_models.items():
        prediction = model.predict(img_array)
        probability = prediction[0][0]  # 이진 분류의 경우
        probabilities.append(probability)
        results[disease] = probability

    # 확률 정규화
    total_probability = sum(probabilities)
    normalized_results = {disease: (prob / total_probability) * 100 for disease, prob in results.items()}

    return normalized_results

def run_diagnosis(image_path, diagnosis_part):
    """진단 부위에 따라 적절한 예측 함수를 호출하는 메인 함수"""
    if diagnosis_part == 'eye':
        return predict_eye_diseases(image_path)
    elif diagnosis_part == 'skin':
        return predict_skin_diseases(image_path)
    else:
        raise ValueError("Invalid diagnosis part. Choose 'eye' or 'skin'.")
