<template>
    <div class="login-container" :class="{ dark: isDark }">

        <!-- Welcome animation -->
        <transition name="welcome-fade">
            <div v-if="showWelcome" class="welcome-overlay" @click="showWelcome = false">
                <div class="welcome-particles" ref="wParticles"></div>
                <div class="welcome-content">
                    <div class="welcome-eye-wrap">
                        <svg class="welcome-eye-svg" viewBox="0 0 260 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <radialGradient id="wIrisGrad" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="rgba(99,179,237,0.3)"/>
                                    <stop offset="100%" stop-color="rgba(43,108,176,0.05)"/>
                                </radialGradient>
                            </defs>
                            <path d="M10 60 Q65 5 130 5 Q195 5 250 60 Q195 115 130 115 Q65 115 10 60 Z"
                                stroke="rgba(99,179,237,0.5)" stroke-width="1.2" fill="rgba(99,179,237,0.03)"
                                class="w-eye-outline"/>
                            <circle cx="130" cy="60" r="36" fill="url(#wIrisGrad)"
                                stroke="rgba(99,179,237,0.7)" stroke-width="1.5" class="w-iris"/>
                            <circle cx="130" cy="60" r="22" fill="rgba(43,108,176,0.12)"
                                stroke="rgba(99,179,237,0.9)" stroke-width="1.2" class="w-pupil-ring"/>
                            <circle cx="130" cy="60" r="10" fill="rgba(99,179,237,0.2)"
                                stroke="rgba(99,179,237,1)" stroke-width="1" class="w-inner-pupil"/>
                            <circle cx="130" cy="60" r="4" fill="#63b3ed" class="w-pupil-core"/>
                            <circle cx="137" cy="53" r="2.5" fill="rgba(255,255,255,0.6)" class="w-highlight"/>
                            <line x1="130" y1="5" x2="130" y2="0" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="w-ray"/>
                            <line x1="130" y1="115" x2="130" y2="120" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="w-ray"/>
                            <line x1="10" y1="60" x2="4" y2="60" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="w-ray"/>
                            <line x1="250" y1="60" x2="256" y2="60" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="w-ray"/>
                            <line x1="40" y1="22" x2="34" y2="16" stroke="rgba(99,179,237,0.3)" stroke-width="0.8" class="w-ray"/>
                            <line x1="220" y1="22" x2="226" y2="16" stroke="rgba(99,179,237,0.3)" stroke-width="0.8" class="w-ray"/>
                        </svg>
                        <div class="w-scan-line"></div>
                        <div class="w-scan-data w-sd1">OD: 0.42</div>
                        <div class="w-scan-data w-sd2">MAC: 0.18</div>
                        <div class="w-scan-data w-sd3">AI ✓</div>
                    </div>
                    <p class="w-label">Welcome to</p>
                    <div class="w-logo-row">
                        <span class="wl wl-1">D</span>
                        <span class="wl wl-2">D</span>
                        <span class="wl wl-3">A</span>
                        <span class="wl wl-4">R</span>
                        <span class="wl wl-5">T</span>
                        <span class="wl-ai">AI</span>
                    </div>
                    <p class="w-tagline">Ophthalmology · Artificial Intelligence · Screening</p>
                    <div class="w-bar-wrap"><div class="w-bar-fill"></div></div>
                </div>
            </div>
        </transition>

        <!-- Existing entry overlay -->
        <transition name="overlay-fade">
            <div v-if="showOverlay" class="entry-overlay">
                
                <!-- Particle field -->
                <div class="particle-field">
                    <div v-for="i in 24" :key="i" class="particle" :style="particleStyle(i)"></div>
                </div>
                <!-- Grid lines -->
                <div class="grid-lines">
                    <div v-for="i in 8" :key="'h'+i" class="grid-h" :style="{ top: (i*12)+'%' }"></div>
                    <div v-for="i in 8" :key="'v'+i" class="grid-v" :style="{ left: (i*12)+'%' }"></div>
                </div>

                <div class="entry-content">
                    <!-- Main retinal scanner — larger -->
                    <div class="retinal-scanner">
                        <svg class="retina-svg" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="rgba(66,153,225,0.25)"/>
                                    <stop offset="100%" stop-color="rgba(66,153,225,0)"/>
                                </radialGradient>
                                <radialGradient id="beamGrad2" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="rgba(99,179,237,0)"/>
                                    <stop offset="70%" stop-color="rgba(99,179,237,0.08)"/>
                                    <stop offset="100%" stop-color="rgba(99,179,237,0)"/>
                                </radialGradient>
                                <linearGradient id="ringGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#63b3ed"/>
                                    <stop offset="50%" stop-color="#4299e1"/>
                                    <stop offset="100%" stop-color="#2b6cb0"/>
                                </linearGradient>
                                <linearGradient id="ringGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stop-color="#e53e3e"/>
                                    <stop offset="100%" stop-color="#fc8181"/>
                                </linearGradient>
                                <filter id="glow">
                                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                                    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                                </filter>
                                <filter id="glow-strong">
                                    <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                                    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                                </filter>
                            </defs>

                            <!-- Background glow -->
                            <circle cx="150" cy="150" r="130" fill="url(#eyeGlow)"/>

                            <!-- Outer orbit rings -->
                            <circle cx="150" cy="150" r="138" stroke="rgba(99,179,237,0.06)" stroke-width="1"/>
                            <circle cx="150" cy="150" r="138" stroke="url(#ringGrad1)" stroke-width="1.5" stroke-dasharray="867" stroke-dashoffset="867" class="ring-draw"/>
                            <circle cx="150" cy="150" r="120" stroke="rgba(99,179,237,0.04)" stroke-width="1"/>
                            <circle cx="150" cy="150" r="120" stroke="rgba(99,179,237,0.35)" stroke-width="1" stroke-dasharray="754" stroke-dashoffset="754" class="ring-draw-2"/>
                            <circle cx="150" cy="150" r="98" stroke="rgba(99,179,237,0.08)" stroke-width="0.5" stroke-dasharray="4 6"/>
                            <circle cx="150" cy="150" r="75" stroke="rgba(99,179,237,0.06)" stroke-width="0.5" stroke-dasharray="3 5" class="ring-spin"/>
                            <circle cx="150" cy="150" r="55" stroke="rgba(99,179,237,0.08)" stroke-width="0.5"/>

                            <!-- Crosshairs -->
                            <line x1="150" y1="6" x2="150" y2="44" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <line x1="150" y1="256" x2="150" y2="294" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <line x1="6" y1="150" x2="44" y2="150" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <line x1="256" y1="150" x2="294" y2="150" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <!-- Diagonal crosshairs -->
                            <line x1="118" y1="18" x2="128" y2="32" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>
                            <line x1="182" y1="18" x2="172" y2="32" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>
                            <line x1="118" y1="282" x2="128" y2="268" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>
                            <line x1="182" y1="282" x2="172" y2="268" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>

                            <!-- Optic disc -->
                            <circle cx="178" cy="132" r="16" fill="rgba(66,153,225,0.08)" stroke="rgba(99,179,237,0.4)" stroke-width="1.5" filter="url(#glow)" class="disc-appear"/>
                            <circle cx="178" cy="132" r="8" fill="rgba(99,179,237,0.18)" stroke="rgba(99,179,237,0.6)" stroke-width="1" class="disc-appear"/>
                            <circle cx="178" cy="132" r="3" fill="rgba(99,179,237,0.8)" class="disc-appear" filter="url(#glow-strong)"/>

                            <!-- Blood vessels -->
                            <path d="M168 126 Q135 112 105 90" stroke="rgba(99,179,237,0.35)" stroke-width="1.8" fill="none" class="vessel" filter="url(#glow)"/>
                            <path d="M165 135 Q132 138 98 148" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M168 142 Q150 168 136 196" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M186 125 Q210 106 232 88" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M190 135 Q218 136 244 143" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M184 145 Q196 172 192 204" stroke="rgba(99,179,237,0.25)" stroke-width="1.2" fill="none" class="vessel"/>
                            <!-- Sub-vessels -->
                            <path d="M140 100 Q125 95 110 104" stroke="rgba(99,179,237,0.2)" stroke-width="1" fill="none" class="vessel-2"/>
                            <path d="M120 148 Q108 160 100 175" stroke="rgba(99,179,237,0.2)" stroke-width="1" fill="none" class="vessel-2"/>
                            <path d="M215 100 Q225 110 220 125" stroke="rgba(99,179,237,0.2)" stroke-width="1" fill="none" class="vessel-2"/>

                            <!-- Macula with fovea -->
                            <circle cx="124" cy="150" r="18" fill="none" stroke="url(#ringGrad2)" stroke-width="1.2" stroke-dasharray="5 4" class="macula-appear"/>
                            <circle cx="124" cy="150" r="10" fill="rgba(229,62,62,0.08)" stroke="rgba(229,62,62,0.4)" stroke-width="1" class="macula-appear"/>
                            <circle cx="124" cy="150" r="4" fill="rgba(229,62,62,0.6)" class="macula-appear" filter="url(#glow)"/>

                            <!-- Scanner beam -->
                            <path d="M150 150 L288 150 A138 138 0 0 1 150 288 Z" fill="url(#beamGrad2)" class="scanner-beam"/>

                            <!-- Corner brackets — larger -->
                            <path d="M20 58 L20 20 L58 20" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>
                            <path d="M242 20 L280 20 L280 58" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>
                            <path d="M20 242 L20 280 L58 280" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>
                            <path d="M242 280 L280 280 L280 242" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>

                            <!-- Tick marks around outer ring -->
                            <line x1="150" y1="12" x2="150" y2="20" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="150" y1="280" x2="150" y2="288" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="12" y1="150" x2="20" y2="150" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="280" y1="150" x2="288" y2="150" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="52" y1="35" x2="57" y2="43" stroke="rgba(99,179,237,0.3)" stroke-width="0.8" class="tick"/>
                            <line x1="248" y1="35" x2="243" y2="43" stroke="rgba(99,179,237,0.3)" stroke-width="0.8" class="tick"/>
                            <line x1="35" y1="248" x2="43" y2="243" stroke="rgba(99,179,237,0.3)" stroke-width="0.8" class="tick"/>
                            <line x1="265" y1="248" x2="257" y2="243" stroke="rgba(99,179,237,0.3)" stroke-width="0.8" class="tick"/>

                            <!-- Data readout lines -->
                            <line x1="196" y1="116" x2="226" y2="96" stroke="rgba(99,179,237,0.4)" stroke-width="0.8" class="readout-line"/>
                            <line x1="226" y1="96" x2="256" y2="96" stroke="rgba(99,179,237,0.4)" stroke-width="0.8" class="readout-line"/>
                            <line x1="106" y1="132" x2="76" y2="112" stroke="rgba(229,62,62,0.4)" stroke-width="0.8" class="readout-line"/>
                            <line x1="76" y1="112" x2="46" y2="112" stroke="rgba(229,62,62,0.4)" stroke-width="0.8" class="readout-line"/>
                        </svg>

                        <!-- Scan line -->
                        <div class="scan-line"></div>
                        <!-- Glints -->
                        <div class="glint glint-1"></div>
                        <div class="glint glint-2"></div>
                        <div class="glint glint-3"></div>
                        <div class="glint glint-4"></div>
                        <!-- Data readout labels -->
                        <div class="readout readout-1">OD: 0.42</div>
                        <div class="readout readout-2">MAC: 0.18</div>
                        <div class="readout readout-3">AI ✓</div>
                    </div>

                    <!-- DDART title -->
                    <div class="entry-logo">
                        <span class="entry-d entry-letter">D</span>
                        <span class="entry-d2 entry-letter">D</span>
                        <span class="entry-a entry-letter">A</span>
                        <span class="entry-r entry-letter">R</span>
                        <span class="entry-t entry-letter">T</span>
                        <span class="entry-ai">AI</span>
                    </div>
                    <div class="entry-tagline">Ophthalmology · Artificial Intelligence · Screening</div>

                    <!-- Progress bar -->
                    <div class="entry-bar">
                        <div class="entry-bar-fill" :style="{ width: barWidth + '%' }"></div>
                        <div class="entry-bar-glow" :style="{ left: barWidth + '%' }"></div>
                    </div>
                    <p class="entry-msg">{{ entryMessage }}</p>
                </div>
            </div>
        </transition>

        <div class="header">
            <button class="study-official-btn" @click="goToStudy">Study Official</button>
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
                    <p class="university">Democritus University of Thrace – DDARTECH spin-off company</p>
                </div>
            </transition>
            <img src="/DDART.png" style="height:30px;width:auto;object-fit:contain;" />
        </div>

        <div class="role-toggle">
            <button :class="['role-btn', { active: role === 'health-center' }]" @click="role = 'health-center'; error = ''">{{ t('Health Center', 'Κέντρο Υγείας') }}</button>
            <button :class="['role-btn', { active: role === 'doctor' }]" @click="role = 'doctor'; error = ''">{{ t('Expert', 'Ειδικός Ιατρός') }}</button>
        </div>

        <div class="main-card">
            <div class="card-inner">
                <div class="left-panel">
                    <transition name="panel-slide" mode="out-in">

                        <div v-if="role === 'health-center'" key="hc-info" class="left-content">
                            <h2>{{ t('Health Center Portal', 'Πύλη Κέντρου Υγείας') }}</h2>
                            <p>{{ t('Sign in with your Health Center credentials to upload retinal images for AI screening and expert review.', 'Συνδεθείτε με τα στοιχεία του Κέντρου Υγείας σας για να ανεβάσετε εικόνες αμφιβληστροειδή για αξιολόγηση από ΤΝ και ειδικούς γιατρούς.') }}</p>
                        </div>

                        <div v-else key="doctor-info" class="left-content">
                            <h2>{{ t('Expert Portal', 'Πύλη Ειδικών Ιατρών') }}</h2>
                            <p>{{ t('Access the clinical dashboard to review and evaluate retinal images', 'Πρόσβαση στον κλινικό πίνακα για προβολή και αξιολόγηση εικόνων.') }}</p>
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
                                <label>{{ t('Health Center ID', 'Κωδικος Κεντρου Υγειας') }}</label>
                                <input v-model="centerId" type="text" maxlength="5" :placeholder="t('5-digit center ID', '5-ψήφιος κωδικός κέντρου')" />
                            </div>
                            <div class="field">
                                <label>{{ t('Password', 'Κωδικος') }}</label>
                                <input v-model="password" type="password" :placeholder="t('Your password', 'Ο κωδικός σας')" @keyup.enter="healthCenterLogin" />
                            </div>
                            <transition name="error-pop">
                                <p v-if="error" class="error">{{ error }}</p>
                            </transition>
                            <button class="submit-btn" @click="healthCenterLogin" :disabled="loading">
                                <span class="btn-text">{{ loading ? t('Signing in...', 'Σύνδεση...') : t('Sign In', 'Σύνδεση') }}</span>
                                <span v-if="loading" class="btn-spinner"></span>
                            </button>
                            <p class="access-note">{{ t('Sign in with your 5-digit center ID provided by the DDARTECH administrator. Contact ddart@med.duth.gr to register.', 'Συνδεθείτε με τον 5-ψήφιο κωδικό κέντρου που σας έχει δοθεί από τον διαχειριστή DDARTECH.') }}</p>
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
            <div class="footer-left"><img src="/DDARTECH_Research-removebg-preview.png" class="dept-logo" /></div>
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
            showWelcome: false,
            role: 'health-center',
            mode: 'login',
            centerId: '',
            fullName: '',
            email: '',
            password: '',
            confirmPassword: '',
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
    if (localStorage.getItem('ddart_doctor')) this.$router.push('/research')

    if (sessionStorage.getItem('ddart_logout_anim')) {
        sessionStorage.removeItem('ddart_logout_anim')
        this.showOverlay = true
        this.barWidth = 0
        this.entryMessage = 'SIGNING OUT...'
        const start = performance.now()
        const duration = 2500
        const animate = (now) => {
            const progress = Math.min((now - start) / duration, 1)
            this.barWidth = Math.round((1 - Math.pow(1 - progress, 3)) * 100)
            if (progress < 1) requestAnimationFrame(animate)
            else this.showOverlay = false
        }
        requestAnimationFrame(animate)
        return
    }

    if (!sessionStorage.getItem('ddart_welcomed')) {
        sessionStorage.setItem('ddart_welcomed', '1')
        this.showWelcome = true
        setTimeout(() => { this.showWelcome = false }, 4200)
    }
    this.$nextTick(() => {
    const container = this.$refs.wParticles
    if (!container) return
    for (let i = 0; i < 20; i++) {
        const d = document.createElement('div')
        const seed = i * 137.508
        const x = (Math.sin(seed) * 0.5 + 0.5) * 100
        const y = (Math.cos(seed * 1.3) * 0.5 + 0.5) * 100
        const size = 1.5 + (i % 4) * 0.7
        d.style.cssText = `position:absolute;border-radius:50%;background:#63b3ed;left:${x}%;top:${y}%;width:${size}px;height:${size}px;animation:particle-float linear ${4+(i%5)*1.1}s ${(i*0.3)%5}s infinite;box-shadow:0 0 4px rgba(99,179,237,0.6)`
        container.appendChild(d)
    }
})
},

    methods: {
        particleStyle(i) {
            const seed = i * 137.508
            const x = (Math.sin(seed) * 0.5 + 0.5) * 100
            const y = (Math.cos(seed * 1.3) * 0.5 + 0.5) * 100
            const size = 1.5 + (i % 4) * 0.8
            const delay = (i * 0.4) % 6
            const duration = 4 + (i % 5) * 1.2
            return {
                left: x + '%',
                top: y + '%',
                width: size + 'px',
                height: size + 'px',
                animationDelay: delay + 's',
                animationDuration: duration + 's',
                opacity: 0.15 + (i % 3) * 0.1
            }
        },

        goToStudy() {
            this.showEntryAnimation('STUDY OFFICIAL', '/study')
        },

        toggleDark() {
            this.isDark = !this.isDark
            localStorage.setItem('ddart_dark', this.isDark)
        },

        showEntryAnimation(message, destination) {
            this.entryMessage = message
            this.showOverlay = true
            this.barWidth = 0
            const duration = 4000
            const start = performance.now()
            const animate = (now) => {
                const progress = Math.min((now - start) / duration, 1)
                this.barWidth = Math.round((1 - Math.pow(1 - progress, 3)) * 100)
                if (progress < 1) requestAnimationFrame(animate)
                else setTimeout(() => this.$router.push(destination), 200)
            }
            requestAnimationFrame(animate)
        },

        runAnimThenNavigate(destination) {
            const duration = 4000
            const start = performance.now()
            const animate = (now) => {
                const progress = Math.min((now - start) / duration, 1)
                this.barWidth = Math.round((1 - Math.pow(1 - progress, 3)) * 100)
                if (progress < 1) requestAnimationFrame(animate)
                else setTimeout(() => this.$router.push(destination), 200)
            }
            requestAnimationFrame(animate)
        },

        async healthCenterLogin() {
            this.error = ''
            if (!this.centerId || !this.password) { this.error = this.t('Please fill in all fields', 'Παρακαλώ συμπληρώστε όλα τα πεδία'); return }
            this.loading = true
            this.showOverlay = true
            this.barWidth = 0
            this.entryMessage = this.t('Authenticating...', 'Επαλήθευση...')
            await this.$nextTick()
            await new Promise(r => setTimeout(r, 60))
            try {
                const res = await fetch('https://labiris.myiplist.com/health-center/login', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ center_id: this.centerId, password: this.password })
                })
                const data = await res.json()
                if (!res.ok) {
                    this.showOverlay = false; this.loading = false
                    this.error = data.detail || this.t('Login failed', 'Αποτυχία σύνδεσης'); return
                }
                localStorage.setItem('ddart_health_center', JSON.stringify({ id: data.health_center_id, name: data.name, specialty: data.specialty || '', center_id: data.center_id || '' }))
                this.entryMessage = this.t('Welcome, ' + data.name, 'Καλώς ορίσατε, ' + data.name)
                this.loading = false
                this.runAnimThenNavigate('/health-center')
            } catch {
                this.showOverlay = false; this.loading = false
                this.error = this.t('Connection failed. Please try again.', 'Αποτυχία σύνδεσης. Δοκιμάστε ξανά.')
            }
        },

        async doctorLogin() {
            this.error = ''
            if (!this.email || !this.password) { this.error = this.t('Please fill in all fields', 'Παρακαλώ συμπληρώστε όλα τα πεδία'); return }
            this.loading = true
            this.showOverlay = true
            this.barWidth = 0
            this.entryMessage = this.t('Authenticating...', 'Επαλήθευση...')
            await this.$nextTick()
            await new Promise(r => setTimeout(r, 60))
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/login', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: this.email, password: this.password })
                })
                const data = await res.json()
                if (!res.ok) {
                    this.showOverlay = false; this.loading = false
                    this.error = data.detail || this.t('Login failed', 'Αποτυχία σύνδεσης'); return
                }
                localStorage.setItem('ddart_doctor', JSON.stringify({ id: data.doctor_id, name: data.full_name, is_research: true }))
                this.entryMessage = this.t('Welcome, Dr. ' + data.full_name, 'Καλώς ορίσατε, Δρ. ' + data.full_name)
                this.loading = false
                this.runAnimThenNavigate('/research')
            } catch {
                this.showOverlay = false; this.loading = false
                this.error = this.t('Connection failed. Please try again.', 'Αποτυχία σύνδεσης. Δοκιμάστε ξανά.')
            }
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
                alert(this.t('Account created! You account is pending approval by the administrator.', 'Ο λογαριασμός δημιουργήθηκε! Ο λογαριασμός σας πρέπει να αποδεχτεί από τον admin.'))
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

