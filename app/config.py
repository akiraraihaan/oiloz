import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# ML MODEL FEATURES (8 input parameters)
# ============================================
FEATURE_NAMES = [
    'AVG Choke size',
    'DP_CHOKE_SIZE',
    'ON_STREAM_HRS',
    'AVG_DP_TUBING',
    'AVG_DOWNHOLE_PRESSURE',
    'AVG_DOWNHOLE_TEMPERATURE',
    'AVG_WHP_P',
    'AVG_WHT_P'
]

# Feature descriptions for UI
FEATURE_DESCRIPTIONS = {
    'AVG Choke size': 'Average Choke Size (0.1 - 1.0)',
    'DP_CHOKE_SIZE': 'Differential Pressure at Choke (psi)',
    'ON_STREAM_HRS': 'On-Stream Hours (0 - 24)',
    'AVG_DP_TUBING': 'Average DP Tubing (psi)',
    'AVG_DOWNHOLE_PRESSURE': 'Average Downhole Pressure (psi)',
    'AVG_DOWNHOLE_TEMPERATURE': 'Average Downhole Temperature (°F)',
    'AVG_WHP_P': 'Average Wellhead Pressure (psi)',
    'AVG_WHT_P': 'Average Wellhead Temperature (°F)'
}

# Feature bounds for validation
FEATURE_BOUNDS = {
    'AVG Choke size': (0.1, 1.0),
    'DP_CHOKE_SIZE': (0, 1000),
    'ON_STREAM_HRS': (0, 24),
    'AVG_DP_TUBING': (0, 5000),
    'AVG_DOWNHOLE_PRESSURE': (0, 10000),
    'AVG_DOWNHOLE_TEMPERATURE': (0, 400),
    'AVG_WHP_P': (0, 5000),
    'AVG_WHT_P': (0, 300)
}

# ============================================
# OPTIMIZATION PARAMETERS
# ============================================
CHOKE_MIN = float(os.getenv('CHOKE_MIN', 0.1))
CHOKE_MAX = float(os.getenv('CHOKE_MAX', 1.0))
PENALTY_WEIGHT = float(os.getenv('PENALTY_WEIGHT', 0.5))
OPTIMIZATION_METHOD = os.getenv('OPTIMIZATION_METHOD', 'Powell')

# ============================================
# WELL SELECTION
# ============================================
SELECTED_WELL = os.getenv('SELECTED_WELL', '15/9-F-14')

# ML MODEL PATHS
MODEL_PATHS = {
    'oil': 'ml_models/model_oil_xgb_14.pkl',
    'water': 'ml_models/model_water_xgb_14.pkl'
}

# ============================================
# DATABASE
# ============================================
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///oil_optimization.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
