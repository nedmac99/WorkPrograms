// Minimal handler for Hours/Purity section + submit
// Using provided selectors

const SELECTORS = {
	hoursIn: '#txtHoursIn',
	oxygenPurity: '#txtO2In',
	submit: '#start',
};

// Confirm Reported Problem section (radios, then explicit confirm click)
const CONFIRM_SELECTORS = {
	confirmIssueYes: '#radConfirmIssue', // value="1"
	smokeNo: '#radSmokeNo', // value="2"
	submit: '#btnConfirmDefective',
};

function dispatchEvents(el) {
	try {
		el.dispatchEvent(new Event('input', { bubbles: true }));
		el.dispatchEvent(new Event('change', { bubbles: true }));
	} catch (e) {
		// noop
	}
}

function setValue(el, value) {
	if (!el) return false;
	const tag = (el.tagName || '').toUpperCase();
	if (tag === 'INPUT') {
		const type = (el.type || '').toLowerCase();
		// sanitize numeric inputs while preserving user intent
		if (type === 'number') {
			// strip non-digit except dot for decimals
			const cleaned = String(value ?? '')
				.replace(/%/g, '')
				.replace(/[^0-9.]/g, '');
			el.value = cleaned;
			dispatchEvents(el);
			return true;
		}
		if (type === 'checkbox') {
			el.checked = !!value;
			dispatchEvents(el);
			return true;
		}
		if (type === 'radio') {
			// For radios, select by matching value if provided
			if (value == null || value === '') return false;
			const group = document.querySelectorAll(`input[type="radio"][name="${el.name}"]`);
			for (const r of group) {
				if (String(r.value) === String(value)) {
					r.checked = true;
					dispatchEvents(r);
					return true;
				}
			}
			return false;
		}
		el.value = value ?? '';
		dispatchEvents(el);
		return true;
	}
	if (tag === 'TEXTAREA') {
		el.value = value ?? '';
		dispatchEvents(el);
		return true;
	}
	if (tag === 'SELECT') {
		if (value == null) return false;
		let matched = false;
		for (let i = 0; i < el.options.length; i++) {
			const opt = el.options[i];
			if (String(opt.value) === String(value) || String(opt.text).trim() === String(value).trim()) {
				el.selectedIndex = i;
				matched = true;
				break;
			}
		}
		if (!matched && el.options.length) el.selectedIndex = 0; // graceful fallback
		dispatchEvents(el);
		return matched;
	}
	// Fallback: try contentEditable
	if (el.isContentEditable) {
		el.textContent = value ?? '';
		dispatchEvents(el);
		return true;
	}
	return false;
}

function query(selector) {
	if (!selector) return null;
	try {
		if (typeof selector === 'string' && selector.startsWith('#')) {
			const id = selector.slice(1);
			const byId = document.getElementById(id);
			if (byId) return byId;
		}
		return document.querySelector(selector);
	} catch {
		return null;
	}
}

function getSelectors() {
	return new Promise((resolve) => {
		try {
			chrome.storage?.sync?.get('hoursPuritySelectors', (res) => {
				const cfg = res?.hoursPuritySelectors;
				if (cfg && typeof cfg === 'object') {
					resolve({ ...SELECTORS, ...cfg });
				} else {
					resolve(SELECTORS);
				}
			});
		} catch {
			resolve(SELECTORS);
		}
	});
}

function getConfirmSelectors() {
	return new Promise((resolve) => {
		try {
			chrome.storage?.sync?.get('confirmProblemSelectors', (res) => {
				const cfg = res?.confirmProblemSelectors;
				if (cfg && typeof cfg === 'object') {
					resolve({ ...CONFIRM_SELECTORS, ...cfg });
				} else {
					resolve(CONFIRM_SELECTORS);
				}
			});
		} catch {
			resolve(CONFIRM_SELECTORS);
		}
	});
}

async function fillHoursAndPurity({ hoursIn = '', oxygenPurity = '' } = {}) {
	const selectors = await getSelectors();
	const res = { filled: { hoursIn: false, oxygenPurity: false }, submitted: false };

	const hoursEl = query(selectors.hoursIn);
	// ensure integer for hours
	const hoursClean = String(hoursIn).replace(/[^0-9]/g, '');
	res.filled.hoursIn = setValue(hoursEl, hoursClean);

	const purityEl = query(selectors.oxygenPurity);
	// allow decimals; remove percent if typed
	const purityClean = String(oxygenPurity).replace(/%/g, '').replace(/[^0-9.]/g, '');
	res.filled.oxygenPurity = setValue(purityEl, purityClean);

	const submitEl = query(selectors.submit);
	if (submitEl) {
		try {
			submitEl.click();
			res.submitted = true;
		} catch {
			res.submitted = false;
		}
	}
	return res;
}

