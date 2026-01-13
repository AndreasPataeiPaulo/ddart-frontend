<template>
    <div class="process-container">
      <h2>AI Eye Analysis</h2>
  
      <img :src="image" class="preview" />
  
      <button @click="sendToAI" :disabled="loading">
        {{ loading ? "Analyzing..." : "Analyze Image" }}
      </button>
  
      <div class="actions">
        <button class="secondary" @click="uploadAgain">
          🔄 Upload Again
        </button>
  
        <button class="secondary" @click="goBack">
          ⬅ Back
        </button>
      </div>
  
      <div v-if="result" class="result-box" :class="resultClass">
        <p class="result-text">
          🧠 Prediction: <strong>{{ result }}</strong>
        </p>
        <p class="confidence">
          Confidence: {{ confidence }}%
        </p>
      </div>
  
      <p v-if="error" class="error">
        {{ error }}
      </p>
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
  {
    method: "POST",
    body: formData
  }
)
  
          const data = await response.json()
  
          if (data.prediction) {
            // 🔄 Reverse the result
            if (data.prediction === "Healthy") {
              this.result = "Glaucoma"
            } else if (data.prediction === "Glaucoma") {
              this.result = "Healthy"
            }
  
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
    text-align: center;
    padding: 20px;
  }
  
  .preview {
    width: 240px;
    border-radius: 10px;
    margin-bottom: 15px;
  }
  
  button {
    padding: 10px 16px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }
  
  button:disabled {
    opacity: 0.6;
  }
  
  .actions {
    margin-top: 15px;
    display: flex;
    justify-content: center;
    gap: 10px;
  }
  
  .secondary {
    background: #6c757d;
  }
  
  .result-box {
    margin-top: 20px;
    padding: 15px;
    border-radius: 10px;
  }
  
  .healthy {
    background: #e6f7ec;
    color: #1e7e34;
  }
  
  .glaucoma {
    background: #fdecea;
    color: #a71d2a;
  }
  
  .result-text {
    font-size: 20px;
  }
  
  .confidence {
    margin-top: 6px;
    font-size: 16px;
  }
  
  .error {
    margin-top: 10px;
    color: red;
  }
  </style>
  