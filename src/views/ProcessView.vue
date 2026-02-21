<template>
  <div class="process-container">
    <h1 class="title">DDART A.I. – Eye Analysis</h1>

    <div class="layout">
      <!-- LEFT PANEL -->
      <div class="left-panel">
        <div class="image-card" @drop.prevent="dropFile" @dragover.prevent>
          <img v-if="image" :src="image" class="preview" />
          <p v-else class="placeholder">Drag & drop or upload an image</p>
        </div>

        <div class="recent-uploads" v-if="recentUploads.length">
          <h3>Recent Uploads</h3>
          <div class="uploads-list">
            <div
              v-for="(img, index) in recentUploads"
              :key="index"
              class="upload-thumb"
              :class="{ active: img === image }"
              @click="selectRecent(img)"
            >
              <img :src="img" />
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT PANEL -->
      <div class="right-panel">
        <div class="button-group">
          <button class="analyze-btn glaucoma" @click="analyze('Glaucoma')" :disabled="loading">
            {{ loading && activeType === 'Glaucoma' ? 'Analyzing...' : 'Analyze Glaucoma' }}
          </button>
          <button class="analyze-btn dr" @click="analyze('DR')" :disabled="loading">
            {{ loading && activeType === 'DR' ? 'Analyzing...' : 'Analyze Diabetic Retinopathy' }}
          </button>
          <button class="analyze-btn amd" @click="analyze('AMD')" :disabled="loading">
            {{ loading && activeType === 'AMD' ? 'Analyzing...' : 'Analyze AMD' }}
          </button>
          <button class="analyze-btn all" @click="analyzeAll" :disabled="loading">
            {{ loading && activeType === 'ALL' ? 'Analyzing All...' : 'Analyze All Conditions' }}
          </button>
        </div>

        <!-- Single result -->
        <div v-if="result" class="result-card" :class="activeType ? activeType.toLowerCase() : ''">
          <p class="result-text">{{ activeType }} Prediction: <strong>{{ result }}</strong></p>
          <div class="confidence-bar-container">
            <div class="confidence-bar" :style="{ width: confidence + '%' }"></div>
          </div>
          <p class="confidence">{{ confidence }}%</p>
        </div>

        <!-- All results -->
        <div v-if="allResults" class="all-results">
          <div
            v-for="r in allResults"
            :key="r.type"
            class="all-result-row"
            :class="r.type.toLowerCase()"
          >
            <span class="all-result-type">{{ r.type }}</span>
            <span class="all-result-prediction">
              {{ r.confidence >= 85 ? r.displayPrediction : 'Inconclusive' }}
            </span>
            <div class="confidence-bar-container">
              <div class="confidence-bar" :style="{ width: r.confidence + '%' }"></div>
            </div>
            <span class="all-result-confidence">{{ r.confidence }}%</span>
          </div>

          <div class="highest-result">
             Highest confidence:
            <strong>
              {{ highestResult.type }} —
              {{ highestResult.confidence >= 85 ? highestResult.displayPrediction : 'Inconclusive' }}
              ({{ highestResult.confidence }}%)
            </strong>
          </div>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <div class="actions">
          <button class="secondary" @click="uploadAgain">Upload New Image</button>
          <button class="secondary" @click="goBack">Back</button>
        </div>
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

    // Auto-run if type was passed from home page
    const type = this.$route.query.type
    if (type && this.image) {
      if (type === 'ALL') {
        this.analyzeAll()
      } else {
        this.analyze(type)
      }
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
        const formData = new FormData()
        formData.append("file", blob, "eye.png")

        const endpoints = {
          Glaucoma: "/predict",
          DR: "/predict-dr",
          AMD: "/predict-amd"
        }

        const response = await fetch(
          `https://labiris.myiplist.com${endpoints[type]}`,
          { method: "POST", body: formData }
        )

        const data = await response.json()

        if (!data.prediction) {
          this.error = "Prediction failed"
          return
        }

        let prediction = data.prediction

        if (type === "Glaucoma") {
          if (prediction.toLowerCase() === "glaucoma") prediction = "Healthy"
          else if (prediction.toLowerCase() === "healthy") prediction = "Glaucoma"
        }

        this.confidence = data.confidence
        this.result = data.confidence < 85 ? "Inconclusive" : prediction
        this.addToRecent(this.image)

      } catch (err) {
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

        const endpoints = {
          Glaucoma: "/predict",
          DR: "/predict-dr",
          AMD: "/predict-amd"
        }

        const results = await Promise.all(
          Object.entries(endpoints).map(async ([type, endpoint]) => {
            const formData = new FormData()
            formData.append("file", blob, "eye.png")
            const res = await fetch(`https://labiris.myiplist.com${endpoint}`, {
              method: "POST",
              body: formData
            })
            const data = await res.json()

            let prediction = data.prediction
            if (type === "Glaucoma") {
              if (prediction.toLowerCase() === "glaucoma") prediction = "Healthy"
              else if (prediction.toLowerCase() === "healthy") prediction = "Glaucoma"
            }

            return {
              type,
              prediction: data.prediction,
              displayPrediction: prediction,
              confidence: data.confidence
            }
          })
        )

        this.allResults = results
        this.addToRecent(this.image)

      } catch (err) {
        this.error = "Backend connection failed"
      } finally {
        this.loading = false
      }
    },

    uploadAgain() {
      this.$refs.fileInput.click()
    },

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

    goBack() {
      this.$router.push("/")
    }
  }
}
</script>

