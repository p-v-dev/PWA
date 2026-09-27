import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url));
const output = path.join(root, 'dist');
const variables = [
  'CONTACT_WHATSAPP_NUMBER',
  'CONTACT_WHATSAPP_MESSAGE',
  'CONTACT_INSTAGRAM',
  'CONTACT_PHONE',
  'CONTACT_EMAIL',
  'CONTACT_BUSINESS_HOURS',
  'CONTACT_MAPS_URL',
  'SITE_URL',
];

function parseEnv(source) {
  return Object.fromEntries(
    source
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith('#') && line.includes('='))
      .map((line) => {
        const separator = line.indexOf('=');
        const key = line.slice(0, separator).trim();
        let value = line.slice(separator + 1).trim();
        if (/^(['"]).*\1$/.test(value)) value = value.slice(1, -1);
        return [key, value];
      }),
  );
}

let fileEnv = {};
try {
  fileEnv = parseEnv(await readFile(path.join(root, '.env'), 'utf8'));
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}

const env = Object.fromEntries(
  variables.map((name) => [name, process.env[name] ?? fileEnv[name] ?? '']),
);
const whatsappNumber = env.CONTACT_WHATSAPP_NUMBER.replace(/\D/g, '');
const phoneNumber = env.CONTACT_PHONE.replace(/\D/g, '');
const instagram = env.CONTACT_INSTAGRAM.replace(/^@/, '');
const siteUrl = (env.SITE_URL || 'https://p-v-dev.github.io/PWA/').replace(/\/+$/, '') + '/';

if (!/^55\d{10,11}$/.test(whatsappNumber)) {
  throw new Error('CONTACT_WHATSAPP_NUMBER deve conter 55, DDD e número, somente com dígitos.');
}
if (env.CONTACT_EMAIL && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(env.CONTACT_EMAIL)) {
  throw new Error('CONTACT_EMAIL inválido.');
}
if (env.CONTACT_MAPS_URL) {
  const mapsUrl = new URL(env.CONTACT_MAPS_URL);
  if (mapsUrl.protocol !== 'https:') throw new Error('CONTACT_MAPS_URL deve usar HTTPS.');
}
if (new URL(siteUrl).protocol !== 'https:') {
  throw new Error('SITE_URL deve usar HTTPS.');
}

const message = env.CONTACT_WHATSAPP_MESSAGE || 'Olá, gostaria de solicitar um orçamento.';
const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
const config = {
  whatsappUrl,
  instagramLabel: instagram ? `@${instagram}` : '',
  instagramUrl: instagram ? `https://www.instagram.com/${instagram}/` : '',
  phoneLabel: env.CONTACT_PHONE,
  phoneUrl: phoneNumber ? `tel:${phoneNumber}` : '',
  emailLabel: env.CONTACT_EMAIL,
  emailUrl: env.CONTACT_EMAIL ? `mailto:${env.CONTACT_EMAIL}` : '',
  businessHours: env.CONTACT_BUSINESS_HOURS,
  mapsUrl: env.CONTACT_MAPS_URL,
};

await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
for (const entry of ['index.html', 'styles.css', 'script.js', 'assets', 'robots.txt', 'sitemap.xml', 'llms.txt']) {
  await cp(path.join(root, entry), path.join(output, entry), { recursive: true });
}
for (const filename of ['robots.txt', 'sitemap.xml', 'llms.txt']) {
  const filePath = path.join(output, filename);
  const content = await readFile(filePath, 'utf8');
  await writeFile(
    filePath,
    content
      .replace(/^# Substitua SEU_DOMINIO_AQUI.*\r?\n/gm, '')
      .replace(/^<!-- Substitua SEU_DOMINIO_AQUI.*-->\r?\n/gm, '')
      .replaceAll('https://SEU_DOMINIO_AQUI/', siteUrl)
      .replace('INFORMAÇÃO A PREENCHER: link oficial do WhatsApp', whatsappUrl),
  );
}
await writeFile(
  path.join(output, 'contact-config.js'),
  `window.PWA_CONTACT = ${JSON.stringify(config, null, 2).replaceAll('<', '\\u003c')};\n`,
);

console.log('Site gerado em dist/.');
