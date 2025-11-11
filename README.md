# CST8276---Advanced-Database-Topics

## Features

- **Data Catalog**: Browse and search housing indicators with metadata
- **Data Visualization**: View trends and charts for housing indicators
- **Data Export**: Export data in CSV or JSON formats
- **RESTful API**: Full-featured API for programmatic access
- **Data Load Pipeline**: Automated ETL process for loading CSV files into MongoDB
- **Search & Filter**: Advanced search and filtering capabilities
- **Admin Dashboard**: Admin endpoints for monitoring and error tracking

## Technology Stack

- **Backend**: Python 3.11, FastAPI
- **Database**: MongoDB 8.2
- **Data Processing**: Pandas
- **Validation**: Pydantic
- **Frontend**: HTML5, CSS3, JavaScript
- **Testing**: Pytest

### Prerequisites
- Python 3.11
- MongoDB
- pip (Python package manager)
- Docker (Optional)

### Quick Setup Using Virtual Environment 

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create and activate a virtual environment**:
   ```bash
   py -3.11 -m venv venv
   On Windows: .\venv\Scripts\activate
   ```

3. **Run the setup script** (handles everything automatically):
   ```bash
   python setup.py
   ```
   
   This single command will:
   - Check if Python version is 3.11.x
   - Install all dependencies
   - Create `.env` file (if it doesn't exist)
   - Start MongoDB with Docker (if Docker is available)
   - Verify MongoDB connection

4. **Load data into MongoDB**:
   ```bash
   python data_load/run_all.py
   ```

### Quick Setup Using Docker Deployment
1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Using Docker Compose**:
```bash
docker compose up --build -d
```

This will start:
- MongoDB on port 27017
- API server on port 8000

3. **Load data into MongoDB (Execute Data Load Script)**:
```bash
docker exec hna_api python data_load/run_all.py
```