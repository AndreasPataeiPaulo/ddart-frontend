<template>
  <div class="process-container">
    <!-- Header -->
    <div class="header">
      <p class="university">Democritus University of Thrace – DDART tech spin-off application</p>
      <p class="subtitle">Ophthalmology A.I. Screening Program</p>
      <img src="/DDART.png" style="height:30px;width:auto;object-fit:contain;" />
    </div>

    <!-- Main Card -->
    <div class="main-card">
      <div class="card-inner">
        <!-- LEFT: Image -->
        <div class="image-zone" @drop.prevent="dropFile" @dragover.prevent @click="uploadAgain">
          <transition name="fade" mode="out-in">
            <img v-if="image" key="image" :src="image" class="preview" />
            <div v-else key="placeholder" class="upload-placeholder">
              <p>Upload a fundus image to begin screening</p>
              <span>Click or drag & drop</span>
            </div>
          </transition>
        </div>

        <!-- RIGHT: Buttons + Results -->
        <div class="right-panel">
          <div class="button-group">
            <button class="action-btn" @click="analyze('Glaucoma')" :disabled="loading">
              {{ loading && activeType === 'Glaucoma' ? 'Analyzing...' : 'Glaucoma Screening' }}
            </button>
            <button class="action-btn" @click="analyze('DR')" :disabled="loading">
              {{ loading && activeType === 'DR' ? 'Analyzing...' : 'Diabetic Retinopathy' }}
            </button>
            <button class="action-btn" @click="analyze('AMD')" :disabled="loading">
              {{ loading && activeType === 'AMD' ? 'Analyzing...' : 'AMD Screening' }}
            </button>
            <button class="action-btn all" @click="analyzeAll" :disabled="loading">
              {{ loading && activeType === 'ALL' ? 'Analyzing All...' : ' Full Screening' }}
            </button>
          </div>

          <transition name="fade-slide" mode="out-in">
            <!-- Loading -->
            <div v-if="loading" key="loading" class="loading-indicator">
              <div class="spinner"></div>
              <p class="loading-text">{{ activeType === 'ALL' ? 'Running full screening...' : 'Analyzing image...' }}
              </p>
              <p class="loading-subtext">Enhancing contrast & running predictions</p>
            </div>

            <!-- Single result -->
            <div v-else-if="result" key="result" class="result-card">
              <p class="result-label">{{ activeType }} Screening Result</p>
              <p class="result-value">{{ result }}</p>
              <div class="bar-container">
                <div class="bar" :style="{ width: confidence + '%' }"></div>
              </div>
              <p class="result-confidence">Confidence: {{ confidence }}%</p>
            </div>

            <!-- All results -->
            <div v-else-if="allResults" key="allresults" class="all-results">
              <div v-for="r in allResults" :key="r.type" class="result-row">
                <span class="row-type">{{ r.type }}</span>
                <span class="row-prediction">{{ r.confidence >= 85 ? r.displayPrediction : 'Inconclusive' }}</span>
                <div class="bar-container">
                  <div class="bar" :style="{ width: r.confidence + '%' }"></div>
                </div>
                <span class="row-confidence">{{ r.confidence }}%</span>
              </div>
              <div class="highest-result">
                🏆 Highest confidence: <strong>{{ highestResult.type }} — {{ highestResult.confidence >= 85 ?
                  highestResult.displayPrediction : 'Inconclusive' }} ({{ highestResult.confidence }}%)</strong>
              </div>
            </div>

            <div v-else key="empty"></div>
          </transition>

          <transition name="fade">
            <p v-if="error" class="error">{{ error }}</p>
          </transition>
        </div>
      </div>
    </div>

    <!-- Recent uploads -->
    <transition name="fade-slide " >
      <div v-if="recentUploads.length" class="recent-uploads">
        <h3>Recent Uploads</h3>
        <div class="thumbs">
          <img v-for="(img, idx) in recentUploads" :key="idx" :src="img" class="thumb" @click="selectRecent(img)" />
        </div>
      </div>
    </transition>

    <!-- Bottom buttons -->
    <div class="action-buttons">
      <button class="action-btn" @click="uploadAgain">Upload New Image</button>
      <button class="action-btn" @click="goBack">Back to Home</button>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div class="footer-left">
        <img src="/DDARTECH_Research-removebg-preview.png" class="dept-logo" />
      </div>
      <div class="footer-right">
        <p>For technical support please call +3025510 30990 (office hours)</p>
        <p>email: <a href="mailto:ddart@med.duth.gr">ddart@med.duth.gr</a></p>
        <p class="made-by">Made by Andreas</p>
      </div>
    </div>

    <input type="file" accept="image/*" ref="fileInput" hidden @change="handleFileUpload" />
  </div>
