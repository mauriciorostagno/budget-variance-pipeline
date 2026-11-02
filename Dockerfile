FROM apache/airflow:3.3.2

# Dependencies the classification agent needs, installed next to Airflow.
RUN pip install --no-cache-dir groq python-dotenv psycopg2-binary requests

# dbt gets its own virtualenv. Airflow and dbt pin overlapping libraries, and
# keeping them apart means a dbt upgrade can never break the scheduler.
# It lives under the airflow user's home because /opt belongs to root.
#
# Both versions are pinned to what the project was developed against. Left
# unpinned, pip resolves dbt-core to a pre-release and the orchestrator ends up
# running a different dbt than the one the models were written and tested with.
RUN python -m venv /home/airflow/dbt-venv \
    && /home/airflow/dbt-venv/bin/pip install --no-cache-dir \
        dbt-core==1.12.5 \
        dbt-postgres==1.11.0
