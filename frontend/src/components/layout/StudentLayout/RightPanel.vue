<template>
  <div class="border-start bg-white p-3" style="width: 300px; min-height: 100vh;">
    <!-- Pinned Resources -->
    <div class="mb-4">
      <h6 class="fw-semibold text-secondary mb-3">
        <i class="bi bi-pin-angle me-2 text-primary"></i>Pinned resources
      </h6>
      <div class="list-group small">
        <a href="#" class="list-group-item list-group-item-action border rounded mb-2" @click="openResource('CS301 • Lab 2 rubric')">
          <i class="bi bi-journal-text me-2 text-secondary"></i>CS301 • Lab 2 rubric
        </a>
        <a href="#" class="list-group-item list-group-item-action border rounded mb-2" @click="openResource('Systems • Lecture 5')">
          <i class="bi bi-gear-fill me-2 text-secondary"></i>Systems • Lecture 5
        </a>
        <a href="#" class="list-group-item list-group-item-action border rounded" @click="openResource('Linear Algebra • Notes')">
          <i class="bi bi-book me-2 text-secondary"></i>Linear Algebra • Notes
        </a>
      </div>
    </div>

    <!-- ⚡ Quick Actions -->
    <div class="mb-4">
      <h6 class="fw-semibold text-secondary mb-3">
        <i class="bi bi-lightning-charge-fill me-2 text-warning"></i>Quick actions
      </h6>
      <div class="d-grid gap-2">
        <button type="button" class="btn btn-light border text-start py-2" @click="viewDeadlines">
          <i class="bi bi-calendar-check me-2 text-danger"></i>View deadlines
        </button>
        <button type="button" class="btn btn-light border text-start py-2" @click="shareToClass">
          <i class="bi bi-share me-2 text-primary"></i>Share to class
        </button>
        <button type="button" class="btn btn-light border text-start py-2" @click="viewPinned">
          <i class="bi bi-pin-angle me-2 text-success"></i>Pinned resources
        </button>
      </div>
    </div>

    <!--  Continue Section -->
    <div>
      <h6 class="fw-semibold text-secondary mb-3">
        <i class="bi bi-clock-history me-2 text-info"></i>Continue where you left
      </h6>
      <div class="list-group small">
        <a href="#" class="list-group-item list-group-item-action border rounded mb-2 d-flex align-items-center" @click="continueStudy('CS301 Thread • Graphs')">
          <i class="bi bi-diagram-3-fill me-2 text-secondary"></i>
          CS301 Thread • Graphs
        </a>
        <a href="#" class="list-group-item list-group-item-action border rounded d-flex align-items-center" @click="continueStudy('Systems Lab • Setup')">
          <i class="bi bi-cpu-fill me-2 text-secondary"></i>
          Systems Lab • Setup
        </a>
      </div>
    </div>

    <!-- Deadlines Modal -->
    <div class="modal fade" id="deadlinesModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 shadow">
          <div class="modal-header bg-danger text-white rounded-top-4">
            <h5 class="modal-title"><i class="bi bi-calendar-check me-2"></i>Upcoming Deadlines</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <ul class="list-group small">
              <li class="list-group-item">CS301 Project • Due Nov 5</li>
              <li class="list-group-item">Linear Algebra Quiz • Due Nov 8</li>
              <li class="list-group-item">Systems Assignment • Due Nov 10</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Share Modal -->
    <div class="modal fade" id="shareModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 shadow">
          <div class="modal-header bg-primary text-white rounded-top-4">
            <h5 class="modal-title"><i class="bi bi-share me-2"></i>Share Resource</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" class="form-control mb-3" placeholder="Enter email or username" />
            <button class="btn btn-primary w-100 rounded-pill" @click="shareNow">Share</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    openResource(name) {
      alert(`Opening resource: ${name}`)
    },
    viewDeadlines() {
      const modal = new bootstrap.Modal(document.getElementById('deadlinesModal'))
      modal.show()
    },
    shareToClass() {
      const modal = new bootstrap.Modal(document.getElementById('shareModal'))
      modal.show()
    },
    viewPinned() {
      alert('Viewing all pinned resources ')
    },
    continueStudy(topic) {
      alert(`Resuming: ${topic}`)
    },
    shareNow() {
      alert('Resource shared successfully ')
      const modal = bootstrap.Modal.getInstance(document.getElementById('shareModal'))
      modal.hide()
    }
  }
}
</script>

<style scoped>
.list-group-item {
  transition: background 0.2s ease, transform 0.2s ease;
}
.list-group-item:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
}
.btn {
  transition: all 0.2s ease;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
</style>
