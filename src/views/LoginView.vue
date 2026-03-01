<template>
    <div class="login-container" :class="{ dark: isDark }">

        <transition name="overlay-fade">
            <div v-if="showOverlay" class="entry-overlay">
                <div class="entry-content">
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
            <button class="study-official-btn" @click="$router.push('/study')">Study Official</button>
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
                            <label class="research-check" :class="{ checked: loginAsResearch }" @click="loginAsResearch = !loginAsResearch">
                                <div class="check-box"><span v-if="loginAsResearch">✓</span></div>
                                <div class="check-text">
                                    <span class="check-title">{{ t('Sign in as Research Team', 'Σύνδεση ως Ερευνητική Ομάδα') }}</span>
                                    <span class="check-desc">{{ t('Access the AI agreement study panel', 'Πρόσβαση στη μελέτη συμφωνίας ΤΝ') }}</span>
                                </div>
                            </label>
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
                            <label class="research-check" :class="{ checked: isResearch }" @click="isResearch = !isResearch">
                                <div class="check-box"><span v-if="isResearch">✓</span></div>
                                <div class="check-text">
                                    <span class="check-title">{{ t('Part of Research Team', 'Μέλος Ερευνητικής Ομάδας') }}</span>
                                    <span class="check-desc">{{ t('I will be participating in the AI agreement study', 'Θα συμμετέχω στη μελέτη συμφωνίας ΤΝ') }}</span>
                                </div>
                            </label>
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
            isResearch: false,
            loginAsResearch: false,
            error: '',
            loading: false,
            isDark: localStorage.getItem('ddart_dark') === 'true',
            showOverlay: false,
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
        toggleDark() {
            this.isDark = !this.isDark
            localStorage.setItem('ddart_dark', this.isDark)
        },

        showEntryAnimation(message, destination) {
            this.entryMessage = message
            this.showOverlay = true
            this.barWidth = 0
            const start = performance.now()
            const duration = 1600
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

.entry-overlay { position: fixed; inset: 0; z-index: 9999; background: #1a2a4a; display: flex; align-items: center; justify-content: center; }
.entry-content { display: flex; flex-direction: column; align-items: center; gap: 28px; }
.entry-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 22px; font-weight: 700; color: white; letter-spacing: 4px; display: flex; align-items: baseline; gap: 2px; animation: logo-appear 0.6s cubic-bezier(0.4, 0, 0.2, 1) both; }
.entry-ddart { color: white; }
.entry-ai { color: #e53e3e; font-size: 72px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; }
.entry-bar { width: 260px; height: 3px; background: rgba(255,255,255,0.15); border-radius: 2px; overflow: hidden; }
.entry-bar-fill { height: 100%; background: linear-gradient(90deg, #4299e1, #63b3ed); border-radius: 2px; transition: width 0.05s linear; }
.entry-msg { color: rgba(255,255,255,0.7); font-size: 14px; font-weight: 400; letter-spacing: 0.3px; margin: 0; animation: msg-appear 0.5s 0.3s cubic-bezier(0.4, 0, 0.2, 1) both; }
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

.study-official-btn { position: absolute; top: 0; left: 0; background: none; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 11px; font-weight: 700; color: #718096; cursor: pointer; padding: 4px 10px; letter-spacing: 0.3px; transition: all 0.2s ease; }
.study-official-btn:hover { color: #2b6cb0; border-color: #2b6cb0; background: #ebf8ff; }
.dark .study-official-btn { color: #718096; border-color: #4a5568; }
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