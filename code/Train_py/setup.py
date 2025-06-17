#!/usr/bin/env python3
"""
Setup script for AQI Prediction Pipeline
Installs dependencies and prepares the environment.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(cmd, description):
    """Run a command and log the result."""
    try:
        logger.info(f"Running: {description}")
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("Python 3.8+ is required")
        return False
    logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies."""
    logger.info("Installing dependencies from requirements.txt...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
        
    return True

def create_directories():
    """Create necessary directories."""
    directories = [
        "data/processed",
        "data/windows", 
        "models",
        "reports/explanations",
        "reports/optuna",
        "notebooks"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")
        
    return True

def check_data_availability():
    """Check if data files are available."""
    data_files = [
        "data/raw/Combine/Combine_AllData.csv",
        "data/raw/Combine_Nomolization/Nomorlization_Combine_AllData.csv",
        "data/raw/Separate/",
        "data/raw/Separate_Nomorlization/"
    ]
    
    logger.info("Checking data availability...")
    available = []
    missing = []
    
    for data_file in data_files:
        path = Path(data_file)
        if path.exists():
            if path.is_file():
                size_mb = path.stat().st_size / (1024 * 1024)
                logger.info(f"✅ Found: {data_file} ({size_mb:.1f}MB)")
                available.append(data_file)
            elif path.is_dir() and len(list(path.glob('*.csv'))) > 0:
                file_count = len(list(path.glob('*.csv')))
                logger.info(f"✅ Found: {data_file} ({file_count} files)")
                available.append(data_file)
            else:
                logger.warning(f"⚠️  Empty directory: {data_file}")
                missing.append(data_file)
        else:
            logger.warning(f"❌ Missing: {data_file}")
            missing.append(data_file)
    
    if missing:
        logger.warning("Some data files are missing. The pipeline will only run for available data.")
        logger.info("Please ensure data files are placed in the correct directories:")
        for file in missing:
            logger.info(f"  - {file}")
    
    return len(available) > 0

def verify_installation():
    """Verify that key packages are installed correctly."""
    packages_to_check = [
        'numpy', 'pandas', 'sklearn', 'lightgbm', 
        'torch', 'optuna', 'shap', 'fastapi', 'uvicorn'
    ]
    
    logger.info("Verifying package installation...")
    
    for package in packages_to_check:
        try:
            __import__(package)
            logger.info(f"✅ {package} imported successfully")
        except ImportError as e:
            logger.error(f"❌ Failed to import {package}: {e}")
            return False
    
    # Check optional packages
    optional_packages = ['captum']
    for package in optional_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} (optional) imported successfully")
        except ImportError:
            logger.warning(f"⚠️  {package} (optional) not available - LSTM explanations will be limited")
    
    return True

def main():
    """Main setup function."""
    logger.info("="*60)
    logger.info("AQI PREDICTION PIPELINE SETUP")
    logger.info("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        logger.error("Failed to create directories")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Failed to install dependencies")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        logger.error("Package verification failed")
        sys.exit(1)
    
    # Check data availability
    data_available = check_data_availability()
    
    logger.info("="*60)
    logger.info("SETUP COMPLETED SUCCESSFULLY!")
    logger.info("="*60)
    
    if data_available:
        logger.info("✅ Data files detected - ready to run pipeline")
        logger.info("\nTo run the complete pipeline:")
        logger.info("  python run_pipeline.py")
        logger.info("\nTo check data availability:")
        logger.info("  python run_pipeline.py --check-data")
        logger.info("\nTo run specific pipelines:")
        logger.info("  python run_pipeline.py --pipelines combine combine_norm")
    else:
        logger.warning("⚠️  No data files detected")
        logger.info("Please place your data files in the appropriate directories and run setup again")
    
    logger.info("\nFor more options:")
    logger.info("  python run_pipeline.py --help")
    logger.info("  python src/serve_predict.py --help")

if __name__ == "__main__":
    main() 