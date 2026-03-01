<template>
    <div class="research-container">
        <div class="header">
            <div class="user-bar">
                <span>Dr. {{ doctorName }} — Research Mode</span>
                <button class="logout-btn" @click="logout">Sign Out</button>
            </div>
            <p class="university">Democritus University of Thrace – DDART spin-off company</p>
            <p class="subtitle">Ophthalmology A.I. Screening Program — Research Study</p>
            <div class="logo">DDART<span>AI</span></div>
        </div>

        <div class="panel-tabs">
            <button :class="['panel-tab', { active: tab === 'pending' }]" @click="tab = 'pending'">
                Pending Examinations
                <span v-if="allPending.length" class="badge">{{ allPending.length }}</span>
            </button>
            <button :class="['panel-tab', { active: tab === 'hc' }]" @click="tab = 'hc'; loadHCPending()">
                Health Center Uploads
                <span v-if="hcPending.length" class="badge hc-badge">{{ hcPending.length }}</span>
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
                <div v-else-if="allPending.length === 0" class="empty-state">
                    <p>No pending examinations. All images have been reviewed.</p>
                </div>
                <div v-else>
                    <p class="section-hint">Examine each fundus image and select your diagnosis before submitting.</p>
                    <div class="image-card">
                        <div class="image-card-header">
                            <span class="image-counter">Image {{ currentIndex + 1 }} of {{ allPending.length }}</span>
                            <div class="image-nav">
                                <button class="nav-btn" @click="currentIndex--" :disabled="currentIndex === 0">←</button>
                                <button class="nav-btn" @click="currentIndex++" :disabled="currentIndex === allPending.length - 1">→</button>
                            </div>
                        </div>
                        <div class="image-card-body">
                            <div class="image-side">
                                <img :src="'https://labiris.myiplist.com/research/image/' + currentImage.id" class="fundus-image" />
                                <p class="image-id">Image #{{ currentImage.id }}</p>
                            </div>
                            <div class="diagnosis-side">
                                <h3>Your Diagnosis</h3>
                                <div class="category-badge" :class="'cat-' + currentImage.category">{{ categoryLabel(currentImage.category) }}</div>
                                <p class="diagnosis-hint">Select your diagnosis for this image:</p>
                                <div v-if="currentImage.category === 'amd'" class="diagnosis-group">
                                    <label class="diagnosis-label">AMD</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.amd === 'AMD' }"><input type="radio" v-model="currentDiagnosis.amd" value="AMD" /> AMD Detected</label>
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.amd === 'Normal' }"><input type="radio" v-model="currentDiagnosis.amd" value="Normal" /> Normal</label>
                                    </div>
                                </div>
                                <div v-else-if="currentImage.category === 'glaucoma'" class="diagnosis-group">
                                    <label class="diagnosis-label">Glaucoma</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.glaucoma === 'Glaucoma' }"><input type="radio" v-model="currentDiagnosis.glaucoma" value="Glaucoma" /> Glaucoma</label>
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.glaucoma === 'Healthy' }"><input type="radio" v-model="currentDiagnosis.glaucoma" value="Healthy" /> Healthy</label>
                                    </div>
                                </div>
                                <div v-else-if="currentImage.category === 'dr'" class="diagnosis-group">
                                    <label class="diagnosis-label">Diabetic Retinopathy</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.dr === 'No_DR' }"><input type="radio" v-model="currentDiagnosis.dr" value="No_DR" /> No DR</label>
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.dr === 'Mild' }"><input type="radio" v-model="currentDiagnosis.dr" value="Mild" /> Mild</label>
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.dr === 'Moderate' }"><input type="radio" v-model="currentDiagnosis.dr" value="Moderate" /> Moderate</label>
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.dr === 'Severe' }"><input type="radio" v-model="currentDiagnosis.dr" value="Severe" /> Severe</label>
                                        <label class="radio-option" :class="{ selected: currentDiagnosis.dr === 'Proliferate_DR' }"><input type="radio" v-model="currentDiagnosis.dr" value="Proliferate_DR" /> Proliferative</label>
                                    </div>
                                </div>
                                <p v-if="submitError" class="error">{{ submitError }}</p>
                                <button class="submit-btn" @click="submitDiagnosis" :disabled="submitting || !diagnosisComplete">
                                    {{ submitting ? 'Submitting...' : '✓ Submit Diagnosis' }}
                                </button>
                                <p v-if="!diagnosisComplete" class="hint">Please select a diagnosis to submit.</p>
                            </div>
                        </div>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" :style="{ width: ((currentIndex + 1) / allPending.length * 100) + '%' }"></div>
                    </div>
                </div>
            </div>

            <!-- HEALTH CENTER UPLOADS TAB — BLIND TEST -->
            <div v-else-if="tab === 'hc'" key="hc" class="panel-section">
                <div v-if="hcLoading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading uploads...</p>
                </div>
                <div v-else-if="hcPending.length === 0" class="empty-state">
                    <p>No pending health center uploads requiring review.</p>
                </div>
                <div v-else>
                    <p class="section-hint">
                        Examine each image and provide your diagnosis. AI results are hidden until after you submit.
                    </p>

                    <div class="image-card">
                        <div class="image-card-header">
                            <span class="image-counter">Upload {{ hcIndex + 1 }} of {{ hcPending.length }}</span>
                            <div class="image-nav">
                                <button class="nav-btn" @click="hcIndex--" :disabled="hcIndex === 0">←</button>
                                <button class="nav-btn" @click="hcIndex++" :disabled="hcIndex === hcPending.length - 1">→</button>
                            </div>
                        </div>

                        <div class="image-card-body">
                            <div class="image-side">
                                <img :src="'https://labiris.myiplist.com/research/hc-image/' + currentHC.id + '?doctor_id=' + doctorId" class="fundus-image" />
                                <div class="patient-info-panel">
                                    <div class="patient-info-row">
                                        <span class="pi-label">AMKA</span>
                                        <span class="pi-value amka">{{ currentHC.patient_amka }}</span>
                                    </div>
                                    <div class="patient-info-row">
                                        <span class="pi-label">Health Center</span>
                                        <span class="pi-value">{{ currentHC.center_name }}</span>
                                    </div>
                                    <div class="patient-info-row">
                                        <span class="pi-label">Uploaded</span>
                                        <span class="pi-value">{{ formatDate(currentHC.uploaded_at) }}</span>
                                    </div>
                                </div>
                            </div>

                            <div class="diagnosis-side">
                                <h3>Your Diagnosis</h3>
                                <p class="diagnosis-hint">
                                    Diagnose the conditions below. AI results will be revealed in the Concluded tab.
                                </p>

                                <!-- Only show conditions where AI ≥ 90% — but NO scores shown -->
                                <div v-if="currentHC.ai_glaucoma_conf >= 90" class="diagnosis-group">
                                    <label class="diagnosis-label">Glaucoma</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.glaucoma === 'Glaucoma' }"><input type="radio" v-model="hcDiagnosis.glaucoma" value="Glaucoma" /> Glaucoma</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.glaucoma === 'Healthy' }"><input type="radio" v-model="hcDiagnosis.glaucoma" value="Healthy" /> Healthy</label>
                                    </div>
                                </div>

                                <div v-if="currentHC.ai_dr_conf >= 90" class="diagnosis-group">
                                    <label class="diagnosis-label">Diabetic Retinopathy</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'No DR' }"><input type="radio" v-model="hcDiagnosis.dr" value="No DR" /> No DR</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Mild' }"><input type="radio" v-model="hcDiagnosis.dr" value="Mild" /> Mild</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Moderate' }"><input type="radio" v-model="hcDiagnosis.dr" value="Moderate" /> Moderate</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Severe' }"><input type="radio" v-model="hcDiagnosis.dr" value="Severe" /> Severe</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Proliferative DR' }"><input type="radio" v-model="hcDiagnosis.dr" value="Proliferative DR" /> Proliferative</label>
                                    </div>
                                </div>

                                <div v-if="currentHC.ai_amd_conf >= 90" class="diagnosis-group">
                                    <label class="diagnosis-label">AMD</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.amd === 'AMD' }"><input type="radio" v-model="hcDiagnosis.amd" value="AMD" /> AMD</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.amd === 'Normal' }"><input type="radio" v-model="hcDiagnosis.amd" value="Normal" /> Normal</label>
                                    </div>
                                </div>

                                <div class="blind-notice">
                                    AI confidence scores are hidden during evaluation
                                </div>

                                <p v-if="hcSubmitError" class="error">{{ hcSubmitError }}</p>
                                <button class="submit-btn" @click="submitHCDiagnosis" :disabled="hcSubmitting || !hcDiagnosisComplete">
                                    {{ hcSubmitting ? 'Submitting...' : '✓ Submit Diagnosis' }}
                                </button>
                                <p v-if="!hcDiagnosisComplete" class="hint">Please diagnose all conditions above.</p>
                            </div>
                        </div>
                    </div>

                    <div class="progress-bar-container">
                        <div class="progress-bar" :style="{ width: ((hcIndex + 1) / hcPending.length * 100) + '%' }"></div>
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
                    <div class="concluded-list">
                        <div v-for="item in concludedImages" :key="item.id" class="concluded-item">
                            <img :src="'https://labiris.myiplist.com/research/image/' + item.image_id" class="concluded-thumb" />
                            <div class="concluded-info">
                                <div class="concluded-header">
                                    <p class="concluded-title">Image #{{ item.image_id }}</p>
                                    <div class="category-badge" :class="'cat-' + item.category">{{ categoryLabel(item.category) }}</div>
                                </div>
                                <div class="comparison-grid">
                                    <div class="comparison-header"><span>Your Diagnosis</span><span>AI Diagnosis</span><span>Match</span></div>
                                    <div class="comparison-row">
                                        <span>{{ doctorAnswer(item) }}</span>
                                        <span>{{ aiAnswer(item) }}</span>
                                        <span :class="doctorAnswer(item) === aiAnswer(item) ? 'match-yes' : 'match-no'">{{ doctorAnswer(item) === aiAnswer(item) ? '✓ Match' : '✗ Differ' }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- HC concluded section -->
                    <div v-if="hcConcluded.length" class="hc-concluded-section">
                        <h4 class="hc-concluded-title">Health Center Upload Reviews</h4>
                        <div class="concluded-list">
                            <div v-for="item in hcConcluded" :key="'hc-' + item.id" class="concluded-item">
                                <img :src="'https://labiris.myiplist.com/research/hc-image/' + item.id + '?doctor_id=' + doctorId" class="concluded-thumb" />
                                <div class="concluded-info">
                                    <div class="concluded-header">
                                        <p class="concluded-title">AMKA: {{ item.patient_amka }}</p>
                                        <span class="center-tag">{{ item.center_name }}</span>
                                        <span class="date-tag">{{ formatDate(item.uploaded_at) }}</span>
                                    </div>
                                    <div class="comparison-grid">
                                        <div class="comparison-header"><span>Condition</span><span>Your Answer</span><span>AI Answer</span><span>AI Conf.</span><span>Match</span></div>
                                        <div v-if="item.ai_glaucoma_conf >= 90" class="comparison-row five-col">
                                            <span class="cond-label">Glaucoma</span>
                                            <span>{{ item.doctor_glaucoma }}</span>
                                            <span>{{ item.ai_glaucoma }}</span>
                                            <span class="conf-reveal">{{ item.ai_glaucoma_conf }}%</span>
                                            <span :class="item.doctor_glaucoma === item.ai_glaucoma ? 'match-yes' : 'match-no'">{{ item.doctor_glaucoma === item.ai_glaucoma ? '✓' : '✗' }}</span>
                                        </div>
                                        <div v-if="item.ai_dr_conf >= 90" class="comparison-row five-col">
                                            <span class="cond-label">DR</span>
                                            <span>{{ item.doctor_dr }}</span>
                                            <span>{{ item.ai_dr }}</span>
                                            <span class="conf-reveal">{{ item.ai_dr_conf }}%</span>
                                            <span :class="item.doctor_dr === item.ai_dr ? 'match-yes' : 'match-no'">{{ item.doctor_dr === item.ai_dr ? '✓' : '✗' }}</span>
                                        </div>
                                        <div v-if="item.ai_amd_conf >= 90" class="comparison-row five-col">
                                            <span class="cond-label">AMD</span>
                                            <span>{{ item.doctor_amd }}</span>
                                            <span>{{ item.ai_amd }}</span>
                                            <span class="conf-reveal">{{ item.ai_amd_conf }}%</span>
                                            <span :class="item.doctor_amd === item.ai_amd ? 'match-yes' : 'match-no'">{{ item.doctor_amd === item.ai_amd ? '✓' : '✗' }}</span>
                                        </div>
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
            doctorName: '', doctorId: null,
            tab: 'pending',
            allPending: [], pendingLoading: false,
            currentIndex: 0,
            currentDiagnosis: { glaucoma: null, dr: null, amd: null },
            submitting: false, submitError: '',
            hcPending: [], hcLoading: false,
            hcIndex: 0,
            hcDiagnosis: { glaucoma: null, dr: null, amd: null },
            hcSubmitting: false, hcSubmitError: '',
            concludedImages: [], hcConcluded: [], concludedLoading: false
        }
    },

    computed: {
        currentImage() { return this.allPending[this.currentIndex] || {} },
        currentHC() { return this.hcPending[this.hcIndex] || {} },

        diagnosisComplete() {
            const cat = this.currentImage.category
            if (cat === 'amd') return !!this.currentDiagnosis.amd
            if (cat === 'glaucoma') return !!this.currentDiagnosis.glaucoma
            if (cat === 'dr') return !!this.currentDiagnosis.dr
            return false
        },

        hcDiagnosisComplete() {
            const hc = this.currentHC
            if (!hc.id) return false
            if (hc.ai_glaucoma_conf >= 90 && !this.hcDiagnosis.glaucoma) return false
            if (hc.ai_dr_conf >= 90 && !this.hcDiagnosis.dr) return false
            if (hc.ai_amd_conf >= 90 && !this.hcDiagnosis.amd) return false
            return true
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
            return items.length ? Math.round(items.filter(i => i.doctor_amd === i.ai_amd).length / items.length * 100) : 0
        },
        glaucomaAgreement() {
            const items = this.concludedImages.filter(i => i.category === 'glaucoma')
            return items.length ? Math.round(items.filter(i => i.doctor_glaucoma === i.ai_glaucoma).length / items.length * 100) : 0
        },
        drAgreement() {
            const items = this.concludedImages.filter(i => i.category === 'dr')
            return items.length ? Math.round(items.filter(i => i.doctor_dr === i.ai_dr).length / items.length * 100) : 0
        }
    },

    mounted() {
        const stored = localStorage.getItem('ddart_doctor')
        if (!stored) { this.$router.push('/login'); return }
        const doctor = JSON.parse(stored)
        this.doctorName = doctor.name
        this.doctorId = doctor.id
        this.loadPending()
        this.loadHCPending()
    },

    watch: {
        currentIndex() { this.currentDiagnosis = { glaucoma: null, dr: null, amd: null }; this.submitError = '' },
        hcIndex() { this.hcDiagnosis = { glaucoma: null, dr: null, amd: null }; this.hcSubmitError = '' }
    },

    methods: {
        categoryLabel(cat) { return { amd: 'AMD', glaucoma: 'Glaucoma', dr: 'DR' }[cat] || cat },
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
        formatDate(dt) {
            if (!dt) return '—'
            return new Date(dt).toLocaleDateString('el-GR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
        },

        async loadPending() {
            this.pendingLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/research/pending/${this.doctorId}`)
                const data = await res.json()
                this.allPending = data.images || []
                this.currentIndex = 0
            } catch { } finally { this.pendingLoading = false }
        },

        async loadHCPending() {
            this.hcLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/research/pending-hc?doctor_id=${this.doctorId}`)
                const data = await res.json()
                // Only include images where at least one condition is ≥ 90%
                this.hcPending = (Array.isArray(data) ? data : []).filter(hc =>
                    hc.ai_glaucoma_conf >= 90 || hc.ai_dr_conf >= 90 || hc.ai_amd_conf >= 90
                )
                this.hcIndex = 0
            } catch { } finally { this.hcLoading = false }
        },

        async loadConcluded() {
            this.concludedLoading = true
            try {
                const [res1, res2] = await Promise.all([
                    fetch(`https://labiris.myiplist.com/research/concluded/${this.doctorId}`),
                    fetch(`https://labiris.myiplist.com/research/concluded-hc?doctor_id=${this.doctorId}`)
                ])
                const data1 = await res1.json()
                const data2 = await res2.json()
                this.concludedImages = data1.results || []
                this.hcConcluded = Array.isArray(data2) ? data2 : []
            } catch { } finally { this.concludedLoading = false }
        },

        async submitDiagnosis() {
            if (!this.diagnosisComplete) return
            this.submitting = true; this.submitError = ''
            try {
                const res = await fetch('https://labiris.myiplist.com/research/submit', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        doctor_id: this.doctorId, image_id: this.currentImage.id,
                        doctor_glaucoma: this.currentDiagnosis.glaucoma || 'N/A',
                        doctor_dr: this.currentDiagnosis.dr || 'N/A',
                        doctor_amd: this.currentDiagnosis.amd || 'N/A'
                    })
                })
                if (!res.ok) { this.submitError = 'Submission failed. Please try again.'; return }
                this.allPending.splice(this.currentIndex, 1)
                if (this.currentIndex >= this.allPending.length && this.currentIndex > 0) this.currentIndex--
                this.currentDiagnosis = { glaucoma: null, dr: null, amd: null }
            } catch { this.submitError = 'Connection failed.' }
            finally { this.submitting = false }
        },

        async submitHCDiagnosis() {
            if (!this.hcDiagnosisComplete) return
            this.hcSubmitting = true; this.hcSubmitError = ''
            const hc = this.currentHC
            try {
                const res = await fetch('https://labiris.myiplist.com/research/submit-hc', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        upload_id: hc.id, doctor_id: this.doctorId,
                        doctor_glaucoma: this.hcDiagnosis.glaucoma || 'N/A',
                        doctor_dr: this.hcDiagnosis.dr || 'N/A',
                        doctor_amd: this.hcDiagnosis.amd || 'N/A'
                    })
                })
                if (!res.ok) { this.hcSubmitError = 'Submission failed. Please try again.'; return }
                this.hcPending.splice(this.hcIndex, 1)
                if (this.hcIndex >= this.hcPending.length && this.hcIndex > 0) this.hcIndex--
                this.hcDiagnosis = { glaucoma: null, dr: null, amd: null }
            } catch { this.hcSubmitError = 'Connection failed.' }
            finally { this.hcSubmitting = false }
        },

        logout() { localStorage.removeItem('ddart_doctor'); this.$router.push('/login') }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; min-height: 100%; background: #f0f4f8; font-family: 'Source Sans 3', sans-serif; }

