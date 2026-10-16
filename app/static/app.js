const element = (id) => document.getElementById(id);
const actor = () => element('actor').value;
const money = (minor) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(minor / 100);

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { 'X-Demo-User': actor(), ...options.headers },
  });
  const body = await response.json();
  return { response, body };
}

function showError(message) {
  element('page-error').textContent = message;
  element('page-error').hidden = !message;
}

async function refresh() {
  const selectedActor = actor();
  try {
    const [records, summary] = await Promise.all([api('/api/charging-sessions'), api('/api/summary')]);
    if (!records.response.ok || !summary.response.ok) throw new Error('Unable to load charging history.');
    if (actor() !== selectedActor) return;
    element('session-count').textContent = summary.body.sessions;
    element('energy-total').textContent = `${(summary.body.energy_wh / 1000).toFixed(1)} kWh`;
    element('cost-total').textContent = money(summary.body.amount_minor);
    const table = element('session-rows');
    table.replaceChildren();
    for (const record of records.body) {
      const row = document.createElement('tr');
      const idCell = document.createElement('td');
      const link = document.createElement('button');
      link.className = 'record-link';
      link.textContent = record.id;
      link.addEventListener('click', () => {
        element('session-id').value = record.id;
        inspect();
      });
      idCell.append(link);
      row.append(idCell);
      for (const text of [new Date(record.charged_at).toLocaleDateString(), `${record.energy_wh / 1000} kWh`, money(record.amount_minor)]) {
        const cell = document.createElement('td');
        cell.textContent = text;
        row.append(cell);
      }
      table.append(row);
    }
    showError('');
  } catch (error) {
    showError(error.message);
  }
}

async function inspect() {
  const selectedActor = actor();
  const sessionId = element('session-id').value.trim();
  element('lookup-status').textContent = 'Requesting';
  try {
    const { response, body } = await api(`/api/charging-sessions/${encodeURIComponent(sessionId)}`);
    if (actor() !== selectedActor) return;
    element('lookup-status').textContent = `HTTP ${response.status}`;
    element('lookup-output').textContent = JSON.stringify(body, null, 2);
  } catch (error) {
    element('lookup-status').textContent = 'Request failed';
    element('lookup-output').textContent = error.message;
  }
}

element('lookup-form').addEventListener('submit', (event) => { event.preventDefault(); inspect(); });
element('refresh').addEventListener('click', refresh);
element('actor').addEventListener('change', () => {
  element('lookup-status').textContent = 'Not requested';
  element('lookup-output').textContent = 'Identity changed. Request a record to inspect access.';
  element('upload-result').textContent = '';
  refresh();
});
element('upload-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const file = element('csv-file').files[0];
  if (!file) return;
  const data = new FormData();
  data.append('file', file);
  const button = event.currentTarget.querySelector('button');
  const selectedActor = actor();
  button.disabled = true;
  element('upload-result').textContent = 'Importing…';
  try {
    const { response, body } = await api('/api/imports/csv', { method: 'POST', body: data });
    if (actor() !== selectedActor) return;
    element('upload-result').textContent = response.ok
      ? `Imported ${body.imported} records: ${body.session_ids.join(', ')}.`
      : `HTTP ${response.status}: ${typeof body.detail === 'string' ? body.detail : 'Invalid request.'}`;
    if (response.ok) await refresh();
  } catch (error) {
    element('upload-result').textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

async function start() {
  try {
    const { response, body } = await api('/api/demo/context');
    if (!response.ok) throw new Error(body.detail || 'Demo API unavailable.');
    element('connection').textContent = 'Local synthetic API';
    element('versions').textContent = Object.entries(body.dependencies).map(([name, version]) => `${name} ${version}`).join(' · ');
    await refresh();
  } catch (error) {
    element('connection').textContent = 'API unavailable';
    showError(error.message);
  }
}
start();