<style>
html, body {
  margin: 0;
  height: 100%;
  overflow: auto;
}

.process-container {
  min-height: 100vh;
  background: #f4f6fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  font-family: "Segoe UI", Tahoma, sans-serif;
}

.title {
  color: #007bff;
  margin-bottom: 10px;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  width: 100%;
  max-width: 1100px;
}

.left-panel, .right-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.image-card {
  background: white;
  border-radius: 15px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.preview {
  max-width: 100%;
  max-height: 260px;
  border-radius: 10px;
}

.placeholder { color: #777; }

.recent-uploads h3 { font-size: 14px; text-align: center; }

.uploads-list { display: flex; gap: 8px; justify-content: center; }

.upload-thumb {
  width: 60px;
  cursor: pointer;
  border-radius: 6px;
  border: 2px solid transparent;
}

.upload-thumb.active { border-color: #007bff; }
.upload-thumb img { width: 100%; border-radius: 6px; }

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.analyze-btn {
  padding: 12px;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
}

.analyze-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.analyze-btn:hover:not(:disabled) { transform: translateY(-1px); opacity: 0.9; }

.analyze-btn.glaucoma { background: #dc3545; }
.analyze-btn.dr       { background: #17a2b8; }
.analyze-btn.amd      { background: #ffc107; color: #212529; }
.analyze-btn.all      { background: #6f42c1; }

/* Single result card */
.result-card {
  padding: 15px;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  color: white;
}

.result-card.glaucoma { background: #dc3545; }
.result-card.dr       { background: #17a2b8; }
.result-card.amd      { background: #ffc107; color: #212529; }

.confidence-bar-container {
  width: 80%;
  height: 12px;
  background: rgba(255,255,255,0.4);
  border-radius: 6px;
  margin: 6px auto;
}

.confidence-bar {
  height: 100%;
  background: white;
  border-radius: 6px;
  transition: width 0.5s ease;
}

/* All results */
.all-results {
  background: white;
  border-radius: 12px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.all-result-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.all-result-row.glaucoma { background: #dc3545; }
.all-result-row.dr       { background: #17a2b8; }
.all-result-row.amd      { background: #ffc107; color: #212529; }

.all-result-row .confidence-bar-container {
  flex: 1;
  margin: 0;
  width: auto;
}

.all-result-type        { width: 75px; flex-shrink: 0; }
.all-result-prediction  { width: 110px; flex-shrink: 0; }
.all-result-confidence  { width: 45px; text-align: right; flex-shrink: 0; }

.highest-result {
  text-align: center;
  color: #333;
  font-size: 14px;
  padding-top: 8px;
  border-top: 1px solid #eee;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.secondary {
  padding: 8px 14px;
  border-radius: 8px;
  background: #6c757d;
  color: white;
  border: none;
  cursor: pointer;
}

.error { color: red; font-weight: 600; }
</style>