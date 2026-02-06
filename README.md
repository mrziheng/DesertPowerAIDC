# DesertAIDC: Renewable Energy Potential Assessment for AI Data Centers in Desert Regions

## Project Overview

DesertAIDC is a comprehensive research project designed to evaluate the renewable energy potential for deploying artificial intelligence data centers in global desert regions. This project integrates optimized configurations of solar, wind, and energy storage systems to provide sustainable clean energy solutions for AI data centers.

## Key Features

- 🔍 **Multi-dimensional Assessment**: Comprehensive consideration of technical, economic, and environmental factors
- 🌍 **Global Coverage**: Coverage of major desert regions worldwide
- ⚡ **Optimization Modeling**: Power system optimization based on Gurobi solver
- 📊 **Visualization Analysis**: Rich charts and map presentations
- 💰 **Cost-Benefit Analysis**: Levelized Cost of Electricity (LCOE) analysis

## Directory Structure

```
DesertAIDC/
├── data/                    # Data directory
│   ├── fig/Vis/            # Visualization result images
│   ├── geo/                # Geospatial data
│   │   ├── Base/           # Base geographic data
│   │   └── desert/         # Desert region vector data
│   ├── net/                # Network infrastructure data
│   ├── res/                # Result data
│   │   └── scen/sub/       # Scenario analysis subdirectory
│   └── vre/                # Variable renewable energy data
├── *.ipynb                 # Jupyter Notebook analysis scripts
├── *.py                    # Python core modules
└── README.md              # Project documentation
```

## Core Functional Modules

### 1. Data Processing and Analysis
- **[utils.py](./utils.py)**: Utility function library including LCOE calculation, directory management, and basic functions
- **[Visual.py](./Visual.py)**: Map visualization class providing professional geospatial data display functionality

### 2. Power System Modeling
- **[PowerModel.py](./PowerModel.py)**: Wind-Solar-Storage hybrid power generation system optimization model
- **[OptPowerDep.py](./OptPowerDep.py)**: Distributed computing framework for large-scale optimization solving

### 3. Main Analysis Notebooks
- **[AssessPoten.ipynb](./AssessPoten.ipynb)**: Desert region renewable energy potential assessment
- **[AssessEco.ipynb](./AssessEco.ipynb)**: Environmental impact assessment
- **[AssessEcoSensitivity.ipynb](./AssessEcoSensitivity.ipynb)**: Sensitivity analysis
- **[VisDesertArea.ipynb](./VisDesertArea.ipynb)**: Desert area visualization
- **[VisDesertVRE.ipynb](./VisDesertVRE.ipynb)**: Variable renewable energy resource visualization
- **[VisEcoSens.ipynb](./VisEcoSens.ipynb)**: Ecological sensitivity visualization
- **[VisGenProfile.ipynb](./VisGenProfile.ipynb)**: Generation profile analysis
- **[VisLantency.ipynb](./VisLantency.ipynb)**: Latency analysis
- **[VisPUE.ipynb](./VisPUE.ipynb)**: Power Usage Effectiveness analysis
- **[VisRoadDist.ipynb](./VisRoadDist.ipynb)**: Road distance analysis
- **[VisTemp.ipynb](./VisTemp.ipynb)**: Temperature condition analysis
- **[VisWSSConfig.ipynb](./VisWSSConfig.ipynb)**: Wind-Solar-Storage configuration visualization

## Technology Stack

### Programming Language
- Python 3.x

### Core Dependencies
- **Data Analysis**: pandas, numpy, geopandas
- **Optimization Modeling**: gurobipy (Gurobi Optimizer)
- **Visualization**: matplotlib, seaborn, contextily
- **Geospatial Processing**: shapely, geopandas
- **Scientific Computing**: math, multiprocessing

### Data Formats
- CSV: Structured data storage
- GeoPackage (.gpkg): Geospatial data
- Shapefile (.shp): Vector geographic data
- Pickle (.pkl): Python object serialization
- JSON Lines (.jsonl): Network data

## Installation and Configuration

### Environment Requirements
```bash
# Recommended conda environment
conda create -n desertaidc python=3.9
conda activate desertaidc

# Install core dependencies
pip install pandas geopandas matplotlib seaborn gurobipy shapely contextily
```

### Gurobi Solver Installation
```bash
# Academic license application: https://www.gurobi.com/free-academic-license/
# Commercial use requires purchasing a license
conda install -c gurobi gurobi
```

### Data Preparation
The project requires large data files. Please contact the project lead to obtain the complete dataset.

## Usage

### 1. Basic Analysis Workflow
```python
# Import core modules
from utils import calcu_lcoe
from Visual import MapViser
from PowerModel import opt_power

# Execute potential assessment
# Detailed steps please refer to AssessPoten.ipynb
```

### 2. Running Jupyter Notebooks
```bash
# Start Jupyter service
jupyter notebook

# Open corresponding analysis notebooks in browser
```

## Main Analysis Results

### 1. Technical Potential Assessment
- Global desert region wind-solar resource endowment analysis
- Optimal wind-solar-storage ratio optimization
- Spatiotemporal distribution characteristics of generation capacity

### 2. Economic Analysis
- LCOE calculation under different cost scenarios
- Cumulative generation vs. cost relationship curves
- Regional cost difference comparison

### 3. Environmental Impact Evaluation
- Ecological sensitivity zoning
- Environmental constraint identification
- Sustainable development indicator system

### 4. Infrastructure Suitability
- Road accessibility analysis
- Temperature condition suitability
- Network latency evaluation

## Visualization Examples

Main visualization charts generated by the project include:
- Desert region distribution maps
- Wind-solar resource potential maps
- LCOE spatial distribution maps
- Cumulative generation cost curves
- Ecological sensitivity maps
- Infrastructure accessibility maps

## Project Application Value

### Policy Making Support
- Scientific basis for government renewable energy development planning
- Support for carbon neutrality goal implementation pathway research

### Investment Decision Reference
- Site selection recommendations for enterprises investing in green data centers
- Reduction of project investment risks and uncertainties

### Technology Development Guidance
- Guidance for wind-solar-storage system optimization design
- Promotion of related technological innovation and industrial upgrading

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contact

For more information or to obtain the complete dataset, please contact the project lead (mrziheng@outlook.com).

---
