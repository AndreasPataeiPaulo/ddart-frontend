<template>
    <div class="login-container">
        <div class="header">
            <p class="university">Democritus University of Thrace – DDART spin-off company</p>
            <p class="subtitle">Ophthalmology A.I. Screening Program</p>
            <div class="logo">DDART<span>AI</span></div>
        </div>

        <div class="role-toggle">
            <button :class="['role-btn', { active: role === 'patient' }]" @click="role = 'patient'; error = ''">👤
                Patient</button>
            <button :class="['role-btn', { active: role === 'doctor' }]" @click="role = 'doctor'; error = ''">🩺 Doctor
                / Staff</button>
        </div>

        <div class="main-card">
            <div class="card-inner">
                <div class="left-panel">
                    <transition name="fade" mode="out-in">
                        <div v-if="role === 'patient'" key="patient-info" class="left-content">
                            <h2>Patient Portal</h2>
                            <p>Sign in or create an account to access the DDART-AI screening system and view your
                                screening history.</p>
                            <ul>
                                <li>🔒 Your data is stored securely</li>
                                <li>👁 View last 5 screening results</li>
                                <li>📋 AMKA verification required</li>
                            </ul>
                        </div>
                        <div v-else key="doctor-info" class="left-content">
                            <h2>Doctor Portal</h2>
                            <p>Access the clinical dashboard to view patient screenings, statistics, and export data for
                                research.</p>
                            <ul>
                                <li>👥 View all patient records</li>
                                <li>📊 Aggregate statistics</li>
                                <li>📥 Export to CSV</li>
                                <li>🔬 Research study participation</li>
                                <li>✅ Access approved by administrator</li>
                            </ul>
                        </div>
                    </transition>
                </div>

                <div class="right-panel">
                    <div class="tabs">
                        <button :class="['tab', { active: mode === 'login' }]" @click="mode = 'login'; error = ''">Sign
                            In</button>
                        <button :class="['tab', { active: mode === 'signup' }]"
                            @click="mode = 'signup'; error = ''">Apply For Account</button>
                    </div>

                    <transition name="fade-slide" mode="out-in">

                        <!-- PATIENT LOGIN -->
                        <div v-if="role === 'patient' && mode === 'login'" key="p-login" class="form">
                            <div class="field">
                                <label>AMKA</label>
                                <input v-model="amka" type="text" maxlength="11" placeholder="11-digit AMKA number" />
                            </div>
                            <div class="field">
                                <label>Password</label>
                                <input v-model="password" type="password" placeholder="Your password"
                                    @keyup.enter="login" />
                            </div>
                            <p v-if="error" class="error">{{ error }}</p>
                            <button class="submit-btn" @click="login" :disabled="loading">{{ loading ? 'Signing in...' :
                                'Sign In' }}</button>
                        </div>

                        <!-- PATIENT SIGNUP -->
                        <div v-else-if="role === 'patient' && mode === 'signup'" key="p-signup" class="form">
                            <div class="field">
                                <label>Full Name</label>
                                <input v-model="fullName" type="text" placeholder="As it appears on your ID" />
                            </div>
                            <div class="field">
                                <label>AMKA</label>
                                <input v-model="amka" type="text" maxlength="11" placeholder="11-digit AMKA number" />
                                <span class="hint">Your Greek social security number</span>
                            </div>
                            <div class="field">
                                <label>Password</label>
                                <input v-model="password" type="password" placeholder="At least 6 characters" />
                            </div>
                            <div class="field">
                                <label>Confirm Password</label>
                                <input v-model="confirmPassword" type="password" placeholder="Repeat password" />
                            </div>
                            <p v-if="error" class="error">{{ error }}</p>
                            <p class="gdpr-note">By registering, you consent to the storage of your personal data for
                                ophthalmology screening research at Democritus University of Thrace, in accordance with
                                GDPR.</p>
                            <button class="submit-btn" @click="signup" :disabled="loading">{{ loading ? 'Registering...'
                                : 'Create Account' }}</button>
                        </div>

                        <!-- DOCTOR LOGIN -->
                        <div v-else-if="role === 'doctor' && mode === 'login'" key="d-login" class="form">
                            <div class="field">
                                <label>Email</label>
                                <input v-model="email" type="email" placeholder="Your email address" />
                            </div>
                            <div class="field">
                                <label>Password</label>
                                <input v-model="password" type="password" placeholder="Your password"
                                    @keyup.enter="doctorLogin" />
                            </div>
                            <label class="research-check" :class="{ checked: loginAsResearch }"
                                @click="loginAsResearch = !loginAsResearch">
                                <div class="check-box"><span v-if="loginAsResearch">✓</span></div>
                                <div class="check-text">
                                    <span class="check-title">🔬 Sign in as Research Team</span>
                                    <span class="check-desc">Access the AI agreement study panel</span>
                                </div>
                            </label>
                            <p v-if="error" class="error">{{ error }}</p>
                            <button class="submit-btn" @click="doctorLogin" :disabled="loading">{{ loading ? 'Signing in...' : 'Sign In' }}</button>
                        </div>

                        <!-- DOCTOR SIGNUP -->
                        <div v-else-if="role === 'doctor' && mode === 'signup'" key="d-signup" class="form">
                            <div class="field">
                                <label>Full Name</label>
                                <input v-model="fullName" type="text" placeholder="Dr. First Last" />
                            </div>
                            <div class="field">
                                <label>Email</label>
                                <input v-model="email" type="email" placeholder="Your email address" />
                            </div>
                            <div class="field">
                                <label>Password</label>
                                <input v-model="password" type="password" placeholder="At least 6 characters" />
                            </div>
                            <div class="field">
                                <label>Confirm Password</label>
                                <input v-model="confirmPassword" type="password" placeholder="Repeat password" />
                            </div>
                            <label class="research-check" :class="{ checked: isResearch }"
                                @click="isResearch = !isResearch">
                                <div class="check-box"><span v-if="isResearch">✓</span></div>
                                <div class="check-text">
                                    <span class="check-title">🔬 Part of Research Team</span>
                                    <span class="check-desc">I will be participating in the AI agreement study</span>
                                </div>
                            </label>
                            <p v-if="error" class="error">{{ error }}</p>
                            <p class="gdpr-note">Your account will be reviewed and approved by the DDART administrator
                                before you can access the doctor panel.</p>
                            <button class="submit-btn" @click="doctorSignup" :disabled="loading">{{ loading ?
                                'Registering...' : 'Request Access' }}</button>
                        </div>

                    </transition>
                </div>
            </div>
        </div>

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
            role: 'patient',
            mode: 'login',
            fullName: '',
            amka: '',
            email: '',
            password: '',
            confirmPassword: '',
            isResearch: false,
            loginAsResearch: false,
            error: '',
            loading: false
        }
    },

    mounted() {
        if (localStorage.getItem('ddart_patient')) this.$router.push('/')
        if (localStorage.getItem('ddart_doctor')) {
            const d = JSON.parse(localStorage.getItem('ddart_doctor'))
            this.$router.push(d.is_research ? '/research' : '/doctor')
        }
    },

    methods: {
        async login() {
            this.error = ''
            if (!this.amka || !this.password) { this.error = 'Please fill in all fields'; return }
            this.loading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/auth/login', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ amka: this.amka, password: this.password })
                })
                const data = await res.json()
                if (!res.ok) { this.error = data.detail || 'Login failed'; return }
                localStorage.setItem('ddart_patient', JSON.stringify({ id: data.patient_id, name: data.full_name }))
                this.$router.push('/')
            } catch { this.error = 'Connection failed. Please try again.' }
            finally { this.loading = false }
        },

        async signup() {
            this.error = ''
            if (!this.fullName || !this.amka || !this.password || !this.confirmPassword) { this.error = 'Please fill in all fields'; return }
            if (this.password !== this.confirmPassword) { this.error = 'Passwords do not match'; return }
            if (this.amka.length !== 11 || !/^\d+$/.test(this.amka)) { this.error = 'AMKA must be exactly 11 digits'; return }
            if (this.password.length < 6) { this.error = 'Password must be at least 6 characters'; return }
            this.loading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/auth/signup', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name: this.fullName, amka: this.amka, password: this.password })
                })
                const data = await res.json()
                if (!res.ok) { this.error = data.detail || 'Registration failed'; return }
                localStorage.setItem('ddart_patient', JSON.stringify({ id: data.patient_id, name: data.full_name }))
                this.$router.push('/')
            } catch { this.error = 'Connection failed. Please try again.' }
            finally { this.loading = false }
        },

        async doctorLogin() {
            this.error = ''
            if (!this.email || !this.password) { this.error = 'Please fill in all fields'; return }
            this.loading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/login', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: this.email, password: this.password })
                })
                const data = await res.json()
                if (!res.ok) { this.error = data.detail || 'Login failed'; return }
                const isResearch = this.loginAsResearch || data.is_research
                localStorage.setItem('ddart_doctor', JSON.stringify({ id: data.doctor_id, name: data.full_name, is_research: isResearch }))
                this.$router.push(isResearch ? '/research' : '/doctor')
            } catch { this.error = 'Connection failed. Please try again.' }
            finally { this.loading = false }
        },

        async doctorSignup() {
            this.error = ''
            if (!this.fullName || !this.email || !this.password || !this.confirmPassword) { this.error = 'Please fill in all fields'; return }
            if (this.password !== this.confirmPassword) { this.error = 'Passwords do not match'; return }
            if (this.password.length < 6) { this.error = 'Password must be at least 6 characters'; return }
            this.loading = true
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/signup', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name: this.fullName, email: this.email, password: this.password, is_research: this.isResearch })
                })
                const data = await res.json()
                if (!res.ok) { this.error = data.detail || 'Registration failed'; return }
                alert('Account created! Your access is pending approval by the administrator.')
                this.mode = 'login'
            } catch { this.error = 'Connection failed. Please try again.' }
            finally { this.loading = false }
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

