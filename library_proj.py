import uuid
import json

class Books:
    def __init__(self, id, title, author, year, status):
        """
        Инициализация объекта класса Книги:
        id: Уникальный идентификатор книги.
        title: Название книги.
        author: Автор книги.
        year: Год издания книги.
        status: Статус книги (например, 'в наличии' или 'выдана').
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f"Идентификатор книги: {self.id}\nНазвание книги: {self.title}\nАвтор книги: {self.author}\nГод издания: {self.year}\nСтатус книги: {self.status}"


class Books_Library:
    """Класс для управления библиотекой книг."""

    def __init__(self, file_name: str = r"data/book_database.json"):
        """
        Инициализация объекта библиотеки

        file_name: Имя файла базы данных книг.

        """
        self.file_name = file_name
        self.books = self.load_book_library() # создание списка книг
    
    #Загрузка данных из библиотеки
    def load_book_library(self):
        """Читает данные из файла базы данных и создает список объектов класса Books на основе этих данных.

        В случае, если файл не найден, ошибка чтения или некорректного формата файла,
    выводится сообщение об ошибке, и возвращается пустой список.
        
        Returns: Список объектов Books, созданных на основе данных из файла.        
        """
        try:
            with open(self.file_name, "r", encoding='utf-8') as file:
                book_data = json.load(file)
                books = [Books(**book) for book in book_data]
        except FileNotFoundError:
            books = []
        except json.JSONDecodeError:
            print("Ошибка чтения файла базы данных. Проверьте корректность содержимого.")
            books = []
        return books
    

    #Сохранение книги в библиотеке
    def save_book_database(self):
        """
        Сохраняет текущий список книг (self.books) в файл базы данных.

        Функция преобразует объекты класса Books в словари и записывает их в файл в формате JSON. 
        Используется кодировка UTF-8 и отступы для читаемости(indent=2). 
        Данные сохраняются в файл, указанный в self.file_name.
        """
        book_data = [{
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "status": book.status}
            for book in self.books] # генератор списка на основе списка книг (self.books)
        
        with open(self.file_name, "w", encoding='utf-8') as file:
            json.dump(book_data, file, indent=2, ensure_ascii=False)


    #ДОБАВЛЕНИЕ КНИГИ В БД БИБЛИОТЕКИ
    def add_book(self, book: Books):
        """ 
        Добавляет новую книгу в библиотеку.

        book (Books): Объект класса Books, представляющий книгу для добавления.

        Действия:
        - Добавляет книгу в список `self.books`.
        - Сохраняет обновленный список книг в файл базы данных.
        """ 
        self.books.append(book) # добавление книги в уже существущий список книг
        self.save_book_database()
        print("Книга успешно добавлена\n")


    #Удаление книги из БД библиотеки
    def delete_book(self, id_delete: str):
        """
        Удаляет книгу из библиотеки по указанному ID.

        Параметры:
            id_delete (str): Уникальный идентификатор книги для удаления.

        Returns:
            str: Сообщение о результате операции ("Книга удалена из библиотеки" или "Книга с данным ID не найдена
        """
        book_to_delete = next((book for book in self.books if book.id == id_delete), None)
        if book_to_delete is None:
            return f"Ошибка: Книга с ID {id_delete} не найдена\n"
        # Удаление книги
        self.books.remove(book_to_delete)
        self.save_book_database()
        return "Книга успешно удалена\n"
    

    # Поиск книг
    def search_book(self, criterion: list[str])-> set[Books]:
        """
        Осуществляет поиск книг по заданным критериям.

        Args:
            criterion (list[str]): передает список параметров по которым, производится поиск книг

        Returns:
            set[Books]: возвращает результат в виде множества книг
        """
        results = set()
        for crit in criterion:
            result = [book for book in self.books if any(crit.lower() in value.lower() for value in vars(book).values())]
            results.update(result)
        return results


    # Отображение всех книг
    def show_all_books(self):
        """
        Возвращает полный список всех книг, находящихся в библиотеке.

        Returns:
            list: Список объектов класса `Books`, представляющих книги в библиотеке.
        """
        return self.books
    

    # Изменение статуса книги
    def change_status(self, id: str, new_status: str):
        """
        Изменение статуса книги.

        Args:
            id (str): Уникальный идентификатор книги для поиска.
            new_status (str): Новый статус книги ("1" для "В наличии", "2" для "Выдана").

        Returns:
            str: Результат операции, сообщение об успешности изменения или об ошибке.

        Примечание:
            После изменения статуса книги изменения сохраняются в базе данных
            с помощью вызова `self.save_book_database()`.
        """
        for book in self.books:
            if book.id == id:
                if new_status == "1":
                    book.status = "В наличии"
                else:
                    book.status = "Выдана"
                result = "Статус изменён"
                self.save_book_database()
                break
            else:
                result = "Книга не найдена"
        return result


def main():
    library_database = Books_Library()
    while True:
        choice = input("Выберите действие:\n"
        "1. Добавление книги\n"
        "2. Удаление книги\n"
        "3. Поиск книги\n"
        "4. Отображение всех книг\n"
        "5. Изменение статуса книги\n"
        "Ваш выбор: "
        )
    
        if choice == "1":
            while True:
                # Ввод данных
                print("Введите следующие данные (или введите 'exit' для выхода из этой операции):")
                title = input("Введите название книги: ").strip()
                if title.lower() == 'exit':
                    print("Выход из программы\n")
                    break
                author = input("Введите автора книги: ").strip()
                if author.lower() == 'exit':
                    print("Выход из программы\n")
                    break
                year = input("Введите год издания книги: ").strip()
                if year.lower() == 'exit':
                    print("Выход из программы\n")
                    break

                 # Проверка введенных данных
                if not title:
                    print("Поле 'Название книги' не может быть пустым.")
                elif not author:
                    print("Поле 'Автор книги' не может быть пустым.")
                elif not year.isdigit() or int(year) < 1000 or int(year) > 9999:
                    print("Поле 'Год издания книги' должен быть числом из четырех цифр и не может быть пустым .")
                else:
                    # Все введённые данные валидны, создаем объект класса "Books"
                    id = str(uuid.uuid4()) # создание уникального ID
                    status = "в наличии"
                    book = Books(id, title, author, year, status)
                    library_database.add_book(book)
                    break


        elif choice == "2":
            id_delete = input("Введите ID книги, которую хотите удалить:\n")
            result = library_database.delete_book(id_delete)
            print(result)


        elif choice == "3":
            criterion = input("Для поиска книги введите одну из полей: автор, название книги или год издания: ")
            if criterion:
                results = library_database.search_book(criterion.split(", "))
                if len(results) == 0:
                    print("По вашему запросу книги не найдены!")
                else:
                    print("Найдены следующие книги:")
                    for book in results:
                        print(book, "\n")
            else:
                print("Введите данные!\n")
            

        elif choice == "4":
            results = library_database.show_all_books()
            if results:
                for book in results:
                    print(book, '\n')
            else:
                print("Библиотека пуста\n")


        elif choice == "5":
            id = input("Введите ID книги: ")
            new_status = input("Выберите статус книги:\n1. В наличии\n2. Выдана\n")
            if new_status == "1" or new_status == "2":
                result = library_database.change_status(id, new_status)
                print(result, "\n")
            else:
                print('Некорректный выбор. Выберите из существующих состояний\n')
            


if __name__ == "__main__":
    main()