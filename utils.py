import matplotlib.pyplot as plt
import io
import base64
from models import db, Client

PROGRAMS = {
    "Fat Loss (FL) – 3 day": {"factor": 22, "desc": "3-day full-body fat loss"},
    "Fat Loss (FL) – 5 day": {"factor": 24, "desc": "5-day split, higher volume fat loss"},
    "Muscle Gain (MG) – PPL": {"factor": 35, "desc": "Push/Pull/Legs hypertrophy"},
    "Beginner (BG)": {"factor": 26, "desc": "3-day simple beginner full-body"},
}

def generate_adherence_chart(client_name):
    from models import Progress
    progress = Progress.query.filter_by(client_name=client_name).order_by(Progress.id).all()
    if not progress:
        return None
    
    weeks = [p.week for p in progress]
    adherence = [p.adherence for p in progress]
    
    plt.figure(figsize=(10, 5))
    plt.plot(weeks, adherence, marker='o', linewidth=2, color='#d4af37')
    plt.title(f'Weekly Adherence – {client_name}')
    plt.xlabel('Week')
    plt.ylabel('Adherence (%)')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

def calculate_bmi(client):
    if not client.height or not client.weight or client.height <= 0 or client.weight <= 0:
        return None
    h_m = client.height / 100
    return round(client.weight / (h_m * h_m), 1)

def get_bmi_category(bmi):
    if bmi < 18.5: return "Underweight", "Potential nutrient deficiency"
    elif bmi < 25: return "Normal", "Low risk if active"
    elif bmi < 30: return "Overweight", "Moderate risk; focus adherence"
    else: return "Obese", "Higher risk; prioritize fat loss"
