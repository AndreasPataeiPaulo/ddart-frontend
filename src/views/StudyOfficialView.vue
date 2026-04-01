<template>
    <div class="study-container">

        <!-- Login modal -->
        <transition name="modal-fade">
            <div v-if="!authenticated" class="modal-backdrop">
                <div class="modal-box">
                    <img src="/DDART.png" style="height:30px;width:auto;object-fit:contain;" />
                    <h3>Study Official Access</h3>
                    <p>Enter the study access code to continue.</p>
                    <div class="field">
                        <input v-model="codeInput" type="password" placeholder="Access code"
                            @keyup.enter="authenticate" autofocus />
                    </div>
                    <transition name="error-pop">
                        <p v-if="authError" class="error">{{ authError }}</p>
                    </transition>
                    <button class="submit-btn" @click="authenticate" :disabled="authLoading">
                        {{ authLoading ? 'Verifying...' : 'Enter' }}
                    </button>
                    <button class="back-btn" @click="$router.push('/login')">← Back to Login</button>
                </div>
            </div>
        </transition>

        <!-- Main dashboard -->
        <div v-if="authenticated" class="dashboard">
            <div class="header">
                <div class="user-bar">
                    <span class="user-bar-title">Study Official Dashboard</span>
                    <div class="user-bar-actions">
                        <button class="tab-pill" :class="{ active: mainTab === 'study' }" @click="mainTab = 'study'">📊 Study</button>
                        <button class="tab-pill" :class="{ active: mainTab === 'admin' }" @click="mainTab = 'admin'; loadAdmin(); loadThresholds()">🛠 Admin</button>
                        <button class="logout-btn" @click="logout">Sign Out</button>
                    </div>
                </div>
                <p class="university">Democritus University of Thrace – DDART spin-off company</p>
                <p class="subtitle">Ophthalmology A.I. Screening Program — Study Overview</p>
                <img src="/DDART.png" style="height:30px;width:auto;object-fit:contain;" />
            </div>

            <!-- ═══════════════════════════════════════ STUDY TAB ═══════════════════════════════════════ -->
            <div v-if="mainTab === 'study'">
                <div class="panel-tabs">
                    <button :class="['panel-tab', { active: tab === 'general' }]" @click="switchTab('general')">General</button>
                    <button :class="['panel-tab', { active: tab === 'glaucoma' }]" @click="switchTab('glaucoma')">Glaucoma</button>
                    <button :class="['panel-tab', { active: tab === 'dr' }]" @click="switchTab('dr')">Diabetic Retinopathy</button>
                    <button :class="['panel-tab', { active: tab === 'amd' }]" @click="switchTab('amd')">AMD</button>
                    <button :class="['panel-tab', { active: tab === 'biomarkers' }]" @click="switchTab('biomarkers')">Biomarkers</button>
                </div>

                <div v-if="loading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading study data...</p>
                </div>

                <transition name="fade-slide" mode="out-in">

                    <!-- GENERAL TAB -->
                    <div v-if="!loading && tab === 'general'" key="general" class="panel-section">
                        <div class="stat-grid">
                            <div class="stat-card">
                                <p class="stat-value">{{ stats.general.total_images }}</p>
                                <p class="stat-label">HC Images Uploaded</p>
                            </div>
                            <div class="stat-card">
                                <p class="stat-value">{{ stats.general.hc_total_reviewed }}</p>
                                <p class="stat-label">Images Reviewed</p>
                            </div>
                            <div class="stat-card">
                                <p class="stat-value">{{ stats.doctors.length }}</p>
                                <p class="stat-label">Active Researchers</p>
                            </div>
                        </div>

                        <div class="section-card">
                            <h4 class="section-title">Inter-Rater Agreement <span class="section-sub">(when 2+ experts reviewed the same HC upload)</span></h4>
                            <div class="agreement-row-grid">
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.inter_rater_glaucoma)">
                                        <span class="agree-pct">{{ stats.general.inter_rater_glaucoma }}%</span>
                                    </div>
                                    <p class="agree-label">Glaucoma</p>
                                </div>
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.inter_rater_dr)">
                                        <span class="agree-pct">{{ stats.general.inter_rater_dr }}%</span>
                                    </div>
                                    <p class="agree-label">DR</p>
                                </div>
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.inter_rater_amd)">
                                        <span class="agree-pct">{{ stats.general.inter_rater_amd }}%</span>
                                    </div>
                                    <p class="agree-label">AMD</p>
                                </div>
                                <div class="agree-block">
                                    <div class="agree-ring overall" :style="ringStyle(overallInterRater)">
                                        <span class="agree-pct">{{ overallInterRater }}%</span>
                                    </div>
                                    <p class="agree-label">Overall</p>
                                </div>
                            </div>
                        </div>

                        <div class="section-card">
                            <h4 class="section-title">Expert vs AI Agreement on HC Uploads <span class="section-sub">(AI confidence ≥{{ confThreshold }}% only)</span></h4>
                            <p style="font-size:12px;color:#718096;margin:-12px 0 16px;">For HC uploads where the AI was highly confident (≥90%), this shows how often the reviewing expert agreed with the AI diagnosis.</p>
                            <div class="agreement-row-grid">
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.hc_ai_agree_glaucoma)">
                                        <span class="agree-pct">{{ stats.general.hc_ai_agree_glaucoma }}%</span>
                                    </div>
                                    <p class="agree-label">Glaucoma</p>
                                </div>
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.hc_ai_agree_dr)">
                                        <span class="agree-pct">{{ stats.general.hc_ai_agree_dr }}%</span>
                                    </div>
                                    <p class="agree-label">DR</p>
                                </div>
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.hc_ai_agree_amd)">
                                        <span class="agree-pct">{{ stats.general.hc_ai_agree_amd }}%</span>
                                    </div>
                                    <p class="agree-label">AMD</p>
                                </div>
                            </div>
                        </div>

                        <div class="section-card">
                            <h4 class="section-title">Extended Agreement <span class="section-sub">(AI match + Referral for Other Reason — excluded from standard metrics)</span></h4>
                            <p style="font-size:12px;color:#718096;margin:-12px 0 16px;line-height:1.6;">Per condition: % of expert reviews where the expert either agreed with the AI <strong>or</strong> flagged a referral for an independent reason. Inconclusive reviews excluded. Not counted in AI agreement or inter-rater statistics.</p>
                            <div class="agreement-row-grid">
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.ref_ext_glaucoma ? stats.general.ref_ext_glaucoma.pct : 0)">
                                        <span class="agree-pct">{{ stats.general.ref_ext_glaucoma ? stats.general.ref_ext_glaucoma.pct : 0 }}%</span>
                                    </div>
                                    <p class="agree-label">Glaucoma</p>
                                    <p class="ref-sub" v-if="stats.general.ref_ext_glaucoma && stats.general.ref_ext_glaucoma.total">
                                        <span class="ref-chip ref-agree">✓ {{ stats.general.ref_ext_glaucoma.agree_count }} agree AI</span>
                                        <span class="ref-chip ref-other">⚑ {{ stats.general.ref_ext_glaucoma.other_count }} other</span>
                                    </p>
                                </div>
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.ref_ext_dr ? stats.general.ref_ext_dr.pct : 0)">
                                        <span class="agree-pct">{{ stats.general.ref_ext_dr ? stats.general.ref_ext_dr.pct : 0 }}%</span>
                                    </div>
                                    <p class="agree-label">DR</p>
                                    <p class="ref-sub" v-if="stats.general.ref_ext_dr && stats.general.ref_ext_dr.total">
                                        <span class="ref-chip ref-agree">✓ {{ stats.general.ref_ext_dr.agree_count }} agree AI</span>
                                        <span class="ref-chip ref-other">⚑ {{ stats.general.ref_ext_dr.other_count }} other</span>
                                    </p>
                                </div>
                                <div class="agree-block">
                                    <div class="agree-ring" :style="ringStyle(stats.general.ref_ext_amd ? stats.general.ref_ext_amd.pct : 0)">
                                        <span class="agree-pct">{{ stats.general.ref_ext_amd ? stats.general.ref_ext_amd.pct : 0 }}%</span>
                                    </div>
                                    <p class="agree-label">AMD</p>
                                    <p class="ref-sub" v-if="stats.general.ref_ext_amd && stats.general.ref_ext_amd.total">
                                        <span class="ref-chip ref-agree">✓ {{ stats.general.ref_ext_amd.agree_count }} agree AI</span>
                                        <span class="ref-chip ref-other">⚑ {{ stats.general.ref_ext_amd.other_count }} other</span>
                                    </p>
                                </div>
                            </div>
                            <p style="font-size:11px;color:#a0aec0;margin:16px 0 0;font-style:italic;">Total referrals for other reason across all conditions: <strong>{{ stats.general.referral_other_count }}</strong></p>
                        </div>

                        <div class="section-card">
                            <h4 class="section-title">Health Center Uploads</h4>
                            <div v-if="!stats.hc_upload_counts || stats.hc_upload_counts.length === 0" class="empty-state">No uploads yet.</div>
                            <table v-else class="data-table">
                                <thead>
                                    <tr><th>Health Center</th><th>Specialty</th><th>Images Uploaded</th><th>Reviewed</th><th>Share</th></tr>
                                </thead>
                                <tbody>
                                    <tr v-for="hc in stats.hc_upload_counts" :key="hc.name">
                                        <td>{{ hc.name }}</td>
                                        <td><span :class="['specialty-chip', hc.specialty]">{{ hc.specialty || '—' }}</span></td>
                                        <td>{{ hc.total }}</td>
                                        <td>{{ hc.reviewed }}</td>
                                        <td>
                                            <div class="mini-bar-wrap">
                                                <div class="mini-bar" :style="{ width: maxHCUploads > 0 ? (hc.total / maxHCUploads * 100) + '%' : '0%' }"></div>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                    <!-- Inconclusive studies button -->
                    <div style="display:flex;justify-content:flex-start;">
                        <button class="inconclusive-studies-btn" @click="loadInconclusive(); showInconclusiveModal = true">
                            ⚠ Inconclusive Studies
                            <span v-if="inconclusiveRows.length" class="inconclusive-count-badge">{{ inconclusiveRows.length }}</span>
                        </button>
                    </div>

                    </div>

                    <!-- BIOMARKERS TAB -->
                    <div v-else-if="!loading && tab === 'biomarkers'" key="biomarkers" class="panel-section">
                        <div class="section-card">
                            <div class="bio-header-row">
                                <h4 class="section-title" style="margin-bottom:0">Biomarker Reviews</h4>
                                <div class="bio-header-actions">
                                    <button class="refresh-btn" @click="loadBiomarkers" :disabled="bioLoading">⟳ Refresh</button>
                                    <button class="export-btn" @click="exportBiomarkersCSV" :disabled="filteredBioRows.length === 0">⬇ Export CSV</button>
                                    <button class="export-btn excel" @click="exportBiomarkersExcel" :disabled="filteredBioRows.length === 0">⬇ Export Excel</button>
                                </div>
                            </div>
                            <div class="bio-filter-bar">
                                <select v-model="bioFilter" class="bio-filter-select">
                                    <option value="all">All conditions</option>
                                    <option value="glaucoma">Glaucoma</option>
                                    <option value="dr">Diabetic Retinopathy</option>
                                    <option value="amd">AMD</option>
                                </select>
                                <span class="bio-count">{{ filteredBioRows.length }} reviews</span>
                            </div>
                            <div v-if="bioLoading" class="loading-state"><div class="spinner"></div><p>Loading...</p></div>
                            <div v-else-if="filteredBioRows.length === 0" class="empty-state">No reviews submitted yet.</div>
                            <div v-else class="bio-review-list">
                                <!-- Group by upload_id — same image reviews shown side by side -->
                                <div v-for="group in groupedBioRows" :key="group.upload_id" class="bio-group-card">
                                    <!-- Image header -->
                                    <div class="bio-group-header">
                                        <span class="bio-review-img">{{ group.patient_amka }} — {{ group.center_name }}</span>
                                        <span class="bio-group-count" v-if="group.reviews.length > 1">{{ group.reviews.length }} doctors reviewed</span>
                                    </div>
                                    <!-- Reviews side by side -->
                                    <div class="bio-group-reviews" :class="{ 'bio-group-split': group.reviews.length >= 2 }">
                                        <div v-for="row in group.reviews" :key="row.id" class="bio-review-card">
                                            <div class="bio-review-header">
                                                <span class="bio-review-doctor">Dr. {{ row.doctor_name }}</span>
                                                <span class="bio-review-date">{{ row.reviewed_at ? row.reviewed_at.slice(0,10) : '' }}</span>
                                            </div>
                                            <div class="bio-review-diagnoses">
                                                <span v-if="row.doctor_glaucoma && row.doctor_glaucoma !== 'N/A'" class="bio-diag-chip">Glaucoma: {{ row.doctor_glaucoma }}</span>
                                                <span v-if="row.doctor_dr && row.doctor_dr !== 'N/A'" class="bio-diag-chip">DR: {{ row.doctor_dr }}</span>
                                                <span v-if="row.doctor_amd && row.doctor_amd !== 'N/A'" class="bio-diag-chip">AMD: {{ row.doctor_amd }}</span>
                                            </div>
                                            <div v-if="row.biomarkers && Object.keys(row.biomarkers).length > 0" class="bio-markers-grid">
                                                <div v-for="(val, key) in row.biomarkers" :key="key" class="bio-marker-item" :class="'bm-' + val">
                                                    <span class="bm-key">{{ key.replace(/_/g, ' ') }}</span>
                                                    <span class="bm-val">{{ val }}</span>
                                                </div>
                                            </div>
                                            <div v-else class="bio-no-markers">No biomarkers recorded.</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- CONDITION TABS (Glaucoma / DR / AMD) — ENHANCED -->
                    <div v-else-if="!loading && (tab === 'glaucoma' || tab === 'dr' || tab === 'amd')" :key="tab" class="panel-section">

                        <!-- Summary bar -->
                        <div class="condition-summary-bar">
                            <div class="csb-item">
                                <span class="csb-val">{{ currentRows.length }}</span>
                                <span class="csb-label">Images</span>
                            </div>
                            <div class="csb-item">
                                <span class="csb-val">{{ totalReviewsForCondition }}</span>
                                <span class="csb-label">Total Reviews</span>
                            </div>
                            <div class="csb-item">
                                <span class="csb-val">{{ conditionAIAgree }}%</span>
                                <span class="csb-label">AI Agreement</span>
                            </div>
                            <div class="csb-item">
                                <span class="csb-val">{{ conditionInterRater }}%</span>
                                <span class="csb-label">Inter-Rater</span>
                            </div>
                        </div>

                        <!-- HC per-image breakdown -->
                        <div class="section-card">
                            <div class="condition-header-row">
                                <h4 class="section-title" style="margin-bottom:0">
                                    Health Center Uploads — {{ conditionLabel }}
                                    <span class="section-sub">({{ groupedHCRows.length }} images)</span>
                                </h4>
                                <select v-model="conditionFilter" class="bio-filter-select">
                                    <option value="all">All</option>
                                    <option value="reviewed">Reviewed only</option>
                                    <option value="unreviewed">Unreviewed only</option>
                                    <option value="agree">All experts match AI</option>
                                    <option value="disagree">Any expert differs</option>
                                    <option value="highconf">High confidence ≥{{ confThreshold }}%</option>
                                </select>
                            </div>

                            <div v-if="filteredHCRows.length === 0" class="empty-state">No health center cases for this condition yet.</div>

                            <table v-else class="data-table">
                                <thead>
                                    <tr>
                                        <th>Image</th>
                                        <th>Patient ID</th>
                                        <th>Health Center</th>
                                        <th>AI Result</th>
                                        <th>Referral</th>
                                        <th>Confidence</th>
                                        <th>Reviews</th>
                                        <th>Agreement</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="g in filteredHCRows" :key="g.upload_id">
                                        <td>
                                            <button class="img-link-btn" @click="openHCDetail(g)">
                                                Image #{{ g.upload_id }}
                                            </button>
                                        </td>
                                        <td class="amka-cell">{{ g.patient_amka }}</td>
                                        <td>{{ g.center_name }}</td>
                                        <td><span class="ai-chip" :class="aiChipClass(g.ai_result)">{{ g.ai_result }}</span></td>
                                        <td><span :class="['referral-badge', isReferral(g.ai_result, tab) ? 'referral-yes' : 'referral-no']">{{ isReferral(g.ai_result, tab) ? 'Referral' : 'No Referral' }}</span></td>
                                        <td><span :class="['conf-badge', g.ai_conf >= confThreshold ? 'conf-high' : 'conf-low']">{{ g.ai_conf }}%</span></td>
                                        <td><span class="review-count-badge">{{ g.reviews.length }}</span></td>
                                        <td>
                                            <span v-if="g.reviews.length === 0" class="no-review">—</span>
                                            <span v-else :class="['pct-badge', g.allAgree ? 'pct-good' : g.anyAgree ? 'pct-mid' : 'pct-low']">
                                                {{ g.agreeCount }}/{{ g.reviews.length }} match AI
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                </transition>
            </div>

            <!-- ═══════════════════════════════════════ ADMIN TAB ═══════════════════════════════════════ -->
            <div v-if="mainTab === 'admin'" class="panel-section">

                <div v-if="adminLoading" class="loading-state"><div class="spinner"></div><p>Loading...</p></div>

                <div v-else class="admin-grid">

                    <!-- Doctor management -->
                    <div class="section-card">
                        <div class="admin-section-header">
                            <h4 class="section-title" style="margin-bottom:0">Doctor Accounts</h4>
                            <span class="admin-count-badge">{{ adminDoctors.length }} total</span>
                        </div>
                        <div v-if="adminDoctors.length === 0" class="empty-state">No doctors registered yet.</div>
                        <div v-else class="doctor-list">
                            <div v-for="doc in adminDoctors" :key="doc.id" class="doctor-row">
                                <div class="doctor-info">
                                    <span class="doctor-name">{{ doc.full_name }}</span>
                                    <span class="doctor-email">{{ doc.email }}</span>
                                    <div class="doctor-badges">
                                        <span :class="['status-badge', doc.approved ? 'badge-approved' : 'badge-pending']">
                                            {{ doc.approved ? '✓ Approved' : '⏳ Pending' }}
                                        </span>
                                        <span v-if="doc.is_research" class="status-badge badge-research">Research</span>
                                    </div>
                                </div>
                                <div class="doctor-actions">
                                    <button v-if="!doc.approved" class="action-btn approve-btn"
                                        @click="approveDoctor(doc.id)" :disabled="actionLoading === doc.id">
                                        {{ actionLoading === doc.id ? '...' : '✓ Approve' }}
                                    </button>
                                    <button v-else class="action-btn unapprove-btn"
                                        @click="unapproveDoctor(doc.id)" :disabled="actionLoading === doc.id">
                                        {{ actionLoading === doc.id ? '...' : '✗ Revoke' }}
                                    </button>
                                    <button class="action-btn delete-btn"
                                        @click="deleteDoctor(doc.id, doc.full_name)" :disabled="actionLoading === doc.id">
                                        🗑
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Health center management -->
                    <div class="section-card">
                        <div class="admin-section-header">
                            <h4 class="section-title" style="margin-bottom:0">Health Centers</h4>
                            <button class="refresh-btn" @click="loadAdmin">⟳ Refresh</button>
                        </div>
                        <div v-if="adminHCs.length === 0" class="empty-state">No health centers registered.</div>
                        <table v-else class="data-table">
                            <thead><tr><th>Name</th><th>Specialty</th><th>Center ID</th><th>Created</th><th></th></tr></thead>
                            <tbody>
                                <tr v-for="hc in adminHCs" :key="hc.id">
                                    <td>{{ hc.name }}</td>
                                    <td><span :class="['specialty-chip', hc.specialty]">{{ hc.specialty || '—' }}</span></td>
                                    <td><code class="center-id-code">{{ hc.center_id || '—' }}</code></td>
                                    <td>{{ hc.created_at ? hc.created_at.slice(0,10) : '' }}</td>
                                    <td>
                                        <button class="action-btn delete-btn" @click="deleteHC(hc.id, hc.name)">🗑</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <p class="admin-note">To register a new health center, run <code>python3 ~/register_hc.py</code> on the Pi.</p>
                    </div>

                    <!-- AI Threshold Controls -->
                    <div class="section-card">
                        <h4 class="section-title">AI Thresholds <span class="section-sub">(applies to future uploads only)</span></h4>
                        <p class="threshold-info">Changes here affect new uploads going forward. Past results are never altered.</p>
                        <div v-if="thresholdsLoading" class="threshold-loading">Loading thresholds...</div>
                        <div v-else class="threshold-grid">
                            <div class="threshold-group">
                                <p class="threshold-group-title">HC Display Thresholds <span class="threshold-group-sub">Min confidence to show "Referral" vs "Inconclusive" to health center</span></p>
                                <div class="threshold-row">
                                    <span class="thr-label">Glaucoma</span>
                                    <input type="range" min="50" max="99" step="1" v-model.number="thresholds.hc_threshold_glaucoma" class="thr-slider" />
                                    <span class="thr-value" :class="thresholdColor(thresholds.hc_threshold_glaucoma)">{{ thresholds.hc_threshold_glaucoma }}%</span>
                                </div>
                                <div class="threshold-row">
                                    <span class="thr-label">DR</span>
                                    <input type="range" min="50" max="99" step="1" v-model.number="thresholds.hc_threshold_dr" class="thr-slider" />
                                    <span class="thr-value" :class="thresholdColor(thresholds.hc_threshold_dr)">{{ thresholds.hc_threshold_dr }}%</span>
                                </div>
                                <div class="threshold-row">
                                    <span class="thr-label">AMD</span>
                                    <input type="range" min="50" max="99" step="1" v-model.number="thresholds.hc_threshold_amd" class="thr-slider" />
                                    <span class="thr-value" :class="thresholdColor(thresholds.hc_threshold_amd)">{{ thresholds.hc_threshold_amd }}%</span>
                                </div>
                            </div>
                            <div class="threshold-group">
                                <p class="threshold-group-title">Expert Routing Thresholds <span class="threshold-group-sub">Min confidence to route image to expert for review</span></p>
                                <div class="threshold-row">
                                    <span class="thr-label">Glaucoma</span>
                                    <input type="range" min="50" max="99" step="1" v-model.number="thresholds.expert_threshold_glaucoma" class="thr-slider" />
                                    <span class="thr-value" :class="thresholdColor(thresholds.expert_threshold_glaucoma)">{{ thresholds.expert_threshold_glaucoma }}%</span>
                                </div>
                                <div class="threshold-row">
                                    <span class="thr-label">DR</span>
                                    <input type="range" min="50" max="99" step="1" v-model.number="thresholds.expert_threshold_dr" class="thr-slider" />
                                    <span class="thr-value" :class="thresholdColor(thresholds.expert_threshold_dr)">{{ thresholds.expert_threshold_dr }}%</span>
                                </div>
                                <div class="threshold-row">
                                    <span class="thr-label">AMD</span>
                                    <input type="range" min="50" max="99" step="1" v-model.number="thresholds.expert_threshold_amd" class="thr-slider" />
                                    <span class="thr-value" :class="thresholdColor(thresholds.expert_threshold_amd)">{{ thresholds.expert_threshold_amd }}%</span>
                                </div>
                            </div>
                        </div>
                        <div class="threshold-actions">
                            <transition name="save-flash">
                                <span v-if="thresholdSaved" class="threshold-saved">✓ Saved</span>
                            </transition>
                            <button class="thr-save-btn" @click="saveThresholds" :disabled="thresholdSaving">
                                {{ thresholdSaving ? 'Saving...' : 'Save Thresholds' }}
                            </button>
                        </div>
                    </div>

                    <!-- ── Danger Zone ── -->
                    <div class="section-card danger-zone-card">
                        <h4 class="section-title danger-title">⚠ Danger Zone</h4>
                        <p class="danger-desc">These actions are destructive and cannot be undone. Use with caution.</p>
                        <div class="danger-actions">
                            <div class="danger-action-item">
                                <div class="danger-action-info">
                                    <span class="danger-action-label">Delete Pending Examinations</span>
                                    <span class="danger-action-sub">Removes all HC uploads that have not yet been reviewed by any expert.</span>
                                </div>
                                <button class="danger-btn" @click="showDeletePendingModal = true">Delete Pending</button>
                            </div>
                            <div class="danger-action-item">
                                <div class="danger-action-info">
                                    <span class="danger-action-label">Reset All Study Data</span>
                                    <span class="danger-action-sub">Permanently deletes all reviews, diagnoses, biomarker records and uploaded images.</span>
                                </div>
                                <button class="danger-btn danger-btn-strong" @click="showResetModal = true">Reset Study</button>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- ═══════════ IMAGE DETAIL MODAL ═══════════ -->
        <transition name="zoom-fade">
            <div v-if="detailImage" class="zoom-backdrop" @click.self="detailImage = null">
                <div class="detail-box">
                    <div class="detail-toolbar">
                        <span class="zoom-title">Image #{{ detailImage.image_id }} — {{ conditionLabel }}</span>
                        <button class="zoom-close-btn" @click="detailImage = null">✕ Close</button>
                    </div>
                    <div class="detail-body">
                        <!-- Left: image -->
                        <div class="detail-img-col">
                            <div class="detail-img-wrap" v-if="!zoomError">
                                <img :src="thumbSrc(detailImage.image_id)" class="detail-img-full"
                                    draggable="false" @error="zoomError = true" />
                            </div>
                            <div v-else class="zoom-error">Image could not be loaded.</div>
                            <div class="detail-ai-row">
                                <span class="detail-ai-label">AI Result:</span>
                                <span class="ai-chip" :class="aiChipClass(detailImage.ai_result)">{{ detailImage.ai_result }}</span>
                            </div>
                        </div>

                        <!-- Right: reviews -->
                        <div class="detail-reviews-col">
                            <h5 class="detail-reviews-title">Doctor Reviews ({{ detailImage.total_reviews }})</h5>

                            <div v-if="detailImage.total_reviews === 0" class="empty-state" style="padding:20px">
                                No reviews yet for this image.
                            </div>

                            <div v-else class="detail-reviews-list" :class="{ 'detail-reviews-side-by-side': Object.keys(detailImage.doctor_answers).length >= 2 }">
                                <div v-for="(answer, docName) in detailImage.doctor_answers" :key="docName" class="detail-review-row">
                                    <div class="detail-review-header">
                                        <span class="detail-doc-name">Dr. {{ docName }}</span>
                                        <span :class="['answer-chip', answer === detailImage.ai_result ? 'chip-match' : 'chip-differ']">
                                            {{ answer }}
                                        </span>
                                        <span :class="answer === detailImage.ai_result ? 'match-yes' : 'match-no'" style="font-size:11px">
                                            {{ answer === detailImage.ai_result ? '✓ Matches AI' : '✗ Differs from AI' }}
                                        </span>
                                    </div>
                                    <!-- Biomarkers for this doctor + image -->
                                    <div v-if="getBiomarkersFor(detailImage.image_id, docName)" class="detail-biomarkers">
                                        <div class="bio-markers-grid" style="margin-top:4px">
                                            <div v-for="(val, key) in getBiomarkersFor(detailImage.image_id, docName)"
                                                :key="key" class="bio-marker-item" :class="'bm-' + val">
                                                <span class="bm-key">{{ key.replace(/_/g, ' ') }}</span>
                                                <span class="bm-val">{{ val }}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else class="bio-no-markers">No biomarkers recorded.</div>
                                </div>
                            </div>

                            <div v-if="detailImage.inter_rater_pct !== null" class="detail-stats-row">
                                <span class="detail-stat-label">Inter-Rater Agreement:</span>
                                <span :class="['pct-badge', detailImage.inter_rater_pct >= 80 ? 'pct-good' : detailImage.inter_rater_pct >= 50 ? 'pct-mid' : 'pct-low']">
                                    {{ detailImage.inter_rater_pct }}%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <!-- HC Image Detail Modal -->
        <transition name="zoom-fade">
            <div v-if="hcDetail" class="zoom-backdrop" @click.self="hcDetail = null">
                <div class="detail-box">
                    <div class="detail-toolbar">
                        <span class="zoom-title">Image #{{ hcDetail.upload_id }} — AMKA: {{ hcDetail.patient_amka }} | {{ hcDetail.center_name }}</span>
                        <div style="display:flex;gap:8px;align-items:center;">
                            <button class="delete-upload-btn" @click="deleteUpload(hcDetail.upload_id)" :disabled="deletingUploadId === hcDetail.upload_id">
                                {{ deletingUploadId === hcDetail.upload_id ? 'Deleting...' : '🗑 Delete Image' }}
                            </button>
                            <button class="zoom-close-btn" @click="hcDetail = null">✕ Close</button>
                        </div>
                    </div>
                    <div class="detail-body">
                        <!-- Left: image + AI result for this specialty only -->
                        <div class="detail-img-col">
                            <div class="detail-img-wrap">
                                <img :src="hcThumbSrc(hcDetail.upload_id)" class="detail-img-full"
                                    draggable="false" @error="e => e.target.style.display='none'" />
                            </div>
                            <div style="margin-top:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">
                                <span style="font-size:12px;color:#718096;font-weight:600;text-transform:capitalize">{{ hcDetail.specialty }} AI:</span>
                                <span class="ai-chip" :class="aiChipClass(hcDetail.ai_result)">{{ hcDetail.ai_result }}</span>
                                <span :class="['conf-badge', hcDetail.ai_conf >= confThreshold ? 'conf-high' : 'conf-low']">{{ hcDetail.ai_conf }}%</span>
                            </div>
                        </div>
                        <!-- Right: all expert reviews for this specialty -->
                        <div class="detail-reviews-col">
                            <h5 class="detail-reviews-title">Expert Reviews ({{ hcDetail.reviews.length }})</h5>
                            <div v-if="hcDetail.reviews.length === 0" class="empty-state" style="padding:20px">Not yet reviewed by any expert.</div>
                            <div v-else class="detail-reviews-list" :class="{ 'detail-reviews-side-by-side': hcDetail.reviews.length >= 2 }">
                                <div v-for="r in hcDetail.reviews" :key="r.reviewer" class="detail-review-row">
                                    <div class="detail-review-header">
                                        <span class="detail-doc-name">Dr. {{ r.reviewer }}</span>
                                        <span style="font-size:11px;color:#a0aec0;margin-left:auto">{{ r.reviewed_at ? r.reviewed_at.slice(0,10) : '' }}</span>
                                    </div>
                                    <div style="display:flex;align-items:center;gap:8px;margin-top:8px;flex-wrap:wrap">
                                        <span style="font-size:12px;color:#718096;font-weight:600;text-transform:capitalize">{{ hcDetail.specialty }}:</span>
                                        <span :class="['answer-chip', r.answer === hcDetail.ai_result ? 'chip-match' : 'chip-differ']">{{ r.answer || '—' }}</span>
                                        <span :class="r.answer === hcDetail.ai_result ? 'match-yes' : 'match-no'">{{ r.answer === hcDetail.ai_result ? '✓ matches AI' : '✗ differs from AI' }}</span>
                                    </div>
                                    <!-- Biomarkers for this doctor -->
                                    <div v-if="getBiomarkersFor(hcDetail.upload_id, r.reviewer)" class="detail-biomarkers" style="margin-top:10px">
                                        <p style="font-size:10px;font-weight:700;color:#a0aec0;text-transform:uppercase;letter-spacing:0.5px;margin:0 0 6px">Biomarkers</p>
                                        <div class="bio-markers-grid">
                                            <div v-for="(val, key) in getBiomarkersFor(hcDetail.upload_id, r.reviewer)"
                                                :key="key" class="bio-marker-item" :class="'bm-' + val">
                                                <span class="bm-key">{{ key.replace(/_/g, ' ') }}</span>
                                                <span class="bm-val">{{ val }}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else class="bio-no-markers" style="margin-top:8px">No biomarkers recorded.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <!-- Reset study modal -->
        <transition name="modal-fade">
            <div v-if="showResetModal" class="modal-backdrop">
                <div class="modal-box">
                    <h3 style="color:#c53030;margin:0;">⚠ Reset Study Data</h3>
                    <p style="text-align:center;color:#718096;font-size:13px;">This will permanently delete all reviews, diagnoses and biomarker records. This <strong>cannot</strong> be undone.</p>
                    <div class="field">
                        <input v-model="resetCode" type="password" placeholder="Enter admin reset code" @keyup.enter="resetStudy" />
                    </div>
                    <p v-if="resetError" class="error">{{ resetError }}</p>
                    <button class="submit-btn" style="background:#c53030" @click="resetStudy" :disabled="resetLoading">
                        {{ resetLoading ? 'Resetting...' : 'Confirm Reset' }}
                    </button>
                    <button class="back-btn" @click="showResetModal = false; resetCode = ''; resetError = ''">Cancel</button>
                </div>
            </div>
        </transition>

        <!-- Delete pending examinations modal -->
        <transition name="modal-fade">
            <div v-if="showDeletePendingModal" class="modal-backdrop">
                <div class="modal-box">
                    <h3 style="color:#c53030;margin:0;">⚠ Delete Pending Examinations</h3>
                    <p style="text-align:center;color:#718096;font-size:13px;">This will permanently delete all HC uploads that have <strong>not yet been reviewed</strong> by any expert. This <strong>cannot</strong> be undone.</p>
                    <div class="field">
                        <input v-model="deletePendingCode" type="password" placeholder="Enter admin access code" @keyup.enter="deletePendingExams" />
                    </div>
                    <p v-if="deletePendingError" class="error">{{ deletePendingError }}</p>
                    <button class="submit-btn" style="background:#c53030" @click="deletePendingExams" :disabled="deletePendingLoading">
                        {{ deletePendingLoading ? 'Deleting...' : 'Confirm Delete' }}
                    </button>
                    <button class="back-btn" @click="showDeletePendingModal = false; deletePendingCode = ''; deletePendingError = ''">Cancel</button>
                </div>
            </div>
        </transition>



        <!-- Inconclusive Studies Modal -->
        <transition name="modal-fade">
            <div v-if="showInconclusiveModal" class="modal-backdrop" @click.self="showInconclusiveModal = false">
                <div class="inconclusive-modal-box">
                    <div class="inconclusive-modal-header">
                        <h3>⚠ Inconclusive Studies</h3>
                        <button class="zoom-close-btn" @click="showInconclusiveModal = false">✕ Close</button>
                    </div>
                    <div v-if="inconclusiveLoading" class="loading-state"><div class="spinner"></div><p>Loading...</p></div>
                    <div v-else-if="inconclusiveRows.length === 0" class="empty-state">No inconclusive studies submitted yet.</div>
                    <div v-else class="inconclusive-list">
                        <div v-for="row in inconclusiveRows" :key="row.id" class="inconclusive-item">
                            <div class="inconclusive-item-header">
                                <span class="inconclusive-amka">{{ row.patient_amka }}</span>
                                <span class="inconclusive-center">{{ row.center_name }}</span>
                                <span :class="['specialty-chip', row.specialty]">{{ row.specialty || '—' }}</span>
                                <span class="inconclusive-doctor">Dr. {{ row.doctor_name }}</span>
                                <span class="inconclusive-date">{{ row.reviewed_at ? row.reviewed_at.slice(0,10) : '' }}</span>
                            </div>
                            <div v-if="row.biomarkers && Object.keys(row.biomarkers).length > 0" class="bio-markers-grid" style="margin-top:8px">
                                <div v-for="(val, key) in row.biomarkers" :key="key" class="bio-marker-item" :class="'bm-' + val">
                                    <span class="bm-key">{{ key.replace(/_/g, ' ') }}</span>
                                    <span class="bm-val">{{ val }}</span>
                                </div>
                            </div>
                            <p v-else class="bio-no-markers">No biomarkers recorded.</p>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <div v-if="authenticated" class="footer">
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
            authenticated: false,
            codeInput: '',
            authError: '',
            authLoading: false,
            mainTab: 'study',
            tab: 'general',
            loading: false,
            stats: {
                doctors: [],
                general: {
                    total_images: 0, total_reviews: 0, hc_total_reviewed: 0,
                    inter_rater_glaucoma: 0, inter_rater_dr: 0, inter_rater_amd: 0,
                    ai_agree_glaucoma: 0, ai_agree_dr: 0, ai_agree_amd: 0,
                    prevalence_glaucoma: 0, prevalence_dr: 0, prevalence_amd: 0,
                    hc_ai_agree_glaucoma: 0, hc_ai_agree_dr: 0, hc_ai_agree_amd: 0,
                    referral_other_count: 0, referral_other_pct: 0,
                    ref_ext_glaucoma: null, ref_ext_dr: null, ref_ext_amd: null
                },
                glaucoma_rows: [], dr_rows: [], amd_rows: [], hc_rows: [],
                hc_upload_counts: []
            },
            bioRows: [],
            timelineWeeks: [],
            timelineLoading: false,
            timelineChart: null,
            exportLoading: false,
            confThreshold: 90,
            bioLoading: false,
            bioFilter: 'all',
            conditionFilter: 'all',
            // image detail modal
            detailImage: null,
            hcDetail: null,
            zoomError: false,
            // admin
            adminLoading: false,
            thresholds: {
                hc_threshold_glaucoma: 85,
                hc_threshold_dr: 75,
                hc_threshold_amd: 80,
                expert_threshold_glaucoma: 90,
                expert_threshold_dr: 90,
                expert_threshold_amd: 90
            },
            thresholdsLoading: false,
            thresholdSaving: false,
            thresholdSaved: false,
            adminDoctors: [],
            adminHCs: [],
            actionLoading: null,
            // reset
            showResetModal: false,
            resetCode: '',
            resetError: '',
            resetLoading: false,
            showDeletePendingModal: false,
            deletePendingCode: '',
            deletePendingError: '',
            deletePendingLoading: false,
            deletingUploadId: null,
            showInconclusiveModal: false,
            inconclusiveRows: [],
            inconclusiveLoading: false
        }
    },

    async created() {
        if (!window.Chart) {
            await new Promise((resolve, reject) => {
                const s = document.createElement('script')
                s.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js'
                s.onload = resolve; s.onerror = reject
                document.head.appendChild(s)
            })
        }
    },

    computed: {
        overallInterRater() {
            const g = this.stats.general
            const vals = [g.inter_rater_glaucoma, g.inter_rater_dr, g.inter_rater_amd].filter(v => v > 0)
            return vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0
        },
        currentRows() {
            if (this.tab === 'glaucoma') return this.stats.glaucoma_rows
            if (this.tab === 'dr') return this.stats.dr_rows
            if (this.tab === 'amd') return this.stats.amd_rows
            return []
        },
        filteredConditionRows() {
            const rows = this.currentRows
            if (this.conditionFilter === 'reviewed') return rows.filter(r => r.total_reviews > 0)
            if (this.conditionFilter === 'unreviewed') return rows.filter(r => r.total_reviews === 0)
            if (this.conditionFilter === 'agree') return rows.filter(r => r.ai_agree_count === r.total_reviews && r.total_reviews > 0)
            if (this.conditionFilter === 'disagree') return rows.filter(r => r.ai_agree_count < r.total_reviews && r.total_reviews > 0)
            return rows
        },
        conditionLabel() {
            return { glaucoma: 'Glaucoma', dr: 'Diabetic Retinopathy', amd: 'AMD' }[this.tab] || ''
        },
        maxReviewed() {
            return Math.max(...this.stats.doctors.map(d => d.reviewed), 1)
        },
        maxHCUploads() {
            if (!this.stats.hc_upload_counts || !this.stats.hc_upload_counts.length) return 1
            return Math.max(...this.stats.hc_upload_counts.map(h => h.total), 1)
        },
        filteredBioRows() {
            const rows = this.bioRows
            if (this.bioFilter === 'all') return rows
            return rows.filter(r => {
                if (this.bioFilter === 'glaucoma') return r.doctor_glaucoma && r.doctor_glaucoma !== 'N/A'
                if (this.bioFilter === 'dr') return r.doctor_dr && r.doctor_dr !== 'N/A'
                if (this.bioFilter === 'amd') return r.doctor_amd && r.doctor_amd !== 'N/A'
                return true
            })
        },
        groupedBioRows() {
            const rows = this.filteredBioRows
            const map = new Map()
            for (const row of rows) {
                const key = row.upload_id || row.image_id || row.id
                if (!map.has(key)) {
                    map.set(key, {
                        upload_id: key,
                        patient_amka: row.patient_amka,
                        center_name: row.center_name,
                        reviews: []
                    })
                }
                map.get(key).reviews.push(row)
            }
            return [...map.values()]
        },
        hcRowsForCondition() {
            if (!this.stats.hc_rows) return []
            return this.stats.hc_rows
        },
        // Group HC rows by upload_id, filtered to only the specialty matching the current tab
        groupedHCRows() {
            const tab = this.tab
            const aiCol = 'ai_' + tab
            const confCol = 'ai_' + tab + '_conf'
            const docCol = 'doctor_' + tab
            const map = {}
            for (const h of this.hcRowsForCondition) {
                // Only show uploads from health centers whose specialty matches this tab
                if ((h.specialty || '').toLowerCase() !== tab) continue
                if (!map[h.id]) {
                    map[h.id] = {
                        upload_id: h.id,
                        patient_amka: h.patient_amka,
                        center_name: h.center_name,
                        specialty: h.specialty,
                        ai_result: h[aiCol],
                        ai_conf: h[confCol],
                        reviews: []
                    }
                }
                if (h.reviewer) {
                    map[h.id].reviews.push({
                        reviewer: h.reviewer,
                        answer: h[docCol],
                        reviewed_at: h.reviewed_at
                    })
                }
            }
            return Object.values(map).map(g => ({
                ...g,
                agreeCount: g.reviews.filter(r => r.answer === g.ai_result).length,
                allAgree: g.reviews.length > 0 && g.reviews.every(r => r.answer === g.ai_result),
                anyAgree: g.reviews.some(r => r.answer === g.ai_result)
            }))
        },
        filteredHCRows() {
            const rows = this.groupedHCRows
            if (this.conditionFilter === 'reviewed') return rows.filter(g => g.reviews.length > 0)
            if (this.conditionFilter === 'unreviewed') return rows.filter(g => g.reviews.length === 0)
            if (this.conditionFilter === 'agree') return rows.filter(g => g.allAgree)
            if (this.conditionFilter === 'disagree') return rows.filter(g => g.reviews.length > 0 && !g.allAgree)
            if (this.conditionFilter === 'highconf') return rows.filter(g => g.ai_conf >= this.confThreshold)
            return rows
        },
        totalReviewsForCondition() {
            return this.currentRows.reduce((s, r) => s + r.total_reviews, 0)
        },
        maxReviewed() {
            if (!this.stats.doctors || !this.stats.doctors.length) return 1
            return Math.max(...this.stats.doctors.map(d => d.reviewed), 1)
        },
        conditionAIAgree() {
            const rows = this.currentRows.filter(r => r.total_reviews > 0)
            if (!rows.length) return 0
            const total = rows.reduce((s, r) => s + r.total_reviews, 0)
            const agree = rows.reduce((s, r) => s + r.ai_agree_count, 0)
            return Math.round(agree / total * 100)
        },
        conditionInterRater() {
            const key = { glaucoma: 'inter_rater_glaucoma', dr: 'inter_rater_dr', amd: 'inter_rater_amd' }[this.tab]
            return this.stats.general[key] || 0
        }
    },

    methods: {
        async authenticate() {
            if (!this.codeInput) return
            this.authLoading = true
            this.authError = ''
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/stats?code=${encodeURIComponent(this.codeInput)}&conf_threshold=${this.confThreshold}`)
                if (!res.ok) { this.authError = 'Invalid access code.'; return }
                const data = await res.json()
                this.stats = data
                this.authenticated = true
                this.loadBiomarkers()
                this.loadTimeline()
            } catch { this.authError = 'Connection failed.' }
            finally { this.authLoading = false }
        },

        async loadStats() {
            this.loading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/stats?code=${encodeURIComponent(this.codeInput)}&conf_threshold=${this.confThreshold}`)
                const data = await res.json()
                this.stats = data
            } catch { } finally { this.loading = false }
        },

        async switchTab(t) {
            this.tab = t
            if (t === 'biomarkers') {
                await this.loadBiomarkers()
            } else {
                await this.loadStats()
                if (t === 'general') {
                    await this.loadTimeline()
                }
            }
        },

        async loadBiomarkers() {
            this.bioLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/biomarkers?code=${encodeURIComponent(this.codeInput)}`)
                if (!res.ok) { console.error('Biomarkers fetch failed:', res.status); return }
                const data = await res.json()
                console.log('Biomarkers raw:', data)
                this.bioRows = (data.rows || []).map(r => {
                    let bm = null
                    try {
                        if (r.biomarkers && r.biomarkers !== 'null' && r.biomarkers !== '{}') {
                            bm = typeof r.biomarkers === 'string' ? JSON.parse(r.biomarkers) : r.biomarkers
                            if (bm && Object.keys(bm).length === 0) bm = null
                        }
                    } catch(e) { bm = null }
                    return { ...r, biomarkers: bm }
                })
                console.log('Biomarkers parsed rows:', this.bioRows.length)
            } catch(e) { console.error('Biomarkers error:', e) } finally { this.bioLoading = false }
        },

        isReferral(aiResult, condition) {
            if (condition === 'glaucoma') return aiResult === 'Glaucoma'
            if (condition === 'dr') return aiResult !== 'No_DR' && aiResult !== null && aiResult !== ''
            if (condition === 'amd') return aiResult === 'AMD'
            return false
        },

        thresholdColor(val) {
            if (val >= 85) return 'thr-high'
            if (val >= 70) return 'thr-mid'
            return 'thr-low'
        },

        async loadThresholds() {
            this.thresholdsLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/settings?code=${encodeURIComponent(this.codeInput)}`)
                if (res.ok) {
                    const data = await res.json()
                    this.thresholds = {
                        hc_threshold_glaucoma: data.hc_threshold_glaucoma ?? 85,
                        hc_threshold_dr: data.hc_threshold_dr ?? 75,
                        hc_threshold_amd: data.hc_threshold_amd ?? 80,
                        expert_threshold_glaucoma: data.expert_threshold_glaucoma ?? 90,
                        expert_threshold_dr: data.expert_threshold_dr ?? 90,
                        expert_threshold_amd: data.expert_threshold_amd ?? 90
                    }
                }
            } catch {}
            finally { this.thresholdsLoading = false }
        },

        async saveThresholds() {
            this.thresholdSaving = true
            this.thresholdSaved = false
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/settings?code=${encodeURIComponent(this.codeInput)}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.thresholds)
                })
                if (res.ok) {
                    this.thresholdSaved = true
                    setTimeout(() => { this.thresholdSaved = false }, 2500)
                }
            } catch {}
            finally { this.thresholdSaving = false }
        },

        async loadAdmin() {
            this.adminLoading = true
            try {
                const [docRes, hcRes] = await Promise.all([
                    fetch('https://labiris.myiplist.com/admin/doctors'),
                    fetch('https://labiris.myiplist.com/admin/health-centers')
                ])
                const docData = await docRes.json()
                const hcData = await hcRes.json()
                this.adminDoctors = docData.doctors || []
                this.adminHCs = hcData.health_centers || []
            } catch { } finally { this.adminLoading = false }
        },

        async approveDoctor(id) {
            this.actionLoading = id
            try {
                await fetch(`https://labiris.myiplist.com/admin/approve/${id}`, { method: 'POST' })
                await this.loadAdmin()
            } finally { this.actionLoading = null }
        },

        async unapproveDoctor(id) {
            this.actionLoading = id
            try {
                await fetch(`https://labiris.myiplist.com/admin/unapprove/${id}`, { method: 'POST' })
                await this.loadAdmin()
            } finally { this.actionLoading = null }
        },

        async deleteDoctor(id, name) {
            if (!confirm(`Delete Dr. ${name}? This cannot be undone.`)) return
            this.actionLoading = id
            try {
                await fetch(`https://labiris.myiplist.com/admin/doctor/${id}`, { method: 'DELETE' })
                await this.loadAdmin()
            } finally { this.actionLoading = null }
        },

        async deleteHC(id, name) {
            if (!confirm(`Delete health center "${name}"? This cannot be undone.`)) return
            try {
                await fetch(`https://labiris.myiplist.com/admin/health-center/${id}`, { method: 'DELETE' })
                await this.loadAdmin()
            } catch { }
        },

        openImageDetail(row) {
            this.zoomError = false
            this.detailImage = row
        },

        openHCDetail(g) {
            this.zoomError = false
            this.hcDetail = g
        },

        thumbSrc(imageId) {
            return `https://labiris.myiplist.com/research/image/${imageId}`
        },

        hcThumbSrc(uploadId) {
            // HC images need doctor_id — use a known approved doctor or just try
            return `https://labiris.myiplist.com/study/hc-image/${uploadId}?code=${encodeURIComponent(this.codeInput)}`
        },

        getBiomarkersFor(imageId, docName) {
            const row = this.bioRows.find(r => (r.upload_id === imageId || r.image_id === imageId) && r.doctor_name === docName)
            if (!row || !row.biomarkers) return null
            const bm = typeof row.biomarkers === 'string' ? JSON.parse(row.biomarkers) : row.biomarkers
            return Object.keys(bm).length > 0 ? bm : null
        },

        exportBiomarkersCSV() {
            const rows = this.filteredBioRows
            if (!rows.length) return
            // Collect all biomarker keys
            const bmKeys = new Set()
            rows.forEach(r => { if (r.biomarkers) Object.keys(r.biomarkers).forEach(k => bmKeys.add(k)) })
            const keys = [...bmKeys]
            const headers = ['Image ID', 'Doctor', 'Date', 'Glaucoma', 'DR', 'AMD', ...keys.map(k => k.replace(/_/g, ' '))]
            const lines = [headers.join(',')]
            rows.forEach(r => {
                const bm = r.biomarkers || {}
                const row = [
                    r.image_id, `"${r.doctor_name}"`,
                    r.reviewed_at ? r.reviewed_at.slice(0, 10) : '',
                    r.doctor_glaucoma || '', r.doctor_dr || '', r.doctor_amd || '',
                    ...keys.map(k => bm[k] || '')
                ]
                lines.push(row.join(','))
            })
            const blob = new Blob([lines.join('\n')], { type: 'text/csv' })
            const a = document.createElement('a')
            a.href = URL.createObjectURL(blob)
            a.download = `ddart_biomarkers_${new Date().toISOString().slice(0, 10)}.csv`
            a.click()
        },

        exportBiomarkersExcel() {
            // Build HTML table then use data URI (works without SheetJS)
            const rows = this.filteredBioRows
            if (!rows.length) return
            const bmKeys = new Set()
            rows.forEach(r => { if (r.biomarkers) Object.keys(r.biomarkers).forEach(k => bmKeys.add(k)) })
            const keys = [...bmKeys]
            const headers = ['Image ID', 'Doctor', 'Date', 'Glaucoma', 'DR', 'AMD', ...keys.map(k => k.replace(/_/g, ' '))]

            let html = '<table><tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr>'
            rows.forEach(r => {
                const bm = r.biomarkers || {}
                const cells = [
                    r.image_id, r.doctor_name,
                    r.reviewed_at ? r.reviewed_at.slice(0, 10) : '',
                    r.doctor_glaucoma || '', r.doctor_dr || '', r.doctor_amd || '',
                    ...keys.map(k => bm[k] || '')
                ]
                html += '<tr>' + cells.map(c => `<td>${c}</td>`).join('') + '</tr>'
            })
            html += '</table>'

            const blob = new Blob([`<html><head><meta charset="UTF-8"></head><body>${html}</body></html>`],
                { type: 'application/vnd.ms-excel' })
            const a = document.createElement('a')
            a.href = URL.createObjectURL(blob)
            a.download = `ddart_biomarkers_${new Date().toISOString().slice(0, 10)}.xls`
            a.click()
        },

        async resetStudy() {
            if (!this.resetCode) { this.resetError = 'Please enter the reset code.'; return }
            this.resetLoading = true
            this.resetError = ''
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/reset?code=${encodeURIComponent(this.resetCode)}`, { method: 'POST' })
                if (!res.ok) { this.resetError = 'Invalid code or reset failed.'; return }
                this.showResetModal = false
                this.resetCode = ''
                await this.loadStats()
                this.bioRows = []
                alert('Study data has been reset successfully.')
            } catch { this.resetError = 'Connection failed.' }
            finally { this.resetLoading = false }
        },

        async deleteUpload(uploadId) {
            if (!confirm('Permanently delete this image and all its reviews? This cannot be undone.')) return
            this.deletingUploadId = uploadId
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/delete-upload/${uploadId}?code=${encodeURIComponent(this.codeInput)}`, { method: 'DELETE' })
                if (!res.ok) { alert('Delete failed.'); return }
                this.hcDetail = null
                await this.loadStats()
                // Remove from local hc_rows so table updates immediately
                if (this.stats.hc_rows) {
                    this.stats.hc_rows = this.stats.hc_rows.filter(r => r.id !== uploadId)
                }
            } catch { alert('Connection failed.') }
            finally { this.deletingUploadId = null }
        },

        async loadInconclusive() {
            this.inconclusiveLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/inconclusive?code=${encodeURIComponent(this.codeInput)}`)
                if (!res.ok) return
                const data = await res.json()
                this.inconclusiveRows = (data.rows || []).map(r => {
                    let bm = null
                    try {
                        if (r.biomarkers && r.biomarkers !== 'null' && r.biomarkers !== '{}') {
                            bm = typeof r.biomarkers === 'string' ? JSON.parse(r.biomarkers) : r.biomarkers
                            if (bm && Object.keys(bm).length === 0) bm = null
                        }
                    } catch { bm = null }
                    return { ...r, biomarkers: bm }
                })
            } catch (e) { console.error(e) }
            finally { this.inconclusiveLoading = false }
        },

        async deletePendingExams() {
            if (!this.deletePendingCode) { this.deletePendingError = 'Please enter the access code.'; return }
            this.deletePendingLoading = true
            this.deletePendingError = ''
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/delete-pending?code=${encodeURIComponent(this.deletePendingCode)}`, { method: 'POST' })
                if (!res.ok) { this.deletePendingError = 'Invalid code or deletion failed.'; return }
                const data = await res.json()
                this.showDeletePendingModal = false
                this.deletePendingCode = ''
                await this.loadStats()
                alert(`Deleted ${data.deleted ?? 'all'} pending examinations successfully.`)
            } catch { this.deletePendingError = 'Connection failed.' }
            finally { this.deletePendingLoading = false }
        },

        logout() {
            localStorage.removeItem('ddart_study')
            this.authenticated = false
            this.codeInput = ''
            sessionStorage.setItem('ddart_logout_anim', '1')
            this.$router.push('/login')
        },

        ringStyle(pct) {
            const color = pct >= 80 ? '#38a169' : pct >= 60 ? '#d69e2e' : '#e53e3e'
            const deg = Math.round(pct / 100 * 360)
            return { background: `conic-gradient(${color} ${deg}deg, #e2e8f0 ${deg}deg)` }
        },

        prevPct(count) {
            if (!this.stats.general.total_images) return 0
            return Math.round(count / this.stats.general.total_images * 100)
        },

        toggleConfThreshold() {
            this.confThreshold = this.confThreshold === 90 ? 70 : 90
            this.loadStats()
        },

        aiChipClass(val) {
            if (!val) return ''
            const positive = ['Glaucoma', 'AMD', 'Mild', 'Moderate', 'Severe', 'Proliferative DR', 'Proliferate_DR']
            return positive.includes(val) ? 'chip-positive' : 'chip-negative'
        },

        async loadTimeline() {
            this.timelineLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/timeline?code=${encodeURIComponent(this.codeInput)}`)
                const data = await res.json()
                this.timelineWeeks = data.weeks || []
                await this.$nextTick()
                this.renderTimelineChart()
            } catch(e) { console.error(e) }
            finally { this.timelineLoading = false }
        },

        renderTimelineChart() {
            const canvas = this.$refs.timelineChart
            if (!canvas || !this.timelineWeeks.length) return
            if (this.timelineChart) { this.timelineChart.destroy(); this.timelineChart = null }
            const labels = this.timelineWeeks.map(w => w.week)
            const values = this.timelineWeeks.map(w => w.count)
            this.timelineChart = new Chart(canvas.getContext('2d'), {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Reviews',
                        data: values,
                        backgroundColor: 'rgba(43,108,176,0.7)',
                        borderColor: '#2b6cb0',
                        borderWidth: 1,
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1, font: { size: 11 } }, grid: { color: 'rgba(0,0,0,0.05)' } },
                        x: { ticks: { font: { size: 10 } }, grid: { display: false } }
                    }
                }
            })
        },

        async exportFullCSV() {
            this.exportLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/export?code=${encodeURIComponent(this.codeInput)}`)
                const data = await res.json()
                const rows = data.rows || []
                if (!rows.length) { alert('No data to export.'); return }

                // Collect all biomarker keys
                const bmKeys = new Set()
                rows.forEach(r => {
                    if (r.biomarkers) {
                        try {
                            const bm = typeof r.biomarkers === 'string' ? JSON.parse(r.biomarkers) : r.biomarkers
                            Object.keys(bm).forEach(k => bmKeys.add(k))
                        } catch {}
                    }
                })
                const bmArr = [...bmKeys]

                const headers = ['Upload ID','Patient AMKA','Uploaded At','Health Center','Specialty',
                    'AI Glaucoma','AI Glaucoma Conf%','AI DR','AI DR Conf%','AI AMD','AI AMD Conf%',
                    'Reviewer','Expert Glaucoma','Expert DR','Expert AMD','Reviewed At',
                    ...bmArr.map(k => 'BM: ' + k.replace(/_/g, ' '))]

                const csvRows = rows.map(r => {
                    let bm = {}
                    try { bm = r.biomarkers ? (typeof r.biomarkers === 'string' ? JSON.parse(r.biomarkers) : r.biomarkers) : {} } catch {}
                    return [
                        r.upload_id, r.patient_amka, r.uploaded_at, r.center_name, r.specialty,
                        r.ai_glaucoma, r.ai_glaucoma_conf, r.ai_dr, r.ai_dr_conf, r.ai_amd, r.ai_amd_conf,
                        r.reviewer || '', r.doctor_glaucoma || '', r.doctor_dr || '', r.doctor_amd || '', r.reviewed_at || '',
                        ...bmArr.map(k => bm[k] || '')
                    ].map(v => `"${String(v ?? '').replace(/"/g, '""')}"`).join(',')
                })

                const csv = [headers.join(','), ...csvRows].join('\n')
                const a = document.createElement('a')
                a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv)
                a.download = `ddart_full_export_${new Date().toISOString().slice(0,10)}.csv`
                a.click()
            } catch(e) { console.error(e) }
            finally { this.exportLoading = false }
        },

        async exportFullExcel() {
            this.exportLoading = true
            try {
                const res = await fetch(`https://labiris.myiplist.com/study/export?code=${encodeURIComponent(this.codeInput)}`)
                const data = await res.json()
                const rows = data.rows || []
                if (!rows.length) { alert('No data to export.'); return }

                const bmKeys = new Set()
                rows.forEach(r => {
                    try {
                        const bm = r.biomarkers ? (typeof r.biomarkers === 'string' ? JSON.parse(r.biomarkers) : r.biomarkers) : {}
                        Object.keys(bm).forEach(k => bmKeys.add(k))
                    } catch {}
                })
                const bmArr = [...bmKeys]

                const headers = ['Upload ID','Patient AMKA','Uploaded At','Health Center','Specialty',
                    'AI Glaucoma','AI Glaucoma Conf%','AI DR','AI DR Conf%','AI AMD','AI AMD Conf%',
                    'Reviewer','Expert Glaucoma','Expert DR','Expert AMD','Reviewed At',
                    ...bmArr.map(k => 'BM: ' + k.replace(/_/g, ' '))]

                const tableRows = rows.map(r => {
                    let bm = {}
                    try { bm = r.biomarkers ? (typeof r.biomarkers === 'string' ? JSON.parse(r.biomarkers) : r.biomarkers) : {} } catch {}
                    return [
                        r.upload_id, r.patient_amka, r.uploaded_at, r.center_name, r.specialty,
                        r.ai_glaucoma, r.ai_glaucoma_conf, r.ai_dr, r.ai_dr_conf, r.ai_amd, r.ai_amd_conf,
                        r.reviewer || '', r.doctor_glaucoma || '', r.doctor_dr || '', r.doctor_amd || '', r.reviewed_at || '',
                        ...bmArr.map(k => bm[k] || '')
                    ]
                })

                let html = '<table><tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr>'
                tableRows.forEach(row => {
                    html += '<tr>' + row.map(v => `<td>${v ?? ''}</td>`).join('') + '</tr>'
                })
                html += '</table>'

                const a = document.createElement('a')
                a.href = 'data:application/vnd.ms-excel;charset=utf-8,' + encodeURIComponent(html)
                a.download = `ddart_full_export_${new Date().toISOString().slice(0,10)}.xls`
                a.click()
            } catch(e) { console.error(e) }
            finally { this.exportLoading = false }
        }
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; min-height: 100%; background: #f0f4f8; font-family: 'Source Sans 3', sans-serif; }

