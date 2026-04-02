from flask import Blueprint, render_template, request, jsonify, flash
from models import db, Client, Progress, Workout, Metric
from utils import generate_adherence_chart, calculate_bmi, get_bmi_category, PROGRAMS

main = Blueprint('main', __name__)

@main.route('/')
def index():
    clients = Client.query.order_by(Client.name).all()
    return render_template('index.html', clients=clients, programs=PROGRAMS)

@main.route('/client/<name>')
def client_dashboard(name):
    client = Client.query.filter_by(name=name).first_or_404()
    progress = Progress.query.filter_by(client_name=name).order_by(Progress.id).all()
    latest_metric = Metric.query.filter_by(client_name=name).order_by(Metric.date.desc()).first()
    workouts = Workout.query.filter_by(client_name=name).order_by(Workout.date.desc()).limit(10).all()
    return render_template('dashboard.html', 
                         client=client, progress=progress, 
                         latest_metric=latest_metric, workouts=workouts,
                         programs=PROGRAMS)

@main.route('/api/save_client', methods=['POST'])
def save_client():
    print("method hitting-----------------")

    data = request.json
    client = Client.query.filter_by(name=data['name']).first()
    factor = PROGRAMS.get(data.get('program'), {}).get('factor', 0)
    calories = int(data.get('weight', 0) * factor) if data.get('weight') else None
    
    client_data = {**data, 'calories': calories}
    if client:
        for key, value in client_data.items():
            if key != 'id' and value is not None:
                setattr(client, key, value)
    else:
        client = Client(**client_data)
        db.session.add(client)
    db.session.commit()
    return jsonify({'success': True, 'client': client_data})

@main.route('/api/save_progress', methods=['POST'])
def save_progress():
    data = request.json
    progress = Progress(
        client_name=data['client_name'],
        week=datetime.now().strftime("Week %U - %Y"),
        adherence=data['adherence']
    )
    db.session.add(progress)
    db.session.commit()
    return jsonify({'success': True})

@main.route('/api/chart/adherence/<name>')
def adherence_chart(name):
    plot_url = generate_adherence_chart(name)
    return jsonify({'chart': plot_url}) if plot_url else jsonify({'error': 'No data'})

@main.route('/api/bmi/<name>')
def bmi_info(name):
    client = Client.query.filter_by(name=name).first_or_404()
    bmi = calculate_bmi(client)
    if not bmi:
        return jsonify({'error': 'Missing height/weight'})
    category, risk = get_bmi_category(bmi)
    return jsonify({'bmi': bmi, 'category': category, 'risk': risk})
