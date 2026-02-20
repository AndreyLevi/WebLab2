const API_URL = "/api";
let authToken = localStorage.getItem('token');

// ===== Аутентификация =====

// Вход
document.getElementById('login-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(API_URL + "/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            authToken = data.access_token;
            window.location.href = 'index.html';
        } else {
            const error = await response.json();
            showMessage(error.detail, 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения', 'error');
    }
});

// Регистрация
document.getElementById('register-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    
    try {
        const response = await fetch(API_URL + "/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });
        
        if (response.ok) {
            showMessage('Регистрация успешна! Теперь войдите.', 'success');
            document.getElementById('register-form').reset();
        } else {
            const error = await response.json();
            showMessage('Ошибка: ' + error.detail, 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения', 'error');
    }
});

// ===== Работа со ссылками =====

async function loadLinks() {
    const container = document.getElementById('links-container');
    if (!container) return;
    
    checkAuth();
    
    try {
        const response = await fetch(API_URL + "/links/", {
            headers: { "Authorization": `Bearer ${authToken}` }
        });
        
        if (response.status === 401) {
            window.location.href = 'login.html';
            return;
        }
        
        const links = await response.json();
        
        if (links.length === 0) {
            container.innerHTML = "<p>Ссылок пока нет.</p>";
            return;
        }
        
        container.innerHTML = links.map(link => `
            <div class="link-card">
                <h3><a href="${link.url}" target="_blank">${link.title}</a></h3>
                <p>${link.description || 'Без описания'}</p>
                <small>ID: ${link.id} | Дата: ${new Date(link.created_at).toLocaleDateString()}</small>
                <button onclick="deleteLink(${link.id})" class="delete-btn">Удалить</button>
            </div>
        `).join('');
        
    } catch (error) {
        container.innerHTML = "<p style='color: red;'>Ошибка загрузки</p>";
    }
}

async function deleteLink(id) {
    if (!confirm('Удалить эту ссылку?')) return;
    
    checkAuth();
    
    try {
        const response = await fetch(API_URL + "/links/" + id, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            showMessage('Ссылка удалена', 'success');
            loadLinks();
        } else {
            showMessage('Ошибка удаления', 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения', 'error');
    }
}

// ===== Утилиты =====

function checkAuth() {
    if (!authToken) {
        window.location.href = 'login.html';
    }
}

function showMessage(text, type) {
    const msgDiv = document.getElementById('message');
    if (msgDiv) {
        msgDiv.className = type;
        msgDiv.innerText = text;
    }
}

function logout() {
    localStorage.removeItem('token');
    authToken = null;
    window.location.href = 'login.html';
}

// Проверка авторизации при загрузке
if (window.location.pathname.includes('index.html') || 
    window.location.pathname.includes('manage.html')) {
    checkAuth();
}