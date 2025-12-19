const API_BASE = '/api/v1';

document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const section = btn.dataset.section;
        switchSection(section);
    });
});

let dashboardUpdateInterval = null;

function switchSection(sectionName) {
    if (dashboardUpdateInterval) {
        clearInterval(dashboardUpdateInterval);
        dashboardUpdateInterval = null;
    }
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.section === sectionName) {
            btn.classList.add('active');
        }
    });
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionName).classList.add('active');
    loadData(sectionName);
    if (sectionName === 'reports') {
        loadDashboard();
        dashboardUpdateInterval = setInterval(() => {
            loadDashboard();
        }, 5000);
    }
}

async function loadData(sectionName) {
    try {
        let data;
        switch(sectionName) {
            case 'clients':
                data = await fetch(`${API_BASE}/clients`).then(r => r.json());
                renderTable('clients', data, getClientsTableHeaders(), getClientsTableRow);
                break;
            case 'vehicles':
                data = await fetch(`${API_BASE}/vehicles`).then(r => r.json());
                renderTable('vehicles', data, getVehiclesTableHeaders(), getVehiclesTableRow);
                break;
            case 'parking-spaces':
                data = await fetch(`${API_BASE}/parking-spaces`).then(r => r.json());
                renderTable('parking-spaces', data, getParkingSpacesTableHeaders(), getParkingSpacesTableRow);
                break;
            case 'tariffs':
                data = await fetch(`${API_BASE}/tariffs`).then(r => r.json());
                renderTable('tariffs', data, getTariffsTableHeaders(), getTariffsTableRow);
                break;
            case 'sessions':
                data = await fetch(`${API_BASE}/parking-sessions`).then(r => r.json());
                renderTable('sessions', data, getSessionsTableHeaders(), getSessionsTableRow);
                break;
            case 'payments':
                data = await fetch(`${API_BASE}/payments`).then(r => r.json());
                renderTable('payments', data, getPaymentsTableHeaders(), getPaymentsTableRow);
                break;
            case 'reports':
                await loadDashboard();
                break;
        }
    } catch (error) {
        showNotification('Ошибка при загрузке данных', 'error');
        console.error(error);
    }
}

