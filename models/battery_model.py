"""
Simplified Battery Model for Hackathon Demo
This is a simplified battery degradation model instead of full PyBaMM
"""

import numpy as np
import asyncio
from typing import Dict, List
import math

class BatteryModel:
    def __init__(self):
        # Battery parameters for different chemistries
        self.chemistries = {
            "nmc": {
                "nominal_capacity": 3000,  # mAh
                "nominal_voltage": 3.7,   # V
                "max_voltage": 4.2,       # V
                "min_voltage": 2.5,       # V
                "degradation_rate": 0.001,  # per cycle
                "thermal_sensitivity": 0.002
            },
            "lfp": {
                "nominal_capacity": 2800,  # mAh
                "nominal_voltage": 3.2,   # V
                "max_voltage": 3.65,      # V
                "min_voltage": 2.0,       # V
                "degradation_rate": 0.0008,  # per cycle (more stable)
                "thermal_sensitivity": 0.0015
            }
        }

    async def simulate_cycle(self, chemistry: str, temperature: float,
                           c_rate: float, target_soc: float) -> Dict:
        """
        Simulate a single charge-discharge cycle
        Returns simulation results including capacity retention and thermal data
        """
        if chemistry not in self.chemistries:
            raise ValueError(f"Unsupported chemistry: {chemistry}")

        params = self.chemistries[chemistry]

        # Simulate charging phase
        charge_time = self._calculate_charge_time(c_rate, target_soc, params)
        max_temp = self._calculate_max_temperature(temperature, c_rate, charge_time)

        # Calculate degradation
        degradation_factor = self._calculate_degradation(
            c_rate, temperature, max_temp, params
        )

        # Generate capacity history (simplified aging curve)
        capacity_history = self._generate_capacity_history(degradation_factor)

        # Calculate health score (0-100)
        final_capacity = capacity_history[-1]
        health_score = int((final_capacity / 100.0) * 100)

        return {
            "max_temp": round(max_temp, 1),
            "charge_time": round(charge_time, 1),
            "health_score": health_score,
            "capacity_history": capacity_history,
            "degradation_rate": round(degradation_factor * 100, 3),
            "efficiency": round(0.95 - degradation_factor, 3)  # Simplified
        }

    def _calculate_charge_time(self, c_rate: float, target_soc: float, params: Dict) -> float:
        """Calculate charging time in minutes"""
        # Simplified charging time calculation
        capacity = params["nominal_capacity"]
        charge_amount = (target_soc / 100.0) * capacity  # mAh to charge
        current = c_rate * capacity  # mA
        time_hours = charge_amount / current
        return time_hours * 60  # Convert to minutes

    def _calculate_max_temperature(self, ambient_temp: float, c_rate: float, charge_time: float) -> float:
        """Calculate maximum temperature during charging"""
        # Simplified thermal model
        heat_generation = c_rate * 0.1  # Heat per unit C-rate
        time_factor = min(charge_time / 60, 2)  # Time-based heating
        temp_rise = heat_generation * time_factor * 10  # Degrees C
        return ambient_temp + temp_rise

    def _calculate_degradation(self, c_rate: float, ambient_temp: float,
                             max_temp: float, params: Dict) -> float:
        """Calculate capacity degradation factor"""
        # Base degradation
        degradation = params["degradation_rate"]

        # C-rate stress factor
        c_rate_stress = (c_rate - 1.0) * 0.0005 if c_rate > 1.0 else 0

        # Temperature stress factor
        temp_stress = max(0, (max_temp - 25) * params["thermal_sensitivity"])

        # Total degradation per cycle
        total_degradation = degradation + c_rate_stress + temp_stress

        return min(total_degradation, 0.01)  # Cap at 1% per cycle

    def _generate_capacity_history(self, degradation_rate: float, cycles: int = 100) -> List[float]:
        """Generate capacity retention over multiple cycles"""
        capacity = 100.0  # Start at 100%
        history = [capacity]

        for _ in range(cycles - 1):
            capacity -= degradation_rate * 100  # Convert to percentage
            capacity = max(capacity, 50.0)  # Don't go below 50%
            history.append(round(capacity, 2))

        return history

    async def simulate_multiple_cycles(self, chemistry: str, temperature: float,
                                     c_rate: float, target_soc: float, num_cycles: int = 50) -> Dict:
        """Simulate multiple cycles for aging studies"""
        results = []
        total_degradation = 0

        for cycle in range(num_cycles):
            # Slight variation in conditions for realism
            temp_variation = np.random.normal(0, 2)  # ±2°C variation
            current_temp = temperature + temp_variation

            cycle_result = await self.simulate_cycle(
                chemistry, current_temp, c_rate, target_soc
            )

            results.append({
                "cycle": cycle + 1,
                "capacity": cycle_result["capacity_history"][-1],
                "max_temp": cycle_result["max_temp"],
                "health_score": cycle_result["health_score"]
            })

            total_degradation += cycle_result["degradation_rate"]

            # Small delay to simulate processing time
            await asyncio.sleep(0.01)

        avg_degradation = total_degradation / num_cycles

        return {
            "cycle_results": results,
            "average_degradation": round(avg_degradation, 4),
            "final_capacity": results[-1]["capacity"],
            "total_cycles": num_cycles
        }