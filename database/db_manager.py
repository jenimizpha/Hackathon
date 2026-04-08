"""
Database Manager for Battery-Life Lab
Simplified SQLite implementation for hackathon demo
"""

import sqlite3
import json
from typing import List, Dict
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path: str = "battery_lab.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Experiments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT UNIQUE,
                    strategy TEXT,
                    peak_c_rate REAL,
                    max_temp REAL,
                    health_score INTEGER,
                    status TEXT,
                    capacity_retention TEXT,  -- JSON array
                    cycle_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    chemistry TEXT,
                    temperature REAL,
                    target_soc REAL
                )
            ''')

            # Optimization history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS optimization_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    c_rate REAL,
                    performance REAL,
                    confidence REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # System metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT,
                    value REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

    def save_experiment(self, experiment_data: Dict):
        """Save experiment result to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO experiments
                (experiment_id, strategy, peak_c_rate, max_temp, health_score,
                 status, capacity_retention, cycle_count, chemistry, temperature, target_soc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                experiment_data['experiment_id'],
                experiment_data['strategy'],
                experiment_data['peak_c_rate'],
                experiment_data['max_temp'],
                experiment_data['health_score'],
                experiment_data['status'],
                json.dumps(experiment_data['capacity_retention']),
                experiment_data['cycle_count'],
                experiment_data.get('chemistry', 'nmc'),
                experiment_data.get('temperature', 25.0),
                experiment_data.get('target_soc', 80.0)
            ))

            conn.commit()

    def get_recent_experiments(self, limit: int = 10) -> List[Dict]:
        """Get recent experiments"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT experiment_id, strategy, peak_c_rate, max_temp,
                       health_score, status, capacity_retention, cycle_count
                FROM experiments
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))

            rows = cursor.fetchall()

            experiments = []
            for row in rows:
                experiment = {
                    'experiment_id': row[0],
                    'strategy': row[1],
                    'peak_c_rate': row[2],
                    'max_temp': row[3],
                    'health_score': row[4],
                    'status': row[5],
                    'capacity_retention': json.loads(row[6]) if row[6] else [],
                    'cycle_count': row[7]
                }
                experiments.append(experiment)

            return experiments

    def save_optimization_result(self, c_rate: float, performance: float, confidence: float):
        """Save optimization result"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO optimization_history (c_rate, performance, confidence)
                VALUES (?, ?, ?)
            ''', (c_rate, performance, confidence))

            conn.commit()

    def get_optimization_history(self) -> List[Dict]:
        """Get optimization history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT c_rate, performance, confidence, timestamp
                FROM optimization_history
                ORDER BY timestamp DESC
                LIMIT 50
            ''')

            rows = cursor.fetchall()

            history = []
            for row in rows:
                entry = {
                    'c_rate': row[0],
                    'performance': row[1],
                    'confidence': row[2],
                    'timestamp': row[3]
                }
                history.append(entry)

            return history

    def save_metric(self, metric_name: str, value: float):
        """Save system metric"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO system_metrics (metric_name, value)
                VALUES (?, ?)
            ''', (metric_name, value))

            conn.commit()

    def get_metrics(self, metric_name: str, limit: int = 100) -> List[Dict]:
        """Get system metrics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT value, timestamp
                FROM system_metrics
                WHERE metric_name = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (metric_name, limit))

            rows = cursor.fetchall()

            metrics = []
            for row in rows:
                metric = {
                    'value': row[0],
                    'timestamp': row[1]
                }
                metrics.append(metric)

            return metrics

    def get_experiment_stats(self) -> Dict:
        """Get experiment statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Count total experiments
            cursor.execute('SELECT COUNT(*) FROM experiments')
            total_experiments = cursor.fetchone()[0]

            # Average health score
            cursor.execute('SELECT AVG(health_score) FROM experiments')
            avg_health = cursor.fetchone()[0] or 0

            # Best performing experiment
            cursor.execute('''
                SELECT experiment_id, health_score
                FROM experiments
                ORDER BY health_score DESC
                LIMIT 1
            ''')
            best_row = cursor.fetchone()
            best_experiment = {
                'id': best_row[0] if best_row else None,
                'score': best_row[1] if best_row else 0
            }

            return {
                'total_experiments': total_experiments,
                'average_health_score': round(avg_health, 1),
                'best_experiment': best_experiment
            }