.study-container { display: flex; flex-direction: column; align-items: center; padding: 30px 20px 0; min-height: 100vh; }
.dashboard { width: 100%; max-width: 1100px; display: flex; flex-direction: column; align-items: center; }

/* Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(10,20,40,0.85); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.modal-box { background: white; border-radius: 12px; padding: 40px; width: 320px; display: flex; flex-direction: column; align-items: center; gap: 16px; animation: appear 0.35s cubic-bezier(0.34,1.56,0.64,1) both; }
@keyframes appear { from { opacity: 0; transform: scale(0.9) translateY(20px); } to { opacity: 1; transform: scale(1) translateY(0); } }
.modal-box h3 { font-family: 'Playfair Display', serif; color: #2d3748; font-size: 18px; margin: 0; }
.modal-box p { font-size: 13px; color: #718096; margin: 0; text-align: center; }
.field { width: 100%; }
.field input { width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; color: #2d3748; outline: none; transition: border-color 0.2s, box-shadow 0.2s; }
.field input:focus { border-color: #2b6cb0; box-shadow: 0 0 0 3px rgba(43,108,176,0.12); }
.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0; }
.submit-btn { width: 100%; padding: 10px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.submit-btn:hover:not(:disabled) { background: #2c5282; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.back-btn { width: 100%; padding: 8px; background: none; border: 1px solid #e2e8f0; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; }
.back-btn:hover { background: #f8fafc; }

/* Header */
.header { text-align: center; margin-bottom: 24px; width: 100%; }
.user-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.user-bar-title { font-size: 13px; font-weight: 700; color: #4a5568; }
.user-bar-actions { display: flex; align-items: center; gap: 8px; }
.tab-pill { padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; cursor: pointer; border: 1px solid #e2e8f0; background: white; color: #718096; font-family: 'Source Sans 3', sans-serif; transition: all 0.2s; }
.tab-pill.active { background: #2b6cb0; color: white; border-color: #2b6cb0; }
.conf-toggle-btn { padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; cursor: pointer; border: 1px solid #feebc8; background: #fffaf0; color: #c05621; font-family: 'Source Sans 3', sans-serif; transition: all 0.2s; }
.conf-toggle-btn:hover { background: #feebc8; }
.conf-toggle-btn.conf-low-mode { background: #c05621; color: white; border-color: #c05621; }
.logout-btn { padding: 4px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; font-family: 'Source Sans 3', sans-serif; background: none; border: 1px solid #e2e8f0; color: #718096; }
.logout-btn:hover { background: #f8fafc; }
.university { font-size: 14px; color: #2c5282; font-weight: 600; margin: 0 0 4px; }
.subtitle { font-size: 13px; color: #4a6fa5; margin: 0 0 16px; }

/* Tabs */
.panel-tabs { display: flex; gap: 8px; width: 100%; margin-bottom: 20px; }
.panel-tab { flex: 1; padding: 10px; border: 1px solid #e2e8f0; border-radius: 4px; background: white; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; transition: all 0.2s; }
.panel-tab:hover { background: #f8fafc; }
.panel-tab.active { background: #2b6cb0; color: white; border-color: #2b6cb0; }

.panel-section { width: 100%; display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; }

/* Stat cards */
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.stat-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; text-align: center; }
.stat-value { font-size: 36px; font-weight: 700; color: #2b6cb0; margin: 0; font-family: 'Playfair Display', serif; line-height: 1; }
.stat-label { font-size: 11px; color: #a0aec0; margin: 6px 0 0; text-transform: uppercase; letter-spacing: 0.5px; }

/* Section cards */
.section-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; }
.section-title { font-family: 'Playfair Display', serif; font-size: 16px; color: #2c5282; margin: 0 0 20px; }
.section-sub { font-family: 'Source Sans 3', sans-serif; font-size: 12px; color: #a0aec0; font-weight: 400; }

/* Agreement rings */
.agreement-row-grid { display: flex; gap: 32px; align-items: center; justify-content: center; flex-wrap: wrap; }
.agree-block { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.agree-ring { width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; }
.agree-ring::before { content: ''; position: absolute; inset: 8px; background: white; border-radius: 50%; }
.agree-ring.overall { width: 96px; height: 96px; }
.agree-pct { position: relative; z-index: 1; font-size: 16px; font-weight: 700; color: #2d3748; }
.agree-ring.overall .agree-pct { font-size: 20px; }
.agree-label { font-size: 12px; color: #718096; font-weight: 600; }

/* Prevalence */
.prevalence-grid { display: flex; flex-direction: column; gap: 12px; }
.prev-bar-row { display: grid; grid-template-columns: 80px 1fr 80px; align-items: center; gap: 12px; }
.prev-label { font-size: 13px; font-weight: 600; color: #4a5568; }
.prev-bar-wrap { height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; }
.prev-bar { height: 100%; border-radius: 5px; transition: width 0.6s ease; }
.glaucoma-bar { background: #38a169; }
.dr-bar { background: #e53e3e; }
.amd-bar { background: #2b6cb0; }
.prev-count { font-size: 12px; color: #718096; text-align: right; }

/* Data table */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { background: #f8fafc; color: #a0aec0; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; padding: 8px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; white-space: nowrap; }
.data-table td { padding: 10px 12px; border-bottom: 1px solid #f0f4f8; color: #2d3748; vertical-align: middle; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #f8fafc; }
.mini-bar-wrap { height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; width: 120px; }
.mini-bar { height: 100%; background: #2b6cb0; border-radius: 4px; }
.condition-table-wrap { overflow-x: auto; }
.amka-cell { font-family: monospace; letter-spacing: 1px; color: #2b6cb0; font-weight: 700; }
.match-yes { color: #38a169; font-weight: 700; }
.match-no { color: #e53e3e; font-weight: 700; }

/* Chips & badges */
.ai-chip { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.chip-positive { background: #fff5f5; color: #c53030; }
.chip-negative { background: #f0fff4; color: #276749; }
.answer-chip { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; white-space: nowrap; }
.chip-match { background: #f0fff4; color: #276749; }
.chip-differ { background: #fff5f5; color: #c53030; }
.pct-badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.pct-good { background: #f0fff4; color: #276749; }
.pct-mid { background: #fffaf0; color: #c05621; }
.pct-low { background: #fff5f5; color: #c53030; }
.conf-badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.conf-high { background: #fffaf0; color: #c05621; }
.conf-low { background: #f0fff4; color: #276749; }
.specialty-chip { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.specialty-chip.glaucoma { background: #f0fff4; color: #276749; }
.specialty-chip.dr { background: #fff5f5; color: #c53030; }
.specialty-chip.amd { background: #ebf8ff; color: #2b6cb0; }
.review-count-badge { background: #e2e8f0; color: #4a5568; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px; }

/* Condition summary bar */
.condition-summary-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.csb-item { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }
.csb-val { display: block; font-size: 28px; font-weight: 700; color: #2b6cb0; font-family: 'Playfair Display', serif; }
.csb-label { font-size: 11px; color: #a0aec0; text-transform: uppercase; letter-spacing: 0.5px; }

/* Condition header */
.condition-header-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.condition-filter-row { display: flex; gap: 8px; }

/* Image grid */
.img-link-btn { background: none; border: none; color: #2b6cb0; font-weight: 600; font-size: 13px; cursor: pointer; padding: 2px 0; text-decoration: underline; }
.img-link-btn:hover { color: #1a4a8a; }
.thumb-id { color: white; font-weight: 700; font-size: 13px; opacity: 0; transition: opacity 0.2s; }
.thumb-view { color: white; font-size: 11px; font-weight: 600; opacity: 0; transition: opacity 0.2s; }
.image-card:hover .thumb-id, .image-card:hover .thumb-view { opacity: 1; }
.image-card-body { padding: 10px; display: flex; flex-direction: column; gap: 5px; }
.image-card-row { display: flex; align-items: center; justify-content: space-between; }
.image-card-label { font-size: 10px; color: #a0aec0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; }

/* Detail modal */
.detail-box { background: white; border-radius: 12px; width: 90vw; max-width: 860px; max-height: 90vh; overflow: hidden; display: flex; flex-direction: column; }
.detail-toolbar { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; border-bottom: 1px solid #e2e8f0; }
.detail-body { display: grid; grid-template-columns: 300px 1fr; overflow: hidden; flex: 1; }
.detail-img-col { padding: 20px; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; gap: 12px; background: #f8fafc; }
.detail-img-wrap { border-radius: 8px; overflow: hidden; background: #e2e8f0; }
.detail-img-full { width: 100%; display: block; object-fit: contain; max-height: 260px; }
.detail-ai-row { display: flex; align-items: center; gap: 8px; }
.detail-ai-label { font-size: 12px; font-weight: 700; color: #4a5568; }
.detail-reviews-col { padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }
.detail-reviews-title { font-family: 'Playfair Display', serif; font-size: 15px; color: #2c5282; margin: 0; }
.detail-reviews-list { display: flex; flex-direction: column; gap: 12px; }
.detail-review-row { border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; background: #f8fafc; }
.detail-review-header { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.detail-doc-name { font-weight: 700; font-size: 13px; color: #2d3748; }
.detail-biomarkers { margin-top: 8px; }
.detail-bio-title { font-size: 11px; font-weight: 700; color: #718096; text-transform: uppercase; letter-spacing: 0.3px; }
.detail-stats-row { display: flex; align-items: center; gap: 8px; padding-top: 12px; border-top: 1px solid #e2e8f0; }
.detail-stat-label { font-size: 12px; font-weight: 600; color: #4a5568; }
.zoom-close-btn { background: rgba(229,62,62,0.15); border: none; color: #c53030; font-size: 13px; padding: 6px 16px; border-radius: 6px; cursor: pointer; font-weight: 700; transition: background 0.2s; }
.zoom-close-btn:hover { background: rgba(229,62,62,0.3); }
.zoom-title { font-size: 14px; font-weight: 700; color: #2d3748; }
.zoom-error { color: #fc8181; font-size: 14px; padding: 40px; text-align: center; }

/* HC subsection */
.hc-subsection { margin-top: 24px; padding-top: 20px; border-top: 1px solid #e2e8f0; }
.hc-sub-title { font-size: 14px; font-weight: 700; color: #553c9a; margin: 0 0 12px; }

/* Biomarkers */
.bio-header-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 10px; }
.bio-header-actions { display: flex; gap: 8px; }
.bio-filter-bar { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.bio-filter-select { padding: 6px 10px; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 13px; background: white; font-family: 'Source Sans 3', sans-serif; }
.bio-count { font-size: 12px; color: #718096; }
.bio-review-list { display: flex; flex-direction: column; gap: 16px; }
.bio-group-card { border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden; background: white; }
.bio-group-header { display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: #f0f4f8; border-bottom: 1px solid #e2e8f0; }
.bio-group-count { font-size: 11px; font-weight: 700; color: #2b6cb0; background: #ebf8ff; padding: 2px 8px; border-radius: 10px; }
.bio-group-reviews { display: flex; flex-direction: column; }
.bio-group-split { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
.bio-group-split .bio-review-card { border-radius: 0; border: none; border-right: 1px solid #e2e8f0; }
.bio-group-split .bio-review-card:last-child { border-right: none; }
.bio-review-card { border: none; border-bottom: 1px solid #f0f4f8; padding: 14px; background: #f8fafc; }
.bio-review-card:last-child { border-bottom: none; }
.bio-review-header { display: flex; gap: 16px; align-items: center; margin-bottom: 8px; flex-wrap: wrap; }
.bio-review-img { font-weight: 700; font-size: 13px; color: #2b6cb0; }
.bio-review-doctor { font-size: 12px; color: #553c9a; font-weight: 600; }
.bio-review-date { font-size: 11px; color: #a0aec0; margin-left: auto; }
.bio-review-diagnoses { display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }
.bio-diag-chip { background: #ebf8ff; color: #2b6cb0; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; border: 1px solid #bee3f8; }
.bio-markers-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 4px; }
.bio-marker-item { display: flex; justify-content: space-between; align-items: center; padding: 4px 8px; border-radius: 4px; font-size: 11px; background: #f7fafc; border: 1px solid #e2e8f0; }
.bm-key { color: #4a5568; text-transform: capitalize; }
.bm-val { font-weight: 700; font-size: 10px; padding: 1px 5px; border-radius: 3px; }
.bio-marker-item.bm-yes .bm-val { background: #c6f6d5; color: #276749; }
.bio-marker-item.bm-no .bm-val { background: #fed7d7; color: #9b2c2c; }
.bio-marker-item.bm-inconclusive .bm-val { background: #fefcbf; color: #744210; }
.bio-no-markers { font-size: 12px; color: #a0aec0; font-style: italic; }

/* Export/refresh buttons */
.refresh-btn { padding: 5px 12px; border: 1px solid #e2e8f0; border-radius: 4px; background: white; font-size: 12px; font-weight: 600; color: #4a5568; cursor: pointer; font-family: 'Source Sans 3', sans-serif; transition: background 0.2s; }
.refresh-btn:hover:not(:disabled) { background: #f0f4f8; }
.export-btn { padding: 5px 12px; border: 1px solid #bee3f8; border-radius: 4px; background: #ebf8ff; font-size: 12px; font-weight: 600; color: #2b6cb0; cursor: pointer; font-family: 'Source Sans 3', sans-serif; transition: background 0.2s; }
.export-btn:hover:not(:disabled) { background: #bee3f8; }
.export-btn.excel { background: #f0fff4; border-color: #c6f6d5; color: #276749; }
.export-btn.excel:hover:not(:disabled) { background: #c6f6d5; }
.export-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* Admin */
.admin-grid { display: flex; flex-direction: column; gap: 16px; width: 100%; }
.admin-section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.admin-count-badge { background: #e2e8f0; color: #4a5568; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 10px; }
.doctor-list { display: flex; flex-direction: column; gap: 0; }
.doctor-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f0f4f8; gap: 12px; }
.doctor-row:last-child { border-bottom: none; }
.doctor-info { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.doctor-name { font-size: 14px; font-weight: 700; color: #2d3748; }
.doctor-email { font-size: 12px; color: #718096; }
.doctor-badges { display: flex; gap: 6px; margin-top: 4px; flex-wrap: wrap; }
.status-badge { font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 10px; }
.badge-approved { background: #f0fff4; color: #276749; }
.badge-pending { background: #fffaf0; color: #c05621; }
.badge-research { background: #ebf8ff; color: #2b6cb0; }
.doctor-actions { display: flex; gap: 6px; }
.action-btn { padding: 5px 12px; border-radius: 4px; font-size: 12px; font-weight: 700; cursor: pointer; border: none; font-family: 'Source Sans 3', sans-serif; transition: opacity 0.2s; }
.action-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.approve-btn { background: #f0fff4; color: #276749; border: 1px solid #c6f6d5; }
.approve-btn:hover:not(:disabled) { background: #c6f6d5; }
.unapprove-btn { background: #fffaf0; color: #c05621; border: 1px solid #feebc8; }
.unapprove-btn:hover:not(:disabled) { background: #feebc8; }
.delete-btn { background: #fff5f5; color: #c53030; border: 1px solid #fed7d7; }
.delete-btn:hover:not(:disabled) { background: #fed7d7; }
.admin-note { font-size: 12px; color: #a0aec0; margin: 12px 0 0; font-style: italic; }
.center-id-code { background: #f0f4f8; padding: 2px 6px; border-radius: 4px; font-size: 12px; color: #2b6cb0; font-weight: 700; }

/* Reset button */
.danger-zone-card { border-color: #fed7d7 !important; }
.danger-title { color: #c53030 !important; }
.danger-desc { font-size: 12px; color: #a0aec0; margin: -8px 0 16px; font-style: italic; }
.danger-actions { display: flex; flex-direction: column; gap: 0; }
.danger-action-item { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 14px 0; border-bottom: 1px solid #fff5f5; }
.danger-action-item:last-child { border-bottom: none; }
.danger-action-info { display: flex; flex-direction: column; gap: 3px; }
.danger-action-label { font-size: 13px; font-weight: 700; color: #2d3748; }
.danger-action-sub { font-size: 12px; color: #a0aec0; line-height: 1.5; }
.danger-btn { padding: 7px 16px; background: #fff5f5; border: 1px solid #fed7d7; border-radius: 6px; color: #c53030; font-family: 'Source Sans 3', sans-serif; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.danger-btn:hover { background: #fed7d7; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(197,48,48,0.15); }
.danger-btn:active { transform: scale(0.96); }
.danger-btn-strong { background: #e53e3e; border-color: #c53030; color: white; }
.danger-btn-strong:hover { background: #c53030; box-shadow: 0 2px 8px rgba(197,48,48,0.3); }

/* Loading */
.loading-state { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 60px; color: #718096; }
.spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #2b6cb0; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state { padding: 32px; text-align: center; color: #a0aec0; font-size: 13px; }

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.fade-slide-enter-active { transition: all 0.3s ease; }
.fade-slide-leave-active { transition: all 0.2s ease; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-6px); }
.zoom-fade-enter-active, .zoom-fade-leave-active { transition: opacity 0.2s ease; }
.zoom-fade-enter-from, .zoom-fade-leave-to { opacity: 0; }
.error-pop-enter-active { transition: opacity 0.25s ease, transform 0.25s cubic-bezier(0.34,1.56,0.64,1); }
.error-pop-leave-active { transition: opacity 0.15s ease; }
.error-pop-enter-from { opacity: 0; transform: translateY(-4px) scale(0.97); }
.error-pop-leave-to { opacity: 0; }

/* Footer */
.footer { width: 100%; max-width: 1100px; display: flex; justify-content: space-between; align-items: center; padding: 16px 0 24px; border-top: 1px solid #e2e8f0; margin-top: auto; }
.dept-logo { height: 55px; width: auto; object-fit: contain; }
.footer-right { text-align: right; }
.footer-right p { font-size: 12px; color: #718096; margin: 2px 0; }
.footer-right a { color: #2b6cb0; text-decoration: none; }
.made-by { font-size: 10px; color: #cbd5e0; margin-top: 4px; }

@media (max-width: 768px) {
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
    .condition-summary-bar { grid-template-columns: repeat(2, 1fr); }
    .agreement-row-grid { gap: 20px; }
    .panel-tabs { flex-wrap: wrap; }
    .detail-body { grid-template-columns: 1fr; }
    .detail-img-col { border-right: none; border-bottom: 1px solid #e2e8f0; }
    .image-grid { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); }
    .admin-grid { grid-template-columns: 1fr; }
}

/* ── Threshold controls ── */
.threshold-info { font-size: 12px; color: #718096; margin: -8px 0 16px; font-style: italic; }
.threshold-loading { font-size: 13px; color: #a0aec0; padding: 12px 0; }
.threshold-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.threshold-group { display: flex; flex-direction: column; gap: 10px; }
.threshold-group-title { font-size: 12px; font-weight: 700; color: #2c5282; text-transform: uppercase; letter-spacing: 0.4px; margin: 0 0 4px; display: flex; flex-direction: column; gap: 2px; }
.threshold-group-sub { font-size: 11px; color: #a0aec0; font-weight: 400; text-transform: none; letter-spacing: 0; }
.threshold-row { display: flex; align-items: center; gap: 12px; }
.thr-label { font-size: 13px; font-weight: 600; color: #4a5568; min-width: 72px; }
.thr-slider { flex: 1; height: 4px; accent-color: #2b6cb0; cursor: pointer; }
.thr-value { font-size: 14px; font-weight: 700; min-width: 44px; text-align: right; font-family: 'Courier New', monospace; }
.thr-high { color: #2b6cb0; }
.thr-mid  { color: #d69e2e; }
.thr-low  { color: #e53e3e; }
.threshold-actions { display: flex; align-items: center; justify-content: flex-end; gap: 16px; margin-top: 20px; padding-top: 16px; border-top: 1px solid #e2e8f0; }
.thr-save-btn { padding: 9px 24px; background: #2b6cb0; color: white; border: none; border-radius: 4px; font-family: 'Source Sans 3', sans-serif; font-size: 13px; font-weight: 700; cursor: pointer; transition: background 0.2s, transform 0.15s; }
.thr-save-btn:hover:not(:disabled) { background: #2c5282; transform: translateY(-1px); }
.thr-save-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.threshold-saved { font-size: 13px; font-weight: 700; color: #38a169; animation: savedPop 0.35s cubic-bezier(0.34,1.56,0.64,1); }
@keyframes savedPop { from { opacity:0; transform: scale(0.8); } to { opacity:1; transform: scale(1); } }
.save-flash-enter-active { transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.34,1.56,0.64,1); }
.save-flash-leave-active { transition: opacity 0.4s ease; }
.save-flash-enter-from { opacity: 0; transform: scale(0.8); }
.save-flash-leave-to { opacity: 0; }
@media (max-width: 700px) { .threshold-grid { grid-template-columns: 1fr; } }

/* ── Referral badge ── */
.ref-sub { display: flex; gap: 4px; flex-wrap: wrap; justify-content: center; margin: 4px 0 0; }
.ref-chip { font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 8px; white-space: nowrap; }
.ref-agree { background: #f0fff4; color: #276749; }
.ref-other { background: #fffaf0; color: #b7791f; }

.referral-badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.referral-yes { background: #fff5f5; color: #c53030; }
.referral-no { background: #f0fff4; color: #276749; }

/* ── Side-by-side biomarkers when 2+ doctors reviewed same image ── */
.detail-reviews-side-by-side { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.detail-reviews-side-by-side .detail-review-row { margin: 0; }

/* ── Inconclusive studies ── */
.delete-upload-btn { padding: 6px 14px; background: #fff5f5; border: 1px solid #fed7d7; border-radius: 6px; color: #c53030; font-family: 'Source Sans 3', sans-serif; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.delete-upload-btn:hover:not(:disabled) { background: #fed7d7; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(197,48,48,0.15); }
.delete-upload-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.inconclusive-studies-btn { display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #fffaf0; border: 1.5px solid #feebc8; border-radius: 8px; color: #b7791f; font-family: 'Source Sans 3', sans-serif; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s cubic-bezier(0.4,0,0.2,1); }
.inconclusive-studies-btn:hover { background: #feebc8; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(214,158,46,0.15); }
.inconclusive-count-badge { background: #d69e2e; color: white; font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 8px; }
.inconclusive-modal-box { background: white; border-radius: 12px; width: 90vw; max-width: 760px; max-height: 80vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 24px 60px rgba(0,0,0,0.2); }
.inconclusive-modal-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 24px; border-bottom: 1px solid #e2e8f0; background: #fffaf0; }
.inconclusive-modal-header h3 { font-family: 'Playfair Display', serif; font-size: 16px; color: #b7791f; margin: 0; }
.inconclusive-list { overflow-y: auto; display: flex; flex-direction: column; gap: 12px; padding: 20px; }
.inconclusive-item { border: 1px solid #feebc8; border-radius: 8px; padding: 14px; background: #fffaf0; }
.inconclusive-item-header { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 4px; }
.inconclusive-amka { font-family: monospace; font-size: 13px; font-weight: 700; color: #2b6cb0; letter-spacing: 1px; }
.inconclusive-center { font-size: 12px; color: #4a5568; font-weight: 600; }
.inconclusive-doctor { font-size: 12px; color: #553c9a; font-weight: 600; }
.inconclusive-date { font-size: 11px; color: #a0aec0; margin-left: auto; }
</style>