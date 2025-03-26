from flask import Blueprint, request, jsonify
from datetime import datetime

maintenance_routes = Blueprint('maintenance', __name__)

# Initialize with sample data
maintenance_records = [
    {
        'date': '2024-03-15',
        'panelId': 'A1',
        'technician': 'John Doe',
        'type': 'Routine Check',
        'status': 'Completed'
    },
    {
        'date': '2024-03-14',
        'panelId': 'B3',
        'technician': 'Jane Smith',
        'type': 'Repair',
        'status': 'Pending'
    }
]

@maintenance_routes.route('/', methods=['GET', 'POST'])
def handle_maintenance():
    global maintenance_records  # Make sure we're using the global variable
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)  # Debug log
            
            # Create maintenance record
            new_record = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'panelId': data.get('panelId'),
                'technician': data.get('technicianName'),
                'type': 'Routine Check',
                'status': 'Completed',
                'dc_power': data.get('dc_power'),
                'ac_power': data.get('ac_power'),
                'ambient_temperature': data.get('ambient_temperature'),
                'module_temperature': data.get('module_temperature'),
                'irradiation': data.get('irradiation')
            }
            
            # Add new record to the beginning of the list
            maintenance_records.insert(0, new_record)
            print("Updated records:", maintenance_records)  # Debug log
            
            return jsonify({'success': True, 'record': new_record}), 200
            
        except Exception as e:
            print("Error:", str(e))  # Debug log
            return jsonify({'error': str(e)}), 400
    
    # GET method - return all records
    return jsonify(maintenance_records), 200