function renderTable(sectionName, data, headers, rowRenderer) {
    const container = document.getElementById(`${sectionName}-table-container`);
    
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>Нет данных</p></div>';
        return;
    }

    let html = '<table><thead><tr>';
    headers.forEach(header => {
        html += `<th>${header}</th>`;
    });
    html += '<th>Действия</th></tr></thead><tbody>';
    
    data.forEach(item => {
        html += rowRenderer(item);
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

function getClientsTableHeaders() {
    return ['ID', 'Имя', 'Фамилия', 'Телефон'];
}

function getVehiclesTableHeaders() {
    return ['ID', 'Марка', 'Модель', 'Номер', 'Цвет', 'Тип ID', 'Клиент ID'];
}

function getParkingSpacesTableHeaders() {
    return ['ID', 'Номер', 'Тип ID'];
}

function getTariffsTableHeaders() {
    return ['ID', 'Название', 'Цена за час', 'Цена за день'];
}

function getSessionsTableHeaders() {
    return ['ID', 'Транспорт ID', 'Место ID', 'Тариф ID', 'Время входа', 'Время выхода', 'Стоимость'];
}

function getPaymentsTableHeaders() {
    return ['ID', 'Сессия ID', 'Сумма', 'Метод ID', 'Время'];
}
function getClientsTableRow(item) {
    return `
        <tr>
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.surname}</td>
            <td>${item.phone}</td>
            <td>
                <button class="btn btn-secondary" onclick="showEditForm('clients', ${item.id})">Редактировать</button>
                <button class="btn btn-danger" onclick="deleteItem('clients', ${item.id})">Удалить</button>
            </td>
        </tr>
    `;
}

function getVehiclesTableRow(item) {
    return `
        <tr>
            <td>${item.id}</td>
            <td>${item.brand}</td>
            <td>${item.model}</td>
            <td>${item.license_plate}</td>
            <td>${item.color}</td>
            <td>${item.type_id}</td>
            <td>${item.client_id}</td>
            <td>
                <button class="btn btn-secondary" onclick="showEditForm('vehicles', ${item.id})">Редактировать</button>
                <button class="btn btn-danger" onclick="deleteItem('vehicles', ${item.id})">Удалить</button>
            </td>
        </tr>
    `;
}

function getParkingSpacesTableRow(item) {
    return `
        <tr>
            <td>${item.id}</td>
            <td>${item.number}</td>
            <td>${item.type_id}</td>
            <td>
                <button class="btn btn-secondary" onclick="showEditForm('parking-spaces', ${item.id})">Редактировать</button>
                <button class="btn btn-danger" onclick="deleteItem('parking-spaces', ${item.id})">Удалить</button>
            </td>
        </tr>
    `;
}

function getTariffsTableRow(item) {
    return `
        <tr>
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.price_per_hour}</td>
            <td>${item.price_per_day}</td>
            <td>
                <button class="btn btn-secondary" onclick="showEditForm('tariffs', ${item.id})">Редактировать</button>
                <button class="btn btn-danger" onclick="deleteItem('tariffs', ${item.id})">Удалить</button>
            </td>
        </tr>
    `;
}

function getSessionsTableRow(item) {
    return `
        <tr>
            <td>${item.id}</td>
            <td>${item.vehicle_id}</td>
            <td>${item.space_id}</td>
            <td>${item.tariff_id}</td>
            <td>${new Date(item.time_in).toLocaleString('ru-RU')}</td>
            <td>${item.time_out ? new Date(item.time_out).toLocaleString('ru-RU') : '-'}</td>
            <td>${item.total_cost || '-'}</td>
            <td>
                <button class="btn btn-secondary" onclick="showEditForm('sessions', ${item.id})">Редактировать</button>
            </td>
        </tr>
    `;
}

function getPaymentsTableRow(item) {
    return `
        <tr>
            <td>${item.id}</td>
            <td>${item.session_id}</td>
            <td>${item.amount}</td>
            <td>${item.method_id}</td>
            <td>${new Date(item.time).toLocaleString('ru-RU')}</td>
            <td>
                <button class="btn btn-secondary" onclick="showEditForm('payments', ${item.id})">Редактировать</button>
            </td>
        </tr>
    `;
}
async function showCreateForm(sectionName) {
    const formContainer = document.getElementById(`${sectionName}-form-container`);
    formContainer.classList.remove('hidden');
    
    let formHTML = '';
    switch(sectionName) {
        case 'clients':
            formHTML = getClientsForm();
            break;
        case 'vehicles':
            formHTML = await getVehiclesForm();
            break;
        case 'parking-spaces':
            formHTML = await getParkingSpacesForm();
            break;
        case 'tariffs':
            formHTML = getTariffsForm();
            break;
        case 'sessions':
            formHTML = await getSessionsForm();
            break;
        case 'payments':
            formHTML = await getPaymentsForm();
            break;
    }
    
    formContainer.innerHTML = formHTML;
    formContainer.scrollIntoView({ behavior: 'smooth' });
}

async function showEditForm(sectionName, id) {
    const formContainer = document.getElementById(`${sectionName}-form-container`);
    formContainer.classList.remove('hidden');
    
    try {
        let data;
        const endpoint = getEndpoint(sectionName);
        data = await fetch(`${API_BASE}${endpoint}/${id}`).then(r => r.json());
        
        let formHTML = '';
        switch(sectionName) {
            case 'clients':
                formHTML = getClientsForm(data);
                break;
            case 'vehicles':
                formHTML = await getVehiclesForm(data);
                break;
            case 'parking-spaces':
                formHTML = await getParkingSpacesForm(data);
                break;
            case 'tariffs':
                formHTML = getTariffsForm(data);
                break;
            case 'sessions':
                formHTML = await getSessionsForm(data);
                break;
            case 'payments':
                formHTML = await getPaymentsForm(data);
                break;
        }
        
        formContainer.innerHTML = formHTML;
        formContainer.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showNotification('Ошибка при загрузке данных', 'error');
        console.error(error);
    }
}

function getClientsForm(data = null) {
    return `
        <h3>${data ? 'Редактировать клиента' : 'Создать клиента'}</h3>
        <form onsubmit="saveItem(event, 'clients', ${data ? data.id : 'null'})">
            <div class="form-group">
                <label>Имя</label>
                <input type="text" name="name" value="${data ? data.name : ''}" required>
            </div>
            <div class="form-group">
                <label>Фамилия</label>
                <input type="text" name="surname" value="${data ? data.surname : ''}" required>
            </div>
            <div class="form-group">
                <label>Телефон</label>
                <input type="text" name="phone" value="${data ? data.phone : ''}" required>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-success">Сохранить</button>
                <button type="button" class="btn btn-secondary" onclick="hideForm('clients')">Отмена</button>
            </div>
        </form>
    `;
}

async function getVehiclesForm(data = null) {
    const vehicleTypes = await fetch(`${API_BASE}/references/vehicle-types`).then(r => r.json());
    const clients = await fetch(`${API_BASE}/clients`).then(r => r.json());
    
    return `
        <h3>${data ? 'Редактировать транспорт' : 'Создать транспорт'}</h3>
        <form onsubmit="saveItem(event, 'vehicles', ${data ? data.id : 'null'})">
            <div class="form-group">
                <label>Марка</label>
                <input type="text" name="brand" value="${data ? data.brand : ''}" required>
            </div>
            <div class="form-group">
                <label>Модель</label>
                <input type="text" name="model" value="${data ? data.model : ''}" required>
            </div>
            <div class="form-group">
                <label>Номер</label>
                <input type="text" name="license_plate" value="${data ? data.license_plate : ''}" required>
            </div>
            <div class="form-group">
                <label>Цвет</label>
                <input type="text" name="color" value="${data ? data.color : ''}" required>
            </div>
            <div class="form-group">
                <label>Тип транспорта</label>
                <select name="type_id" required>
                    <option value="">Выберите тип</option>
                    ${vehicleTypes.map(t => `<option value="${t.id}" ${data && data.type_id === t.id ? 'selected' : ''}>${t.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Клиент</label>
                <select name="client_id" required>
                    <option value="">Выберите клиента</option>
                    ${clients.map(c => `<option value="${c.id}" ${data && data.client_id === c.id ? 'selected' : ''}>${c.name} ${c.surname}</option>`).join('')}
                </select>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-success">Сохранить</button>
                <button type="button" class="btn btn-secondary" onclick="hideForm('vehicles')">Отмена</button>
            </div>
        </form>
    `;
}

async function getParkingSpacesForm(data = null) {
    const vehicleTypes = await fetch(`${API_BASE}/references/vehicle-types`).then(r => r.json());
    
    return `
        <h3>${data ? 'Редактировать место' : 'Создать место'}</h3>
        <form onsubmit="saveItem(event, 'parking-spaces', ${data ? data.id : 'null'})">
            <div class="form-group">
                <label>Номер места</label>
                <input type="text" name="number" value="${data ? data.number : ''}" required>
            </div>
            <div class="form-group">
                <label>Тип транспорта</label>
                <select name="type_id" required>
                    <option value="">Выберите тип</option>
                    ${vehicleTypes.map(t => `<option value="${t.id}" ${data && data.type_id === t.id ? 'selected' : ''}>${t.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-success">Сохранить</button>
                <button type="button" class="btn btn-secondary" onclick="hideForm('parking-spaces')">Отмена</button>
            </div>
        </form>
    `;
}

function getTariffsForm(data = null) {
    return `
        <h3>${data ? 'Редактировать тариф' : 'Создать тариф'}</h3>
        <form onsubmit="saveItem(event, 'tariffs', ${data ? data.id : 'null'})">
            <div class="form-group">
                <label>Название</label>
                <input type="text" name="name" value="${data ? data.name : ''}" required>
            </div>
            <div class="form-group">
                <label>Цена за час</label>
                <input type="number" step="0.01" name="price_per_hour" value="${data ? data.price_per_hour : ''}" required>
            </div>
            <div class="form-group">
                <label>Цена за день</label>
                <input type="number" step="0.01" name="price_per_day" value="${data ? data.price_per_day : ''}" required>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-success">Сохранить</button>
                <button type="button" class="btn btn-secondary" onclick="hideForm('tariffs')">Отмена</button>
            </div>
        </form>
    `;
}

async function getSessionsForm(data = null) {
    const vehicles = await fetch(`${API_BASE}/vehicles`).then(r => r.json());
    const spaces = await fetch(`${API_BASE}/parking-spaces`).then(r => r.json());
    const tariffs = await fetch(`${API_BASE}/tariffs`).then(r => r.json());
    
    const timeIn = data ? new Date(data.time_in).toISOString().slice(0, 16) : '';
    const timeOut = data && data.time_out ? new Date(data.time_out).toISOString().slice(0, 16) : '';
    
    return `
        <h3>${data ? 'Редактировать сессию' : 'Создать сессию'}</h3>
        <form onsubmit="saveItem(event, 'sessions', ${data ? data.id : 'null'})">
            <div class="form-group">
                <label>Транспорт</label>
                <select name="vehicle_id" required>
                    <option value="">Выберите транспорт</option>
                    ${vehicles.map(v => `<option value="${v.id}" ${data && data.vehicle_id === v.id ? 'selected' : ''}>${v.brand} ${v.model} (${v.license_plate})</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Парковочное место</label>
                <select name="space_id" required>
                    <option value="">Выберите место</option>
                    ${spaces.map(s => `<option value="${s.id}" ${data && data.space_id === s.id ? 'selected' : ''}>${s.number}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Тариф</label>
                <select name="tariff_id" required>
                    <option value="">Выберите тариф</option>
                    ${tariffs.map(t => `<option value="${t.id}" ${data && data.tariff_id === t.id ? 'selected' : ''}>${t.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Время входа</label>
                <input type="datetime-local" name="time_in" value="${timeIn}" required>
            </div>
            <div class="form-group">
                <label>Время выхода</label>
                <input type="datetime-local" name="time_out" id="session-time-out" value="${timeOut}" onchange="calculateSessionCost()">
                <small style="color: #7f8c8d; font-size: 12px;">Если указано, стоимость рассчитается автоматически</small>
            </div>
            <div class="form-group">
                <label>Общая стоимость</label>
                <input type="number" step="0.01" name="total_cost" id="session-total-cost" value="${data ? (data.total_cost || '') : ''}" ${data ? '' : 'readonly'} placeholder="Рассчитывается автоматически при указании времени выхода">
                ${data ? '<small style="color: #7f8c8d; font-size: 12px;">Можно изменить вручную при редактировании</small>' : ''}
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-success">Сохранить</button>
                <button type="button" class="btn btn-secondary" onclick="hideForm('sessions')">Отмена</button>
            </div>
        </form>
    `;
}

async function getPaymentsForm(data = null) {
    const sessions = await fetch(`${API_BASE}/parking-sessions`).then(r => r.json());
    const methods = await fetch(`${API_BASE}/references/payment-methods`).then(r => r.json());
    
    const time = data ? new Date(data.time).toISOString().slice(0, 16) : '';
    
    return `
        <h3>${data ? 'Редактировать платеж' : 'Создать платеж'}</h3>
        <form onsubmit="saveItem(event, 'payments', ${data ? data.id : 'null'})">
            <div class="form-group">
                <label>Сессия парковки</label>
                <select name="session_id" id="payment-session-select" onchange="updatePaymentAmount()" required>
                    <option value="">Выберите сессию</option>
                    ${sessions.map(s => `<option value="${s.id}" data-cost="${s.total_cost || ''}" ${data && data.session_id === s.id ? 'selected' : ''}>Сессия #${s.id}${s.total_cost ? ' (Стоимость: ' + s.total_cost + ' ₽)' : ''}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Сумма (автоматически из сессии, если не указана)</label>
                <input type="number" step="0.01" name="amount" id="payment-amount-input" value="${data ? data.amount : ''}" placeholder="Автоматически из сессии">
            </div>
            <div class="form-group">
                <label>Способ оплаты</label>
                <select name="method_id" required>
                    <option value="">Выберите способ</option>
                    ${methods.map(m => `<option value="${m.id}" ${data && data.method_id === m.id ? 'selected' : ''}>${m.name}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Время</label>
                <input type="datetime-local" name="time" value="${time}" required>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-success">Сохранить</button>
                <button type="button" class="btn btn-secondary" onclick="hideForm('payments')">Отмена</button>
            </div>
        </form>
    `;
}

function updatePaymentAmount() {
    const select = document.getElementById('payment-session-select');
    const input = document.getElementById('payment-amount-input');
    if (select && input && select.value) {
        const option = select.options[select.selectedIndex];
        const cost = option.getAttribute('data-cost');
        if (cost && !input.value) {
            input.value = cost;
        }
    }
}

async function calculateSessionCost() {
    const timeInInput = document.querySelector('input[name="time_in"]');
    const timeOutInput = document.getElementById('session-time-out');
    const tariffSelect = document.querySelector('select[name="tariff_id"]');
    const costInput = document.getElementById('session-total-cost');
    
    if (!timeInInput || !timeOutInput || !tariffSelect || !costInput) {
        return;
    }
    
    const timeIn = timeInInput.value;
    const timeOut = timeOutInput.value;
    const tariffId = tariffSelect.value;
    
    if (!timeIn || !timeOut || !tariffId) {
        return;
    }
    
    try {
        const tariffs = await fetch(`${API_BASE}/tariffs`).then(r => r.json());
        const tariff = tariffs.find(t => t.id === parseInt(tariffId));
        
        if (!tariff) {
            return;
        }
        const start = new Date(timeIn);
        const end = new Date(timeOut);
        
        if (end <= start) {
            costInput.value = '';
            return;
        }
        
        const diffMs = end - start;
        const diffHours = diffMs / (1000 * 60 * 60);
        const hoursRounded = Math.ceil(diffHours);
        const cost = hoursRounded * parseFloat(tariff.price_per_hour);
        
        costInput.value = cost.toFixed(2);
    } catch (error) {
        console.error('Ошибка расчета стоимости:', error);
    }
}
async function saveItem(event, sectionName, id) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (key === 'time_in' || key === 'time_out' || key === 'time') {
            if (value) {
                data[key] = new Date(value).toISOString();
            }
        } else if (key === 'type_id' || key === 'client_id' || key === 'space_id' || key === 'tariff_id' || key === 'vehicle_id' || key === 'session_id' || key === 'method_id') {
            data[key] = parseInt(value);
        } else if (key === 'price_per_hour' || key === 'price_per_day' || key === 'amount' || key === 'total_cost') {
            if (key === 'amount' && sectionName === 'payments' && !value) {
                continue;
            }
            if (key === 'total_cost' && sectionName === 'sessions' && !value) {
                continue;
            }
            if (value) {
                data[key] = parseFloat(value);
            }
        } else {
            data[key] = value;
        }
    }
    
    try {
        const endpoint = getEndpoint(sectionName);
        let response;
        
        if (id) {
            response = await fetch(`${API_BASE}${endpoint}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        
        if (response.ok) {
            showNotification(id ? 'Данные обновлены' : 'Данные созданы', 'success');
            hideForm(sectionName);
            loadData(sectionName);
            if (sectionName === 'sessions' || sectionName === 'payments') {
                const reportsSection = document.getElementById('reports');
                if (reportsSection && reportsSection.classList.contains('active')) {
                    loadDashboard();
                }
            }
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Ошибка при сохранении', 'error');
        }
    } catch (error) {
        showNotification('Ошибка при сохранении данных', 'error');
        console.error(error);
    }
}
async function deleteItem(sectionName, id) {
    if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
        return;
    }
    
    try {
        const endpoint = getEndpoint(sectionName);
        const response = await fetch(`${API_BASE}${endpoint}/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Запись удалена', 'success');
            loadData(sectionName);
        } else {
            showNotification('Ошибка при удалении', 'error');
        }
    } catch (error) {
        showNotification('Ошибка при удалении данных', 'error');
        console.error(error);
    }
}
function getEndpoint(sectionName) {
    const endpoints = {
        'clients': '/clients',
        'vehicles': '/vehicles',
        'parking-spaces': '/parking-spaces',
        'tariffs': '/tariffs',
        'sessions': '/parking-sessions',
        'payments': '/payments'
    };
    return endpoints[sectionName];
}
function hideForm(sectionName) {
    const formContainer = document.getElementById(`${sectionName}-form-container`);
    formContainer.classList.add('hidden');
    formContainer.innerHTML = '';
}
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.remove('hidden');
    
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

let revenueChart = null;
let sessionsChart = null;
async function loadDashboard() {
    try {
        const period = document.getElementById('period-select').value;
        const response = await fetch(`${API_BASE}/reports/dashboard?period=${period}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Ошибка ответа:', response.status, errorText);
            showNotification(`Ошибка при загрузке дашборда: ${response.status}`, 'error');
            return;
        }
        
        const data = await response.json();

        document.getElementById('total-revenue').textContent = formatCurrency(data.total_revenue || 0);
        document.getElementById('total-sessions').textContent = data.total_sessions || 0;
        document.getElementById('average-check').textContent = formatCurrency(data.average_check || 0);
        document.getElementById('active-sessions').textContent = data.active_sessions || 0;
        document.getElementById('free-spaces').textContent = data.free_spaces || 0;
        updateRevenueChart(data.revenue_by_period || []);
        updateSessionsChart(data.sessions_by_period || []);
    } catch (error) {
        showNotification('Ошибка при загрузке дашборда', 'error');
        console.error('Ошибка загрузки дашборда:', error);
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
    }).format(value);
}

function updateRevenueChart(data) {
    const ctx = document.getElementById('revenue-chart');
    if (!ctx) return;
    
    const labels = data.map(item => {
        if (!item.period) return '';
        try {
            const date = new Date(item.period);
            if (isNaN(date.getTime())) return item.period;
            return date.toLocaleDateString('ru-RU');
        } catch (e) {
            return item.period;
        }
    });
    const revenues = data.map(item => item.revenue || 0);
    
    if (revenueChart) {
        revenueChart.data.labels = labels;
        revenueChart.data.datasets[0].data = revenues;
        revenueChart.update('none');
    } else {
        revenueChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Выручка (₽)',
                    data: revenues,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                animation: {
                    duration: 0
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString('ru-RU') + ' ₽';
                            }
                        }
                    }
                }
            }
        });
    }
}

function updateSessionsChart(data) {
    const ctx = document.getElementById('sessions-chart');
    if (!ctx) return;
    
    const labels = data.map(item => {
        if (!item.period) return '';
        try {
            const date = new Date(item.period);
            if (isNaN(date.getTime())) return item.period;
            return date.toLocaleDateString('ru-RU');
        } catch (e) {
            return item.period;
        }
    });
    const counts = data.map(item => item.count || 0);
    
    if (sessionsChart) {
        sessionsChart.data.labels = labels;
        sessionsChart.data.datasets[0].data = counts;
        sessionsChart.update('none');
    } else {
        sessionsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Количество сессий',
                    data: counts,
                    borderColor: '#27ae60',
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                animation: {
                    duration: 0
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
}
document.addEventListener('DOMContentLoaded', () => {
    loadData('clients');
});

