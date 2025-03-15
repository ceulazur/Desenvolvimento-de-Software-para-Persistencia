document.addEventListener("DOMContentLoaded", function () {
  const app = document.getElementById("app");
  let isEditing = false;

  function fetchBooks() {
    fetch("/livros")
      .then((response) => response.json())
      .then((books) => {
        app.innerHTML = `
          <h2>Lista de Livros</h2>
          <ul id="books-list"></ul>
          <h2 id="form-title">Adicionar Novo Livro</h2>
          <form id="book-form">
            <input type="number" id="book-id" placeholder="ID" required />
            <input type="text" id="book-title" placeholder="Título" required />
            <input type="text" id="book-author" placeholder="Autor" required />
            <input type="number" id="book-year" placeholder="Ano" required />
            <input type="text" id="book-genre" placeholder="Gênero" required />
            <input type="number" id="book-pages" placeholder="Páginas" required />
            <button type="submit"><i class="fas fa-plus"></i></button>
          </form>
        `;
        const booksList = document.getElementById("books-list");
        books.forEach((book) => {
          const li = document.createElement("li");
          li.innerHTML = `
            <p>
              ${book.title} por ${book.author} (${book.year}) - ${book.genre}, ${book.pages} páginas
            </p>
            <button onclick="deleteBook(${book.id})"><i class="fas fa-trash-alt"></i></button>
            <button onclick="editBook(${book.id})"><i class="fas fa-edit"></i></button>
          `;
          booksList.appendChild(li);
        });

        document
          .getElementById("book-form")
          .addEventListener("submit", function (e) {
            e.preventDefault();
            const bookId = document.getElementById("book-id").value;
            const newBook = {
              id: bookId,
              title: document.getElementById("book-title").value,
              author: document.getElementById("book-author").value,
              year: document.getElementById("book-year").value,
              genre: document.getElementById("book-genre").value,
              pages: document.getElementById("book-pages").value,
            };
            const method = isEditing ? "PUT" : "POST";
            const url = isEditing ? `/livros/${bookId}` : "/livros";
            fetch(url, {
              method: method,
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(newBook),
            }).then(() => {
              fetchBooks();
              resetForm();
            });
          });
      });
  }

  window.deleteBook = function (id) {
    fetch(`/livros/${id}`, {
      method: "DELETE",
    }).then(() => fetchBooks());
  };

  window.editBook = function (id) {
    fetch(`/livros/${id}`)
      .then((response) => response.json())
      .then((book) => {
        isEditing = true;
        document.getElementById("form-title").innerText = "Editar Livro";
        document.getElementById("book-id").value = book.id;
        document.getElementById("book-title").value = book.title;
        document.getElementById("book-author").value = book.author;
        document.getElementById("book-year").value = book.year;
        document.getElementById("book-genre").value = book.genre;
        document.getElementById("book-pages").value = book.pages;
        document.querySelector("#book-form button").innerHTML =
          '<i class="fas fa-sync-alt"></i>';
      });
  };

  function resetForm() {
    isEditing = false;
    document.getElementById("form-title").innerText = "Adicionar Novo Livro";
    document.getElementById("book-id").value = "";
    document.getElementById("book-title").value = "";
    document.getElementById("book-author").value = "";
    document.getElementById("book-year").value = "";
    document.getElementById("book-genre").value = "";
    document.getElementById("book-pages").value = "";
    document.querySelector("#book-form button").innerHTML =
      '<i class="fas fa-plus"></i>';
  }

  fetchBooks();
});
