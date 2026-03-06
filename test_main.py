import pytest
import sqlite3
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app # Assuming your FastAPI code is in main.py

client = TestClient(app)

@pytest.fixture
def mock_db():
    """Sets up an in-memory database with your specific schema."""
    conn = sqlite3.connect(":memory:")
    # Critical: row_factory allows row['Region'] syntax which dict(row) requires
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    # 1. Updated Schema
    cursor.execute("""
        CREATE TABLE usage_table (
            id INTEGER PRIMARY KEY,
            Region TEXT,
            Year INTEGER,
            Percentage_using REAL,
            Source TEXT
        )
    """)
    
    # 2. Updated Seed Data
    sample_data = [
        (1, "North America", 2020, 91.5, "ITU"),
        (2, "Europe", 2020, 85.2, "World Bank"),
        (3, "North America", 2021, 93.1, "ITU")
    ]
    cursor.executemany("INSERT INTO usage_table VALUES (?, ?, ?, ?, ?)", sample_data)
    conn.commit()
    return conn

# --- TESTS ---

def test_read_all_data(mock_db):
    with patch("main.get_internet_usage_db", return_value=mock_db):
        response = client.get("/internet_usage_data/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        # Verify the structure of a single record
        assert data[0]["Percentage_using"] == 91.5
        assert "Source" in data[0]

def test_filter_by_year(mock_db):
    with patch("main.get_internet_usage_db", return_value=mock_db):
        response = client.get("/internet_usage_data/?year=2021")
        data = response.json()
        assert len(data) == 1
        assert data[0]["Year"] == 2021
        assert data[0]["Region"] == "North America"

def test_filter_by_region(mock_db):
    with patch("main.get_internet_usage_db", return_value=mock_db):
        # Note: Handling spaces in URLs using %20 or just letting the client handle it
        response = client.get("/internet_usage_data/?region=Europe")
        data = response.json()
        assert len(data) == 1
        assert data[0]["Source"] == "World Bank"

def test_filter_both(mock_db):
    with patch("main.get_internet_usage_db", return_value=mock_db):
        url = "/internet_usage_data/?year=2020&region=North%20America"
        response = client.get(url)
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["Percentage_using"] == 91.5