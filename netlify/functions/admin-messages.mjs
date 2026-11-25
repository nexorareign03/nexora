import crypto from 'node:crypto';
import { getStore } from '@netlify/blobs';

// GET   /api/admin/messages                      -> list of enquiries (newest first)
// PATCH /api/admin/messages {key, status}        -> status "new" or "done"
// Both need the header:  Authorization: Bearer <ADMIN_TOKEN>
const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

function authorised(req) {
  const token = process.env.ADMIN_TOKEN || '';
  const given = (req.headers.get('authorization') || '').replace(/^Bearer\s+/i, '');
  const a = Buffer.from(given), b = Buffer.from(token);
  return !!token && a.length === b.length && crypto.timingSafeEqual(a, b);
}

export default async (req) => {
  if (!authorised(req)) return json({ error: 'Unauthorized' }, 401);
  const store = getStore('messages');

  if (req.method === 'PATCH') {
    let b;
    try { b = await req.json(); } catch { return json({ error: 'Invalid request.' }, 400); }
    if (!b || typeof b.key !== 'string' || !/^[\w:.\-]{10,120}$/.test(b.key) || !['new', 'done'].includes(b.status)) return json({ error: 'Invalid request.' }, 400);
    const item = await store.get(b.key, { type: 'json' });
    if (!item) return json({ error: 'Not found' }, 404);
    item.status = b.status;
    await store.setJSON(b.key, item);
    return json({ ok: true });
  }

  if (req.method !== 'GET') return json({ error: 'Method not allowed' }, 405);
  const { blobs } = await store.list();
  const items = (await Promise.all(blobs.map(async x => {
    const v = await store.get(x.key, { type: 'json' });
    return v ? { ...v, key: x.key } : null;
  }))).filter(Boolean);
  items.sort((m, n) => n.createdAt.localeCompare(m.createdAt));
  return json(items);
};

export const config = { path: '/api/admin/messages' };
