import numpy as np
import pandas as pd
import joblib
from scipy.optimize import minimize
from app.config import (
    CHOKE_MIN, CHOKE_MAX, PENALTY_WEIGHT, 
    OPTIMIZATION_METHOD, MODEL_PATHS, FEATURE_NAMES
)
import os

# ============================================
# LOAD MODELS (Global - loaded once)
# ============================================
def load_models():
    """Load XGBoost models for oil and water prediction"""
    try:
        model_oil = joblib.load(MODEL_PATHS['oil'])
        model_water = joblib.load(MODEL_PATHS['water'])
        print("✅ Models loaded successfully")
        return model_oil, model_water
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return None, None

# Initialize models
MODEL_OIL = None
MODEL_WATER = None

def initialize_models():
    """Initialize global model variables"""
    global MODEL_OIL, MODEL_WATER
    MODEL_OIL, MODEL_WATER = load_models()

# ============================================
# PREDICTION FUNCTIONS
# ============================================
def validate_input(input_dict):
    """
    Validate user input against bounds
    Returns: (is_valid, error_message)
    """
    from app.config import FEATURE_BOUNDS
    
    errors = []
    
    for feature in FEATURE_NAMES:
        if feature not in input_dict:
            errors.append(f"Missing feature: {feature}")
            continue
        
        try:
            value = float(input_dict[feature])
        except (ValueError, TypeError):
            errors.append(f"Invalid value for {feature}: must be numeric")
            continue
        
        min_val, max_val = FEATURE_BOUNDS[feature]
        if not (min_val <= value <= max_val):
            errors.append(
                f"{feature} out of bounds. Expected {min_val}-{max_val}, got {value}"
            )
    
    if errors:
        return False, errors
    
    return True, None


def predict_production(input_features):
    """
    Predict oil and water production given input features
    
    Args:
        input_features: dict or list of 8 features
    
    Returns:
        dict with 'oil' and 'water' predictions (guaranteed ≥ 0)
    """
    if MODEL_OIL is None or MODEL_WATER is None:
        return None, "Models not loaded"
    
    try:
        # Convert to array if dict
        if isinstance(input_features, dict):
            input_array = np.array([input_features[f] for f in FEATURE_NAMES]).reshape(1, -1)
        else:
            input_array = np.array(input_features).reshape(1, -1)
        
        oil_pred = MODEL_OIL.predict(input_array)[0]
        water_pred = MODEL_WATER.predict(input_array)[0]
        
        # Ensure non-negative predictions (models might predict negative)
        oil_pred = max(0, float(oil_pred))
        water_pred = max(0, float(water_pred))
        
        return {
            'oil': oil_pred,
            'water': water_pred
        }, None
    
    except Exception as e:
        return None, f"Prediction error: {str(e)}"