async function confirmReportedProblem() {
	const selectors = await getConfirmSelectors();
	const res = { setYes: false, setSmokeNo: false, submitted: false };

	const yesEl = query(selectors.confirmIssueYes);
	if (yesEl) {
		yesEl.checked = true;
		dispatchEvents(yesEl);
		res.setYes = true;
	}

	const smokeNoEl = query(selectors.smokeNo);
	if (smokeNoEl) {
		smokeNoEl.checked = true;
		dispatchEvents(smokeNoEl);
		res.setSmokeNo = true;
	}
	const submitEl = query(selectors.submit);
	if (submitEl) {
		try {
			submitEl.click();
			res.submitted = true;
		} catch {
			res.submitted = false;
		}
	}

	return res;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (!message || !message.action) return;
	if (message.action === 'FILL_HOURS_AND_PURITY') {
		fillHoursAndPurity(message.values || {})
			.then((results) => sendResponse({ ok: true, results }))
			.catch((err) => sendResponse({ ok: false, error: String(err) }));
		return true; // async response
	}
	if (message.action === 'CONFIRM_REPORTED_PROBLEM') {
		confirmReportedProblem()
			.then((results) => sendResponse({ ok: true, results }))
			.catch((err) => sendResponse({ ok: false, error: String(err) }));
		return true;
	}
});

// Helpful console notice so you know it's active
console.info('[Form Automation Helper] Content script ready. Configure via storage keys "hoursPuritySelectors" and "confirmProblemSelectors" or edit constants.');

// ---------------- Failure Reason Section ----------------
const FAILURE_REASON_SELECTORS = {
	q1Radio: '#radRepairYes',
	q2Radio: '#radAbuseNo',
	firstCheckbox: '#1',
	reasonsContainer: '', // optional fallback container
	confirmBtn: '#btnRepairStatus',
};

function getFailureSelectors() {
	return new Promise((resolve) => {
		try {
			chrome.storage?.sync?.get('failureReasonSelectors', (res) => {
				const cfg = res?.failureReasonSelectors;
				if (cfg && typeof cfg === 'object') {
					resolve({ ...FAILURE_REASON_SELECTORS, ...cfg });
				} else {
					resolve(FAILURE_REASON_SELECTORS);
				}
			});
		} catch {
			resolve(FAILURE_REASON_SELECTORS);
		}
	});
}

function waitForSelector(selector, timeoutMs = 2000, intervalMs = 100) {
	return new Promise((resolve) => {
		if (!selector) return resolve(null);
		const start = Date.now();
		const tick = () => {
			const el = query(selector);
			if (el) return resolve(el);
			if (Date.now() - start >= timeoutMs) return resolve(null);
			setTimeout(tick, intervalMs);
		};
		tick();
	});
}

function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

function clickElement(el) {
	if (!el) return;
	try { el.focus(); } catch {}
	try { el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, view: window })); } catch {}
	try { el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, view: window })); } catch {}
	try { el.click(); } catch {}
	try { el.dispatchEvent(new MouseEvent('click', { bubbles: true, view: window })); } catch {}
}

function robustClick(el) {
	if (!el) return false;
	try { el.scrollIntoView({ block: 'center', inline: 'center' }); } catch {}
	try { el.focus({ preventScroll: true }); } catch {}
	const rect = (typeof el.getBoundingClientRect === 'function') ? el.getBoundingClientRect() : null;
	const cx = rect ? rect.left + Math.min(Math.max(rect.width / 2, 1), rect.width - 1) : 0;
	const cy = rect ? rect.top + Math.min(Math.max(rect.height / 2, 1), rect.height - 1) : 0;
	const target = el;
	try { target.dispatchEvent(new MouseEvent('pointerdown', { bubbles: true, clientX: cx, clientY: cy })); } catch {}
	try { target.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, clientX: cx, clientY: cy })); } catch {}
	try { target.dispatchEvent(new MouseEvent('pointerup', { bubbles: true, clientX: cx, clientY: cy })); } catch {}
	try { target.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, clientX: cx, clientY: cy })); } catch {}
	try { target.dispatchEvent(new MouseEvent('click', { bubbles: true, clientX: cx, clientY: cy })); } catch {}
	try { target.click?.(); } catch {}
	return true;
}

function runInPage(code) {
	try {
		const s = document.createElement('script');
		s.textContent = code;
		(document.documentElement || document.head || document.body).appendChild(s);
		s.parentNode.removeChild(s);
		return true;
	} catch { return false; }
}

function sendKey(el, key, options = {}) {
	if (!el) return;
	const evtInit = { key, code: key, keyCode: key.length === 1 ? key.toUpperCase().charCodeAt(0) : (key === 'Enter' ? 13 : 0), which: undefined, bubbles: true, cancelable: true, ...options };
	try { el.dispatchEvent(new KeyboardEvent('keydown', evtInit)); } catch {}
	try { el.dispatchEvent(new KeyboardEvent('keypress', evtInit)); } catch {}
	try { el.dispatchEvent(new KeyboardEvent('keyup', evtInit)); } catch {}
}

