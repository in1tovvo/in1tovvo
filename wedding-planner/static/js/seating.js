// 桌席安排脚本
(function() {
    'use strict';
    
    const floorPlan = document.getElementById('floorPlan');
    
    // 配置
    const config = {
        table: {
            diameter: 120,
            gap: 40
        },
        seat: {
            diameter: 28,
            offsetFactor: 0.85
        }
    };
    
    // 初始化
    function init() {
        if (!floorPlan) return;
        
        // 使用全局数据
        if (window.tablesData && window.tablesData.length > 0) {
            renderTables();
        } else {
            floorPlan.innerHTML = '<div class="text-center py-5">暂无桌席</div>';
        }
        bindEvents();
    }
    
    // 渲染桌席
    function renderTables() {
        if (!window.tablesData || window.tablesData.length === 0) return;
        
        floorPlan.innerHTML = '';
        
        const containerWidth = floorPlan.clientWidth || 800;
        const tableSize = config.table.diameter + config.table.gap;
        const cols = Math.max(1, Math.floor((containerWidth - 100) / tableSize));
        const startX = (containerWidth - (cols * tableSize)) / 2 + tableSize / 2;
        
        window.tablesData.forEach((table, index) => {
            const col = index % cols;
            const row = Math.floor(index / cols);
            const x = startX + col * tableSize;
            const y = 50 + row * tableSize;
            
            createTableElement(table, x, y);
        });
    }
    
    // 创建桌子元素
    function createTableElement(table, x, y) {
        const tableEl = document.createElement('div');
        tableEl.className = 'table-shape';
        tableEl.dataset.tableId = table.id;
        tableEl.dataset.tableNumber = table.table_number;
        tableEl.style.left = x + 'px';
        tableEl.style.top = y + 'px';
        tableEl.style.width = config.table.diameter + 'px';
        tableEl.style.height = config.table.diameter + 'px';
        tableEl.style.marginLeft = -(config.table.diameter / 2) + 'px';
        tableEl.style.marginTop = -(config.table.diameter / 2) + 'px';
        tableEl.style.zIndex = '20';
        
        tableEl.innerHTML = `
            <div class="table-number">桌${table.table_number}</div>
            <div class="table-name">${table.table_name || ''}</div>
            <div class="occupied-badge">
                <span class="occupied-count">0</span>/<span class="total-count">${table.capacity}</span>
            </div>
            <button class="btn btn-sm btn-outline-danger position-absolute top-0 end-0 translate-middle clear-table" 
                    style="display:none;font-size:0.7rem;padding:2px 8px; z-index:30;">清空</button>
            <i class="bi bi-flower1 position-absolute top-0 start-0 translate-middle" style="font-size:1rem;color:var(--wedding-gold);z-index:5;top:-8px;left:-8px;"></i>
            <i class="bi bi-flower2 position-absolute top-0 end-0 translate-middle" style="font-size:1rem;color:var(--wedding-rose);z-index:5;top:-8px;right:-8px;transform:translate(50%,-50%) rotate(45deg);"></i>
        `;
        
        // 悬停显示清空按钮
        tableEl.addEventListener('mouseenter', function() {
            this.querySelector('.clear-table').style.display = 'block';
        });
        tableEl.addEventListener('mouseleave', function() {
            this.querySelector('.clear-table').style.display = 'none';
        });
        
        // 清空整桌
        tableEl.querySelector('.clear-table').addEventListener('click', function(e) {
            e.stopPropagation();
            if (confirm('清空该桌所有座位？')) {
                clearTable(table.id);
            }
        });
        
        floorPlan.appendChild(tableEl);
        
        // 渲染座位
        const tableGuests = window.seatingData[table.table_number.toString()] || [];
        renderSeats(tableEl, table, tableGuests);
    }
    
    // 渲染座位
    function renderSeats(tableEl, table, guests) {
        const occupiedCount = guests.length;
        tableEl.querySelector('.occupied-count').textContent = occupiedCount;
        
        // 显示桌子的完整容量
        const numSeats = table.capacity;
        const radius = config.table.diameter / 2;
        const seatOffset = radius * config.seat.offsetFactor;
        const angleStep = (2 * Math.PI) / numSeats;
        
        for (let i = 0; i < numSeats; i++) {
            const seatNum = i + 1;
            const angle = i * angleStep - Math.PI / 2;
            
            // 座位相对于桌子左上角的坐标
            // 从桌子中心(radius, radius)出发，偏移seatOffset，再减去座位半径居中
            const x = radius + seatOffset * Math.cos(angle) - config.seat.diameter / 2;
            const y = radius + seatOffset * Math.sin(angle) - config.seat.diameter / 2;
            
            const seatEl = document.createElement('div');
            seatEl.className = 'seat-spot';
            seatEl.dataset.seatNumber = seatNum;
            seatEl.dataset.tableId = table.id;
            seatEl.dataset.tableNumber = table.table_number;
            seatEl.style.left = x + 'px';
            seatEl.style.top = y + 'px';
            seatEl.style.width = config.seat.diameter + 'px';
            seatEl.style.height = config.seat.diameter + 'px';
            seatEl.style.zIndex = '25';
            seatEl.title = `座位 ${seatNum}`;
            
            const guest = guests.find(g => g.seat_number === seatNum);
            if (guest) {
                seatEl.classList.add('occupied');
                seatEl.title = `${guest.name} (${guest.relationship})`;
                const displayName = guest.name.length > 3 ? guest.name.substring(0,3) : guest.name;
                seatEl.innerHTML = `
                    <span class="guest-name">${escapeHtml(displayName)}</span>
                    <button class="remove-seat" data-guest-id="${guest.id}" style="z-index:30;">×</button>
                `;
            } else {
                seatEl.textContent = seatNum;
            }
            
            tableEl.appendChild(seatEl);
        }
    }
    
    // HTML转义
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // 绑定事件
    function bindEvents() {
        // 添加桌席表单
        const addTableForm = document.getElementById('addTableForm');
        if (addTableForm) {
            addTableForm.addEventListener('submit', function(e) {
                e.preventDefault();
                addTable();
            });
        }
        
        // 点击空座位安排宾客
        floorPlan.addEventListener('click', function(e) {
            if (e.target.classList.contains('seat-spot') && !e.target.classList.contains('occupied')) {
                const tableId = e.target.dataset.tableId;
                const tableNumber = e.target.dataset.tableNumber;
                const seatNumber = e.target.dataset.seatNumber;
                showGuestSelector(tableId, tableNumber, seatNumber);
            }
        });
        
        // 点击移除座位按钮
        floorPlan.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-seat')) {
                e.stopPropagation();
                const guestId = e.target.dataset.guestId;
                const tableId = e.target.closest('.table-shape').dataset.tableId;
                const seatNumber = e.target.dataset.seatNumber || e.target.closest('.seat-spot').dataset.seatNumber;
                removeGuestFromSeat(guestId, tableId, seatNumber);
            }
        });
        
        // 窗口大小变化
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(renderTables, 300);
        });
    }
    
    // 添加桌席
    window.addTable = function() {
        const form = document.getElementById('addTableForm');
        const formData = new FormData(form);
        const data = {
            table_number: parseInt(formData.get('table_number')),
            table_name: formData.get('table_name') || '',
            capacity: parseInt(formData.get('capacity')),
            shape: 'round'
        };
        
        fetch('/seating/api/table', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(r => r.json())
        .then(res => {
            if (res.success) {
                // 重新加载页面数据
                location.reload();
            } else {
                alert('添加失败: ' + (res.error || '未知错误'));
            }
        })
        .catch(err => {
            alert('网络错误');
            console.error(err);
        });
    };
    
    // 显示宾客选择器
    window.showGuestSelector = function(tableId, tableNumber, seatNumber) {
        const availableGuests = window.allGuests.filter(g => !g.table_number && !g.seat_number && g.id);
        
        if (availableGuests.length === 0) {
            alert('暂无未安排座位的宾客');
            return;
        }
        
        availableGuests.sort((a, b) => {
            const order = { 'bride': 1, 'groom': 2, 'both': 3 };
            return (order[a.side] || 4) - (order[b.side] || 4);
        });
        
        const modalHtml = `
            <div class="modal fade show" id="guestSelectModal" tabindex="-1" style="display:block;background:rgba(0,0,0,0.5)">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">选择宾客 - 桌${tableNumber} 座位${seatNumber}</h5>
                            <button type="button" class="btn-close" onclick="closeGuestSelect()"></button>
                        </div>
                        <div class="modal-body">
                            <div class="list-group">
                                ${availableGuests.map(guest => `
                                    <button type="button" class="list-group-item list-group-item-action" 
                                            onclick="assignGuestToSeat(${guest.id}, ${tableId}, ${tableNumber}, ${seatNumber})">
                                        <div class="d-flex justify-content-between">
                                            <span>${escapeHtml(guest.name)}</span>
                                            <small class="text-muted">${guest.relationship} · ${guest.side === 'bride' ? '女方' : guest.side === 'groom' ? '男方' : '双方'}</small>
                                        </div>
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHtml;
        document.body.appendChild(modalContainer.firstElementChild);
        
        document.getElementById('guestSelectModal').addEventListener('click', function(e) {
            if (e.target === this) closeGuestSelect();
        });
    };
    
    window.closeGuestSelect = function() {
        const modal = document.getElementById('guestSelectModal');
        if (modal) modal.remove();
    };
    
    window.assignGuestToSeat = function(guestId, tableId, tableNumber, seatNumber) {
        fetch('/seating/api/arrange', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ guest_id: guestId, table_id: tableId, table_number: tableNumber, seat_number: seatNumber })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success || data.status === 'success') {
                closeGuestSelect();
                location.reload();
            } else {
                alert('分配失败: ' + (data.error || data.message || '未知错误'));
            }
        })
        .catch(() => alert('网络错误'));
    };
    
    window.removeGuestFromSeat = function(guestId, tableId, seatNumber) {
        fetch(`/seating/api/remove/${guestId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_id: tableId, seat_number: seatNumber })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success || data.status === 'success') location.reload();
            else alert('移除失败');
        })
        .catch(() => alert('网络错误'));
    };
    
    window.clearTable = function(tableId) {
        fetch('/seating/clear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_id: tableId })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) location.reload();
            else alert('清空失败');
        })
        .catch(() => alert('网络错误'));
    };
    
    // 初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
