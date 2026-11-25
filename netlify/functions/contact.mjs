import nodemailer from 'nodemailer';
import crypto from 'node:crypto';
import { getStore } from '@netlify/blobs';

// Keep these lists in sync with LISTS in public/assets/app.js
const SERVICES = ['Website design & development', 'Graphic design & branding', 'Multimedia & video editing', 'Computer & IT support', 'CCTV & security systems', 'Networking services', 'Digital marketing', 'Software & application development', 'Additional services', 'Not sure yet'];
const SURVEY = ['CCTV installation', 'Wi-Fi / network setup', 'Access control', 'Other'];
const ISSUES = ['Computer or laptop', 'Wi-Fi / internet', 'CCTV / cameras', 'Printer', 'Email / accounts', 'Software', 'Other'];
const SLOTS = ['Morning', 'Afternoon', 'Evening'];
const MODES = ['WhatsApp call', 'Phone call', 'Video call', 'In person'];
const PROPERTIES = ['Home', 'Office', 'School', 'Shop / retail', 'Other'];
const URGENCY = ['Not urgent', 'Soon', 'Urgent'];
const TYPES = {
  quote: { label: 'Quote request', services: SERVICES },
  consultation: { label: 'Consultation booking', services: SERVICES },
  survey: { label: 'Site survey request', services: SURVEY },
  support: { label: 'Support request', services: ISSUES }
};

const env = k => process.env[k] || '';
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');
const pick = (v, list) => (list.includes(v) ? v : '');
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

// Short "Key: value" text of the extra fields, used in emails and WhatsApp alerts
function detailLines(e) {
  const d = e.details || {};
  const rows = [['Phone', e.phone], ['Date', d.date], ['Time', d.slot], ['How', d.mode], ['Location', d.location], ['Property', d.property], ['Size', d.quantity], ['Urgency', d.urgency]];
  return rows.filter(([, v]) => v);
}

async function sendMail(e) {
  if (!env('SMTP_HOST') || !env('MAIL_TO')) return false;
  const port = Number(env('SMTP_PORT') || 587);
  const mailer = nodemailer.createTransport({
    host: env('SMTP_HOST'), port, secure: port === 465,
    auth: env('SMTP_USER') ? { user: env('SMTP_USER'), pass: env('SMTP_PASS') } : undefined
  });
  const label = TYPES[e.type].label;
  const rows = [['Name', e.name], ['Email', e.email], ...detailLines(e).filter(([k]) => k !== 'Email'), ['Service', e.service], ['Budget', e.budget]].filter(([, v]) => v && v !== 'Not specified');
  await mailer.sendMail({
    from: env('MAIL_FROM') || env('SMTP_USER'),
    to: env('MAIL_TO'),
    replyTo: e.email || undefined,
    subject: `${label}: ${e.service || 'General'} (${e.name})`,
    text: `${label}\n\n${rows.map(([k, v]) => `${k}: ${v}`).join('\n')}\n\n${e.message}`,
    html: `<p><b>${esc(label)}</b></p><p>${rows.map(([k, v]) => `<b>${esc(k)}:</b> ${esc(v)}`).join('<br>')}</p><p>${esc(e.message).replace(/\n/g, '<br>')}</p>`
  });
  return true;
}