/* ══════════════════════════════════════════
   ENTRY OVERLAY — CINEMATIC VERSION
   ══════════════════════════════════════════ */
.entry-overlay { position: fixed; inset: 0; z-index: 9999; background: radial-gradient(ellipse at 50% 40%, #0a1628 0%, #04080f 100%); display: flex; align-items: center; justify-content: center; overflow: hidden; }
.welcome-overlay { position: fixed; inset: 0; z-index: 10000; background: radial-gradient(ellipse at 50% 40%, #071428 0%, #020810 100%); display: flex; align-items: center; justify-content: center; overflow: hidden; cursor: pointer; }
.welcome-particles { position: absolute; inset: 0; pointer-events: none; }
.welcome-content { display: flex; flex-direction: column; align-items: center; gap: 20px; position: relative; z-index: 2; }
.welcome-eye-wrap { position: relative; width: 260px; height: 120px; animation: wEyeIn 0.9s 0.1s cubic-bezier(0.22,1,0.36,1) both; filter: drop-shadow(0 0 18px rgba(99,179,237,0.5)); }
.welcome-eye-svg { width: 100%; height: 100%; }
@keyframes wEyeIn { from { opacity:0; transform: scale(0.5) translateY(30px); } to { opacity:1; transform: scale(1) translateY(0); } }
.w-eye-outline { stroke-dasharray: 600; stroke-dashoffset: 600; animation: wDraw 1.2s 0.3s ease forwards; }
.w-iris { stroke-dasharray: 226; stroke-dashoffset: 226; animation: wDraw 0.6s 1.2s ease forwards; }
.w-pupil-ring { stroke-dasharray: 138; stroke-dashoffset: 138; animation: wDraw 0.5s 1.5s ease forwards; }
.w-inner-pupil { opacity: 0; animation: wFade 0.4s 1.8s ease forwards; }
.w-pupil-core { opacity: 0; animation: wFade 0.4s 1.95s ease forwards; }
.w-highlight { opacity: 0; animation: wFade 0.3s 2.0s ease forwards; }
.w-ray { opacity: 0; animation: wFade 0.4s 2.1s ease forwards; }
@keyframes wDraw { to { stroke-dashoffset: 0; } }
@keyframes wFade { to { opacity: 1; } }
.w-scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, rgba(99,179,237,0) 15%, rgba(99,179,237,0.95) 50%, rgba(99,179,237,0) 85%, transparent); animation: wScan 2s 1.2s ease-in-out infinite; }
@keyframes wScan { 0% { top: 8%; opacity: 0; } 8% { opacity: 1; } 92% { opacity: 1; } 100% { top: 92%; opacity: 0; } }
.w-scan-data { position: absolute; font-family: 'Courier New', monospace; font-size: 10px; font-weight: 700; letter-spacing: 1px; opacity: 0; animation: wFade 0.4s ease forwards; }
.w-sd1 { top: 22%; right: -44px; color: rgba(99,179,237,0.85); animation-delay: 2.2s; }
.w-sd2 { top: 55%; left: -50px; color: rgba(229,62,62,0.85); animation-delay: 2.4s; }
.w-sd3 { bottom: 18%; right: -36px; color: rgba(72,187,120,0.9); animation-delay: 2.6s; }
.w-label { font-size: 12px; font-weight: 700; letter-spacing: 5px; color: rgba(99,179,237,0.5); text-transform: uppercase; margin: 0; opacity: 0; animation: wFade 0.6s 1.6s ease forwards; }
.w-logo-row { display: flex; align-items: baseline; font-family: 'Arial Narrow', Arial, sans-serif; font-weight: 900; letter-spacing: 6px; }
.wl { color: white; font-size: 46px; opacity: 0; display: inline-block; }
.wl-1 { animation: wLetter 0.5s 1.8s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-2 { animation: wLetter 0.5s 1.95s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-3 { animation: wLetter 0.5s 2.1s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-4 { animation: wLetter 0.5s 2.25s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-5 { animation: wLetter 0.5s 2.4s cubic-bezier(0.34,1.56,0.64,1) forwards; }
@keyframes wLetter { from { opacity:0; transform: translateY(-40px) scale(0.6); } to { opacity:1; transform: translateY(0) scale(1); } }
.wl-ai { color: #e53e3e; font-size: 88px; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; margin-left: 10px; opacity: 0; animation: wAiSlam 0.7s 2.6s cubic-bezier(0.22,1,0.36,1) forwards; }
@keyframes wAiSlam { 0% { opacity:0; transform: scale(4) translateY(-10px); filter: blur(16px); } 60% { opacity:1; filter: blur(0); } 80% { transform: scale(0.95); } 100% { opacity:1; transform: scale(1); filter: blur(0); } }
.w-tagline { font-size: 11px; font-weight: 600; letter-spacing: 3px; color: rgba(99,179,237,0.4); text-transform: uppercase; margin: 0; opacity: 0; animation: wFade 0.6s 3.1s ease forwards; }
.w-bar-wrap { width: 220px; height: 1px; background: rgba(255,255,255,0.06); overflow: hidden; opacity: 0; animation: wFade 0.3s 3.0s ease forwards; }
.w-bar-fill { height: 100%; width: 0%; background: linear-gradient(90deg, #2b6cb0, #63b3ed, #90cdf4); animation: wBarFill 1.1s 3.1s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes wBarFill { to { width: 100%; } }
.welcome-fade-enter-active { transition: opacity 0.4s ease; }
.welcome-fade-leave-active { transition: opacity 0.8s ease, transform 0.8s ease, filter 0.8s ease; }
.welcome-fade-enter-from { opacity: 0; }
.welcome-fade-leave-to { opacity: 0; transform: scale(1.04); filter: blur(6px); }
/* Background grid */
.grid-lines { position: absolute; inset: 0; pointer-events: none; }
.grid-h { position: absolute; left: 0; right: 0; height: 1px; background: rgba(99,179,237,0.04); animation: grid-fade-in 1s ease both; }
.grid-v { position: absolute; top: 0; bottom: 0; width: 1px; background: rgba(99,179,237,0.04); animation: grid-fade-in 1s ease both; }
@keyframes grid-fade-in { from { opacity: 0; } to { opacity: 1; } }

/* Floating particles */
.particle-field { position: absolute; inset: 0; pointer-events: none; }
.particle { position: absolute; background: #63b3ed; border-radius: 50%; animation: particle-float linear infinite; transform: translate(-50%, -50%); box-shadow: 0 0 4px rgba(99,179,237,0.6); }
@keyframes particle-float { 0% { transform: translate(-50%, -50%) scale(1); opacity: 0.15; } 50% { transform: translate(-50%, -60%) scale(1.4); opacity: 0.5; } 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.15; } }

.entry-content { display: flex; flex-direction: column; align-items: center; gap: 24px; position: relative; z-index: 2; }

/* Retinal scanner — larger */
.retinal-scanner { position: relative; width: 300px; height: 300px; animation: scanner-appear 0.8s cubic-bezier(0.22, 1, 0.36, 1) both; }
@keyframes scanner-appear { from { opacity: 0; transform: scale(0.7) rotate(-8deg); } to { opacity: 1; transform: scale(1) rotate(0deg); } }
.retina-svg { width: 100%; height: 100%; }

/* Ring draw animations */
.ring-draw { animation: ring-draw 2s 0.2s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
@keyframes ring-draw { from { stroke-dashoffset: 867; } to { stroke-dashoffset: 0; } }
.ring-draw-2 { animation: ring-draw-2 1.6s 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
@keyframes ring-draw-2 { from { stroke-dashoffset: 754; } to { stroke-dashoffset: 0; } }
.ring-spin { animation: ring-spin 12s linear infinite; transform-origin: 150px 150px; }
@keyframes ring-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* Crosshairs */
.crosshair { opacity: 0; animation: elem-appear 0.5s 1.2s ease forwards; }
.tick { opacity: 0; animation: elem-appear 0.4s 1.4s ease forwards; }
@keyframes elem-appear { to { opacity: 1; } }

/* Vessels */
.vessel { stroke-dasharray: 300; stroke-dashoffset: 300; animation: vessel-draw 1.2s 0.9s ease forwards; }
.vessel-2 { stroke-dasharray: 200; stroke-dashoffset: 200; animation: vessel-draw 1s 1.3s ease forwards; }
@keyframes vessel-draw { to { stroke-dashoffset: 0; } }

/* Optic disc & macula */
.disc-appear { opacity: 0; animation: disc-pop 0.6s 1.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
.macula-appear { opacity: 0; animation: disc-pop 0.6s 1.7s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
@keyframes disc-pop { from { opacity: 0; transform: scale(0); transform-box: fill-box; transform-origin: center; } to { opacity: 1; transform: scale(1); } }

/* Readout lines */
.readout-line { stroke-dasharray: 60; stroke-dashoffset: 60; animation: vessel-draw 0.6s 1.9s ease forwards; }

/* Scanner beam */
.scanner-beam { transform-origin: 150px 150px; animation: scan-rotate 3s linear infinite; }
@keyframes scan-rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* Corner brackets */
.bracket { opacity: 0; animation: bracket-slide 0.5s 0.1s cubic-bezier(0.22, 1, 0.36, 1) forwards; }
@keyframes bracket-slide { from { opacity: 0; stroke-dashoffset: 80; } to { opacity: 1; stroke-dashoffset: 0; } }

/* Scan line */
.scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, rgba(99,179,237,0.0) 15%, rgba(99,179,237,0.8) 50%, rgba(99,179,237,0.0) 85%, transparent); animation: scan-sweep 2.5s ease-in-out infinite; filter: blur(0.5px); }
@keyframes scan-sweep { 0% { top: 8%; opacity: 0; } 8% { opacity: 1; } 92% { opacity: 1; } 100% { top: 92%; opacity: 0; } }

/* Glints */
.glint { position: absolute; border-radius: 50%; background: #63b3ed; animation: glint-pulse 2.2s ease-in-out infinite; box-shadow: 0 0 8px 2px rgba(99,179,237,0.8); }
.glint-1 { width: 5px; height: 5px; top: 4px; left: calc(50% - 2px); animation-delay: 0s; }
.glint-2 { width: 4px; height: 4px; top: calc(50% - 2px); right: 4px; animation-delay: 0.75s; }
.glint-3 { width: 5px; height: 5px; bottom: 4px; left: calc(50% - 2px); animation-delay: 1.5s; }
.glint-4 { width: 4px; height: 4px; top: calc(50% - 2px); left: 4px; animation-delay: 0.37s; }
@keyframes glint-pulse { 0%, 100% { opacity: 0.2; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.8); } }

/* Data readouts */
.readout { position: absolute; font-family: 'Courier New', monospace; font-size: 10px; font-weight: 700; letter-spacing: 1px; opacity: 0; animation: elem-appear 0.4s ease forwards; }
.readout-1 { top: 26%; right: 2%; color: rgba(99,179,237,0.8); animation-delay: 2s; }
.readout-2 { top: 36%; left: 1%; color: rgba(229,62,62,0.8); animation-delay: 2.1s; }
.readout-3 { bottom: 28%; right: 4%; color: rgba(72,187,120,0.9); animation-delay: 2.2s; font-size: 11px; }

/* DDART logo — letter by letter */
.entry-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 28px; font-weight: 900; letter-spacing: 6px; display: flex; align-items: baseline; gap: 0; }
.entry-letter { color: white; opacity: 0; display: inline-block; animation: letter-drop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; text-shadow: 0 0 20px rgba(99,179,237,0.4); }
.entry-d  { animation-delay: 1.6s; }
.entry-d2 { animation-delay: 1.75s; }
.entry-a  { animation-delay: 1.9s; }
.entry-r  { animation-delay: 2.05s; }
.entry-t  { animation-delay: 2.2s; }
.entry-ai { color: #e53e3e; font-size: 56px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; opacity: 0; margin-left: 6px; animation: ai-slam 0.6s 2.4s cubic-bezier(0.22, 1, 0.36, 1) forwards; text-shadow: 0 0 30px rgba(229,62,62,0.5); }
@keyframes letter-drop { from { opacity: 0; transform: translateY(-20px) scale(0.8); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes ai-slam { from { opacity: 0; transform: scale(2.5); filter: blur(8px); } to { opacity: 1; transform: scale(1); filter: blur(0); } }

/* Tagline */
.entry-tagline { font-size: 10px; font-weight: 600; letter-spacing: 3px; color: rgba(99,179,237,0.5); text-transform: uppercase; opacity: 0; animation: elem-appear 0.6s 2.8s ease forwards; margin-top: -10px; }

/* Progress bar */
.entry-bar { width: 260px; height: 2px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: visible; position: relative; opacity: 0; animation: elem-appear 0.4s 1s ease forwards; }
.entry-bar-fill { height: 100%; background: linear-gradient(90deg, #2b6cb0, #63b3ed, #90cdf4); border-radius: 2px; transition: width 0.05s linear; position: relative; }
.entry-bar-glow { position: absolute; top: -3px; width: 12px; height: 8px; background: rgba(99,179,237,0.9); border-radius: 50%; filter: blur(3px); transform: translateX(-50%); transition: left 0.05s linear; }
.entry-msg { color: rgba(255,255,255,0.45); font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin: 0; opacity: 0; animation: elem-appear 0.5s 1.1s ease forwards; }

/* Overlay transition */
.overlay-fade-leave-active { transition: opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1), filter 0.6s ease; }
.overlay-fade-leave-to { opacity: 0; transform: scale(1.06); filter: blur(4px); }

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
@keyframes particle-float { 0%,100% { transform:translate(-50%,-50%) scale(1); opacity:0.12; } 50% { transform:translate(-50%,-65%) scale(1.5); opacity:0.45; } }
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