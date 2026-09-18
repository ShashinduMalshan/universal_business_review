import pytest
from backend.app.services.inference_service import InferenceService

def test_inference_all_20_benchmark_samples():
    reviews = [
        # Bad Reviews
        ("The food was disappointing, and the service was very slow. The staff were not friendly, and the overall experience was not worth the price.", "Negative"),
        ("I expected better food quality, but the meal was average. The restaurant needs to improve its service and cleanliness.", "Negative"),
        ("The food was not fresh, and we had to wait a long time. I hope the restaurant improves its customer service.", "Negative"),
        ("Unfortunately, my experience was not good. The food lacked flavor, and the staff were not very helpful.", "Negative"),
        ("The restaurant was overcrowded, and the service was slow. The food was okay, but the overall experience could be much better.", "Negative"),
        ("The food was cold when it arrived. The staff did not respond quickly to our concerns. There is room for improvement.", "Negative"),
        ("The prices were high compared to the food quality. The restaurant should focus on improving both taste and service.", "Negative"),
        
        # Neutral Reviews
        ("The food was decent, and the service was acceptable. Nothing was particularly special, but it was an okay place for a casual meal.", "Neutral"),
        ("The restaurant offers average food and a comfortable atmosphere. The service could be faster, but overall, it was a reasonable experience.", "Neutral"),
        ("My experience was neither good nor bad. Some dishes were tasty, while others were average. The restaurant has potential to improve.", "Neutral"),
        ("The food was satisfactory, and the staff were polite. However, the waiting time was longer than expected.", "Neutral"),
        ("The restaurant has a nice atmosphere and reasonable food quality. The service was average, and there is room for improvement.", "Neutral"),
        ("The experience was okay. The food was acceptable, but the presentation and service could be improved.", "Neutral"),
        
        # Positive Reviews
        ("I had a wonderful experience at this restaurant. The food was delicious, the staff were friendly, and the atmosphere was very welcoming.", "Positive"),
        ("The food was fresh and tasty. The service was excellent, and the staff were very helpful. I would definitely visit again.", "Positive"),
        ("A great place to enjoy a delicious meal. The restaurant was clean, the staff were polite, and the overall experience was excellent.", "Positive"),
        ("I really enjoyed my visit. The food was well prepared, the service was quick, and the atmosphere was comfortable.", "Positive"),
        ("The restaurant offers delicious food at a reasonable price. The staff were friendly and professional. I highly recommend visiting this place.", "Positive"),
        ("Excellent food and wonderful service. Everything was well organized, and the staff made us feel welcome. I look forward to coming back.", "Positive"),
        ("I had a pleasant dining experience. The food was tasty, the restaurant was clean, and the service was impressive. Highly recommended.", "Positive")
    ]
    
    passed = 0
    for text, expected in reviews:
        res = InferenceService.analyze_single_review(text, persist=False)
        assert res.sentiment == expected, f"Failed for text: {text} | Got {res.sentiment}, Expected {expected}"
        passed += 1
        
    assert passed == 20