</template>

<script>

export default {
  data() {
    return {
      image: null,
      result: null,
      confidence: null,
      error: null,
      loading: false,
      activeType: null,
      recentUploads: [],
      allResults: null
    }
  },

  computed: {
    highestResult() {
      if (!this.allResults) return null
      return [...this.allResults].sort((a, b) => b.confidence - a.confidence)[0]
    }
  },

  mounted() {
    this.image = this.$route.query.img || null
    this.loadRecentUploads()
    const type = this.$route.query.type
    if (type && this.image) {
      if (type === 'ALL') this.analyzeAll()
      else this.analyze(type)
    }
  },

  methods: {
    async analyze(type) {
      if (!this.image) return
      this.loading = true
      this.activeType = type
      this.result = null
      this.confidence = null
      this.error = null
      this.allResults = null

      try {
        const blob = await (await fetch(this.image)).blob()
        const endpoints = { Glaucoma: "/predict", DR: "/predict-dr", AMD: "/predict-amd" }

        if (type === "AMD") {
          const [amdData, glaucomaData] = await Promise.all([
            fetch(`https://labiris.myiplist.com/predict-amd`, { method: "POST", body: (() => { const f = new FormData(); f.append("file", blob, "eye.png"); return f })() }).then(r => r.json()),
            fetch(`https://labiris.myiplist.com/predict`, { method: "POST", body: (() => { const f = new FormData(); f.append("file", blob, "eye.png"); return f })() }).then(r => r.json())
          ])
          let glaucomaPrediction = glaucomaData.prediction
          if (glaucomaPrediction.toLowerCase() === "glaucoma") glaucomaPrediction = "Healthy"
          else if (glaucomaPrediction.toLowerCase() === "healthy") glaucomaPrediction = "Glaucoma"
          if (glaucomaPrediction === "Glaucoma" && glaucomaData.confidence >= 92) {
            this.confidence = glaucomaData.confidence
            this.result = `Glaucoma (detected during AMD screening, probably no AMD, ${glaucomaData.confidence}% confidence)`
          } else {
            this.confidence = amdData.confidence
            this.result = amdData.confidence < 85 ? "Inconclusive" : amdData.prediction
          }
          this.addToRecent(this.image)
          await this.saveToHistory(type, this.result, this.confidence)
          return
        }

        const formData = new FormData()
        formData.append("file", blob, "eye.png")
        const response = await fetch(`https://labiris.myiplist.com${endpoints[type]}`, { method: "POST", body: formData })
        const data = await response.json()
        if (!data.prediction) { this.error = "Prediction failed"; return }
        let prediction = data.prediction
        if (type === "Glaucoma") {
          if (prediction.toLowerCase() === "glaucoma") prediction = "Healthy"
          else if (prediction.toLowerCase() === "healthy") prediction = "Glaucoma"
        }
        this.confidence = data.confidence
        this.result = data.confidence < 85 ? "Inconclusive" : prediction
        this.addToRecent(this.image)
        await this.saveToHistory(type, this.result, this.confidence)
      } catch {
        this.error = "Backend connection failed"
      } finally {
        this.loading = false
      }
    },

    async analyzeAll() {
      if (!this.image) return
      this.loading = true
      this.activeType = 'ALL'
      this.result = null
      this.confidence = null
      this.error = null
      this.allResults = null

      try {
        const blob = await (await fetch(this.image)).blob()
        const endpoints = { Glaucoma: "/predict", DR: "/predict-dr", AMD: "/predict-amd" }
        const results = await Promise.all(
          Object.entries(endpoints).map(async ([type, endpoint]) => {
            const formData = new FormData()
            formData.append("file", blob, "eye.png")
            const res = await fetch(`https://labiris.myiplist.com${endpoint}`, { method: "POST", body: formData })
            const data = await res.json()
            let prediction = data.prediction
            if (type === "Glaucoma") {
              if (prediction.toLowerCase() === "glaucoma") prediction = "Healthy"
              else if (prediction.toLowerCase() === "healthy") prediction = "Glaucoma"
            }
            return { type, prediction: data.prediction, displayPrediction: prediction, confidence: data.confidence }
          })
        )
        this.allResults = results
        this.addToRecent(this.image)
        for (const r of results) {
          await this.saveToHistory(r.type, r.displayPrediction, r.confidence)
        }
      } catch {
        this.error = "Backend connection failed"
      } finally {
        this.loading = false
      }
    },

    async saveToHistory(type, result, confidence) {
      const stored = localStorage.getItem('ddart_patient')
      if (!stored) return
      const patient = JSON.parse(stored)
      try {
        await fetch('https://labiris.myiplist.com/history/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            patient_id: patient.id,
            screening_type: type,
            result: result,
            confidence: confidence,
            image_b64: this.image
          })
        })
      } catch { }
    },

    uploadAgain() { this.$refs.fileInput.click() },

    handleFileUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => {
        this.image = e.target.result
        this.result = null
        this.confidence = null
        this.activeType = null
        this.allResults = null
        this.addToRecent(this.image)
      }
      reader.readAsDataURL(file)
    },

    dropFile(event) {
      const file = event.dataTransfer.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => {
        this.image = e.target.result
        this.result = null
        this.confidence = null
        this.activeType = null
        this.allResults = null
        this.addToRecent(this.image)
      }
      reader.readAsDataURL(file)
    },

    addToRecent(img) {
      if (!this.recentUploads.includes(img)) {
        this.recentUploads.unshift(img)
        if (this.recentUploads.length > 5) this.recentUploads.pop()
        localStorage.setItem("recentUploads", JSON.stringify(this.recentUploads))
      }
    },

    loadRecentUploads() {
      const saved = localStorage.getItem("recentUploads")
      if (saved) this.recentUploads = JSON.parse(saved)
    },

    selectRecent(img) {
      this.image = img
      this.result = null
      this.confidence = null
      this.activeType = null
      this.allResults = null
    },

    goBack() { this.$router.push("/") }
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

