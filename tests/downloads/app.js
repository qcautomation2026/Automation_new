import express from 'express';
import { q, logAudit } from '../db.js';
import { requireAuth, requireCouple, str, int, oneOf, isoDate, dataUrlImage } from '../auth.js';
import {
  CATEGORIES, CATEGORY_IDS, POINT_OPTIONS, POINT_VALUES, REWARD_CATEGORIES,
  balanceFor, coupleSnapshot, evaluateAchievements, achievementList, streakFor, MILESTONE,
} from '../domain.js';

export const router = express.Router();
const ah = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.use(requireAuth);

/* Static catalog used to build the Give Love flow. */
router.get('/catalog', (req, res) => {
  res.json({ categories: CATEGORIES, pointOptions: POINT_OPTIONS, rewardCategories: REWARD_CATEGORIES, milestone: MILESTONE });
});

router.use(requireCouple);

/** Authorization anchor. Comes from the session, never from the request body or params. */
const scoped = (req) => Number(req.user.couple_id);
const meId = (req) => Number(req.user.id);

const eventRow = (r, viewerId) => ({
  id: Number(r.id), fromId: Number(r.from_user), toId: Number(r.to_user),
  fromName: r.from_name, toName: r.to_name,
  category: r.category, reason: r.reason, points: Number(r.points), message: r.message,
  createdAt: r.created_at, mine: Number(r.from_user) === viewerId,
});

/* ---------------- appreciation events ---------------- */

router.get('/events', ah(async (req, res) => {
  const limit = Math.min(Number(req.query.limit) || 100, 300);
  const filters = ['e.couple_id = ?'];
  const params = [scoped(req)];
  if (req.query.from) { filters.push('e.from_user = ?'); params.push(int(req.query.from, { field: 'from', min: 1 })); }
  if (req.query.category) { filters.push('e.category = ?'); params.push(oneOf(req.query.category, CATEGORY_IDS, 'category')); }
  if (req.query.points) { filters.push('e.points = ?'); params.push(Number(oneOf(String(req.query.points), POINT_VALUES.map(String), 'points'))); }

  const rows = await q.all(`
    SELECT e.*, uf.display_name AS from_name, ut.display_name AS to_name
    FROM events e
    JOIN users uf ON uf.id = e.from_user
    JOIN users ut ON ut.id = e.to_user
    WHERE ${filters.join(' AND ')}
    ORDER BY e.id DESC LIMIT ?`, ...params, limit);

  res.json({ events: rows.map((r) => eventRow(r, meId(req))) });
}));

router.post('/events', ah(async (req, res) => {
  const coupleId = scoped(req);
  const partner = await q.get('SELECT id, display_name FROM users WHERE couple_id = ? AND id != ?', coupleId, meId(req));
  if (!partner) return res.status(409).json({ error: 'Your partner has not joined yet.', code: 'NO_PARTNER' });

  const category = oneOf(req.body.category, CATEGORY_IDS, 'Category');
  const reason = str(req.body.reason, { field: 'Reason', max: 80 });
  const points = int(req.body.points, { field: 'Points', min: 1, max: 50 });
  if (!POINT_VALUES.includes(points)) {
    return res.status(400).json({ error: 'Choose one of the available point amounts.', field: 'points' });
  }
  const message = str(req.body.message, { field: 'Message', max: 300, required: false });
  const partnerId = Number(partner.id);

  const before = (await balanceFor(coupleId, partnerId)).current;
  const info = await q.run(`
    INSERT INTO events (couple_id, from_user, to_user, category, reason, points, message)
    VALUES (?, ?, ?, ?, ?, ?, ?)`, coupleId, meId(req), partnerId, category, reason, points, message);

  const newAchievements = await evaluateAchievements(coupleId);
  const row = await q.get(`
    SELECT e.*, uf.display_name AS from_name, ut.display_name AS to_name
    FROM events e JOIN users uf ON uf.id = e.from_user JOIN users ut ON ut.id = e.to_user
    WHERE e.id = ?`, info.lastInsertRowid);

  res.status(201).json({
    event: eventRow(row, meId(req)),
    milestoneReached: before < MILESTONE && before + points >= MILESTONE,
    newAchievements,
    ...(await coupleSnapshot(coupleId, meId(req))),
  });
}));

/* ---------------- rewards ---------------- */

router.get('/rewards', ah(async (req, res) => {
  const coupleId = scoped(req);
  const rewards = await q.all(
    'SELECT id, category, emoji, name, description, cost FROM rewards WHERE couple_id = ? AND archived = 0 ORDER BY cost, id', coupleId);
  const redemptions = await q.all(`
    SELECT r.id, r.name, r.emoji, r.cost, r.completed, r.created_at, r.completed_at,
           r.redeemed_by, u.display_name AS redeemed_by_name
    FROM redemptions r JOIN users u ON u.id = r.redeemed_by
    WHERE r.couple_id = ? ORDER BY r.id DESC`, coupleId);
  res.json({ rewards, redemptions, balance: await balanceFor(coupleId, meId(req)) });
}));

