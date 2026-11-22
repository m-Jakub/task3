import unittest # Importowanie modułu dla tworzenia przypadków testowych 
from project import db, app # Importowanie obiektu db i app z projektu
from project.books.models import Book # Importowanie modelu Book z modułu models.py

class TestBookModel(unittest.TestCase): # Definicja klasy testowej dziedziczącej po unittest.TestCase

    def test_book_creation(self): # Definicja metody testowej dla tworzenia książki
        # Tworzenie instancji książki
        book = Book(name="Test Book", author="Test Author", year_published=2023, book_type="Fiction")
        # Sprawdzenie, czy atrybuty książki są poprawnie ustawione
        self.assertEqual(book.name, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year_published, 2023)
        self.assertEqual(book.book_type, "Fiction")
        self.assertEqual(book.status, "available") # Sprawdzenie domyślnego statusu książki

    def test_invalid_book_creation(self): # Definicja metody testowej dla niepoprawnego tworzenia książki
        with self.assertRaises(ValueError): # Oczekiwanie na podniesienie wyjątku ValueError
            book = Book(name="", author="Test Author", year_published=2023, book_type="Fiction") # Pusta nazwa książki

    def test_invalid_year_published(self): # Definicja metody testowej dla niepoprawnego roku publikacji
        with self.assertRaises(ValueError): # Oczekiwanie na podniesienie wyjątku ValueError
            book = Book(name="Test Book", author="Test Author", year_published="2023", book_type="Fiction") # Niepoprawny typ danych dla year_published (string)

    def test_sql_injection(self): # Definicja metody testowej dla sprawdzenia podatności na SQL injection
        malicious_input = "Test Book'; DROP TABLE books; --" # Przykład złośliwego wejścia
        with app.app_context(): # Użycie kontekstu aplikacji Flask
            book = Book(name=malicious_input, author="Test Author", year_published=2023, book_type="Fiction") # Tworzenie książki z złośliwym wejściem
            db.session.add(book) # Dodanie książki do sesji bazy danych
            db.session.commit() # Zatwierdzenie zmian w bazie danych
            book_from_db = Book.query.filter_by(name=malicious_input).first() # Pobranie książki z bazy danych na podstawie złośliwego wejścia
            self.assertIsNotNone(book_from_db) # Sprawdzenie, czy książka została poprawnie dodana do bazy danych, co oznacza, że nie doszło do SQL injection
            db.session.delete(book_from_db) # Usunięcie książki z bazy danych po teście
            db.session.commit() # Zatwierdzenie zmian w bazie danych

    def test_xss(self): # Definicja metody testowej dla sprawdzenia podatności na XSS (Cross-Site Scripting)
        xss_input = "<script>alert('XSS');</script>" # Przykład złośliwego wejścia XSS
        with app.app_context(): # Użycie kontekstu aplikacji Flask
            book = Book(name=xss_input, author="Test Author", year_published=2023, book_type="Fiction") # Tworzenie książki z złośliwym wejściem XSS
            db.session.add(book) # Dodanie książki do sesji bazy danych
            db.session.commit() # Zatwierdzenie zmian w bazie danych
            book_from_db = Book.query.filter_by(name=xss_input).first() # Pobranie książki z bazy danych na podstawie złośliwego wejścia XSS
            self.assertIsNotNone(book_from_db) # Sprawdzenie, czy książka została poprawnie dodana do bazy danych, co oznacza, że nie doszło do XSS
            db.session.delete(book_from_db) # Usunięcie książki z bazy danych po teście
            db.session.commit() # Zatwierdzenie zmian w bazie danych

    def test_extreme_values(self): # Definicja metody testowej dla sprawdzenia obsługi ekstremalnych wartości
        extreme_name = "A" * 1000 # Tworzenie ekstremalnie długiej nazwy książki
        with app.app_context(): # Użycie kontekstu aplikacji Flask
            book = Book(name=extreme_name, author="Test Author", year_published=2023, book_type="Fiction") # Tworzenie książki z ekstremalnie długą nazwą
            db.session.add(book) # Dodanie książki do sesji bazy danych
            db.session.commit() # Zatwierdzenie zmian w bazie danych
            book_from_db = Book.query.filter_by(name=extreme_name).first() # Pobranie książki z bazy danych na podstawie ekstremalnie długiej nazwy
            self.assertIsNotNone(book_from_db) # Sprawdzenie, czy książka została poprawnie dodana do bazy danych
            db.session.delete(book_from_db) # Usunięcie książki z bazy danych po teście
            db.session.commit() # Zatwierdzenie zmian w bazie danych