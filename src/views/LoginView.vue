<template>
    <div class="login-container" :class="{ dark: isDark }">

        <!-- Study Official modal -->
        <transition name="modal-fade">
            <div v-if="showStudyModal" class="study-modal-backdrop">
                <div class="study-modal-box">
                    <div class="modal-logo">DDART<span>AI</span></div>
                    <h3>Study Official Access</h3>
                    <p>Enter the study access code to continue.</p>
                    <div class="field" style="width:100%">
                        <input v-model="studyCode" type="password" placeholder="Access code" @keyup.enter="studyLogin" autofocus />
                    </div>
                    <transition name="error-pop">
                        <p v-if="studyError" class="error">{{ studyError }}</p>
                    </transition>
                    <div class="study-modal-btns">
                        <button class="study-back-btn" @click="showStudyModal = false; studyCode = ''; studyError = ''">← Back</button>
                        <button class="submit-btn study-submit" @click="studyLogin" :disabled="!studyCode">Enter</button>
                    </div>
                </div>
            </div>
        </transition>

        <transition name="overlay-fade">
            <div v-if="showOverlay" class="entry-overlay">
                <div class="entry-content">
                    <div class="retinal-scanner">
                        <svg class="retina-svg" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <!-- Outer ring -->
                            <circle cx="100" cy="100" r="90" stroke="rgba(99,179,237,0.15)" stroke-width="1"/>
                            <circle cx="100" cy="100" r="90" stroke="url(#ringGrad)" stroke-width="1.5" stroke-dasharray="565" stroke-dashoffset="565" class="ring-draw"/>
                            <!-- Mid ring -->
                            <circle cx="100" cy="100" r="66" stroke="rgba(99,179,237,0.1)" stroke-width="1"/>
                            <circle cx="100" cy="100" r="66" stroke="rgba(99,179,237,0.4)" stroke-width="1" stroke-dasharray="415" stroke-dashoffset="415" class="ring-draw-2"/>
                            <!-- Inner ring -->
                            <circle cx="100" cy="100" r="42" stroke="rgba(99,179,237,0.08)" stroke-width="1"/>
                            <!-- Crosshairs -->
                            <line x1="100" y1="4" x2="100" y2="30" stroke="rgba(99,179,237,0.3)" stroke-width="1" class="crosshair"/>
                            <line x1="100" y1="170" x2="100" y2="196" stroke="rgba(99,179,237,0.3)" stroke-width="1" class="crosshair"/>
                            <line x1="4" y1="100" x2="30" y2="100" stroke="rgba(99,179,237,0.3)" stroke-width="1" class="crosshair"/>
                            <line x1="170" y1="100" x2="196" y2="100" stroke="rgba(99,179,237,0.3)" stroke-width="1" class="crosshair"/>
                            <!-- Optic nerve/disc -->
                            <circle cx="118" cy="88" r="10" fill="none" stroke="rgba(99,179,237,0.25)" stroke-width="1.5"/>
                            <circle cx="118" cy="88" r="5" fill="rgba(99,179,237,0.12)"/>
                            <!-- Vessels radiating from disc -->
                            <path d="M112 84 Q90 75 70 60" stroke="rgba(99,179,237,0.2)" stroke-width="1.2" fill="none" class="vessel"/>
                            <path d="M110 90 Q88 92 65 98" stroke="rgba(99,179,237,0.2)" stroke-width="1.2" fill="none" class="vessel"/>
                            <path d="M112 95 Q100 112 90 130" stroke="rgba(99,179,237,0.2)" stroke-width="1.2" fill="none" class="vessel"/>
                            <path d="M124 83 Q140 70 155 58" stroke="rgba(99,179,237,0.2)" stroke-width="1.2" fill="none" class="vessel"/>
                            <path d="M126 90 Q145 90 162 95" stroke="rgba(99,179,237,0.2)" stroke-width="1.2" fill="none" class="vessel"/>
                            <path d="M122 96 Q130 114 128 135" stroke="rgba(99,179,237,0.2)" stroke-width="1.2" fill="none" class="vessel"/>
                            <!-- Macula -->
                            <circle cx="82" cy="100" r="8" fill="none" stroke="rgba(229,62,62,0.3)" stroke-width="1" stroke-dasharray="3 3"/>
                            <circle cx="82" cy="100" r="3" fill="rgba(229,62,62,0.2)"/>
                            <!-- Scanner beam -->
                            <defs>
                                <radialGradient id="beamGrad" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="rgba(99,179,237,0.0)"/>
                                    <stop offset="85%" stop-color="rgba(99,179,237,0.06)"/>
                                    <stop offset="100%" stop-color="rgba(99,179,237,0.0)"/>
                                </radialGradient>
                                <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stop-color="#4299e1"/>
                                    <stop offset="100%" stop-color="#63b3ed"/>
                                </linearGradient>
                            </defs>
                            <path d="M100 100 L190 100 A90 90 0 0 1 100 190 Z" fill="url(#beamGrad)" class="scanner-beam"/>
                            <!-- Corner brackets -->
                            <path d="M14 40 L14 14 L40 14" stroke="rgba(99,179,237,0.5)" stroke-width="1.5" fill="none" class="bracket"/>
                            <path d="M160 14 L186 14 L186 40" stroke="rgba(99,179,237,0.5)" stroke-width="1.5" fill="none" class="bracket"/>
                            <path d="M14 160 L14 186 L40 186" stroke="rgba(99,179,237,0.5)" stroke-width="1.5" fill="none" class="bracket"/>
                            <path d="M160 186 L186 186 L186 160" stroke="rgba(99,179,237,0.5)" stroke-width="1.5" fill="none" class="bracket"/>
                        </svg>
                        <!-- Scan line -->
                        <div class="scan-line"></div>
                        <!-- Glint dots around the ring -->
                        <div class="glint glint-1"></div>
                        <div class="glint glint-2"></div>
                        <div class="glint glint-3"></div>
                    </div>
                    <div class="entry-logo">
                        <span class="entry-ddart">DDART</span><span class="entry-ai">AI</span>
                    </div>
                    <div class="entry-bar">
                        <div class="entry-bar-fill" :style="{ width: barWidth + '%' }"></div>
                    </div>
                    <p class="entry-msg">{{ entryMessage }}</p>
                </div>
            </div>
        </transition>

        <div class="header">
            <button class="study-official-btn" @click="showStudyModal = true">Study Official</button>
            <div class="header-controls">
                <div class="lang-toggle">
                    <button :class="['lang-btn', { active: lang === 'en' }]" @click="setLang('en')">EN</button>
                    <span class="lang-sep">|</span>
                    <button :class="['lang-btn', { active: lang === 'gr' }]" @click="setLang('gr')">EL</button>
                </div>
                <button class="dark-btn" @click="toggleDark">{{ isDark ? 'Light' : 'Dark' }}</button>
            </div>
            <transition name="header-fade" mode="out-in">
                <div :key="lang" class="header-text">
                    <p class="university">Democritus University of Thrace – DDART spin-off company</p>
                    <p class="subtitle">{{ t('Ophthalmology A.I. Screening Program', 'Πρόγραμμα Οφθαλμολογικής Διάγνωσης Τ.Ν.') }}</p>
                </div>
            </transition>
            <div class="logo">DDART<span>AI</span></div>
        </div>

        <div class="role-toggle">
            <button :class="['role-btn', { active: role === 'health-center' }]" @click="role = 'health-center'; error = ''">{{ t('Health Center', 'Κέντρο Υγείας') }}</button>
            <button :class="['role-btn', { active: role === 'doctor' }]" @click="role = 'doctor'; error = ''">{{ t('Doctor / Staff', 'Ιατρός / Προσωπικό') }}</button>
        </div>

        <div class="main-card">
            <div class="card-inner">
                <div class="left-panel">
                    <transition name="panel-slide" mode="out-in">

                        <div v-if="role === 'health-center'" key="hc-info" class="left-content">
                            <h2>{{ t('Health Center Portal', 'Πύλη Κέντρου Υγείας') }}</h2>
                            <p>{{ t('Sign in with your health center credentials to upload patient retinal images for immediate AI screening and research review.', 'Συνδεθείτε με τα στοιχεία του κέντρου υγείας σας για να ανεβάσετε εικόνες αμφιβληστροειδούς για διάγνωση ΤΝ και αξιολόγηση από ερευνητές.') }}</p>
                            <ul>
                                <li>{{ t('Images analysed instantly by AI', 'Ακαριαία ανάλυση εικόνων από ΤΝ') }}</li>
                                <li>{{ t('All three conditions screened', 'Έλεγχος και για τις τρεις παθήσεις') }}</li>
                                <li>{{ t('Results reviewed by research team', 'Αποτελέσματα αξιολογούνται από ερευνητές') }}</li>
                                <li>{{ t('Access granted by administrator', 'Πρόσβαση χορηγείται από διαχειριστή') }}</li>
                            </ul>
                        </div>

                        <div v-else key="doctor-info" class="left-content">
                            <h2>{{ t('Doctor Portal', 'Πύλη Ιατρών') }}</h2>
                            <p>{{ t('Access the clinical dashboard to view patient screenings, statistics, and export data for research.', 'Πρόσβαση στον κλινικό πίνακα για προβολή εξετάσεων, στατιστικών και εξαγωγή δεδομένων.') }}</p>
                            <ul>
                                <li>{{ t('View all patient records', 'Προβολή όλων των ασθενών') }}</li>
                                <li>{{ t('Aggregate statistics', 'Συγκεντρωτικά στατιστικά') }}</li>
                                <li>{{ t('Export to CSV', 'Εξαγωγή σε CSV') }}</li>
                                <li>{{ t('Research study participation', 'Συμμετοχή σε ερευνητική μελέτη') }}</li>
                                <li>{{ t('Access approved by administrator', 'Πρόσβαση εγκεκριμένη από διαχειριστή') }}</li>
                            </ul>
                        </div>

                    </transition>
                </div>

                <div class="right-panel">
                    <div class="tabs">
                        <button :class="['tab', { active: mode === 'login' }]" @click="mode = 'login'; error = ''">{{ t('Sign In', 'Σύνδεση') }}</button>
                        <button v-if="role === 'doctor'" :class="['tab', { active: mode === 'signup' }]" @click="mode = 'signup'; error = ''">{{ t('Sign Up', 'Εγγραφή') }}</button>
                    </div>

                    <transition name="form-slide" mode="out-in">

                        <!-- HEALTH CENTER LOGIN -->
                        <div v-if="role === 'health-center' && mode === 'login'" key="hc-login" class="form">
                            <div class="field">
                                <label>{{ t('Health Center Name', 'Όνομα Κέντρου Υγείας') }}</label>
                                <input v-model="centerName" type="text" :placeholder="t('Full name of your health center', 'Πλήρες όνομα κέντρου υγείας')" />
                            </div>
                            <div class="field">
                                <label>{{ t('Password', 'Κωδικός') }}</label>
                                <input v-model="password" type="password" :placeholder="t('Your password', 'Ο κωδικός σας')" @keyup.enter="healthCenterLogin" />
                            </div>
                            <transition name="error-pop">
                                <p v-if="error" class="error">{{ error }}</p>
                            </transition>
                            <button class="submit-btn" @click="healthCenterLogin" :disabled="loading">
                                <span class="btn-text">{{ loading ? t('Signing in...', 'Σύνδεση...') : t('Sign In', 'Σύνδεση') }}</span>
                                <span v-if="loading" class="btn-spinner"></span>
                            </button>
                            <p class="access-note">{{ t('Access is granted by the DDART administrator. Contact ddart@med.duth.gr to register your center.', 'Η πρόσβαση χορηγείται από τον διαχειριστή DDART. Επικοινωνήστε με ddart@med.duth.gr για εγγραφή του κέντρου σας.') }}</p>
                        </div>

                        <!-- DOCTOR LOGIN -->
                        <div v-else-if="role === 'doctor' && mode === 'login'" key="d-login" class="form">
                            <div class="field">
                                <label>{{ t('Email', 'Email') }}</label>
                                <input v-model="email" type="email" :placeholder="t('Your email address', 'Η διεύθυνση email σας')" />
                            </div>
                            <div class="field">
                                <label>{{ t('Password', 'Κωδικός') }}</label>
                                <input v-model="password" type="password" :placeholder="t('Your password', 'Ο κωδικός σας')" @keyup.enter="doctorLogin" />
                            </div>

                            <transition name="error-pop">
                                <p v-if="error" class="error">{{ error }}</p>
                            </transition>
                            <button class="submit-btn" @click="doctorLogin" :disabled="loading">
                                <span class="btn-text">{{ loading ? t('Signing in...', 'Σύνδεση...') : t('Sign In', 'Σύνδεση') }}</span>
                                <span v-if="loading" class="btn-spinner"></span>
                            </button>
                        </div>

                        <!-- DOCTOR SIGNUP -->
                        <div v-else-if="role === 'doctor' && mode === 'signup'" key="d-signup" class="form">
                            <div class="field">
                                <label>{{ t('Full Name', 'Ονοματεπώνυμο') }}</label>
                                <input v-model="fullName" type="text" :placeholder="t('Dr. First Last', 'Δρ. Όνομα Επώνυμο')" />
                            </div>
                            <div class="field">
                                <label>{{ t('Email', 'Email') }}</label>
                                <input v-model="email" type="email" :placeholder="t('Your email address', 'Η διεύθυνση email σας')" />
                            </div>
                            <div class="field">
                                <label>{{ t('Password', 'Κωδικός') }}</label>
                                <input v-model="password" type="password" :placeholder="t('At least 6 characters', 'Τουλάχιστον 6 χαρακτήρες')" />
                            </div>
                            <div class="field">
                                <label>{{ t('Confirm Password', 'Επιβεβαίωση Κωδικού') }}</label>
                                <input v-model="confirmPassword" type="password" :placeholder="t('Repeat password', 'Επαναλάβετε τον κωδικό')" />
                            </div>

                            <transition name="error-pop">
                                <p v-if="error" class="error">{{ error }}</p>
                            </transition>
                            <p class="gdpr-note">{{ t('Your account will be reviewed and approved by the DDART administrator before you can access the doctor panel.', 'Ο λογαριασμός σας θα αξιολογηθεί και εγκριθεί από τον διαχειριστή DDART πριν αποκτήσετε πρόσβαση.') }}</p>
                            <button class="submit-btn" @click="doctorSignup" :disabled="loading">
                                <span class="btn-text">{{ loading ? t('Registering...', 'Εγγραφή...') : t('Request Access', 'Αίτηση Πρόσβασης') }}</span>
                                <span v-if="loading" class="btn-spinner"></span>
                            </button>
                        </div>

                    </transition>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="footer-left"><img src="/democritus.png" class="dept-logo" /></div>
            <div class="footer-right">
                <p>{{ t('For technical support please call', 'Για τεχνική υποστήριξη καλέστε') }} +3025510 30990 ({{ t('office hours', 'ώρες γραφείου') }})</p>
                <p>email: <a href="mailto:ddart@med.duth.gr">ddart@med.duth.gr</a></p>
                <p class="made-by">Made by Andreas</p>
            </div>
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
            role: 'health-center',
            mode: 'login',
            centerName: '',
            fullName: '',
            email: '',
            password: '',
            confirmPassword: '',
            error: '',
            loading: false,
            isDark: localStorage.getItem('ddart_dark') === 'true',
            showOverlay: false,
            showStudyModal: false,
            studyCode: '',
            studyError: '',
            barWidth: 0,
            entryMessage: ''
        }
    },

    mounted() {
        if (localStorage.getItem('ddart_health_center')) this.$router.push('/health-center')
        if (localStorage.getItem('ddart_doctor')) {
            this.$router.push('/research')
        }
    },

    methods: {
        async studyLogin() {
            this.studyError = ''
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/stats?code=${encodeURIComponent(this.studyCode)}`)
                if (!res.ok) { this.studyError = 'Invalid access code.'; return }
                localStorage.setItem('ddart_study_code', this.studyCode)
                this.showStudyModal = false
                this.$router.push('/study')
            } catch { this.studyError = 'Connection failed.' }
        },

        toggleDark() {
            this.isDark = !this.isDark
            localStorage.setItem('ddart_dark', this.isDark)
        },

        showEntryAnimation(message, destination) {
            this.entryMessage = message
            this.showOverlay = true
            this.barWidth = 0
            const start = performance.now()
            const duration = 2500
            const animate = (now) => {
                const progress = Math.min((now - start) / duration, 1)
                this.barWidth = Math.round((1 - Math.pow(1 - progress, 3)) * 100)
                if (progress < 1) {
                    requestAnimationFrame(animate)
                } else {
                    setTimeout(() => this.$router.push(destination), 200)
                }
            }
            requestAnimationFrame(animate)
        },

        async healthCenterLogin() {
            this.error = ''
            if (!this.centerName || !this.password) { this.error = this.t('Please fill in all fields', 'Παρακαλώ συμπληρώστε όλα τα πεδία'); return }
            this.loading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/health-center/login', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: this.centerName, password: this.password })
                })
                const data = await res.json()
                if (!res.ok) { this.error = data.detail || this.t('Login failed', 'Αποτυχία σύνδεσης'); return }
                localStorage.setItem('ddart_health_center', JSON.stringify({ id: data.health_center_id, name: data.name }))
                this.loading = false
                this.showEntryAnimation(
                    this.t('Welcome, ' + data.name, 'Καλώς ορίσατε, ' + data.name),
                    '/health-center'
                )
            } catch { this.error = this.t('Connection failed. Please try again.', 'Αποτυχία σύνδεσης. Δοκιμάστε ξανά.') }
            finally { this.loading = false }
        },

        async doctorLogin() {
            this.error = ''
            if (!this.email || !this.password) { this.error = this.t('Please fill in all fields', 'Παρακαλώ συμπληρώστε όλα τα πεδία'); return }
            this.loading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/login', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: this.email, password: this.password })
                })
                const data = await res.json()
                if (!res.ok) { this.error = data.detail || this.t('Login failed', 'Αποτυχία σύνδεσης'); return }
                localStorage.setItem('ddart_doctor', JSON.stringify({ id: data.doctor_id, name: data.full_name, is_research: true }))
                this.loading = false
                this.showEntryAnimation(
                    this.t('Welcome, Dr. ' + data.full_name, 'Καλώς ορίσατε, Δρ. ' + data.full_name),
                    '/research'
                )
            } catch { this.error = this.t('Connection failed. Please try again.', 'Αποτυχία σύνδεσης. Δοκιμάστε ξανά.') }
            finally { this.loading = false }
        },

        async doctorSignup() {
            this.error = ''
            if (!this.fullName || !this.email || !this.password || !this.confirmPassword) { this.error = this.t('Please fill in all fields', 'Παρακαλώ συμπληρώστε όλα τα πεδία'); return }
            if (this.password !== this.confirmPassword) { this.error = this.t('Passwords do not match', 'Οι κωδικοί δεν ταιριάζουν'); return }
            if (this.password.length < 6) { this.error = this.t('Password must be at least 6 characters', 'Ο κωδικός πρέπει να έχει τουλάχιστον 6 χαρακτήρες'); return }
            this.loading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/signup', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name: this.fullName, email: this.email, password: this.password, is_research: this.isResearch })
                })
                const data = await res.json()
                if (!res.ok) { this.error = data.detail || this.t('Registration failed', 'Αποτυχία εγγραφής'); return }
                alert(this.t('Account created! You can now sign in.', 'Ο λογαριασμός δημιουργήθηκε! Μπορείτε τώρα να συνδεθείτε.'))
                this.mode = 'login'
            } catch { this.error = this.t('Connection failed. Please try again.', 'Αποτυχία σύνδεσης. Δοκιμάστε ξανά.') }
            finally { this.loading = false }
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; min-height: 100%; background: #f0f4f8; font-family: 'Source Sans 3', sans-serif; overflow-x: hidden; }

.login-container { display: flex; flex-direction: column; align-items: center; padding: 30px 20px 0; min-height: 100vh; width: 100%; background: #f0f4f8; transition: background 0.4s cubic-bezier(0.4, 0, 0.2, 1); }

.entry-overlay { position: fixed; inset: 0; z-index: 9999; background: radial-gradient(ellipse at center, #0d1f3c 0%, #060d1a 100%); display: flex; align-items: center; justify-content: center; }
.entry-content { display: flex; flex-direction: column; align-items: center; gap: 20px; }

/* Retinal scanner */
.retinal-scanner { position: relative; width: 200px; height: 200px; animation: scanner-appear 0.5s ease both; }
@keyframes scanner-appear { from { opacity: 0; transform: scale(0.85); } to { opacity: 1; transform: scale(1); } }
.retina-svg { width: 100%; height: 100%; }

/* Outer ring draw animation */
.ring-draw { animation: ring-draw 1.8s 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
@keyframes ring-draw { from { stroke-dashoffset: 565; } to { stroke-dashoffset: 0; } }
.ring-draw-2 { animation: ring-draw-2 1.4s 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
@keyframes ring-draw-2 { from { stroke-dashoffset: 415; } to { stroke-dashoffset: 0; } }

/* Crosshairs fade in */
.crosshair { opacity: 0; animation: fade-in 0.4s 1s ease forwards; }
@keyframes fade-in { to { opacity: 1; } }

/* Vessels draw in */
.vessel { stroke-dasharray: 200; stroke-dashoffset: 200; animation: vessel-draw 1s 0.8s ease forwards; }
@keyframes vessel-draw { to { stroke-dashoffset: 0; } }

/* Corner brackets */
.bracket { opacity: 0; animation: fade-in 0.5s 0.2s ease forwards; }

/* Scanner beam rotating */
.scanner-beam { transform-origin: 100px 100px; animation: scan-rotate 2s linear infinite; }
@keyframes scan-rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* Horizontal scan line sweeping */
.scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent 0%, rgba(99,179,237,0.0) 20%, rgba(99,179,237,0.6) 50%, rgba(99,179,237,0.0) 80%, transparent 100%); animation: scan-sweep 2s ease-in-out infinite; border-radius: 1px; }
@keyframes scan-sweep { 0% { top: 10%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 90%; opacity: 0; } }

/* Glint dots */
.glint { position: absolute; width: 4px; height: 4px; background: #63b3ed; border-radius: 50%; animation: glint-pulse 2s ease-in-out infinite; box-shadow: 0 0 6px #63b3ed; }
.glint-1 { top: 6px; left: 50%; animation-delay: 0s; }
.glint-2 { top: 50%; right: 6px; animation-delay: 0.66s; }
.glint-3 { bottom: 6px; left: 50%; animation-delay: 1.33s; }
@keyframes glint-pulse { 0%, 100% { opacity: 0.3; transform: scale(1); } 50% { opacity: 1; transform: scale(1.5); } }

/* Logo & bar */
.entry-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 22px; font-weight: 700; color: white; letter-spacing: 4px; display: flex; align-items: baseline; gap: 2px; animation: logo-appear 0.6s 0.4s cubic-bezier(0.4, 0, 0.2, 1) both; }
.entry-ddart { color: white; }
.entry-ai { color: #e53e3e; font-size: 72px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; }
.entry-bar { width: 200px; height: 2px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; }
.entry-bar-fill { height: 100%; background: linear-gradient(90deg, #4299e1, #63b3ed); border-radius: 2px; transition: width 0.05s linear; }
.entry-msg { color: rgba(255,255,255,0.55); font-size: 13px; font-weight: 400; letter-spacing: 1px; text-transform: uppercase; margin: 0; animation: msg-appear 0.5s 0.6s cubic-bezier(0.4, 0, 0.2, 1) both; }
@keyframes logo-appear { from { opacity: 0; transform: scale(0.92) translateY(8px); } to { opacity: 1; transform: scale(1) translateY(0); } }
@keyframes msg-appear { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.overlay-fade-leave-active { transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1), transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.overlay-fade-leave-to { opacity: 0; transform: scale(1.04); }

.header-controls { position: absolute; top: 20px; right: 20px; display: flex; align-items: center; gap: 12px; }
.lang-toggle { display: flex; align-items: center; gap: 4px; }
.lang-btn { background: none; border: none; font-family: 'Source Sans 3', sans-serif; font-size: 12px; font-weight: 700; color: #a0aec0; cursor: pointer; padding: 3px 6px; border-radius: 3px; transition: color 0.2s ease, background 0.2s ease; letter-spacing: 0.5px; }
.lang-btn.active { color: #2b6cb0; background: #ebf8ff; }
.lang-btn:hover:not(.active) { color: #4a5568; }
.lang-sep { color: #e2e8f0; font-size: 12px; }
.dark-btn { background: none; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 11px; font-weight: 700; color: #718096; cursor: pointer; padding: 3px 10px; transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease; letter-spacing: 0.4px; }
.dark-btn:hover { background: #edf2f7; }
.header { text-align: center; margin-bottom: 20px; width: 100%; position: relative; }
.header-text { transition: opacity 0.2s ease; }
.university { font-size: 14px; color: #2c5282; font-weight: 600; margin: 0 0 4px; transition: color 0.4s ease; }
.subtitle { font-size: 13px; color: #4a6fa5; margin: 0 0 16px; transition: color 0.4s ease; }
.logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 18px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; justify-content: center; gap: 2px; transition: color 0.4s ease; }
.logo span { color: #e53e3e; font-size: 48px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }

.role-toggle { display: flex; gap: 8px; margin-bottom: 20px; background: white; border: 1px solid #e2e8f0; border-radius: 6px; padding: 4px; width: 100%; max-width: 760px; transition: background 0.4s ease, border-color 0.4s ease; }
.role-btn { flex: 1; padding: 8px 16px; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; white-space: nowrap; transition: background 0.25s cubic-bezier(0.4, 0, 0.2, 1), color 0.25s ease, transform 0.15s ease; }
.role-btn.active { background: #2b6cb0; color: white; }
.role-btn:hover:not(.active) { background: #f0f4f8; }
.role-btn:active { transform: scale(0.98); }

.main-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; width: 100%; max-width: 760px; margin-bottom: 24px; box-shadow: 0 2px 16px rgba(0,0,0,0.07); transition: background 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease; overflow: hidden; }
.card-inner { display: grid; grid-template-columns: 260px 1fr; min-height: 360px; }
.left-panel { background: #2b6cb0; display: flex; align-items: center; padding: 32px 28px; overflow: hidden; transition: background 0.4s ease; }
.left-content h2 { font-family: 'Playfair Display', serif; color: white; font-size: 20px; margin: 0 0 10px; }
.left-content p { color: rgba(255,255,255,0.85); font-size: 13px; line-height: 1.7; margin: 0 0 14px; }
.left-content ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
.left-content li { color: rgba(255,255,255,0.9); font-size: 13px; }
.right-panel { padding: 24px 28px; display: flex; flex-direction: column; gap: 14px; overflow: hidden; }

.tabs { display: flex; border-bottom: 2px solid #e2e8f0; gap: 4px; transition: border-color 0.4s ease; }
.tab { padding: 8px 20px; border: none; background: none; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; color: #718096; cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: color 0.2s ease, border-bottom-color 0.2s ease; }
.tab.active { color: #2b6cb0; border-bottom-color: #2b6cb0; }

.form { display: flex; flex-direction: column; gap: 12px; }
.field { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 12px; font-weight: 600; color: #4a5568; text-transform: uppercase; letter-spacing: 0.4px; transition: color 0.4s ease; }
.field input { padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; color: #2d3748; outline: none; width: 100%; background: white; transition: border-color 0.2s ease, background 0.4s ease, color 0.4s ease, box-shadow 0.2s ease; }
.field input:focus { border-color: #2b6cb0; box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.12); }
.hint { font-size: 11px; color: #a0aec0; transition: color 0.4s ease; }
.gdpr-note { font-size: 11px; color: #718096; line-height: 1.6; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px 10px; margin: 0; transition: background 0.4s ease, border-color 0.4s ease, color 0.4s ease; }
.access-note { font-size: 11px; color: #718096; line-height: 1.6; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px 10px; margin: 0; transition: background 0.4s ease, border-color 0.4s ease, color 0.4s ease; }

.research-check { display: flex; align-items: flex-start; gap: 10px; padding: 12px; border: 1.5px solid #e2e8f0; border-radius: 6px; cursor: pointer; background: white; transition: border-color 0.25s ease, background 0.25s ease, box-shadow 0.25s ease; }
.research-check:hover { box-shadow: 0 2px 8px rgba(43, 108, 176, 0.1); }
.research-check.checked { border-color: #2b6cb0; background: #ebf8ff; }
.check-box { width: 20px; height: 20px; min-width: 20px; border: 2px solid #e2e8f0; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: white; background: white; margin-top: 1px; transition: background 0.2s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s ease, transform 0.15s ease; }
.research-check.checked .check-box { background: #2b6cb0; border-color: #2b6cb0; transform: scale(1.05); }
.check-text { display: flex; flex-direction: column; gap: 2px; }
.check-title { font-size: 13px; font-weight: 700; color: #2d3748; transition: color 0.4s ease; }
.check-desc { font-size: 11px; color: #718096; transition: color 0.4s ease; }

.submit-btn { padding: 11px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 4px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease; }
.submit-btn:hover:not(:disabled) { background: #2c5282; box-shadow: 0 4px 12px rgba(43, 108, 176, 0.3); transform: translateY(-1px); }
.submit-btn:active:not(:disabled) { transform: translateY(0); box-shadow: none; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.35); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }
@keyframes spin { to { transform: rotate(360deg); } }
.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0; }

.footer { width: 100%; max-width: 760px; display: flex; justify-content: space-between; align-items: center; padding: 16px 0 24px; border-top: 1px solid #e2e8f0; margin-top: auto; gap: 16px; transition: border-color 0.4s ease; }
.dept-logo { height: 50px; width: auto; object-fit: contain; }
.footer-right { text-align: right; }
.footer-right p { font-size: 12px; color: #718096; margin: 2px 0; transition: color 0.4s ease; }
.footer-right a { color: #2b6cb0; text-decoration: none; transition: color 0.4s ease; }
.made-by { font-size: 10px; color: #cbd5e0; margin-top: 4px; }

.panel-slide-enter-active { transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1), transform 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
.panel-slide-leave-active { transition: opacity 0.2s cubic-bezier(0.4, 0, 1, 1), transform 0.2s cubic-bezier(0.4, 0, 1, 1); }
.panel-slide-enter-from { opacity: 0; transform: translateY(12px); }
.panel-slide-leave-to   { opacity: 0; transform: translateY(-8px); }
.form-slide-enter-active { transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.form-slide-leave-active { transition: opacity 0.18s cubic-bezier(0.4, 0, 1, 1), transform 0.18s cubic-bezier(0.4, 0, 1, 1); }
.form-slide-enter-from { opacity: 0; transform: translateX(10px); }
.form-slide-leave-to   { opacity: 0; transform: translateX(-10px); }
.header-fade-enter-active { transition: opacity 0.25s ease; }
.header-fade-leave-active { transition: opacity 0.15s ease; }
.header-fade-enter-from, .header-fade-leave-to { opacity: 0; }
.error-pop-enter-active { transition: opacity 0.25s ease, transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); }
.error-pop-leave-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.error-pop-enter-from { opacity: 0; transform: translateY(-4px) scale(0.97); }
.error-pop-leave-to   { opacity: 0; transform: translateY(-2px); }

.dark.login-container { background: #1a202c; }
.dark .university { color: #90cdf4; }
.dark .subtitle { color: #7fb3d3; }
.dark .logo { color: #90cdf4; }
.dark .role-toggle { background: #2d3748; border-color: #4a5568; }
.dark .role-btn { color: #a0aec0; }
.dark .role-btn:hover:not(.active) { background: #3d4a5c; }
.dark .main-card { background: #2d3748; border-color: #4a5568; box-shadow: 0 2px 16px rgba(0,0,0,0.3); }
.dark .right-panel { background: #2d3748; }
.dark .tabs { border-bottom-color: #4a5568; }
.dark .tab { color: #a0aec0; }
.dark .tab.active { color: #63b3ed; border-bottom-color: #63b3ed; }
.dark .field label { color: #a0aec0; }
.dark .field input { background: #1a202c; border-color: #4a5568; color: #e2e8f0; }
.dark .field input:focus { border-color: #63b3ed; box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.15); }
.dark .field input::placeholder { color: #4a5568; }
.dark .hint { color: #718096; }
.dark .gdpr-note, .dark .access-note { background: #1a202c; border-color: #4a5568; color: #a0aec0; }
.dark .research-check { background: #1a202c; border-color: #4a5568; }
.dark .research-check:hover { box-shadow: 0 2px 8px rgba(99, 179, 237, 0.12); }
.dark .research-check.checked { background: #1a365d; border-color: #63b3ed; }
.dark .check-box { background: #1a202c; border-color: #4a5568; }
.dark .research-check.checked .check-box { background: #2b6cb0; border-color: #63b3ed; }
.dark .check-title { color: #e2e8f0; }
.dark .check-desc { color: #718096; }
.dark .lang-btn.active { color: #63b3ed; background: #1a365d; }
.dark .lang-btn:hover:not(.active) { color: #e2e8f0; }
.dark .lang-sep { color: #4a5568; }
.dark .dark-btn { border-color: #4a5568; color: #a0aec0; }
.dark .dark-btn:hover { background: #3d4a5c; }
.dark .submit-btn:hover:not(:disabled) { box-shadow: 0 4px 12px rgba(99, 179, 237, 0.25); }
.dark .footer { border-top-color: #4a5568; }
.dark .footer-right p { color: #718096; }
.dark .footer-right a { color: #63b3ed; }

.study-modal-backdrop { position: fixed; inset: 0; background: rgba(10,20,40,0.85); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.study-modal-box { background: white; border-radius: 12px; padding: 36px; width: 300px; display: flex; flex-direction: column; align-items: center; gap: 14px; animation: modal-appear 0.3s cubic-bezier(0.34,1.56,0.64,1) both; }
@keyframes modal-appear { from { opacity: 0; transform: scale(0.92) translateY(16px); } to { opacity: 1; transform: scale(1) translateY(0); } }
.modal-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 14px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; gap: 2px; }
.modal-logo span { color: #e53e3e; font-size: 30px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }
.study-modal-box h3 { font-family: 'Playfair Display', serif; color: #2d3748; font-size: 17px; margin: 0; }
.study-modal-box p { font-size: 13px; color: #718096; margin: 0; text-align: center; }
.study-modal-btns { display: flex; gap: 8px; width: 100%; }
.study-back-btn { flex: 1; padding: 10px; background: none; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; transition: all 0.2s; }
.study-back-btn:hover { background: #f8fafc; border-color: #cbd5e0; }
.submit-btn.study-submit { flex: 1; margin-top: 0; }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.dark .study-modal-box { background: #2d3748; }
.dark .study-modal-box h3 { color: #e2e8f0; }
.dark .study-modal-box p { color: #a0aec0; }
.dark .study-back-btn { border-color: #4a5568; color: #a0aec0; }
.dark .study-back-btn:hover { background: #3d4a5c; }

.study-official-btn { position: absolute; top: 0; left: 0; background: none; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 11px; font-weight: 700; color: #718096; cursor: pointer; padding: 4px 10px; letter-spacing: 0.3px; transition: all 0.2s ease; }
.study-official-btn:hover { color: #2b6cb0; border-color: #2b6cb0; background: #ebf8ff; }
.dark .study-modal-backdrop { position: fixed; inset: 0; background: rgba(10,20,40,0.85); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.study-modal-box { background: white; border-radius: 12px; padding: 36px; width: 300px; display: flex; flex-direction: column; align-items: center; gap: 14px; animation: modal-appear 0.3s cubic-bezier(0.34,1.56,0.64,1) both; }
@keyframes modal-appear { from { opacity: 0; transform: scale(0.92) translateY(16px); } to { opacity: 1; transform: scale(1) translateY(0); } }
.modal-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 14px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; gap: 2px; }
.modal-logo span { color: #e53e3e; font-size: 30px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }
.study-modal-box h3 { font-family: 'Playfair Display', serif; color: #2d3748; font-size: 17px; margin: 0; }
.study-modal-box p { font-size: 13px; color: #718096; margin: 0; text-align: center; }
.study-modal-btns { display: flex; gap: 8px; width: 100%; }
.study-back-btn { flex: 1; padding: 10px; background: none; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; transition: all 0.2s; }
.study-back-btn:hover { background: #f8fafc; border-color: #cbd5e0; }
.submit-btn.study-submit { flex: 1; margin-top: 0; }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.dark .study-modal-box { background: #2d3748; }
.dark .study-modal-box h3 { color: #e2e8f0; }
.dark .study-modal-box p { color: #a0aec0; }
.dark .study-back-btn { border-color: #4a5568; color: #a0aec0; }
.dark .study-back-btn:hover { background: #3d4a5c; }

.study-official-btn { color: #718096; border-color: #4a5568; }
.dark .study-official-btn:hover { color: #63b3ed; border-color: #63b3ed; background: #1a365d; }

@media (max-width: 768px) {
    .login-container { padding: 20px 16px 0; }
    .header-controls { top: 12px; right: 12px; }
    .university { font-size: 12px; }
    .logo span { font-size: 36px; }
    .role-toggle { max-width: 100%; }
    .role-btn { font-size: 12px; padding: 8px 10px; }
    .card-inner { grid-template-columns: 1fr; min-height: unset; }
    .left-panel { padding: 20px; align-items: flex-start; }
    .left-content h2 { font-size: 18px; }
    .left-content p { font-size: 12px; margin-bottom: 10px; }
    .left-content li { font-size: 12px; }
    .right-panel { padding: 20px; }
    .footer { flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .footer-right { text-align: center; }
    .dept-logo { height: 40px; }
    .entry-ai { font-size: 56px; }
}
@media (max-width: 480px) {
    .login-container { padding: 16px 12px 0; }
    .university { font-size: 11px; }
    .logo span { font-size: 30px; }
    .tab { padding: 8px 12px; font-size: 13px; }
    .right-panel { padding: 16px; }
    .header-controls { gap: 8px; }
    .entry-bar { width: 200px; }
    .entry-ai { font-size: 48px; }
}
</style>