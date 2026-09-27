const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('.site-nav');
const contact = window.PWA_CONTACT ?? {};

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  navigation.classList.toggle('is-open', !isOpen);
});

navigation?.addEventListener('click', () => {
  navigation.classList.remove('is-open');
  menuButton?.setAttribute('aria-expanded', 'false');
});

document.querySelectorAll('[data-contact-link="whatsapp"]').forEach((link) => {
  if (contact.whatsappUrl) link.href = contact.whatsappUrl;
});

const optionalContacts = {
  instagram: [contact.instagramUrl, contact.instagramLabel],
  phone: [contact.phoneUrl, contact.phoneLabel],
  email: [contact.emailUrl, contact.emailLabel],
  maps: [contact.mapsUrl, 'Ver localização no Google Maps'],
};

for (const [name, [url, label]] of Object.entries(optionalContacts)) {
  if (!url) continue;
  const field = document.querySelector(`[data-contact-field="${name}"]`);
  const link = field?.querySelector(`[data-contact-link="${name}"]`);
  if (field && link) {
    field.hidden = false;
    link.href = url;
    link.textContent = label;
  }
}

if (contact.businessHours) {
  const field = document.querySelector('[data-contact-field="businessHours"]');
  const label = field?.querySelector('[data-contact-label="businessHours"]');
  if (field && label) {
    field.hidden = false;
    label.textContent = contact.businessHours;
  }
}

document.querySelector('#year').textContent = new Date().getFullYear();
