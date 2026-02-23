# Geogambler turniir ennustussüsteem

See on FastAPI-põhine veebirakendus, mis võimaldab osalejatel ennustada Geoguessri turniiri voorude võitjaid ning adminil hallata ennustusvoore.

## Käivitamine
1. Paigalda vajalikud teegid:
   ```
   pip install -r requirements.txt
   ```

2. Loo .env fail juurkausta:
```
ADMIN_PASSWORD=admin
```

3. Käivita rakendus:
```
uvicorn main:app --reload
```

## Funktsionaalsus
- Osaleja saab:
  - vaadata edetabelit
  - ennustada avatud voorus
- Admin saab:
  - avada/lõpetada ennustusvoore
  - vaadata edetabelit

## Andmebaas
Rakendus kasutab SQLite andmebaasi. Skeem luuakse automaatselt, kui andmebaasi pole.

## Vaated
- / - kasutaja vaade
- /admin - admin vaade (parooliga)

## Mallid
Mallid asuvad kaustas templates.
