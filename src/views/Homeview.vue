<template>
  <div class="home-container">
    <!-- Header -->
    <div class="header">
      <div class="user-bar">
        <span>Account: {{ patientName }}</span>
        <button class="results-btn" @click="showHistory = true">📋 My Results</button>
        <button class="logout-btn" @click="logout">Sign Out</button>
      </div>
      <p class="university">Democritus University of Thrace – DDART spin-off company</p>
      <p class="subtitle">Ophthalmology A.I. Screening Program</p>
      <div class="logo">DDART<span>AI</span></div>
    </div>

    <!-- Main Card -->
    <div class="main-card">
      <div class="card-inner">
        <div class="upload-zone" @drop.prevent="dropFile" @dragover.prevent @click="triggerUpload">
          <input type="file" accept="image/*" ref="fileInput" hidden @change="uploadFile" />
          <transition name="fade" mode="out-in">
            <div v-if="!uploadedImage" key="placeholder" class="upload-placeholder">
              <p>Upload a fundus image to begin screening</p>
              <span>Click or drag & drop</span>
            </div>
            <img v-else key="image" :src="uploadedImage" class="uploaded-image" />
          </transition>
        </div>
        <div class="description">
          <p>
            DDART-AI is an artificial intelligence platform developed for the automated screening
            of retinal conditions using fundus photography. The system analyzes eye images and
            provides predictions for three major ophthalmic conditions: Glaucoma, Diabetic
            Retinopathy, and Age-Related Macular Degeneration (AMD).
          </p>
          <p>
            The A.I. models are based on deep convolutional neural networks trained on clinical
            fundus datasets. Results include a confidence score and are intended to assist — not
            replace — clinical judgment.
          </p>
          <p>
            For further information on DDART-AI please contact the Department of Ophthalmology
            at Democritus University of Thrace.
          </p>
        </div>
      </div>
    </div>

    <!-- Buttons -->
    <div class="action-buttons">
      <button class="action-btn" @click="analyzeImage('Glaucoma')" :disabled="!uploadedImage">Glaucoma
        Screening</button>
      <button class="action-btn" @click="analyzeImage('DR')" :disabled="!uploadedImage">Diabetic Retinopathy</button>
      <button class="action-btn" @click="analyzeImage('AMD')" :disabled="!uploadedImage">AMD Screening</button>
      <button class="action-btn" @click="analyzeImage('ALL')" :disabled="!uploadedImage">Full Screening</button>
    </div>

    <!-- Recent uploads -->
    <transition name="fade-slide">
      <div v-if="recentUploads.length" class="recent-uploads">
        <h3>Recent Uploads</h3>
        <div class="thumbs">
          <img v-for="(img, idx) in recentUploads" :key="idx" :src="img" class="thumb" @click="uploadedImage = img" />
        </div>
      </div>
    </transition>

    <!-- My Results Modal -->
    <transition name="modal">
      <div v-if="showHistory" class="modal-overlay" @click.self="showHistory = false">
        <div class="modal-content">
          <div class="modal-header">
            <h3>My Screening History</h3>
            <button class="modal-close" @click="showHistory = false">✕</button>
          </div>

          <div v-if="historyLoading" class="modal-loading">
            <div class="spinner"></div>
            <p>Loading results...</p>
          </div>

          <div v-else-if="history.length === 0" class="modal-empty">
            <p>No screening history yet. Run a screening to see your results here.</p>
          </div>

          <div v-else class="history-list">
            <transition-group name="list" tag="div" class="history-list-inner">
              <div v-for="(h, idx) in history" :key="idx" class="history-item">
                <img v-if="h.image" :src="h.image" class="history-thumb" @click="loadImageFromHistory(h.image)"
                  title="Click to load this image" />
                <div v-else class="history-thumb-placeholder">No image</div>
                <div class="history-info">
                  <span class="history-type">{{ h.type }}</span>
                  <span class="history-result" :class="resultClass(h.result)">{{ h.result }}</span>
                  <span class="history-confidence">{{ h.confidence }}%</span>
                  <span class="history-date">{{ formatDate(h.date) }}</span>
                </div>
              </div>
            </transition-group>
          </div>
        </div>
      </div>
    </transition>

    <!-- Footer -->
    <div class="footer">
      <div class="footer-left">
        <img src="/democritus.png" class="dept-logo" />
      </div>
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
      uploadedImage: null,
      recentUploads: [],
      patientName: '',
      patientId: null,
      showHistory: false,
      historyLoading: false,
      history: []
    }
  },

  mounted() {
    const stored = localStorage.getItem('ddart_patient')
    if (!stored) { this.$router.push('/login'); return }
    const patient = JSON.parse(stored)
    this.patientName = patient.name
    this.patientId = patient.id
  },

  watch: {
    showHistory(val) {
      if (val) this.loadHistory()
    }
  },

  methods: {
    triggerUpload() { this.$refs.fileInput.click() },

    uploadFile(event) {
      const file = event.target.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => { this.uploadedImage = e.target.result; this.addToRecent(e.target.result) }
      reader.readAsDataURL(file)
    },

    dropFile(event) {
      const file = event.dataTransfer.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => { this.uploadedImage = e.target.result; this.addToRecent(e.target.result) }
      reader.readAsDataURL(file)
    },

    addToRecent(img) {
      if (!this.recentUploads.includes(img)) {
        this.recentUploads.unshift(img)
        if (this.recentUploads.length > 5) this.recentUploads.pop()
      }
    },

    analyzeImage(type) {
      if (!this.uploadedImage) return
      this.$router.push({ name: "Process", query: { img: this.uploadedImage, type } })
    },

    logout() {
      localStorage.removeItem('ddart_patient')
      this.$router.push('/login')
    },

    async loadHistory() {
      this.historyLoading = true
      try {
        const res = await fetch(`https://labiris.myiplist.com/history/${this.patientId}`)
        const data = await res.json()
        this.history = data.history || []
      } catch {
        this.history = []
      } finally {
        this.historyLoading = false
      }
    },

    loadImageFromHistory(img) {
      this.uploadedImage = img
      this.showHistory = false
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('el-GR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },

    resultClass(result) {
      if (!result) return ''
      const r = result.toLowerCase()
      if (r.includes('healthy') || r.includes('normal') || r.includes('no_dr')) return 'result-good'
      if (r.includes('inconclusive')) return 'result-inconclusive'
      return 'result-bad'
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

.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 20px 0;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 24px;
  width: 100%;
  max-width: 760px;
}

.user-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 13px;
  color: #4a5568;
}

.logout-btn,
.results-btn {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  font-family: 'Source Sans 3', sans-serif;
  transition: all 0.2s;
}

.logout-btn {
  background: none;
  border: 1px solid #e2e8f0;
  color: #718096;
}

.logout-btn:hover {
  background: #f8fafc;
}

.results-btn {
  background: #2b6cb0;
  border: none;
  color: white;
  font-weight: 600;
}

.results-btn:hover {
  background: #2c5282;
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
  grid-template-columns: 260px 1fr;
  min-height: 320px;
}

.upload-zone {
  border-right: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: #f8fafc;
  transition: background 0.2s;
  padding: 20px;
  overflow: hidden;
}

.upload-zone:hover {
  background: #edf2f7;
}

.upload-placeholder {
  text-align: center;
  color: #718096;
}

.upload-placeholder p {
  font-size: 14px;
  margin: 0 0 6px;
  color: #4a5568;
  font-weight: 600;
}

.upload-placeholder span {
  font-size: 12px;
  color: #a0aec0;
}

.uploaded-image {
  max-width: 100%;
  max-height: 280px;
  border-radius: 4px;
  object-fit: contain;
}

.description {
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.description p {
  font-size: 13.5px;
  line-height: 1.7;
  color: #4a5568;
  margin: 0 0 12px;
}

.description p:last-child {
  margin-bottom: 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
  width: 100%;
  max-width: 760px;
  margin-bottom: 24px;
}

.action-btn {
  flex: 1;
  padding: 14px 10px;
  border: none;
  border-radius: 4px;
  font-family: 'Source Sans 3', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: white;
  background: #2b6cb0;
  cursor: pointer;
  transition: all 0.25s ease;
  letter-spacing: 0.3px;
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: #2c5282;
}

.recent-uploads {
  width: 100%;
  max-width: 760px;
  margin-bottom: 24px;
}

.recent-uploads h3 {
  font-size: 13px;
  color: #718096;
  margin: 0 0 8px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.thumbs {
  display: flex;
  gap: 8px;
}

.thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s;
}

.thumb:hover {
  border-color: #2b6cb0;
  transform: scale(1.05);
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 6px;
  width: 90%;
  max-width: 680px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-family: 'Playfair Display', serif;
  color: #2c5282;
  font-size: 18px;
}

.modal-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #718096;
  padding: 0;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #2d3748;
}

.modal-loading,
.modal-empty {
  padding: 40px;
  text-align: center;
  color: #718096;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e2e8f0;
  border-top-color: #2b6cb0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.history-list {
  padding: 12px 16px;
}

.history-list-inner {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 10px 12px;
  transition: background 0.2s;
}

.history-item:hover {
  background: #edf2f7;
}

.history-thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 3px;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s;
}

.history-thumb:hover {
  opacity: 0.8;
  transform: scale(1.05);
}

.history-thumb-placeholder {
  width: 56px;
  height: 56px;
  background: #edf2f7;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #a0aec0;
  border: 1px solid #e2e8f0;
}

.history-info {
  display: flex;
  gap: 16px;
  align-items: center;
  flex: 1;
  font-size: 13px;
  flex-wrap: wrap;
}

.history-type {
  font-weight: 700;
  color: #2d3748;
  width: 75px;
}

.history-result {
  flex: 1;
  font-weight: 600;
}

.result-good {
  color: #276749;
}

.result-bad {
  color: #c53030;
}

.result-inconclusive {
  color: #b7791f;
}

.history-confidence {
  color: #2b6cb0;
  font-weight: 600;
}

.history-date {
  color: #a0aec0;
  font-size: 11px;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-slide-enter-active {
  transition: all 0.3s ease;
}

.fade-slide-leave-active {
  transition: all 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

.modal-enter-active {
  transition: all 0.3s ease;
}

.modal-leave-active {
  transition: all 0.2s ease;
}

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content {
  transform: translateY(20px) scale(0.97);
}

.modal-leave-to .modal-content {
  transform: translateY(20px) scale(0.97);
}

.modal-content {
  transition: transform 0.3s ease;
}

.list-enter-active {
  transition: all 0.3s ease;
}

.list-leave-active {
  transition: all 0.2s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-10px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(10px);
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