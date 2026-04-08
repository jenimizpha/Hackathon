"""
Battery-Life Lab Backend API
FastAPI application for AI-powered battery optimization
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
import asyncio
import json
from datetime import datetime
import os

# Import our modules
from models.battery_model import BatteryModel
from models.optimizer import BatteryOptimizer
from database.db_manager import DatabaseManager

app = FastAPI(
    title="Battery-Life Lab API",
    description="AI-powered battery optimization platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving the frontend)
app.mount("/static", StaticFiles(directory="."), name="static")

# Initialize components
battery_model = BatteryModel()
optimizer = BatteryOptimizer()
db_manager = DatabaseManager()

# Pydantic models for API
class SimulationParams(BaseModel):
    chemistry: str = "nmc"  # nmc or lfp
    temperature: float = 25.0  # Celsius
    c_rate: float = 1.5  # Charging current rate
    target_soc: float = 80.0  # Target state of charge (%)

class ExperimentResult(BaseModel):
    experiment_id: str
    strategy: str
    peak_c_rate: float
    max_temp: float
    health_score: int
    status: str
    capacity_retention: List[float]
    cycle_count: int

class OptimizationResult(BaseModel):
    suggested_c_rate: float
    confidence: float
    predicted_gain: float
    estimated_soh: float
    charging_time: int  # minutes
    thermal_risk: str
    projected_cycles: int

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Battery-Life Lab API", "version": "1.0.0"}

@app.post("/api/simulate", response_model=ExperimentResult)
async def run_simulation(params: SimulationParams, background_tasks: BackgroundTasks):
    """Run a battery simulation with given parameters"""
    try:
        # Generate experiment ID
        experiment_id = f"EXP-{np.random.randint(1000, 9999)}"

        # Run simulation
        result = await battery_model.simulate_cycle(
            chemistry=params.chemistry,
            temperature=params.temperature,
            c_rate=params.c_rate,
            target_soc=params.target_soc
        )

        # Create experiment result
        experiment_result = ExperimentResult(
            experiment_id=experiment_id,
            strategy="Custom Simulation",
            peak_c_rate=params.c_rate,
            max_temp=result["max_temp"],
            health_score=result["health_score"],
            status="completed",
            capacity_retention=result["capacity_history"],
            cycle_count=len(result["capacity_history"])
        )

        # Save to database in background
        background_tasks.add_task(db_manager.save_experiment, experiment_result.dict())

        return experiment_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.get("/api/optimize", response_model=OptimizationResult)
async def get_optimization():
    """Get AI optimization recommendations"""
    try:
        # Get current best parameters from optimizer
        recommendation = optimizer.get_recommendation()

        return OptimizationResult(
            suggested_c_rate=recommendation["c_rate"],
            confidence=recommendation["confidence"],
            predicted_gain=recommendation["gain"],
            estimated_soh=recommendation["soh"],
            charging_time=recommendation["time"],
            thermal_risk=recommendation["risk"],
            projected_cycles=recommendation["cycles"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.get("/api/experiments", response_model=List[ExperimentResult])
async def get_experiments(limit: int = 10):
    """Get recent experiments"""
    try:
        experiments = db_manager.get_recent_experiments(limit)
        return [ExperimentResult(**exp) for exp in experiments]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@app.post("/api/optimize/run")
async def run_optimization_cycle(background_tasks: BackgroundTasks):
    """Run a full optimization cycle (planning -> simulation -> learning)"""
    try:
        # This would run the full autonomous loop
        background_tasks.add_task(optimizer.run_optimization_cycle)
        return {"message": "Optimization cycle started", "status": "running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization cycle failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)