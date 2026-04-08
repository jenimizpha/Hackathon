# Hackathon
**BatteryLife Lab: AI Battery Optimization**  An AI-powered web app that simulates battery behavior and finds optimal charging strategies to extend battery life. It analyzes factors like current, temperature, and usage to reduce degradation and improve performance using smart optimization techniques.

## Features

- **AI-Powered Optimization**: Uses Bayesian optimization to find optimal charging strategies
- **Real-time Simulation**: Interactive dashboard with live battery simulations
- **Multiple Chemistries**: Support for NMC and LFP battery chemistries
- **Thermal Analysis**: Monitors temperature effects on battery health
- **Experiment Tracking**: Database storage of all simulation results
- **REST API**: FastAPI backend for programmatic access

## Architecture

- **Frontend**: Vanilla JavaScript with Chart.js for visualizations
- **Backend**: FastAPI (Python) with async support
- **AI/ML**: Simplified Bayesian optimization (can be extended with PyTorch/Botorch)
- **Database**: SQLite for development (easily upgradeable to InfluxDB/PostgreSQL)
- **Simulation**: Custom battery model (simplified version of PyBaMM for hackathon)

## Quick Start

### Prerequisites

- Python 3.8+
- Git

### Backend Setup

1. **Clone and navigate to the repository**:
   ```bash
   git clone https://github.com/jenimizpha/Hackathon.git
   cd Hackathon
   ```

2. **Run the automated setup** (Windows):
   ```bash
   setup.bat
   ```
   Or manually:
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Test the backend** (optional):
   ```bash
   python test_backend.py
   ```

4. **Run the backend server**:
   ```bash
   python run_backend.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Open the frontend**:
   - Open `index.html` in your browser, or
   - Serve the files using a local server: `python -m http.server 3000`

2. **Access the application**:
   - Frontend: `http://localhost:3000` (or direct file opening)
   - API Docs: `http://localhost:8000/docs`

## API Endpoints

### Core Endpoints

- `GET /` - API root
- `POST /api/simulate` - Run battery simulation
- `GET /api/optimize` - Get AI optimization recommendations
- `GET /api/experiments` - Get experiment history
- `POST /api/optimize/run` - Trigger optimization cycle
- `GET /api/health` - Health check

### Example API Usage

```python
import requests

# Run a simulation
params = {
    "chemistry": "nmc",
    "temperature": 25.0,
    "c_rate": 1.5,
    "target_soc": 80.0
}
response = requests.post("http://localhost:8000/api/simulate", json=params)
result = response.json()

# Get optimization recommendation
response = requests.get("http://localhost:8000/api/optimize")
recommendation = response.json()
```

## Project Structure

```
Hackathon/
├── index.html              # Frontend dashboard
├── script.js               # Frontend JavaScript
├── style.css               # Frontend styles
├── main.py                 # FastAPI backend
├── run_backend.py          # Backend runner script
├── requirements.txt        # Python dependencies
├── models/
│   ├── battery_model.py    # Battery simulation model
│   └── optimizer.py        # AI optimization logic
├── database/
│   └── db_manager.py       # Database operations
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest
```

### Database

The application uses SQLite for simplicity. Database files:
- `battery_lab.db` - Main application database

### Extending the AI Model

The current implementation includes simplified models. To extend:

1. **Battery Model**: Replace with PyBaMM or other electrochemical models
2. **Optimizer**: Integrate full BoTorch for Bayesian optimization
3. **Database**: Upgrade to InfluxDB for time-series data

## Deployment

### Local Development

1. Start backend: `python run_backend.py`
2. Serve frontend: `python -m http.server 3000`
3. Access at `http://localhost:3000`

### Production Deployment

For production deployment, consider:
- Using a WSGI server (Gunicorn)
- Setting up proper CORS policies
- Adding authentication
- Using a production database
- Containerizing with Docker

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
