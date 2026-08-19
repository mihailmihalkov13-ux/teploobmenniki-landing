document.addEventListener('DOMContentLoaded', () => {

  // Год в футере
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---------- Модальное окно ----------
  const overlay = document.getElementById('modalOverlay');
  const openButtons = document.querySelectorAll('[data-open-modal]');
  const closeBtn = document.getElementById('modalClose');

  const openModal = () => {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  const closeModal = () => {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  };

  openButtons.forEach(btn => btn.addEventListener('click', openModal));
  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });

  // ---------- Мобильное меню ----------
  const burger = document.getElementById('burgerBtn');
  const nav = document.getElementById('mainNav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      nav.classList.toggle('nav-open');
      burger.classList.toggle('active');
    });
    nav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => nav.classList.remove('nav-open'));
    });
  }

  // ---------- Отзывы: простая карусель ----------
  const track = document.getElementById('reviewsTrack');
  const prevBtn = document.getElementById('reviewPrev');
  const nextBtn = document.getElementById('reviewNext');
  if (track && prevBtn && nextBtn) {
    let index = 0;
    const cards = track.querySelectorAll('.review-card');
    const visibleCount = () => window.innerWidth <= 1024 ? 1 : 3;

    const update = () => {
      const cardWidth = cards[0].getBoundingClientRect().width + 24;
      track.style.transform = `translateX(-${index * cardWidth}px)`;
    };

    nextBtn.addEventListener('click', () => {
      const max = cards.length - visibleCount();
      index = Math.min(index + 1, Math.max(max, 0));
      update();
    });
    prevBtn.addEventListener('click', () => {
      index = Math.max(index - 1, 0);
      update();
    });
    window.addEventListener('resize', () => { index = 0; update(); });
  }

  // ---------- Формы: валидация и отправка заявки на бэкенд ----------
  const forms = [document.getElementById('contactForm'), document.getElementById('modalForm')];
  forms.forEach(form => {
    if (!form) return;
    const phoneInput = form.elements.phone;
    const consentInput = form.querySelector('.consent input[type="checkbox"]');

    const validatePhone = () => {
      if (!phoneInput) return;
      const digits = (phoneInput.value.match(/\d/g) || []).length;
      phoneInput.setCustomValidity(digits >= 10 ? '' : 'Введите корректный номер телефона (минимум 10 цифр)');
    };
    const validateConsent = () => {
      if (!consentInput) return;
      consentInput.setCustomValidity(consentInput.checked ? '' : 'Чтобы продолжить, дайте согласие на обработку персональных данных');
    };

    phoneInput?.addEventListener('input', validatePhone);
    consentInput?.addEventListener('change', validateConsent);

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      validatePhone();
      validateConsent();
      if (!form.reportValidity()) return;

      const submitBtn = form.querySelector('button[type="submit"]');
      const payload = {
        name: form.elements.name?.value || '',
        phone: phoneInput?.value || '',
        message: form.elements.message?.value || '',
        consent: consentInput?.checked || false
      };

      if (submitBtn) submitBtn.disabled = true;
      try {
        const res = await fetch('/api/lead', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('request failed');

        form.reset();
        alert('Спасибо! Заявка отправлена, мы свяжемся с вами в ближайшее время.');
        closeModal();
      } catch (err) {
        alert('Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам напрямую.');
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  });

});
