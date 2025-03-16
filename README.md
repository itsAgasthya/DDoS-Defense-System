# DDoS Defense System

A real-time DDoS defense system with a modern web interface for monitoring and controlling network traffic, featuring nature-inspired defense mechanisms and predictive security.

## Features

- **Real-time Traffic Monitoring**
  - Live packet processing statistics
  - Dynamic threat level indicators
  - Packets per second (PPS) monitoring
  - System uptime tracking
  - Alert history and notifications

- **Intelligent Defense Mechanisms**
  - Multiple detection models:
    - Anomaly Detection
    - DDoS Classification
    - Traffic Analysis
  - Adaptive threat level assessment
  - Configurable alert thresholds

- **Modern Web Interface**
  - Real-time dashboard with live updates
  - Interactive monitoring controls
  - Configurable system settings
  - Model status overview
  - Responsive Material-UI design

## Screenshots

![image](https://github.com/user-attachments/assets/0c488bcd-ad4a-4a48-93a2-665416d556cb)

![image](https://github.com/user-attachments/assets/42e5a652-2c42-4e1c-9fa2-5124a3527fb7)

![image](https://github.com/user-attachments/assets/ac1f28a8-d62c-4fa1-93d5-97654170b5df)

![image](https://github.com/user-attachments/assets/e7dc2df2-e948-478d-a5fc-8dfc5dbcb750)


## System Requirements

- Python 3.9+
- Node.js 14+ and npm
- Modern web browser

## Project Structure

```
ddos-defense/
├── backend/                 # FastAPI backend server
│   ├── main.py             # Main server file
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   └── App.tsx        # Main application
│   └── package.json       # Node.js dependencies
└── README.md              # This file
```

## Quick Start

### Backend Setup

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Start the frontend development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000

## Usage Guide

1. **Start Monitoring**
   - Navigate to http://localhost:3000/monitoring
   - Click "Start Monitoring" to begin traffic analysis
   - Use "Stop Monitoring" to halt the system

2. **View Dashboard**
   - Go to http://localhost:3000
   - Monitor real-time statistics:
     - Current threat level
     - Packets processed
     - Packets per second
     - System uptime
     - Recent alerts

3. **Configure Settings**
   - Visit http://localhost:3000/settings
   - Adjust alert thresholds:
     - Critical level (default: 1000 PPS)
     - High level (default: 750 PPS)
     - Medium level (default: 500 PPS)
   - Save changes to update the system

4. **Check Detection Models**
   - Access http://localhost:3000/models
   - View active detection models
   - Monitor model status and descriptions

## API Endpoints

- `GET /monitoring/status` - Get current monitoring status and statistics
- `POST /monitoring/start` - Start the monitoring system
- `POST /monitoring/stop` - Stop the monitoring system
- `PUT /monitoring/thresholds` - Update alert thresholds

## Development

The system uses:
- FastAPI for the backend API
- React with TypeScript for the frontend
- Material-UI for the user interface
- Real-time updates with 5-second polling interval

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
