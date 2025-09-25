#!/bin/bash

# Inicializar banco de dados
python -c "
from app import create_tables
create_tables()
print('Banco de dados inicializado!')
"

# Executar com gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app