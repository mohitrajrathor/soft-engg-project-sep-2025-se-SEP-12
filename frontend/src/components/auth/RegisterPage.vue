<template>
  <div class="signup-wrapper d-flex align-items-center justify-content-center">
    <div class="container-fluid d-flex justify-content-center align-items-center">
      <div class="row big-card shadow-lg rounded-4 overflow-hidden">
        
        <!-- Left Side -->
        <div class="col-lg-6 col-md-5 left-section d-flex flex-column justify-content-center align-items-center">
          <div class="text-content text-center">
            <h1 class="fw-bold mb-3 display-6 text-dark">Join AURA Today</h1>
            <p class="lead fw-medium mb-3 text-dark">
              Explore personalized learning tools and study smarter with AURA.
            </p>
            <p class="small text-dark">AI-powered tools built for IITM BS students.</p>
          </div>
        </div>

        <!-- Right Side -->
        <div class="col-lg-6 col-md-7 form-section d-flex flex-column justify-content-center align-items-center bg-white">
          <div class="form-container p-4 p-md-5 w-100" style="max-width: 420px;">
            <div class="text-end mb-3">
              <small class="text-muted">
                Already a user?
                <router-link to="/login" class="text-primary fw-semibold text-decoration-none">Sign in</router-link>
              </small>
            </div>

            <h3 class="fw-bold mb-2 text-primary text-center">Create your account</h3>
            <p class="text-muted mb-4 text-center">Get started with premium features</p>

            <form>
              <div class="mb-3">
                <input type="text" class="form-control rounded-pill fs-6" placeholder="Your full name" />
              </div>
              <div class="mb-3">
                <input type="email" class="form-control rounded-pill fs-6" placeholder="IITM email" />
              </div>
              <div class="mb-3">
                <input type="password" class="form-control rounded-pill fs-6" placeholder="Create password" />
              </div>
              <div class="mb-4">
                <input type="password" class="form-control rounded-pill fs-6" placeholder="Confirm password" />
              </div>
              <div class="mb-4">
                <select class="form-select rounded-pill fs-6">
                  <option disabled selected>Select your role</option>
                  <option value="student">Student</option>
                  <option value="ta">Teaching Assistant (TA)</option>
                  <option value="instructor">Instructor</option>
                </select>
              </div>

              <button type="submit" class="btn btn-gradient rounded-pill w-100 mb-3 fw-semibold fs-5 text-white">
                Sign up
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.signup-wrapper {
  background: url('/src/assets/login.jpg') no-repeat center center / cover;
  min-height: 100dvh; /* ✅ adjusts better with zoom and browser bars */
  width: 100%;
  overflow: hidden;
}

.big-card {
  width: 90%;
  max-width: 1100px;
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
}

.left-section {
  background: url('/src/assets/background.png') no-repeat center center / cover;
  min-height: 60dvh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.left-section .text-content {
  background: rgba(255, 255, 255, 0.85);
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  width: 85%;
  text-align: center;
}

.btn-gradient {
  background: linear-gradient(135deg, #1976d2, #004ba0);
  border: none;
  transition: 0.3s;
}

.btn-gradient:hover {
  background: linear-gradient(135deg, #0d47a1, #002b7a);
  transform: scale(1.03);
}

/* Responsive */
@media (max-width: 992px) {
  .big-card {
    flex-direction: column;
  }
  .left-section {
    min-height: 30dvh;
  }
}

@media (max-width: 768px) {
  .left-section {
    display: none;
  }
  .form-section {
    flex: 1 1 100%;
  }
}
</style>
