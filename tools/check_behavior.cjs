/* Run with node tools/check_behavior.cjs. No network or submission is performed. */
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const shared = fs.readFileSync(path.join(root, 'js/home.js'), 'utf8');
const contact = fs.readFileSync(path.join(root, 'js/contact.js'), 'utf8');
const dataFor = code => JSON.parse(fs.readFileSync(path.join(root, 'assets/i18n', code + '.json'), 'utf8'));
let cases = 0;
function language({ languages, saved, explicit = '', lang = 'pt-BR', visited = false, storageThrows = false }) {
  const d = dataFor(lang);
  const routes = { 'pt-BR': 'contato.html', en: 'en/contact.html', es: 'es/contacto.html' };
  let redirected = null;
  const values = new Map(saved ? [['felipecode-language', saved]] : []);
  if (visited) values.set('felipecode-visited', '1');
  const store = { getItem(k) { if (storageThrows) throw Error('blocked'); return values.get(k) || null; }, setItem(k, v) { if (storageThrows) throw Error('blocked'); values.set(k, v); } };
  const document = { querySelector(s) { return s === '#site-data' ? { textContent: JSON.stringify({lang, routes, ui:d.ui, search:[]}) } : null; }, querySelectorAll() { return []; }, addEventListener() {} };
  const context = { document, navigator: { languages }, location: { search: explicit, href: 'https://example.test/contato.html' + explicit, hash: '#conteudo', replace(v) { redirected = v; } }, URL, URLSearchParams, window: { localStorage: store, sessionStorage: store } };
  vm.runInNewContext(shared, context);
  cases++;
  return redirected;
}
assert.match(language({ languages:['en-US'] }), /en\/contact.html#conteudo$/);
assert.match(language({ languages:['es-MX'] }), /es\/contacto.html#conteudo$/);
assert.equal(language({ languages:['pt-PT'] }), null);
assert.equal(language({ languages:['fr-FR'] }), null);
assert.match(language({ languages:['fr-FR','es-AR'] }), /es\/contacto.html/);
assert.match(language({ languages:['en-US'], saved:'es' }), /es\/contacto.html/);
assert.equal(language({ languages:['en-US'], explicit:'?lang=pt-BR' }), null);
assert.equal(language({ languages:['es'], lang:'en' }), null);
assert.equal(language({ languages:['en'], visited:true }), null);
assert.match(language({ languages:['en'], storageThrows:true }), /en\/contact.html/);

async function unconfiguredForm(code) {
  const d = dataFor(code);
  let submissions = 0;
  let listener;
  const nodes = new Map();
  function element(id, value = '') {
    const attributes = new Map();
    const el = { id, name: id === 'description' ? 'message' : id, value, textContent:'', validity:{valid:true}, disabled:true, checked:false,
      addEventListener() {}, setAttribute(k,v) { attributes.set(k,v); }, getAttribute(k) { return attributes.get(k); }, hasAttribute(k) { return attributes.has(k); }, removeAttribute(k) { attributes.delete(k); }, focus() { nodes.set('focused', id); } };
    nodes.set(id, el); return el;
  }
  for (const id of ['name','email','phone','service','description']) { element(id); element(id+'-error'); }
  const fields = nodes;
  for (const id of ['contact-submit','form-status','integration-notice','form-privacy','botcheck']) element(id);
  const fieldset = element('fieldset');
  const form = {
    querySelector() { return fieldset; },
    addEventListener(event, fn) { listener = fn; },
    setAttribute() {},
    removeAttribute() {}
  };
  nodes.set('contact-sidebar > p', element('direct-contact'));
  const document = { querySelector(selector) { if (selector === '#contact-form') return form; if (selector === '#site-data') return {textContent:JSON.stringify(d)}; return nodes.get(selector.slice(1)); }, getElementById(id) { return nodes.get(id); } };
  const context = { document, window: { FELIPECODE_CONTACT:{accessKey:'',enabled:false} }, URLSearchParams, location:{search:''}, fetch() { submissions++; throw Error('Network must not be used'); }, setTimeout, clearTimeout, AbortController };
  vm.runInNewContext(contact, context);
  assert.equal(fieldset.disabled, false);
  await listener({preventDefault(){}});
  assert.equal(nodes.get('focused'),'name');
  assert.equal(nodes.get('form-status').textContent,d.contact.invalid);
  for (const [id,value] of Object.entries({name:'Teste Local',email:'test@example.technology',phone:'+34 612 345 678',service:'0',description:'A local validation test with no outgoing request.'})) fields.get(id).value=value;
  await listener({preventDefault(){}});
  assert.equal(nodes.get('form-status').textContent,d.contact.validInactive);
  for (const value of ['+1 (202) 555-0123','+55 71 99999-9999','+44 7700 900123']) {
    fields.get('phone').value=value;
    await listener({preventDefault(){}});
    assert.equal(nodes.get('form-status').textContent,d.contact.validInactive);
    cases++;
  }
  for (const value of ['11999999999','+0000','+1234567890123456','+abc12345678']) {
    fields.get('phone').value=value;
    await listener({preventDefault(){}});
    assert.equal(nodes.get('phone-error').textContent,d.contact.phoneError);
    cases++;
  }
  assert.equal(submissions,0);
  cases+=3;

  // Exercise the transport contract with a local stub that always rejects.
  context.window.FELIPECODE_CONTACT = {
    accessKey: '00000000-0000-0000-0000-000000000000',
    enabled: true
  };
  let completeRequest;
  let requestBody;
  context.fetch = (url, options) => {
    assert.equal(url, 'https://api.web3forms.com/submit');
    assert.equal(options.method, 'POST');
    requestBody = JSON.parse(options.body);
    submissions++;
    return new Promise(resolve => { completeRequest = resolve; });
  };
  vm.runInNewContext(contact, context);
  fields.get('phone').value = '+34 612 345 678';
  const submit = () => listener({preventDefault(){}});
  fields.get('botcheck').checked = true;
  await submit();
  assert.equal(nodes.get('form-status').textContent, d.contact.spam);
  assert.equal(submissions, 0);
  fields.get('botcheck').checked = false;
  const inFlight = submit();
  assert.equal(fieldset.disabled, true);
  assert.equal(nodes.get('contact-submit').textContent, d.contact.sending);
  await submit();
  assert.equal(submissions, 1);
  assert.deepEqual(requestBody, {
    name: fields.get('name').value,
    email: fields.get('email').value,
    phone: fields.get('phone').value,
    service: d.contact.options[0],
    message: fields.get('description').value,
    access_key: context.window.FELIPECODE_CONTACT.accessKey,
    subject: 'Novo orçamento recebido - FelipeCode',
    from_name: 'Felipercode0698',
    replyto: fields.get('email').value,
    botcheck: false
  });
  completeRequest({ok:false, status:429, json:async () => ({success:false})});
  await inFlight;
  assert.equal(nodes.get('form-status').textContent, d.contact.failure);
  assert.equal(fieldset.disabled, false);
  assert.equal(fields.get('description').value, requestBody.message);
  cases+=5;
}
(async()=>{ for(const code of ['pt-BR','en','es']) await unconfiguredForm(code); console.log(`PASS: ${cases} behavior checks. Contact tests cover validation, localized payload, spam trap, pending state, duplicate blocking and error recovery. No network or simulated success.`); })().catch(error=>{console.error(error);process.exitCode=1;});
