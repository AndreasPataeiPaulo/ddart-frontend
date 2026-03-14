<template>
    <div class="research-container">


        <!-- Fullscreen zoom overlay -->
        <transition name="zoom-fade">
            <div v-if="zoomSrc" class="zoom-backdrop" @click.self="closeZoom">
                <div class="zoom-toolbar">
                    <button class="zoom-btn" @click="zoomIn">＋</button>
                    <span class="zoom-pct">{{ Math.round(zoomLevel * 100) }}%</span>
                    <button class="zoom-btn" @click="zoomOut">－</button>
                    <button class="zoom-btn" @click="resetZoom" title="Reset">⊙</button>
                    <button class="zoom-btn zoom-close" @click="closeZoom">✕</button>
                </div>
                <div class="zoom-img-wrap"
                    @mousedown.prevent="startPan"
                    @mousemove.prevent="doPan"
                    @mouseup="endPan"
                    @mouseleave="endPan"
                    @wheel.prevent="onWheel"
                    :style="{ cursor: isPanning ? 'grabbing' : (zoomLevel > 1 ? 'grab' : 'zoom-in') }">
                    <img :src="zoomSrc" class="zoom-img"
                        :style="{ transform: 'translate(' + panX + 'px, ' + panY + 'px) scale(' + zoomLevel + ')', transformOrigin: zoomOrigin }"
                        draggable="false" />
                </div>
                <p class="zoom-hint">Scroll to zoom · Drag to pan · Click outside to close</p>
            </div>
        </transition>

        <!-- Expertise modal — shown on first login only -->
        <transition name="modal-fade">
            <div v-if="showExpertiseModal" class="modal-backdrop">
                <div class="modal-box">
                    <img src="/DDART.png" style="height:30px;width:auto;object-fit:contain;" />
                    <h3>Welcome, Dr. {{ doctorName }}</h3>
                    <p>Before you begin, please select your area of expertise.</p>
                    <p style="font-size:12px;color:#718096;margin:-4px 0 8px;">Select one specialty — you will only grade images for this condition.</p>
                    <div class="expertise-options">
                        <label class="expertise-option" :class="{ selected: expertiseSingle === 'glaucoma' }" @click="expertiseSingle = 'glaucoma'">
                            <div class="exp-check"><span v-if="expertiseSingle === 'glaucoma'">✓</span></div>
                            <div class="exp-text">
                                <span class="exp-title">Glaucoma</span>
                                <span class="exp-desc">Optic nerve &amp; intraocular pressure</span>
                            </div>
                        </label>
                        <label class="expertise-option" :class="{ selected: expertiseSingle === 'dr' }" @click="expertiseSingle = 'dr'">
                            <div class="exp-check"><span v-if="expertiseSingle === 'dr'">✓</span></div>
                            <div class="exp-text">
                                <span class="exp-title">Diabetic Retinopathy</span>
                                <span class="exp-desc">Retinal vascular changes from diabetes</span>
                            </div>
                        </label>
                        <label class="expertise-option" :class="{ selected: expertiseSingle === 'amd' }" @click="expertiseSingle = 'amd'">
                            <div class="exp-check"><span v-if="expertiseSingle === 'amd'">✓</span></div>
                            <div class="exp-text">
                                <span class="exp-title">AMD</span>
                                <span class="exp-desc">Age-related macular degeneration</span>
                            </div>
                        </label>
                    </div>
                    <p v-if="expertiseError" class="error">{{ expertiseError }}</p>
                    <button class="submit-btn" @click="saveExpertise" :disabled="expertiseSaving || !expertiseSingle">
                        {{ expertiseSaving ? 'Saving...' : 'Confirm & Continue' }}
                    </button>
                </div>
            </div>
        </transition>

        <div class="header">
            <div class="user-bar">
                <span>🔬 Dr. {{ doctorName }} — Research Mode</span>
                <button class="logout-btn" @click="logout">Sign Out</button>
            </div>
            <p class="university">Democritus University of Thrace – DDART spin-off company</p>
            <img src="/DDART.png" style="height:30px;width:auto;object-fit:contain;" />
        </div>

        <div class="panel-tabs">

            <button :class="['panel-tab', { active: tab === 'hc' }]" @click="tab = 'hc'; loadHCPending()">
            Pending examinations 
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
                                <img :src="'https://labiris.myiplist.com/research/image/' + currentImage.id" class="fundus-image zoomable" @click="openZoom('https://labiris.myiplist.com/research/image/' + currentImage.id)" />
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
                    <p>No pending health center uploads matching your expertise.</p>
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
                                <img :src="'https://labiris.myiplist.com/research/hc-image/' + currentHC.id + '?doctor_id=' + doctorId" class="fundus-image zoomable" @click="openZoom('https://labiris.myiplist.com/research/hc-image/' + currentHC.id + '?doctor_id=' + doctorId)" />
                                <div class="patient-info-panel">
                                    <div class="patient-info-row">
                                        <span class="pi-label">S.S.N.</span>
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
                                <p class="diagnosis-hint">Diagnose the condition and complete the biometrics checklist below.</p>

                                <!-- DR Final Diagnosis + Biometrics -->
                                <div v-if="doctorExpertise.dr" class="diagnosis-group">
                                    <label class="diagnosis-label">Referral for Diabetic Retinopathy</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'No_DR' }"><input type="radio" v-model="hcDiagnosis.dr" value="No_DR" /> No DR</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Mild' }"><input type="radio" v-model="hcDiagnosis.dr" value="Mild" /> Mild</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Moderate' }"><input type="radio" v-model="hcDiagnosis.dr" value="Moderate" /> Moderate</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Severe' }"><input type="radio" v-model="hcDiagnosis.dr" value="Severe" /> Severe</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.dr === 'Proliferate_DR' }"><input type="radio" v-model="hcDiagnosis.dr" value="Proliferate_DR" /> Proliferative</label>
                                    </div>
                                    <div class="bio-table">
                                        <div class="bio-header"><span class="bio-name-col">DIABETIC RETINOPATHY</span><span>YES</span><span>NO</span><span>INCONCLUSIVE</span></div>
                                        <div v-for="item in drBiomarkers" :key="item.key" class="bio-row" @mouseenter="activeTip = item.key" @mouseleave="activeTip = null">
                                            <span class="bio-name-col">
                                                {{ item.label }}
                                                <transition name="tip-fade"><span v-if="activeTip === item.key" class="bio-tip">{{ item.tip }}</span></transition>
                                            </span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="yes" /></span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="no" /></span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="inconclusive" /></span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Glaucoma Final Diagnosis + Biometrics -->
                                <div v-if="doctorExpertise.glaucoma" class="diagnosis-group">
                                    <label class="diagnosis-label">Referral for Glaucoma</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.glaucoma === 'Glaucoma' }"><input type="radio" v-model="hcDiagnosis.glaucoma" value="Glaucoma" /> Yes</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.glaucoma === 'Healthy' }"><input type="radio" v-model="hcDiagnosis.glaucoma" value="Healthy" /> No</label>
                                    </div>
                                    <div class="bio-table">
                                        <div class="bio-header"><span class="bio-name-col">GLAUCOMA</span><span>YES</span><span>NO</span><span>INCONCLUSIVE</span></div>
                                        <div v-for="item in glaucomaBiomarkers" :key="item.key" class="bio-row" @mouseenter="activeTip = item.key" @mouseleave="activeTip = null">
                                            <span class="bio-name-col">
                                                {{ item.label }}
                                                <transition name="tip-fade"><span v-if="activeTip === item.key" class="bio-tip">{{ item.tip }}</span></transition>
                                            </span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="yes" /></span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="no" /></span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="inconclusive" /></span>
                                        </div>
                                    </div>
                                </div>

                                <!-- AMD Final Diagnosis + Biometrics -->
                                <div v-if="doctorExpertise.amd" class="diagnosis-group">
                                    <label class="diagnosis-label">Referral for AMD</label>
                                    <div class="radio-group">
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.amd === 'AMD' }"><input type="radio" v-model="hcDiagnosis.amd" value="AMD" /> Yes</label>
                                        <label class="radio-option" :class="{ selected: hcDiagnosis.amd === 'Normal' }"><input type="radio" v-model="hcDiagnosis.amd" value="Normal" /> No</label>
                                    </div>
                                    <div class="bio-table">
                                        <div class="bio-header"><span class="bio-name-col">AMD</span><span>YES</span><span>NO</span><span>INCONCLUSIVE</span></div>
                                        <div v-for="item in amdBiomarkers" :key="item.key" class="bio-row" @mouseenter="activeTip = item.key" @mouseleave="activeTip = null">
                                            <span class="bio-name-col">
                                                {{ item.label }}
                                                <transition name="tip-fade"><span v-if="activeTip === item.key" class="bio-tip">{{ item.tip }}</span></transition>
                                            </span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="yes" /></span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="no" /></span>
                                            <span><input type="radio" :name="'bio_'+item.key" v-model="biomarkers[item.key]" value="inconclusive" /></span>
                                        </div>
                                    </div>
                                </div>

                                <div class="blind-notice">AI confidence scores are hidden during evaluation</div>
                                <p v-if="hcSubmitError" class="error">{{ hcSubmitError }}</p>
                                <button class="submit-btn" @click="submitHCDiagnosis" :disabled="hcSubmitting || !hcDiagnosisComplete">
                                    {{ hcSubmitting ? 'Submitting...' : '✓ Submit Diagnosis' }}
                                </button>
                                <p v-if="!hcDiagnosisComplete" class="hint">Please select a final result above to submit.</p>
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
                <div v-else-if="concludedImages.length === 0 && hcConcluded.length === 0" class="empty-state">
                    <p>No concluded examinations yet.</p>
                </div>
                <div v-else>
                    <div v-if="concludedImages.length > 0">
                        
                        <div class="concluded-list">
                            <div v-for="item in concludedImages" :key="item.id" class="concluded-item">
                                <img :src="'https://labiris.myiplist.com/research/image/' + item.image_id" class="concluded-thumb zoomable" @click="openZoom('https://labiris.myiplist.com/research/image/' + item.image_id)" />
                                <div class="concluded-info">
                                    <div class="concluded-header">
                                        <p class="concluded-title">Image #{{ item.image_id }}</p>
                                        <div class="category-badge" :class="'cat-' + item.category">{{ categoryLabel(item.category) }}</div>
                                    </div>
                                    <div class="comparison-grid">
                                        <div class="comparison-header one-col"><span>Your Diagnosis</span></div>
                                        <div class="comparison-row one-col">
                                            <span>{{ doctorAnswer(item) }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="hcConcluded.length > 0" class="hc-concluded-section">
                        <h4 class="hc-concluded-title">Health Center Upload Reviews</h4>
                        <div class="concluded-list">
                            <div v-for="item in hcConcluded" :key="'hc-' + item.id" class="concluded-item">
                                <img :src="'https://labiris.myiplist.com/research/hc-image/' + item.id + '?doctor_id=' + doctorId" class="concluded-thumb zoomable" @click="openZoom('https://labiris.myiplist.com/research/hc-image/' + item.id + '?doctor_id=' + doctorId)" />
                                <div class="concluded-info">
                                    <div class="concluded-header">
                                        <p class="concluded-title">S.S.N.: {{ item.patient_amka }}</p>
                                        <span class="center-tag">{{ item.center_name }}</span>
                                        <span class="date-tag">{{ formatDate(item.uploaded_at) }}</span>
                                    </div>
                                    <div class="comparison-grid">
                                        <div class="comparison-header two-col"><span>Condition</span><span>Your Answer</span></div>
                                        <div v-if="item.ai_glaucoma_conf >= 90 && doctorExpertise.glaucoma" class="comparison-row two-col">
                                            <span class="cond-label">Glaucoma</span>
                                            <span>{{ item.doctor_glaucoma }}</span>
                                        </div>
                                        <div v-if="item.ai_dr_conf >= 90 && doctorExpertise.dr" class="comparison-row two-col">
                                            <span class="cond-label">DR</span>
                                            <span>{{ item.doctor_dr }}</span>
                                        </div>
                                        <div v-if="item.ai_amd_conf >= 90 && doctorExpertise.amd" class="comparison-row two-col">
                                            <span class="cond-label">AMD</span>
                                            <span>{{ item.doctor_amd }}</span>
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
            <div class="footer-left"><img src="/DDARTECH_Research-removebg-preview.png" class="dept-logo" /></div>
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
            tab: 'hc',
            showLogoutOverlay: false,
            logoutBarWidth: 0,

            // Expertise
            showExpertiseModal: false,
            expertiseSingle: '',
            expertise: { glaucoma: false, dr: false, amd: false },
            doctorExpertise: { glaucoma: false, dr: false, amd: false },
            expertiseSaving: false,
            expertiseError: '',

            // Biometrics checklist
            biomarkers: {},
            activeTip: null,
        drBiomarkers: [
            { key: 'microaneurysms', label: 'Microaneurysms', tip: 'Small balloon-like swellings in tiny blood vessels of the retina — earliest sign of DR.' },
            { key: 'hard_exudates', label: 'Hard exudates', tip: 'Lipid and protein deposits appearing as bright yellow-white spots with sharp margins.' },
            { key: 'dot_blot_hemorrhages', label: 'Dot-blot hemorrhages', tip: 'Small round hemorrhages in the inner nuclear layer, indicating capillary rupture.' },
            { key: 'cotton_wool_spots', label: 'Cotton wool spots', tip: 'Fluffy white patches caused by nerve fiber layer infarcts from capillary occlusion.' },
            { key: 'venous_beading', label: 'Venous beading', tip: 'Irregular venous caliber changes resembling a string of beads — sign of severe NPDR.' },
            { key: 'irmas', label: 'IRMAs', tip: 'Intraretinal microvascular abnormalities — abnormal vessel growth within the retina.' },
            { key: 'macular_thickening', label: 'Macular thickening', tip: 'Swelling of the macula due to fluid accumulation, leading to central vision loss.' },
            { key: 'neo_vessels', label: 'Neo-vessels', tip: 'New abnormal blood vessels growing on the retinal surface or optic disc — defines PDR.' },
            { key: 'mild_npdr', label: 'MILD NPDR', tip: 'At least one microaneurysm; less severe than moderate NPDR.' },
            { key: 'moderate_npdr', label: 'MODERATE NPDR', tip: 'More than mild NPDR but less than the 4-2-1 rule threshold for severe NPDR.' },
            { key: 'severe_npdr', label: 'SEVERE NPDR', tip: '4-2-1 rule: hemorrhages in 4 quadrants, venous beading in 2, or IRMA in 1 quadrant.' },
            { key: 'pre_pdr', label: 'PRE-PDR', tip: 'Features of severe NPDR with early neovascularization not yet meeting full PDR criteria.' },
            { key: 'pdr', label: 'PDR', tip: 'Proliferative diabetic retinopathy — neovascularization present, high risk of vitreous hemorrhage.' },
            { key: 'dme', label: 'DME', tip: 'Diabetic macular edema — fluid in the macula causing vision distortion; can occur at any DR stage.' },
        ],
        glaucomaBiomarkers: [
            { key: 'cup_disc_ratio', label: 'Cup to disc ratio > 0.6', tip: 'Enlarged cup-to-disc ratio (>0.6) suggests significant optic nerve head cupping from glaucoma.' },
            { key: 'rim_notching', label: 'Neuroretinal Rim Notching superiorly and/or inferiorly', tip: 'Focal loss of neuroretinal rim tissue, especially at superior/inferior poles — characteristic of glaucoma.' },
            { key: 'nfl_thinning', label: 'Thinning of the nerve fiber layer', tip: 'Loss of the retinal nerve fiber layer visible as a darker wedge-shaped defect.' },
            { key: 'disc_hemorrhage', label: 'Disc Hemorrhage', tip: 'Splinter hemorrhage at the disc margin — strongly associated with glaucomatous progression.' },
            { key: 'peripapillary_atrophy', label: 'Peripapillary Atrophy', tip: 'Atrophic changes in the retinal pigment epithelium surrounding the optic disc.' },
            { key: 'bayoneting', label: 'Bayoneting', tip: 'Blood vessels appear to bend at the disc margin then disappear — sign of deep excavation.' },
            { key: 'glaucomatous_disc', label: 'glaucomatous disc', tip: 'Overall disc appearance consistent with glaucomatous damage.' },
        ],
        amdBiomarkers: [
            { key: 'drusen', label: 'Drusen >63μm', tip: 'Yellow extracellular deposits under the retina. Intermediate drusen (>63μm) indicate AMD risk.' },
            { key: 'pigmentation', label: 'Macular hyper- and/or hypopigmentation', tip: 'Abnormal RPE pigmentation changes in the macula — dark clumps or pale areas.' },
            { key: 'atrophy', label: 'Atrophy', tip: 'Geographic atrophy — well-defined area of RPE and photoreceptor loss in the macula.' },
            { key: 'subretinal_hemorrhage', label: 'Sub/intra retinal hemorrhage', tip: 'Blood beneath or within the retina, often indicating choroidal neovascularization in wet AMD.' },
            { key: 'hard_exudates_amd', label: 'Hard exudates', tip: 'Lipid deposits in the macula associated with neovascular AMD leakage.' },
            { key: 'subretinal_fibrous', label: 'Subretinal fibrous tissue/scar', tip: 'End-stage wet AMD — fibrous scar replacing the macula after choroidal neovascularization.' },
            { key: 'dry_amd', label: 'DRY AMD', tip: 'Atrophic AMD — slow progressive loss of RPE and photoreceptors without neovascularization.' },
            { key: 'eamd', label: 'eAMD', tip: 'Exudative (wet) AMD — choroidal neovascularization with rapid vision loss if untreated.' },
        ],

            // Pending
            allPending: [], pendingLoading: false,
            currentIndex: 0,
            currentDiagnosis: { glaucoma: null, dr: null, amd: null },
            submitting: false, submitError: '',

            // HC
            hcPending: [], hcLoading: false,
            hcIndex: 0,
            hcDiagnosis: { glaucoma: null, dr: null, amd: null },
            hcSubmitting: false, hcSubmitError: '',

            // Concluded
            concludedImages: [], hcConcluded: [], concludedLoading: false,

            // Zoom
            zoomSrc: null,
            zoomLevel: 1,
            zoomOrigin: "center center",
            panX: 0, panY: 0,
            isPanning: false,
            panStartX: 0, panStartY: 0,
            panStartOffX: 0, panStartOffY: 0
        }
    },

    computed: {
        currentImage() { return this.allPending[this.currentIndex] || {} },
        currentHC() { return this.hcPending[this.hcIndex] || {} },
        anyExpertise() { return !!this.expertiseSingle },

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
            if (this.doctorExpertise.glaucoma && !this.hcDiagnosis.glaucoma) return false
            if (this.doctorExpertise.dr && !this.hcDiagnosis.dr) return false
            if (this.doctorExpertise.amd && !this.hcDiagnosis.amd) return false
            return true
        },

        overallAgreement() {
            if (!this.concludedImages.length) return 0
            return Math.round(this.concludedImages.filter(i => this.doctorAnswer(i) === this.aiAnswer(i)).length / this.concludedImages.length * 100)
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

    async mounted() {
        window.addEventListener('keydown', (e) => { if (e.key === 'Escape') this.closeZoom() })
        const stored = localStorage.getItem('ddart_doctor')
        if (!stored) { this.$router.push('/login'); return }
        const doctor = JSON.parse(stored)
        this.doctorName = doctor.name
        this.doctorId = doctor.id

        // Load expertise from backend
        try {
            const res = await fetch(`https://labiris.myiplist.com/doctor/expertise/${doctor.id}`)
            const data = await res.json()
            if (data.expertise) {
                const parts = data.expertise.split(',')
                this.expertiseSingle = parts[0] || ''
                this.doctorExpertise = {
                    glaucoma: parts.includes('glaucoma'),
                    dr: parts.includes('dr'),
                    amd: parts.includes('amd')
                }
                this.loadPending()
                this.loadHCPending()
            } else {
                // First time — show modal
                this.showExpertiseModal = true
            }
        } catch {
            this.showExpertiseModal = true
        }
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

        async saveExpertise() {
            if (!this.anyExpertise) return
            this.expertiseSaving = true
            this.expertiseError = ''
            const parts = [this.expertiseSingle]
            try {
                const res = await fetch('https://labiris.myiplist.com/doctor/expertise', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ doctor_id: this.doctorId, expertise: parts.join(',') })
                })
                if (!res.ok) { this.expertiseError = 'Failed to save. Please try again.'; return }
                this.doctorExpertise = { ...this.expertise }
                this.showExpertiseModal = false
                this.loadPending()
                this.loadHCPending()
            } catch { this.expertiseError = 'Connection failed.' }
            finally { this.expertiseSaving = false }
        },

        async loadPending() {
            this.pendingLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/research/pending/${this.doctorId}`)
                const data = await res.json()
                // Filter by expertise
                const exp = this.doctorExpertise
                this.allPending = (data.images || []).filter(img => {
                    if (img.category === 'glaucoma') return exp.glaucoma
                    if (img.category === 'dr') return exp.dr
                    if (img.category === 'amd') return exp.amd
                    return false
                })
                this.currentIndex = 0
            } catch { } finally { this.pendingLoading = false }
        },

        async loadHCPending() {
            this.hcLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/research/pending-hc?doctor_id=${this.doctorId}`)
                const data = await res.json()
                const exp = this.doctorExpertise
                // Only include images where AI ≥ 90% on at least one condition within doctor's expertise
                this.hcPending = (Array.isArray(data) ? data : []).filter(hc => {
                    if (exp.glaucoma && hc.ai_glaucoma_conf >= 90) return true
                    if (exp.dr && hc.ai_dr_conf >= 90) return true
                    if (exp.amd && hc.ai_amd_conf >= 90) return true
                    return false
                })
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
                if (!res.ok) { this.submitError = 'Submission failed.'; return }
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
                        doctor_amd: this.hcDiagnosis.amd || 'N/A',
                        biomarkers: JSON.stringify(this.biomarkers)
                    })
                })
                if (!res.ok) { this.hcSubmitError = 'Submission failed.'; return }
                this.hcPending.splice(this.hcIndex, 1)
                if (this.hcIndex >= this.hcPending.length && this.hcIndex > 0) this.hcIndex--
                this.hcDiagnosis = { glaucoma: null, dr: null, amd: null }
                this.biomarkers = {}
            } catch { this.hcSubmitError = 'Connection failed.' }
            finally { this.hcSubmitting = false }
        },

        openZoom(src) { this.zoomSrc = src; this.zoomLevel = 1; this.panX = 0; this.panY = 0; this.zoomOrigin = "center center" },
        closeZoom() { this.zoomSrc = null; this.zoomLevel = 1; this.panX = 0; this.panY = 0 },
        resetZoom() { this.zoomLevel = 1; this.panX = 0; this.panY = 0; this.zoomOrigin = "center center" },
        zoomIn() { this.zoomLevel = Math.min(this.zoomLevel + 0.25, 6) },
        zoomOut() { this.zoomLevel = Math.max(this.zoomLevel - 0.25, 0.5); if (this.zoomLevel <= 1) { this.panX = 0; this.panY = 0 } },
        onWheel(e) {
            const wrap = e.currentTarget.getBoundingClientRect()
            const mx = e.clientX - wrap.left
            const my = e.clientY - wrap.top
            const delta = e.deltaY > 0 ? -0.15 : 0.15
            const newLevel = Math.min(Math.max(this.zoomLevel + delta, 0.5), 6)
            // Zoom toward cursor
            const ratio = newLevel / this.zoomLevel
            this.panX = mx - ratio * (mx - this.panX)
            this.panY = my - ratio * (my - this.panY)
            this.zoomLevel = newLevel
            if (this.zoomLevel <= 1) { this.panX = 0; this.panY = 0 }
        },
        startPan(e) {
            if (this.zoomLevel <= 1) return
            this.isPanning = true
            this.panStartX = e.clientX - this.panX
            this.panStartY = e.clientY - this.panY
        },
        doPan(e) {
            if (!this.isPanning) return
            this.panX = e.clientX - this.panStartX
            this.panY = e.clientY - this.panStartY
        },
        endPan() { this.isPanning = false },

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
                        localStorage.removeItem('ddart_doctor')
                        this.$router.push('/login')
                    }, 100)
                }
            }
            requestAnimationFrame(animate)
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; min-height: 100%; background: #f0f4f8; font-family: 'Source Sans 3', sans-serif; }


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

