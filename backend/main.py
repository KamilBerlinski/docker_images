import os
import time
import psycopg2
import sys

print("--- STARTUJĘ PROCES ETL ---")

# 1. Pobieramy namiary na bazę ze zmiennych środowiskowych (te z docker-compose.yaml)
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')

print(f"Próba połączenia do bazy: {db_host}...")

# 2. Mechanizm Retry (Ponawiania)
connection = None
for i in range(5):
    try:
        connection = psycopg2.connect(
            host=db_host,      
            user=db_user,
            password=db_pass,
            dbname=db_name
        )
        print("Suckes! Połączono z bazą.")
        break # Wychodzimy z pętli, bo się udało
    except psycopg2.OperationalError as e:
        print(f"Baza jeszcze śpi... próba {i+1}/5. Czekam 5s.")
        time.sleep(5)

if not connection:
    print("FATAL ERROR: Nie udało się połączyć z bazą po 5 próbach.")
    sys.exit(1)

# 3. Pobieranie danych (Ekstrakcja)
try:
    # 'with connection' automatycznie zatwierdza transakcję (commit)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pracownicy;")
            records = cursor.fetchall()

            print("\n--- RAPORT Z BAZY DANYCH ---")
            print(f"{'ID':<2} {'IMIE':<15} {'STANOWISKO'}")
            print("-" * 40)
    
            for row in records:
                # row to krotka (id, imie, stanowisko)
                print(f"{row[0]:<2} {row[1]:<15} {row[2]}")
                
            print("-" * 40)

except Exception as e:
    print(f"Błąd zapytania: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("\nPołączenie zamknięte. Koniec pracy.")