document.addEventListener('DOMContentLoaded', () => {
	// Theme handling (UI-only; no automation logic touched)
	const themeToggle = document.getElementById('themeToggle');
	const prefersDark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : { matches: true, addEventListener: () => {} };
	let themePref = 'auto'; // 'auto' | 'light' | 'dark'

	function resolveTheme(pref) {
		if (pref === 'light' || pref === 'dark') return pref;
		return prefersDark.matches ? 'dark' : 'light';
	}
	function updateToggleLabel() {
		if (!themeToggle) return;
		themeToggle.textContent = themePref === 'auto' ? 'Auto' : (themePref === 'light' ? 'Light' : 'Dark');
		themeToggle.title = `Theme: ${themeToggle.textContent}`;
	}
	function applyTheme() {
		const theme = resolveTheme(themePref);
		try { document.documentElement.setAttribute('data-theme', theme === 'light' ? 'light' : 'dark'); } catch {}
		updateToggleLabel();
	}
	function onSystemChange() {
		if (themePref === 'auto') applyTheme();
	}
	chrome.storage?.sync?.get(['uiThemePref'], (res) => {
		themePref = res?.uiThemePref || 'auto';
		applyTheme();
	});
	try { prefersDark.addEventListener?.('change', onSystemChange); } catch {}
	themeToggle?.addEventListener('click', async () => {
		themePref = themePref === 'auto' ? 'light' : (themePref === 'light' ? 'dark' : 'auto');
		try { await chrome.storage?.sync?.set({ uiThemePref: themePref }); } catch {}
		applyTheme();
	});
	const form = document.getElementById('hoursPurityForm');
	const runBtn = document.getElementById('runAutomationBtn');
	const status = document.getElementById('status');
	const hoursInput = document.getElementById('hoursIn');
	const purityInput = document.getElementById('oxygenPurity');
		const partNumberInput = document.getElementById('partNumber');
	// Final Test Results inputs
	const oxygenPurity2Input = document.getElementById('oxygenPurity2');
	const oxygenPurity5Input = document.getElementById('oxygenPurity5');
	const psiValueInput = document.getElementById('psiValue');
	const hoursOutInput = document.getElementById('hoursOut');
	const saveValuesBtn = document.getElementById('saveValuesBtn');
	const runPartsBtn = document.getElementById('runPartsBtn');
	const runSerialBtn = document.getElementById('runSerialBtn');
	const runPartsSerialBtn = document.getElementById('runPartsSerialBtn');
	// Removed separate confirm button; combined into run
	const selHours = document.getElementById('hpSelHours');
	const selPurity = document.getElementById('hpSelPurity');
	const selSubmit = document.getElementById('hpSelSubmit');
	const selYes = document.getElementById('cpSelYes');
	const selNo = document.getElementById('cpSelNo');
	const saveBtn = document.getElementById('hpSaveSelectors');
	const clearBtn = document.getElementById('hpClearSelectors');
	const selectorStatus = document.getElementById('selectorStatus');

	// Parts selections UI elements
	const partsCheckboxes = document.getElementById('partsCheckboxes');
	const refreshPartsBtn = document.getElementById('refreshPartsBtn');
	const savePartsSelectionsBtn = document.getElementById('savePartsSelectionsBtn');
	const clearPartsSelectionsBtn = document.getElementById('clearPartsSelectionsBtn');
	const partsStatus = document.getElementById('partsStatus');

	// Starter list to ensure preselection is possible before first detection
	const DEFAULT_PART_NAMES = [
		'Sieve bed Refurbished',
		'Regulator valve',
		'Pnuematic valve',
		'Compressor',
		'Control Board',
		'No Part Needed',
	];

	const DEFAULT_SELECTORS = {
		hoursIn: '#txtHoursIn',
		oxygenPurity: '#txtO2In',
		submit: '#start',
	};

	const DEFAULT_CONFIRM_SELECTORS = {
		confirmIssueYes: '#radConfirmIssue',
		smokeNo: '#radSmokeNo',
	};

	const DEFAULT_FAILURE_SELECTORS = {
		q1Radio: '#radRepairYes',
		q2Radio: '#radAbuseNo',
		firstCheckbox: '#1',
		reasonsContainer: '',
		confirmBtn: '#btnRepairStatus',
	};

	const DEFAULT_PARTS_SELECTORS = {
		tableContainer: '#tblParts',
		rowSelector: 'tbody tr',
		noRadioInRow: 'input[id^="radPartNo"]',
		specificYesSelector: '#radPartYes175243',
	};

		const DEFAULT_SERIAL_SELECTORS = {
			confirmCheckbox: '#chkConfirmRepair',
			serialInput: 'input[name="serial"]',
			submitBtn: '#partsConfirm',
		};

	function setPartsStatus(msg, ok = true) {
		if (!partsStatus) return;
		partsStatus.textContent = msg;
		partsStatus.style.color = ok ? 'green' : 'red';
	}

	function renderPartsCheckboxesFromNames(names = [], selections = []) {
		if (!partsCheckboxes) return;
		partsCheckboxes.innerHTML = '';
		try {
			const keys = Array.isArray(names) ? names : [];
			if (!keys.length) {
				const p = document.createElement('div');
				p.textContent = 'No parts found. Ensure the parts table is visible, then click “Refresh Parts List”.';
				p.style.color = '#666';
				partsCheckboxes.appendChild(p);
				return;
			}
			for (const key of keys) {
				const id = `partsChk_${String(key).replace(/[^a-z0-9]+/gi, '_')}`;
				const row = document.createElement('label');
				row.style.fontSize = '12px';
				const cb = document.createElement('input');
				cb.type = 'checkbox';
				cb.id = id;
				cb.checked = Array.isArray(selections) && selections.includes(key);
				cb.dataset.partKey = key;
				row.appendChild(cb);
				row.append(` ${key}`);
				partsCheckboxes.appendChild(row);
			}
		} catch (e) {
			// ignore render errors
		}
	}

	async function loadPartsList() {
		try {
			const { partsSelections } = await new Promise((resolve) => chrome.storage?.sync?.get(['partsSelections'], resolve));
			// Always render fixed six-item list to preserve selections
			renderPartsCheckboxesFromNames(DEFAULT_PART_NAMES, Array.isArray(partsSelections) ? partsSelections : []);
			setPartsStatus('Loaded 6 parts (fixed list)');
		} catch (e) {
			setPartsStatus(String(e), false);
		}
	}

	function setStatus(msg, ok = true) {
		if (!status) return;
		status.textContent = msg;
		status.style.color = ok ? 'green' : 'red';
	}

	function sleep(ms) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}

	async function getActiveTab() {
		const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
		return tabs[0];
	}

	async function closeDiagnosisModal(tabId) {
		try {
			const [{ result } = {}] = await chrome.scripting.executeScript({
				target: { tabId, allFrames: true },
				world: 'MAIN',
				func: () => {
					const modals = Array.from(document.querySelectorAll('.modal, [role="dialog"]'));
					const diag = modals.find(m => /diagnosis\s*codes?\s*cannot\s*be\s*empty/i.test(m.innerText || ''));
					if (!diag) return false;
					const closeBtn = Array.from(diag.querySelectorAll('button, .btn, [data-dismiss="modal"], .close'))
						.find(b => /close/i.test(b.innerText || b.value || '') || b.hasAttribute?.('data-dismiss') || b.classList?.contains('close'));
					try { closeBtn?.click(); } catch {}
					return true;
				}
			});
			return !!result;
		} catch {
			return false;
		}
	}

	async function sendFillFinalSection(values) {
		const tab = await getActiveTab();
		if (!tab?.id) {
			setStatus('No active tab found', false);
			return;
		}
		try {
			const response = await chrome.tabs.sendMessage(tab.id, { action: 'RUN_TEST_RESULTS', values });
			if (response?.ok) {
				setStatus('Final Test Results filled');
			} else {
				setStatus(response?.error || 'Could not fill final section', false);
			}
		} catch (e) {
			setStatus(String(e), false);
		}
	}

	async function sendFill(hoursIn, oxygenPurity) {
		const tab = await getActiveTab();
		if (!tab?.id) {
			setStatus('No active tab found', false);
			return;
		}
		try {
			const response = await chrome.tabs.sendMessage(tab.id, {
				action: 'FILL_HOURS_AND_PURITY',
				values: { hoursIn, oxygenPurity },
			});
			if (response?.ok) {
				setStatus('Filled and submitted');
			} else {
				setStatus(response?.error || 'Unknown error', false);
			}
		} catch (e) {
			setStatus(String(e), false);
		}
	}

	async function runPartsOnly() {
		const tab = await getActiveTab();
		if (!tab?.id) { setStatus('No active tab found', false); return; }
		try {
			// Small pre-delay to let dynamic tables render
			await sleep(250);
			const resp = await chrome.tabs.sendMessage(tab.id, { action: 'RUN_PARTS_TABLE' });
			if (resp?.ok) {
				setStatus('Parts table completed');
				return true;
			} else {
				setStatus(resp?.error || 'Error running parts table', false);
				return false;
			}
		} catch (e) {
			setStatus(String(e), false);
			return false;
		}
	}

	async function runSerialOnly() {
		const tab = await getActiveTab();
		if (!tab?.id) { setStatus('No active tab found', false); return; }
		const partNumber = partNumberInput?.value || '';
		try {
			await chrome.storage.sync.set({ partNumberValue: partNumber });
			const resp = await chrome.tabs.sendMessage(tab.id, { action: 'RUN_SERIAL_POPUP', value: partNumber });
			if (!resp?.ok) { setStatus(resp?.error || 'Error running serial popup', false); return false; }
			// Main-world confirm click for reliability
			await chrome.scripting.executeScript({
				target: { tabId: tab.id, allFrames: true },
				world: 'MAIN',
				func: (selector) => {
					const sleep = (ms) => new Promise(r => setTimeout(r, ms));
					const isVisible = (el) => {
						if (!el) return false;
						const rect = el.getBoundingClientRect?.();
						const style = window.getComputedStyle?.(el);
						const visibleStyle = style ? (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && style.pointerEvents !== 'none') : true;
						return (el.offsetParent !== null || (rect && rect.width > 0 && rect.height > 0)) && visibleStyle && !el.disabled;
					};
					const findBtn = () => {
						let el = null;
						try { el = document.querySelector(selector); } catch {}
						if (isVisible(el)) return el;
						const byId = document.getElementById('partsConfirm');
						if (isVisible(byId)) return byId;
						const modal = document.querySelector('.modal.show, .modal.in, [role="dialog"]');
						const scope = modal || document;
						const candidates = Array.from(scope.querySelectorAll('.row button#partsConfirm, button#partsConfirm, button, input[type="button"], input[type="submit"]')).filter(isVisible);
						const byText = candidates.find((e) => (e.innerText || e.value || '').trim().toLowerCase() === 'confirm');
						return byText || null;
					};
					(async () => {
						await sleep(250);
						let btn = findBtn();
						const start = Date.now();
						while (!btn && Date.now() - start < 2000) { await sleep(150); btn = findBtn(); }
						if (btn) { try { btn.scrollIntoView({ block: 'center', inline: 'center' }); } catch {} try { btn.focus(); } catch {} try { btn.click(); } catch {} try { btn.dispatchEvent(new MouseEvent('click', { bubbles: true })); } catch {} if (typeof window.MFWpartsConfirmed === 'function') { try { window.MFWpartsConfirmed(); } catch {} } }
					})();
				},
				args: ['#partsConfirm']
			});
			setStatus('Serial filled and confirmed');
			return true;
		} catch (e) {
			setStatus(String(e), false);
			return false;
		}
	}

	async function runPartsSerial() {
		setStatus('Running parts + serial...');
		const okParts = await runPartsOnly();
		if (!okParts) return;
		await sleep(250);
		const okSerial = await runSerialOnly();
		if (okSerial) setStatus('Parts + serial completed');
	}

	runBtn?.addEventListener('click', async (e) => {
		e.preventDefault();
		const hoursIn = hoursInput?.value || '';
		const oxygenPurity = purityInput?.value || '';
		const partNumber = partNumberInput?.value || '';
		const testResults = {
			oxygenPurity2: oxygenPurity2Input?.value || '',
			oxygenPurity5: oxygenPurity5Input?.value || '',
			psi: psiValueInput?.value || '',
			hoursOut: hoursOutInput?.value || '',
		};
		// Step 1: fill + submit hours/purity
		await sendFill(hoursIn, oxygenPurity);
		// Step 2: set radios yes/no (no submit)
		const tab = await getActiveTab();
		if (!tab?.id) {
			setStatus('No active tab found', false);
			return;
		}
		try {
			const response1 = await chrome.tabs.sendMessage(tab.id, { action: 'CONFIRM_REPORTED_PROBLEM' });
			if (!response1?.ok) {
				setStatus(response1?.error || 'Error running confirm section', false);
				return;
			}
			// Step 3: run failure reason
			const response2 = await chrome.tabs.sendMessage(tab.id, { action: 'RUN_FAILURE_REASON' });
			if (!response2?.ok) {
				setStatus(response2?.error || 'Error running failure reason', false);
				return;
			}
			// Allow parts table to fully render
			await sleep(600);
			// Step 4: run parts table
			let response3 = await chrome.tabs.sendMessage(tab.id, { action: 'RUN_PARTS_TABLE' });
			if (!response3?.ok || !response3?.results?.specificYesClicked || !response3?.results?.diagnosisSet || !response3?.results?.primaryCauseClicked) {
				// If we hit the diagnosis modal, close and retry once
				await closeDiagnosisModal(tab.id);
				await sleep(400);
				response3 = await chrome.tabs.sendMessage(tab.id, { action: 'RUN_PARTS_TABLE' });
				if (!response3?.ok) {
					setStatus(response3?.error || 'Error running parts table', false);
					return;
				}
			}
			// Brief settle after table interactions
			await sleep(350);
			// Ensure no blocking modal is open before serial
			await closeDiagnosisModal(tab.id);
			// Step 5: run serial popup (fill + confirm)
			try { await chrome.storage.sync.set({ partNumberValue: partNumber }); } catch {}
			const response4 = await chrome.tabs.sendMessage(tab.id, { action: 'RUN_SERIAL_POPUP', value: partNumber });
			if (!response4?.ok) {
				setStatus(response4?.error || 'Error running serial popup', false);
				return;
			}
			// MAIN-world confirm click to ensure page handler fires
			try {
				await chrome.scripting.executeScript({
					target: { tabId: tab.id, allFrames: true },
					world: 'MAIN',
					func: (selector) => {
						const sleep = (ms) => new Promise(r => setTimeout(r, ms));
						const isVisible = (el) => {
							if (!el) return false;
							const rect = el.getBoundingClientRect?.();
							const style = window.getComputedStyle?.(el);
							const visibleStyle = style ? (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && style.pointerEvents !== 'none') : true;
							return (el.offsetParent !== null || (rect && rect.width > 0 && rect.height > 0)) && visibleStyle && !el.disabled;
						};
						const findBtn = () => {
							let el = null;
							try { el = document.querySelector(selector); } catch {}
							if (isVisible(el)) return el;
							const byId = document.getElementById('partsConfirm');
							if (isVisible(byId)) return byId;
							const modal = document.querySelector('.modal.show, .modal.in, [role="dialog"]');
							const scope = modal || document;
							const candidates = Array.from(scope.querySelectorAll('.row button#partsConfirm, button#partsConfirm, button, input[type="button"], input[type="submit"]'))
								.filter(isVisible);
							const byText = candidates.find((e) => (e.innerText || e.value || '').trim().toLowerCase() === 'confirm');
							return byText || null;
						};
						(async () => {
							await sleep(250);
							let btn = findBtn();
							const start = Date.now();
							while (!btn && Date.now() - start < 2000) {
								await sleep(150);
								btn = findBtn();
							}
							if (btn) {
								try { btn.scrollIntoView({ block: 'center', inline: 'center' }); } catch {}
								try { btn.focus(); } catch {}
								try { btn.click(); } catch {}
								try { btn.dispatchEvent(new MouseEvent('click', { bubbles: true })); } catch {}
								if (typeof window.MFWpartsConfirmed === 'function') {
									try { window.MFWpartsConfirmed(); } catch {}
								}
							}
						})();
					},
					args: ['#partsConfirm']
				});
			} catch {}
			// Allow confirm action to finalize and UI to update
			await sleep(1200);
			// Final step: fill Final Test Results (same as standalone button)
			await sendFillFinalSection(testResults);
			setStatus('Automation complete');
		} catch (e2) {
			setStatus(String(e2), false);
		}
	});

	// Save button: persist values without submitting
		saveValuesBtn?.addEventListener('click', async () => {
		const hoursIn = hoursInput?.value || '';
		const oxygenPurity = purityInput?.value || '';
			const partNumber = partNumberInput?.value || '';
			const testResults = {
				oxygenPurity2: oxygenPurity2Input?.value || '',
				oxygenPurity5: oxygenPurity5Input?.value || '',
				psi: psiValueInput?.value || '',
				hoursOut: hoursOutInput?.value || '',
			};
		try {
				await chrome.storage.sync.set({ hoursPurityValues: { hoursIn, oxygenPurity }, partNumberValue: partNumber, testResultsValues: testResults });
			setStatus('Values saved');
		} catch (e) {
			setStatus(String(e), false);
		}
	});

	// Standalone: Run only the Parts Table step
	runPartsBtn?.addEventListener('click', runPartsOnly);

	// Standalone: Run only the Serial Fill step
	runSerialBtn?.addEventListener('click', runSerialOnly);

	// Combined: Run Parts then Serial
	runPartsSerialBtn?.addEventListener('click', runPartsSerial);

	// Standalone button removed; Run Automation calls sendFillFinalSection internally

	// Load last-used values on popup open
	chrome.storage?.sync?.get(['hoursPurityValues','partNumberValue','testResultsValues'], (res) => {
		const v = res?.hoursPurityValues;
		if (v && typeof v === 'object') {
			if (hoursInput && v.hoursIn != null) hoursInput.value = String(v.hoursIn);
			if (purityInput && v.oxygenPurity != null) purityInput.value = String(v.oxygenPurity);
		}
		const pn = res?.partNumberValue;
		if (partNumberInput && pn != null) partNumberInput.value = String(pn);
		const tr = res?.testResultsValues;
		if (tr && typeof tr === 'object') {
			if (oxygenPurity2Input && tr.oxygenPurity2 != null) oxygenPurity2Input.value = String(tr.oxygenPurity2);
			if (oxygenPurity5Input && tr.oxygenPurity5 != null) oxygenPurity5Input.value = String(tr.oxygenPurity5);
			if (psiValueInput && tr.psi != null) psiValueInput.value = String(tr.psi);
			if (hoursOutInput && tr.hoursOut != null) hoursOutInput.value = String(tr.hoursOut);
		}
	});

	// Selector storage helpers
	function setSelectorStatus(msg, ok = true) {
		if (!selectorStatus) return;
		selectorStatus.textContent = msg;
		selectorStatus.style.color = ok ? 'green' : 'red';
	}

	function populateSelectorInputs(values) {
		if (selHours) selHours.value = values.hoursIn || '';
		if (selPurity) selPurity.value = values.oxygenPurity || '';
		if (selSubmit) selSubmit.value = values.submit || '';
	}

	function populateConfirmSelectorInputs(values) {
		if (selYes) selYes.value = values.confirmIssueYes || '';
		if (selNo) selNo.value = values.smokeNo || '';
	}

		chrome.storage?.sync?.get(['hoursPuritySelectors', 'confirmProblemSelectors', 'failureReasonSelectors', 'partsTableSelectors', 'serialPopupSelectors', 'hoursPurityValues', 'partNumberValue', 'partsSelections'], async (res) => {
		const hpStored = res?.hoursPuritySelectors;
		if (hpStored && typeof hpStored === 'object') {
			populateSelectorInputs({ ...DEFAULT_SELECTORS, ...hpStored });
		} else {
			populateSelectorInputs(DEFAULT_SELECTORS);
		}

		const cpStored = res?.confirmProblemSelectors;
		if (cpStored && typeof cpStored === 'object') {
			populateConfirmSelectorInputs({ ...DEFAULT_CONFIRM_SELECTORS, ...cpStored });
		} else {
			populateConfirmSelectorInputs(DEFAULT_CONFIRM_SELECTORS);
		}

		const frStored = res?.failureReasonSelectors;
		if (frStored && typeof frStored === 'object') {
			const q1 = document.getElementById('frSelQ1');
			const q2 = document.getElementById('frSelQ2');
			const cb = document.getElementById('frSelCheckbox');
			const cont = document.getElementById('frSelContainer');
			const conf = document.getElementById('frSelConfirm');
			if (q1) q1.value = frStored.q1Radio || '';
			if (q2) q2.value = frStored.q2Radio || '';
			if (cb) cb.value = frStored.firstCheckbox || '';
			if (cont) cont.value = frStored.reasonsContainer || '';
			if (conf) conf.value = frStored.confirmBtn || '';
		} else {
			const q1 = document.getElementById('frSelQ1');
			const q2 = document.getElementById('frSelQ2');
			const cb = document.getElementById('frSelCheckbox');
			const cont = document.getElementById('frSelContainer');
			const conf = document.getElementById('frSelConfirm');
			if (q1) q1.value = DEFAULT_FAILURE_SELECTORS.q1Radio;
			if (q2) q2.value = DEFAULT_FAILURE_SELECTORS.q2Radio;
			if (cb) cb.value = DEFAULT_FAILURE_SELECTORS.firstCheckbox;
			if (cont) cont.value = DEFAULT_FAILURE_SELECTORS.reasonsContainer;
			if (conf) conf.value = DEFAULT_FAILURE_SELECTORS.confirmBtn;
		}

		const v = res?.hoursPurityValues;
		if (v && typeof v === 'object') {
			if (hoursInput && v.hoursIn != null) hoursInput.value = String(v.hoursIn);
			if (purityInput && v.oxygenPurity != null) purityInput.value = String(v.oxygenPurity);
		}
		const pn = res?.partNumberValue;
		if (partNumberInput && pn != null) partNumberInput.value = String(pn);
		const tr = res?.testResultsValues;
		if (tr && typeof tr === 'object') {
			if (oxygenPurity2Input) oxygenPurity2Input.value = String(tr.oxygenPurity2 || '');
			if (oxygenPurity5Input) oxygenPurity5Input.value = String(tr.oxygenPurity5 || '');
			if (psiValueInput) psiValueInput.value = String(tr.psi || '');
			if (hoursOutInput) hoursOutInput.value = String(tr.hoursOut || '');
		}

		const ptStored = res?.partsTableSelectors;
		const c = document.getElementById('ptSelContainer');
		const r = document.getElementById('ptSelRow');
		const n = document.getElementById('ptSelNo');
		const y = document.getElementById('ptSelSpecificYes');
		if (ptStored && typeof ptStored === 'object') {
			if (c) c.value = ptStored.tableContainer || DEFAULT_PARTS_SELECTORS.tableContainer;
			if (r) r.value = ptStored.rowSelector || DEFAULT_PARTS_SELECTORS.rowSelector;
			if (n) n.value = ptStored.noRadioInRow || DEFAULT_PARTS_SELECTORS.noRadioInRow;
			if (y) y.value = ptStored.specificYesSelector || DEFAULT_PARTS_SELECTORS.specificYesSelector;
		} else {
			if (c) c.value = DEFAULT_PARTS_SELECTORS.tableContainer;
			if (r) r.value = DEFAULT_PARTS_SELECTORS.rowSelector;
			if (n) n.value = DEFAULT_PARTS_SELECTORS.noRadioInRow;
			if (y) y.value = DEFAULT_PARTS_SELECTORS.specificYesSelector;
			// Persist defaults once for convenience
			chrome.storage?.sync?.set({ partsTableSelectors: DEFAULT_PARTS_SELECTORS });
		}

		// Serial popup selectors
		const spStored = res?.serialPopupSelectors;
		const spC = document.getElementById('spSelCheckbox');
		const spS = document.getElementById('spSelSerial');
		const spB = document.getElementById('spSelSubmit');
		if (spStored && typeof spStored === 'object') {
			if (spC) spC.value = spStored.confirmCheckbox || DEFAULT_SERIAL_SELECTORS.confirmCheckbox;
			if (spS) spS.value = spStored.serialInput || DEFAULT_SERIAL_SELECTORS.serialInput;
			if (spB) spB.value = spStored.submitBtn || DEFAULT_SERIAL_SELECTORS.submitBtn;
		} else {
			if (spC) spC.value = DEFAULT_SERIAL_SELECTORS.confirmCheckbox;
			if (spS) spS.value = DEFAULT_SERIAL_SELECTORS.serialInput;
			if (spB) spB.value = DEFAULT_SERIAL_SELECTORS.submitBtn;
			// Persist defaults once for convenience
			chrome.storage?.sync?.set({ serialPopupSelectors: DEFAULT_SERIAL_SELECTORS });
		}

		// Initial load of parts list
		await loadPartsList();
	});

	// Refresh simply re-renders the fixed list and applies saved selections
	refreshPartsBtn?.addEventListener('click', loadPartsList);

	saveBtn?.addEventListener('click', async () => {
		const payload = {
			hoursIn: selHours?.value?.trim() || DEFAULT_SELECTORS.hoursIn,
			oxygenPurity: selPurity?.value?.trim() || DEFAULT_SELECTORS.oxygenPurity,
			submit: selSubmit?.value?.trim() || DEFAULT_SELECTORS.submit,
		};
		const confirmPayload = {
			confirmIssueYes: selYes?.value?.trim() || DEFAULT_CONFIRM_SELECTORS.confirmIssueYes,
			smokeNo: selNo?.value?.trim() || DEFAULT_CONFIRM_SELECTORS.smokeNo,
		};
		const frPayload = {
			q1Radio: document.getElementById('frSelQ1')?.value?.trim() || DEFAULT_FAILURE_SELECTORS.q1Radio,
			q2Radio: document.getElementById('frSelQ2')?.value?.trim() || DEFAULT_FAILURE_SELECTORS.q2Radio,
			firstCheckbox: document.getElementById('frSelCheckbox')?.value?.trim() || DEFAULT_FAILURE_SELECTORS.firstCheckbox,
			reasonsContainer: document.getElementById('frSelContainer')?.value?.trim() || DEFAULT_FAILURE_SELECTORS.reasonsContainer,
			confirmBtn: document.getElementById('frSelConfirm')?.value?.trim() || DEFAULT_FAILURE_SELECTORS.confirmBtn,
		};
		try {
			await chrome.storage.sync.set({
				hoursPuritySelectors: payload,
				confirmProblemSelectors: confirmPayload,
				failureReasonSelectors: frPayload,
				partsTableSelectors: {
					tableContainer: document.getElementById('ptSelContainer')?.value?.trim() || '',
					rowSelector: document.getElementById('ptSelRow')?.value?.trim() || '',
					noRadioInRow: document.getElementById('ptSelNo')?.value?.trim() || '',
					specificYesSelector: document.getElementById('ptSelSpecificYes')?.value?.trim() || '',
				},
					serialPopupSelectors: {
						confirmCheckbox: document.getElementById('spSelCheckbox')?.value?.trim() || DEFAULT_SERIAL_SELECTORS.confirmCheckbox,
						serialInput: document.getElementById('spSelSerial')?.value?.trim() || DEFAULT_SERIAL_SELECTORS.serialInput,
						submitBtn: document.getElementById('spSelSubmit')?.value?.trim() || DEFAULT_SERIAL_SELECTORS.submitBtn,
					},
			});
			setSelectorStatus('Selectors saved');
		} catch (e) {
			setSelectorStatus(String(e), false);
		}
	});

	clearBtn?.addEventListener('click', async () => {
		try {
				await chrome.storage.sync.remove(['hoursPuritySelectors', 'confirmProblemSelectors', 'failureReasonSelectors', 'partsTableSelectors', 'serialPopupSelectors']);
			populateSelectorInputs(DEFAULT_SELECTORS);
			populateConfirmSelectorInputs(DEFAULT_CONFIRM_SELECTORS);
			// Reset parts selectors to defaults in UI and storage
			const c = document.getElementById('ptSelContainer');
			const r = document.getElementById('ptSelRow');
			const n = document.getElementById('ptSelNo');
			const y = document.getElementById('ptSelSpecificYes');
			if (c) c.value = DEFAULT_PARTS_SELECTORS.tableContainer;
			if (r) r.value = DEFAULT_PARTS_SELECTORS.rowSelector;
			if (n) n.value = DEFAULT_PARTS_SELECTORS.noRadioInRow;
			if (y) y.value = DEFAULT_PARTS_SELECTORS.specificYesSelector;
			await chrome.storage.sync.set({ partsTableSelectors: DEFAULT_PARTS_SELECTORS });
				// Reset serial popup selectors
				const spC = document.getElementById('spSelCheckbox');
				const spS = document.getElementById('spSelSerial');
				const spB = document.getElementById('spSelSubmit');
				if (spC) spC.value = DEFAULT_SERIAL_SELECTORS.confirmCheckbox;
				if (spS) spS.value = DEFAULT_SERIAL_SELECTORS.serialInput;
				if (spB) spB.value = DEFAULT_SERIAL_SELECTORS.submitBtn;
				await chrome.storage.sync.set({ serialPopupSelectors: DEFAULT_SERIAL_SELECTORS });
				// Clear parts selections
				await chrome.storage.sync.remove(['partsSelections']);
				renderPartsCheckboxesFromNames([], []);
			setSelectorStatus('Stored selectors cleared');
		} catch (e) {
			setSelectorStatus(String(e), false);
		}
	});

		// Save selected parts
		savePartsSelectionsBtn?.addEventListener('click', async () => {
			try {
				if (!partsCheckboxes) { setPartsStatus('No parts available', false); return; }
				const chks = Array.from(partsCheckboxes.querySelectorAll('input[type="checkbox"][data-part-key]'));
				const selected = chks.filter(c => c.checked).map(c => c.dataset.partKey);
				await chrome.storage.sync.set({ partsSelections: selected });
				setPartsStatus('Parts selections saved');
			} catch (e) {
				setPartsStatus(String(e), false);
			}
		});

		// Clear selected parts
		clearPartsSelectionsBtn?.addEventListener('click', async () => {
			try {
				await chrome.storage.sync.remove('partsSelections');
				if (partsCheckboxes) {
					Array.from(partsCheckboxes.querySelectorAll('input[type="checkbox"][data-part-key]')).forEach(c => { c.checked = false; });
				}
				setPartsStatus('Parts selections cleared');
			} catch (e) {
				setPartsStatus(String(e), false);
			}
		});

    // Removed standalone parts and serial buttons; both integrated into Run Automation
});