.research-container { display: flex; flex-direction: column; align-items: center; padding: 30px 20px 0; min-height: 100vh; }
.header { text-align: center; margin-bottom: 24px; width: 100%; max-width: 900px; }
.user-bar { display: flex; align-items: center; justify-content: flex-end; gap: 10px; margin-bottom: 10px; font-size: 13px; color: #4a5568; }
.logout-btn { padding: 4px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; font-family: 'Source Sans 3', sans-serif; background: none; border: 1px solid #e2e8f0; color: #718096; transition: background 0.2s; }
.logout-btn:hover { background: #f8fafc; }
.university { font-size: 14px; color: #2c5282; font-weight: 600; margin: 0 0 4px; }
.subtitle { font-size: 13px; color: #4a6fa5; margin: 0 0 16px; }
.logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 18px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; justify-content: center; gap: 2px; }
.logo span { color: #e53e3e; font-size: 48px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }

/* Expertise modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(10,20,40,0.88); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.modal-box { background: white; border-radius: 12px; padding: 40px; width: 420px; display: flex; flex-direction: column; align-items: center; gap: 20px; animation: appear 0.35s cubic-bezier(0.34,1.56,0.64,1) both; }
@keyframes appear { from { opacity: 0; transform: scale(0.9) translateY(20px); } to { opacity: 1; transform: scale(1) translateY(0); } }
.modal-logo { font-family: 'Arial Narrow', Arial, sans-serif; font-size: 16px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; gap: 2px; }
.modal-logo span { color: #e53e3e; font-size: 36px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; }
.modal-box h3 { font-family: 'Playfair Display', serif; color: #2d3748; font-size: 20px; margin: 0; text-align: center; }
.modal-box p { font-size: 13px; color: #718096; margin: 0; text-align: center; line-height: 1.6; }
.expertise-options { display: flex; flex-direction: column; gap: 10px; width: 100%; }
.expertise-option { display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px; border: 1.5px solid #e2e8f0; border-radius: 8px; cursor: pointer; transition: all 0.2s; background: white; }
.expertise-option:hover { border-color: #2b6cb0; box-shadow: 0 2px 8px rgba(43,108,176,0.1); }
.expertise-option.selected { border-color: #2b6cb0; background: #ebf8ff; }
.exp-check { width: 22px; height: 22px; min-width: 22px; border: 2px solid #e2e8f0; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: white; background: white; transition: all 0.2s; margin-top: 1px; }
.expertise-option.selected .exp-check { background: #2b6cb0; border-color: #2b6cb0; }
.exp-text { display: flex; flex-direction: column; gap: 2px; }
.exp-title { font-size: 14px; font-weight: 700; color: #2d3748; }
.exp-desc { font-size: 12px; color: #718096; }
.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0; }

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

.submit-btn { padding: 11px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; width: 100%; }
.submit-btn:hover:not(:disabled) { background: #2c5282; }
.submit-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.hint { font-size: 11px; color: #a0aec0; margin: 0; }

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
.comparison-header.two-col, .comparison-row.two-col { grid-template-columns: 120px 1fr; }
.comparison-header.one-col, .comparison-row.one-col { grid-template-columns: 1fr; }
.comparison-row { display: grid; grid-template-columns: 1fr 1fr 100px; gap: 8px; align-items: center; }
.cond-label { font-weight: 700; color: #4a5568; font-size: 12px; }
.conf-reveal { font-weight: 700; color: #2b6cb0; font-size: 12px; }
.match-yes { color: #38a169; font-weight: 700; }
.match-no { color: #e53e3e; font-weight: 700; }
.hc-concluded-section { margin-top: 28px; }
.hc-concluded-title { font-family: 'Playfair Display', serif; font-size: 16px; color: #2c5282; margin: 0 0 14px; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.fade-slide-enter-active { transition: all 0.3s ease; }
.fade-slide-leave-active { transition: all 0.2s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-6px); }


/* Zoom overlay */
.zoom-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.92); z-index: 9999; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; }
.zoom-toolbar { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.1); border-radius: 8px; padding: 6px 12px; }
.zoom-btn { background: rgba(255,255,255,0.15); border: none; color: white; font-size: 16px; width: 32px; height: 32px; border-radius: 6px; cursor: pointer; transition: background 0.2s; display: flex; align-items: center; justify-content: center; }
.zoom-btn:hover { background: rgba(255,255,255,0.3); }
.zoom-btn.zoom-close { background: rgba(229,62,62,0.4); margin-left: 8px; }
.zoom-btn.zoom-close:hover { background: rgba(229,62,62,0.7); }
.zoom-pct { color: white; font-size: 13px; font-weight: 700; min-width: 48px; text-align: center; }
.zoom-img-wrap { display: flex; align-items: center; justify-content: center; overflow: hidden; width: 90vw; height: 75vh; position: relative; }
.zoom-img { max-width: 85vw; max-height: 72vh; object-fit: contain; transform-origin: top left; transition: transform 0.08s ease; border-radius: 4px; user-select: none; }
.zoom-hint { color: rgba(255,255,255,0.4); font-size: 11px; margin: 0; }
.zoomable { cursor: zoom-in; transition: opacity 0.2s; }
.zoomable:hover { opacity: 0.85; }
.zoom-fade-enter-active, .zoom-fade-leave-active { transition: opacity 0.2s ease; }
.zoom-fade-enter-from, .zoom-fade-leave-to { opacity: 0; }

.footer { width: 100%; max-width: 900px; display: flex; justify-content: space-between; align-items: center; padding: 16px 0 24px; border-top: 1px solid #e2e8f0; margin-top: auto; }
.dept-logo { height: 55px; width: auto; object-fit: contain; }
.footer-right { text-align: right; }
.footer-right p { font-size: 12px; color: #718096; margin: 2px 0; }
.footer-right a { color: #2b6cb0; text-decoration: none; }
.made-by { font-size: 10px; color: #cbd5e0; margin-top: 4px; }

/* ── Biomarkers table ── */
.bio-table { width: 100%; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; margin-top: 12px; font-size: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.bio-header { display: grid; grid-template-columns: 1fr 52px 52px 110px; background: #2b6cb0; padding: 8px 12px; font-size: 11px; font-weight: 700; color: white; letter-spacing: 0.5px; text-transform: uppercase; }
.bio-header span:not(.bio-name-col) { text-align: center; display: flex; align-items: center; justify-content: center; }
.bio-row { display: grid; grid-template-columns: 1fr 52px 52px 110px; padding: 6px 12px; border-bottom: 1px solid #f0f4f8; align-items: center; transition: background 0.15s; position: relative; }
.bio-row:last-child { border-bottom: none; }
.bio-row:nth-child(even) { background: #f8fafc; }
.bio-row:hover { background: #ebf8ff; }
.bio-name-col { color: #2d3748; font-size: 12px; line-height: 1.4; position: relative; }
.bio-row span:not(.bio-name-col) { display: flex; align-items: center; justify-content: center; }
.bio-row input[type=radio] { width: 15px; height: 15px; accent-color: #2b6cb0; cursor: pointer; }
.bio-tip { position: absolute; left: 0; top: calc(100% + 4px); background: #2d3748; color: white; font-size: 11px; line-height: 1.5; padding: 6px 10px; border-radius: 5px; white-space: normal; width: 240px; z-index: 200; pointer-events: none; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.bio-tip::before { content: ''; position: absolute; top: -4px; left: 12px; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 4px solid #2d3748; }
.tip-fade-enter-active, .tip-fade-leave-active { transition: opacity 0.15s ease; }
.tip-fade-enter-from, .tip-fade-leave-to { opacity: 0; }
.dark .bio-table { border-color: #4a5568; }
.dark .bio-header { background: #1a365d; }
.dark .bio-row { border-bottom-color: #2d3748; }
.dark .bio-row:nth-child(even) { background: #1e2a3a; }
.dark .bio-row:hover { background: #1a365d; }
.dark .bio-name-col { color: #e2e8f0; }
.dark .bio-tip { background: #e2e8f0; color: #2d3748; }
.dark .bio-tip::before { border-bottom-color: #e2e8f0; }
</style>