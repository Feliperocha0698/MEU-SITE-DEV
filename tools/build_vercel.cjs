const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const output = path.join(root, 'dist');
const files = [
  'index.html', 'sobre-mim.html', 'portfolio.html', 'servicos.html', 'contato.html',
  'en/index.html', 'en/about.html', 'en/portfolio.html', 'en/services.html', 'en/contact.html',
  'es/index.html', 'es/sobre-mi.html', 'es/portafolio.html', 'es/servicios.html', 'es/contacto.html',
  'assets/css/home.css', 'assets/css/site.css',
  'assets/icons/br.svg', 'assets/icons/us.svg', 'assets/icons/es.svg', 'assets/icons/felipe-code.svg',
  'img/minha-foto.png', 'img/FORMULARIO-1.png', 'img/LISTA-DE-TAREFAS.png',
  'img/RELOGIO-DIGITAL.png', 'img/icons/whatsapp.png',
  'js/home.js', 'js/contact.js', 'js/contact-config.js',
  'robots.txt', 'sitemap.xml'
];

// Reject unexpected output entries so local files cannot be deployed by mistake.
const allowed = new Set();
for (const file of files) {
  for (let entry = file; entry !== '.'; entry = path.posix.dirname(entry)) {
    allowed.add(entry);
  }
}
function verifyOutput(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    const relative = path.relative(output, fullPath).split(path.sep).join('/');
    if (!allowed.has(relative) || entry.isSymbolicLink()) {
      throw new Error(`Unexpected preview output entry: ${relative}`);
    }
    if (entry.isDirectory()) verifyOutput(fullPath);
  }
}
fs.mkdirSync(output, { recursive: true });
if (fs.realpathSync(output) !== path.join(fs.realpathSync(root), 'dist')) {
  throw new Error('Preview output must be the dist directory inside this project.');
}
verifyOutput(output);
for (const file of files) {
  const target = path.join(output, file);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(path.join(root, file), target);
}
console.log(`Prepared ${files.length} public files for Vercel.`);
