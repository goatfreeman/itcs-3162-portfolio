(() => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  if (!toggle || !nav) return;

  const setOpen = (isOpen) => {
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    toggle.textContent = isOpen ? 'Close' : 'Menu';
    nav.classList.toggle('is-open', isOpen);
  };

  const close = () => setOpen(false);

  toggle.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    setOpen(!isOpen);
  });

  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) close();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') close();
  });

  const viewer = document.querySelector('[data-image-viewer]');
  const viewerImage = viewer?.querySelector('[data-viewer-image]');
  const viewerCaption = viewer?.querySelector('[data-viewer-caption]');
  const viewerClose = viewer?.querySelector('[data-viewer-close]');
  let returnFocus = null;

  if (viewer && viewerImage && viewerCaption && viewerClose && typeof viewer.showModal === 'function') {
    document.addEventListener('click', (event) => {
      const trigger = event.target.closest('[data-expand-image]');
      if (!trigger) return;
      returnFocus = trigger;
      viewerImage.src = trigger.dataset.image;
      viewerImage.alt = trigger.dataset.alt || '';
      viewerCaption.textContent = trigger.dataset.caption || trigger.dataset.alt || '';
      viewer.showModal();
    });

    viewerClose.addEventListener('click', () => viewer.close());
    viewer.addEventListener('click', (event) => {
      if (event.target === viewer) viewer.close();
    });
    viewer.addEventListener('close', () => {
      if (returnFocus?.isConnected) returnFocus.focus();
      returnFocus = null;
    });
  }
})();
