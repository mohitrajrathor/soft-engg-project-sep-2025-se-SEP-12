<template>
  <div class="login-wrapper">
    <div class="login-box">
      
      <!-- 🔹 Left Section -->
      <div class="left-section">
        <div class="text-content">
          <h1>Welcome to AURA</h1>
          <p class="lead">
            Your personalized academic assistant — track, analyze, and enhance your learning journey.
          </p>
          <p class="small">
            Designed for IITM BS students.
          </p>
        </div>
      </div>

      <!-- 🔹 Right Section -->
      <div class="right-section">
        <div class="form-content">
          <div class="text-end mb-3">
            <small class="text-muted">
              New here? 
              <router-link to="/register" class="text-primary fw-semibold text-decoration-none">
                Sign up
              </router-link>
            </small>
          </div>

          <h2 class="text-primary fw-bold mb-2">Sign in to AURA</h2>
          <p class="text-muted mb-4">Your academic dashboard awaits.</p>

          <form @submit.prevent>
            <div class="mb-3">
              <input type="email" class="form-control rounded-pill" placeholder="IITM email" required />
            </div>
            <div class="mb-4">
              <input type="password" class="form-control rounded-pill" placeholder="Password" required />
            </div>

            <button class="btn btn-gradient rounded-pill w-100 mb-3 fw-semibold">
              Sign in
            </button>

            <p class="text-center text-muted small mb-3">or continue with</p>

            <div class="d-flex justify-content-center gap-2">
              <button type="button" class="btn btn-outline-primary rounded-pill w-50">
                <i class="bi bi-google me-1"></i> Google
              </button>
              <button type="button" class="btn btn-outline-primary rounded-pill w-50">
                <i class="bi bi-facebook me-1"></i> Facebook
              </button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* ✅ Page background */
.login-wrapper {
  background: url('/src/assets/login.jpg') no-repeat center center / cover;
  height: 100dvh;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* ✅ Main login box */
.login-box {
  display: flex;
  flex-direction: row;
  width: 1000px; /* fixed width */
  height: 600px; /* fixed height */
  border-radius: 1.5rem;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 8px 35px rgba(0, 0, 0, 0.3);
}

/* ✅ Left Section */
.left-section {
  width: 50%;
  background: url('/src/assets/background.png') no-repeat center center / cover;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2.5rem;
}

.text-content {
  background: rgba(255, 255, 255, 0.85);
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  width: 85%;
  max-width: 450px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.text-content h1 {
  color: #000000c7;
  font-weight: 800;
  font-size: 2.2rem;
  margin-bottom: 1rem;
}

.text-content .lead {
  color: #212121;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.text-content .small {
  font-size: 0.95rem;
  color: #424242;
}

/* ✅ Right Section */
.right-section {
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem;
}

.form-content {
  width: 100%;
  max-width: 360px;
}

/* ✅ Buttons */
.btn-gradient {
  background: linear-gradient(135deg, #1976d2, #004ba0);
  border: none;
  color: white;
  font-size: 1.05rem;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  background: linear-gradient(135deg, #0d47a1, #002b7a);
  transform: scale(1.03);
}

/* ✅ Inputs */
input.form-control {
  padding: 0.9rem 1.1rem;
  border: 1px solid #cfd8dc;
  font-size: 1rem;
}

input.form-control:focus {
  border-color: #1976d2;
  box-shadow: 0 0 10px rgba(25, 118, 210, 0.3);
}

/* ✅ Prevent auto shrink on zoom */
* {
  flex-shrink: 0;
}

/* ✅ Responsive for small screens */
@media (max-width: 992px) {
  .login-box {
    flex-direction: column;
    width: 95%;
    height: auto;
  }

  .left-section {
    width: 100%;
    height: 250px;
    padding: 1.5rem;
  }

  .text-content {
    width: 100%;
    padding: 1.5rem;
  }

  .right-section {
    width: 100%;
    padding: 2rem 1.5rem;
  }
}
</style>
