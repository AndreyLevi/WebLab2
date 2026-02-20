// Адрес нашего API
const API_URL = "/api/links";

// Функция загрузки всех ссылок
async function loadLinks() {
    const container = document.getElementById('links-container');
    
    // Если элемента нет на странице - выходим
    if (!container) return;
    
    try {
        // Делаем запрос к API
        const response = await fetch(API_URL + "/");
        const links = await response.json();
        
        // Если ссылок нет
        if (links.length === 0) {
            container.innerHTML = "<p>Ссылок пока нет. Добавьте первую!</p>";
            return;
        }
        
        // Создаём HTML для каждой ссылки
        container.innerHTML = links.map(link => `
            <div class="link-card">
                <h3><a href="${link.url}" target="_blank">${link.title}</a></h3>
                <p>${link.description || 'Без описания'}</p>
                <small style="color: #888;">ID: ${link.id}</small>
            </div>
        `).join('');
        
    } catch (error) {
        container.innerHTML = "<p style='color: red;'>Ошибка загрузки ссылок</p>";
        console.error(error);
    }
}

// Обработка формы добавления ссылки
document.getElementById('add-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();  // Отменяем стандартную отправку формы
    
    // Получаем данные из полей
    const url = document.getElementById('url').value;
    const title = document.getElementById('title').value;
    const description = document.getElementById('desc').value;
    const messageDiv = document.getElementById('message');
    
    try {
        // Отправляем POST запрос
        const response = await fetch(API_URL + "/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json" 
            },
            body: JSON.stringify({ 
                url: url, 
                title: title, 
                description: description 
            })
        });
        
        // Проверяем ответ
        if (response.ok) {
            messageDiv.style.color = "green";
            messageDiv.style.background = "#d4edda";
            messageDiv.innerText = "Ссылка успешно добавлена!";
            
            // Очищаем форму
            document.getElementById('add-form').reset();
        } else {
            const error = await response.json();
            messageDiv.style.color = "red";
            messageDiv.style.background = "#f8d7da";
            messageDiv.innerText = "Ошибка: " + error.detail;
        }
    } catch (error) {
        messageDiv.innerText = "Ошибка соединения с сервером";
    }
});

// Функция удаления ссылки
async function deleteLink() {
    const id = document.getElementById('delete-id').value;
    const messageDiv = document.getElementById('message');
    
    if (!id) {
        messageDiv.innerText = "Введите ID ссылки";
        return;
    }
    
    try {
        const response = await fetch(API_URL + "/" + id, { 
            method: "DELETE" 
        });
        
        if (response.ok) {
            messageDiv.style.color = "green";
            messageDiv.style.background = "#d4edda";
            messageDiv.innerText = " Ссылка удалена!";
            document.getElementById('delete-id').value = "";
        } else {
            messageDiv.style.color = "red";
            messageDiv.style.background = "#f8d7da";
            messageDiv.innerText = "Ссылка с таким ID не найдена";
        }
    } catch (error) {
        messageDiv.innerText = "Ошибка соединения";
    }
}