function closeDiagnosisModalIfPresent() {
	try {
		const modals = Array.from(document.querySelectorAll('.modal, [role="dialog"]'));
		const diag = modals.find(m => /diagnosis\s*codes?\s*cannot\s*be\s*empty/i.test(m.innerText || ''));
		if (diag) {
			const btn = Array.from(diag.querySelectorAll('button, .btn, [data-dismiss="modal"], .close'))
				.find(b => /close/i.test(b.innerText || b.value || '') || b.hasAttribute?.('data-dismiss') || b.classList?.contains('close'));
			try { btn?.click(); } catch {}
			return true;
		}
	} catch {}
	return false;
}

function isVisible(el) {
	if (!el) return false;
	const rect = el.getBoundingClientRect?.();
	const style = window.getComputedStyle?.(el);
	const visibleStyle = style ? (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && style.pointerEvents !== 'none') : true;
	return (el.offsetParent !== null || (rect && rect.width > 0 && rect.height > 0)) && visibleStyle;
}

async function runFailureReason() {
	const sel = await getFailureSelectors();
	const result = { q1: false, q2: false, checkbox: false, confirmed: false, waited: false };

	const q1 = query(sel.q1Radio);
	if (q1) {
		if (!q1.checked) q1.checked = true;
		dispatchEvents(q1);
		try { q1.click(); } catch {}
		result.q1 = true;
	}

	const q2 = query(sel.q2Radio);
	if (q2) {
		if (!q2.checked) q2.checked = true;
		dispatchEvents(q2);
		try { q2.click(); } catch {}
		result.q2 = true;
	}

	// Wait for checkbox or container to appear
	let firstCb = null;
	if (sel.firstCheckbox) {
		firstCb = await waitForSelector(sel.firstCheckbox, 2000, 100);
	}
	result.waited = true;
	if (!firstCb && sel.reasonsContainer) {
		const container = await waitForSelector(sel.reasonsContainer, 2000, 100);
		if (container) firstCb = container.querySelector('input[type="checkbox"]');
	}
	if (firstCb) {
		firstCb.checked = true;
		dispatchEvents(firstCb);
		result.checkbox = true;
	}

	const confirmBtn = query(sel.confirmBtn);
	if (confirmBtn) {
		try {
			confirmBtn.click();
			result.confirmed = true;
		} catch {
			result.confirmed = false;
		}
	}

	return result;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (!message || !message.action) return;
	if (message.action === 'RUN_FAILURE_REASON') {
		runFailureReason()
			.then((res) => sendResponse({ ok: true, results: res }))
			.catch((err) => sendResponse({ ok: false, error: String(err) }));
		return true;
	}
});

// ---------------- Parts Table Section ----------------
const PARTS_TABLE_SELECTORS = {
	tableContainer: '#tblParts',
	rowSelector: 'tbody tr',
	noRadioInRow: 'input[id^="radPartNo"]',
	specificYesSelector: '#radPartYes175243',
};

function getPartsSelectors() {
	return new Promise((resolve) => {
		try {
			chrome.storage?.sync?.get('partsTableSelectors', (res) => {
				const cfg = res?.partsTableSelectors;
				if (cfg && typeof cfg === 'object') {
					resolve({ ...PARTS_TABLE_SELECTORS, ...cfg });
				} else {
					resolve(PARTS_TABLE_SELECTORS);
				}
			});
		} catch {
			resolve(PARTS_TABLE_SELECTORS);
		}
	});
}

function getPartsConfigAndSelections() {
	return new Promise((resolve) => {
		try {
			chrome.storage?.sync?.get(['partsConfig', 'partsSelections', 'partNumberValue'], (res) => {
				let cfg = res?.partsConfig;
				if (typeof cfg === 'string') {
					try { cfg = JSON.parse(cfg); } catch { cfg = {}; }
				}
				if (!cfg || typeof cfg !== 'object') cfg = {};
				const selections = Array.isArray(res?.partsSelections) ? res.partsSelections : [];
				const partNumberValue = res?.partNumberValue || '';
				resolve({ cfg, selections, partNumberValue });
			});
		} catch {
			resolve({ cfg: {}, selections: [], partNumberValue: '' });
		}
	});
}

function findDiagnosisSelectInRow(row, yesEl) {
	let dcEl = row?.querySelector('select[id*="cmbDC" i], select[name*="cmbDC" i], select[id*="diagnosis" i], select[name*="diagnosis" i], select[id*="diag" i], select[name*="diag" i], select[id*="code" i], select[name*="code" i]');
	if (!dcEl && yesEl) {
		const m = (yesEl.id || '').match(/(\d+)/);
		if (m && m[1]) dcEl = document.querySelector(`#cmbDC${m[1]}`);
	}
	return dcEl;
}

