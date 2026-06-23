"""Shared CSS styling for Celios8 Solar Dashboard."""

def get_solar_css():
    """Return CSS styling for solar-themed dashboard - consistent with Celios ECC style."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .page-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ECEFF1;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }
    
    .page-subtitle {
        font-size: 0.9rem;
        color: #9E9E9E;
        font-weight: 400;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: #1A1F2B;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #66BB6A;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #B0BEC5;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    
    .metric-desc {
        font-size: 0.75rem;
        color: #9E9E9E;
        margin-top: 0.8rem;
        line-height: 1.4;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ECEFF1;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    
    .note-box {
        background: #2A1F1C;
        border: 1px solid #FF6B35;
        border-left: 4px solid #FF6B35;
        border-radius: 4px;
        padding: 1rem 1.2rem;
        font-size: 0.9rem;
        color: #ECEFF1;
        margin-bottom: 1.5rem;
    }
    
    .info-box {
        background: #1A2F2A;
        border: 1px solid #2E7D32;
        border-left: 4px solid #2E7D32;
        border-radius: 4px;
        padding: 1rem 1.2rem;
        font-size: 0.9rem;
        color: #ECEFF1;
        margin-bottom: 1.5rem;
    }
    
    .dev-placeholder {
        background: #1A1F2B;
        border: 2px dashed #2E7D32;
        border-radius: 8px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .dev-placeholder h2 {
        color: #66BB6A;
        font-size: 1.8rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .dev-placeholder p {
        color: #9E9E9E;
        font-size: 0.95rem;
    }
    </style>
    """
