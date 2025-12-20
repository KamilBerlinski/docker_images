import getpass as gp
import platform 
import datetime as dt
import os

print(f"test, time {dt.datetime.today()}")
print(f"{platform.system()}, {platform.release()}")
print(f"user {gp.getuser()} \n")
print(f"TRYB PRACY: {os.environ.get('SRODOWISKO')}")
print(f"Hasło z env: {os.environ.get('TAJNE_HASLO')}")
