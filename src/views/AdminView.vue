<template>
    <div class="admin-container">

        <!-- Auth gate -->
        <div v-if="!authenticated" class="auth-gate">
            <div class="auth-box">
                <div class="admin-logo">DDART<span>AI</span></div>
                <h2>Admin Access</h2>
                <p>Enter the administrator password to continue.</p>
                <div class="field">
                    <label>Password</label>
                    <input v-model="adminPassword" type="password" placeholder="Admin password" @keyup.enter="authenticate" autofocus />
                </div>
                <transition name="error-pop">
                    <p v-if="authError" class="error">{{ authError }}</p>
                </transition>
                <button class="btn-primary" @click="authenticate" :disabled="!adminPassword">Enter</button>
            </div>
        </div>

        <!-- Admin panel -->
        <div v-else class="admin-panel">
            <div class="admin-header">
                <div class="admin-logo">DDART<span>AI</span></div>
                <h1>Health Center Administration</h1>
                <button class="btn-ghost" @click="authenticated = false; adminPassword = ''">Sign Out</button>
            </div>

            <div class="admin-body">

                <!-- Register new center -->
                <div class="admin-card">
                    <h2>Register New Health Center</h2>
                    <p class="card-sub">A unique 5-digit ID will be generated automatically.</p>

                    <div class="form-grid">
                        <div class="field">
                            <label>Health Center Name</label>
                            <input v-model="newName" type="text" placeholder="Full official name" />
                        </div>
                        <div class="field">
                            <label>Login Password</label>
                            <input v-model="newPassword" type="password" placeholder="Password for this center" />
                        </div>
                        <div class="field">
                            <label>Specialty</label>
                            <div class="specialty-picker">
                                <button
                                    v-for="s in specialties"
                                    :key="s.value"
                                    :class="['specialty-btn', s.value, { active: newSpecialty === s.value }]"
                                    @click="newSpecialty = s.value"
                                >
                                    <span class="s-icon">{{ s.icon }}</span>
                                    {{ s.label }}
                                </button>
                            </div>
                        </div>
                    </div>

                    <transition name="error-pop">
                        <p v-if="registerError" class="error">{{ registerError }}</p>
                    </transition>
                    <transition name="error-pop">
                        <div v-if="lastRegistered" class="success-banner">
                            <strong>✓ Registered successfully</strong>
                            <span>{{ lastRegistered.name }}</span>
                            <span class="id-pill">ID: {{ lastRegistered.center_id }}</span>
                            <span :class="['spec-pill', lastRegistered.specialty]">{{ lastRegistered.specialty.toUpperCase() }}</span>
                        </div>
                    </transition>

                    <button class="btn-primary" @click="registerCenter" :disabled="registering || !newName || !newPassword || !newSpecialty">
                        <span>{{ registering ? 'Registering...' : 'Register Center' }}</span>
                        <span v-if="registering" class="btn-spinner"></span>
                    </button>
                </div>

                <!-- Centers list -->
                <div class="admin-card">
                    <div class="card-header-row">
                        <h2>Registered Centers</h2>
                        <button class="btn-ghost small" @click="loadCenters">↻ Refresh</button>
                    </div>

                    <div v-if="loadingCenters" class="loading-row">Loading...</div>
                    <div v-else-if="centers.length === 0" class="empty-row">No centers registered yet.</div>
                    <div v-else class="centers-table">
                        <div class="table-header">
                            <span>Name</span>
                            <span>Center ID</span>
                            <span>Specialty</span>
                            <span></span>
                        </div>
                        <div v-for="c in centers" :key="c.id" class="table-row">
                            <span class="center-name">{{ c.name }}</span>
                            <span class="center-id-mono">{{ c.center_id }}</span>
                            <span :class="['spec-pill', c.specialty]">{{ c.specialty.toUpperCase() }}</span>
                            <button class="btn-delete" @click="confirmDelete(c)" title="Delete">✕</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Delete confirm modal -->
        <transition name="modal-fade">
            <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null">
                <div class="modal-box">
                    <h3>Delete Health Center?</h3>
                    <p>This will permanently remove <strong>{{ deleteTarget.name }}</strong> (ID: {{ deleteTarget.center_id }}). They will no longer be able to log in.</p>
                    <div class="modal-btns">
                        <button class="btn-ghost" @click="deleteTarget = null">Cancel</button>
                        <button class="btn-danger" @click="deleteCenter" :disabled="deleting">{{ deleting ? 'Deleting...' : 'Delete' }}</button>
                    </div>
                </div>
            </div>
        </transition>

    </div>
