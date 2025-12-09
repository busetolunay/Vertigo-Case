import pandas as pd
import logging
import uuid
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from datetime import datetime, timezone
from src.database import SessionLocal, engine
from src import models

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_and_seed_data(csv_path: str):
    logger.info(f"Reading data from {csv_path}...")
    
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)

    # 1. Read CSV (Auto-detect separator: comma or tab)
    try:
        df = pd.read_csv(csv_path, sep=None, engine='python')
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        return

    # 2. Data Cleaning
    initial_count = len(df)
    
    # Normalize headers to lowercase to avoid 'Name' vs 'name' issues
    df.columns = [c.lower().strip() for c in df.columns]

    # Drop rows where 'name' is missing
    df = df.dropna(subset=['name'])
    df = df[df['name'].astype(str).str.strip() != '']
    logger.info(f"Dropped {initial_count - len(df)} rows due to missing names.")

    # Robust Date Parsing Function
    def parse_smart_date(date_val):
        if pd.isna(date_val) or str(date_val).strip() == '':
            return datetime.now(timezone.utc)
        
        str_val = str(date_val).strip()
        
        # Case A: Unix Timestamp (Digits only)
        # e.g., 1719227554
        if str_val.isdigit() or str_val.replace('.', '', 1).isdigit():
            try:
                # Convert to float first, then to datetime
                return datetime.fromtimestamp(float(str_val), tz=timezone.utc)
            except ValueError:
                pass

        # Case B: Standard Date Strings
        try:
            dt = pd.to_datetime(str_val)
            if dt.tz is None:
                dt = dt.tz_localize('UTC')
            else:
                dt = dt.tz_convert('UTC')
            return dt
        except Exception:
            return datetime.now(timezone.utc)

    # Apply date parsing
    df['created_at_clean'] = df['created_at'].apply(parse_smart_date)

    # 3. Insert into Database
    db = SessionLocal()
    try:
        logger.info("Starting database insertion...")
        counter = 0
        
        for _, row in df.iterrows():
            # Check duplicates (Optional but recommended)
            exists = db.query(models.Clan).filter(models.Clan.name == row['name']).first()
            if exists:
                continue

            clan = models.Clan(
                id=str(uuid.uuid4()),  # Explicitly generate UUID
                name=str(row['name']).strip(),
                region=str(row['region']).strip(), 
                created_at=row['created_at_clean']
            )
            db.add(clan)
            counter += 1
        
        db.commit()
        logger.info(f"Successfully inserted {counter} clans.")
        
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Path inside the Docker container
    # Note: Ensure your CSV is actually copied to this location in Dockerfile
    csv_file = "clan_sample_data.csv" 
    
    if os.path.exists(csv_file):
        clean_and_seed_data(csv_file)
    else:
        logger.error(f"File not found: {csv_file}")
