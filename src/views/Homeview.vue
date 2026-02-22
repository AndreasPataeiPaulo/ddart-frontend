<template>
  <div class="home-container">
    <!-- Header -->
    <div class="header">
      <p class="university">Democritus University of Thrace – DDART spin-off company</p>
      <p class="subtitle">Ophthalmology A.I. Screening Program</p>
      <div class="logo">DDART<span>AI</span></div>
    </div>

    <!-- Main Card -->
    <div class="main-card">
      <div class="card-inner">
        <!-- Upload area -->
        <div class="upload-zone" @drop.prevent="dropFile" @dragover.prevent @click="triggerUpload">
          <input type="file" accept="image/*" ref="fileInput" hidden @change="uploadFile" />
          <div v-if="!uploadedImage" class="upload-placeholder">
            <div class="upload-icon">👁</div>
            <p>Upload a fundus image to begin screening</p>
            <span>Click or drag & drop</span>
          </div>
          <img v-else :src="uploadedImage" class="uploaded-image" />
        </div>

        <!-- Description -->
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
            replace — clinical judgment. Images are processed locally and are not stored.
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
      <button class="action-btn glaucoma" @click="analyzeImage('Glaucoma')" :disabled="!uploadedImage">
        Glaucoma Screening
      </button>
      <button class="action-btn dr" @click="analyzeImage('DR')" :disabled="!uploadedImage">
        Diabetic Retinopathy
      </button>
      <button class="action-btn amd" @click="analyzeImage('AMD')" :disabled="!uploadedImage">
        AMD Screening
      </button>
      <button class="action-btn all" @click="analyzeImage('ALL')" :disabled="!uploadedImage">
        🔍 Full Screening
      </button>
    </div>

    <!-- Recent uploads -->
    <div v-if="recentUploads.length" class="recent-uploads">
      <h3>Recent Uploads</h3>
      <div class="thumbs">
        <img
          v-for="(img, idx) in recentUploads"
          :key="idx"
          :src="img"
          class="thumb"
          @click="uploadedImage = img"
        />
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div class="footer-left">
        <div class="dept-placeholder">DEPARTMENT OF OPHTHALMOLOGY</div>
      </div>
      <div class="footer-right">
        <p>For technical support please call +3025510 30990 (office hours)</p>
        <p>email: <a href="mailto:ddart@med.duth.gr">ddart@med.duth.gr</a></p>
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
    }
  },
  methods: {
    triggerUpload() {
      this.$refs.fileInput.click()
    },
    uploadFile(event) {
      const file = event.target.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadedImage = e.target.result
        this.addToRecent(this.uploadedImage)
      }
      reader.readAsDataURL(file)
    },
    dropFile(event) {
      const file = event.dataTransfer.files[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadedImage = e.target.result
        this.addToRecent(this.uploadedImage)
      }
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
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body {
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
}

.university {
  font-size: 14px;
  color: #2c5282;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin: 0 0 4px;
}

.subtitle {
  font-size: 13px;
  color: #4a6fa5;
  margin: 0 0 16px;
}

.logo {
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  font-weight: 700;
  color: #2c5282;
  letter-spacing: 2px;
  line-height: 1;
}

.logo span { color: #e53e3e; }

.main-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  width: 100%;
  max-width: 760px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
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
}

.upload-zone:hover { background: #edf2f7; }

.upload-placeholder { text-align: center; color: #718096; }
.upload-icon { font-size: 36px; margin-bottom: 10px; }
.upload-placeholder p { font-size: 14px; margin: 0 0 6px; color: #4a5568; font-weight: 600; }
.upload-placeholder span { font-size: 12px; color: #a0aec0; }

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

.description p:last-child { margin-bottom: 0; }

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
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: 0.3px;
}

.action-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.action-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }

.action-btn.glaucoma { background: #c53030; }
.action-btn.dr       { background: #2b6cb0; }
.action-btn.amd      { background: #276749; }
.action-btn.all      { background: #2d3748; }

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

.thumbs { display: flex; gap: 8px; }

.thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: border-color 0.2s;
}

.thumb:hover { border-color: #2b6cb0; }

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

.dept-placeholder {
  font-size: 11px;
  font-weight: 700;
  color: #4a6fa5;
  letter-spacing: 0.5px;
  border: 1px solid #4a6fa5;
  padding: 6px 10px;
  border-radius: 3px;
}

.footer-right { text-align: right; }
.footer-right p { font-size: 12px; color: #718096; margin: 2px 0; }
.footer-right a { color: #2b6cb0; text-decoration: none; }
</style>