.process-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 20px 0;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 24px;
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
  line-height: 1;
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 2px;
}

.logo span {
  color: #e53e3e;
  font-size: 48px;
  font-weight: 900;
  letter-spacing: -1px;
  font-family: 'Arial Black', Arial, sans-serif;
}

.main-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  width: 100%;
  max-width: 760px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.card-inner {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 320px;
}

.image-zone {
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

.image-zone:hover {
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

.preview {
  max-width: 100%;
  max-height: 280px;
  border-radius: 4px;
  object-fit: contain;
}

.right-panel {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  width: 100%;
  padding: 11px 14px;
  border: none;
  border-radius: 4px;
  font-family: 'Source Sans 3', sans-serif;
  font-size: 13.5px;
  font-weight: 600;
  color: white;
  background: #2b6cb0;
  cursor: pointer;
  transition: all 0.25s ease;
  letter-spacing: 0.3px;
  text-align: center;
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.action-btn:hover:not(:disabled) {
  background: #2c5282;
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
}

.action-btn.all {
  background: #2d3748;
}

.action-btn.all:hover:not(:disabled) {
  background: #1a202c;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 4px solid #e2e8f0;
  border-top-color: #2b6cb0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-weight: 600;
  color: #2d3748;
  margin: 0;
  font-size: 14px;
}

.loading-subtext {
  font-size: 11px;
  color: #a0aec0;
  margin: 0;
}

.result-card {
  background: #ebf8ff;
  border: 1px solid #bee3f8;
  border-radius: 4px;
  padding: 14px 16px;
}

.result-label {
  font-size: 11px;
  color: #4a6fa5;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 4px;
  font-weight: 600;
}

.result-value {
  font-size: 20px;
  font-weight: 700;
  color: #2c5282;
  margin: 0 0 10px;
  font-family: 'Playfair Display', serif;
}

.result-confidence {
  font-size: 12px;
  color: #4a6fa5;
  margin: 4px 0 0;
}

.all-results {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.row-type {
  width: 70px;
  font-weight: 600;
  color: #2d3748;
  flex-shrink: 0;
}

.row-prediction {
  width: 100px;
  color: #4a5568;
  flex-shrink: 0;
}

.row-confidence {
  width: 40px;
  text-align: right;
  color: #718096;
  flex-shrink: 0;
  font-size: 12px;
}

.bar-container {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.bar {
  height: 100%;
  background: #2b6cb0;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.highest-result {
  font-size: 12px;
  color: #4a5568;
  padding-top: 8px;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

.error {
  color: #c53030;
  font-size: 13px;
  font-weight: 600;
}

.recent-uploads {
  width: 100%;
  max-width: 760px;
  margin-bottom: 16px;
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

.action-buttons {
  display: flex;
  gap: 12px;
  width: 100%;
  max-width: 760px;
  margin-bottom: 20px;
}

.action-buttons .action-btn {
  flex: 1;
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
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>