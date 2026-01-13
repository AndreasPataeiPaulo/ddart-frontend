<template>
  <div class="process-container">
    <h1 class="title">AI Eye Analysis</h1>

    <div class="image-card">
      <img :src="image" class="preview" />
    </div>

    <button class="analyze-btn" @click="sendToAI" :disabled="loading">
      {{ loading ? "Analyzing..." : "Analyze Image" }}
    </button>

    <div class="actions">
      <button class="secondary" @click="uploadAgain">🔄 Upload Again</button>
      <button class="secondary" @click="goBack">⬅ Back</button>
    </div>

    <div v-if="result" class="result-card" :class="resultClass">
      <p class="result-text">
        🧠 Prediction: <strong>{{ result }}</strong>
      </p>
      <p class="confidence">
        Confidence: {{ confidence }}%
      </p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
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
      loading: false
    }
  },
  computed: {
    resultClass() {
      if (this.result === "Healthy") return "healthy"
      if (this.result === "Glaucoma") return "glaucoma"
      if (this.result === "AMD") return "amd"
      return ""
    }
  },
  mounted() {
    this.image = this.$route.query.img
  },
  methods: {
    async sendToAI() {
      try {
        this.loading = true
        this.result = null
        this.confidence = null
        this.error = null

        const res = await fetch(this.image)
        const blob = await res.blob()

        const formData = new FormData()
        formData.append("file", blob, "eye.png")

        const response = await fetch(
          "https://nonglobular-unmisgivingly-zoie.ngrok-free.dev/predict",
          { method: "POST", body: formData }
        )

        const data = await response.json()

        if (data.prediction) {
          this.result = data.prediction
          this.confidence = data.confidence
        } else {
          this.error = "Prediction failed"
        }
      } catch (err) {
        this.error = "Backend connection failed"
      } finally {
        this.loading = false
      }
    },
    uploadAgain() {
      this.$router.push("/")
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style>
.process-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 30px 20px;
  background: #f4f6fa;
  min-height: 100vh;
}

.title {
  font-size: 32px;
  color: #007bff;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.image-card {
  background: white;
  padding: 15px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.preview {
  max-width: 300px;
  border-radius: 12px;
  border: 2px solid #007bff;
}

.analyze-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(90deg, #007bff, #00c6ff);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.analyze-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,198,255,0.4);
}

.actions {
  display: flex;
  gap: 12px;
}

.secondary {
  background-color: #6c757d;
  padding: 10px 16px;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.secondary:hover {
  background-color: #5a6268;
}

.result-card {
  margin-top: 20px;
  padding: 18px 22px;
  border-radius: 15px;
  width: 320px;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  color: white;
}

.healthy {
  background: #28a745;
}

.glaucoma {
  background: #dc3545;
}

.amd {
  background: #ffc107;
  color: #212529;
}

.result-text {
  font-size: 20px;
  margin-bottom: 6px;
}

.confidence {
  font-size: 16px;
}

.error {
  color: red;
  margin-top: 10px;
  font-weight: 600;
}
</style>
