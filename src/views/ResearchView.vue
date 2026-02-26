<template>
    <div class="research-container">
        <div class="header">
            <div class="user-bar">
                <span>🔬 Dr. {{ doctorName }} — Research Mode</span>
                <button class="logout-btn" @click="logout">Sign Out</button>
            </div>
            <p class="university">Democritus University of Thrace – DDART spin-off company</p>
            <p class="subtitle">Ophthalmology A.I. Screening Program — Research Study</p>
            <div class="logo">DDART<span>AI</span></div>
        </div>

        <div class="panel-tabs">
            <button :class="['panel-tab', { active: tab === 'pending' }]" @click="tab = 'pending'">
                 Pending Examinations <span v-if="pendingImages.length" class="badge">{{ pendingImages.length
                    }}</span>
            </button>
            <button :class="['panel-tab', { active: tab === 'concluded' }]" @click="tab = 'concluded'; loadConcluded()">
                 Concluded Examinations
            </button>
        </div>

        <transition name="fade-slide" mode="out-in">

            <!-- PENDING TAB -->
            <div v-if="tab === 'pending'" key="pending" class="panel-section">
                <div v-if="pendingLoading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading images...</p>
                </div>
                <div v-else-if="pendingImages.length === 0" class="empty-state">
                    <p>🎉 No pending examinations. All images have been reviewed.</p>
                </div>
                <div v-else>
                    <p class="section-hint">Examine each fundus image and select your diagnosis before submitting.</p>

                    <div class="image-card">
                        <div class="image-card-header">
                            <span class="image-counter">Image {{ currentIndex + 1 }} of {{ pendingImages.length
                                }}</span>
                            <div class="image-nav">
                                <button class="nav-btn" @click="currentIndex--"
                                    :disabled="currentIndex === 0">←</button>
                                <button class="nav-btn" @click="currentIndex++"
                                    :disabled="currentIndex === pendingImages.length - 1">→</button>
                            </div>
                        </div>

                        <div class="image-card-body">
                            <div class="image-side">
                                <img :src="'https://labiris.myiplist.com/research/image/' + currentImage.id"
                                    class="fundus-image" />
                                <p class="image-id">Image #{{ currentImage.id }}</p>
                            </div>

                            <div class="diagnosis-side">
                                <h3>Your Diagnosis</h3>
                                <div class="category-badge" :class="'cat-' + currentImage.category">
                                    {{ categoryLabel(currentImage.category) }}
                                </div>
                                <p class="diagnosis-hint">Select your diagnosis for this image:</p>

                                <!-- AMD only -->
                                <div v-if="currentImage.category === 'amd'" class="diagnosis-group">
                                    <label class="diagnosis-label">AMD</label>
                                    <div class="radio-group">
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.amd === 'AMD' }">
                                            <input type="radio" v-model="currentDiagnosis.amd" value="AMD" /> AMD
                                            Detected
                                        </label>
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.amd === 'Normal' }">
                                            <input type="radio" v-model="currentDiagnosis.amd" value="Normal" /> Normal
                                        </label>
                                    </div>
                                </div>

                                <!-- Glaucoma only -->
                                <div v-else-if="currentImage.category === 'glaucoma'" class="diagnosis-group">
                                    <label class="diagnosis-label">Glaucoma</label>
                                    <div class="radio-group">
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.glaucoma === 'Glaucoma' }">
                                            <input type="radio" v-model="currentDiagnosis.glaucoma" value="Glaucoma" />
                                            Glaucoma
                                        </label>
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.glaucoma === 'Healthy' }">
                                            <input type="radio" v-model="currentDiagnosis.glaucoma" value="Healthy" />
                                            Healthy
                                        </label>
                                    </div>
                                </div>

                                <!-- DR only -->
                                <div v-else-if="currentImage.category === 'dr'" class="diagnosis-group">
                                    <label class="diagnosis-label">Diabetic Retinopathy</label>
                                    <div class="radio-group">
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.dr === 'No_DR' }">
                                            <input type="radio" v-model="currentDiagnosis.dr" value="No_DR" /> No DR
                                        </label>
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.dr === 'Mild' }">
                                            <input type="radio" v-model="currentDiagnosis.dr" value="Mild" /> Mild
                                        </label>
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.dr === 'Moderate' }">
                                            <input type="radio" v-model="currentDiagnosis.dr" value="Moderate" />
                                            Moderate
                                        </label>
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.dr === 'Severe' }">
                                            <input type="radio" v-model="currentDiagnosis.dr" value="Severe" /> Severe
                                        </label>
                                        <label class="radio-option"
                                            :class="{ selected: currentDiagnosis.dr === 'Proliferate_DR' }">
                                            <input type="radio" v-model="currentDiagnosis.dr" value="Proliferate_DR" />
                                            Proliferative
                                        </label>
                                    </div>
                                </div>

                                <p v-if="submitError" class="error">{{ submitError }}</p>
                                <button class="submit-btn" @click="submitDiagnosis"
                                    :disabled="submitting || !diagnosisComplete">
                                    {{ submitting ? 'Submitting...' : '✓ Submit Diagnosis' }}
                                </button>
                                <p v-if="!diagnosisComplete" class="hint">Please select a diagnosis to submit.</p>
                            </div>
                        </div>
                    </div>

                    <div class="progress-bar-container">
                        <div class="progress-bar"
                            :style="{ width: ((currentIndex + 1) / pendingImages.length * 100) + '%' }"></div>
                    </div>
                </div>
            </div>

            <!-- CONCLUDED TAB -->
            <div v-else-if="tab === 'concluded'" key="concluded" class="panel-section">
                <div v-if="concludedLoading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading results...</p>
                </div>
                <div v-else-if="concludedImages.length === 0" class="empty-state">
                    <p>No concluded examinations yet.</p>
                </div>
                <div v-else>
                    <!-- Agreement banner -->
                    <div class="agreement-banner">
                        <div class="agreement-score">
                            <p class="agreement-value">{{ overallAgreement }}%</p>
                            <p class="agreement-label">Overall Agreement with AI</p>
                        </div>
                        <div class="agreement-breakdown">
                            <div v-if="amdCount > 0" class="agreement-stat">
                                <span class="stat-label">AMD</span>
                                <span class="stat-value">{{ amdAgreement }}%</span>
                                <span class="stat-count">{{ amdCount }} images</span>
                            </div>
                            <div v-if="glaucomaCount > 0" class="agreement-stat">
                                <span class="stat-label">Glaucoma</span>
                                <span class="stat-value">{{ glaucomaAgreement }}%</span>
                                <span class="stat-count">{{ glaucomaCount }} images</span>
                            </div>
                            <div v-if="drCount > 0" class="agreement-stat">
                                <span class="stat-label">DR</span>
                                <span class="stat-value">{{ drAgreement }}%</span>
                                <span class="stat-count">{{ drCount }} images</span>
                            </div>
                        </div>
                    </div>

                    <!-- Individual results -->
                    <div class="concluded-list">
                        <div v-for="item in concludedImages" :key="item.id" class="concluded-item">
                            <img :src="'https://labiris.myiplist.com/research/image/' + item.image_id"
                                class="concluded-thumb" />
                            <div class="concluded-info">
                                <div class="concluded-header">
                                    <p class="concluded-title">Image #{{ item.image_id }}</p>
                                    <div class="category-badge" :class="'cat-' + item.category">{{
                                        categoryLabel(item.category) }}</div>
                                </div>
                                <div class="comparison-grid">
                                    <div class="comparison-header">
                                        <span>Your Diagnosis</span><span>AI Diagnosis</span><span>Match</span>
                                    </div>
                                    <div class="comparison-row">
                                        <span>{{ doctorAnswer(item) }}</span>
                                        <span>{{ aiAnswer(item) }}</span>
                                        <span :class="doctorAnswer(item) === aiAnswer(item) ? 'match-yes' : 'match-no'">
                                            {{ doctorAnswer(item) === aiAnswer(item) ? '✓ Match' : '✗ Differ' }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
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
</template>

<script>
export default {
    
    data() {
        return {
            doctorName: '',
            doctorId: null,
            tab: 'pending',
            pendingImages: [],
            pendingLoading: false,
            currentIndex: 0,
            currentDiagnosis: { glaucoma: null, dr: null, amd: null },
            submitting: false,
            submitError: '',
            concludedImages: [],
            concludedLoading: false
        }
    },

    computed: {
        currentImage() {
            return this.pendingImages[this.currentIndex] || {}
        },
        diagnosisComplete() {
            const cat = this.currentImage.category
            if (cat === 'amd') return !!this.currentDiagnosis.amd
            if (cat === 'glaucoma') return !!this.currentDiagnosis.glaucoma
            if (cat === 'dr') return !!this.currentDiagnosis.dr
            return false
        },
        overallAgreement() {
            if (!this.concludedImages.length) return 0
            const matches = this.concludedImages.filter(i => this.doctorAnswer(i) === this.aiAnswer(i)).length
            return Math.round(matches / this.concludedImages.length * 100)
        },
        amdCount() { return this.concludedImages.filter(i => i.category === 'amd').length },
        glaucomaCount() { return this.concludedImages.filter(i => i.category === 'glaucoma').length },
        drCount() { return this.concludedImages.filter(i => i.category === 'dr').length },
        amdAgreement() {
            const items = this.concludedImages.filter(i => i.category === 'amd')
            if (!items.length) return 0
            return Math.round(items.filter(i => i.doctor_amd === i.ai_amd).length / items.length * 100)
        },
        glaucomaAgreement() {
            const items = this.concludedImages.filter(i => i.category === 'glaucoma')
            if (!items.length) return 0
            return Math.round(items.filter(i => i.doctor_glaucoma === i.ai_glaucoma).length / items.length * 100)
        },
        drAgreement() {
            const items = this.concludedImages.filter(i => i.category === 'dr')
            if (!items.length) return 0
            return Math.round(items.filter(i => i.doctor_dr === i.ai_dr).length / items.length * 100)
        }
    },

    mounted() {
        const stored = localStorage.getItem('ddart_doctor')
        if (!stored) { this.$router.push('/login'); return }
        const doctor = JSON.parse(stored)
        this.doctorName = doctor.name
        this.doctorId = doctor.id
        this.loadPending()
    },

    watch: {
        currentIndex() {
            this.currentDiagnosis = { glaucoma: null, dr: null, amd: null }
            this.submitError = ''
        }
    },

    methods: {
        categoryLabel(cat) {
            return { amd: '👁 AMD', glaucoma: '🔵 Glaucoma', dr: '🩸 DR' }[cat] || cat
        },
        doctorAnswer(item) {
            if (item.category === 'amd') return item.doctor_amd
            if (item.category === 'glaucoma') return item.doctor_glaucoma
            if (item.category === 'dr') return item.doctor_dr
            return '—'
        },
        aiAnswer(item) {
            if (item.category === 'amd') return item.ai_amd
            if (item.category === 'glaucoma') return item.ai_glaucoma
            if (item.category === 'dr') return item.ai_dr
            return '—'
        },

        async loadPending() {
            this.pendingLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/research/pending/${this.doctorId}`)
                const data = await res.json()
                this.pendingImages = data.images || []
                this.currentIndex = 0
            } catch { } finally { this.pendingLoading = false }
        },

        async loadConcluded() {
            this.concludedLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/research/concluded/${this.doctorId}`)
                const data = await res.json()
                this.concludedImages = data.results || []
            } catch { } finally { this.concludedLoading = false }
        },

        async submitDiagnosis() {
            if (!this.diagnosisComplete) return
            this.submitting = true
            this.submitError = ''
            try {
                const res = await fetch('https://labiris.myiplist.com/research/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        doctor_id: this.doctorId,
                        image_id: this.currentImage.id,
                        doctor_glaucoma: this.currentDiagnosis.glaucoma || 'N/A',
                        doctor_dr: this.currentDiagnosis.dr || 'N/A',
                        doctor_amd: this.currentDiagnosis.amd || 'N/A'
                    })
                })
                if (!res.ok) { this.submitError = 'Submission failed. Please try again.'; return }
                this.pendingImages.splice(this.currentIndex, 1)
                if (this.currentIndex >= this.pendingImages.length && this.currentIndex > 0) this.currentIndex--
                this.currentDiagnosis = { glaucoma: null, dr: null, amd: null }
            } catch { this.submitError = 'Connection failed.' }
            finally { this.submitting = false }
        },

        logout() {
            localStorage.removeItem('ddart_doctor')
            this.$router.push('/login')
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

.research-container {
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
    max-width: 900px;
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
    max-width: 900px;
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

.badge {
    background: #e53e3e;
    color: white;
    border-radius: 10px;
    padding: 1px 7px;
    font-size: 11px;
    margin-left: 6px;
}

.panel-section {
    width: 100%;
    max-width: 900px;
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

.empty-state {
    padding: 40px;
    text-align: center;
    color: #718096;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
}

.section-hint {
    font-size: 13px;
    color: #718096;
    margin: 0 0 16px;
}

/* Category badge */
.category-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 12px;
}

.cat-amd {
    background: #ebf8ff;
    color: #2b6cb0;
}

.cat-glaucoma {
    background: #f0fff4;
    color: #276749;
}

.cat-dr {
    background: #fff5f5;
    color: #c53030;
}

.image-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    overflow: hidden;
    margin-bottom: 12px;
}

.image-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    border-bottom: 1px solid #e2e8f0;
    background: #f8fafc;
}