.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 20px 0;
    min-height: 100vh;
}

.header {
    text-align: center;
    margin-bottom: 20px;
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

.role-toggle {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 4px;
}

.role-btn {
    flex: 1;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #718096;
    cursor: pointer;
    transition: all 0.2s;
    background: none;
}

.role-btn.active {
    background: #2b6cb0;
    color: white;
}

.role-btn:hover:not(.active) {
    background: #f8fafc;
}

.main-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    width: 100%;
    max-width: 760px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.card-inner {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 360px;
}

.left-panel {
    background: #2b6cb0;
    border-radius: 4px 0 0 4px;
    display: flex;
    align-items: center;
    padding: 32px 28px;
    overflow: hidden;
}

.left-content h2 {
    font-family: 'Playfair Display', serif;
    color: white;
    font-size: 22px;
    margin: 0 0 12px;
}

.left-content p {
    color: rgba(255, 255, 255, 0.85);
    font-size: 13.5px;
    line-height: 1.7;
    margin: 0 0 16px;
}

.left-content ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.left-content li {
    color: rgba(255, 255, 255, 0.9);
    font-size: 13px;
}

.right-panel {
    padding: 28px 32px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow: hidden;
}

.tabs {
    display: flex;
    border-bottom: 2px solid #e2e8f0;
    gap: 4px;
}

.tab {
    padding: 8px 20px;
    border: none;
    background: none;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #718096;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
}

.tab.active {
    color: #2b6cb0;
    border-bottom-color: #2b6cb0;
}

.form {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.field label {
    font-size: 12px;
    font-weight: 600;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.field input {
    padding: 9px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    color: #2d3748;
    transition: border-color 0.2s;
    outline: none;
}

.field input:focus {
    border-color: #2b6cb0;
}

.hint {
    font-size: 11px;
    color: #a0aec0;
}

.gdpr-note {
    font-size: 11px;
    color: #718096;
    line-height: 1.6;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 8px 10px;
    margin: 0;
}

.research-check {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 12px;
    border: 1.5px solid #e2e8f0;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
    background: white;
}

.research-check.checked {
    border-color: #2b6cb0;
    background: #ebf8ff;
}

.check-box {
    width: 20px;
    height: 20px;
    border: 2px solid #e2e8f0;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 13px;
    font-weight: 700;
    color: white;
    background: white;
    transition: all 0.2s;
    margin-top: 1px;
}

.research-check.checked .check-box {
    background: #2b6cb0;
    border-color: #2b6cb0;
}

.check-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.check-title {
    font-size: 13px;
    font-weight: 700;
    color: #2d3748;
}

.check-desc {
    font-size: 11px;
    color: #718096;
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
    margin-top: 4px;
}

.submit-btn:hover:not(:disabled) {
    background: #2c5282;
}

.submit-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.error {
    color: #c53030;
    font-size: 13px;
    font-weight: 600;
    margin: 0;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.fade-slide-enter-active {
    transition: all 0.25s ease;
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
    transform: translateY(-10px);
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