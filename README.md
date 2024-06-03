
## O projekcie
Projekt został stworzony na potrzeby zaliczenia kursu "Zaawansowana Aplikacja w Chmurze" w programie Corporate Readiness
Certificate. Jest to REST API stworzone za pomocą biblioteki FastApi w języku Python. API jest symulacją części 
systemu biblioteki. Pozwala dodawać autorów, książki oraz wykonywać na nich podstawowe zapytania CRUD.


### Local Setup

#### Wymagania

* [Docker][Docker-url]

#### Uruchomienie 
1. W głównym katalogu projektu utwórz plik `.env` z następującą zawartością:
   ```sh
   APP_PORT=*wybrany port*
   APP_NAME=*nazwa aplikacji*
   POSTGRES_USER=*nazwa użytkownika*
   POSTGRES_PASSWORD=*hasło*
   POSTGRES_DB=*nazwa bazy danych*
   POSTGRES_PORT=*port bazy danych*
   ```
2. Uruchom kontenery za pomocą docker-compose:
   ```sh
   docker compose up
   ```
3. Aplikacja będzie dostępna pod adresem `http://localhost:*wybrany port*`
4. Jeśli pomimo instrukcji 
   ```sh
   depends_on:
      - postgres
   ```
    w pliku `docker-compose.yml` obraz aplikacji uruchamia się przed bazą danych, spróbuj ponownie uruchomić ten kontener.
5. Aplikacja jest dostępna pod adresem `http://localhost:*wybrany port*`
6. Dokumentacja API jest dostępna pod adresem `http://localhost:*wybrany port*/docs`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Docker-url]: https://www.docker.com/