.image-counter {
    font-size: 13px;
    font-weight: 600;
    color: #4a5568;
}

.image-nav {
    display: flex;
    gap: 8px;
}

.nav-btn {
    padding: 4px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    background: white;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
}

.nav-btn:hover:not(:disabled) {
    background: #edf2f7;
}

.nav-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.image-card-body {
    display: grid;
    grid-template-columns: 340px 1fr;
    min-height: 360px;
}

.image-side {
    border-right: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background: #1a202c;
}

.fundus-image {
    max-width: 100%;
    max-height: 300px;
    border-radius: 4px;
    object-fit: contain;
}

.image-id {
    color: #718096;
    font-size: 11px;
    margin: 8px 0 0;
}

.diagnosis-side {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.diagnosis-side h3 {
    font-family: 'Playfair Display', serif;
    color: #2c5282;
    font-size: 18px;
    margin: 0;
}

.diagnosis-hint {
    font-size: 12px;
    color: #a0aec0;
    margin: 0;
}

.diagnosis-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.diagnosis-label {
    font-size: 12px;
    font-weight: 700;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.radio-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.radio-option {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border: 1.5px solid #e2e8f0;
    border-radius: 4px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    color: #4a5568;
    transition: all 0.15s;
    background: white;
}

.radio-option input {
    display: none;
}

.radio-option:hover {
    border-color: #2b6cb0;
    color: #2b6cb0;
}

.radio-option.selected {
    border-color: #2b6cb0;
    background: #ebf8ff;
    color: #2b6cb0;
}

.submit-btn {
    padding: 11px;
    background: #2b6cb0;
    color: white;
    border: none;
    border-radius: 4px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
    background: #2c5282;
}

.submit-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.hint {
    font-size: 11px;
    color: #a0aec0;
    margin: 0;
}

.error {
    color: #c53030;
    font-size: 13px;
    font-weight: 600;
    margin: 0;
}

.progress-bar-container {
    height: 4px;
    background: #e2e8f0;
    border-radius: 2px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: #2b6cb0;
    border-radius: 2px;
    transition: width 0.4s ease;
}

/* Agreement */
.agreement-banner {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 32px;
    margin-bottom: 20px;
}

.agreement-score {
    text-align: center;
    min-width: 120px;
}

.agreement-value {
    font-size: 52px;
    font-weight: 700;
    color: #2b6cb0;
    margin: 0;
    font-family: 'Playfair Display', serif;
    line-height: 1;
}

.agreement-label {
    font-size: 12px;
    color: #718096;
    margin: 4px 0 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.agreement-breakdown {
    display: flex;
    gap: 24px;
    flex: 1;
    justify-content: center;
}

.agreement-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}

.agreement-stat .stat-label {
    font-size: 11px;
    color: #a0aec0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.agreement-stat .stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #2d3748;
}

.agreement-stat .stat-count {
    font-size: 10px;
    color: #a0aec0;
}

/* Concluded list */
.concluded-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.concluded-item {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 16px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
}

.concluded-thumb {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
    flex-shrink: 0;
    background: #1a202c;
}

.concluded-info {
    flex: 1;
}

.concluded-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

.concluded-title {
    font-weight: 700;
    color: #2d3748;
    font-size: 13px;
    margin: 0;
}

.comparison-grid {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 13px;
}

.comparison-header {
    display: grid;
    grid-template-columns: 1fr 1fr 100px;
    gap: 8px;
    font-weight: 700;
    color: #a0aec0;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding-bottom: 4px;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 4px;
}

.comparison-row {
    display: grid;
    grid-template-columns: 1fr 1fr 100px;
    gap: 8px;
    align-items: center;
}

.match-yes {
    color: #38a169;
    font-weight: 700;
}

.match-no {
    color: #e53e3e;
    font-weight: 700;
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
    max-width: 900px;
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