function setDiagnosisValue(dcEl, desiredTextOrValue) {
	if (!dcEl) return false;
	let matched = false;
	const val = String(desiredTextOrValue || '').trim();
	if (val) {
		for (let i = 0; i < (dcEl.options?.length || 0); i++) {
			const opt = dcEl.options[i];
			const t = String(opt.textContent || '').trim();
			const v = String(opt.value || '').trim();
			if (t === val || v === val || t.toLowerCase() === val.toLowerCase() || v.toLowerCase() === val.toLowerCase()) {
				dcEl.selectedIndex = i;
				matched = true;
				break;
			}
		}
	}
	if (!matched) {
		// Fallback: INV4 preferred if present
		for (let i = 0; i < (dcEl.options?.length || 0); i++) {
			const opt = dcEl.options[i];
			if (/inv\s*4/i.test(opt.textContent || '') || /^INV4\|/i.test(opt.value || '')) {
				dcEl.selectedIndex = i;
				matched = true;
				break;
			}
		}
	}
	dispatchEvents(dcEl);
	return matched;
}

// Default diagnosis codes per part name (can be extended)
const PARTS_DEFAULT_CODES = {
	// Example defaults; adjust as needed
	'Sieve Tank': 'INV4 - Saturated',
};

function extractPartName(row) {
	if (!row) return '';
	// Try common patterns: first or second cell text
	const cells = Array.from(row.querySelectorAll('td'));
	for (const cell of cells) {
		const txt = (cell.innerText || cell.textContent || '').trim();
		if (txt && txt.length > 1 && txt.length < 200) {
			// Skip cells that look like radio/select containers
			if (cell.querySelector('input, select, button')) continue;
			return txt;
		}
	}
	// Fallback: entire row text trimmed
	return (row.innerText || '').trim();
}

function findYesRadioInRow(row) {
	if (!row) return null;
	let el = row.querySelector('input[id^="radPartYes"], input[type="radio"][value="1"], input[type="radio"][name*="Yes" i]');
	if (!el) {
		// Try global by id pattern
		const idMatch = Array.from(row.querySelectorAll('input[type="radio"][id]')).map(e => e.id.match(/radPartYes\d+/)).find(Boolean);
		if (idMatch) el = document.getElementById(idMatch[0]);
	}
	return el;
}

function findPrimaryCauseInRow(row, yesEl) {
	if (!row) return null;
	let pcEl = row.querySelector('input[type="checkbox"][id^="chkPC"], input[type="radio"][name*="PC" i], input[type="checkbox"][name*="PC" i]');
	if (!pcEl && yesEl) {
		const m2 = (yesEl.id || '').match(/(\d+)/);
		if (m2 && m2[1]) pcEl = document.querySelector(`#chkPC${m2[1]}`);
	}
	return pcEl;
}

function getPartsList() {
	return new Promise(async (resolve) => {
		const sel = await getPartsSelectors();
		const container = await waitForSelector(sel.tableContainer || sel.rowSelector, 3000, 100);
		if (!container) return resolve([]);
		let rows = (container.matches && container.matches(sel.rowSelector))
			? [container]
			: Array.from((sel.rowSelector ? container.querySelectorAll(sel.rowSelector) : [])).filter(r => r && r.offsetParent !== null);
		const names = rows.map(extractPartName).filter(n => n);
		resolve(names);
	});
}

