/**
 * AccessEvent — вспомогательный JavaScript.
 * Все уведомления ВИЗУАЛЬНЫЕ.
 */

/* ============================================================
   УВЕДОМЛЕНИЯ
   ============================================================ */
function showNotification(message, type = 'info') {
    const container = document.getElementById('notifications');
    if (!container) return;

    const notice = document.createElement('div');
    notice.className = 'notification notification-' + type;
    notice.setAttribute('role', 'status');
    notice.setAttribute('aria-live', 'polite');
    notice.textContent = message;
    container.appendChild(notice);

    setTimeout(() => {
        notice.classList.add('notification-out');
        setTimeout(() => notice.remove(), 1200);
    }, 4000);
}

/* ============================================================
   ВАЛИДАЦИЯ ФОРМ
   ============================================================ */
function setupFormValidation() {
    document.querySelectorAll('.validate-me').forEach(form => {
        form.addEventListener('submit', e => {
            const required = form.querySelectorAll('[required]');
            let valid = true;

            required.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#f85149';
                    field.style.boxShadow = '0 0 0 4px rgba(248, 81, 73, 0.15)';
                    field.setAttribute('aria-invalid', 'true');
                } else {
                    field.style.borderColor = '';
                    field.style.boxShadow = '';
                    field.removeAttribute('aria-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                showNotification('Заполните обязательные поля', 'error');
            }
        });
    });
}

/* ============================================================
   КУРСОРНЫЙ ТРЕКИНГ + 3D-НАКЛОН
   Устанавливает --mx/--my (для подсветки) и
   --rx/--ry (для 3D-наклона в сторону курсора).
   ============================================================ */
function setupCursorTracking() {
    const selectors = [
        '.btn',
        '.feature-card',
        '.event-card',
        '.profile-card',
        '.nav-link',
        '.hero',
        '.registrations-list li',
        '.badge',
        '.form-container'
    ].join(', ');

    document.querySelectorAll(selectors).forEach(el => {
        el.addEventListener('mousemove', e => {
            const rect = el.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;   // 0..1
            const y = (e.clientY - rect.top)  / rect.height;  // 0..1

            // Позиция курсора в процентах — для радиального градиента
            el.style.setProperty('--mx', (x * 100) + '%');
            el.style.setProperty('--my', (y * 100) + '%');

            // Угол наклона: центр = 0°, края = ±максимум
            const maxTilt = 6;  // градусов
            const rx = ((0.5 - y) * maxTilt).toFixed(2) + 'deg';  // вверх/вниз
            const ry = ((x - 0.5) * maxTilt).toFixed(2) + 'deg';  // влево/вправо

            el.style.setProperty('--rx', rx);
            el.style.setProperty('--ry', ry);
        });

        el.addEventListener('mouseleave', () => {
            el.style.setProperty('--mx', '50%');
            el.style.setProperty('--my', '50%');
            el.style.setProperty('--rx', '0deg');
            el.style.setProperty('--ry', '0deg');
        });
    });
}

/* ============================================================
   SCROLL REVEAL
   ============================================================ */
function setupScrollReveal() {
    const targets = document.querySelectorAll(
        '.event-card, .feature-card, .registrations-list li'
    );
    if (!('IntersectionObserver' in window)) return;

    targets.forEach(t => t.classList.add('reveal'));

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

    targets.forEach(t => observer.observe(t));
}

/* ============================================================
   ЗАПУСК
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    setupFormValidation();
    setupCursorTracking();
    setupScrollReveal();
});

if (typeof module !== 'undefined') {
    module.exports = { showNotification, setupFormValidation };
}