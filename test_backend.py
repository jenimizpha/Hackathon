#!/usr/bin/env python3
"""
Simple test script for Battery-Life Lab backend components
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")

    try:
        from models.battery_model import BatteryModel
        print("✅ BatteryModel imported")
    except ImportError as e:
        print(f"❌ BatteryModel import failed: {e}")
        return False

    try:
        from models.optimizer import BatteryOptimizer
        print("✅ BatteryOptimizer imported")
    except ImportError as e:
        print(f"❌ BatteryOptimizer import failed: {e}")
        return False

    try:
        from database.db_manager import DatabaseManager
        print("✅ DatabaseManager imported")
    except ImportError as e:
        print(f"❌ DatabaseManager import failed: {e}")
        return False

    try:
        import fastapi
        print("✅ FastAPI imported")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False

    return True

def test_battery_model():
    """Test battery model functionality"""
    print("\nTesting BatteryModel...")

    try:
        from models.battery_model import BatteryModel
        import asyncio

        model = BatteryModel()

        # Test basic simulation
        async def run_test():
            result = await model.simulate_cycle("nmc", 25.0, 1.5, 80.0)
            print(f"✅ Simulation result: SOH={result['health_score']}%, Max Temp={result['max_temp']}°C")
            return result

        result = asyncio.run(run_test())
        return True

    except Exception as e:
        print(f"❌ BatteryModel test failed: {e}")
        return False

def test_optimizer():
    """Test optimizer functionality"""
    print("\nTesting BatteryOptimizer...")

    try:
        from models.optimizer import BatteryOptimizer

        optimizer = BatteryOptimizer()
        recommendation = optimizer.get_recommendation()

        print(f"✅ Optimizer recommendation: C-rate={recommendation['c_rate']}, Confidence={recommendation['confidence']}")
        return True

    except Exception as e:
        print(f"❌ Optimizer test failed: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("\nTesting DatabaseManager...")

    try:
        from database.db_manager import DatabaseManager

        db = DatabaseManager(":memory:")  # Use in-memory database for testing

        # Test saving experiment
        test_experiment = {
            'experiment_id': 'TEST-001',
            'strategy': 'Test Strategy',
            'peak_c_rate': 1.5,
            'max_temp': 35.0,
            'health_score': 85,
            'status': 'completed',
            'capacity_retention': [100, 99, 98, 97],
            'cycle_count': 4
        }

        db.save_experiment(test_experiment)
        print("✅ Experiment saved to database")

        # Test retrieving experiments
        experiments = db.get_recent_experiments(5)
        print(f"✅ Retrieved {len(experiments)} experiments from database")

        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Battery-Life Lab Backend Tests")
    print("=" * 40)

    tests = [
        ("Imports", test_imports),
        ("Battery Model", test_battery_model),
        ("Optimizer", test_optimizer),
        ("Database", test_database)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")

    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! Backend is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())