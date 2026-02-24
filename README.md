# Geogamblr: Geoguessri turniiri ennustusrakendus

Veebirakendus, mis võimaldab osalejatel ennustada Geoguessri turniiri voorude võitjaid ning adminil alustada ja lõpetada ennustusvoore.

<table>
  <tr>
    <td rowspan="2">
      <img src="https://github.com/user-attachments/assets/cfde961f-47b1-4063-ab6f-290ca1bf9f49" height="800"/>
    </td>
    <td>
      <img alt="image" src="https://github.com/user-attachments/assets/e9d6457c-7aa2-424a-b777-35205fe14476" height="400"/>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="image" src="https://github.com/user-attachments/assets/889b0632-4930-4da2-8180-889c57b4a83e" height="400"/>
    </td>
  </tr>
</table>

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