async function runPartsTable() {
	const sel = await getPartsSelectors();
	const result = { rowsNoClicked: 0, specificYesClicked: false, diagnosisSet: false, primaryCauseClicked: false };

	// Load optional configured parts mapping and selections
	const { cfg, selections, partNumberValue } = await getPartsConfigAndSelections();
	const hasSelections = Array.isArray(selections) && selections.length > 0;

	// Wait for the table container
	const container = await waitForSelector(sel.tableContainer || sel.rowSelector, 3000, 100);
	if (!container) return result;

	// If only rowSelector provided, query from document; else query within container
	let rows = (container.matches && container.matches(sel.rowSelector))
		? [container]
		: Array.from((sel.rowSelector ? container.querySelectorAll(sel.rowSelector) : []));
	// Only operate on visible rows to avoid hidden/template entries
	rows = rows.filter((row) => row && row.offsetParent !== null);

	// Only pre-click "No" on all rows when no explicit selections were provided
	if (!hasSelections) {
		for (const row of rows) {
			try {
				const noRadio = sel.noRadioInRow ? row.querySelector(sel.noRadioInRow) : null;
				if (noRadio) {
					if (!noRadio.checked) noRadio.checked = true;
					dispatchEvents(noRadio);
					try { noRadio.click(); } catch {}
					result.rowsNoClicked += 1;
				}
			} catch {}
		}
	}

	// If we have configured selections with explicit selectors, use them; else try name-based selection
	if (selections && selections.length && Object.keys(cfg).length) {
		let primaryCauseDone = false;
		const matchedRows = new Set();
		for (const partName of selections) {
			const conf = cfg[partName];
			if (!conf || typeof conf !== 'object') continue;
			const yesEl = query(conf.yesSelector || '');
			if (!yesEl) continue;
			const row = yesEl.closest('tr') || document;
			matchedRows.add(row);
			if (!yesEl.checked) yesEl.checked = true;
			dispatchEvents(yesEl);
			try { yesEl.click(); } catch {}
			await sleep(120);
			try { if (closeDiagnosisModalIfPresent()) { await sleep(150); } } catch {}
			result.specificYesClicked = true;
			let dcEl = null;
			if (conf.diagnosisSelector) {
				try { dcEl = row.querySelector(conf.diagnosisSelector) || document.querySelector(conf.diagnosisSelector); } catch {}
			}
			if (!dcEl) dcEl = findDiagnosisSelectInRow(row, yesEl);
			if (dcEl) {
				clickElement(dcEl);
				await sleep(80);
				const chosen = setDiagnosisValue(dcEl, conf.defaultDiagnosis || '');
				if (!chosen) {
					// Bootstrap-select style fallback
					let bsBtn = row.querySelector('.bootstrap-select button.dropdown-toggle, button.dropdown-toggle[aria-haspopup="listbox"], .dropdown button');
					if (bsBtn) {
						try { bsBtn.click(); } catch {}
						await sleep(120);
						let item = Array.from(document.querySelectorAll('.dropdown-menu.show .inner li a, .dropdown-menu .inner li a, .dropdown-menu li a'))
							.find(a => (conf.defaultDiagnosis ? (a.innerText || '').trim() === conf.defaultDiagnosis : /inv\s*4/i.test(a.innerText || '')))
							|| Array.from(document.querySelectorAll('.dropdown-menu.show .inner li:not(.disabled) a, .dropdown-menu .inner li:not(.disabled) a'))[0];
						if (item) {
							try { item.click(); } catch {}
							await sleep(80);
							result.diagnosisSet = true;
							const hiddenSel = row.querySelector('select');
							if (hiddenSel) dispatchEvents(hiddenSel);
						}
						try { if (closeDiagnosisModalIfPresent()) { await sleep(100); } } catch {}
					}
					else {
						result.diagnosisSet = true;
					}
			} else {
				// No diagnosis control present on this row; consider satisfied
				result.diagnosisSet = true;
			}
		}

			// Only first checked part gets Primary Cause
			if (!primaryCauseDone) {
				let pcEl = null;
				if (conf.primaryCauseSelector) {
					try { pcEl = row.querySelector(conf.primaryCauseSelector) || document.querySelector(conf.primaryCauseSelector); } catch {}
				}
				if (!pcEl) {
					const m2 = (yesEl.id || '').match(/(\d+)/);
					if (m2 && m2[1]) pcEl = document.querySelector(`#chkPC${m2[1]}`);
				}
				if (pcEl) {
					if (!pcEl.checked) pcEl.checked = true;
					dispatchEvents(pcEl);
					clickElement(pcEl);
					result.primaryCauseClicked = true;
					primaryCauseDone = true;
				} else {
					// If no PC control exists, mark as satisfied for gating
					result.primaryCauseClicked = true;
					primaryCauseDone = true;
				}
			}

			// Sieve Tank special: fill serial if configured
			if (conf.serialSelector) {
				const serEl = row.querySelector(conf.serialSelector) || document.querySelector(conf.serialSelector);
				if (serEl) setValue(serEl, partNumberValue || '');
			}
		}
		// Ensure unselected rows are set to No
		for (const row of rows) {
			if (matchedRows.has(row)) continue;
			try {
				const noRadio = sel.noRadioInRow ? row.querySelector(sel.noRadioInRow) : null;
				if (noRadio) { if (!noRadio.checked) noRadio.checked = true; dispatchEvents(noRadio); try { noRadio.click(); } catch {} }
			} catch {}
		}
	}
	 else if (selections && selections.length) {
		// Name-based selection: match rows by normalized tokens (typo tolerant, punctuation-stripped)
		const norm = (s) => String(s || '')
			.toLowerCase()
			.replace(/pnuematic/g, 'pneumatic')
			.replace(/sieve\s+bed/g, 'sieve tank')
			.replace(/[^a-z0-9]+/g, ' ')
			.replace(/\s+/g, ' ')
			.trim();
		const tokenize = (s) => norm(s).split(' ').filter(Boolean);
		const rowsTokens = rows.map((row) => {
			const nameRaw = extractPartName(row);
			return { row, name: nameRaw, tokens: tokenize(nameRaw) };
		});
		let primaryCauseDone = false;
		const matchedRows = new Set();
		for (const partName of selections) {
			const selTokens = tokenize(partName);
			// Find first row that contains all selected tokens
			const match = rowsTokens.find(rt => selTokens.every(t => rt.tokens.includes(t)));
			const row = match?.row;
			if (!row) continue;
			matchedRows.add(row);
			const yesEl = findYesRadioInRow(row);
			if (!yesEl) continue;
			if (!yesEl.checked) yesEl.checked = true;
			dispatchEvents(yesEl);
			try { yesEl.click(); } catch {}
			await sleep(120);
			try { if (closeDiagnosisModalIfPresent()) { await sleep(150); } } catch {}
			result.specificYesClicked = true;

			let dcEl = findDiagnosisSelectInRow(row, yesEl);
			if (dcEl) {
				clickElement(dcEl);
				await sleep(80);
				const desired = PARTS_DEFAULT_CODES[partName] || '';
				let chosen = false;
				if (desired) {
					chosen = setDiagnosisValue(dcEl, desired);
				}
				if (!chosen) {
					// Try bootstrap-style dropdown menu first
					let bsBtn = row.querySelector('.bootstrap-select button.dropdown-toggle, button.dropdown-toggle[aria-haspopup="listbox"], .dropdown button');
					if (bsBtn) {
						try { bsBtn.click(); } catch {}
						await sleep(120);
						let item = Array.from(document.querySelectorAll('.dropdown-menu.show .inner li a, .dropdown-menu .inner li a, .dropdown-menu li a'))
							.find(a => desired ? (a.innerText || '').trim().toLowerCase() === desired.toLowerCase() : /inv\s*4/i.test(a.innerText || ''))
							|| Array.from(document.querySelectorAll('.dropdown-menu.show .inner li:not(.disabled) a, .dropdown-menu .inner li:not(.disabled) a'))[0];
						if (item) {
							try { item.click(); } catch {}
							await sleep(80);
							result.diagnosisSet = true;
							const hiddenSel = row.querySelector('select');
							if (hiddenSel) dispatchEvents(hiddenSel);
						} else {
							// Fallback: select first non-empty option from hidden select
							const opts = Array.from(dcEl.options || []);
							const firstValid = opts.find(o => (o.value || '').trim() && !/select/i.test(o.textContent || '')) || opts[0];
							if (firstValid) { try { firstValid.selected = true; } catch {} dispatchEvents(dcEl); result.diagnosisSet = true; }
						}
						try { if (closeDiagnosisModalIfPresent()) { await sleep(100); } } catch {}
					} else {
						// No bootstrap: pick first sensible option if desired not matched
						const opts = Array.from(dcEl.options || []);
						const firstValid = opts.find(o => (o.value || '').trim() && !/select/i.test(o.textContent || '')) || opts[0];
						if (firstValid) { try { firstValid.selected = true; } catch {} dispatchEvents(dcEl); result.diagnosisSet = true; }
					}
				} else {
					result.diagnosisSet = true;
				}
			} else {
				// No diagnosis selector present for this row
				result.diagnosisSet = true;
			}

			if (!primaryCauseDone) {
				const pcEl = findPrimaryCauseInRow(row, yesEl);
				if (pcEl) { if (!pcEl.checked) pcEl.checked = true; dispatchEvents(pcEl); clickElement(pcEl); result.primaryCauseClicked = true; primaryCauseDone = true; }
				else { result.primaryCauseClicked = true; primaryCauseDone = true; }
			}

			// Fill Sieve Tank/Bed serial when applicable
			if (/sieve\s*(tank|bed)/i.test(partName)) {
				const serEl = row.querySelector('input[type="text"][name*="serial" i], input[name*="serialvalue" i], input[id*="serial" i]');
				if (serEl) setValue(serEl, partNumberValue || '');
			}
		}
		// Ensure any non-matched row is explicitly set to No
		for (const row of rows) {
			if (matchedRows.has(row)) continue;
			try {
				const noRadio = sel.noRadioInRow ? row.querySelector(sel.noRadioInRow) : null;
				if (noRadio) { if (!noRadio.checked) noRadio.checked = true; dispatchEvents(noRadio); try { noRadio.click(); } catch {} }
			} catch {}
		}
	} else {
		// No selections provided: do not auto-select any part; respect "No" pre-clicks only
	}

	return result;
}

