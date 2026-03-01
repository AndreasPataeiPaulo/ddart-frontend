<template>
    <div class="study-container">

        <!-- Login modal -->
        <transition name="modal-fade">
            <div v-if="!authenticated" class="modal-backdrop">
                <div class="modal-box">
                    <div class="modal-logo">DDART<span>AI</span></div>
                    <h3>Study Official Access</h3>
                    <p>Enter the study access code to continue.</p>
                    <div class="field">
                        <input
                            v-model="codeInput"
                            type="password"
                            placeholder="Access code"
                            @keyup.enter="authenticate"
                            autofocus
                        />
                    </div>
                    <transition name="error-pop">
                        <p v-if="authError" class="error">{{ authError }}</p>
                    </transition>
                    <button class="submit-btn" @click="authenticate" :disabled="authLoading">
                        {{ authLoading ? 'Verifying...' : 'Enter' }}
                    </button>
                </div>
            </div>
        </transition>

        <!-- Main dashboard -->
        <div v-if="authenticated">
            <div class="header">
                <div class="user-bar">
                    <span>Study Official Dashboard</span>
                    <button class="logout-btn" @click="logout">Sign Out</button>
                </div>
                <p class="university">Democritus University of Thrace – DDART spin-off company</p>
                <p class="subtitle">Ophthalmology A.I. Screening Program — Study Overview</p>
                <div class="logo">DDART<span>AI</span></div>
            </div>

            <div class="panel-tabs">
                <button :class="['panel-tab', { active: tab === 'general' }]" @click="tab = 'general'">General</button>
                <button :class="['panel-tab', { active: tab === 'glaucoma' }]" @click="tab = 'glaucoma'">Glaucoma</button>
                <button :class="['panel-tab', { active: tab === 'dr' }]" @click="tab = 'dr'">Diabetic Retinopathy</button>
                <button :class="['panel-tab', { active: tab === 'amd' }]" @click="tab = 'amd'">AMD</button>
            </div>

            <div v-if="loading" class="loading-state">
                <div class="spinner"></div>
                <p>Loading study data...</p>
            </div>

            <transition name="fade-slide" mode="out-in">

                <!-- GENERAL TAB -->
                <div v-if="!loading && tab === 'general'" key="general" class="panel-section">

                    <!-- Top stat cards -->
                    <div class="stat-grid">
                        <div class="stat-card">
                            <p class="stat-value">{{ stats.general.total_images }}</p>
                            <p class="stat-label">Total Images</p>
                        </div>
                        <div class="stat-card">
                            <p class="stat-value">{{ stats.general.total_reviews }}</p>
                            <p class="stat-label">Total Reviews</p>
                        </div>
                        <div class="stat-card">
                            <p class="stat-value">{{ stats.general.hc_total_reviewed }}</p>
                            <p class="stat-label">HC Uploads Reviewed</p>
                        </div>
                        <div class="stat-card">
                            <p class="stat-value">{{ stats.doctors.length }}</p>
                            <p class="stat-label">Active Researchers</p>
                        </div>
                    </div>

                    <!-- Agreement section -->
                    <div class="section-card">
                        <h4 class="section-title">Inter-Rater Agreement <span class="section-sub">(researchers vs each other)</span></h4>
                        <div class="agreement-row-grid">
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.inter_rater_glaucoma)">
                                    <span class="agree-pct">{{ stats.general.inter_rater_glaucoma }}%</span>
                                </div>
                                <p class="agree-label">Glaucoma</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.inter_rater_dr)">
                                    <span class="agree-pct">{{ stats.general.inter_rater_dr }}%</span>
                                </div>
                                <p class="agree-label">DR</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.inter_rater_amd)">
                                    <span class="agree-pct">{{ stats.general.inter_rater_amd }}%</span>
                                </div>
                                <p class="agree-label">AMD</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring overall" :style="ringStyle(overallInterRater)">
                                    <span class="agree-pct">{{ overallInterRater }}%</span>
                                </div>
                                <p class="agree-label">Overall</p>
                            </div>
                        </div>
                    </div>

                    <div class="section-card">
                        <h4 class="section-title">AI Agreement <span class="section-sub">(researchers vs AI)</span></h4>
                        <div class="agreement-row-grid">
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.ai_agree_glaucoma)">
                                    <span class="agree-pct">{{ stats.general.ai_agree_glaucoma }}%</span>
                                </div>
                                <p class="agree-label">Glaucoma</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.ai_agree_dr)">
                                    <span class="agree-pct">{{ stats.general.ai_agree_dr }}%</span>
                                </div>
                                <p class="agree-label">DR</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.ai_agree_amd)">
                                    <span class="agree-pct">{{ stats.general.ai_agree_amd }}%</span>
                                </div>
                                <p class="agree-label">AMD</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring overall" :style="ringStyle(overallAIAgree)">
                                    <span class="agree-pct">{{ overallAIAgree }}%</span>
                                </div>
                                <p class="agree-label">Overall</p>
                            </div>
                        </div>
                    </div>

                    <!-- HC AI Agreement -->
                    <div class="section-card">
                        <h4 class="section-title">Health Center Upload AI Agreement <span class="section-sub">(high-confidence only ≥90%)</span></h4>
                        <div class="agreement-row-grid">
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.hc_ai_agree_glaucoma)">
                                    <span class="agree-pct">{{ stats.general.hc_ai_agree_glaucoma }}%</span>
                                </div>
                                <p class="agree-label">Glaucoma</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.hc_ai_agree_dr)">
                                    <span class="agree-pct">{{ stats.general.hc_ai_agree_dr }}%</span>
                                </div>
                                <p class="agree-label">DR</p>
                            </div>
                            <div class="agree-block">
                                <div class="agree-ring" :style="ringStyle(stats.general.hc_ai_agree_amd)">
                                    <span class="agree-pct">{{ stats.general.hc_ai_agree_amd }}%</span>
                                </div>
                                <p class="agree-label">AMD</p>
                            </div>
                        </div>
                    </div>

                    <!-- Condition prevalence -->
                    <div class="section-card">
                        <h4 class="section-title">Condition Prevalence <span class="section-sub">(AI findings in research images)</span></h4>
                        <div class="prevalence-grid">
                            <div class="prev-bar-row">
                                <span class="prev-label">Glaucoma</span>
                                <div class="prev-bar-wrap">
                                    <div class="prev-bar glaucoma-bar" :style="{ width: prevPct(stats.general.prevalence_glaucoma) + '%' }"></div>
                                </div>
                                <span class="prev-count">{{ stats.general.prevalence_glaucoma }} / {{ stats.general.total_images }}</span>
                            </div>
                            <div class="prev-bar-row">
                                <span class="prev-label">DR</span>
                                <div class="prev-bar-wrap">
                                    <div class="prev-bar dr-bar" :style="{ width: prevPct(stats.general.prevalence_dr) + '%' }"></div>
                                </div>
                                <span class="prev-count">{{ stats.general.prevalence_dr }} / {{ stats.general.total_images }}</span>
                            </div>
                            <div class="prev-bar-row">
                                <span class="prev-label">AMD</span>
                                <div class="prev-bar-wrap">
                                    <div class="prev-bar amd-bar" :style="{ width: prevPct(stats.general.prevalence_amd) + '%' }"></div>
                                </div>
                                <span class="prev-count">{{ stats.general.prevalence_amd }} / {{ stats.general.total_images }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Per-doctor breakdown -->
                    <div class="section-card">
                        <h4 class="section-title">Researcher Activity</h4>
                        <table class="data-table">
                            <thead>
                                <tr><th>Researcher</th><th>Images Reviewed</th><th>Share</th></tr>
                            </thead>
                            <tbody>
                                <tr v-for="doc in stats.doctors" :key="doc.id">
                                    <td>{{ doc.name }}</td>
                                    <td>{{ doc.reviewed }}</td>
                                    <td>
                                        <div class="mini-bar-wrap">
                                            <div class="mini-bar" :style="{ width: maxReviewed > 0 ? (doc.reviewed / maxReviewed * 100) + '%' : '0%' }"></div>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- CONDITION TABS -->
                <div v-else-if="!loading && (tab === 'glaucoma' || tab === 'dr' || tab === 'amd')" :key="tab" class="panel-section">
                    <div class="section-card">
                        <h4 class="section-title">
                            {{ conditionLabel }} — Per-Image Expert Breakdown
                            <span class="section-sub">({{ currentRows.length }} images reviewed)</span>
                        </h4>

                        <div v-if="currentRows.length === 0" class="empty-state">No data yet for this condition.</div>

                        <div v-else class="condition-table-wrap">
                            <table class="data-table condition-table">
                                <thead>
                                    <tr>
                                        <th>Image</th>
                                        <th>AI Result</th>
                                        <th v-for="doc in stats.doctors" :key="doc.id">{{ doc.name }}</th>
                                        <th>Inter-Rater</th>
                                        <th>AI Agree</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="row in currentRows" :key="row.image_id">
                                        <td class="img-cell">#{{ row.image_id }}</td>
                                        <td>
                                            <span class="ai-chip" :class="aiChipClass(row.ai_result)">{{ row.ai_result }}</span>
                                        </td>
                                        <td v-for="doc in stats.doctors" :key="doc.id">
                                            <span v-if="row.doctor_answers[doc.name]"
                                                :class="['answer-chip', row.doctor_answers[doc.name] === row.ai_result ? 'chip-match' : 'chip-differ']">
                                                {{ row.doctor_answers[doc.name] }}
                                            </span>
                                            <span v-else class="no-review">—</span>
                                        </td>
                                        <td>
                                            <span v-if="row.inter_rater_pct !== null" :class="['pct-badge', row.inter_rater_pct >= 80 ? 'pct-good' : row.inter_rater_pct >= 50 ? 'pct-mid' : 'pct-low']">
                                                {{ row.inter_rater_pct }}%
                                            </span>
                                            <span v-else class="no-review">1 reviewer</span>
                                        </td>
                                        <td>
                                            <span class="pct-badge" :class="row.ai_agree_count === row.total_reviews ? 'pct-good' : row.ai_agree_count > 0 ? 'pct-mid' : 'pct-low'">
                                                {{ row.ai_agree_count }}/{{ row.total_reviews }}
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <!-- HC rows for this condition -->
                        <div v-if="hcRowsForCondition.length > 0" class="hc-subsection">
                            <h5 class="hc-sub-title">Health Center Uploads — {{ conditionLabel }}</h5>
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>AMKA</th>
                                        <th>Health Center</th>
                                        <th>AI Result</th>
                                        <th>AI Conf.</th>
                                        <th>Reviewer</th>
                                        <th>Reviewer Answer</th>
                                        <th>Match</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="h in hcRowsForCondition" :key="h.id">
                                        <td class="amka-cell">{{ h.patient_amka }}</td>
                                        <td>{{ h.center_name }}</td>
                                        <td><span class="ai-chip" :class="aiChipClass(h['ai_' + tab])">{{ h['ai_' + tab] }}</span></td>
                                        <td><span :class="['conf-badge', h['ai_' + tab + '_conf'] >= 90 ? 'conf-high' : 'conf-low']">{{ h['ai_' + tab + '_conf'] }}%</span></td>
                                        <td>{{ h.reviewer }}</td>
                                        <td>{{ h['doctor_' + tab] }}</td>
                                        <td>
                                            <span :class="h['doctor_' + tab] === h['ai_' + tab] ? 'match-yes' : 'match-no'">
                                                {{ h['doctor_' + tab] === h['ai_' + tab] ? '✓ Match' : '✗ Differ' }}
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

            </transition>

            <div class="footer">
                <div class="footer-left"><img src="/democritus.png" class="dept-logo" /></div>
                <div class="footer-right">
                    <p>For technical support please call +3025510 30990 (office hours)</p>
                    <p>email: <a href="mailto:ddart@med.duth.gr">ddart@med.duth.gr</a></p>
                    <p class="made-by">Made by Andreas</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            authenticated: false,
            codeInput: '',
            authError: '',
            authLoading: false,
            tab: 'general',
            loading: false,
            stats: {
                doctors: [],
                general: {
                    total_images: 0, total_reviews: 0, hc_total_reviewed: 0,
                    inter_rater_glaucoma: 0, inter_rater_dr: 0, inter_rater_amd: 0,
                    ai_agree_glaucoma: 0, ai_agree_dr: 0, ai_agree_amd: 0,
                    prevalence_glaucoma: 0, prevalence_dr: 0, prevalence_amd: 0,
                    hc_ai_agree_glaucoma: 0, hc_ai_agree_dr: 0, hc_ai_agree_amd: 0
                },
                glaucoma_rows: [], dr_rows: [], amd_rows: [], hc_rows: []
            }
        }
    },

    computed: {
        overallInterRater() {
            const g = this.stats.general
            const vals = [g.inter_rater_glaucoma, g.inter_rater_dr, g.inter_rater_amd].filter(v => v > 0)
            return vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0
        },
        overallAIAgree() {
            const g = this.stats.general
            const vals = [g.ai_agree_glaucoma, g.ai_agree_dr, g.ai_agree_amd].filter(v => v > 0)
            return vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0
        },
        currentRows() {
            if (this.tab === 'glaucoma') return this.stats.glaucoma_rows
            if (this.tab === 'dr') return this.stats.dr_rows
            if (this.tab === 'amd') return this.stats.amd_rows
            return []
        },
        conditionLabel() {
            return { glaucoma: 'Glaucoma', dr: 'Diabetic Retinopathy', amd: 'AMD' }[this.tab] || ''
        },
        maxReviewed() {
            return Math.max(...this.stats.doctors.map(d => d.reviewed), 1)
        },
        hcRowsForCondition() {
            if (!this.stats.hc_rows) return []
            return this.stats.hc_rows.filter(h => {
                if (this.tab === 'glaucoma') return h.ai_glaucoma_conf >= 90
                if (this.tab === 'dr') return h.ai_dr_conf >= 90
                if (this.tab === 'amd') return h.ai_amd_conf >= 90
                return false
            })
        }
    },

    methods: {
        async authenticate() {
            if (!this.codeInput) return
            this.authLoading = true
            this.authError = ''
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/stats?code=${encodeURIComponent(this.codeInput)}`)
                if (!res.ok) { this.authError = 'Invalid access code.'; return }
                const data = await res.json()
                this.stats = data
                this.authenticated = true
                localStorage.setItem('ddart_study', 'true')
            } catch { this.authError = 'Connection failed.' }
            finally { this.authLoading = false }
        },

        async loadStats() {
            this.loading = true
            try {
                const code = this.codeInput || 'ddart'
                const res = await fetch(`https://labiris.myiplist.com/study/stats?code=${code}`)
                const data = await res.json()
                this.stats = data
            } catch { } finally { this.loading = false }
        },

        logout() {
            localStorage.removeItem('ddart_study')
            this.authenticated = false
            this.codeInput = ''
        },

        ringStyle(pct) {
            const color = pct >= 80 ? '#38a169' : pct >= 60 ? '#d69e2e' : '#e53e3e'
            const deg = Math.round(pct / 100 * 360)
            return { background: `conic-gradient(${color} ${deg}deg, #e2e8f0 ${deg}deg)` }
        },

        prevPct(count) {
            if (!this.stats.general.total_images) return 0
            return Math.round(count / this.stats.general.total_images * 100)
        },

        aiChipClass(val) {
            if (!val) return ''
            const positive = ['Glaucoma', 'AMD', 'Mild', 'Moderate', 'Severe', 'Proliferative DR', 'Proliferate_DR']
            return positive.includes(val) ? 'chip-positive' : 'chip-negative'
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; min-height: 100%; background: #f0f4f8; font-family: 'Source Sans 3', sans-serif; }

.study-container { display: flex; flex-direction: column; align-items: center; padding: 30px 20px 0; min-height: 100vh; }

/* Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(10,20,40,0.85); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.modal-box { background: white; border-radius: 12px; padding: 40px; width: 320px; display: flex; flex-direction: column; align-items: center; gap: 16px; animation: appear 0.35s cubic-bezier(0.34,1.56,0.64,1) both; }
@keyframes appear { from { opacity: 0; transform: scale(0.9) translateY(20px); } to { opacity: 1; transform: scale(1) translateY(0); } }
.modal-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 16px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; gap: 2px; }
.modal-logo span { color: #e53e3e; font-size: 36px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }
.modal-box h3 { font-family: 'Playfair Display', serif; color: #2d3748; font-size: 18px; margin: 0; }
.modal-box p { font-size: 13px; color: #718096; margin: 0; text-align: center; }
.field { width: 100%; }
.field input { width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; color: #2d3748; outline: none; transition: border-color 0.2s, box-shadow 0.2s; }
.field input:focus { border-color: #2b6cb0; box-shadow: 0 0 0 3px rgba(43,108,176,0.12); }
.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0; }
.submit-btn { width: 100%; padding: 10px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.submit-btn:hover:not(:disabled) { background: #2c5282; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* Header */
.header { text-align: center; margin-bottom: 24px; width: 100%; max-width: 1000px; }
.user-bar { display: flex; align-items: center; justify-content: flex-end; gap: 10px; margin-bottom: 10px; font-size: 13px; color: #4a5568; }
.logout-btn { padding: 4px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; font-family: 'Source Sans 3', sans-serif; background: none; border: 1px solid #e2e8f0; color: #718096; transition: background 0.2s; }
.logout-btn:hover { background: #f8fafc; }
.university { font-size: 14px; color: #2c5282; font-weight: 600; margin: 0 0 4px; }
.subtitle { font-size: 13px; color: #4a6fa5; margin: 0 0 16px; }
.logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 18px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; justify-content: center; gap: 2px; }
.logo span { color: #e53e3e; font-size: 48px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }

/* Tabs */
.panel-tabs { display: flex; gap: 8px; width: 100%; max-width: 1000px; margin-bottom: 20px; }
.panel-tab { flex: 1; padding: 10px; border: 1px solid #e2e8f0; border-radius: 4px; background: white; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; transition: all 0.2s; }
.panel-tab:hover { background: #f8fafc; }
.panel-tab.active { background: #2b6cb0; color: white; border-color: #2b6cb0; }

.panel-section { width: 100%; max-width: 1000px; margin-bottom: 24px; display: flex; flex-direction: column; gap: 16px; }

/* Stat cards */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.stat-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; text-align: center; }
.stat-value { font-size: 36px; font-weight: 700; color: #2b6cb0; margin: 0; font-family: 'Playfair Display', serif; line-height: 1; }
.stat-label { font-size: 11px; color: #a0aec0; margin: 6px 0 0; text-transform: uppercase; letter-spacing: 0.5px; }

/* Section cards */
.section-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; }
.section-title { font-family: 'Playfair Display', serif; font-size: 16px; color: #2c5282; margin: 0 0 20px; }
.section-sub { font-family: 'Source Sans 3', sans-serif; font-size: 12px; color: #a0aec0; font-weight: 400; }

/* Agreement rings */
.agreement-row-grid { display: flex; gap: 32px; align-items: center; justify-content: center; flex-wrap: wrap; }
.agree-block { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.agree-ring { width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; }
.agree-ring::before { content: ''; position: absolute; inset: 8px; background: white; border-radius: 50%; }
.agree-ring.overall { width: 96px; height: 96px; }
.agree-pct { position: relative; z-index: 1; font-size: 16px; font-weight: 700; color: #2d3748; }
.agree-ring.overall .agree-pct { font-size: 20px; }
.agree-label { font-size: 12px; color: #718096; font-weight: 600; }

/* Prevalence bars */
.prevalence-grid { display: flex; flex-direction: column; gap: 12px; }
.prev-bar-row { display: grid; grid-template-columns: 80px 1fr 80px; align-items: center; gap: 12px; }
.prev-label { font-size: 13px; font-weight: 600; color: #4a5568; }
.prev-bar-wrap { height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; }
.prev-bar { height: 100%; border-radius: 5px; transition: width 0.6s ease; }
.glaucoma-bar { background: #38a169; }
.dr-bar { background: #e53e3e; }
.amd-bar { background: #2b6cb0; }
.prev-count { font-size: 12px; color: #718096; text-align: right; }

/* Data table */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { background: #f8fafc; color: #a0aec0; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; padding: 8px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; white-space: nowrap; }
.data-table td { padding: 10px 12px; border-bottom: 1px solid #f0f4f8; color: #2d3748; vertical-align: middle; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #f8fafc; }
.mini-bar-wrap { height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; width: 120px; }
.mini-bar { height: 100%; background: #2b6cb0; border-radius: 4px; }

/* Condition table */
.condition-table-wrap { overflow-x: auto; }
.condition-table { min-width: 600px; }
.img-cell { font-weight: 700; color: #4a5568; }
.ai-chip { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.chip-positive { background: #fff5f5; color: #c53030; }
.chip-negative { background: #f0fff4; color: #276749; }
.answer-chip { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; white-space: nowrap; }
.chip-match { background: #f0fff4; color: #276749; }
.chip-differ { background: #fff5f5; color: #c53030; }
.no-review { color: #cbd5e0; font-size: 12px; }
.pct-badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.pct-good { background: #f0fff4; color: #276749; }
.pct-mid { background: #fffaf0; color: #c05621; }
.pct-low { background: #fff5f5; color: #c53030; }
.conf-badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.conf-high { background: #fffaf0; color: #c05621; }
.conf-low { background: #f0fff4; color: #276749; }
.amka-cell { font-family: monospace; letter-spacing: 1px; color: #2b6cb0; font-weight: 700; }
.match-yes { color: #38a169; font-weight: 700; }
.match-no { color: #e53e3e; font-weight: 700; }

/* HC subsection */
.hc-subsection { margin-top: 24px; padding-top: 20px; border-top: 1px solid #e2e8f0; }
.hc-sub-title { font-size: 14px; font-weight: 700; color: #553c9a; margin: 0 0 12px; }

/* Loading */
.loading-state { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 60px; color: #718096; }
.spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #2b6cb0; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state { padding: 32px; text-align: center; color: #a0aec0; font-size: 13px; }

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.fade-slide-enter-active { transition: all 0.3s ease; }
.fade-slide-leave-active { transition: all 0.2s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-6px); }
.error-pop-enter-active { transition: opacity 0.25s ease, transform 0.25s cubic-bezier(0.34,1.56,0.64,1); }
.error-pop-leave-active { transition: opacity 0.15s ease; }
.error-pop-enter-from { opacity: 0; transform: translateY(-4px) scale(0.97); }
.error-pop-leave-to { opacity: 0; }

/* Footer */
.footer { width: 100%; max-width: 1000px; display: flex; justify-content: space-between; align-items: center; padding: 16px 0 24px; border-top: 1px solid #e2e8f0; margin-top: auto; }
.dept-logo { height: 55px; width: auto; object-fit: contain; }
.footer-right { text-align: right; }
.footer-right p { font-size: 12px; color: #718096; margin: 2px 0; }
.footer-right a { color: #2b6cb0; text-decoration: none; }
.made-by { font-size: 10px; color: #cbd5e0; margin-top: 4px; }

@media (max-width: 768px) {
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
    .agreement-row-grid { gap: 20px; }
    .panel-tabs { flex-wrap: wrap; }
}
</style>