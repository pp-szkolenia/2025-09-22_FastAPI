# FastAPI – szkolenie

### 1. Wprowadzenie
1. Idea aplikacji webowej
2. Protokół HTTP (klient, serwer, zasób, request, response)
3. Endpoint, URL, URI
4. Przykłady API oraz jak się z nimi komunikujemy
5. Przegląd narzędzi (terminal, Postman, JSON viewer)
6. Czym jest REST API
7. Format JSON
8. Type annotation w Pythonie
9. Omówienie projektu

### 2. FastAPI
1. Hello world
2. Ścieżki i routing
3. Metoda POST, request body, Pydantic
4. Pobranie konkretnego zasobu (path parameter)
5. HTTPException i błąd 404
6. JSONResponse zamiast słownika, domyślny `status_code`
7. Metoda DELETE, odpowiedź 204
8. Metoda PUT
9. Struktura projektu - `app.main:app`, modele do osobnego pliku
10. Struktura projektu - podział endpointów na osobne pliki
11. Automatyczna dokumentacja (`/docs`, `/redoc`)
12. Model odpowiedzi
13. Requestowanie API w Pythonie
14. Pydantic - rozszerzenie
15. Testy API - `TestClient`

###  3. Bazy danych
1. SQL i bazy danych w aplikacji webowej
2. Konfiguracja bazy dla projektu
3. Psycopg
4. Przechowywanie sekretów
5. SQLAlchemy (ORM)

### 4. CRUD
1. Omówienie poszczególnych liter
2. Implementacja operacji bazodanowych w psycopg
3. Implementacja operacji bazodanowych w SQLAlchemy
5. Query parameters (sortowanie, filtrowanie)

### 5. Pozostałe zagadnienia
1. Hashowanie haseł
2. Uwierzytelnianie i autoryzacja
3. Middleware
4. Frontend aplikacji
