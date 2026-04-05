let allDepartments = [];
let filteredData = [];

// Filter states
let active8Group = null;
let active18Group = null;
let searchQuery = '';

const domElements = {
    stats: document.getElementById('result-stats'),
    searchInput: document.getElementById('search-input'),
    filter8Groups: document.getElementById('filter-8-groups'),
    filter18Groups: document.getElementById('filter-18-groups'),
    popularSchoolsList: document.getElementById('popular-schools-list'),
    resultsContainer: document.getElementById('results-container')
};

const POPULAR_SCHOOLS = [
    "臺灣大學", "成功大學", "交通大學",
    "師範大學", "政治大學", "清華大學"
];

const SUBJECT_MAP = {
    '國': '國文', '英': '英文', '數A': '數A', '數B': '數B', '數學A': '數A', '數學B': '數B', '自': '自然', '社': '社會', '聽': '聽力', '英聽': '英聽'
};

const LEVEL_MAP = {
    '頂標': '頂', '前標': '前', '均標': '均', '後標': '後', '底標': '底'
};

// Initialize App
async function initApp() {
    try {
        const response = await fetch('./all_departments.json');
        if (!response.ok) throw new Error('Failed to load data');

        allDepartments = await response.json();
        filteredData = [...allDepartments];

        buildFilters();
        buildPopularSchools();
        attachEventListeners();
        renderResults();

    } catch (e) {
        console.error(e);
        domElements.resultsContainer.innerHTML = '<div class="no-results">載入失敗。</div>';
    }
}

// --- SIDEBAR UI LOGIC ---

function toggleCollapse(id) {
    const content = document.getElementById(id);
    const header = content.previousElementSibling;
    const isExpanded = content.classList.toggle('expanded');
    header.classList.toggle('active', isExpanded);
}

function buildPopularSchools() {
    let html = '';
    POPULAR_SCHOOLS.forEach(school => {
        html += `<div class="pill school-pill" data-school="${school}">${school}</div>`;
    });
    domElements.popularSchoolsList.innerHTML = html;

    const pills = domElements.popularSchoolsList.querySelectorAll('.school-pill');
    pills.forEach(p => p.addEventListener('click', (e) => {
        const isAlreadySelected = e.target.classList.contains('active');
        pills.forEach(btn => btn.classList.remove('active'));

        if (isAlreadySelected) {
            searchQuery = '';
            domElements.searchInput.value = '';
        } else {
            e.target.classList.add('active');
            searchQuery = e.target.dataset.school.toLowerCase();
            domElements.searchInput.value = e.target.dataset.school;
            clearCategoryFilters();
        }
        applyFilters();
    }));
}

function clearCategoryFilters() {
    active8Group = null;
    active18Group = null;
    generateGroupFilters();
}

function buildFilters() {
    generateGroupFilters();
}

function generateGroupFilters() {
    // 8 Groups
    const eightContainer = domElements.filter8Groups;
    eightContainer.innerHTML = '';

    const categories8 = [
        "第一類學群", "第二類學群", "第三類學群", "第四類學群",
        "第五類學群", "第六類學群", "第七類學群", "第八類學群"
    ];

    categories8.forEach(cat => {
        const btn = document.createElement('div');
        btn.className = 'pill';
        if (active8Group === cat) btn.classList.add('active');
        btn.textContent = cat.replace('學群', ''); // Simplify text
        btn.onclick = () => {
            if (active8Group === cat) {
                active8Group = null;
            } else {
                active8Group = cat;
                active18Group = null;
                document.querySelectorAll('#filter-18-groups .pill').forEach(p => p.classList.remove('active'));
            }
            btn.classList.toggle('active');
            applyFilters();
            generateGroupFilters();
        };
        eightContainer.appendChild(btn);
    });

    // 18 Groups
    const eighteenContainer = domElements.filter18Groups;
    eighteenContainer.innerHTML = '';

    const all18Set = new Set();
    allDepartments.forEach(d => {
        if (d.eighteen_groups) d.eighteen_groups.forEach(g => { if (g) all18Set.add(g); });
    });

    Array.from(all18Set).sort().forEach(group => {
        const btn = document.createElement('div');
        btn.className = 'pill';
        if (active18Group === group) btn.classList.add('active');
        btn.textContent = group.replace('學群', ''); // Simplify text
        btn.onclick = () => {
            if (active18Group === group) {
                active18Group = null;
            } else {
                active18Group = group;
                active8Group = null;
                document.querySelectorAll('#filter-8-groups .pill').forEach(p => p.classList.remove('active'));
            }
            btn.classList.toggle('active');
            applyFilters();
            generateGroupFilters();
        };
        eighteenContainer.appendChild(btn);
    });
}

