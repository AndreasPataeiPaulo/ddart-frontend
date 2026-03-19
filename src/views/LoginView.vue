<template>
    <div class="login-container" :class="{ dark: isDark }">

        <!-- Welcome animation -->
        <transition name="welcome-fade">
            <div v-if="showWelcome" class="welcome-overlay" @click="showWelcome = false">
                <div class="welcome-particles" ref="wParticles"></div>
                <div class="welcome-content">
                    <div class="wl-center-logo">
                        <svg viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg" class="wl-center-svg">
                            <defs>
                                <radialGradient id="beaconGrad" cx="50%" cy="0%" r="100%" fx="50%" fy="0%">
                                    <stop offset="0%" stop-color="#90cdf4" stop-opacity="0.9"/>
                                    <stop offset="100%" stop-color="#90cdf4" stop-opacity="0"/>
                                </radialGradient>
                                <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="#63b3ed" stop-opacity="0.6"/>
                                    <stop offset="100%" stop-color="#63b3ed" stop-opacity="0"/>
                                </radialGradient>
                            </defs>
                            <circle cx="120" cy="120" r="108" stroke="rgba(255,255,255,0.04)" stroke-width="12" fill="none"/>
                            <circle cx="120" cy="120" r="82"  stroke="rgba(43,108,176,0.08)"  stroke-width="10" fill="none"/>
                            <g class="wl-arc-outer-g">
                                <path d="M120 12 A108 108 0 1 1 12 120" stroke="#c8d0dc" stroke-width="12" stroke-linecap="round" fill="none" class="wl-arc-outer"/>
                            </g>
                            <g class="wl-arc-inner-g">
                                <path d="M120 38 A82 82 0 1 1 38 120" stroke="#2b6cb0" stroke-width="10" stroke-linecap="round" fill="none" class="wl-arc-inner"/>
                            </g>
                            <g class="wl-lh-g">
                                <rect x="90" y="158" width="60" height="10" rx="3" fill="#1a3a5c" class="wlh wlh1"/>
                                <rect x="95" y="152" width="50" height="8"  rx="2" fill="#1e4570" class="wlh wlh1"/>
                                <path d="M103,152 L117,152 L114,96 L106,96 Z" fill="#2d4a6b" class="wlh wlh2"/>
                                <path d="M103.8,145 L116.2,145 L115.8,138 L104.2,138 Z" fill="#1a3352" class="wlh wlh2"/>
                                <path d="M104.8,132 L115.2,132 L114.8,125 L105.2,125 Z" fill="#1a3352" class="wlh wlh2"/>
                                <path d="M105.5,119 L114.5,119 L114.2,112 L105.8,112 Z" fill="#1a3352" class="wlh wlh2"/>
                                <path d="M106,106 L114,106 L113.8,100 L106.2,100 Z"     fill="#1a3352" class="wlh wlh2"/>
                                <rect x="108" y="140" width="4" height="3"  rx="0.5" fill="#63b3ed" opacity="0.8" class="wlh wlh2"/>
                                <rect x="108" y="127" width="4" height="3"  rx="0.5" fill="#63b3ed" opacity="0.8" class="wlh wlh2"/>
                                <rect x="108" y="114" width="4" height="3"  rx="0.5" fill="#63b3ed" opacity="0.8" class="wlh wlh2"/>
                                <rect x="108" y="101" width="4" height="3"  rx="0.5" fill="#63b3ed" opacity="0.8" class="wlh wlh2"/>
                                <rect x="107" y="148" width="6" height="10" rx="3" fill="#0f2540" class="wlh wlh1"/>
                                <rect x="100" y="92" width="20" height="4" rx="1.5" fill="#2b6cb0" class="wlh wlh3"/>
                                <rect x="101" y="89" width="1.5" height="4" fill="#1e4570" class="wlh wlh3"/>
                                <rect x="104" y="89" width="1.5" height="4" fill="#1e4570" class="wlh wlh3"/>
                                <rect x="107" y="89" width="1.5" height="4" fill="#1e4570" class="wlh wlh3"/>
                                <rect x="110" y="89" width="1.5" height="4" fill="#1e4570" class="wlh wlh3"/>
                                <rect x="113" y="89" width="1.5" height="4" fill="#1e4570" class="wlh wlh3"/>
                                <rect x="116" y="89" width="1.5" height="4" fill="#1e4570" class="wlh wlh3"/>
                                <rect x="100" y="88" width="20" height="1.5" fill="#3d82c4" class="wlh wlh3"/>
                                <rect x="104" y="70" width="12" height="20" rx="2" fill="#1e3a5c" class="wlh wlh4"/>
                                <rect x="105.5" y="72" width="4"  height="8" rx="0.5" fill="#90cdf4" opacity="0.7" class="wlh wlh4"/>
                                <rect x="110.5" y="72" width="4"  height="8" rx="0.5" fill="#90cdf4" opacity="0.7" class="wlh wlh4"/>
                                <rect x="104"   y="76" width="12" height="1" fill="#1a3352" class="wlh wlh4"/>
                                <rect x="110"   y="70" width="1"  height="20" fill="#1a3352" class="wlh wlh4"/>
                                <path d="M102,70 L118,70 L113,60 L107,60 Z" fill="#2b6cb0" class="wlh wlh5"/>
                                <rect x="119" y="52" width="2.5" height="9" rx="1" fill="#2b6cb0" class="wlh wlh6"/>
                                <rect x="119" y="49" width="2.5" height="4" rx="1" fill="#63b3ed" class="wlh wlh6"/>
                                <circle cx="120" cy="49" r="2.5" fill="#90cdf4" class="wlh wlh7"/>
                                <polygon points="121.5,49 129,52 121.5,55" fill="#e53e3e" opacity="0.85" class="wlh wlh7"/>
                                <circle cx="120" cy="80" r="18" fill="url(#glowGrad)" class="wl-lh-glow"/>
                                <g class="wl-beacon-beam wl-beacon-on">
                                    <path d="M120,80 L70,30 L80,20 L120,80 Z" fill="url(#beaconGrad)" opacity="0.25"/>
                                </g>
                                <circle cx="120" cy="80" r="4" fill="#e2f8ff" class="wlh wlh7"/>
                                <circle cx="120" cy="80" r="2" fill="white"  class="wlh wlh7"/>
                            </g>
                        </svg>
                    </div>
                    <div class="w-logo-row">
                        <span class="wl wl-1">D</span><span class="wl wl-2">D</span><span class="wl wl-3">A</span><span class="wl wl-4">R</span><span class="wl wl-5">T</span>
                        <span class="wl wl-ai-text">AI</span>
                    </div>
                    <p class="w-tagline">Ophthalmology · Artificial Intelligence · Screening</p>
                    <div class="w-bar-wrap"><div class="w-bar-fill"></div></div>
                </div>
            </div>
        </transition>

        <!-- Entry overlay -->
        <transition name="overlay-fade">
            <div v-if="showOverlay" class="entry-overlay">
                <div class="particle-field">
                    <div v-for="i in 24" :key="i" class="particle" :style="particleStyle(i)"></div>
                </div>
                <div class="grid-lines">
                    <div v-for="i in 8" :key="'h'+i" class="grid-h" :style="{ top: (i*12)+'%' }"></div>
                    <div v-for="i in 8" :key="'v'+i" class="grid-v" :style="{ left: (i*12)+'%' }"></div>
                </div>
                <div class="entry-content">
                    <div class="retinal-scanner">
                        <svg class="retina-svg" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(66,153,225,0.25)"/><stop offset="100%" stop-color="rgba(66,153,225,0)"/></radialGradient>
                                <radialGradient id="beamGrad2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(99,179,237,0)"/><stop offset="70%" stop-color="rgba(99,179,237,0.08)"/><stop offset="100%" stop-color="rgba(99,179,237,0)"/></radialGradient>
                                <linearGradient id="ringGrad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#63b3ed"/><stop offset="50%" stop-color="#4299e1"/><stop offset="100%" stop-color="#2b6cb0"/></linearGradient>
                                <linearGradient id="ringGrad2" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#e53e3e"/><stop offset="100%" stop-color="#fc8181"/></linearGradient>
                                <filter id="glow"><feGaussianBlur stdDeviation="2.5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
                                <filter id="glow-strong"><feGaussianBlur stdDeviation="4" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
                            </defs>
                            <circle cx="150" cy="150" r="130" fill="url(#eyeGlow)"/>
                            <circle cx="150" cy="150" r="138" stroke="rgba(99,179,237,0.06)" stroke-width="1"/>
                            <circle cx="150" cy="150" r="138" stroke="url(#ringGrad1)" stroke-width="1.5" stroke-dasharray="867" stroke-dashoffset="867" class="ring-draw"/>
                            <circle cx="150" cy="150" r="120" stroke="rgba(99,179,237,0.35)" stroke-width="1" stroke-dasharray="754" stroke-dashoffset="754" class="ring-draw-2"/>
                            <circle cx="150" cy="150" r="98" stroke="rgba(99,179,237,0.08)" stroke-width="0.5" stroke-dasharray="4 6"/>
                            <circle cx="150" cy="150" r="75" stroke="rgba(99,179,237,0.06)" stroke-width="0.5" stroke-dasharray="3 5" class="ring-spin"/>
                            <circle cx="150" cy="150" r="55" stroke="rgba(99,179,237,0.08)" stroke-width="0.5"/>
                            <line x1="150" y1="6" x2="150" y2="44" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <line x1="150" y1="256" x2="150" y2="294" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <line x1="6" y1="150" x2="44" y2="150" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <line x1="256" y1="150" x2="294" y2="150" stroke="rgba(99,179,237,0.5)" stroke-width="1" class="crosshair" filter="url(#glow)"/>
                            <line x1="118" y1="18" x2="128" y2="32" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>
                            <line x1="182" y1="18" x2="172" y2="32" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>
                            <line x1="118" y1="282" x2="128" y2="268" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>
                            <line x1="182" y1="282" x2="172" y2="268" stroke="rgba(99,179,237,0.25)" stroke-width="0.8" class="crosshair"/>
                            <circle cx="178" cy="132" r="16" fill="rgba(66,153,225,0.08)" stroke="rgba(99,179,237,0.4)" stroke-width="1.5" filter="url(#glow)" class="disc-appear"/>
                            <circle cx="178" cy="132" r="8" fill="rgba(99,179,237,0.18)" stroke="rgba(99,179,237,0.6)" stroke-width="1" class="disc-appear"/>
                            <circle cx="178" cy="132" r="3" fill="rgba(99,179,237,0.8)" class="disc-appear" filter="url(#glow-strong)"/>
                            <path d="M168 126 Q135 112 105 90" stroke="rgba(99,179,237,0.35)" stroke-width="1.8" fill="none" class="vessel" filter="url(#glow)"/>
                            <path d="M165 135 Q132 138 98 148" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M168 142 Q150 168 136 196" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M186 125 Q210 106 232 88" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M190 135 Q218 136 244 143" stroke="rgba(99,179,237,0.3)" stroke-width="1.5" fill="none" class="vessel"/>
                            <path d="M184 145 Q196 172 192 204" stroke="rgba(99,179,237,0.25)" stroke-width="1.2" fill="none" class="vessel"/>
                            <path d="M140 100 Q125 95 110 104" stroke="rgba(99,179,237,0.2)" stroke-width="1" fill="none" class="vessel-2"/>
                            <path d="M120 148 Q108 160 100 175" stroke="rgba(99,179,237,0.2)" stroke-width="1" fill="none" class="vessel-2"/>
                            <path d="M215 100 Q225 110 220 125" stroke="rgba(99,179,237,0.2)" stroke-width="1" fill="none" class="vessel-2"/>
                            <circle cx="124" cy="150" r="18" fill="none" stroke="url(#ringGrad2)" stroke-width="1.2" stroke-dasharray="5 4" class="macula-appear"/>
                            <circle cx="124" cy="150" r="10" fill="rgba(229,62,62,0.08)" stroke="rgba(229,62,62,0.4)" stroke-width="1" class="macula-appear"/>
                            <circle cx="124" cy="150" r="4" fill="rgba(229,62,62,0.6)" class="macula-appear" filter="url(#glow)"/>
                            <path d="M150 150 L288 150 A138 138 0 0 1 150 288 Z" fill="url(#beamGrad2)" class="scanner-beam"/>
                            <path d="M20 58 L20 20 L58 20" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>
                            <path d="M242 20 L280 20 L280 58" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>
                            <path d="M20 242 L20 280 L58 280" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>
                            <path d="M242 280 L280 280 L280 242" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none" class="bracket" filter="url(#glow)"/>
                            <line x1="150" y1="12" x2="150" y2="20" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="150" y1="280" x2="150" y2="288" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="12" y1="150" x2="20" y2="150" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="280" y1="150" x2="288" y2="150" stroke="rgba(99,179,237,0.4)" stroke-width="1" class="tick"/>
                            <line x1="196" y1="116" x2="226" y2="96" stroke="rgba(99,179,237,0.4)" stroke-width="0.8" class="readout-line"/>
                            <line x1="226" y1="96" x2="256" y2="96" stroke="rgba(99,179,237,0.4)" stroke-width="0.8" class="readout-line"/>
                            <line x1="106" y1="132" x2="76" y2="112" stroke="rgba(229,62,62,0.4)" stroke-width="0.8" class="readout-line"/>
                            <line x1="76" y1="112" x2="46" y2="112" stroke="rgba(229,62,62,0.4)" stroke-width="0.8" class="readout-line"/>
                        </svg>
                        <div class="scan-line"></div>
                        <div class="glint glint-1"></div><div class="glint glint-2"></div><div class="glint glint-3"></div><div class="glint glint-4"></div>
                        <div class="readout readout-1">OD: 0.42</div>
                        <div class="readout readout-2">MAC: 0.18</div>
                        <div class="readout readout-3">AI ✓</div>
                    </div>
                    <div class="entry-logo">
                        <span class="entry-d entry-letter">D</span><span class="entry-d2 entry-letter">D</span><span class="entry-a entry-letter">A</span><span class="entry-r entry-letter">R</span><span class="entry-t entry-letter">T</span>
                        <span class="entry-ai">AI</span>
                    </div>
                    <div class="entry-tagline">Ophthalmology · Artificial Intelligence · Screening</div>
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
            <div class="role-indicator" :style="{ transform: role === 'health-center' ? 'translateX(0)' : 'translateX(100%)' }"></div>
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
                        <div class="tab-underline" :style="tabUnderlineStyle"></div>
                    </div>

                    <transition name="form-slide" mode="out-in">

                        <!-- HEALTH CENTER LOGIN -->
                        <div v-if="role === 'health-center' && mode === 'login'" key="hc-login" class="form">
                            <div class="field" :class="{ focused: focusedField === 'centerId', filled: centerId }">
                                <label>{{ t('Health Center ID', 'Κωδικος Κεντρου Υγειας') }}</label>
                                <div class="input-wrap">
                                    <input v-model="centerId" type="text" maxlength="5"
                                        :placeholder="t('5-digit center ID', '5-ψήφιος κωδικός κέντρου')"
                                        @focus="focusedField = 'centerId'" @blur="focusedField = ''" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <div class="field" :class="{ focused: focusedField === 'hcPass', filled: password }">
                                <label>{{ t('Password', 'Κωδικος') }}</label>
                                <div class="input-wrap">
                                    <input v-model="password" type="password"
                                        :placeholder="t('Your password', 'Ο κωδικός σας')"
                                        @focus="focusedField = 'hcPass'" @blur="focusedField = ''"
                                        @keyup.enter="healthCenterLogin" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <transition name="error-pop">
                                <p v-if="error" class="error">{{ error }}</p>
                            </transition>
                            <button class="submit-btn" @click="healthCenterLogin" :disabled="loading">
                                <span class="btn-bg"></span>
                                <span class="btn-text">{{ loading ? t('Signing in...', 'Σύνδεση...') : t('Sign In', 'Σύνδεση') }}</span>
                                <span v-if="loading" class="btn-spinner"></span>
                            </button>
                            <p class="access-note">{{ t('Sign in with your 5-digit center ID provided by the DDARTECH administrator. Contact ddart@med.duth.gr to register.', 'Συνδεθείτε με τον 5-ψήφιο κωδικό κέντρου που σας έχει δοθεί από τον διαχειριστή DDARTECH.') }}</p>
                        </div>

                        <!-- DOCTOR LOGIN -->
                        <div v-else-if="role === 'doctor' && mode === 'login'" key="d-login" class="form">
                            <div class="field" :class="{ focused: focusedField === 'email', filled: email }">
                                <label>{{ t('Email', 'Email') }}</label>
                                <div class="input-wrap">
                                    <input v-model="email" type="email"
                                        :placeholder="t('Your email address', 'Η διεύθυνση email σας')"
                                        @focus="focusedField = 'email'" @blur="focusedField = ''" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <div class="field" :class="{ focused: focusedField === 'pass', filled: password }">
                                <label>{{ t('Password', 'Κωδικός') }}</label>
                                <div class="input-wrap">
                                    <input v-model="password" type="password"
                                        :placeholder="t('Your password', 'Ο κωδικός σας')"
                                        @focus="focusedField = 'pass'" @blur="focusedField = ''"
                                        @keyup.enter="doctorLogin" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <transition name="error-pop">
                                <p v-if="error" class="error">{{ error }}</p>
                            </transition>
                            <button class="submit-btn" @click="doctorLogin" :disabled="loading">
                                <span class="btn-bg"></span>
                                <span class="btn-text">{{ loading ? t('Signing in...', 'Σύνδεση...') : t('Sign In', 'Σύνδεση') }}</span>
                                <span v-if="loading" class="btn-spinner"></span>
                            </button>
                        </div>

                        <!-- DOCTOR SIGNUP -->
                        <div v-else-if="role === 'doctor' && mode === 'signup'" key="d-signup" class="form">
                            <div class="field" :class="{ focused: focusedField === 'fullName', filled: fullName }">
                                <label>{{ t('Full Name', 'Ονοματεπώνυμο') }}</label>
                                <div class="input-wrap">
                                    <input v-model="fullName" type="text"
                                        :placeholder="t('Dr. First Last', 'Δρ. Όνομα Επώνυμο')"
                                        @focus="focusedField = 'fullName'" @blur="focusedField = ''" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <div class="field" :class="{ focused: focusedField === 'suEmail', filled: email }">
                                <label>{{ t('Email', 'Email') }}</label>
                                <div class="input-wrap">
                                    <input v-model="email" type="email"
                                        :placeholder="t('Your email address', 'Η διεύθυνση email σας')"
                                        @focus="focusedField = 'suEmail'" @blur="focusedField = ''" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <div class="field" :class="{ focused: focusedField === 'suPass', filled: password }">
                                <label>{{ t('Password', 'Κωδικός') }}</label>
                                <div class="input-wrap">
                                    <input v-model="password" type="password"
                                        :placeholder="t('At least 6 characters', 'Τουλάχιστον 6 χαρακτήρες')"
                                        @focus="focusedField = 'suPass'" @blur="focusedField = ''" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <div class="field" :class="{ focused: focusedField === 'suConf', filled: confirmPassword }">
                                <label>{{ t('Confirm Password', 'Επιβεβαίωση Κωδικού') }}</label>
                                <div class="input-wrap">
                                    <input v-model="confirmPassword" type="password"
                                        :placeholder="t('Repeat password', 'Επαναλάβετε τον κωδικό')"
                                        @focus="focusedField = 'suConf'" @blur="focusedField = ''" />
                                    <div class="input-line"></div>
                                </div>
                            </div>
                            <transition name="error-pop">
                                <p v-if="error" class="error">{{ error }}</p>
                            </transition>
                            <p class="gdpr-note">{{ t('Your account will be reviewed and approved by the DDART administrator before you can access the doctor panel.', 'Ο λογαριασμός σας θα αξιολογηθεί και εγκριθεί από τον διαχειριστή DDART πριν αποκτήσετε πρόσβαση.') }}</p>
                            <button class="submit-btn" @click="doctorSignup" :disabled="loading">
                                <span class="btn-bg"></span>
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
            entryMessage: '',
            focusedField: ''
        }
    },

    computed: {
        tabUnderlineStyle() {
            if (this.role !== 'doctor') return { width: '100%', transform: 'translateX(0)' }
            return {
                width: '50%',
                transform: this.mode === 'login' ? 'translateX(0)' : 'translateX(100%)'
            }
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
            setTimeout(() => { this.showWelcome = false }, 3500)
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
            return { left: x + '%', top: y + '%', width: size + 'px', height: size + 'px', animationDelay: delay + 's', animationDuration: duration + 's', opacity: 0.15 + (i % 3) * 0.1 }
        },

        goToStudy() { this.showEntryAnimation('STUDY OFFICIAL', '/study') },
        toggleDark() { this.isDark = !this.isDark; localStorage.setItem('ddart_dark', this.isDark) },

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
                if (!res.ok) { this.showOverlay = false; this.loading = false; this.error = data.detail || this.t('Login failed', 'Αποτυχία σύνδεσης'); return }
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
                if (!res.ok) { this.showOverlay = false; this.loading = false; this.error = data.detail || this.t('Login failed', 'Αποτυχία σύνδεσης'); return }
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
                alert(this.t('Account created! Your account is pending approval by the administrator.', 'Ο λογαριασμός δημιουργήθηκε! Ο λογαριασμός σας πρέπει να αποδεχτεί από τον admin.'))
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

/* ── Base container ── */
.login-container { display: flex; flex-direction: column; align-items: center; padding: 30px 20px 0; min-height: 100vh; width: 100%; background: #f0f4f8; transition: background 0.5s cubic-bezier(0.4,0,0.2,1); }

/* ── Welcome overlay ── */
.entry-overlay { position: fixed; inset: 0; z-index: 9999; background: radial-gradient(ellipse at 50% 40%, #0a1628 0%, #04080f 100%); display: flex; align-items: center; justify-content: center; overflow: hidden; }
/* ── Welcome overlay — lighthouse animation (3s total) ── */
.welcome-overlay { position: fixed; inset: 0; z-index: 10000; background: radial-gradient(ellipse at 50% 40%, #071428 0%, #020810 100%); display: flex; align-items: center; justify-content: center; overflow: hidden; cursor: pointer; }
.welcome-particles { position: absolute; inset: 0; pointer-events: none; }
.welcome-content { display: flex; flex-direction: column; align-items: center; gap: 20px; position: relative; z-index: 2; }

/* Center logo container */
.wl-center-logo { opacity: 0; animation: wLogoAppear 0.5s 0.1s cubic-bezier(0.22,1,0.36,1) forwards; filter: drop-shadow(0 0 24px rgba(43,108,176,0.4)); }
.wl-center-svg { width: 200px; height: 200px; }
@keyframes wLogoAppear { from { opacity:0; transform: scale(0.75); } to { opacity:1; transform: scale(1); } }

/* Both arcs spin clockwise — outer slower, inner faster */
.wl-arc-outer-g { transform-origin: 120px 120px; animation: wSpin 7s 0.2s linear infinite; }
.wl-arc-inner-g { transform-origin: 120px 120px; animation: wSpin 4s 0.2s linear infinite; }
@keyframes wSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* Arcs draw in quickly */
.wl-arc-outer { stroke-dasharray: 680; stroke-dashoffset: 680; animation: wArcDraw 0.7s 0.2s cubic-bezier(0.4,0,0.2,1) forwards; }
.wl-arc-inner { stroke-dasharray: 515; stroke-dashoffset: 515; animation: wArcDraw 0.6s 0.45s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes wArcDraw { to { stroke-dashoffset: 0; } }

/* Lighthouse group fades in as a unit */
.wl-lh-g { opacity: 0; animation: wFadeIn 0.1s 0.85s forwards; }
@keyframes wFadeIn { to { opacity: 1; } }

/* Parts build bottom to top — compressed into 0.85s–1.7s window */
.wlh { opacity: 0; transform-box: fill-box; transform-origin: center bottom; }
.wlh1 { animation: wlhPop 0.22s 0.9s  cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wlh2 { animation: wlhPop 0.22s 1.08s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wlh3 { animation: wlhPop 0.2s  1.26s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wlh4 { animation: wlhPop 0.2s  1.44s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wlh5 { animation: wlhPop 0.18s 1.6s  cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wlh6 { animation: wlhPop 0.18s 1.74s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wlh7 { animation: wlhPop 0.18s 1.86s cubic-bezier(0.34,1.56,0.64,1) forwards; }
@keyframes wlhPop { from { opacity:0; transform: scaleY(0); } to { opacity:1; transform: scaleY(1); } }

/* Beacon rotates and glows */
.wl-beacon-beam { transform-origin: 120px 80px; animation: wBeaconSpin 2.4s 2s linear infinite; }
.wl-beacon-on { opacity: 0; animation: wFadeIn2 0.3s 2s forwards; }
@keyframes wBeaconSpin { to { transform: rotate(360deg); } }
@keyframes wFadeIn2 { to { opacity: 1; } }
.wl-lh-glow { opacity: 0; animation: wGlowPulse 2.4s 2s ease-in-out infinite; }
@keyframes wGlowPulse { 0%,100% { opacity:0.25; } 50% { opacity:0.85; } }

/* DDART AI letters drop in — 2.0s to 2.75s */
.w-logo-row { display: flex; align-items: baseline; font-family: 'Arial Narrow', Arial, sans-serif; font-weight: 900; letter-spacing: 6px; }
.wl { color: white; font-size: 42px; opacity: 0; display: inline-block; }
.wl-1 { animation: wLetter 0.3s 2.0s  cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-2 { animation: wLetter 0.3s 2.1s  cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-3 { animation: wLetter 0.3s 2.2s  cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-4 { animation: wLetter 0.3s 2.3s  cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-5 { animation: wLetter 0.3s 2.4s  cubic-bezier(0.34,1.56,0.64,1) forwards; }
.wl-ai-text { color: #e53e3e; font-size: 42px; font-family: 'Arial Black', Arial, sans-serif; opacity: 0; margin-left: 8px; animation: wLetter 0.35s 2.52s cubic-bezier(0.34,1.56,0.64,1) forwards; }
@keyframes wLetter { from { opacity:0; transform: translateY(-28px) scale(0.65); } to { opacity:1; transform: translateY(0) scale(1); } }
.w-tagline { font-size: 11px; font-weight: 600; letter-spacing: 3px; color: rgba(99,179,237,0.4); text-transform: uppercase; margin: 0; opacity: 0; animation: wFade 0.4s 2.7s ease forwards; }
.w-bar-wrap { width: 220px; height: 1px; background: rgba(255,255,255,0.06); overflow: hidden; opacity: 0; animation: wFade 0.2s 2.65s ease forwards; }
.w-bar-fill { height: 100%; width: 0%; background: linear-gradient(90deg, #2b6cb0, #63b3ed, #90cdf4); animation: wBarFill 0.6s 2.7s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes wBarFill { to { width: 100%; } }
.welcome-fade-enter-active { transition: opacity 0.4s ease; }
.welcome-fade-leave-active { transition: opacity 0.8s ease, transform 0.8s ease, filter 0.8s ease; }
.welcome-fade-enter-from { opacity: 0; }
.welcome-fade-leave-to { opacity: 0; transform: scale(1.04); filter: blur(6px); }

/* ── Entry overlay internals ── */
.grid-lines { position: absolute; inset: 0; pointer-events: none; }
.grid-h { position: absolute; left: 0; right: 0; height: 1px; background: rgba(99,179,237,0.04); animation: grid-fade-in 1s ease both; }
.grid-v { position: absolute; top: 0; bottom: 0; width: 1px; background: rgba(99,179,237,0.04); animation: grid-fade-in 1s ease both; }
@keyframes grid-fade-in { from { opacity: 0; } to { opacity: 1; } }
.particle-field { position: absolute; inset: 0; pointer-events: none; }
.particle { position: absolute; background: #63b3ed; border-radius: 50%; animation: particle-float linear infinite; transform: translate(-50%,-50%); box-shadow: 0 0 4px rgba(99,179,237,0.6); }
@keyframes particle-float { 0%,100% { transform: translate(-50%,-50%) scale(1); opacity: 0.15; } 50% { transform: translate(-50%,-60%) scale(1.4); opacity: 0.5; } }
.entry-content { display: flex; flex-direction: column; align-items: center; gap: 24px; position: relative; z-index: 2; }
.retinal-scanner { position: relative; width: 300px; height: 300px; animation: scanner-appear 0.8s cubic-bezier(0.22,1,0.36,1) both; }
@keyframes scanner-appear { from { opacity: 0; transform: scale(0.7) rotate(-8deg); } to { opacity: 1; transform: scale(1) rotate(0deg); } }
.retina-svg { width: 100%; height: 100%; }
.ring-draw { animation: ring-draw 2s 0.2s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw { from { stroke-dashoffset: 867; } to { stroke-dashoffset: 0; } }
.ring-draw-2 { animation: ring-draw-2 1.6s 0.5s cubic-bezier(0.4,0,0.2,1) forwards; }
@keyframes ring-draw-2 { from { stroke-dashoffset: 754; } to { stroke-dashoffset: 0; } }
.ring-spin { animation: ring-spin 12s linear infinite; transform-origin: 150px 150px; }
@keyframes ring-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.crosshair { opacity: 0; animation: elem-appear 0.5s 1.2s ease forwards; }
.tick { opacity: 0; animation: elem-appear 0.4s 1.4s ease forwards; }
@keyframes elem-appear { to { opacity: 1; } }
.vessel { stroke-dasharray: 300; stroke-dashoffset: 300; animation: vessel-draw 1.2s 0.9s ease forwards; }
.vessel-2 { stroke-dasharray: 200; stroke-dashoffset: 200; animation: vessel-draw 1s 1.3s ease forwards; }
@keyframes vessel-draw { to { stroke-dashoffset: 0; } }
.disc-appear { opacity: 0; animation: disc-pop 0.6s 1.5s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.macula-appear { opacity: 0; animation: disc-pop 0.6s 1.7s cubic-bezier(0.34,1.56,0.64,1) forwards; }
@keyframes disc-pop { from { opacity: 0; transform: scale(0); transform-box: fill-box; transform-origin: center; } to { opacity: 1; transform: scale(1); } }
.readout-line { stroke-dasharray: 60; stroke-dashoffset: 60; animation: vessel-draw 0.6s 1.9s ease forwards; }
.scanner-beam { transform-origin: 150px 150px; animation: scan-rotate 3s linear infinite; }
@keyframes scan-rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.bracket { opacity: 0; animation: bracket-slide 0.5s 0.1s cubic-bezier(0.22,1,0.36,1) forwards; }
@keyframes bracket-slide { from { opacity: 0; stroke-dashoffset: 80; } to { opacity: 1; stroke-dashoffset: 0; } }
.scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, rgba(99,179,237,0) 15%, rgba(99,179,237,0.8) 50%, rgba(99,179,237,0) 85%, transparent); animation: scan-sweep 2.5s ease-in-out infinite; filter: blur(0.5px); }
@keyframes scan-sweep { 0% { top: 8%; opacity: 0; } 8% { opacity: 1; } 92% { opacity: 1; } 100% { top: 92%; opacity: 0; } }
.glint { position: absolute; border-radius: 50%; background: #63b3ed; animation: glint-pulse 2.2s ease-in-out infinite; box-shadow: 0 0 8px 2px rgba(99,179,237,0.8); }
.glint-1 { width: 5px; height: 5px; top: 4px; left: calc(50% - 2px); animation-delay: 0s; }
.glint-2 { width: 4px; height: 4px; top: calc(50% - 2px); right: 4px; animation-delay: 0.75s; }
.glint-3 { width: 5px; height: 5px; bottom: 4px; left: calc(50% - 2px); animation-delay: 1.5s; }
.glint-4 { width: 4px; height: 4px; top: calc(50% - 2px); left: 4px; animation-delay: 0.37s; }
@keyframes glint-pulse { 0%,100% { opacity: 0.2; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.8); } }
.readout { position: absolute; font-family: 'Courier New', monospace; font-size: 10px; font-weight: 700; letter-spacing: 1px; opacity: 0; animation: elem-appear 0.4s ease forwards; }
.readout-1 { top: 26%; right: 2%; color: rgba(99,179,237,0.8); animation-delay: 2s; }
.readout-2 { top: 36%; left: 1%; color: rgba(229,62,62,0.8); animation-delay: 2.1s; }
.readout-3 { bottom: 28%; right: 4%; color: rgba(72,187,120,0.9); animation-delay: 2.2s; font-size: 11px; }
.entry-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 28px; font-weight: 900; letter-spacing: 6px; display: flex; align-items: baseline; gap: 0; }
.entry-letter { color: white; opacity: 0; display: inline-block; animation: letter-drop 0.5s cubic-bezier(0.34,1.56,0.64,1) forwards; text-shadow: 0 0 20px rgba(99,179,237,0.4); }
.entry-d { animation-delay: 1.6s; } .entry-d2 { animation-delay: 1.75s; } .entry-a { animation-delay: 1.9s; } .entry-r { animation-delay: 2.05s; } .entry-t { animation-delay: 2.2s; }
.entry-ai { color: #e53e3e; font-size: 56px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; opacity: 0; margin-left: 6px; animation: ai-slam 0.6s 2.4s cubic-bezier(0.22,1,0.36,1) forwards; text-shadow: 0 0 30px rgba(229,62,62,0.5); }
@keyframes letter-drop { from { opacity: 0; transform: translateY(-20px) scale(0.8); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes ai-slam { from { opacity: 0; transform: scale(2.5); filter: blur(8px); } to { opacity: 1; transform: scale(1); filter: blur(0); } }
.entry-tagline { font-size: 10px; font-weight: 600; letter-spacing: 3px; color: rgba(99,179,237,0.5); text-transform: uppercase; opacity: 0; animation: elem-appear 0.6s 2.8s ease forwards; margin-top: -10px; }
.entry-bar { width: 260px; height: 2px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: visible; position: relative; opacity: 0; animation: elem-appear 0.4s 1s ease forwards; }
.entry-bar-fill { height: 100%; background: linear-gradient(90deg, #2b6cb0, #63b3ed, #90cdf4); border-radius: 2px; transition: width 0.05s linear; position: relative; }
.entry-bar-glow { position: absolute; top: -3px; width: 12px; height: 8px; background: rgba(99,179,237,0.9); border-radius: 50%; filter: blur(3px); transform: translateX(-50%); transition: left 0.05s linear; }
.entry-msg { color: rgba(255,255,255,0.45); font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin: 0; opacity: 0; animation: elem-appear 0.5s 1.1s ease forwards; }
.overlay-fade-leave-active { transition: opacity 0.6s cubic-bezier(0.4,0,0.2,1), transform 0.6s cubic-bezier(0.4,0,0.2,1), filter 0.6s ease; }
.overlay-fade-leave-to { opacity: 0; transform: scale(1.06); filter: blur(4px); }

/* ══════════════════════════════════════
   HEADER
══════════════════════════════════════ */
.header-controls { position: absolute; top: 20px; right: 20px; display: flex; align-items: center; gap: 12px; }
.lang-toggle { display: flex; align-items: center; gap: 4px; }
.lang-btn { background: none; border: none; font-family: 'Source Sans 3', sans-serif; font-size: 12px; font-weight: 700; color: #a0aec0; cursor: pointer; padding: 3px 6px; border-radius: 3px; transition: color 0.25s ease, background 0.25s ease, transform 0.15s ease; letter-spacing: 0.5px; }
.lang-btn.active { color: #2b6cb0; background: #ebf8ff; }
.lang-btn:hover:not(.active) { color: #4a5568; transform: translateY(-1px); }
.lang-btn:active { transform: scale(0.92); }
.lang-sep { color: #e2e8f0; font-size: 12px; }
.dark-btn { background: none; border: 1px solid #e2e8f0; border-radius: 20px; font-family: 'Source Sans 3', sans-serif; font-size: 11px; font-weight: 700; color: #718096; cursor: pointer; padding: 3px 12px; transition: background 0.25s ease, border-color 0.25s ease, color 0.25s ease, transform 0.15s ease, box-shadow 0.25s ease; letter-spacing: 0.4px; }
.dark-btn:hover { background: #edf2f7; border-color: #cbd5e0; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.dark-btn:active { transform: scale(0.95) translateY(0); }
.header { text-align: center; margin-bottom: 20px; width: 100%; position: relative; }
.header-text { transition: opacity 0.2s ease; }
.university { font-size: 14px; color: #2c5282; font-weight: 600; margin: 0 0 4px; transition: color 0.5s ease; }

/* ══════════════════════════════════════
   ROLE TOGGLE — animated sliding pill
══════════════════════════════════════ */
.role-toggle { position: relative; display: flex; gap: 0; margin-bottom: 20px; background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 4px; width: 100%; max-width: 760px; transition: background 0.4s ease, border-color 0.4s ease; overflow: hidden; }
.role-indicator { position: absolute; top: 4px; left: 4px; width: calc(50% - 4px); height: calc(100% - 8px); background: #2b6cb0; border-radius: 5px; transition: transform 0.35s cubic-bezier(0.4,0,0.2,1); pointer-events: none; box-shadow: 0 2px 8px rgba(43,108,176,0.25); }
.role-btn { flex: 1; padding: 8px 16px; border: none; border-radius: 5px; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; background: none; white-space: nowrap; position: relative; z-index: 1; transition: color 0.3s ease, transform 0.15s ease; }
.role-btn.active { color: white; }
.role-btn:hover:not(.active) { color: #4a5568; }
.role-btn:active { transform: scale(0.97); }

/* ══════════════════════════════════════
   MAIN CARD
══════════════════════════════════════ */
.main-card { background: white; border: 1px solid #e2e8f0; border-radius: 10px; width: 100%; max-width: 760px; margin-bottom: 24px; box-shadow: 0 2px 20px rgba(0,0,0,0.07); transition: background 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease; overflow: hidden; }
.card-inner { display: grid; grid-template-columns: 260px 1fr; min-height: 360px; }
.left-panel { background: #2b6cb0; display: flex; align-items: center; padding: 32px 28px; overflow: hidden; transition: background 0.4s ease; }
.left-content h2 { font-family: 'Playfair Display', serif; color: white; font-size: 20px; margin: 0 0 10px; }
.left-content p { color: rgba(255,255,255,0.85); font-size: 13px; line-height: 1.7; margin: 0; }
.right-panel { padding: 24px 28px; display: flex; flex-direction: column; gap: 14px; overflow: hidden; }

/* ══════════════════════════════════════
   TABS — sliding underline
══════════════════════════════════════ */
.tabs { position: relative; display: flex; border-bottom: 1px solid #e2e8f0; gap: 0; transition: border-color 0.4s ease; }
.tab { flex: 1; padding: 10px 20px; border: none; background: none; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; color: #a0aec0; cursor: pointer; transition: color 0.25s ease, transform 0.15s ease; position: relative; }
.tab.active { color: #2b6cb0; }
.tab:hover:not(.active) { color: #718096; }
.tab:active { transform: scale(0.97); }
.tab-underline { position: absolute; bottom: -1px; height: 2px; background: #2b6cb0; border-radius: 2px 2px 0 0; transition: transform 0.35s cubic-bezier(0.4,0,0.2,1), width 0.35s cubic-bezier(0.4,0,0.2,1); }

/* ══════════════════════════════════════
   FORM FIELDS — floating label style
══════════════════════════════════════ */
.form { display: flex; flex-direction: column; gap: 10px; }
.field { display: flex; flex-direction: column; gap: 4px; }
.field label { font-size: 11px; font-weight: 700; color: #a0aec0; text-transform: uppercase; letter-spacing: 0.6px; transition: color 0.25s ease; }
.field.focused label { color: #2b6cb0; }
.input-wrap { position: relative; }
.field input { padding: 9px 0 8px; border: none; border-bottom: 1.5px solid #e2e8f0; border-radius: 0; font-family: 'Source Sans 3', sans-serif; font-size: 14px; color: #2d3748; outline: none; width: 100%; background: transparent; transition: border-color 0.25s ease, color 0.4s ease; }
.field input::placeholder { color: #cbd5e0; transition: color 0.25s ease; }
.field.focused input::placeholder { color: #a0aec0; }
.input-line { position: absolute; bottom: 0; left: 0; width: 0%; height: 2px; background: #2b6cb0; border-radius: 2px; transition: width 0.35s cubic-bezier(0.4,0,0.2,1); }
.field.focused .input-line { width: 100%; }

.hint { font-size: 11px; color: #a0aec0; }
.gdpr-note { font-size: 11px; color: #718096; line-height: 1.6; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 10px; margin: 0; transition: background 0.4s ease, border-color 0.4s ease, color 0.4s ease; }
.access-note { font-size: 11px; color: #718096; line-height: 1.6; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 10px; margin: 0; transition: background 0.4s ease, border-color 0.4s ease, color 0.4s ease; }

/* ══════════════════════════════════════
   SUBMIT BUTTON — shimmer fill effect
══════════════════════════════════════ */
.submit-btn { position: relative; overflow: hidden; padding: 12px; background: #2b6cb0; color: white; border: none; border-radius: 6px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 700; cursor: pointer; margin-top: 6px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.3s ease, transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.3s ease; letter-spacing: 0.3px; }
.submit-btn .btn-bg { position: absolute; inset: 0; background: linear-gradient(135deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.12) 50%, rgba(255,255,255,0) 100%); transform: translateX(-100%); transition: transform 0.6s cubic-bezier(0.4,0,0.2,1); pointer-events: none; }
.submit-btn:hover:not(:disabled) { background: #2c5282; box-shadow: 0 6px 20px rgba(43,108,176,0.35); transform: translateY(-2px); }
.submit-btn:hover:not(:disabled) .btn-bg { transform: translateX(100%); }
.submit-btn:active:not(:disabled) { transform: translateY(0) scale(0.98); box-shadow: 0 2px 8px rgba(43,108,176,0.2); transition: transform 0.1s ease, box-shadow 0.1s ease; }
.submit-btn:disabled { opacity: 0.45; cursor: not-allowed; }
.btn-text { position: relative; z-index: 1; }
.btn-spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.35); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; position: relative; z-index: 1; }
@keyframes spin { to { transform: rotate(360deg); } }
.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0; }

/* ══════════════════════════════════════
   STUDY OFFICIAL BUTTON
══════════════════════════════════════ */
.study-official-btn { position: absolute; top: 0; left: 0; background: none; border: 1px solid #e2e8f0; border-radius: 20px; font-family: 'Source Sans 3', sans-serif; font-size: 11px; font-weight: 700; color: #718096; cursor: pointer; padding: 4px 12px; letter-spacing: 0.3px; transition: all 0.3s cubic-bezier(0.4,0,0.2,1); }
.study-official-btn:hover { color: #2b6cb0; border-color: #2b6cb0; background: #ebf8ff; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(43,108,176,0.15); }
.study-official-btn:active { transform: scale(0.95); }

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
.footer { width: 100%; max-width: 760px; display: flex; justify-content: space-between; align-items: center; padding: 16px 0 24px; border-top: 1px solid #e2e8f0; margin-top: auto; gap: 16px; transition: border-color 0.4s ease; }
.dept-logo { height: 50px; width: auto; object-fit: contain; }
.footer-right { text-align: right; }
.footer-right p { font-size: 12px; color: #718096; margin: 2px 0; transition: color 0.4s ease; }
.footer-right a { color: #2b6cb0; text-decoration: none; transition: color 0.2s ease; }
.footer-right a:hover { color: #2c5282; }
.made-by { font-size: 10px; color: #cbd5e0; margin-top: 4px; }

/* ══════════════════════════════════════
   TRANSITIONS
══════════════════════════════════════ */
.panel-slide-enter-active { transition: opacity 0.35s cubic-bezier(0.4,0,0.2,1), transform 0.35s cubic-bezier(0.4,0,0.2,1); }
.panel-slide-leave-active { transition: opacity 0.2s cubic-bezier(0.4,0,1,1), transform 0.2s cubic-bezier(0.4,0,1,1); }
.panel-slide-enter-from { opacity: 0; transform: translateY(12px); }
.panel-slide-leave-to { opacity: 0; transform: translateY(-8px); }
.form-slide-enter-active { transition: opacity 0.3s cubic-bezier(0.4,0,0.2,1), transform 0.3s cubic-bezier(0.4,0,0.2,1); }
.form-slide-leave-active { transition: opacity 0.18s cubic-bezier(0.4,0,1,1), transform 0.18s cubic-bezier(0.4,0,1,1); }
.form-slide-enter-from { opacity: 0; transform: translateX(10px); }
.form-slide-leave-to { opacity: 0; transform: translateX(-10px); }
.header-fade-enter-active { transition: opacity 0.25s ease; }
.header-fade-leave-active { transition: opacity 0.15s ease; }
.header-fade-enter-from, .header-fade-leave-to { opacity: 0; }
.error-pop-enter-active { transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.34,1.56,0.64,1), max-height 0.3s ease; }
.error-pop-leave-active { transition: opacity 0.2s ease, transform 0.2s ease, max-height 0.2s ease; }
.error-pop-enter-from { opacity: 0; transform: translateY(-6px) scale(0.96); max-height: 0; }
.error-pop-leave-to { opacity: 0; transform: translateY(-4px); max-height: 0; }

/* ══════════════════════════════════════
   DARK MODE
══════════════════════════════════════ */
.dark.login-container { background: #1a202c; }
.dark .university { color: #90cdf4; }
.dark .role-toggle { background: #2d3748; border-color: #4a5568; }
.dark .role-indicator { box-shadow: 0 2px 8px rgba(99,179,237,0.2); }
.dark .role-btn { color: #a0aec0; }
.dark .role-btn:hover:not(.active) { color: #e2e8f0; }
.dark .main-card { background: #2d3748; border-color: #4a5568; box-shadow: 0 2px 20px rgba(0,0,0,0.3); }
.dark .right-panel { background: #2d3748; }
.dark .tabs { border-bottom-color: #4a5568; }
.dark .tab { color: #718096; }
.dark .tab.active { color: #63b3ed; }
.dark .tab-underline { background: #63b3ed; }
.dark .field label { color: #718096; }
.dark .field.focused label { color: #63b3ed; }
.dark .field input { border-bottom-color: #4a5568; color: #e2e8f0; }
.dark .field input::placeholder { color: #4a5568; }
.dark .input-line { background: #63b3ed; }
.dark .gdpr-note, .dark .access-note { background: #1a202c; border-color: #4a5568; color: #a0aec0; }
.dark .submit-btn { background: #2b6cb0; }
.dark .submit-btn:hover:not(:disabled) { background: #2c5282; box-shadow: 0 6px 20px rgba(99,179,237,0.25); }
.dark .lang-btn.active { color: #63b3ed; background: #1a365d; }
.dark .lang-btn:hover:not(.active) { color: #e2e8f0; }
.dark .lang-sep { color: #4a5568; }
.dark .dark-btn { border-color: #4a5568; color: #a0aec0; }
.dark .dark-btn:hover { background: #3d4a5c; border-color: #718096; }
.dark .footer { border-top-color: #4a5568; }
.dark .footer-right p { color: #718096; }
.dark .footer-right a { color: #63b3ed; }
.dark .study-official-btn { border-color: #4a5568; color: #718096; }
.dark .study-official-btn:hover { color: #63b3ed; border-color: #63b3ed; background: #1a365d; box-shadow: 0 2px 8px rgba(99,179,237,0.15); }

/* ══════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════ */
@keyframes particle-float { 0%,100% { transform:translate(-50%,-50%) scale(1); opacity:0.12; } 50% { transform:translate(-50%,-65%) scale(1.5); opacity:0.45; } }
@media (max-width: 768px) {
    .login-container { padding: 20px 16px 0; }
    .header-controls { top: 12px; right: 12px; }
    .university { font-size: 12px; }
    .role-toggle { max-width: 100%; }
    .role-btn { font-size: 12px; padding: 8px 10px; }
    .card-inner { grid-template-columns: 1fr; min-height: unset; }
    .left-panel { padding: 20px; align-items: flex-start; }
    .left-content h2 { font-size: 18px; }
    .left-content p { font-size: 12px; margin-bottom: 10px; }
    .right-panel { padding: 20px; }
    .footer { flex-direction: column; align-items: center; text-align: center; gap: 12px; }
    .footer-right { text-align: center; }
    .dept-logo { height: 40px; }
    .entry-ai { font-size: 56px; }
}
@media (max-width: 480px) {
    .login-container { padding: 16px 12px 0; }
    .university { font-size: 11px; }
    .tab { padding: 8px 12px; font-size: 13px; }
    .right-panel { padding: 16px; }
    .header-controls { gap: 8px; }
    .entry-bar { width: 200px; }
    .entry-ai { font-size: 48px; }
}
</style>