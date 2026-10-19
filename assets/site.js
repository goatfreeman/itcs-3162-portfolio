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
  let previousScrollY = 0;
  let returnFocus = null;

  const restorePageScroll = () => {
    const root = document.documentElement;
    const previousBehavior = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto';
    window.scrollTo(0, previousScrollY);
    root.style.scrollBehavior = previousBehavior;
  };

  if (viewer && viewerImage && viewerCaption && viewerClose && typeof viewer.showModal === 'function') {
    document.addEventListener('click', (event) => {
      const trigger = event.target.closest('[data-expand-image]');
      if (!trigger) return;
      event.preventDefault();
      previousScrollY = window.scrollY;
      returnFocus = trigger;
      viewerImage.src = trigger.dataset.image;
      viewerImage.alt = trigger.dataset.alt || '';
      viewerCaption.textContent = trigger.dataset.caption || trigger.dataset.alt || '';
      viewer.showModal();
      viewer.focus({ preventScroll: true });
      restorePageScroll();
      window.requestAnimationFrame(restorePageScroll);
      window.setTimeout(restorePageScroll, 50);
    });

    const restoreFocus = () => {
      const focusTarget = returnFocus;
      returnFocus = null;
      window.setTimeout(() => {
        if (focusTarget?.isConnected) focusTarget.focus({ preventScroll: true });
        restorePageScroll();
      }, 0);
    };

    const closeViewer = () => {
      viewer.close();
      restoreFocus();
    };

    viewerClose.addEventListener('click', closeViewer);
    viewer.addEventListener('click', (event) => {
      if (event.target === viewer) closeViewer();
    });
    viewer.addEventListener('cancel', () => window.setTimeout(restoreFocus, 0));
    viewer.addEventListener('close', restorePageScroll);
  }
})();
