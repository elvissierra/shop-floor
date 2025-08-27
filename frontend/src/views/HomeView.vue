
// store now uses GraphQL service

<template>
  <div class="home">
    <div class="hero">
      <h1>Shop Floor Management</h1>
      <p class="subtitle">Streamline your manufacturing process with our comprehensive shop floor management platform</p>
      <div class="cta-buttons">
        <router-link to="/departments" class="cta-button primary">View Departments</router-link>
        <router-link to="/parts" class="cta-button secondary">Manage Parts</router-link>
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">🏭</div>
        <h3>Department Management</h3>
        <p>Organize and track your manufacturing departments efficiently</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🔧</div>
        <h3>Part Tracking</h3>
        <p>Monitor parts through the entire production lifecycle</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Quality Control</h3>
        <p>Maintain high standards with comprehensive quality tracking</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">⚠️</div>
        <h3>Defect Management</h3>
        <p>Identify and address production issues quickly</p>
      </div>
    </div>

    <div class="stats-section">
      <div class="stat-card">
        <h3>Active Departments</h3>
        <p class="stat-number">{{ departmentCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Parts</h3>
        <p class="stat-number">{{ partCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Quality Rate</h3>
        <p class="stat-number">{{ qualityRate }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useShopFloorStore } from '../stores/shopFloor';

const store = useShopFloorStore();
const departmentCount = ref(0);
const partCount = ref(0);
const qualityRate = ref(0);

onMounted(async () => {
  try {
    const departments = await store.fetchDepartments();
    const parts = await store.fetchParts();
    departmentCount.value = departments.length;
    partCount.value = parts.length;
    // Calculate quality rate (example calculation)
    qualityRate.value = 98;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.cta-button {
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}

.cta-button:hover {
  transform: translateY(-2px);
}

.primary {
  background-color: #42b983;
  color: white;
}

.secondary {
  background-color: white;
  color: #2c3e50;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #666;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  background: white;
  margin-top: 2rem;
}

.stat-card {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #42b983;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .features {
    grid-template-columns: 1fr;
  }
}
</style> 