// Provide parts names to popup for rendering checkboxes
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (!message || !message.action) return;
	if (message.action === 'GET_PARTS_LIST') {
		getPartsList()
			.then((parts) => sendResponse({ ok: true, parts }))
			.catch((err) => sendResponse({ ok: false, error: String(err) }));
		return true;
	}
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (!message || !message.action) return;
	if (message.action === 'RUN_PARTS_TABLE') {
		runPartsTable()
			.then((res) => sendResponse({ ok: true, results: res }))
			.catch((err) => sendResponse({ ok: false, error: String(err) }));
		return true;
	}
});

// ---------------- Serial Popup Section ----------------
const SERIAL_POPUP_SELECTORS = {
	confirmCheckbox: '#chkConfirmRepair',
	serialInput: 'input[name="serial"]',
	submitBtn: '#partsConfirm',
};

function getSerialSelectors() {
	return new Promise((resolve) => {
		try {
			chrome.storage?.sync?.get('serialPopupSelectors', (res) => {
				const cfg = res?.serialPopupSelectors;
				if (cfg && typeof cfg === 'object') {
					resolve({ ...SERIAL_POPUP_SELECTORS, ...cfg });
				} else {
					resolve(SERIAL_POPUP_SELECTORS);
				}
			});
		} catch {
			resolve(SERIAL_POPUP_SELECTORS);
		}
	});
}