.research-container { display: flex; flex-direction: column; align-items: center; padding: 30px 20px 0; min-height: 100vh; }
.header { text-align: center; margin-bottom: 24px; width: 100%; max-width: 900px; }
.user-bar { display: flex; align-items: center; justify-content: flex-end; gap: 10px; margin-bottom: 10px; font-size: 13px; color: #4a5568; }
.logout-btn { padding: 4px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; font-family: 'Source Sans 3', sans-serif; background: none; border: 1px solid #e2e8f0; color: #718096; transition: background 0.2s; }
.logout-btn:hover { background: #f8fafc; }
.university { font-size: 14px; color: #2c5282; font-weight: 600; margin: 0 0 4px; }
.subtitle { font-size: 13px; color: #4a6fa5; margin: 0 0 16px; }
.logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 18px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; justify-content: center; gap: 2px; }
.logo span { color: #e53e3e; font-size: 48px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }

.panel-tabs { display: flex; gap: 8px; width: 100%; max-width: 900px; margin-bottom: 20px; }
.panel-tab { flex: 1; padding: 10px; border: 1px solid #e2e8f0; border-radius: 4px; background: white; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; transition: all 0.2s; }
.panel-tab:hover { background: #f8fafc; }
.panel-tab.active { background: #2b6cb0; color: white; border-color: #2b6cb0; }
.badge { background: #e53e3e; color: white; border-radius: 10px; padding: 1px 7px; font-size: 11px; margin-left: 6px; }
.hc-badge { background: #805ad5; }

.panel-section { width: 100%; max-width: 900px; margin-bottom: 24px; }
.loading-state { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 40px; color: #718096; background: white; border: 1px solid #e2e8f0; border-radius: 4px; }
.spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #2b6cb0; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state { padding: 40px; text-align: center; color: #718096; background: white; border: 1px solid #e2e8f0; border-radius: 4px; }
.section-hint { font-size: 13px; color: #718096; margin: 0 0 16px; }

.category-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
.cat-amd { background: #ebf8ff; color: #2b6cb0; }
.cat-glaucoma { background: #f0fff4; color: #276749; }
.cat-dr { background: #fff5f5; color: #c53030; }

.image-card { background: white; border: 1px solid #e2e8f0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); overflow: hidden; margin-bottom: 12px; }
.image-card-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid #e2e8f0; background: #f8fafc; }
.image-counter { font-size: 13px; font-weight: 600; color: #4a5568; }
.image-nav { display: flex; gap: 8px; }
.nav-btn { padding: 4px 12px; border: 1px solid #e2e8f0; border-radius: 4px; background: white; cursor: pointer; font-size: 14px; transition: all 0.2s; }
.nav-btn:hover:not(:disabled) { background: #edf2f7; }
.nav-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.image-card-body { display: grid; grid-template-columns: 320px 1fr; min-height: 380px; }
.image-side { border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; background: #1a202c; gap: 12px; }
.fundus-image { max-width: 100%; max-height: 260px; border-radius: 4px; object-fit: contain; }
.image-id { color: #718096; font-size: 11px; margin: 0; }

.patient-info-panel { width: 100%; background: rgba(255,255,255,0.07); border-radius: 6px; padding: 10px 14px; display: flex; flex-direction: column; gap: 6px; }
.patient-info-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
.pi-label { font-size: 10px; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap; padding-top: 1px; }
.pi-value { font-size: 12px; color: rgba(255,255,255,0.9); font-weight: 600; text-align: right; }
.pi-value.amka { font-family: monospace; font-size: 13px; letter-spacing: 1px; color: #63b3ed; }

.diagnosis-side { padding: 20px 24px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; }
.diagnosis-side h3 { font-family: 'Playfair Display', serif; color: #2c5282; font-size: 18px; margin: 0; }
.diagnosis-hint { font-size: 12px; color: #a0aec0; margin: 0; }

.diagnosis-group { display: flex; flex-direction: column; gap: 8px; }
.diagnosis-label { font-size: 12px; font-weight: 700; color: #4a5568; text-transform: uppercase; letter-spacing: 0.5px; }
.radio-group { display: flex; flex-wrap: wrap; gap: 6px; }
.radio-option { display: flex; align-items: center; gap: 6px; padding: 7px 14px; border: 1.5px solid #e2e8f0; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 600; color: #4a5568; transition: all 0.15s; background: white; }
.radio-option input { display: none; }
.radio-option:hover { border-color: #2b6cb0; color: #2b6cb0; }
.radio-option.selected { border-color: #2b6cb0; background: #ebf8ff; color: #2b6cb0; }

.blind-notice { font-size: 11px; color: #a0aec0; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px 12px; text-align: center; font-style: italic; }

.submit-btn { padding: 11px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.submit-btn:hover:not(:disabled) { background: #2c5282; }
.submit-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.hint { font-size: 11px; color: #a0aec0; margin: 0; }
.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0; }

.progress-bar-container { height: 4px; background: #e2e8f0; border-radius: 2px; overflow: hidden; }
.progress-bar { height: 100%; background: #2b6cb0; border-radius: 2px; transition: width 0.4s ease; }

.agreement-banner { background: white; border: 1px solid #e2e8f0; border-radius: 4px; padding: 24px; display: flex; align-items: center; gap: 32px; margin-bottom: 20px; }
.agreement-score { text-align: center; min-width: 120px; }
.agreement-value { font-size: 52px; font-weight: 700; color: #2b6cb0; margin: 0; font-family: 'Playfair Display', serif; line-height: 1; }
.agreement-label { font-size: 12px; color: #718096; margin: 4px 0 0; text-transform: uppercase; letter-spacing: 0.5px; }
.agreement-breakdown { display: flex; gap: 24px; flex: 1; justify-content: center; }
.agreement-stat { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.agreement-stat .stat-label { font-size: 11px; color: #a0aec0; text-transform: uppercase; letter-spacing: 0.5px; }
.agreement-stat .stat-value { font-size: 28px; font-weight: 700; color: #2d3748; }
.agreement-stat .stat-count { font-size: 10px; color: #a0aec0; }

.concluded-list { display: flex; flex-direction: column; gap: 12px; }
.concluded-item { background: white; border: 1px solid #e2e8f0; border-radius: 4px; padding: 16px; display: flex; gap: 16px; align-items: flex-start; }
.concluded-thumb { width: 80px; height: 80px; object-fit: cover; border-radius: 4px; border: 1px solid #e2e8f0; flex-shrink: 0; background: #1a202c; }
.concluded-info { flex: 1; }
.concluded-header { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }
.concluded-title { font-weight: 700; color: #2d3748; font-size: 13px; margin: 0; }
.center-tag { background: #e9d8fd; color: #553c9a; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px; }
.date-tag { font-size: 11px; color: #a0aec0; }
.comparison-grid { display: flex; flex-direction: column; gap: 4px; font-size: 13px; }
.comparison-header { display: grid; grid-template-columns: 1fr 1fr 100px; gap: 8px; font-weight: 700; color: #a0aec0; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; padding-bottom: 4px; border-bottom: 1px solid #e2e8f0; margin-bottom: 4px; }
.comparison-header.five-col, .comparison-row.five-col { grid-template-columns: 100px 1fr 1fr 60px 50px; }
.comparison-row { display: grid; grid-template-columns: 1fr 1fr 100px; gap: 8px; align-items: center; }
.cond-label { font-weight: 700; color: #4a5568; font-size: 12px; }
.conf-reveal { font-weight: 700; color: #2b6cb0; font-size: 12px; }
.match-yes { color: #38a169; font-weight: 700; }
.match-no { color: #e53e3e; font-weight: 700; }

.hc-concluded-section { margin-top: 28px; }
.hc-concluded-title { font-family: 'Playfair Display', serif; font-size: 16px; color: #2c5282; margin: 0 0 14px; }

.fade-slide-enter-active { transition: all 0.3s ease; }
.fade-slide-leave-active { transition: all 0.2s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-6px); }

.footer { width: 100%; max-width: 900px; display: flex; justify-content: space-between; align-items: center; padding: 16px 0 24px; border-top: 1px solid #e2e8f0; margin-top: auto; }
.dept-logo { height: 55px; width: auto; object-fit: contain; }
.footer-right { text-align: right; }
.footer-right p { font-size: 12px; color: #718096; margin: 2px 0; }
.footer-right a { color: #2b6cb0; text-decoration: none; }
.made-by { font-size: 10px; color: #cbd5e0; margin-top: 4px; }
</style>