</template>

<script>
const API = 'https://labiris.myiplist.com'
const ADMIN_PW = 'ddart_admin_2024'

export default {
    data() {
        return {
            authenticated: false,
            adminPassword: '',
            authError: '',

            newName: '',
            newPassword: '',
            newSpecialty: '',
            registerError: '',
            registering: false,
            lastRegistered: null,

            centers: [],
            loadingCenters: false,

            deleteTarget: null,
            deleting: false,

            specialties: [
                { value: 'glaucoma', label: 'Glaucoma', icon: '👁' },
                { value: 'dr', label: 'Diabetic Retinopathy', icon: '🩸' },
                { value: 'amd', label: 'AMD', icon: '🔬' }
            ]
        }
    },

    methods: {
        async authenticate() {
            this.authError = ''
            try {
                const res = await fetch(`${API}/admin/centers?admin_password=${encodeURIComponent(this.adminPassword)}`)
                if (!res.ok) { this.authError = 'Invalid password.'; return }
                this.centers = await res.json()
                this.authenticated = true
            } catch { this.authError = 'Connection failed.' }
        },

        async loadCenters() {
            this.loadingCenters = true
            try {
                const res = await fetch(`${API}/admin/centers?admin_password=${encodeURIComponent(this.adminPassword)}`)
                if (res.ok) this.centers = await res.json()
            } finally { this.loadingCenters = false }
        },

        async registerCenter() {
            this.registerError = ''
            this.lastRegistered = null
            this.registering = true
            try {
                const res = await fetch(`${API}/admin/register-center`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        admin_password: this.adminPassword,
                        name: this.newName,
                        password: this.newPassword,
                        specialty: this.newSpecialty
                    })
                })
                const data = await res.json()
                if (!res.ok) { this.registerError = data.detail || 'Registration failed.'; return }
                this.lastRegistered = data
                this.newName = ''
                this.newPassword = ''
                this.newSpecialty = ''
                this.centers.push(data)
            } catch { this.registerError = 'Connection failed.' }
            finally { this.registering = false }
        },

        confirmDelete(center) { this.deleteTarget = center },

        async deleteCenter() {
            this.deleting = true
            try {
                const res = await fetch(`${API}/admin/centers/${this.deleteTarget.id}?admin_password=${encodeURIComponent(this.adminPassword)}`, {
                    method: 'DELETE'
                })
                if (res.ok) {
                    this.centers = this.centers.filter(c => c.id !== this.deleteTarget.id)
                    this.deleteTarget = null
                }
            } finally { this.deleting = false }
        }
    }
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; }
.admin-container { min-height: 100vh; background: #f0f4f8; font-family: 'Segoe UI', sans-serif; }

.auth-gate { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: radial-gradient(ellipse at center, #0d1f3c, #060d1a); }
.auth-box { background: white; border-radius: 12px; padding: 40px; width: 340px; display: flex; flex-direction: column; gap: 16px; align-items: center; box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
.admin-logo { font-size: 16px; font-weight: 700; color: #2c5282; letter-spacing: 3px; display: flex; align-items: baseline; gap: 2px; }
.admin-logo span { color: #e53e3e; font-size: 36px; font-weight: 900; font-family: 'Arial Black', Arial, sans-serif; line-height: 1; }
.auth-box h2 { font-size: 18px; color: #2d3748; margin: 0; font-weight: 700; }
.auth-box p { font-size: 13px; color: #718096; margin: 0; text-align: center; }

.admin-panel { max-width: 860px; margin: 0 auto; padding: 32px 24px; }
.admin-header { display: flex; align-items: center; gap: 16px; margin-bottom: 28px; padding-bottom: 20px; border-bottom: 2px solid #e2e8f0; }
.admin-header h1 { font-size: 20px; font-weight: 700; color: #2d3748; margin: 0; flex: 1; }

.admin-body { display: flex; flex-direction: column; gap: 24px; }
.admin-card { background: white; border-radius: 10px; border: 1px solid #e2e8f0; padding: 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
.admin-card h2 { font-size: 16px; font-weight: 700; color: #2d3748; margin: 0 0 4px; }
.card-sub { font-size: 13px; color: #718096; margin: 0 0 20px; }
.card-header-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.card-header-row h2 { margin: 0; }

.form-grid { display: flex; flex-direction: column; gap: 14px; margin-bottom: 16px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 11px; font-weight: 700; color: #4a5568; text-transform: uppercase; letter-spacing: 0.5px; }
.field input { padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 14px; color: #2d3748; outline: none; width: 100%; transition: border-color 0.2s, box-shadow 0.2s; }
.field input:focus { border-color: #2b6cb0; box-shadow: 0 0 0 3px rgba(43,108,176,0.1); }

.specialty-picker { display: flex; gap: 8px; }
.specialty-btn { flex: 1; padding: 10px 8px; border: 1.5px solid #e2e8f0; border-radius: 8px; background: white; font-size: 12px; font-weight: 600; color: #718096; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; transition: all 0.2s; }
.specialty-btn:hover { border-color: #cbd5e0; background: #f8fafc; }
.specialty-btn.glaucoma.active { border-color: #48bb78; background: #f0fff4; color: #276749; }
.specialty-btn.dr.active { border-color: #ed8936; background: #fffaf0; color: #c05621; }
.specialty-btn.amd.active { border-color: #9f7aea; background: #faf5ff; color: #553c9a; }
.s-icon { font-size: 16px; }

.success-banner { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: #f0fff4; border: 1px solid #9ae6b4; border-radius: 6px; font-size: 13px; color: #276749; flex-wrap: wrap; margin-bottom: 12px; }
.success-banner strong { font-weight: 700; }
.id-pill { font-family: 'Courier New', monospace; background: #edf2f7; color: #2d3748; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; letter-spacing: 1px; }
.spec-pill { font-size: 11px; font-weight: 700; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.5px; }
.spec-pill.glaucoma { background: #f0fff4; color: #276749; border: 1px solid #9ae6b4; }
.spec-pill.dr { background: #fffaf0; color: #c05621; border: 1px solid #fbd38d; }
.spec-pill.amd { background: #faf5ff; color: #553c9a; border: 1px solid #d6bcfa; }

.centers-table { border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden; }
.table-header { display: grid; grid-template-columns: 1fr 110px 140px 40px; padding: 8px 14px; background: #f8fafc; font-size: 11px; font-weight: 700; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e2e8f0; }
.table-row { display: grid; grid-template-columns: 1fr 110px 140px 40px; padding: 12px 14px; align-items: center; border-bottom: 1px solid #f0f4f8; transition: background 0.15s; }
.table-row:last-child { border-bottom: none; }
.table-row:hover { background: #f8fafc; }
.center-name { font-size: 14px; font-weight: 600; color: #2d3748; }
.center-id-mono { font-family: 'Courier New', monospace; font-size: 13px; font-weight: 700; color: #4a5568; letter-spacing: 1.5px; }
.loading-row, .empty-row { padding: 24px; text-align: center; font-size: 14px; color: #a0aec0; }

.btn-primary { padding: 10px 20px; background: #2b6cb0; color: white; border: none; border-radius: 5px; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background 0.2s; width: 100%; justify-content: center; }
.btn-primary:hover:not(:disabled) { background: #2c5282; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-ghost { padding: 7px 14px; background: none; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 13px; font-weight: 600; color: #718096; cursor: pointer; transition: all 0.2s; }
.btn-ghost:hover { background: #f0f4f8; }
.btn-ghost.small { font-size: 12px; padding: 5px 10px; }
.btn-delete { width: 28px; height: 28px; border-radius: 4px; border: none; background: none; color: #fc8181; font-size: 13px; cursor: pointer; transition: background 0.15s; }
.btn-delete:hover { background: #fff5f5; color: #e53e3e; }
.btn-danger { padding: 9px 20px; background: #e53e3e; color: white; border: none; border-radius: 5px; font-size: 14px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.btn-danger:hover:not(:disabled) { background: #c53030; }
.btn-danger:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.35); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 999; }
.modal-box { background: white; border-radius: 10px; padding: 32px; width: 380px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.modal-box h3 { font-size: 17px; font-weight: 700; color: #2d3748; margin: 0 0 10px; }
.modal-box p { font-size: 13px; color: #718096; line-height: 1.6; margin: 0 0 20px; }
.modal-btns { display: flex; gap: 10px; justify-content: flex-end; }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.error { color: #c53030; font-size: 13px; font-weight: 600; margin: 0 0 12px; }
.error-pop-enter-active { transition: opacity 0.2s, transform 0.2s; }
.error-pop-leave-active { transition: opacity 0.15s; }
.error-pop-enter-from { opacity: 0; transform: translateY(-4px); }
.error-pop-leave-to { opacity: 0; }
</style>