function attachEventListeners() {
    domElements.searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.trim().toLowerCase();
        document.querySelectorAll('.school-pill').forEach(p => p.classList.remove('active'));
        applyFilters();
    });
}

function applyFilters() {
    filteredData = allDepartments.filter(dept => {
        if (searchQuery) {
            const s = (dept.school_name || '').toLowerCase();
            const d = (dept.dept_name || '').toLowerCase();
            if (!s.includes(searchQuery) && !d.includes(searchQuery)) return false;
        }
        if (active8Group && dept.department_group !== active8Group) return false;
        if (active18Group && (!dept.eighteen_groups || !dept.eighteen_groups.includes(active18Group))) return false;
        return true;
    });
    renderResults();
}

function renderResults() {
    domElements.stats.innerText = `找到 ${filteredData.length} 個校系`;

    if (filteredData.length === 0) {
        domElements.resultsContainer.innerHTML = '<div class="no-results">查無資料。</div>';
        return;
    }

    const LIMIT = 150;
    const items = filteredData.slice(0, LIMIT);

    let html = '';
    items.forEach((dept, index) => {
        let rankHTML = '';
        if (dept.distribution_criteria) {
            const schoolRank = dept.distribution_criteria.find(c => c.item === '在校學業');
            if (schoolRank) {
                const val1 = (schoolRank.first_round && schoolRank.first_round.trim()) ? schoolRank.first_round : '<span class="missing-val">缺</span>';
                const val2 = (schoolRank.second_round && schoolRank.second_round.trim()) ? schoolRank.second_round : '<span class="missing-val">缺</span>';
                rankHTML += `<div class="rank-item"><span class="rank-icon">①</span>&nbsp;${val1}</div>`;
                rankHTML += `<div class="rank-item"><span class="rank-icon">②</span>&nbsp;${val2}</div>`;
            } else {
                rankHTML += `<div class="rank-item"><span class="rank-icon">①</span>&nbsp;<span class="missing-val">缺</span></div>`;
                rankHTML += `<div class="rank-item"><span class="rank-icon">②</span>&nbsp;<span class="missing-val">缺</span></div>`;
            }
        }

        let examsHTML = '';
        if (dept.admission_standards) {
            dept.admission_standards.forEach(a => {
                const sub = SUBJECT_MAP[a.subject] || a.subject;
                let lvl = LEVEL_MAP[a.level] || a.level;
                let score = a.score || '';
                if (sub === '聽力' || sub === '英聽') {
                    lvl = lvl.replace('級', '');
                    score = score.replace('級', '');
                } else {
                    score = score ? (score.includes('級分') ? score : score + ' 級分') : '';
                }
                examsHTML += `
                    <div class="exam-mini">
                        <span class="exam-sub">${sub}</span>
                        <span class="exam-lvl">${lvl}</span>
                        <span class="exam-score">${score}</span>
                    </div>
                `;
            });
        }

        let extraText = '';
        let cleanDeptName = (dept.dept_name || '').replace(/[（\(\[【]\s?(含?外加)\s?[）\)\]】]/g, (m, p1) => {
            extraText = p1;
            return '';
        }).replace(/\s+/g, '').trim();

        let deptStyle = 'font-size: 1.25rem;';
        if (cleanDeptName.length > 20) deptStyle = 'font-size: 0.9rem;';
        else if (cleanDeptName.length > 14) deptStyle = 'font-size: 1.05rem;';

        html += `
        <article class="mini-card" style="animation-delay: ${(index % 12) * 0.04}s">
            <header class="mini-card-header">
                <div class="school-name" style="line-height: 1.4;">${dept.school_name || ''}</div>
                <div class="dept-name" style="${deptStyle} line-height: 1.4;">${cleanDeptName} ${extraText ? `<span class="extra-red">${extraText}</span>` : ''}</div>
            </header>
            <div class="mini-card-content">
                <div class="rank-row">
                    <div class="row-label">在<br>校</div>
                    <div class="rank-group">${rankHTML || '無'}</div>
                </div>
                <div class="exam-row">
                    <div class="row-label">學<br>測</div>
                    <div class="exam-group">${examsHTML || '無'}</div>
                </div>
            </div>
        </article>
        `;
    });

    if (filteredData.length > LIMIT) {
        html += `<div class="no-results" style="grid-column: 1/-1;">...</div>`;
    }
    domElements.resultsContainer.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', initApp);
window.toggleCollapse = toggleCollapse; // Exposed to HTML
