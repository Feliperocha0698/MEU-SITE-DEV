/* Shared behavior for all static pages. Translation data is embedded in each HTML. */
(() => {
  'use strict';
  const dataElement = document.querySelector('#site-data');
  if (!dataElement) return;
  const data = JSON.parse(dataElement.textContent);
  const ui = data.ui;
  const read = (store, key) => { try { return window[store].getItem(key); } catch { return null; } };
  const write = (store, key, value) => { try { window[store].setItem(key, value); } catch { /* Storage can be disabled. */ } };
  const supported = ['pt-BR', 'en', 'es'];
  const explicit = new URLSearchParams(location.search).get('lang');
  if (supported.includes(explicit) && explicit === data.lang) write('localStorage', 'felipecode-language', explicit);
  document.querySelectorAll('[data-language]').forEach(link => {
    link.addEventListener('click', () => {
      write('localStorage', 'felipecode-language', link.dataset.language);
      write('sessionStorage', 'felipecode-visited', '1');
    });
  });
  // A language-specific URL wins. Only an initial Portuguese entry is auto-selected.
  // Static links and hreflang remain usable without JavaScript or browser storage.
  if (!read('sessionStorage', 'felipecode-visited') && data.lang === 'pt-BR' && !supported.includes(explicit)) {
    const saved = read('localStorage', 'felipecode-language');
    const detected = (navigator.languages || [navigator.language]).map(value => String(value).toLowerCase())
      .map(value => value.startsWith('pt') ? 'pt-BR' : value.startsWith('en') ? 'en' : value.startsWith('es') ? 'es' : null)
      .find(Boolean) || 'pt-BR';
    const choice = supported.includes(saved) ? saved : detected;
    write('sessionStorage', 'felipecode-visited', '1');
    if (choice !== data.lang) {
      const destination = new URL(data.routes[choice], location.href);
      destination.search = location.search;
      destination.hash = location.hash;
      location.replace(destination.href);
      return;
    }
  }
  write('sessionStorage', 'felipecode-visited', '1');
  const year = document.querySelector('#current-year');
  if (year) year.textContent = new Date().getFullYear();

  const picker = document.querySelector('.language-picker');
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && picker?.open) {
      picker.open = false;
      picker.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', event => {
    if (picker?.open && !picker.contains(event.target)) picker.open = false;
  });

  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const form = document.querySelector('#site-search');
  const input = document.querySelector('#search-input');
  const results = document.querySelector('#search-results');
  const status = document.querySelector('#search-status');
  if (form && input && results && status) {
    form.addEventListener('submit', event => {
      event.preventDefault();
      const query = normalize(input.value);
      results.replaceChildren();
      if (!query) { status.textContent = ui.searchEmpty; input.focus(); return; }
      const words = query.split(/\s+/);
      const matches = data.search.filter(page => words.every(word => normalize(page.title + ' ' + page.terms).includes(word)));
      for (const page of matches) {
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = page.url;
        link.textContent = page.title;
        item.append(link);
        results.append(item);
      }
      status.textContent = matches.length ? `${ui.searchFound} ${matches.length}.` : ui.searchNone;
    });
  }
  const filters = document.querySelector('.project-filters');
  if (filters) {
    filters.hidden = false;
    const cards = [...document.querySelectorAll('#project-grid [data-category]')];
    const count = document.querySelector('#filter-status');
    const empty = document.querySelector('#empty-projects');
    filters.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', () => {
        filters.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; });
        const visible = cards.filter(card => !card.hidden).length;
        count.textContent = `${ui.filterCount} ${visible}.`;
        empty.hidden = visible !== 0;
      });
    });
  }
})();
