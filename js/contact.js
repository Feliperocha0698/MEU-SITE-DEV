/* No submission occurs unless Web3Forms is explicitly configured and enabled. */
(() => {
  'use strict';
  const form = document.querySelector('#contact-form');
  const dataElement = document.querySelector('#site-data');
  if (!form || !dataElement) return;
  const data = JSON.parse(dataElement.textContent);
  const text = data.contact;
  const config = window.FELIPECODE_CONTACT || {};
  const configured = config.enabled === true && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(config.accessKey || '');
  const fieldset = form.querySelector('fieldset');
  const button = document.querySelector('#contact-submit');
  const status = document.querySelector('#form-status');
  const fields = ['name', 'email', 'phone', 'service', 'description'].map(id => document.getElementById(id));
  let busy = false;
  fieldset.disabled = false;
  const requested = new URLSearchParams(location.search).get('service');
  if (/^[0-5]$/.test(requested || '')) document.querySelector('#service').value = requested;
  if (configured) {
    button.textContent = text.send;
    document.querySelector('#integration-notice').textContent = text.ready;
    document.querySelector('#form-privacy').textContent = text.privacyActive;
    document.querySelector('.contact-sidebar > p').textContent = text.directActive;
  }
  function errorFor(field) {
    const value = field.value.trim();
    if (field.id === 'name' && (value.split(/\s+/).length < 2 || value.length > 120)) return text.nameError;
    if (field.id === 'email' && (!value || !field.validity.valid)) return text.emailError;
    if (field.id === 'phone') {
      const digits = value.replace(/\D/g, '');
      if (!/^\+[1-9][\d\s().-]*$/.test(value) || digits.length < 7 || digits.length > 15) return text.phoneError;
    }
    if (field.id === 'service' && !/^[0-5]$/.test(value)) return text.serviceError;
    if (field.id === 'description' && (value.length < 20 || value.length > 5000)) return text.descriptionError;
    return '';
  }
  function validate(field) {
    const error = errorFor(field);
    document.getElementById(field.id + '-error').textContent = error;
    if (error) field.setAttribute('aria-invalid', 'true');
    else field.removeAttribute('aria-invalid');
    return !error;
  }
  fields.forEach(field => field.addEventListener('input', () => {
    if (field.hasAttribute('aria-invalid')) validate(field);
  }));
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    status.textContent = '';
    const valid = fields.map(validate).every(Boolean);
    if (!valid) {
      status.textContent = text.invalid;
      fields.find(field => field.getAttribute('aria-invalid') === 'true').focus();
      return;
    }
    if (document.querySelector('#botcheck').checked) { status.textContent = text.spam; return; }
    if (!configured) {
      status.textContent = text.validInactive;
      status.focus();
      return;
    }
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    const values = Object.fromEntries(fields.map(field => [field.name, field.value.trim()]));
    values.service = text.options[Number(values.service)];
    const payload = {
      ...values,
      access_key: config.accessKey,
      subject: 'Novo orçamento recebido - FelipeCode',
      from_name: 'Felipercode0698',
      replyto: values.email,
      botcheck: false
    };
    busy = true;
    fieldset.disabled = true;
    form.setAttribute('aria-busy', 'true');
    button.textContent = text.sending;
    status.textContent = text.sending;
    try {
      const response = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal
      });
      const result = await response.json();
      if (!response.ok || result.success !== true) throw new Error('Unconfirmed submission');
      status.textContent = text.success;
      form.reset();
    } catch {
      status.textContent = text.failure;
    } finally {
      clearTimeout(timeout);
      busy = false;
      fieldset.disabled = false;
      form.removeAttribute('aria-busy');
      button.textContent = text.send;
      status.focus();
    }
  });
})();
