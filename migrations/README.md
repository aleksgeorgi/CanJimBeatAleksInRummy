project/
│
├── app/
│   ├── __init__.py           # Initializes the Flask app
│   ├── routes.py             # Defines all routes
│   ├── models.py             # SQLAlchemy ORM models
│   ├── db_utils.py           # Utility functions (refactored for ORM)
│   ├── prediction/
│   │   ├── __init__.py       # Makes prediction a package
│   │   ├── prediction_logic.py
│
├── migrations/               # Alembic folder for database migrations
│   ├── versions/             # Versioned migration scripts
│   ├── env.py                # Alembic environment setup
│   ├── alembic.ini           # Alembic configuration file
│
├── config.py                 # Configuration for Flask app
├── requirements.txt          # Python dependencies
├── run.py                    # Entry point to run the app
