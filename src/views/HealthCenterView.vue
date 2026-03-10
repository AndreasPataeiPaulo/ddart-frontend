<template>
    <div class="hc-container" :class="{ dark: isDark }">

        <!-- Success overlay after upload -->
        <transition name="overlay-fade">
            <div v-if="showSuccess" class="success-overlay">
                <div class="success-content">
                    <div class="success-icon">
                        <svg viewBox="0 0 52 52" fill="none">
                            <circle cx="26" cy="26" r="25" stroke="#48bb78" stroke-width="2"/>
                            <path d="M14 26l8 8 16-16" stroke="#48bb78" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <h3>{{ t('Image Uploaded', 'Η εικόνα ανέβηκε') }}</h3>
                    <p>{{ t('AI analysis complete. The research team will review the results.', 'Η ανάλυση ΤΝ ολοκληρώθηκε. Η ερευνητική ομάδα θα αξιολογήσει τα αποτελέσματα.') }}</p>
                    <div class="ai-results">
                        <!-- Glaucoma result -->
                        <div v-if="centerSpecialty === 'glaucoma'" class="ai-result-row">
                            <span class="ai-label">{{ t('Glaucoma', 'Γλαύκωμα') }}</span>
                            <span v-if="lastResult.ai_glaucoma_conf >= 90" :class="['ai-value', lastResult.ai_glaucoma !== 'Healthy' ? 'positive' : 'negative']">
                                {{ lastResult.ai_glaucoma }} ({{ lastResult.ai_glaucoma_conf }}%)
                            </span>
                            <span v-else class="ai-value inconclusive">{{ t('Inconclusive', 'Αναποφάσιστο') }} ({{ lastResult.ai_glaucoma_conf }}%)</span>
                        </div>
                        <!-- DR result -->
                        <div v-else-if="centerSpecialty === 'dr'" class="ai-result-row">
                            <span class="ai-label">{{ t('Diabetic Retinopathy', 'Διαβητική Αμφιβληστροειδοπάθεια') }}</span>
                            <span v-if="lastResult.ai_dr_conf >= 90" :class="['ai-value', lastResult.ai_dr !== 'No_DR' ? 'positive' : 'negative']">
                                {{ lastResult.ai_dr }} ({{ lastResult.ai_dr_conf }}%)
                            </span>
                            <span v-else class="ai-value inconclusive">{{ t('Inconclusive', 'Αναποφάσιστο') }} ({{ lastResult.ai_dr_conf }}%)</span>
                        </div>
                        <!-- AMD result -->
                        <div v-else-if="centerSpecialty === 'amd'" class="ai-result-row">
                            <span class="ai-label">{{ t('AMD', 'ΗΩΕ') }}</span>
                            <span v-if="lastResult.ai_amd_conf >= 90" :class="['ai-value', lastResult.ai_amd !== 'Normal' ? 'positive' : 'negative']">
                                {{ lastResult.ai_amd }} ({{ lastResult.ai_amd_conf }}%)
                            </span>
                            <span v-else class="ai-value inconclusive">{{ t('Inconclusive', 'Αναποφάσιστο') }} ({{ lastResult.ai_amd_conf }}%)</span>
                        </div>
                    </div>
                    <button class="success-btn" @click="resetForm">{{ t('Upload Another', 'Ανέβασμα Άλλης') }}</button>
                </div>
            </div>
        </transition>

        <!-- Header -->
        <div class="hc-header">
            <div class="header-controls">
                <div class="lang-toggle">
                    <button :class="['lang-btn', { active: lang === 'en' }]" @click="setLang('en')">EN</button>
                    <span class="lang-sep">|</span>
                    <button :class="['lang-btn', { active: lang === 'gr' }]" @click="setLang('gr')">EL</button>
                </div>
                <button class="dark-btn" @click="toggleDark">{{ isDark ? 'Light' : 'Dark' }}</button>
                <button class="logout-btn" @click="logout">{{ t('Sign Out', 'Αποσύνδεση') }}</button>
            </div>
            <div class="logo">DDART<span>AI</span></div>
            <div class="center-name">{{ centerName }}</div>
            <div class="center-meta">
                <span :class="['specialty-badge-hc', centerSpecialty]">{{ specialtyLabelFull(centerSpecialty) }}</span>
                <span class="ai-model-tag">AI: DDART AI 1.0</span>
            </div>
            <p class="center-subtitle">{{ t('Retinal Image Upload Portal', 'Πύλη Ανεβάσματος Εικόνων Αμφιβληστροειδούς') }}</p>
        </div>

        <!-- Upload card -->
        <div class="upload-card">
            <div class="upload-card-inner">

                <div class="upload-left">
                    <h2>{{ t('Upload Patient Image', 'Ανέβασμα Εικόνας Ασθενούς') }}</h2>
                    <p>{{ t('Upload a retinal fundus photograph for immediate AI analysis. As a ' + specialtyLabelFull(centerSpecialty) + ' center, the image will be screened specifically for this condition using ResNet-50.', 'Ανεβάστε φωτογραφία βυθού αμφιβληστροειδούς για ακαριαία ανάλυση ΤΝ με το μοντέλο ResNet-50.') }}</p>
                    <div class="instructions">
                        <div class="instruction-step">
                            <span class="step-num">1</span>
                            <span>{{ t('Enter the patient\'s social security number', 'Εισάγετε τον αριθμό ΑΜΚΑ του ασθενούς') }}</span>
                        </div>
                        <div class="instruction-step">
                            <span class="step-num">2</span>
                            <span>{{ t('Select or drag a retinal fundus image', 'Επιλέξτε ή σύρετε εικόνα βυθού αμφιβληστροειδούς') }}</span>
                        </div>
                        <div class="instruction-step">
                            <span class="step-num">3</span>
                            <span>{{ t('Submit — AI analysis runs automatically', 'Υποβολή — η ανάλυση ΤΝ εκτελείται αυτόματα') }}</span>
                        </div>
                        <div class="instruction-step">
                            <span class="step-num">4</span>
                            <span>{{ t('Results are sent to the research team for review', 'Τα αποτελέσματα αποστέλλονται στην ερευνητική ομάδα') }}</span>
                        </div>
                    </div>
                </div>

                <div class="upload-right">
                    <div class="field">
                        <label>{{ t('Patient\'s social security number', 'ΑΜΚΑ Ασθενούς') }}</label>
                        <input
                            v-model="patientAmka"
                            type="text"
                            maxlength="11"
                            :placeholder="t('11-digit social security number', '11-ψήφιος αριθμός ΑΜΚΑ')"
                            :class="{ invalid: amkaError }"
                        />
                        <transition name="error-pop">
                            <span v-if="amkaError" class="field-error">{{ amkaError }}</span>
                        </transition>
                    </div>

                    <div
                        class="drop-zone"
                        :class="{ 'drop-active': isDragging, 'has-image': previewUrl }"
                        @dragover.prevent="isDragging = true"
                        @dragleave="isDragging = false"
                        @drop.prevent="handleDrop"
                        @click="$refs.fileInput.click()"
                    >
                        <input ref="fileInput" type="file" accept="image/*" style="display:none" @change="handleFileChange" />
                        <transition name="preview-fade" mode="out-in">
                            <img v-if="previewUrl" :src="previewUrl" class="preview-img" key="preview" />
                            <div v-else class="drop-placeholder" key="placeholder">
                                <div class="drop-icon">
                                    <svg viewBox="0 0 48 48" fill="none" width="40" height="40">
                                        <rect x="6" y="10" width="36" height="28" rx="3" stroke="#a0aec0" stroke-width="2"/>
                                        <circle cx="17" cy="20" r="4" stroke="#a0aec0" stroke-width="2"/>
                                        <path d="M6 32l10-8 8 6 6-5 12 9" stroke="#a0aec0" stroke-width="2" stroke-linejoin="round"/>
                                    </svg>
                                </div>
                                <p class="drop-main">{{ t('Drop image here or click to browse', 'Σύρετε εικόνα εδώ ή κάντε κλικ για αναζήτηση') }}</p>
                                <p class="drop-sub">{{ t('JPG, PNG, TIFF supported', 'Υποστήριξη JPG, PNG, TIFF') }}</p>
                            </div>
                        </transition>
                    </div>

                    <!-- Consent checkbox -->
                    <label class="consent-check" :class="{ checked: consentGiven }" @click="consentGiven = !consentGiven">
                        <span class="consent-box">{{ consentGiven ? '✓' : '' }}</span>
                        <span class="consent-text">{{ t('The patient has consented to the use of this image for AI analysis and research.', 'Ο ασθενής έχει συναινέσει στη χρήση αυτής της εικόνας για ανάλυση ΤΝ και έρευνα.') }}</span>
                    </label>

                    <transition name="error-pop">
                        <p v-if="uploadError" class="error">{{ uploadError }}</p>
                    </transition>

                    <div class="consent-check" :class="{ checked: consentChecked }" @click="consentChecked = !consentChecked">
                        <div class="consent-box">{{ consentChecked ? '✓' : '' }}</div>
                        <span class="consent-text">{{ t('The patient has consented to the use of this image for AI screening and research.', 'Ο ασθενής έχει δώσει συγκατάθεση για τη χρήση αυτής της εικόνας για ανάλυση ΤΝ και έρευνα.') }}</span>
                    </div>

                    <button class="submit-btn" @click="uploadImage" :disabled="uploading || !selectedFile || !patientAmka || !consentGiven">
                        <span class="btn-text">{{ uploading ? t('Analysing...', 'Ανάλυση...') : t('Upload and Analyse', 'Ανέβασμα και Ανάλυση') }}</span>
                        <span v-if="uploading" class="btn-spinner"></span>
                    </button>

                    <p v-if="uploading" class="uploading-note">
                        {{ t('AI is analysing the image. This may take a moment.', 'Η ΤΝ αναλύει την εικόνα. Αυτό μπορεί να διαρκέσει λίγο.') }}
                    </p>
                </div>
            </div>
        </div>

        <div class="hc-footer">
            <p>{{ t('For technical support contact', 'Για τεχνική υποστήριξη επικοινωνήστε') }} <a href="mailto:ddart@med.duth.gr">ddart@med.duth.gr</a></p>
            <p class="made-by">Made by Andreas</p>
        </div>
    </div>
