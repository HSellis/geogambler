# Geoguessri turniiri ennustusrakendus

Veebirakendus, mis võimaldab osalejatel ennustada Geoguessri turniiri voorude võitjaid ning adminil alustada ja lõpetada ennustusvoore.

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
