<template>
    <div class="doctor-container">
        <!-- Header -->
        <div class="header">
            <div class="user-bar">
                <span>🩺 Dr. {{ doctorName }}</span>
                <button class="logout-btn" @click="logout">Sign Out</button>
            </div>
            <p class="university">Democritus University of Thrace – DDART spin-off company</p>
            <p class="subtitle">Ophthalmology A.I. Screening Program</p>
            <img src="/DDART.png" style="height:30px;width:auto;object-fit:contain;" />
        </div>

        <!-- Tabs -->
        <div class="panel-tabs">
            <button :class="['panel-tab', { active: tab === 'stats' }]" @click="tab = 'stats'"> Statistics</button>
            <button :class="['panel-tab', { active: tab === 'patients' }]" @click="tab = 'patients'; loadPatients()">
                Patients</button>
            <button :class="['panel-tab', { active: tab === 'export' }]" @click="tab = 'export'"> Export</button>
        </div>

        <!-- STATS TAB -->
        <transition name="fade-slide" mode="out-in">
            <div v-if="tab === 'stats'" key="stats" class="panel-section">
                <div v-if="statsLoading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading statistics...</p>
                </div>
                <div v-else-if="stats" class="stats-grid">
                    <div class="stat-card">
                        <p class="stat-value">{{ stats.total_patients }}</p>
                        <p class="stat-label">Registered Patients</p>
                    </div>
                    <div class="stat-card">
                        <p class="stat-value">{{ stats.total_screenings }}</p>
                        <p class="stat-label">Total Screenings</p>
                    </div>
                    <div class="stat-card" v-for="(count, type) in stats.by_type" :key="type">
                        <p class="stat-value">{{ count }}</p>
                        <p class="stat-label">{{ type }} Screenings</p>
                    </div>
                </div>

                <div v-if="stats && stats.by_result.length" class="results-breakdown">
                    <h3>Results Breakdown</h3>
                    <div v-for="r in stats.by_result" :key="r.result" class="breakdown-row">
                        <span class="breakdown-label" :class="resultClass(r.result)">{{ r.result }}</span>
                        <div class="breakdown-bar-container">
                            <div class="breakdown-bar"
                                :style="{ width: (r.count / stats.total_screenings * 100) + '%' }"
                                :class="resultClass(r.result)"></div>
                        </div>
                        <span class="breakdown-count">{{ r.count }}</span>
                    </div>
                </div>
            </div>

            <!-- PATIENTS TAB -->
            <div v-else-if="tab === 'patients'" key="patients" class="panel-section">
                <div v-if="patientsLoading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading patients...</p>
                </div>
                <div v-else-if="selectedPatient" class="patient-detail">
                    <button class="back-btn" @click="selectedPatient = null">← Back to patients</button>
                    <h3>{{ selectedPatient.patient.full_name }}</h3>
                    <p class="patient-since">Registered: {{ formatDate(selectedPatient.patient.created_at) }}</p>

                    <div v-if="selectedPatient.history.length === 0" class="empty-state">No screenings yet.</div>
                    <div v-else class="screening-list">
                        <div v-for="(h, idx) in selectedPatient.history" :key="idx" class="screening-item">
                            <img v-if="h.image" :src="h.image" class="screening-thumb" />
                            <div v-else class="screening-thumb-placeholder">No img</div>
                            <div class="screening-info">
                                <span class="screening-type">{{ h.type }}</span>
                                <span class="screening-result" :class="resultClass(h.result)">{{ h.result }}</span>
                                <span class="screening-confidence">{{ h.confidence }}%</span>
                                <span class="screening-date">{{ formatDate(h.date) }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <div v-if="patients.length === 0" class="empty-state">No patients registered yet.</div>
                    <div v-else class="patient-list">
                        <div v-for="p in patients" :key="p.id" class="patient-row" @click="loadPatientDetail(p.id)">
                            <div class="patient-avatar">{{ p.full_name.charAt(0).toUpperCase() }}</div>
                            <div class="patient-info">
                                <span class="patient-name">{{ p.full_name }}</span>
                                <span class="patient-date">Registered: {{ formatDate(p.created_at) }}</span>
                            </div>
                            <span class="patient-arrow">→</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- EXPORT TAB -->
            <div v-else-if="tab === 'export'" key="export" class="panel-section">
                <div class="export-card">
                    <h3>Export Patient Data</h3>
                    <p>Download a CSV file containing all patient screening results, suitable for research or clinical
                        records.</p>
                    <p class="export-note">⚠️ This file contains sensitive patient data. 
                    </p>
                    <a href="https://labiris.myiplist.com/doctor/export" class="export-btn" download>
                         Download CSV
                    </a>
                </div>
            </div>
        </transition>

        <!-- Footer -->
        <div class="footer">
            <div class="footer-left">
                <img src="/DDARTECH_Research-removebg-preview.png" class="dept-logo" />
            </div>
            <div class="footer-right">
                <p>For technical support please call +3025510 30990 (office hours)</p>
                <p>email: <a href="mailto:ddart@med.duth.gr">ddart@med.duth.gr</a></p>
                <p class="made-by">Made by Andreas</p>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            doctorName: '',
            doctorId: null,
            tab: 'stats',
            stats: null,
            statsLoading: false,
            patients: [],
            patientsLoading: false,
            selectedPatient: null
        }
    },

    mounted() {
        const stored = localStorage.getItem('ddart_doctor')
        if (!stored) { this.$router.push('/login'); return }
        const doctor = JSON.parse(stored)
        this.doctorName = doctor.name
        this.doctorId = doctor.id
        this.loadStats()
    },

    methods: {
        async loadStats() {
            this.statsLoading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/stats')
                this.stats = await res.json()
            } catch { } finally { this.statsLoading = false }
        },

        async loadPatients() {
            this.patientsLoading = true
            this.selectedPatient = null
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/patients')
                const data = await res.json()
                this.patients = data.patients || []
            } catch { } finally { this.patientsLoading = false }
        },

        async loadPatientDetail(patientId) {
            try {
                const res = await fetch(`https://labiris.myiplist.com/doctor/patient/${patientId}`)
                this.selectedPatient = await res.json()
            } catch { }
        },

        logout() {
            localStorage.removeItem('ddart_doctor')
            this.$router.push('/login')
        },

        formatDate(dateStr) {
            return new Date(dateStr).toLocaleDateString('el-GR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
        },

        resultClass(result) {
            if (!result) return ''
            const r = result.toLowerCase()
            if (r.includes('healthy') || r.includes('normal') || r.includes('no_dr')) return 'result-good'
            if (r.includes('inconclusive')) return 'result-inconclusive'
            return 'result-bad'
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

*,
*::before,
*::after {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    min-height: 100%;
    background: #f0f4f8;
    font-family: 'Source Sans 3', sans-serif;
}

.doctor-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 20px 0;
    min-height: 100vh;
}

.header {
    text-align: center;
    margin-bottom: 24px;
    width: 100%;
    max-width: 760px;
}

.user-bar {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 13px;
    color: #4a5568;
}

.logout-btn {
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    font-family: 'Source Sans 3', sans-serif;
    background: none;
    border: 1px solid #e2e8f0;
    color: #718096;
    transition: background 0.2s;
}

.logout-btn:hover {
    background: #f8fafc;
}

.university {
    font-size: 14px;
    color: #2c5282;
    font-weight: 600;
    margin: 0 0 4px;
}

.subtitle {
    font-size: 13px;
    color: #4a6fa5;
    margin: 0 0 16px;
}

.logo {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #2c5282;
    letter-spacing: 3px;
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 2px;
}

.logo span {
    color: #e53e3e;
    font-size: 48px;
    font-weight: 900;
    font-family: 'Arial Black', Arial, sans-serif;
}

.panel-tabs {
    display: flex;
    gap: 8px;
    width: 100%;
    max-width: 760px;
    margin-bottom: 20px;
}

.panel-tab {
    flex: 1;
    padding: 10px;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    background: white;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #718096;
    cursor: pointer;
    transition: all 0.2s;
}

.panel-tab:hover {
    background: #f8fafc;
}

.panel-tab.active {
    background: #2b6cb0;
    color: white;
    border-color: #2b6cb0;
}

.panel-section {
    width: 100%;
    max-width: 760px;
    margin-bottom: 24px;
}

.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 40px;
    color: #718096;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
}

.spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e2e8f0;
    border-top-color: #2b6cb0;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

.stat-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.stat-value {
    font-size: 36px;
    font-weight: 700;
    color: #2b6cb0;
    margin: 0 0 4px;
    font-family: 'Playfair Display', serif;
}

.stat-label {
    font-size: 12px;
    color: #718096;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.results-breakdown {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 20px;
}

.results-breakdown h3 {
    font-size: 13px;
    color: #718096;
    margin: 0 0 16px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.breakdown-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
    font-size: 13px;
}

.breakdown-label {
    width: 130px;
    font-weight: 600;
    flex-shrink: 0;
}

.breakdown-bar-container {
    flex: 1;
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
}

.breakdown-bar {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
    background: #2b6cb0;
}

.breakdown-bar.result-good {
    background: #38a169;
}

.breakdown-bar.result-bad {
    background: #e53e3e;
}

.breakdown-bar.result-inconclusive {
    background: #d69e2e;
}

.breakdown-count {
    width: 30px;
    text-align: right;
    color: #718096;
    flex-shrink: 0;
}

/* Patients */
.patient-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.patient-row {
    display: flex;
    align-items: center;
    gap: 14px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s;
}

.patient-row:hover {
    background: #f8fafc;
    transform: translateX(2px);
}

