<template>
    <div class="process-container">
      <h2 class="title">Diabetic Retinopathy Detection</h2>
  
      <img :src="image" class="preview" />
  
      <button @click="runDetection" :disabled="loading">
        {{ loading ? "Analyzing..." : "Run DR Detection" }}
      </button>

    
      <div v-if="result" class="result-box">
        <p><strong>Stage:</strong> {{ result.prediction }}</p>
        <p><strong>Confidence:</strong> {{ result.confidence }}%</p>
      </div>
  
      <div class="actions">
        <button class="secondary" @click="uploadAgain">🔄 Upload Again</button>
        <button class="secondary" @click="goBack">⬅ Back</button>
      </div>
  
      <p class="footer">made by andreas</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        image: this.$route.query.img,
        loading: false,
        result: null,
        error: null
      }
    },
    methods: {
      async runDetection() {
        this.loading = true
        this.result = null
        this.error = null
  
        try {
          // Convert base64 image → Blob
          const res = await fetch(this.image)
          const blob = await res.blob()
  
          // Prepare form data
          const formData = new FormData()
          formData.append("file", blob, "eye.png")
  
          const response = await fetch(
  "https://nonglobular-unmisgivingly-zoie.ngrok-free.dev/predict-dr", 
  {
    method: "POST",
    body: formData
  }
)
  
          const data = await response.json()
  
          if (data.prediction) {
            this.result = {
              prediction: data.prediction,
              confidence: data.confidence
            }
          } else {
            this.error = "Prediction failed"
          }
        } catch (err) {
          this.error = "Backend connection failed"
          console.error(err)
        } finally {
          this.loading = false
        }
      },
  
      uploadAgain() {
        this.$router.push({ name: "Home" })
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
    gap: 15px;
    margin-top: 30px;
    font-family: Arial, sans-serif;
  }
  
  .title {
    font-size: 22px;
    color: #28a745;
  }
  
  .preview {
    max-width: 300px;
    border-radius: 8px;
    border: 2px solid #ccc;
  }
  
  button {
    padding: 10px 18px;
    border: none;
    border-radius: 6px;
    background-color: #28a745;
    color: white;
    cursor: pointer;
    font-size: 15px;
  }
  
  button:disabled {
    background-color: #aaa;
    cursor: not-allowed;
  }
  
  .result-box {
    background: #f1f1f1;
    padding: 15px;
    border-radius: 8px;
    width: 300px;
    text-align: left;
  }
  
  .actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
  }
  
  .secondary {
    background-color: #6c757d;
  }
  
  .footer {
    position: fixed;
    bottom: 10px;
    right: 10px;
    font-size: 12px;
    color: #555;
  }
  </style>