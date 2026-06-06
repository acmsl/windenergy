/**
 * Cloudflare Worker – ACM SL Contact Form Mailer
 *
 * DESPLIEGUE (una sola vez, cuenta gratuita):
 * ─────────────────────────────────────────────
 * 1. Ir a https://workers.cloudflare.com  → Sign up (gratis)
 * 2. Dashboard → Workers & Pages → Create application → Create Worker
 * 3. Pegar todo este archivo en el editor online y pulsar "Deploy"
 * 4. Copiar la URL que aparece (ej. https://acmsl-mailer.TU_USUARIO.workers.dev)
 * 5. Pegar esa URL en formulario.html → constante WORKER_URL
 *
 * Plan gratuito: 100.000 peticiones/día, más que suficiente.
 */

const SMTP2GO_API_KEY = 'api-4FF8401B844D4E96AD5DF8C44F8CF48D';
const RECIPIENT       = 'support@acm-sl.com';
const SENDER          = 'Formulario ACM SL <support@acm-sl.com>';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin':  '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export default {
  async fetch(request) {

    /* ── Preflight CORS ─────────────────────────────────────── */
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    /* ── Parse body ─────────────────────────────────────────── */
    let data;
    try {
      data = await request.json();
    } catch {
      return json({ ok: false, error: 'Invalid JSON body' }, 400);
    }

    const { nombre, apellidos, email, telefono, direccion, ciudad, pais, mensaje } = data;

    if (!nombre || !apellidos || !email || !telefono || !ciudad || !pais || !mensaje) {
      return json({ ok: false, error: 'Missing required fields' }, 422);
    }

    /* ── Build HTML email ───────────────────────────────────── */
    const html = `
      <table style="font-family:sans-serif;font-size:15px;color:#123047;border-collapse:collapse;width:100%;max-width:640px">
        <tr><td colspan="2" style="background:#006699;color:#fff;padding:14px 20px;font-size:18px;font-weight:700">
          Nuevo mensaje de contacto – ACM SL
        </td></tr>
        <tr><td style="padding:10px 20px;font-weight:600;width:160px">Nombre</td>
            <td style="padding:10px 20px">${esc(nombre)} ${esc(apellidos)}</td></tr>
        <tr style="background:#f3f7fb">
            <td style="padding:10px 20px;font-weight:600">Email</td>
            <td style="padding:10px 20px">${esc(email)}</td></tr>
        <tr><td style="padding:10px 20px;font-weight:600">Teléfono</td>
            <td style="padding:10px 20px">${esc(telefono)}</td></tr>
        <tr style="background:#f3f7fb">
            <td style="padding:10px 20px;font-weight:600">Dirección</td>
            <td style="padding:10px 20px">${esc(direccion || '—')}</td></tr>
        <tr><td style="padding:10px 20px;font-weight:600">Ciudad</td>
            <td style="padding:10px 20px">${esc(ciudad)}</td></tr>
        <tr style="background:#f3f7fb">
            <td style="padding:10px 20px;font-weight:600">País</td>
            <td style="padding:10px 20px">${esc(pais)}</td></tr>
        <tr><td colspan="2" style="padding:10px 20px;font-weight:600">Mensaje</td></tr>
        <tr><td colspan="2" style="padding:10px 20px;background:#f3f7fb;white-space:pre-wrap">${esc(mensaje)}</td></tr>
      </table>`;

    /* ── Call SMTP2GO API (server-side, no CORS) ────────────── */
    const visitorName = `${nombre.trim()} ${apellidos.trim()}`;

    const payload = {
      api_key:   SMTP2GO_API_KEY,
      sender:    SENDER,
      to:        [RECIPIENT],
      cc:        [`${visitorName} <${email}>`],
      subject:   `Contacto web: ${visitorName}`,
      html_body: html,
    };

    let smtpRes, smtpJson;
    try {
      smtpRes  = await fetch('https://api.smtp2go.com/v3/email/send', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(payload),
      });
      smtpJson = await smtpRes.json();
    } catch (err) {
      return json({ ok: false, error: `Network error: ${err.message}` }, 502);
    }

    if (!smtpRes.ok || smtpJson.data?.error) {
      return json({ ok: false, error: smtpJson.data?.error || `SMTP2GO HTTP ${smtpRes.status}` }, 502);
    }

    return json({ ok: true, email_id: smtpJson.data?.email_id });
  },
};

/* ── Helpers ────────────────────────────────────────────────── */
function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