.patient-avatar {
    width: 40px;
    height: 40px;
    background: #2b6cb0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 16px;
    flex-shrink: 0;
}

.patient-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
}

.patient-name {
    font-weight: 600;
    color: #2d3748;
    font-size: 14px;
}

.patient-date {
    font-size: 11px;
    color: #a0aec0;
}

.patient-arrow {
    color: #a0aec0;
    font-size: 16px;
}

.patient-detail {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 20px;
}

.back-btn {
    background: none;
    border: none;
    color: #2b6cb0;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    padding: 0 0 16px;
    font-family: 'Source Sans 3', sans-serif;
}

.back-btn:hover {
    text-decoration: underline;
}

.patient-detail h3 {
    margin: 0 0 4px;
    font-family: 'Playfair Display', serif;
    color: #2c5282;
    font-size: 20px;
}

.patient-since {
    font-size: 12px;
    color: #a0aec0;
    margin: 0 0 16px;
}

.screening-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.screening-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 10px 12px;
}

.screening-thumb {
    width: 56px;
    height: 56px;
    object-fit: cover;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
}

.screening-thumb-placeholder {
    width: 56px;
    height: 56px;
    background: #edf2f7;
    border-radius: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #a0aec0;
}

.screening-info {
    display: flex;
    gap: 16px;
    align-items: center;
    flex: 1;
    font-size: 13px;
    flex-wrap: wrap;
}

.screening-type {
    font-weight: 700;
    color: #2d3748;
    width: 75px;
}

.screening-result {
    flex: 1;
    font-weight: 600;
}

.screening-confidence {
    color: #2b6cb0;
    font-weight: 600;
}

.screening-date {
    color: #a0aec0;
    font-size: 11px;
}

.result-good {
    color: #276749;
}

.result-bad {
    color: #c53030;
}

.result-inconclusive {
    color: #b7791f;
}

.empty-state {
    padding: 40px;
    text-align: center;
    color: #718096;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
}

/* Export */
.export-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 32px;
    text-align: center;
}

.export-card h3 {
    font-family: 'Playfair Display', serif;
    color: #2c5282;
    font-size: 20px;
    margin: 0 0 12px;
}

.export-card p {
    font-size: 14px;
    color: #4a5568;
    line-height: 1.7;
    margin: 0 0 12px;
}

.export-note {
    font-size: 12px;
    color: #b7791f;
    background: #fffff0;
    border: 1px solid #f6e05e;
    border-radius: 4px;
    padding: 8px 12px;
}

.export-btn {
    display: inline-block;
    margin-top: 20px;
    padding: 12px 28px;
    background: #2b6cb0;
    color: white;
    border-radius: 4px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: background 0.2s;
}

.export-btn:hover {
    background: #2c5282;
}

/* Transitions */
.fade-slide-enter-active {
    transition: all 0.3s ease;
}

.fade-slide-leave-active {
    transition: all 0.2s ease;
}

.fade-slide-enter-from {
    opacity: 0;
    transform: translateY(10px);
}

.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-6px);
}

.footer {
    width: 100%;
    max-width: 760px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0 24px;
    border-top: 1px solid #e2e8f0;
    margin-top: auto;
}

.dept-logo {
    height: 55px;
    width: auto;
    object-fit: contain;
}

.footer-right {
    text-align: right;
}

.footer-right p {
    font-size: 12px;
    color: #718096;
    margin: 2px 0;
}

.footer-right a {
    color: #2b6cb0;
    text-decoration: none;
}

.made-by {
    font-size: 10px;
    color: #cbd5e0;
    margin-top: 4px;
}
</style>