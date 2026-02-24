# Geogamblr: Geoguessri turniiri ennustusrakendus

Veebirakendus, mis võimaldab osalejatel ennustada Geoguessri turniiri voorude võitjaid ning adminil alustada ja lõpetada ennustusvoore.

| | |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/321aa9ce-1675-4bd3-ba5d-37e81268e728" height="600"/> | <img src="https://github.com/user-attachments/assets/3b62702c-ef02-4075-9af9-73159b1be530" height="300"/><br><br><img src="https://github.com/user-attachments/assets/30faedc9-3ab6-4d81-8234-8f10871cefd6" height="300"/> |

## Käivitamine
1. Installi vajalikud _library_'d:
   ```
   pip install -r requirements.txt
   ```

2. Loo `.env` fail ja pane sinna admin parool:
    ```
    ADMIN_PASSWORD=...
    ```

3. Käivita rakendus:
    ```
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

## Funktsionaalsus
- Osaleja saab:
  - vaadata edetabelit
  - ennustada avatud voorus
- Admin saab `/admin` lehel:
  - avada/lõpetada ennustusvoore
  - vaadata edetabelit