router.post('/rewards', ah(async (req, res) => {
  const coupleId = scoped(req);
  const { n } = await q.get('SELECT COUNT(*) AS n FROM rewards WHERE couple_id = ? AND archived = 0', coupleId);
  if (Number(n) >= 60) return res.status(409).json({ error: 'You already have 60 rewards. Remove one first.' });

  const category = oneOf(req.body.category, REWARD_CATEGORIES, 'Category');
  const name = str(req.body.name, { field: 'Reward name', max: 50 });
  const description = str(req.body.description, { field: 'Description', max: 160, required: false });
  const emoji = str(req.body.emoji, { field: 'Emoji', max: 8, required: false }) || '🎁';
  const cost = int(req.body.cost, { field: 'Cost', min: 25, max: 1000 });

  const info = await q.run(
    'INSERT INTO rewards (couple_id, category, emoji, name, description, cost) VALUES (?, ?, ?, ?, ?, ?)',
    coupleId, category, emoji, name, description, cost);
  res.status(201).json({
    reward: await q.get('SELECT id, category, emoji, name, description, cost FROM rewards WHERE id = ?', info.lastInsertRowid),
  });
}));

router.delete('/rewards/:id', ah(async (req, res) => {
  const id = int(req.params.id, { field: 'Reward id', min: 1 });
  // couple_id in the WHERE clause is the authorization check.
  const info = await q.run('UPDATE rewards SET archived = 1 WHERE id = ? AND couple_id = ?', id, scoped(req));
  if (!info.changes) return res.status(404).json({ error: 'Reward not found.' });
  res.json({ ok: true });
}));

router.post('/rewards/:id/redeem', ah(async (req, res) => {
  const coupleId = scoped(req);
  const id = int(req.params.id, { field: 'Reward id', min: 1 });
  const reward = await q.get('SELECT * FROM rewards WHERE id = ? AND couple_id = ? AND archived = 0', id, coupleId);
  if (!reward) return res.status(404).json({ error: 'Reward not found.' });

  const cost = Number(reward.cost);
  // The balance is re-checked inside the transaction, so a disabled button is never the only guard
  // and the same points cannot be spent twice by two quick taps.
  const result = await q.tx(async (t) => {
    const row = await t.get(
      `SELECT (SELECT COALESCE(SUM(points),0) FROM events      WHERE couple_id = ?1 AND to_user     = ?2)
            - (SELECT COALESCE(SUM(cost),  0) FROM redemptions WHERE couple_id = ?1 AND redeemed_by = ?2) AS current`,
      coupleId, meId(req));
    if (Number(row.current) < cost) return { short: true };
    await t.run(
      'INSERT INTO redemptions (couple_id, reward_id, name, emoji, cost, redeemed_by) VALUES (?, ?, ?, ?, ?, ?)',
      coupleId, Number(reward.id), reward.name, reward.emoji, cost, meId(req));
    return { short: false };
  });
  if (result.short) return res.status(409).json({ error: 'You do not have enough points for this reward yet.' });

  const newAchievements = await evaluateAchievements(coupleId);
  await logAudit(meId(req), 'reward_redeemed', reward.name, req.ip);
  res.status(201).json({ reward, newAchievements, ...(await coupleSnapshot(coupleId, meId(req))) });
}));

router.post('/redemptions/:id/complete', ah(async (req, res) => {
  const id = int(req.params.id, { field: 'Redemption id', min: 1 });
  const info = await q.run(
    `UPDATE redemptions SET completed = 1, completed_at = datetime('now')
     WHERE id = ? AND couple_id = ? AND completed = 0`, id, scoped(req));
  if (!info.changes) return res.status(404).json({ error: 'Redemption not found or already completed.' });
  res.json({ ok: true });
}));

/* ---------------- memories ---------------- */

router.get('/memories', ah(async (req, res) => {
  const memories = await q.all(`
    SELECT m.id, m.title, m.memory_date, m.description, m.photo, m.created_at, u.display_name AS author
    FROM memories m JOIN users u ON u.id = m.created_by
    WHERE m.couple_id = ? ORDER BY m.memory_date DESC, m.id DESC`, scoped(req));
  res.json({ memories });
}));

router.post('/memories', ah(async (req, res) => {
  const title = str(req.body.title, { field: 'Title', max: 80 });
  const memoryDate = isoDate(req.body.date, { field: 'Date' });
  const description = str(req.body.description, { field: 'Description', max: 500, required: false });
  const photo = dataUrlImage(req.body.photo);

  const info = await q.run(`
    INSERT INTO memories (couple_id, created_by, title, memory_date, description, photo)
    VALUES (?, ?, ?, ?, ?, ?)`, scoped(req), meId(req), title, memoryDate, description, photo);
  const memory = await q.get(`
    SELECT m.id, m.title, m.memory_date, m.description, m.photo, m.created_at, u.display_name AS author
    FROM memories m JOIN users u ON u.id = m.created_by WHERE m.id = ?`, info.lastInsertRowid);
  res.status(201).json({ memory });
}));