// Optional automatic WhatsApp alert via the WhatsApp Business Cloud API (Meta)
async function notifyWhatsApp(e) {
  const to = env('WHATSAPP_TO').replace(/\D/g, '');
  if (!env('WHATSAPP_TOKEN') || !env('WHATSAPP_PHONE_ID') || !to) return false;
  const one = v => String(v || '-').replace(/\s+/g, ' ').slice(0, 500);
  const label = TYPES[e.type].label;
  const extra = detailLines(e).map(([k, v]) => `${k}: ${v}`).join(', ');
  const tpl = env('WHATSAPP_TEMPLATE');
  const params = [e.name, e.email || e.phone, `${label}: ${e.service || 'General'}`, e.budget && e.budget !== 'Not specified' ? e.budget : extra, e.message];
  const body = tpl
    ? { messaging_product: 'whatsapp', to, type: 'template', template: { name: tpl, language: { code: env('WHATSAPP_TEMPLATE_LANG') || 'en' },
        components: [{ type: 'body', parameters: params.map(v => ({ type: 'text', text: one(v) })) }] } }
    : { messaging_product: 'whatsapp', to, type: 'text',
        text: { body: `${label}\nName: ${e.name}\n${e.email ? `Email: ${e.email}\n` : ''}${extra ? `${extra}\n` : ''}Service: ${e.service || '-'}\n\n${e.message || ''}` } };
  const r = await fetch(`https://graph.facebook.com/v20.0/${env('WHATSAPP_PHONE_ID')}/messages`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${env('WHATSAPP_TOKEN')}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error(`WhatsApp ${r.status}: ${await r.text()}`);
  return true;
}

export default async (req) => {
  if (req.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
  let b;
  try { b = await req.json(); } catch { return json({ error: 'Invalid request.' }, 400); }
  if (!b || typeof b !== 'object') return json({ error: 'Invalid request.' }, 400);
  if (b.website) return json({ ok: true }); // honeypot: bots fill this in

  const type = TYPES[b.type] ? b.type : 'quote';
  const name = clean(b.name, 100), email = clean(b.email, 150), message = clean(b.message, 3000);
  const phone = clean(b.phone, 25).replace(/[^\d+\s()-]/g, '');
  const service = pick(b.service, TYPES[type].services);
  const budget = type === 'quote' ? (clean(b.budget, 60) || 'Not specified') : '';
  if (name.length < 2) return json({ error: 'Please enter your name.' }, 400);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ error: 'Please enter a valid email address.' }, 400);
  if (phone && phone.replace(/\D/g, '').length < 7) return json({ error: 'Please enter a valid phone number.' }, 400);
  if (!email && !phone) return json({ error: 'Please add an email address or a phone number so we can reply.' }, 400);

  const details = {};
  if (type === 'consultation' || type === 'survey') {
    const date = clean(b.date, 10);
    if (date) {
      const t = Date.parse(`${date}T00:00:00Z`);
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || Number.isNaN(t) || t < Date.now() - 2 * 864e5) return json({ error: 'Please choose a date that has not passed.' }, 400);
      details.date = date;
    } else if (type === 'consultation') return json({ error: 'Please choose a date.' }, 400);
  }
  if (type === 'consultation') {
    details.slot = pick(b.slot, SLOTS); details.mode = pick(b.mode, MODES);
    if (!details.slot || !details.mode) return json({ error: 'Please choose a time and how you would like to talk.' }, 400);
  }
  if (type === 'survey') {
    details.location = clean(b.location, 200); details.property = pick(b.property, PROPERTIES); details.quantity = clean(b.quantity, 60);
    if (details.location.length < 3) return json({ error: 'Please tell us the location of the site.' }, 400);
    if (!service) return json({ error: 'Please choose what you need.' }, 400);
  }
  if (type === 'support') {
    details.urgency = pick(b.urgency, URGENCY);
    if (!service) return json({ error: 'Please choose what needs help.' }, 400);
  }
  if ((type === 'quote' || type === 'support') && message.length < 10) return json({ error: 'Please tell us a bit more (at least 10 characters).' }, 400);

  const entry = { id: crypto.randomUUID(), createdAt: new Date().toISOString(), type, status: 'new', name, email, phone, service: service || 'Not specified', budget, message, details };
  const tasks = [
    getStore('messages').setJSON(`${entry.createdAt}_${entry.id}`, entry).then(() => true),
    sendMail(entry),
    notifyWhatsApp(entry)
  ];
  // Serverless functions stop after responding, so wait for everything to finish first
  const results = await Promise.allSettled(tasks);
  results.forEach((r, i) => { if (r.status === 'rejected') console.error(['Save', 'Email', 'WhatsApp'][i], 'failed:', r.reason?.message || r.reason); });
  const delivered = results.some(r => r.status === 'fulfilled' && r.value === true);
  if (!delivered) return json({ error: 'We could not send your message. Please try WhatsApp instead.' }, 500);
  return json({ ok: true });
};

export const config = { path: '/api/contact' };
