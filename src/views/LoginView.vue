<template>
    <div class="login-container" :class="{ dark: isDark }">

        <!-- Welcome animation -->
        <transition name="welcome-fade">
            <div v-if="showWelcome" class="welcome-overlay" @click="showWelcome = false">
                <div class="welcome-particles" ref="wParticles"></div>
                <div class="welcome-content">
                    <div class="wl-center-logo">
                        <svg viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg" class="wl-center-svg">
                            <defs>
                                <radialGradient id="bGrad" cx="50%" cy="0%" r="120%">
                                    <stop offset="0%" stop-color="#90cdf4" stop-opacity="0.9" />
                                    <stop offset="100%" stop-color="#90cdf4" stop-opacity="0" />
                                </radialGradient>
                                <radialGradient id="gGrad" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="#4299e1" stop-opacity="0.7" />
                                    <stop offset="100%" stop-color="#4299e1" stop-opacity="0" />
                                </radialGradient>
                            </defs>
                            <circle cx="110" cy="110" r="102" stroke="rgba(255,255,255,0.03)" stroke-width="13"
                                fill="none" class="wl-ring-pulse" />
                            <circle cx="110" cy="110" r="78" stroke="rgba(43,108,176,0.06)" stroke-width="10"
                                fill="none" />
                            <g class="wl-arc-outer-g">
                                <path d="M110 8 A102 102 0 1 1 8 110" stroke="#c8d2de" stroke-width="13"
                                    stroke-linecap="round" fill="none" class="wl-arc-outer" />
                            </g>
                            <g class="wl-arc-inner-g">
                                <path d="M110 32 A78 78 0 1 1 32 110" stroke="#2b6cb0" stroke-width="10"
                                    stroke-linecap="round" fill="none" class="wl-arc-inner" />
                            </g>
                            <g class="wl-lh-g">
                                <rect x="82" y="152" width="56" height="10" rx="3" fill="#1a3a5c" class="wlh wlh1" />
                                <rect x="87" y="146" width="46" height="8" rx="2" fill="#1e4570" class="wlh wlh1" />
                                <path d="M96,146 L124,146 L121,94 L99,94 Z" fill="#2d4a6b" class="wlh wlh2" />
                                <path d="M96.8,138 L123.2,138 L122.6,131 L97.4,131 Z" fill="#1a3352" class="wlh wlh2" />
                                <path d="M97.6,125 L122.4,125 L121.8,118 L98.2,118 Z" fill="#1a3352" class="wlh wlh2" />
                                <path d="M98.4,112 L121.6,112 L121.1,106 L98.9,106 Z" fill="#1a3352" class="wlh wlh2" />
                                <rect x="108" y="133" width="4" height="3" rx="0.5" fill="#63b3ed" opacity="0.85"
                                    class="wlh wlh2" />
                                <rect x="108" y="120" width="4" height="3" rx="0.5" fill="#63b3ed" opacity="0.85"
                                    class="wlh wlh2" />
                                <rect x="108" y="107" width="4" height="3" rx="0.5" fill="#63b3ed" opacity="0.85"
                                    class="wlh wlh2" />
                                <rect x="106" y="143" width="8" height="11" rx="4" fill="#0f2540" class="wlh wlh1" />
                                <rect x="93" y="90" width="24" height="5" rx="2" fill="#2b6cb0" class="wlh wlh3" />
                                <rect x="94" y="87" width="1.5" height="4" fill="#1a3a5c" class="wlh wlh3" />
                                <rect x="97.5" y="87" width="1.5" height="4" fill="#1a3a5c" class="wlh wlh3" />
                                <rect x="101" y="87" width="1.5" height="4" fill="#1a3a5c" class="wlh wlh3" />
                                <rect x="104.5" y="87" width="1.5" height="4" fill="#1a3a5c" class="wlh wlh3" />
                                <rect x="108" y="87" width="1.5" height="4" fill="#1a3a5c" class="wlh wlh3" />
                                <rect x="111.5" y="87" width="1.5" height="4" fill="#1a3a5c" class="wlh wlh3" />
                                <rect x="115" y="87" width="1.5" height="4" fill="#1a3a5c" class="wlh wlh3" />
                                <rect x="93" y="86" width="24" height="1.5" fill="#3d82c4" class="wlh wlh3" />
                                <rect x="98" y="66" width="24" height="25" rx="2" fill="#1e3a5c" class="wlh wlh4" />
                                <rect x="99.5" y="68" width="8" height="10" rx="0.5" fill="#90cdf4" opacity="0.7"
                                    class="wlh wlh4" />
                                <rect x="112.5" y="68" width="8" height="10" rx="0.5" fill="#90cdf4" opacity="0.7"
                                    class="wlh wlh4" />
                                <rect x="98" y="73" width="24" height="1.2" fill="#1a3352" class="wlh wlh4" />
                                <rect x="110" y="66" width="1.2" height="25" fill="#1a3352" class="wlh wlh4" />
                                <path d="M96,66 L124,66 L118,54 L102,54 Z" fill="#2b6cb0" class="wlh wlh5" />
                                <path d="M97.5,66 L122.5,66 L117,56 L103,56 Z" fill="#1e4570" opacity="0.45"
                                    class="wlh wlh5" />
                                <rect x="108.5" y="45" width="3" height="10" rx="1.5" fill="#2b6cb0" class="wlh wlh6" />
                                <rect x="108.5" y="42" width="3" height="4" rx="1.5" fill="#63b3ed" class="wlh wlh6" />
                                <circle cx="110" cy="42" r="3" fill="#90cdf4" class="wlh wlh7" />
                                <polygon points="111.5,42 120,45 111.5,48" fill="#e53e3e" opacity="0.9"
                                    class="wlh wlh7" />
                                <circle cx="110" cy="78" r="22" fill="url(#gGrad)" class="wl-lh-glow" />
                                <g class="wl-beacon-beam wl-beacon-on">
                                    <path d="M110,78 L56,26 L68,16 L110,78 Z" fill="url(#bGrad)" opacity="0.22" />
                                </g>
                                <circle cx="110" cy="78" r="2.5" fill="#e2f8ff" class="wl-lh-dot" />
                                <circle cx="110" cy="78" r="1.2" fill="white" class="wlh wlh7" />
                            </g>
                        </svg>
                    </div>
                    <div class="w-logo-row">
                        <span class="wl wl-1">D</span><span class="wl wl-2">D</span><span class="wl wl-3">A</span><span
                            class="wl wl-4">R</span><span class="wl wl-5">T</span>
                        <span class="wl-ai-slam">AI</span>
                    </div>
                    <p class="w-tagline">
                        <span class="w-tl w-tl-1">Ophthalmology</span>
                        <span class="w-tl w-tl-sep"> · </span>
                        <span class="w-tl w-tl-2">Artificial Intelligence</span>
                        <span class="w-tl w-tl-sep2"> · </span>
                        <span class="w-tl w-tl-3">Screening</span>
                    </p>
                    <div class="w-bar-wrap">
                        <div class="w-bar-fill"></div>
                    </div>
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
                    <div v-for="i in 8" :key="'h' + i" class="grid-h" :style="{ top: (i * 12) + '%' }"></div>
                    <div v-for="i in 8" :key="'v' + i" class="grid-v" :style="{ left: (i * 12) + '%' }"></div>
                </div>
                <div class="entry-content">
                    <div class="retinal-scanner">
                        <svg class="retina-svg" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="rgba(66,153,225,0.25)" />
                                    <stop offset="100%" stop-color="rgba(66,153,225,0)" />
                                </radialGradient>
                                <radialGradient id="beamGrad2" cx="50%" cy="50%" r="50%">
                                    <stop offset="0%" stop-color="rgba(99,179,237,0)" />
                                    <stop offset="70%" stop-color="rgba(99,179,237,0.08)" />
                                    <stop offset="100%" stop-color="rgba(99,179,237,0)" />
                                </radialGradient>
                                <linearGradient id="ringGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#63b3ed" />
                                    <stop offset="50%" stop-color="#4299e1" />
                                    <stop offset="100%" stop-color="#2b6cb0" />
                                </linearGradient>
                                <linearGradient id="ringGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stop-color="#e53e3e" />
                                    <stop offset="100%" stop-color="#fc8181" />
                                </linearGradient>
                                <filter id="glow">
                                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur" />
                                    <feMerge>
                                        <feMergeNode in="coloredBlur" />
                                        <feMergeNode in="SourceGraphic" />
                                    </feMerge>
                                </filter>
                                <filter id="glow-strong">
                                    <feGaussianBlur stdDeviation="4" result="coloredBlur" />
                                    <feMerge>
                                        <feMergeNode in="coloredBlur" />
                                        <feMergeNode in="SourceGraphic" />
                                    </feMerge>
                                </filter>
                            </defs>
                            <circle cx="150" cy="150" r="130" fill="url(#eyeGlow)" />
                            <circle cx="150" cy="150" r="138" stroke="rgba(99,179,237,0.06)" stroke-width="1" />
                            <circle cx="150" cy="150" r="138" stroke="url(#ringGrad1)" stroke-width="1.5"
                                stroke-dasharray="867" stroke-dashoffset="867" class="ring-draw" />
                            <circle cx="150" cy="150" r="120" stroke="rgba(99,179,237,0.35)" stroke-width="1"
                                stroke-dasharray="754" stroke-dashoffset="754" class="ring-draw-2" />
                            <circle cx="150" cy="150" r="98" stroke="rgba(99,179,237,0.08)" stroke-width="0.5"
                                stroke-dasharray="4 6" />
                            <circle cx="150" cy="150" r="75" stroke="rgba(99,179,237,0.06)" stroke-width="0.5"
                                stroke-dasharray="3 5" class="ring-spin" />
                            <circle cx="150" cy="150" r="55" stroke="rgba(99,179,237,0.08)" stroke-width="0.5" />
                            <line x1="150" y1="6" x2="150" y2="44" stroke="rgba(99,179,237,0.5)" stroke-width="1"
                                class="crosshair" filter="url(#glow)" />
                            <line x1="150" y1="256" x2="150" y2="294" stroke="rgba(99,179,237,0.5)" stroke-width="1"
                                class="crosshair" filter="url(#glow)" />
                            <line x1="6" y1="150" x2="44" y2="150" stroke="rgba(99,179,237,0.5)" stroke-width="1"
                                class="crosshair" filter="url(#glow)" />
                            <line x1="256" y1="150" x2="294" y2="150" stroke="rgba(99,179,237,0.5)" stroke-width="1"
                                class="crosshair" filter="url(#glow)" />
                            <line x1="118" y1="18" x2="128" y2="32" stroke="rgba(99,179,237,0.25)" stroke-width="0.8"
                                class="crosshair" />
                            <line x1="182" y1="18" x2="172" y2="32" stroke="rgba(99,179,237,0.25)" stroke-width="0.8"
                                class="crosshair" />
                            <line x1="118" y1="282" x2="128" y2="268" stroke="rgba(99,179,237,0.25)" stroke-width="0.8"
                                class="crosshair" />
                            <line x1="182" y1="282" x2="172" y2="268" stroke="rgba(99,179,237,0.25)" stroke-width="0.8"
                                class="crosshair" />
                            <circle cx="178" cy="132" r="16" fill="rgba(66,153,225,0.08)" stroke="rgba(99,179,237,0.4)"
                                stroke-width="1.5" filter="url(#glow)" class="disc-appear" />
                            <circle cx="178" cy="132" r="8" fill="rgba(99,179,237,0.18)" stroke="rgba(99,179,237,0.6)"
                                stroke-width="1" class="disc-appear" />
                            <circle cx="178" cy="132" r="3" fill="rgba(99,179,237,0.8)" class="disc-appear"
                                filter="url(#glow-strong)" />
                            <path d="M168 126 Q135 112 105 90" stroke="rgba(99,179,237,0.35)" stroke-width="1.8"
                                fill="none" class="vessel" filter="url(#glow)" />
                            <path d="M165 135 Q132 138 98 148" stroke="rgba(99,179,237,0.3)" stroke-width="1.5"
                                fill="none" class="vessel" />
                            <path d="M168 142 Q150 168 136 196" stroke="rgba(99,179,237,0.3)" stroke-width="1.5"
                                fill="none" class="vessel" />
                            <path d="M186 125 Q210 106 232 88" stroke="rgba(99,179,237,0.3)" stroke-width="1.5"
                                fill="none" class="vessel" />
                            <path d="M190 135 Q218 136 244 143" stroke="rgba(99,179,237,0.3)" stroke-width="1.5"
                                fill="none" class="vessel" />
                            <path d="M184 145 Q196 172 192 204" stroke="rgba(99,179,237,0.25)" stroke-width="1.2"
                                fill="none" class="vessel" />
                            <path d="M140 100 Q125 95 110 104" stroke="rgba(99,179,237,0.2)" stroke-width="1"
                                fill="none" class="vessel-2" />
                            <path d="M120 148 Q108 160 100 175" stroke="rgba(99,179,237,0.2)" stroke-width="1"
                                fill="none" class="vessel-2" />
                            <path d="M215 100 Q225 110 220 125" stroke="rgba(99,179,237,0.2)" stroke-width="1"
                                fill="none" class="vessel-2" />
                            <circle cx="124" cy="150" r="18" fill="none" stroke="url(#ringGrad2)" stroke-width="1.2"
                                stroke-dasharray="5 4" class="macula-appear" />
                            <circle cx="124" cy="150" r="10" fill="rgba(229,62,62,0.08)" stroke="rgba(229,62,62,0.4)"
                                stroke-width="1" class="macula-appear" />
                            <circle cx="124" cy="150" r="4" fill="rgba(229,62,62,0.6)" class="macula-appear"
                                filter="url(#glow)" />
                            <path d="M150 150 L288 150 A138 138 0 0 1 150 288 Z" fill="url(#beamGrad2)"
                                class="scanner-beam" />
                            <path d="M20 58 L20 20 L58 20" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none"
                                class="bracket" filter="url(#glow)" />
                            <path d="M242 20 L280 20 L280 58" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none"
                                class="bracket" filter="url(#glow)" />
                            <path d="M20 242 L20 280 L58 280" stroke="rgba(99,179,237,0.7)" stroke-width="2" fill="none"
                                class="bracket" filter="url(#glow)" />
                            <path d="M242 280 L280 280 L280 242" stroke="rgba(99,179,237,0.7)" stroke-width="2"
                                fill="none" class="bracket" filter="url(#glow)" />
                            <line x1="150" y1="12" x2="150" y2="20" stroke="rgba(99,179,237,0.4)" stroke-width="1"
                                class="tick" />
                            <line x1="150" y1="280" x2="150" y2="288" stroke="rgba(99,179,237,0.4)" stroke-width="1"
                                class="tick" />
                            <line x1="12" y1="150" x2="20" y2="150" stroke="rgba(99,179,237,0.4)" stroke-width="1"
                                class="tick" />
                            <line x1="280" y1="150" x2="288" y2="150" stroke="rgba(99,179,237,0.4)" stroke-width="1"
                                class="tick" />
                            <line x1="196" y1="116" x2="226" y2="96" stroke="rgba(99,179,237,0.4)" stroke-width="0.8"
                                class="readout-line" />
                            <line x1="226" y1="96" x2="256" y2="96" stroke="rgba(99,179,237,0.4)" stroke-width="0.8"
                                class="readout-line" />
                            <line x1="106" y1="132" x2="76" y2="112" stroke="rgba(229,62,62,0.4)" stroke-width="0.8"
                                class="readout-line" />
                            <line x1="76" y1="112" x2="46" y2="112" stroke="rgba(229,62,62,0.4)" stroke-width="0.8"
                                class="readout-line" />
                        </svg>
                        <div class="scan-line"></div>
                        <div class="glint glint-1"></div>
                        <div class="glint glint-2"></div>
                        <div class="glint glint-3"></div>
                        <div class="glint glint-4"></div>
                        <div class="readout readout-1">OD: 0.42</div>
                        <div class="readout readout-2">MAC: 0.18</div>
                        <div class="readout readout-3">AI ✓</div>
                    </div>
                    <div class="entry-logo">
                        <span class="entry-d entry-letter">D</span><span class="entry-d2 entry-letter">D</span><span
                            class="entry-a entry-letter">A</span><span class="entry-r entry-letter">R</span><span
                            class="entry-t entry-letter">T</span>
                        <span class="entry-ai">AI</span>
                    </div>
                    <div class="entry-tagline">
                        <span class="etl etl-1">Ophthalmology</span>
                        <span class="etl etl-sep1">&nbsp;·&nbsp;</span>
                        <span class="etl etl-2">Artificial Intelligence</span>
                        <span class="etl etl-sep2">&nbsp;·&nbsp;</span>
                        <span class="etl etl-3">Screening</span>
                    </div>
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
            <button :class="['role-btn', { active: role === 'health-center' }]"
                @click="roleDirection = role === 'doctor' ? -1 : 1; role = 'health-center'; error = ''">{{ t('Health Center', 'Κέντρο Υγείας') }}</button>
            <button :class="['role-btn', { active: role === 'doctor' }]"
                @click="roleDirection = role === 'health-center' ? 1 : -1; role = 'doctor'; error = ''">{{ t('Expert', 'Ειδικός Ιατρός') }}</button>
            <div class="role-indicator"
                :style="{ transform: role === 'health-center' ? 'translateX(0)' : 'translateX(100%)' }"></div>
        </div>

        <div class="main-card">
            <div class="card-inner">
                <div class="left-panel">
                    <transition :name="roleDirection > 0 ? 'panel-right' : 'panel-left'" mode="out-in">
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
                        <button :class="['tab', { active: mode === 'login' }]"
                            @click="modeDirection = -1; mode = 'login'; error = ''">{{ t('Sign In', 'Σύνδεση')
                            }}</button>
                        <button v-if="role === 'doctor'" :class="['tab', { active: mode === 'signup' }]"
                            @click="modeDirection = 1; mode = 'signup'; error = ''">{{ t('Sign Up', 'Εγγραφή')
                            }}</button>
                        <div class="tab-underline" :style="tabUnderlineStyle"></div>
                    </div>

                    <transition :name="modeDirection > 0 ? 'form-right' : 'form-left'" mode="out-in">

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
                                <span class="btn-text">{{ loading ? t('Signing in...', 'Σύνδεση...') : t('Sign In',
                                    'Σύνδεση') }}</span>
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
                                <span class="btn-text">{{ loading ? t('Signing in...', 'Σύνδεση...') : t('Sign In',
                                    'Σύνδεση') }}</span>
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
                <p>{{ t('For technical support please call', 'Για τεχνική υποστήριξη καλέστε') }} +3025510 30990 ({{
                    t('office hours', 'ώρες γραφείου') }})</p>
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
            roleDirection: 1,
            modeDirection: 1,
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
            setTimeout(() => { this.showWelcome = false }, 4500)
        }
        this.$nextTick(() => {
            const container = this.$refs.wParticles
            if (!container) return
            for (let i = 0; i < 28; i++) {
                const d = document.createElement('div')
                const seed = i * 137.508
                const x = (Math.sin(seed) * 0.5 + 0.5) * 100
                const y = (Math.cos(seed * 1.618) * 0.5 + 0.5) * 100
                const size = 1 + ((i * 7) % 4) * 0.6
                const dur = 5 + ((i * 3) % 6)
                const delay = ((i * 0.35) % 5)
                const op = 0.08 + ((i * 11) % 3) * 0.06
                d.style.cssText = `position:absolute;border-radius:50%;background:#63b3ed;left:${x}%;top:${y}%;width:${size}px;height:${size}px;opacity:${op};animation:particle-float ${dur}s ${delay}s ease-in-out infinite;transform:translate(-50%,-50%);box-shadow:0 0 4px rgba(99,179,237,0.5)`
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
    overflow-x: hidden;
}

/* ── Base container ── */
.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 20px 0;
    min-height: 100vh;
    width: 100%;
    background: #f0f4f8;
    transition: background 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Welcome overlay ── */
.entry-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: radial-gradient(ellipse at 50% 40%, #0a1628 0%, #04080f 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

/* ── Welcome overlay — perfected lighthouse animation ── */
.welcome-overlay {
    position: fixed;
    inset: 0;
    z-index: 10000;
    background: radial-gradient(ellipse at 50% 45%, #07142a 0%, #020912 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    cursor: pointer;
}

.welcome-particles {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.welcome-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 22px;
    position: relative;
    z-index: 2;
}

/* Logo container — gentle float-in */
.wl-center-logo {
    opacity: 0;
    animation: wLogoAppear 0.9s 0.05s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    filter: drop-shadow(0 0 32px rgba(43, 108, 176, 0.45));
}

.wl-center-svg {
    width: 220px;
    height: 220px;
}

@keyframes wLogoAppear {
    from {
        opacity: 0;
        transform: scale(0.72) translateY(16px);
    }

    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

/* Arcs spin clockwise — outer slower, inner faster */
.wl-arc-outer-g {
    transform-origin: 110px 110px;
    animation: wSpin 8s linear infinite;
}

.wl-arc-inner-g {
    transform-origin: 110px 110px;
    animation: wSpin 4.8s linear infinite;
}

@keyframes wSpin {
    to {
        transform: rotate(360deg);
    }
}

/* Arc draw-in — starts slow, accelerates */
.wl-arc-outer {
    stroke-dasharray: 659;
    stroke-dashoffset: 659;
    animation: wArcDraw 0.95s 0.08s cubic-bezier(0.22, 0, 0.58, 1) forwards;
}

.wl-arc-inner {
    stroke-dasharray: 497;
    stroke-dashoffset: 497;
    animation: wArcDraw 0.8s 0.32s cubic-bezier(0.22, 0, 0.58, 1) forwards;
}

@keyframes wArcDraw {
    to {
        stroke-dashoffset: 0;
    }
}

/* Subtle ring pulse */
.wl-ring-pulse {
    animation: wRingPulse 3.5s 1.5s ease-in-out infinite;
}

@keyframes wRingPulse {

    0%,
    100% {
        opacity: .03;
    }

    50% {
        opacity: .09;
    }
}

/* Lighthouse parts — cascade with spring easing, bottom to top */
.wl-lh-g {
    opacity: 0;
    animation: wFadeSnap 0.01s 0.95s forwards;
}

@keyframes wFadeSnap {
    to {
        opacity: 1;
    }
}

.wlh {
    opacity: 0;
    transform-box: fill-box;
    transform-origin: center bottom;
}

.wlh1 {
    animation: wlhRise 0.38s 1.0s cubic-bezier(0.34, 1.5, 0.64, 1) forwards;
}

.wlh2 {
    animation: wlhRise 0.36s 1.18s cubic-bezier(0.34, 1.5, 0.64, 1) forwards;
}

.wlh3 {
    animation: wlhRise 0.32s 1.34s cubic-bezier(0.34, 1.5, 0.64, 1) forwards;
}

.wlh4 {
    animation: wlhRise 0.3s 1.48s cubic-bezier(0.34, 1.5, 0.64, 1) forwards;
}

.wlh5 {
    animation: wlhRise 0.28s 1.6s cubic-bezier(0.34, 1.5, 0.64, 1) forwards;
}

.wlh6 {
    animation: wlhRise 0.26s 1.7s cubic-bezier(0.34, 1.5, 0.64, 1) forwards;
}

.wlh7 {
    animation: wlhRise 0.24s 1.78s cubic-bezier(0.34, 1.5, 0.64, 1) forwards;
}

@keyframes wlhRise {
    from {
        opacity: 0;
        transform: scaleY(0);
    }

    to {
        opacity: 1;
        transform: scaleY(1);
    }
}

/* Beacon beam rotates with eased start */
.wl-beacon-beam {
    transform-origin: 110px 78px;
    animation: wBeaconSpin 2.6s 2.0s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

.wl-beacon-on {
    opacity: 0;
    animation: wBOn 0.6s 2.0s ease forwards;
}

@keyframes wBeaconSpin {
    to {
        transform: rotate(360deg);
    }
}

@keyframes wBOn {
    to {
        opacity: 1;
    }
}

/* Glow breathes */
.wl-lh-glow {
    opacity: 0;
    animation: wGlowBreathe 2.6s 2.0s ease-in-out infinite;
}

@keyframes wGlowBreathe {
    0% {
        opacity: 0;
    }

    20% {
        opacity: .35;
    }

    50% {
        opacity: .9;
    }

    80% {
        opacity: .35;
    }

    100% {
        opacity: 0;
    }
}

/* Light dot pulses */
.wl-lh-dot {
    animation: wDotPulse 2.6s 2.0s ease-in-out infinite;
    opacity: 0;
}

@keyframes wDotPulse {

    0%,
    100% {
        opacity: .4;
    }

    50% {
        opacity: 1;
    }
}

/* DDART letters — gentle float with slight overshoot */
.w-logo-row {
    display: flex;
    align-items: baseline;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-weight: 900;
    letter-spacing: 7px;
}

.wl {
    color: white;
    font-size: 24px;
    opacity: 0;
    display: inline-block;
}

.wl-1 {
    animation: wFloat 0.4s 2.05s cubic-bezier(0.34, 1.4, 0.64, 1) forwards;
}

.wl-2 {
    animation: wFloat 0.4s 2.14s cubic-bezier(0.34, 1.4, 0.64, 1) forwards;
}

.wl-3 {
    animation: wFloat 0.4s 2.23s cubic-bezier(0.34, 1.4, 0.64, 1) forwards;
}

.wl-4 {
    animation: wFloat 0.4s 2.32s cubic-bezier(0.34, 1.4, 0.64, 1) forwards;
}

.wl-5 {
    animation: wFloat 0.4s 2.41s cubic-bezier(0.34, 1.4, 0.64, 1) forwards;
}

@keyframes wFloat {
    from {
        opacity: 0;
        transform: translateY(-22px) scale(0.7);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* AI — dramatic bloom: scales from 4.5x with blur, elastic settle */
.wl-ai-slam {
    color: #e53e3e;
    font-size: 76px;
    font-family: 'Arial Black', Arial, sans-serif;
    font-weight: 900;
    line-height: 1;
    opacity: 0;
    margin-left: 10px;
    animation: wAiBloom 0.7s 2.54s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes wAiBloom {
    0% {
        opacity: 0;
        transform: scale(4.5) translateY(-8px);
        filter: blur(18px);
    }

    40% {
        opacity: 1;
        filter: blur(0);
    }

    70% {
        transform: scale(0.95);
    }

    88% {
        transform: scale(1.02);
    }

    100% {
        opacity: 1;
        transform: scale(1);
        filter: blur(0);
    }
}

/* Tagline words drift up with stagger */
.w-tagline {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 3.5px;
    color: rgba(99, 179, 237, 0.42);
    text-transform: uppercase;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    justify-content: center;
}

.w-tl {
    opacity: 0;
    display: inline-block;
}

.w-tl-1 {
    animation: wTlRise 0.45s 2.82s cubic-bezier(0.34, 1.3, 0.64, 1) forwards;
}

.w-tl-sep {
    animation: wTlRise 0.3s 2.98s ease forwards;
}

.w-tl-2 {
    animation: wTlRise 0.45s 3.06s cubic-bezier(0.34, 1.3, 0.64, 1) forwards;
}

.w-tl-sep2 {
    animation: wTlRise 0.3s 3.24s ease forwards;
}

.w-tl-3 {
    animation: wTlRise 0.45s 3.32s cubic-bezier(0.34, 1.3, 0.64, 1) forwards;
}

@keyframes wTlRise {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Progress bar */
.w-bar-wrap {
    width: 200px;
    height: 1px;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 1px;
    overflow: hidden;
    opacity: 0;
    animation: wFade 0.3s 3.5s ease forwards;
}

.w-bar-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #1e4d8c, #4299e1, #90cdf4);
    animation: wBarGrow 0.65s 3.52s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes wBarGrow {
    to {
        width: 100%;
    }
}

@keyframes wFade {
    to {
        opacity: 1;
    }
}

.welcome-fade-enter-active {
    transition: opacity 0.4s ease;
}

.welcome-fade-leave-active {
    transition: opacity 0.8s ease, transform 0.8s ease, filter 0.8s ease;
}

.welcome-fade-enter-from {
    opacity: 0;
}

.welcome-fade-leave-to {
    opacity: 0;
    transform: scale(1.04);
    filter: blur(6px);
}

/* ── Entry overlay internals ── */
.grid-lines {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.grid-h {
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background: rgba(99, 179, 237, 0.04);
    animation: grid-fade-in 1s ease both;
}

.grid-v {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 1px;
    background: rgba(99, 179, 237, 0.04);
    animation: grid-fade-in 1s ease both;
}

@keyframes grid-fade-in {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

.particle-field {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.particle {
    position: absolute;
    background: #63b3ed;
    border-radius: 50%;
    animation: particle-float linear infinite;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 4px rgba(99, 179, 237, 0.6);
}

@keyframes particle-float {

    0%,
    100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.15;
    }

    50% {
        transform: translate(-50%, -60%) scale(1.4);
        opacity: 0.5;
    }
}

.entry-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    position: relative;
    z-index: 2;
}

.retinal-scanner {
    position: relative;
    width: 300px;
    height: 300px;
    animation: scanner-appear 0.8s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes scanner-appear {
    from {
        opacity: 0;
        transform: scale(0.7) rotate(-8deg);
    }

    to {
        opacity: 1;
        transform: scale(1) rotate(0deg);
    }
}

.retina-svg {
    width: 100%;
    height: 100%;
}

.ring-draw {
    animation: ring-draw 2s 0.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes ring-draw {
    from {
        stroke-dashoffset: 867;
    }

    to {
        stroke-dashoffset: 0;
    }
}

.ring-draw-2 {
    animation: ring-draw-2 1.6s 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes ring-draw-2 {
    from {
        stroke-dashoffset: 754;
    }

    to {
        stroke-dashoffset: 0;
    }
}

.ring-spin {
    animation: ring-spin 12s linear infinite;
    transform-origin: 150px 150px;
}

@keyframes ring-spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.crosshair {
    opacity: 0;
    animation: elem-appear 0.5s 1.2s ease forwards;
}

.tick {
    opacity: 0;
    animation: elem-appear 0.4s 1.4s ease forwards;
}

@keyframes elem-appear {
    to {
        opacity: 1;
    }
}

.vessel {
    stroke-dasharray: 300;
    stroke-dashoffset: 300;
    animation: vessel-draw 1.2s 0.9s ease forwards;
}

.vessel-2 {
    stroke-dasharray: 200;
    stroke-dashoffset: 200;
    animation: vessel-draw 1s 1.3s ease forwards;
}

@keyframes vessel-draw {
    to {
        stroke-dashoffset: 0;
    }
}

.disc-appear {
    opacity: 0;
    animation: disc-pop 0.6s 1.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.macula-appear {
    opacity: 0;
    animation: disc-pop 0.6s 1.7s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes disc-pop {
    from {
        opacity: 0;
        transform: scale(0);
        transform-box: fill-box;
        transform-origin: center;
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

.readout-line {
    stroke-dasharray: 60;
    stroke-dashoffset: 60;
    animation: vessel-draw 0.6s 1.9s ease forwards;
}

.scanner-beam {
    transform-origin: 150px 150px;
    animation: scan-rotate 3s linear infinite;
}

@keyframes scan-rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.bracket {
    opacity: 0;
    animation: bracket-slide 0.5s 0.1s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

@keyframes bracket-slide {
    from {
        opacity: 0;
        stroke-dashoffset: 80;
    }

    to {
        opacity: 1;
        stroke-dashoffset: 0;
    }
}

.scan-line {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(99, 179, 237, 0) 15%, rgba(99, 179, 237, 0.8) 50%, rgba(99, 179, 237, 0) 85%, transparent);
    animation: scan-sweep 2.5s ease-in-out infinite;
    filter: blur(0.5px);
}

@keyframes scan-sweep {
    0% {
        top: 8%;
        opacity: 0;
    }

    8% {
        opacity: 1;
    }

    92% {
        opacity: 1;
    }

    100% {
        top: 92%;
        opacity: 0;
    }
}

.glint {
    position: absolute;
    border-radius: 50%;
    background: #63b3ed;
    animation: glint-pulse 2.2s ease-in-out infinite;
    box-shadow: 0 0 8px 2px rgba(99, 179, 237, 0.8);
}

.glint-1 {
    width: 5px;
    height: 5px;
    top: 4px;
    left: calc(50% - 2px);
    animation-delay: 0s;
}

.glint-2 {
    width: 4px;
    height: 4px;
    top: calc(50% - 2px);
    right: 4px;
    animation-delay: 0.75s;
}

.glint-3 {
    width: 5px;
    height: 5px;
    bottom: 4px;
    left: calc(50% - 2px);
    animation-delay: 1.5s;
}

.glint-4 {
    width: 4px;
    height: 4px;
    top: calc(50% - 2px);
    left: 4px;
    animation-delay: 0.37s;
}

@keyframes glint-pulse {

    0%,
    100% {
        opacity: 0.2;
        transform: scale(0.8);
    }

    50% {
        opacity: 1;
        transform: scale(1.8);
    }
}

.readout {
    position: absolute;
    font-family: 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    opacity: 0;
    animation: elem-appear 0.4s ease forwards;
}

.readout-1 {
    top: 26%;
    right: 2%;
    color: rgba(99, 179, 237, 0.8);
    animation-delay: 2s;
}

.readout-2 {
    top: 36%;
    left: 1%;
    color: rgba(229, 62, 62, 0.8);
    animation-delay: 2.1s;
}

.readout-3 {
    bottom: 28%;
    right: 4%;
    color: rgba(72, 187, 120, 0.9);
    animation-delay: 2.2s;
    font-size: 11px;
}

.entry-logo {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 6px;
    display: flex;
    align-items: baseline;
    gap: 0;
}

.entry-letter {
    color: white;
    opacity: 0;
    display: inline-block;
    animation: letter-drop 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    text-shadow: 0 0 16px rgba(99, 179, 237, 0.4);
}

.entry-d {
    animation-delay: 1.6s;
}

.entry-d2 {
    animation-delay: 1.72s;
}

.entry-a {
    animation-delay: 1.84s;
}

.entry-r {
    animation-delay: 1.96s;
}

.entry-t {
    animation-delay: 2.08s;
}

.entry-ai {
    color: #e53e3e;
    font-size: 80px;
    font-weight: 900;
    font-family: 'Arial Black', Arial, sans-serif;
    line-height: 1;
    opacity: 0;
    margin-left: 8px;
    animation: ai-slam 0.6s 2.22s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    text-shadow: 0 0 40px rgba(229, 62, 62, 0.6);
}

@keyframes letter-drop {
    from {
        opacity: 0;
        transform: translateY(-20px) scale(0.75);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes ai-slam {
    from {
        opacity: 0;
        transform: scale(3.5);
        filter: blur(12px);
    }

    60% {
        opacity: 1;
        filter: blur(0);
    }

    80% {
        transform: scale(0.96);
    }

    to {
        opacity: 1;
        transform: scale(1);
        filter: blur(0);
    }
}

.entry-tagline {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 3px;
    color: rgba(99, 179, 237, 0.5);
    text-transform: uppercase;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0;
    margin-top: -8px;
}

.etl {
    opacity: 0;
    display: inline-block;
}

.etl-1 {
    animation: etlIn 0.4s 2.9s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.etl-sep1 {
    animation: etlIn 0.3s 3.06s ease forwards;
}

.etl-2 {
    animation: etlIn 0.4s 3.14s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.etl-sep2 {
    animation: etlIn 0.3s 3.32s ease forwards;
}

.etl-3 {
    animation: etlIn 0.4s 3.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes etlIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.entry-bar {
    width: 260px;
    height: 2px;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 2px;
    overflow: visible;
    position: relative;
    opacity: 0;
    animation: elem-appear 0.4s 1s ease forwards;
}

.entry-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #2b6cb0, #63b3ed, #90cdf4);
    border-radius: 2px;
    transition: width 0.05s linear;
    position: relative;
}

.entry-bar-glow {
    position: absolute;
    top: -3px;
    width: 12px;
    height: 8px;
    background: rgba(99, 179, 237, 0.9);
    border-radius: 50%;
    filter: blur(3px);
    transform: translateX(-50%);
    transition: left 0.05s linear;
}

.entry-msg {
    color: rgba(255, 255, 255, 0.45);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0;
    opacity: 0;
    animation: elem-appear 0.5s 1.1s ease forwards;
}

.overlay-fade-leave-active {
    transition: opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1), filter 0.6s ease;
}

.overlay-fade-leave-to {
    opacity: 0;
    transform: scale(1.06);
    filter: blur(4px);
}

/* ══════════════════════════════════════
   HEADER
══════════════════════════════════════ */
.header-controls {
    position: absolute;
    top: 20px;
    right: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.lang-toggle {
    display: flex;
    align-items: center;
    gap: 2px;
}

.lang-btn {
    background: none;
    border: none;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #b0bac8;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    letter-spacing: 0.5px;
    transition: color 0.2s cubic-bezier(0.4, 0, 0.2, 1), background 0.2s cubic-bezier(0.4, 0, 0.2, 1), transform 0.18s cubic-bezier(0.34, 1.5, 0.64, 1);
}

.lang-btn.active {
    color: #2b6cb0;
    background: #ebf8ff;
}

.lang-btn:hover:not(.active) {
    color: #4a5568;
    background: #f0f4f8;
    transform: translateY(-1px);
}

.lang-btn:active {
    transform: scale(0.9) translateY(0);
}

.lang-sep {
    color: #e2e8f0;
    font-size: 12px;
    user-select: none;
}

.dark-btn {
    background: none;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #718096;
    cursor: pointer;
    padding: 4px 13px;
    letter-spacing: 0.4px;
    transition: background 0.22s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.22s cubic-bezier(0.4, 0, 0.2, 1), color 0.22s cubic-bezier(0.4, 0, 0.2, 1), transform 0.18s cubic-bezier(0.34, 1.5, 0.64, 1), box-shadow 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

.dark-btn:hover {
    background: #f0f4f8;
    border-color: #c8d0dc;
    color: #4a5568;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.07);
}

.dark-btn:active {
    transform: scale(0.94) translateY(0);
    transition-duration: 0.08s;
}

.header {
    text-align: center;
    margin-bottom: 20px;
    width: 100%;
    position: relative;
}

.header-text {
    transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.university {
    font-size: 14px;
    color: #2c5282;
    font-weight: 600;
    margin: 0 0 4px;
    transition: color 0.45s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ══════════════════════════════════════
   ROLE TOGGLE — animated sliding pill
══════════════════════════════════════ */
.role-toggle {
    position: relative;
    display: flex;
    gap: 0;
    margin-bottom: 20px;
    background: white;
    border: 1px solid #e8edf3;
    border-radius: 10px;
    padding: 4px;
    width: 100%;
    max-width: 760px;
    transition: background 0.45s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.45s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
    overflow: hidden;
}

/* Pill glides with a custom spring — fast start, gentle settle */
.role-indicator {
    position: absolute;
    top: 4px;
    left: 4px;
    width: calc(50% - 4px);
    height: calc(100% - 8px);
    background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
    border-radius: 7px;
    transition: transform 0.48s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
    pointer-events: none;
    box-shadow: 0 3px 12px rgba(43, 108, 176, 0.3), 0 1px 3px rgba(43, 108, 176, 0.2);
}

.role-btn {
    flex: 1;
    padding: 9px 16px;
    border: none;
    border-radius: 7px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #8a9ab0;
    cursor: pointer;
    background: none;
    white-space: nowrap;
    position: relative;
    z-index: 1;
    transition: color 0.38s cubic-bezier(0.16, 1, 0.3, 1), transform 0.16s cubic-bezier(0.34, 1.5, 0.64, 1);
}

.role-btn.active {
    color: white;
}

.role-btn:hover:not(.active) {
    color: #4a5568;
}

.role-btn:active {
    transform: scale(0.96);
    transition-duration: 0.08s;
}

/* ══════════════════════════════════════
   MAIN CARD — elevates on hover
══════════════════════════════════════ */
.main-card {
    background: white;
    border: 1px solid #e8edf3;
    border-radius: 12px;
    width: 100%;
    max-width: 760px;
    margin-bottom: 24px;
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06), 0 1px 4px rgba(0, 0, 0, 0.04);
    transition: background 0.45s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.45s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
}

.main-card:hover {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.09), 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card-inner {
    display: grid;
    grid-template-columns: 260px 1fr;
    min-height: 360px;
}

.left-panel {
    background: linear-gradient(160deg, #2b6cb0 0%, #1e4f8a 100%);
    display: flex;
    align-items: center;
    padding: 32px 28px;
    overflow: hidden;
    transition: background 0.45s cubic-bezier(0.4, 0, 0.2, 1);
}

.left-content h2 {
    font-family: 'Playfair Display', serif;
    color: white;
    font-size: 20px;
    margin: 0 0 10px;
}

.left-content p {
    color: rgba(255, 255, 255, 0.82);
    font-size: 13px;
    line-height: 1.75;
    margin: 0;
}

.right-panel {
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    overflow: hidden;
}

/* ══════════════════════════════════════
   TABS — sliding underline (spring)
══════════════════════════════════════ */
.tabs {
    position: relative;
    display: flex;
    border-bottom: 1px solid #e8edf3;
    gap: 0;
    transition: border-color 0.45s ease;
}

.tab {
    flex: 1;
    padding: 11px 20px;
    border: none;
    background: none;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #b0bac8;
    cursor: pointer;
    position: relative;
    transition: color 0.22s cubic-bezier(0.4, 0, 0.2, 1), transform 0.16s cubic-bezier(0.34, 1.5, 0.64, 1);
}

.tab.active {
    color: #2b6cb0;
}

.tab:hover:not(.active) {
    color: #718096;
}

.tab:active {
    transform: scale(0.96);
    transition-duration: 0.08s;
}

/* Underline glides with a spring */
.tab-underline {
    position: absolute;
    bottom: -1px;
    height: 2.5px;
    background: linear-gradient(90deg, #2b6cb0, #4299e1);
    border-radius: 2px 2px 0 0;
    transition: transform 0.42s cubic-bezier(0.16, 1, 0.3, 1), width 0.42s cubic-bezier(0.16, 1, 0.3, 1);
}

/* ══════════════════════════════════════
   FORM FIELDS — animated underline
══════════════════════════════════════ */
.form {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.field label {
    font-size: 10.5px;
    font-weight: 700;
    color: #b0bac8;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    transition: color 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

.field.focused label {
    color: #2b6cb0;
}

.input-wrap {
    position: relative;
}

.field input {
    padding: 10px 0 8px;
    border: none;
    border-bottom: 1.5px solid #e8edf3;
    border-radius: 0;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    color: #2d3748;
    outline: none;
    width: 100%;
    background: transparent;
    transition: border-color 0.22s cubic-bezier(0.4, 0, 0.2, 1), color 0.4s ease;
}

.field input::placeholder {
    color: #c8d0dc;
    transition: color 0.22s ease, opacity 0.22s ease;
}

.field.focused input::placeholder {
    color: #a8b4c4;
    opacity: 0.7;
}

/* Underline grows from left — clean, no offset */
.input-line {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, #2b6cb0, #4299e1);
    border-radius: 2px;
    transform: scaleX(0);
    transform-origin: left center;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.field.focused .input-line {
    transform: scaleX(1);
}

.hint {
    font-size: 11px;
    color: #a0aec0;
}

.gdpr-note,
.access-note {
    font-size: 11px;
    color: #718096;
    line-height: 1.65;
    background: #f8fafc;
    border: 1px solid #e8edf3;
    border-radius: 7px;
    padding: 9px 12px;
    margin: 0;
    transition: background 0.45s ease, border-color 0.45s ease, color 0.45s ease;
}

/* ══════════════════════════════════════
   SUBMIT BUTTON — shimmer + spring lift
══════════════════════════════════════ */
.submit-btn {
    position: relative;
    overflow: hidden;
    padding: 13px;
    background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    margin-top: 4px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    letter-spacing: 0.3px;
    transition: background 0.3s ease, transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Shimmer sweep */
.submit-btn .btn-bg {
    position: absolute;
    inset: 0;
    background: linear-gradient(105deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.14) 45%, rgba(255, 255, 255, 0.14) 55%, rgba(255, 255, 255, 0) 100%);
    transform: translateX(-110%);
    transition: transform 0.65s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
}

.submit-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #2558a0 0%, #2b75c0 100%);
    box-shadow: 0 8px 24px rgba(43, 108, 176, 0.38), 0 3px 8px rgba(43, 108, 176, 0.2);
    transform: translateY(-2px);
}

.submit-btn:hover:not(:disabled) .btn-bg {
    transform: translateX(110%);
}

.submit-btn:active:not(:disabled) {
    transform: translateY(1px) scale(0.985);
    box-shadow: 0 2px 8px rgba(43, 108, 176, 0.2);
    transition: transform 0.09s ease, box-shadow 0.09s ease;
}

.submit-btn:disabled {
    opacity: 0.42;
    cursor: not-allowed;
}

.btn-text {
    position: relative;
    z-index: 1;
}

.btn-spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.65s linear infinite;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.error {
    color: #c53030;
    font-size: 13px;
    font-weight: 600;
    margin: 0;
}

/* ══════════════════════════════════════
   STUDY OFFICIAL BUTTON
══════════════════════════════════════ */
.study-official-btn {
    position: absolute;
    top: 0;
    left: 0;
    background: none;
    border: 1px solid #e8edf3;
    border-radius: 20px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #8a9ab0;
    cursor: pointer;
    padding: 5px 14px;
    letter-spacing: 0.3px;
    transition: color 0.22s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.22s cubic-bezier(0.4, 0, 0.2, 1), background 0.22s cubic-bezier(0.4, 0, 0.2, 1), transform 0.18s cubic-bezier(0.34, 1.5, 0.64, 1), box-shadow 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

.study-official-btn:hover {
    color: #2b6cb0;
    border-color: #93c5fd;
    background: #eff8ff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(43, 108, 176, 0.12);
}

.study-official-btn:active {
    transform: scale(0.94) translateY(0);
    transition-duration: 0.08s;
}

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
.footer {
    width: 100%;
    max-width: 760px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0 24px;
    border-top: 1px solid #e8edf3;
    margin-top: auto;
    gap: 16px;
    transition: border-color 0.45s ease;
}

.dept-logo {
    height: 50px;
    width: auto;
    object-fit: contain;
    transition: opacity 0.2s ease;
}

.dept-logo:hover {
    opacity: 0.8;
}

.footer-right {
    text-align: right;
}

.footer-right p {
    font-size: 12px;
    color: #8a9ab0;
    margin: 2px 0;
    transition: color 0.45s ease;
}

.footer-right a {
    color: #2b6cb0;
    text-decoration: none;
    transition: color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.footer-right a:hover {
    color: #1e4f8a;
}

.made-by {
    font-size: 10px;
    color: #c8d0dc;
    margin-top: 4px;
}

/* ══════════════════════════════════════
   TRANSITIONS — direction-aware springs
══════════════════════════════════════ */

/* Panel (left blue side) — vertical cross-fade */
.panel-right-enter-active,
.panel-left-enter-active {
    transition: opacity 0.42s cubic-bezier(0.16, 1, 0.3, 1), transform 0.42s cubic-bezier(0.16, 1, 0.3, 1);
}

.panel-right-leave-active,
.panel-left-leave-active {
    transition: opacity 0.18s cubic-bezier(0.4, 0, 1, 1), transform 0.18s cubic-bezier(0.4, 0, 1, 1);
}

/* Going right (HC→Expert): new slides up, old slides down */
.panel-right-enter-from {
    opacity: 0;
    transform: translateY(18px);
}

.panel-right-leave-to {
    opacity: 0;
    transform: translateY(-14px);
}

/* Going left (Expert→HC): new slides down, old slides up */
.panel-left-enter-from {
    opacity: 0;
    transform: translateY(-18px);
}

.panel-left-leave-to {
    opacity: 0;
    transform: translateY(14px);
}

/* Form (right side) — horizontal direction-aware slide */
.form-right-enter-active,
.form-left-enter-active {
    transition: opacity 0.36s cubic-bezier(0.16, 1, 0.3, 1), transform 0.36s cubic-bezier(0.16, 1, 0.3, 1);
}

.form-right-leave-active,
.form-left-leave-active {
    transition: opacity 0.15s cubic-bezier(0.4, 0, 1, 1), transform 0.15s cubic-bezier(0.4, 0, 1, 1);
}

/* Going right (login→signup, HC→Expert): new from right, old to left */
.form-right-enter-from {
    opacity: 0;
    transform: translateX(20px);
}

.form-right-leave-to {
    opacity: 0;
    transform: translateX(-16px);
}

/* Going left (signup→login, Expert→HC): new from left, old to right */
.form-left-enter-from {
    opacity: 0;
    transform: translateX(-20px);
}

.form-left-leave-to {
    opacity: 0;
    transform: translateX(16px);
}

/* Header lang fade */
.header-fade-enter-active {
    transition: opacity 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

.header-fade-leave-active {
    transition: opacity 0.14s cubic-bezier(0.4, 0, 1, 1);
}

.header-fade-enter-from,
.header-fade-leave-to {
    opacity: 0;
}

/* Error: springs in from above */
.error-pop-enter-active {
    transition: opacity 0.28s cubic-bezier(0.16, 1, 0.3, 1), transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}

.error-pop-leave-active {
    transition: opacity 0.16s cubic-bezier(0.4, 0, 1, 1), transform 0.16s ease;
}

.error-pop-enter-from {
    opacity: 0;
    transform: translateY(-8px) scale(0.95);
}

.error-pop-leave-to {
    opacity: 0;
    transform: translateY(-4px) scale(0.97);
}

/* ══════════════════════════════════════
   DARK MODE
══════════════════════════════════════ */
.dark.login-container {
    background: #131b2e;
}

.dark .university {
    color: #90cdf4;
}

.dark .role-toggle {
    background: #1e2d45;
    border-color: #2d4060;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
}

.dark .role-indicator {
    background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
    box-shadow: 0 3px 12px rgba(99, 179, 237, 0.25);
}

.dark .role-btn {
    color: #6b8aaa;
}

.dark .role-btn:hover:not(.active) {
    color: #c8d8e8;
}

.dark .main-card {
    background: #1a2540;
    border-color: #2a3a58;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}

.dark .main-card:hover {
    box-shadow: 0 8px 36px rgba(0, 0, 0, 0.38);
}

.dark .left-panel {
    background: linear-gradient(160deg, #1e4078 0%, #142d5a 100%);
}

.dark .right-panel {
    background: #1a2540;
}

.dark .tabs {
    border-bottom-color: #2a3a58;
}

.dark .tab {
    color: #4a6080;
}

.dark .tab.active {
    color: #63b3ed;
}

.dark .tab-underline {
    background: linear-gradient(90deg, #4299e1, #63b3ed);
}

.dark .field label {
    color: #4a6080;
}

.dark .field.focused label {
    color: #63b3ed;
}

.dark .field input {
    border-bottom-color: #2a3a58;
    color: #d8e4f0;
}

.dark .field input::placeholder {
    color: #2a3a58;
}

.dark .input-line {
    background: linear-gradient(90deg, #4299e1, #63b3ed);
}

.dark .gdpr-note,
.dark .access-note {
    background: #0f1a2e;
    border-color: #2a3a58;
    color: #6b8aaa;
}

.dark .submit-btn {
    background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
}

.dark .submit-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #2558a0 0%, #2b75c0 100%);
    box-shadow: 0 8px 24px rgba(99, 179, 237, 0.28);
}

.dark .lang-btn.active {
    color: #63b3ed;
    background: rgba(99, 179, 237, 0.12);
}

.dark .lang-btn:hover:not(.active) {
    color: #c8d8e8;
    background: rgba(255, 255, 255, 0.06);
}

.dark .lang-sep {
    color: #2a3a58;
}

.dark .dark-btn {
    border-color: #2a3a58;
    color: #6b8aaa;
}

.dark .dark-btn:hover {
    background: #1e2d45;
    border-color: #3a5080;
    color: #c8d8e8;
}

.dark .footer {
    border-top-color: #2a3a58;
}

.dark .footer-right p {
    color: #4a6080;
}

.dark .footer-right a {
    color: #63b3ed;
}

.dark .study-official-btn {
    border-color: #2a3a58;
    color: #4a6080;
}

.dark .study-official-btn:hover {
    color: #63b3ed;
    border-color: #4a7aaa;
    background: rgba(99, 179, 237, 0.08);
    box-shadow: 0 4px 12px rgba(99, 179, 237, 0.1);
}

/* ══════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════ */
@keyframes particle-float {

    0%,
    100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.12;
    }

    50% {
        transform: translate(-50%, -65%) scale(1.5);
        opacity: 0.45;
    }
}

@media (max-width: 768px) {
    .login-container {
        padding: 20px 16px 0;
    }

    .header-controls {
        top: 12px;
        right: 12px;
    }

    .university {
        font-size: 12px;
    }

    .role-toggle {
        max-width: 100%;
    }

    .role-btn {
        font-size: 12px;
        padding: 8px 10px;
    }

    .card-inner {
        grid-template-columns: 1fr;
        min-height: unset;
    }

    .left-panel {
        padding: 20px;
        align-items: flex-start;
    }

    .left-content h2 {
        font-size: 18px;
    }

    .left-content p {
        font-size: 12px;
        margin-bottom: 10px;
    }

    .right-panel {
        padding: 20px;
    }

    .footer {
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 12px;
    }

    .footer-right {
        text-align: center;
    }

    .dept-logo {
        height: 40px;
    }

    .entry-ai {
        font-size: 64px;
    }
}

@media (max-width: 480px) {
    .login-container {
        padding: 16px 12px 0;
    }

    .university {
        font-size: 11px;
    }

    .tab {
        padding: 8px 12px;
        font-size: 13px;
    }

    .right-panel {
        padding: 16px;
    }

    .header-controls {
        gap: 8px;
    }

    .entry-bar {
        width: 200px;
    }

    .entry-ai {
        font-size: 56px;
    }
}
</style>