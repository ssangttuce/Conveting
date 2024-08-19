import os
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array



model_path = './ai_weights'

# 안구 질환별 모델 파일 경로
eye_model_paths = {
    '결막염': 'E0_resnet_model.keras',
    '궤양성 각막질환': 'E1_resnet_model.keras',
    '백내장': 'E2_resnet_model.keras',
    '비궤양성 각막질환': 'E3_resnet_model.keras',
    '색소침착성각막염': 'E4_resnet_model.keras',
    '안검 내반증': 'E5_resnet_model.keras',
    '안검종양': 'E7_resnet_model.keras',
    '유루증': 'E8_resnet_model.keras'
}

# 피부 질환별 모델 파일 경로
skin_model_paths = {
    '구진, 플라크': 'A1_cnn_model.keras',
    '비듬, 각질, 상피성잔고리': 'A2_cnn_model.keras',
    '태선화, 과다색소침착': 'A3_cnn_model.keras',
    '농포, 여드름': 'A4_cnn_model.keras',
    '미란, 궤양': 'A5_cnn_model.keras',
    '결절, 종괴': 'A6_cnn_model.keras'
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
