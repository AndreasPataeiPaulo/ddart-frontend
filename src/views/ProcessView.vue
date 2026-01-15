<template>
  <div class="process-container">
    <h1 class="title">DDART A.I. – Eye Analysis</h1>

    <div class="layout">
      <!-- LEFT PANEL -->
      <div class="left-panel">
        <div
          class="image-card"
          @drop.prevent="dropFile"
          @dragover.prevent
        >
          <img v-if="image" :src="image" class="preview" />
          <p v-else class="placeholder">
            Drag & drop or upload an image
          </p>
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
          <button
            class="analyze-btn glaucoma"
            @click="analyze('Glaucoma')"
            :disabled="loading"
          >
            {{ loading && activeType === 'Glaucoma'
              ? 'Analyzing...'
              : 'Analyze Glaucoma' }}
          </button>

          <button
            class="analyze-btn dr"
            @click="analyze('DR')"
            :disabled="loading"
          >
            {{ loading && activeType === 'DR'
              ? 'Analyzing...'
              : 'Analyze Diabetic Retinopathy' }}
          </button>

          <button
            class="analyze-btn amd"
            @click="analyze('AMD')"
            :disabled="loading"
          >
            {{ loading && activeType === 'AMD'
              ? 'Analyzing...'
              : 'Analyze AMD' }}
          </button>
        </div>

        <div v-if="result" class="result-card" :class="resultClass">
          <p class="result-text">
            {{ activeType }} Prediction: <strong>{{ result }}</strong>
          </p>

          <div class="confidence-bar-container">
            <div
              class="confidence-bar"
              :style="{ width: confidence + '%' }"
            ></div>
          </div>

          <p class="confidence">{{ confidence }}%</p>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <div class="actions">
          <button class="secondary" @click="uploadAgain">
            Upload New Image
          </button>
          <button class="secondary" @click="goBack">
            Back
          </button>
        </div>
      </div>
    </div>

    <!-- Hidden Input -->
    <input
      type="file"
      accept="image/*"
      ref="fileInput"
      hidden
      @change="handleFileUpload"
    />
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
      recentUploads: []
    }
  },

  computed: {
    resultClass() {
      return this.activeType
        ? this.activeType.toLowerCase()
        : ""
    }
  },

  mounted() {
    this.image = this.$route.query.img || null
    this.loadRecentUploads()
  },

  methods: {
    async analyze(type) {
      if (!this.image) return

      this.loading = true
      this.activeType = type
      this.result = null
      this.confidence = null
      this.error = null

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
          `https://nonglobular-unmisgivingly-zoie.ngrok-free.dev${endpoints[type]}`,
          {
            method: "POST",
            body: formData
          }
        )

        const data = await response.json()

        if (!data.prediction) {
          this.error = "Prediction failed"
          return
        }

        let prediction = data.prediction

// 🔄 Fix swapped Glaucoma labels
if (type === "Glaucoma") {
  if (prediction.toLowerCase() === "glaucoma") {
    prediction = "Healthy"
  } else if (prediction.toLowerCase() === "healthy") {
    prediction = "Glaucoma"
  }
}

this.result = prediction
this.confidence = data.confidence
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
        this.addToRecent(this.image)
      }
      reader.readAsDataURL(file)
    },

    addToRecent(img) {
      if (!this.recentUploads.includes(img)) {
        this.recentUploads.unshift(img)
        if (this.recentUploads.length > 5) {
          this.recentUploads.pop()
        }
        localStorage.setItem(
          "recentUploads",
          JSON.stringify(this.recentUploads)
        )
      }
    },

    loadRecentUploads() {
      const saved = localStorage.getItem("recentUploads")
      if (saved) {
        this.recentUploads = JSON.parse(saved)
      }
    },

    selectRecent(img) {
      this.image = img
      this.result = null
      this.confidence = null
      this.activeType = null
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
  overflow: hidden;
}

.process-container {
  height: 100vh;
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
  flex: 1;
}

.left-panel,
.right-panel {
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

.placeholder {
  color: #777;
}

.recent-uploads h3 {
  font-size: 14px;
  text-align: center;
}

.uploads-list {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.upload-thumb {
  width: 60px;
  cursor: pointer;
  border-radius: 6px;
  border: 2px solid transparent;
}

.upload-thumb.active {
  border-color: #007bff;
}

.upload-thumb img {
  width: 100%;
  border-radius: 6px;
}

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
}

.glaucoma { background: #dc3545; }
.dr { background: #17a2b8; }
.amd { background: #ffc107; color: #212529; }

.result-card {
  padding: 15px;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  color: white;
}

.glaucoma { background: #dc3545; }
.dr { background: #17a2b8; }
.amd { background: #ffc107; color: #212529; }

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

.error {
  color: red;
  font-weight: 600;
}
</style>
