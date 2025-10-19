(function () {
    const overlay = document.querySelector('.selector-overlay');
    const cards = document.querySelectorAll('.design-card');
    const sections = document.querySelectorAll('.design');
    const openSelector = document.querySelector('.open-selector');

    function setActiveDesign(designId) {
        sections.forEach((section) => {
            const isTarget = section.dataset.design === designId;
            section.toggleAttribute('hidden', !isTarget);
            section.classList.toggle('is-active', isTarget);
        });
    }

    function closeOverlay() {
        overlay.classList.add('is-hidden');
        overlay.setAttribute('aria-hidden', 'true');
        openSelector.focus();
    }

    cards.forEach((card) => {
        const designId = card.dataset.target;
        function activate() {
            setActiveDesign(designId);
            closeOverlay();
        }

        card.addEventListener('click', activate);
        card.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                activate();
            }
        });
    });

    openSelector.addEventListener('click', () => {
        overlay.classList.remove('is-hidden');
        overlay.removeAttribute('aria-hidden');
        const firstCard = overlay.querySelector('.design-card');
        if (firstCard) {
            firstCard.focus();
        }
    });

    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !overlay.classList.contains('is-hidden')) {
            closeOverlay();
        }
    });
})();