</template>

<script>
import { useLanguage } from '../composables/useLanguage.js'

export default {
    setup() {
        const { lang, setLang, t } = useLanguage()
        return { lang, setLang, t }
    },

    data() {
        return {
            centerName: '',
            healthCenterId: null,
            centerSpecialty: '',
            consentChecked: false,
            patientAmka: '',
            amkaError: '',
            selectedFile: null,
            previewUrl: null,
            isDragging: false,
            uploading: false,
            uploadError: '',
            showSuccess: false,
            centerSpecialty: '',
            centerId: '',
            consentGiven: false,
            lastResult: {},
            isDark: localStorage.getItem('ddart_dark') === 'true',
            showLogoutOverlay: false,
            logoutBarWidth: 0
        }
    },

    mounted() {
        const hc = localStorage.getItem('ddart_health_center')
        if (!hc) { this.$router.push('/login'); return }
        const parsed = JSON.parse(hc)
        this.centerName = parsed.name
        this.healthCenterId = parsed.id
        this.centerSpecialty = parsed.specialty || ''
        this.centerSpecialty = parsed.specialty || ''
        this.centerId = parsed.center_id || ''
    },

    watch: {
        patientAmka(val) {
            if (val && (val.length !== 11 || !/^\d+$/.test(val))) {
                this.amkaError = this.t('Must be exactly 11 digits', 'Πρέπει να είναι ακριβώς 11 ψηφία')
            } else {
                this.amkaError = ''
            }
        }
    },

    methods: {
        toggleDark() {
            this.isDark = !this.isDark
            localStorage.setItem('ddart_dark', this.isDark)
        },

        logout() {
            this.showLogoutOverlay = true
            this.logoutBarWidth = 0
            const start = performance.now()
            const duration = 2500
            const animate = (now) => {
                const progress = Math.min((now - start) / duration, 1)
                this.logoutBarWidth = Math.round((1 - Math.pow(1 - progress, 3)) * 100)
                if (progress < 1) {
                    requestAnimationFrame(animate)
                } else {
                    setTimeout(() => {
                        localStorage.removeItem('ddart_health_center')
                        this.$router.push('/login')
                    }, 100)
                }
            }
            requestAnimationFrame(animate)
        },

        handleFileChange(e) {
            const file = e.target.files[0]
            if (file) this.setFile(file)
        },

        handleDrop(e) {
            this.isDragging = false
            const file = e.dataTransfer.files[0]
            if (file && file.type.startsWith('image/')) this.setFile(file)
            else this.uploadError = this.t('Please drop an image file', 'Παρακαλώ σύρετε αρχείο εικόνας')
        },

        setFile(file) {
            this.selectedFile = file
            this.uploadError = ''
            this.consentGiven = false
            const reader = new FileReader()
            reader.onload = (e) => { this.previewUrl = e.target.result }
            reader.readAsDataURL(file)
        },

        async uploadImage() {
            this.uploadError = ''
            if (!this.patientAmka || this.patientAmka.length !== 11 || !/^\d+$/.test(this.patientAmka)) {
                this.uploadError = this.t('Please enter a valid 11-digit social security number', 'Παρακαλώ εισάγετε έγκυρο 11-ψήφιο ΑΜΚΑ')
                return
            }
            if (!this.selectedFile) {
                this.uploadError = this.t('Please select an image', 'Παρακαλώ επιλέξτε εικόνα')
                return
            }
            this.uploading = true
            const b64 = await new Promise((resolve) => {
                const reader = new FileReader()
                reader.onload = (e) => resolve(e.target.result.split(',')[1])
                reader.readAsDataURL(this.selectedFile)
            })
            try {
                const res = await fetch('https://labiris.myiplist.com/health-center/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ health_center_id: this.healthCenterId, patient_amka: this.patientAmka, image_b64: b64, specialty: this.centerSpecialty })
                })
                const data = await res.json()
                if (!res.ok) { this.uploadError = data.detail || this.t('Upload failed', 'Αποτυχία ανεβάσματος'); return }
                this.lastResult = data
                this.showSuccess = true
            } catch {
                this.uploadError = this.t('Connection failed. Please try again.', 'Αποτυχία σύνδεσης. Δοκιμάστε ξανά.')
            } finally {
                this.uploading = false
            }
        },

        specialtyLabelFull(s) {
            return { glaucoma: 'Glaucoma', dr: 'Diabetic Retinopathy', amd: 'AMD' }[s] || s
        },

        resetForm() {
            this.showSuccess = false
            this.patientAmka = ''
            this.selectedFile = null
            this.previewUrl = null
            this.uploadError = ''
            this.lastResult = {}
            this.consentChecked = false
            if (this.$refs.fileInput) this.$refs.fileInput.value = ''
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; min-height: 100%; background: #f0f4f8; font-family: 'Source Sans 3', sans-serif; overflow-x: hidden; }


/* Logout / entry overlay */
.entry-overlay { position: fixed; inset: 0; z-index: 9999; background: radial-gradient(ellipse at center, #0d1f3c 0%, #060d1a 100%); display: flex; align-items: center; justify-content: center; }
.entry-content { display: flex; flex-direction: column; align-items: center; gap: 20px; }
.retinal-scanner { position: relative; width: 200px; height: 200px; animation: scanner-appear 0.5s ease both; }
@keyframes scanner-appear { from { opacity: 0; transform: scale(0.85); } to { opacity: 1; transform: scale(1); } }
.retina-svg { width: 100%; height: 100%; }
.ring-draw { animation: ring-draw 1.8s 0.3s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw { from { stroke-dashoffset: 565; } to { stroke-dashoffset: 0; } }
.ring-draw-2 { animation: ring-draw-2 1.4s 0.5s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw-2 { from { stroke-dashoffset: 415; } to { stroke-dashoffset: 0; } }
.crosshair { opacity: 0; animation: lo-fade-in 0.4s 1s ease forwards; }
@keyframes lo-fade-in { to { opacity: 1; } }
.vessel { stroke-dasharray: 200; stroke-dashoffset: 200; animation: vessel-draw 1s 0.8s ease forwards; }
@keyframes vessel-draw { to { stroke-dashoffset: 0; } }
.bracket { opacity: 0; animation: lo-fade-in 0.5s 0.2s ease forwards; }
.scanner-beam { transform-origin: 100px 100px; animation: scan-rotate 2s linear infinite; }
@keyframes scan-rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent 0%, rgba(99,179,237,0.0) 20%, rgba(99,179,237,0.6) 50%, rgba(99,179,237,0.0) 80%, transparent 100%); animation: scan-sweep 2s ease-in-out infinite; border-radius: 1px; }
@keyframes scan-sweep { 0% { top: 10%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 90%; opacity: 0; } }
.glint { position: absolute; width: 4px; height: 4px; background: #63b3ed; border-radius: 50%; animation: glint-pulse 2s ease-in-out infinite; box-shadow: 0 0 6px #63b3ed; }
.glint-1 { top: 6px; left: 50%; animation-delay: 0s; }
.glint-2 { top: 50%; right: 6px; animation-delay: 0.66s; }
.glint-3 { bottom: 6px; left: 50%; animation-delay: 1.33s; }
@keyframes glint-pulse { 0%,100% { opacity: 0.3; transform: scale(1); } 50% { opacity: 1; transform: scale(1.5); } }
.entry-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 22px; font-weight: 700; color: white; letter-spacing: 4px; display: flex; align-items: baseline; gap: 2px; animation: lo-logo-appear 0.6s 0.4s cubic-bezier(0.4,0,0.2,1) both; }
.entry-ddart { color: white; }
.entry-ai { color: #e53e3e; font-size: 72px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; }
.entry-bar { width: 200px; height: 2px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.entry-bar-fill { height: 100%; background: linear-gradient(90deg, #4299e1, #63b3ed); border-radius: 2px; transition: width 0.05s linear; }
.entry-msg { color: rgba(255,255,255,0.55); font-size: 13px; font-weight: 400; letter-spacing: 1px; text-transform: uppercase; margin: 0; animation: lo-msg-appear 0.5s 0.6s cubic-bezier(0.4,0,0.2,1) both; }
@keyframes lo-logo-appear { from { opacity: 0; transform: scale(0.92) translateY(8px); } to { opacity: 1; transform: scale(1) translateY(0); } }
@keyframes lo-msg-appear { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.overlay-fade-enter-active, .overlay-fade-leave-active { transition: opacity 0.5s ease; }
.overlay-fade-enter-from, .overlay-fade-leave-to { opacity: 0; }

.hc-container { display: flex; flex-direction: column; align-items: center; padding: 30px 20px 0; min-height: 100vh; background: #f0f4f8; transition: background 0.4s ease; }

.success-overlay { position: fixed; inset: 0; z-index: 9999; background: rgba(10, 20, 40, 0.92); display: flex; align-items: center; justify-content: center; padding: 20px; }
.success-content { background: white; border-radius: 12px; padding: 40px; max-width: 480px; width: 100%; display: flex; flex-direction: column; align-items: center; gap: 16px; animation: success-appear 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
@keyframes success-appear { from { opacity: 0; transform: scale(0.9) translateY(20px); } to { opacity: 1; transform: scale(1) translateY(0); } }
.success-icon svg { width: 56px; height: 56px; }
.success-content h3 { font-family: 'Playfair Display', serif; font-size: 22px; color: #2d3748; margin: 0; }
.success-content p { font-size: 14px; color: #718096; text-align: center; margin: 0; line-height: 1.6; }
.ai-results { width: 100%; display: flex; flex-direction: column; gap: 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; }
.ai-result-row { display: flex; justify-content: space-between; align-items: center; font-size: 13px; }
.ai-label { color: #4a5568; font-weight: 600; }
.ai-value { font-weight: 700; }
.ai-value.negative { color: #38a169; }
.ai-value.positive { color: #e53e3e; }
.ai-value.inconclusive { color: #d69e2e; font-style: italic; }
.success-btn { padding: 10px 28px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: background 0.2s ease, transform 0.15s ease; }
.success-btn:hover { background: #2c5282; transform: translateY(-1px); }
.overlay-fade-enter-active, .overlay-fade-leave-active { transition: opacity 0.3s ease; }
.overlay-fade-enter-from, .overlay-fade-leave-to { opacity: 0; }

.hc-header { text-align: center; margin-bottom: 24px; width: 100%; position: relative; }
.header-controls { position: absolute; top: 0; right: 0; display: flex; align-items: center; gap: 8px; }
.lang-toggle { display: flex; align-items: center; gap: 4px; }
.lang-btn { background: none; border: none; font-family: 'Source Sans 3', sans-serif; font-size: 12px; font-weight: 700; color: #a0aec0; cursor: pointer; padding: 3px 6px; border-radius: 3px; transition: color 0.2s ease, background 0.2s ease; letter-spacing: 0.5px; }
.lang-btn.active { color: #2b6cb0; background: #ebf8ff; }
.lang-btn:hover:not(.active) { color: #4a5568; }
.lang-sep { color: #e2e8f0; font-size: 12px; }
.dark-btn { background: none; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 11px; font-weight: 700; color: #718096; cursor: pointer; padding: 3px 10px; transition: background 0.2s ease; letter-spacing: 0.4px; }
.dark-btn:hover { background: #edf2f7; }
.logout-btn { background: none; border: 1px solid #fed7d7; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 11px; font-weight: 700; color: #c53030; cursor: pointer; padding: 3px 10px; transition: background 0.2s ease; letter-spacing: 0.4px; }
.logout-btn:hover { background: #fff5f5; }
.logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 18px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; justify-content: center; gap: 2px; transition: color 0.4s ease; }
.logo span { color: #e53e3e; font-size: 48px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }
.center-name { font-size: 16px; font-weight: 700; color: #2c5282; margin-top: 4px; transition: color 0.4s ease; }
.center-subtitle { font-size: 13px; color: #718096; margin: 4px 0 0; transition: color 0.4s ease; }

.upload-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; width: 100%; max-width: 860px; margin-bottom: 24px; box-shadow: 0 2px 16px rgba(0,0,0,0.07); overflow: hidden; transition: background 0.4s ease, border-color 0.4s ease; }
.upload-card-inner { display: grid; grid-template-columns: 280px 1fr; min-height: 420px; }
.upload-left { background: #2b6cb0; padding: 36px 28px; display: flex; flex-direction: column; gap: 20px; transition: background 0.4s ease; }
.upload-left h2 { font-family: 'Playfair Display', serif; color: white; font-size: 20px; margin: 0; }
.upload-left p { color: rgba(255,255,255,0.85); font-size: 13px; line-height: 1.7; margin: 0; }
.instructions { display: flex; flex-direction: column; gap: 12px; margin-top: 4px; }
.instruction-step { display: flex; align-items: flex-start; gap: 10px; color: rgba(255,255,255,0.9); font-size: 13px; line-height: 1.5; }
.step-num { background: rgba(255,255,255,0.2); color: white; font-weight: 700; font-size: 11px; width: 20px; height: 20px; min-width: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 1px; }
.upload-right { padding: 32px 28px; display: flex; flex-direction: column; gap: 16px; }

.field { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 12px; font-weight: 600; color: #4a5568; text-transform: uppercase; letter-spacing: 0.4px; transition: color 0.4s ease; }
.field input { padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; color: #2d3748; outline: none; width: 100%; background: white; transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.4s ease, color 0.4s ease; }
.field input:focus { border-color: #2b6cb0; box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.12); }
.field input.invalid { border-color: #fc8181; }
.field-error { font-size: 11px; color: #c53030; font-weight: 600; }

.drop-zone { border: 2px dashed #e2e8f0; border-radius: 8px; min-height: 180px; display: flex; align-items: center; justify-content: center; cursor: pointer; overflow: hidden; transition: border-color 0.2s ease, background 0.2s ease; position: relative; }
.drop-zone:hover, .drop-zone.drop-active { border-color: #2b6cb0; background: #ebf8ff; }
.drop-zone.has-image { border-style: solid; border-color: #bee3f8; }
.drop-placeholder { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 20px; }
.drop-icon { opacity: 0.5; }
.drop-main { font-size: 13px; color: #718096; margin: 0; font-weight: 600; text-align: center; }
.drop-sub { font-size: 11px; color: #a0aec0; margin: 0; }
.preview-img { width: 100%; height: 200px; object-fit: contain; padding: 8px; }
.preview-fade-enter-active, .preview-fade-leave-active { transition: opacity 0.2s ease; }
.preview-fade-enter-from, .preview-fade-leave-to { opacity: 0; }

.submit-btn { padding: 12px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease; }
.submit-btn:hover:not(:disabled) { background: #2c5282; box-shadow: 0 4px 12px rgba(43, 108, 176, 0.3); transform: translateY(-1px); }
.submit-btn:active:not(:disabled) { transform: translateY(0); box-shadow: none; }
.submit-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.35); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }
@keyframes spin { to { transform: rotate(360deg); } }
.uploading-note { font-size: 12px; color: #718096; text-align: center; margin: 0; line-height: 1.5; }
.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0; }

.hc-footer { width: 100%; max-width: 860px; padding: 16px 0 24px; border-top: 1px solid #e2e8f0; text-align: center; transition: border-color 0.4s ease; }
.hc-footer p { font-size: 12px; color: #718096; margin: 2px 0; transition: color 0.4s ease; }
.hc-footer a { color: #2b6cb0; text-decoration: none; }
.made-by { font-size: 10px; color: #cbd5e0; }

.error-pop-enter-active { transition: opacity 0.25s ease, transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); }
.error-pop-leave-active { transition: opacity 0.15s ease; }
.error-pop-enter-from { opacity: 0; transform: translateY(-4px) scale(0.97); }
.error-pop-leave-to { opacity: 0; }

.dark
/* Logout / entry overlay */
.entry-overlay { position: fixed; inset: 0; z-index: 9999; background: radial-gradient(ellipse at center, #0d1f3c 0%, #060d1a 100%); display: flex; align-items: center; justify-content: center; }
.entry-content { display: flex; flex-direction: column; align-items: center; gap: 20px; }
.retinal-scanner { position: relative; width: 200px; height: 200px; animation: scanner-appear 0.5s ease both; }
@keyframes scanner-appear { from { opacity: 0; transform: scale(0.85); } to { opacity: 1; transform: scale(1); } }
.retina-svg { width: 100%; height: 100%; }
.ring-draw { animation: ring-draw 1.8s 0.3s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw { from { stroke-dashoffset: 565; } to { stroke-dashoffset: 0; } }
.ring-draw-2 { animation: ring-draw-2 1.4s 0.5s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw-2 { from { stroke-dashoffset: 415; } to { stroke-dashoffset: 0; } }
.crosshair { opacity: 0; animation: lo-fade-in 0.4s 1s ease forwards; }
@keyframes lo-fade-in { to { opacity: 1; } }
.vessel { stroke-dasharray: 200; stroke-dashoffset: 200; animation: vessel-draw 1s 0.8s ease forwards; }
@keyframes vessel-draw { to { stroke-dashoffset: 0; } }
.bracket { opacity: 0; animation: lo-fade-in 0.5s 0.2s ease forwards; }
.scanner-beam { transform-origin: 100px 100px; animation: scan-rotate 2s linear infinite; }
@keyframes scan-rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent 0%, rgba(99,179,237,0.0) 20%, rgba(99,179,237,0.6) 50%, rgba(99,179,237,0.0) 80%, transparent 100%); animation: scan-sweep 2s ease-in-out infinite; border-radius: 1px; }
@keyframes scan-sweep { 0% { top: 10%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 90%; opacity: 0; } }
.glint { position: absolute; width: 4px; height: 4px; background: #63b3ed; border-radius: 50%; animation: glint-pulse 2s ease-in-out infinite; box-shadow: 0 0 6px #63b3ed; }
.glint-1 { top: 6px; left: 50%; animation-delay: 0s; }
.glint-2 { top: 50%; right: 6px; animation-delay: 0.66s; }
.glint-3 { bottom: 6px; left: 50%; animation-delay: 1.33s; }
@keyframes glint-pulse { 0%,100% { opacity: 0.3; transform: scale(1); } 50% { opacity: 1; transform: scale(1.5); } }
.entry-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 22px; font-weight: 700; color: white; letter-spacing: 4px; display: flex; align-items: baseline; gap: 2px; animation: lo-logo-appear 0.6s 0.4s cubic-bezier(0.4,0,0.2,1) both; }
.entry-ddart { color: white; }
.entry-ai { color: #e53e3e; font-size: 72px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; }
.entry-bar { width: 200px; height: 2px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.entry-bar-fill { height: 100%; background: linear-gradient(90deg, #4299e1, #63b3ed); border-radius: 2px; transition: width 0.05s linear; }
.entry-msg { color: rgba(255,255,255,0.55); font-size: 13px; font-weight: 400; letter-spacing: 1px; text-transform: uppercase; margin: 0; animation: lo-msg-appear 0.5s 0.6s cubic-bezier(0.4,0,0.2,1) both; }
@keyframes lo-logo-appear { from { opacity: 0; transform: scale(0.92) translateY(8px); } to { opacity: 1; transform: scale(1) translateY(0); } }
@keyframes lo-msg-appear { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.overlay-fade-enter-active, .overlay-fade-leave-active { transition: opacity 0.5s ease; }
.overlay-fade-enter-from, .overlay-fade-leave-to { opacity: 0; }

.dark.hc-container { background: #1a202c; }
.dark .center-name { color: #90cdf4; }
.dark .center-subtitle { color: #7fb3d3; }
.dark .logo { color: #90cdf4; }
.dark .upload-card { background: #2d3748; border-color: #4a5568; box-shadow: 0 2px 16px rgba(0,0,0,0.3); }
.dark .upload-right { background: #2d3748; }
.dark .field label { color: #a0aec0; }
.dark .field input { background: #1a202c; border-color: #4a5568; color: #e2e8f0; }
.dark .field input:focus { border-color: #63b3ed; box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.15); }
.dark .field input::placeholder { color: #4a5568; }
.dark .drop-zone { border-color: #4a5568; }
.dark .drop-zone:hover, .dark .drop-zone.drop-active { border-color: #63b3ed; background: #1a365d; }
.dark .drop-zone.has-image { border-color: #2b6cb0; }
.dark .drop-main { color: #a0aec0; }
.dark .lang-btn.active { color: #63b3ed; background: #1a365d; }
.dark .lang-btn:hover:not(.active) { color: #e2e8f0; }
.dark .lang-sep { color: #4a5568; }
.dark .dark-btn { border-color: #4a5568; color: #a0aec0; }
.dark .dark-btn:hover { background: #3d4a5c; }
.dark .logout-btn { border-color: #744210; color: #fc8181; }
.dark .logout-btn:hover { background: #2d1515; }
.dark .submit-btn:hover:not(:disabled) { box-shadow: 0 4px 12px rgba(99, 179, 237, 0.25); }
.dark .hc-footer { border-top-color: #4a5568; }
.dark .hc-footer p { color: #718096; }
.dark .hc-footer a { color: #63b3ed; }
.dark .success-content { background: #2d3748; }
.dark .success-content h3 { color: #e2e8f0; }
.dark .ai-results { background: #1a202c; border-color: #4a5568; }
.dark .ai-label { color: #a0aec0; }


/* Center identity badge */
.center-badge { background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; }
.center-badge-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.badge-label { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.55); text-transform: uppercase; letter-spacing: 0.5px; }
.badge-value { font-size: 13px; font-weight: 600; color: white; }
.badge-value.mono { font-family: 'Courier New', monospace; letter-spacing: 2px; font-size: 14px; }
.badge-specialty { font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.3px; }
.badge-specialty.glaucoma { background: rgba(72,187,120,0.2); color: #9ae6b4; border: 1px solid rgba(72,187,120,0.3); }
.badge-specialty.dr { background: rgba(237,137,54,0.2); color: #fbd38d; border: 1px solid rgba(237,137,54,0.3); }
.badge-specialty.amd { background: rgba(159,122,234,0.2); color: #d6bcfa; border: 1px solid rgba(159,122,234,0.3); }

/* Consent checkbox */
.consent-check { display: flex; align-items: flex-start; gap: 10px; padding: 10px 12px; border: 1.5px solid #e2e8f0; border-radius: 6px; cursor: pointer; background: white; transition: border-color 0.2s ease, background 0.2s ease; margin-bottom: 2px; }
.consent-check:hover { border-color: #cbd5e0; }
.consent-check.checked { border-color: #2b6cb0; background: #ebf8ff; }
.consent-box { width: 18px; height: 18px; min-width: 18px; border: 2px solid #e2e8f0; border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 900; color: white; background: white; margin-top: 1px; transition: background 0.2s ease, border-color 0.2s ease; }
.consent-check.checked .consent-box { background: #2b6cb0; border-color: #2b6cb0; }
.consent-text { font-size: 12px; color: #4a5568; line-height: 1.5; }
.dark .consent-check { background: #1a202c; border-color: #4a5568; }
.dark .consent-check.checked { background: #1a365d; border-color: #63b3ed; }
.dark .consent-box { background: #1a202c; border-color: #4a5568; }
.dark .consent-check.checked .consent-box { background: #2b6cb0; border-color: #63b3ed; }
.dark .consent-text { color: #a0aec0; }

.center-meta { display: flex; align-items: center; justify-content: center; gap: 10px; margin: 6px 0 2px; }
.specialty-badge-hc { display: inline-flex; align-items: center; padding: 3px 12px; border-radius: 12px; font-size: 12px; font-weight: 700; letter-spacing: 0.3px; }
.specialty-badge-hc.glaucoma { background: #ebf8ff; color: #2b6cb0; }
.specialty-badge-hc.dr { background: #fff5f5; color: #c53030; }
.specialty-badge-hc.amd { background: #faf5ff; color: #6b46c1; }
.ai-model-tag { font-size: 11px; color: #a0aec0; font-weight: 600; letter-spacing: 0.3px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 2px 10px; }
.ai-result-specialty-label { font-size: 11px; font-weight: 700; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #e2e8f0; }
.consent-check { display: flex; align-items: flex-start; gap: 10px; padding: 12px; border: 1.5px solid #e2e8f0; border-radius: 6px; cursor: pointer; background: white; transition: border-color 0.2s, background 0.2s; }
.consent-check:hover { border-color: #bee3f8; }
.consent-check.checked { border-color: #2b6cb0; background: #ebf8ff; }
.consent-box { width: 18px; height: 18px; min-width: 18px; border: 2px solid #e2e8f0; border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 900; color: white; background: white; margin-top: 1px; transition: background 0.2s, border-color 0.2s; }
.consent-check.checked .consent-box { background: #2b6cb0; border-color: #2b6cb0; }
.consent-text { font-size: 12px; color: #4a5568; line-height: 1.5; }
.dark .consent-check { background: #1a202c; border-color: #4a5568; }
.dark .consent-check.checked { background: #1a365d; border-color: #63b3ed; }
.dark .consent-check.checked .consent-box { background: #2b6cb0; border-color: #63b3ed; }
.dark .consent-text { color: #a0aec0; }
.dark .ai-model-tag { background: #2d3748; border-color: #4a5568; color: #718096; }
.dark .ai-result-specialty-label { color: #718096; border-bottom-color: #4a5568; }

@media (max-width: 768px) {
    
/* Logout / entry overlay */
.entry-overlay { position: fixed; inset: 0; z-index: 9999; background: radial-gradient(ellipse at center, #0d1f3c 0%, #060d1a 100%); display: flex; align-items: center; justify-content: center; }
.entry-content { display: flex; flex-direction: column; align-items: center; gap: 20px; }
.retinal-scanner { position: relative; width: 200px; height: 200px; animation: scanner-appear 0.5s ease both; }
@keyframes scanner-appear { from { opacity: 0; transform: scale(0.85); } to { opacity: 1; transform: scale(1); } }
.retina-svg { width: 100%; height: 100%; }
.ring-draw { animation: ring-draw 1.8s 0.3s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw { from { stroke-dashoffset: 565; } to { stroke-dashoffset: 0; } }
.ring-draw-2 { animation: ring-draw-2 1.4s 0.5s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw-2 { from { stroke-dashoffset: 415; } to { stroke-dashoffset: 0; } }
.crosshair { opacity: 0; animation: lo-fade-in 0.4s 1s ease forwards; }
@keyframes lo-fade-in { to { opacity: 1; } }
.vessel { stroke-dasharray: 200; stroke-dashoffset: 200; animation: vessel-draw 1s 0.8s ease forwards; }
@keyframes vessel-draw { to { stroke-dashoffset: 0; } }
.bracket { opacity: 0; animation: lo-fade-in 0.5s 0.2s ease forwards; }
.scanner-beam { transform-origin: 100px 100px; animation: scan-rotate 2s linear infinite; }
@keyframes scan-rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent 0%, rgba(99,179,237,0.0) 20%, rgba(99,179,237,0.6) 50%, rgba(99,179,237,0.0) 80%, transparent 100%); animation: scan-sweep 2s ease-in-out infinite; border-radius: 1px; }
@keyframes scan-sweep { 0% { top: 10%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 90%; opacity: 0; } }
.glint { position: absolute; width: 4px; height: 4px; background: #63b3ed; border-radius: 50%; animation: glint-pulse 2s ease-in-out infinite; box-shadow: 0 0 6px #63b3ed; }
.glint-1 { top: 6px; left: 50%; animation-delay: 0s; }
.glint-2 { top: 50%; right: 6px; animation-delay: 0.66s; }
.glint-3 { bottom: 6px; left: 50%; animation-delay: 1.33s; }
@keyframes glint-pulse { 0%,100% { opacity: 0.3; transform: scale(1); } 50% { opacity: 1; transform: scale(1.5); } }
.entry-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 22px; font-weight: 700; color: white; letter-spacing: 4px; display: flex; align-items: baseline; gap: 2px; animation: lo-logo-appear 0.6s 0.4s cubic-bezier(0.4,0,0.2,1) both; }
.entry-ddart { color: white; }
.entry-ai { color: #e53e3e; font-size: 72px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; }
.entry-bar { width: 200px; height: 2px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.entry-bar-fill { height: 100%; background: linear-gradient(90deg, #4299e1, #63b3ed); border-radius: 2px; transition: width 0.05s linear; }
.entry-msg { color: rgba(255,255,255,0.55); font-size: 13px; font-weight: 400; letter-spacing: 1px; text-transform: uppercase; margin: 0; animation: lo-msg-appear 0.5s 0.6s cubic-bezier(0.4,0,0.2,1) both; }
@keyframes lo-logo-appear { from { opacity: 0; transform: scale(0.92) translateY(8px); } to { opacity: 1; transform: scale(1) translateY(0); } }
@keyframes lo-msg-appear { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.overlay-fade-enter-active, .overlay-fade-leave-active { transition: opacity 0.5s ease; }
.overlay-fade-enter-from, .overlay-fade-leave-to { opacity: 0; }

.hc-container { padding: 16px 16px 0; }
    .header-controls { position: static; justify-content: flex-end; margin-bottom: 12px; }
    .upload-card-inner { grid-template-columns: 1fr; }
    .upload-left { padding: 20px; }
    .upload-right { padding: 20px; }
    .logo span { font-size: 36px; }
}
@media (max-width: 480px) {
    .upload-right { padding: 16px; }
    .header-controls { flex-wrap: wrap; gap: 6px; }
}
</style>