router.delete('/memories/:id', ah(async (req, res) => {
  const id = int(req.params.id, { field: 'Memory id', min: 1 });
  const info = await q.run('DELETE FROM memories WHERE id = ? AND couple_id = ?', id, scoped(req));
  if (!info.changes) return res.status(404).json({ error: 'Memory not found.' });
  res.json({ ok: true });
}));

/* ---------------- achievements and stats ---------------- */

router.get('/achievements', ah(async (req, res) => {
  res.json({ achievements: await achievementList(scoped(req)) });
}));

router.get('/stats', ah(async (req, res) => {
  const coupleId = scoped(req);
  const rows = await q.all('SELECT id, display_name FROM users WHERE couple_id = ? ORDER BY id', coupleId);
  const perMember = [];
  for (const m of rows) {
    const id = Number(m.id);
    const c = await q.get('SELECT COUNT(*) AS n FROM events WHERE couple_id = ? AND from_user = ?', coupleId, id);
    perMember.push({ id, name: m.display_name, ...(await balanceFor(coupleId, id)), appreciationsGiven: Number(c.n) });
  }
  const favCategory = await q.get(
    'SELECT category, COUNT(*) AS n FROM events WHERE couple_id = ? GROUP BY category ORDER BY n DESC LIMIT 1', coupleId);
  const favReason = await q.get(
    'SELECT reason, COUNT(*) AS n FROM events WHERE couple_id = ? GROUP BY reason ORDER BY n DESC LIMIT 1', coupleId);
  const t = await q.get(`
    SELECT
      (SELECT COUNT(*) FROM events      WHERE couple_id = ?1)                  AS appreciations,
      (SELECT COUNT(*) FROM memories    WHERE couple_id = ?1)                  AS memories,
      (SELECT COUNT(*) FROM redemptions WHERE couple_id = ?1)                  AS redeemed,
      (SELECT COUNT(*) FROM redemptions WHERE couple_id = ?1 AND completed = 1) AS completed,
      (SELECT COUNT(*) FROM achievements WHERE couple_id = ?1)                 AS achievements`, coupleId);

  res.json({
    perMember,
    totals: {
      lifetime: perMember.reduce((n, m) => n + m.lifetime, 0),
      appreciations: Number(t.appreciations),
      memories: Number(t.memories),
      rewardsRedeemed: Number(t.redeemed),
      rewardsCompleted: Number(t.completed),
      achievements: Number(t.achievements),
    },
    favCategory: favCategory ? CATEGORIES.find((c) => c.id === favCategory.category) || null : null,
    favReason: favReason?.reason || null,
    streak: await streakFor(coupleId),
  });
}));

router.get('/snapshot', ah(async (req, res) => {
  res.json(await coupleSnapshot(scoped(req), meId(req)));
}));

/* ---------------- data export ---------------- */

/**
 * Everything this couple owns, as one JSON file they can keep.
 * Password hashes and the audit log are deliberately excluded.
 */
router.get('/export', ah(async (req, res) => {
  const coupleId = scoped(req);
  const couple = await q.get('SELECT nickname, anniversary, created_at FROM couples WHERE id = ?', coupleId);
  const [members, events, rewards, redemptions, memories, achievements] = await Promise.all([
    q.all('SELECT display_name, created_at FROM users WHERE couple_id = ? ORDER BY id', coupleId),
    q.all(`SELECT e.created_at, e.category, e.reason, e.points, e.message,
                  uf.display_name AS from_name, ut.display_name AS to_name
           FROM events e JOIN users uf ON uf.id = e.from_user JOIN users ut ON ut.id = e.to_user
           WHERE e.couple_id = ? ORDER BY e.id`, coupleId),
    q.all('SELECT category, emoji, name, description, cost, archived FROM rewards WHERE couple_id = ? ORDER BY id', coupleId),
    q.all(`SELECT r.name, r.emoji, r.cost, r.completed, r.created_at, r.completed_at, u.display_name AS redeemed_by
           FROM redemptions r JOIN users u ON u.id = r.redeemed_by WHERE r.couple_id = ? ORDER BY r.id`, coupleId),
    q.all(`SELECT m.title, m.memory_date, m.description, m.photo, m.created_at, u.display_name AS author
           FROM memories m JOIN users u ON u.id = m.created_by WHERE m.couple_id = ? ORDER BY m.id`, coupleId),
    q.all('SELECT key, unlocked_at FROM achievements WHERE couple_id = ? ORDER BY id', coupleId),
  ]);

  const stamp = new Date().toISOString().slice(0, 10);
  res.setHeader('Content-Disposition', `attachment; filename="lovebook-backup-${stamp}.json"`);
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.send(JSON.stringify({
    exportedAt: new Date().toISOString(),
    app: 'Q&A Lovebook',
    couple, members, events, rewards, redemptions, memories, achievements,
  }, null, 2));
}));
