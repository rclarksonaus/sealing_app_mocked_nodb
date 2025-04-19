from app import schemas

def score_recommendation(input_data: schemas.InputData, db=None):
    grades = [
        {
            "id": 1,
            "name": "Kalrez 6375",
            "temp_min": -20,
            "temp_max": 230,
            "pressure_min": 0,
            "pressure_max": 20,
            "usage_score": 0.9,
            "recommended_by": "DuPont",
            "media_resistance": [{"media_type": "acid", "rating": "A", "confidence": "High"}],
            "form_fits": ["narrow"],
            "movement_supported": ["rotary"]
        },
        {
            "id": 2,
            "name": "Viton A",
            "temp_min": -10,
            "temp_max": 200,
            "pressure_min": 0,
            "pressure_max": 15,
            "usage_score": 0.75,
            "recommended_by": "Solvay",
            "media_resistance": [{"media_type": "oil", "rating": "B", "confidence": "Medium"}],
            "form_fits": ["standard"],
            "movement_supported": ["linear"]
        }
    ]

    rating_score = {"A": 0.25, "B": 0.15, "C": 0.05, "D": 0.0}
    confidence_penalty = {"Low": -0.05, "Medium": 0.0, "High": 0.0}

    results = []

    for grade in grades:
        score = 0
        reasons = []

        if grade["temp_min"] <= input_data.temp_c <= grade["temp_max"]:
            ratio = (input_data.temp_c - grade["temp_min"]) / (grade["temp_max"] - grade["temp_min"])
            score += 0.25 if ratio < 0.8 else 0.15
            reasons.append("温度适配裕度好" if ratio < 0.8 else "温度适配边缘")

        if grade["pressure_min"] <= input_data.pressure_bar <= grade["pressure_max"]:
            pratio = (input_data.pressure_bar - grade["pressure_min"]) / (grade["pressure_max"] - grade["pressure_min"])
            score += 0.2 if pratio < 0.7 else 0.1
            reasons.append("压力裕度充足" if pratio < 0.7 else "压力接近极限")

        for res in grade["media_resistance"]:
            if res["media_type"] == input_data.media_type:
                score += rating_score.get(res["rating"], 0)
                score += confidence_penalty.get(res["confidence"], 0)
                reasons.append(f"介质评级: {res['rating']}, 可信度: {res['confidence']}")
                break

        if input_data.space_constraint in grade["form_fits"]:
            score += 0.1
            reasons.append("结构空间适配")

        if input_data.movement_type in grade["movement_supported"]:
            score += 0.1
            reasons.append("运动支持")

        score += grade["usage_score"] or 0.0
        if grade["recommended_by"]:
            reasons.append("有推荐历史")

        results.append({
            "grade_id": grade["id"],
            "score": round(score, 3),
            "reason": ", ".join(reasons)
        })

    return {"results": sorted(results, key=lambda x: x['score'], reverse=True)}