async function runSerialPopup(partNumberOverride) {
	const sel = await getSerialSelectors();
	const result = { checkboxClicked: false, serialFilled: false, submitted: false, value: '' };
	let partNumber = partNumberOverride;
	if (!partNumber) {
		try {
			const store = await new Promise((resolve) => chrome.storage?.sync?.get('partNumberValue', resolve));
			partNumber = store?.partNumberValue || '';
		} catch {}
	}
	result.value = String(partNumber || '');

	if (sel.confirmCheckbox) {
		const cb = await waitForSelector(sel.confirmCheckbox, 3000, 100);
		if (cb) {
			if (!cb.checked) cb.checked = true;
			dispatchEvents(cb);
			clickElement(cb);
			result.checkboxClicked = true;
			// Allow popup/modal to render before targeting its input
			await sleep(500);
		}
	}

	if (sel.serialInput) {
		let input = await waitForSelector(sel.serialInput, 5000, 100);
		// If the configured selector hits a hidden field, try to find a visible text input named serial
		const isHidden = (el) => !el || el.type === 'hidden' || el.offsetParent === null || el.closest('[hidden]');
		if (!input || isHidden(input)) {
			const candidates = Array.from(document.querySelectorAll('input[type="text"][name="serial"], input[name="serial"]'))
				.filter((el) => el.type !== 'hidden' && el.offsetParent !== null && !el.disabled);
			if (candidates.length) input = candidates[0];
		}
		if (input) {
			setValue(input, partNumber || '');
			try { input.focus(); } catch {}
			dispatchEvents(input);
			// Press Enter to accept when applicable
			sendKey(input, 'Enter');
			result.serialFilled = true;
		}
	}

	if (sel.submitBtn) {
		// Short pause to allow bindings to register the entered serial
		await sleep(300);

		const isVisible = (el) => {
			if (!el) return false;
			const rect = el.getBoundingClientRect?.();
			const style = window.getComputedStyle?.(el);
			const visibleStyle = style ? (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && style.pointerEvents !== 'none') : true;
			return (el.offsetParent !== null || (rect && rect.width > 0 && rect.height > 0)) && visibleStyle;
		};
		const isEnabled = (el) => el && !el.disabled && el.getAttribute('disabled') == null && el.getAttribute('aria-disabled') !== 'true';

		const findConfirmButton = () => {
			// Primary: configured selector
			let el = null;
			try { el = document.querySelector(sel.submitBtn); } catch {}
			if (el && isVisible(el) && isEnabled(el)) return el;
			// Alternative: by id
			const byId = document.getElementById('partsConfirm');
			if (isVisible(byId) && isEnabled(byId)) return byId;
			// Within open modal/dialog
			const modal = document.querySelector('.modal.show, .modal.in, [role="dialog"]');
			const scope = modal || document;
			const candidates = Array.from(scope.querySelectorAll('.row button#partsConfirm, button#partsConfirm, button, input[type="button"], input[type="submit"]'))
				.filter((e) => isVisible(e) && isEnabled(e));
			const byText = candidates.find((e) => (e.innerText || e.value || '').trim().toLowerCase() === 'confirm');
			if (byText) return byText;
			return null;
		};

		// Poll up to 3000ms for a visible & enabled confirm button, click when found
		const start = Date.now();
		let btn = findConfirmButton();
		while ((!btn || !isVisible(btn) || !isEnabled(btn)) && Date.now() - start < 3000) {
			await sleep(150);
			btn = findConfirmButton();
		}

		if (btn) {
			for (let i = 0; i < 3; i++) {
				robustClick(btn);
				await sleep(150);
				// Heuristic: if modal/dialog disappears, assume success
				const modalNow = document.querySelector('.modal.show, .modal.in, [role="dialog"]');
				if (!modalNow || !isVisible(modalNow)) {
					result.submitted = true;
					break;
				}
			}
			// Last resort: trigger inline handler via attribute or global function
			if (!result.submitted) {
				const handler = btn.getAttribute('onclick');
				if (handler && typeof window.Function === 'function') {
					try { new Function(handler).call(window); result.submitted = true; } catch {}
				}
			}
			if (!result.submitted && typeof window.MFWpartsConfirmed === 'function') {
				try { window.MFWpartsConfirmed(); result.submitted = true; } catch {}
			}

			// If still not submitted, inject into page context to call the handler/click directly
			if (!result.submitted) {
				const injected = runInPage(`(function(){try{ if (typeof MFWpartsConfirmed === 'function') { MFWpartsConfirmed(); } else { var b=document.getElementById('partsConfirm'); if(b){ b.click(); } } }catch(e){}})();`);
				if (injected) {
					await sleep(200);
					const modalNow2 = document.querySelector('.modal.show, .modal.in, [role="dialog"]');
					if (!modalNow2 || !isVisible(modalNow2)) result.submitted = true;
				}
			}
			// If we encountered a validation modal for missing Diagnosis Codes, handle and retry once
			if (!result.submitted) {
				const diagModal = Array.from(document.querySelectorAll('.modal, [role="dialog"]'))
					.find(m => /diagnosis\s*codes?\s*cannot\s*be\s*empty/i.test(m.innerText || ''));
				if (diagModal) {
					// Try closing the modal
					const closeBtn = Array.from(diagModal.querySelectorAll('button, .btn')).find(b => /close/i.test(b.innerText || b.value || '')) || diagModal.querySelector('[data-dismiss="modal"], .close');
					if (closeBtn) { try { closeBtn.click(); } catch {} }
					await sleep(200);
					// Ensure parts diagnosis is set, then try confirm again
					try { await runPartsTable(); } catch {}
					await sleep(300);
					btn = findConfirmButton();
					if (btn) {
						robustClick(btn);
						await sleep(250);
						const modalNow3 = document.querySelector('.modal.show, .modal.in, [role="dialog"]');
						if (!modalNow3 || !isVisible(modalNow3)) result.submitted = true;
					}
				}
			}
		}
	}

	return result;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (!message || !message.action) return;
	if (message.action === 'RUN_SERIAL_POPUP') {
		runSerialPopup(message?.value)
			.then((res) => sendResponse({ ok: true, results: res }))
			.catch((err) => sendResponse({ ok: false, error: String(err) }));
		return true;
	}
});

