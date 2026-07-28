import math
from typing import Dict, Any, Optional

class MedicalCalculators:
    """Implementations of standard clinical formulas."""
    
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
        """Calculates Body Mass Index."""
        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m ** 2)
        category = "Normal"
        if bmi < 18.5: category = "Underweight"
        elif bmi >= 25 and bmi < 30: category = "Overweight"
        elif bmi >= 30: category = "Obese"
        return {"bmi": round(bmi, 2), "category": category}

    @staticmethod
    def calculate_bsa(weight_kg: float, height_cm: float) -> Dict[str, Any]:
        """Calculates Body Surface Area using Du Bois formula."""
        bsa = 0.007184 * (weight_kg ** 0.425) * (height_cm ** 0.725)
        return {"bsa_m2": round(bsa, 3)}

    @staticmethod
    def calculate_egfr(serum_creatinine_mg_dl: float, age: int, is_female: bool, is_black: bool) -> Dict[str, Any]:
        """Calculates eGFR using MDRD equation."""
        egfr = 175 * (serum_creatinine_mg_dl ** -1.154) * (age ** -0.203)
        if is_female: egfr *= 0.742
        if is_black: egfr *= 1.212
        return {"egfr": round(egfr, 2)}

    @staticmethod
    def calculate_curb65(confusion: bool, urea_mg_dl: float, rr: int, sbp: int, dbp: int, age: int) -> Dict[str, Any]:
        """Calculates CURB-65 score for pneumonia severity."""
        score = 0
        if confusion: score += 1
        if urea_mg_dl > 19.6: score += 1
        if rr >= 30: score += 1
        if sbp < 90 or dbp <= 60: score += 1
        if age >= 65: score += 1
        
        risk = "Low"
        if score == 2: risk = "Moderate"
        elif score >= 3: risk = "High"
        
        return {"score": score, "risk": risk}

    @staticmethod
    def calculate_news2(rr: int, spo2: int, air_or_o2: str, sbp: int, hr: int, consciousness: str, temp: float) -> Dict[str, Any]:
        """Calculates National Early Warning Score 2 (Simplified)."""
        score = 0
        # This is a highly simplified mock for demonstration
        if rr <= 8 or rr >= 25: score += 3
        if spo2 <= 91: score += 3
        if air_or_o2.lower() == "o2": score += 2
        if sbp <= 90 or sbp >= 220: score += 3
        if hr <= 40 or hr >= 131: score += 3
        if consciousness.lower() != "alert": score += 3
        if temp <= 35.0 or temp >= 39.1: score += 3
        
        risk = "Low"
        if score >= 5: risk = "Medium"
        if score >= 7: risk = "High"
        
        return {"score": score, "risk": risk}
        
calculators = MedicalCalculators()
