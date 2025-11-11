"""Database connection and utilities."""
from pymongo import MongoClient
from pymongo.database import Database
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client
_client: MongoClient = None
_db: Database = None


def get_client() -> MongoClient:
    """Get or create MongoDB client."""
    global _client
    if _client is None:
        try:
            _client = MongoClient(settings.mongodb_uri)
            # Test connection
            _client.admin.command('ping')
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    return _client


def get_database() -> Database:
    """Get database instance."""
    global _db
    if _db is None:
        client = get_client()
        _db = client[settings.mongodb_db_name]
    return _db


def close_connection():
    """Close MongoDB connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB connection closed")