// ---------------- Final Test Results Section ----------------
// Elements provided by user:
// txtFLowRateLow, txtOxygenLow, txtFLowRateMax, txtOxygenMax, txtPSI, txtHoursOut, radAlarmYes, chkFilters
const TEST_RESULTS_SELECTORS = {
	flow2: ['#txtFLowRateLow', '#txtFlowRateLow'],
	purity2: ['#txtOxygenLow'],
	flow5: ['#txtFLowRateMax', '#txtFlowRateMax'],
	purity5: ['#txtOxygenMax'],
	psi: ['#txtPSI', '#txtPsi'],
	hoursOut: ['#txtHoursOut'],
	alarmPass: ['#radAlarmYes', 'input[type="radio"][name="Alarm"][value="Pass"]'],
	filtersConfirm: ['#chkFilters', 'input[type="checkbox"]#chkFilters'],
};

async function waitForAny(selectors, timeoutMs = 4000, intervalMs = 100) {
	const list = Array.isArray(selectors) ? selectors : [selectors];
	const start = Date.now();
	while (Date.now() - start < timeoutMs) {
		for (const sel of list) {
			try {
				const el = document.querySelector(sel);
				if (el) return el;
			} catch {}
		}
		await sleep(intervalMs);
	}
	return null;
}

function setValueAndBlur(el, value) {
	const ok = setValue(el, value);
	if (el) {
		try { el.dispatchEvent(new Event('blur', { bubbles: true })); } catch {}
	}
	return ok;
}

async function runTestResults(values = {}) {
	const result = {
		filled: { flow2: false, purity2: false, flow5: false, purity5: false, psi: false, hoursOut: false },
		alarmPass: false,
		filtersChecked: false,
	};

	// Constant flows: 2.0 and 5.0
	const f2 = await waitForAny(TEST_RESULTS_SELECTORS.flow2, 5000, 100);
	if (f2) result.filled.flow2 = setValueAndBlur(f2, '2.0');

	const f5 = await waitForAny(TEST_RESULTS_SELECTORS.flow5, 5000, 100);
	if (f5) result.filled.flow5 = setValueAndBlur(f5, '5.0');

	// User-provided purities, psi, hours out
	const p2 = await waitForAny(TEST_RESULTS_SELECTORS.purity2, 5000, 100);
	if (p2) result.filled.purity2 = setValueAndBlur(p2, String(values.oxygenPurity2 ?? ''));

	const p5 = await waitForAny(TEST_RESULTS_SELECTORS.purity5, 5000, 100);
	if (p5) result.filled.purity5 = setValueAndBlur(p5, String(values.oxygenPurity5 ?? ''));

	const psi = await waitForAny(TEST_RESULTS_SELECTORS.psi, 5000, 100);
	if (psi) result.filled.psi = setValueAndBlur(psi, String(values.psi ?? ''));

	const hOut = await waitForAny(TEST_RESULTS_SELECTORS.hoursOut, 5000, 100);
	if (hOut) result.filled.hoursOut = setValueAndBlur(hOut, String(values.hoursOut ?? ''));

	// Alarm Test: Pass
	const alarm = await waitForAny(TEST_RESULTS_SELECTORS.alarmPass, 4000, 100);
	if (alarm) {
		try {
			if (!alarm.checked) alarm.checked = true;
			dispatchEvents(alarm);
			clickElement(alarm);
			result.alarmPass = true;
		} catch {}
	}

	// Install Test Filters in Unit: Confirm (checkbox)
	const filters = await waitForAny(TEST_RESULTS_SELECTORS.filtersConfirm, 4000, 100);
	if (filters) {
		try {
			if (!filters.checked) filters.checked = true;
			dispatchEvents(filters);
			clickElement(filters);
			result.filtersChecked = true;
		} catch {}
	}

	return result;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (!message || !message.action) return;
	if (message.action === 'RUN_TEST_RESULTS') {
		runTestResults(message.values || {})
			.then((res) => sendResponse({ ok: true, results: res }))
			.catch((err) => sendResponse({ ok: false, error: String(err) }));
		return true;
	}
});