def optimize_choke(input_features):
    """
    Find optimal choke size using multi-objective optimization
    
    Objective: Maximize (Oil - Penalty * Water)
    With constraint: Oil >= 0, Water >= 0
    
    Args:
        input_features: dict with 8 features
    
    Returns:
        dict with optimization results
    """
    if MODEL_OIL is None or MODEL_WATER is None:
        return None, "Models not loaded"
    
    try:
        # Current choke value as initial guess
        choke_actual = input_features.get('AVG Choke size', 0.45)
        x0 = [max(CHOKE_MIN, min(choke_actual, CHOKE_MAX))]
        
        # Define objective function for optimization
        def objective_function(choke_array):
            choke_value = choke_array[0]
            
            # Create simulation condition with new choke
            condition = input_features.copy()
            condition['AVG Choke size'] = choke_value
            
            # Predict with new choke
            input_array = np.array([condition[f] for f in FEATURE_NAMES]).reshape(1, -1)
            pred_oil = MODEL_OIL.predict(input_array)[0]
            pred_water = MODEL_WATER.predict(input_array)[0]
            
            # Ensure non-negative values (models might predict negative)
            pred_oil = max(0, pred_oil)
            pred_water = max(0, pred_water)
            
            # Multi-objective score: maximize oil, minimize water (with penalty)
            score = pred_oil - (PENALTY_WEIGHT * pred_water)
            
            # Return negative because scipy minimizes
            return -score
        
        # Optimize
        bounds = [(CHOKE_MIN, CHOKE_MAX)]
        result = minimize(
            fun=objective_function,
            x0=x0,
            method=OPTIMIZATION_METHOD,
            bounds=bounds
        )
        
        if not result.success:
            return None, f"Optimization failed: {result.message}"
        
        # Get optimal choke value
        choke_optimal = float(result.x[0])
        
        # Predict with optimal choke
        condition_opt = input_features.copy()
        condition_opt['AVG Choke size'] = choke_optimal
        input_array = np.array([condition_opt[f] for f in FEATURE_NAMES]).reshape(1, -1)
        oil_opt = max(0, float(MODEL_OIL.predict(input_array)[0]))
        water_opt = max(0, float(MODEL_WATER.predict(input_array)[0]))
        
        # Predict with actual choke
        condition_actual = input_features.copy()
        condition_actual['AVG Choke size'] = choke_actual
        input_array = np.array([condition_actual[f] for f in FEATURE_NAMES]).reshape(1, -1)
        oil_actual = max(0, float(MODEL_OIL.predict(input_array)[0]))
        water_actual = max(0, float(MODEL_WATER.predict(input_array)[0]))
        
        return {
            'choke_optimal': choke_optimal,
            'oil_actual': oil_actual,
            'oil_optimal': oil_opt,
            'oil_gain': oil_opt - oil_actual,
            'water_actual': water_actual,
            'water_optimal': water_opt,
            'water_reduction': water_actual - water_opt
        }, None
    
    except Exception as e:
        return None, f"Optimization error: {str(e)}"


def process_excel_file(filepath):
    """
    Process uploaded Excel file
    
    Expected columns (MUST match exactly):
    - AVG Choke size
    - DP_CHOKE_SIZE
    - ON_STREAM_HRS
    - AVG_DP_TUBING
    - AVG_DOWNHOLE_PRESSURE
    - AVG_DOWNHOLE_TEMPERATURE
    - AVG_WHP_P
    - AVG_WHT_P
    
    Returns: list of (success/fail, result_dict)
    """
    try:
        df = pd.read_excel(filepath)
        results = []
        
        # Check if required columns exist
        missing_cols = [col for col in FEATURE_NAMES if col not in df.columns]
        if missing_cols:
            return {
                'error': f'Missing required columns: {", ".join(missing_cols)}. Expected columns: {", ".join(FEATURE_NAMES)}'
            }
        
        # Process each row
        for idx, row in df.iterrows():
            # Convert row to dict
            input_dict = row.to_dict()
            
            # Filter only required features & check for NaN values
            filtered_dict = {}
            has_nan = False
            for feature in FEATURE_NAMES:
                val = input_dict[feature]
                # Check for NaN or None
                if pd.isna(val) or val is None:
                    has_nan = True
                    break
                try:
                    filtered_dict[feature] = float(val)
                except (ValueError, TypeError):
                    has_nan = True
                    break
            
            if has_nan:
                results.append({
                    'row': idx + 2,  # +2 because row 1 is header, idx is 0-based
                    'success': False,
                    'error': 'Row has missing or invalid values (NaN, empty, non-numeric)'
                })
                continue
            
            # Validate input bounds
            is_valid, errors = validate_input(filtered_dict)
            
            if not is_valid:
                results.append({
                    'row': idx + 2,
                    'success': False,
                    'error': ', '.join(errors)
                })
                continue
            
            # Predict
            pred, pred_error = predict_production(filtered_dict)
            if pred_error:
                results.append({
                    'row': idx + 2,
                    'success': False,
                    'error': pred_error
                })
                continue
            
            # Optimize
            opt, opt_error = optimize_choke(filtered_dict)
            if opt_error:
                results.append({
                    'row': idx + 2,
                    'success': False,
                    'error': opt_error
                })
                continue
            
            # Success
            results.append({
                'row': idx + 2,
                'success': True,
                'data': {
                    **filtered_dict,
                    'predicted_oil': pred['oil'],
                    'predicted_water': pred['water'],
                    'choke_recommended': opt['choke_optimal'],
                    'oil_gain': opt['oil_gain'],
                    'water_reduction': opt['water_reduction']
                }
            })
        
        return results
    
    except Exception as e:
        return {'error': f'Excel parsing error: {str(e)}'}
