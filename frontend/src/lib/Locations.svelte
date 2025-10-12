<script>
  import { onMount } from 'svelte';
  import ConfirmModal from './ConfirmModal.svelte';
  import mapImage from '../assets/map.png';
  import { API_URL } from '../config.js';
  
  export let characterId;
  export let onBack;
  
  let locations = [];
  let filteredLocations = [];
  let character = null;
  let loading = true;
  let error = null;
  let showModal = false;
  let showConfirmDelete = false;
  let locationToDelete = null;
  
  // Фильтры по датам
  let startDate = '';
  let endDate = '';
  
  let formData = {
    x: 0,
    y: 0
  };

  async function fetchCharacter() {
    try {
      const response = await fetch(`${API_URL}/api/characters/${characterId}`);
      if (!response.ok) throw new Error('Ошибка загрузки персонажа');
      character = await response.json();
    } catch (e) {
      error = e.message;
    }
  }

  async function fetchLocations() {
    try {
      loading = true;
      error = null;
      const response = await fetch(`${API_URL}/api/locations/${characterId}`);
      if (!response.ok) throw new Error('Ошибка загрузки локаций');
      const data = await response.json();
      locations = data.locations.sort((a, b) => 
        new Date(a.created_at) - new Date(b.created_at)
      );
      applyDateFilter();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  function applyDateFilter() {
    filteredLocations = locations.filter(loc => {
      const locDate = new Date(loc.created_at);
      const start = startDate ? new Date(startDate) : null;
      const end = endDate ? new Date(endDate) : null;
      
      if (start && locDate < start) return false;
      if (end) {
        const endOfDay = new Date(end);
        endOfDay.setHours(23, 59, 59, 999);
        if (locDate > endOfDay) return false;
      }
      return true;
    });
  }

  function clearDateFilter() {
    startDate = '';
    endDate = '';
    applyDateFilter();
  }

  $: if (startDate || endDate) {
    applyDateFilter();
  }

  async function createLocation() {
    try {
      const response = await fetch(`${API_URL}/api/locations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          character_id: characterId,
          x: parseFloat(formData.x),
          y: parseFloat(formData.y)
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка создания локации');
      }
      
      closeModal();
      await fetchLocations();
    } catch (e) {
      alert(e.message);
    }
  }

  function confirmDeleteLocation(location) {
    locationToDelete = location;
    showConfirmDelete = true;
  }

  async function deleteLocation() {
    if (!locationToDelete) return;
    
    try {
      const response = await fetch(`${API_URL}/api/locations/${locationToDelete.id}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) throw new Error('Ошибка удаления');
      
      await fetchLocations();
      showConfirmDelete = false;
      locationToDelete = null;
    } catch (e) {
      alert(e.message);
      showConfirmDelete = false;
      locationToDelete = null;
    }
  }

  function cancelDelete() {
    showConfirmDelete = false;
    locationToDelete = null;
  }

  function openCreateModal() {
    formData = { x: 0, y: 0 };
    showModal = true;
  }

  function closeModal() {
    showModal = false;
    formData = { x: 0, y: 0 };
  }

  // Функция для создания плавной кривой между точками (Catmull-Rom)
  function createSmoothPath(points) {
    if (points.length < 2) return '';
    if (points.length === 2) {
      return `M ${points[0].x} ${points[0].y} L ${points[1].x} ${points[1].y}`;
    }
    
    let path = `M ${points[0].x} ${points[0].y}`;
    
    for (let i = 0; i < points.length - 1; i++) {
      const p0 = points[Math.max(0, i - 1)];
      const p1 = points[i];
      const p2 = points[i + 1];
      const p3 = points[Math.min(points.length - 1, i + 2)];
      
      // Catmull-Rom to Bezier conversion
      const cp1x = p1.x + (p2.x - p0.x) / 6;
      const cp1y = p1.y + (p2.y - p0.y) / 6;
      const cp2x = p2.x - (p3.x - p1.x) / 6;
      const cp2y = p2.y - (p3.y - p1.y) / 6;
      
      path += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${p2.x} ${p2.y}`;
    }
    
    return path;
  }

  // Функция для расчета угла стрелки
  function getArrowAngle(p1, p2) {
    return Math.atan2(p2.y - p1.y, p2.x - p1.x) * 180 / Math.PI;
  }

  onMount(() => {
    fetchCharacter();
    fetchLocations();
  });
</script>

<div class="locations-container">
  <div class="header">
    <div>
      <button class="btn-back" onclick={onBack}>
        ← Назад к персонажам
      </button>
      {#if character}
        <h2>📍 Локации: {character.name}</h2>
        <p class="character-description">{character.description}</p>
      {/if}
    </div>
    <button class="btn-primary" onclick={openCreateModal}>
      ➕ Добавить локацию
    </button>
  </div>

  {#if !loading && locations.length > 0}
    <div class="date-filters">
      <div class="filter-group">
        <label for="start-date">От:</label>
        <input 
          id="start-date"
          type="date" 
          bind:value={startDate}
          class="date-input"
        />
      </div>
      <div class="filter-group">
        <label for="end-date">До:</label>
        <input 
          id="end-date"
          type="date" 
          bind:value={endDate}
          class="date-input"
        />
      </div>
      {#if startDate || endDate}
        <button class="btn-clear" onclick={clearDateFilter}>
          ✕ Очистить
        </button>
      {/if}
      <div class="filter-info">
        Показано локаций: <strong>{filteredLocations.length}</strong> из <strong>{locations.length}</strong>
      </div>
    </div>
  {/if}

  {#if loading}
    <div class="loading">Загрузка...</div>
  {:else if error}
    <div class="error">{error}</div>
  {:else if locations.length === 0}
    <div class="empty">
      <p>У этого персонажа пока нет локаций</p>
      <button class="btn-primary" onclick={openCreateModal}>
        Создать первую локацию
      </button>
    </div>
  {:else}
    <div class="locations-grid">
      {#each filteredLocations as location}
        <div class="location-card">
          <div class="location-header">
            <h3>🗺️ Локация</h3>
            <button 
              class="btn-icon" 
              onclick={() => confirmDeleteLocation(location)}
              title="Удалить"
            >
              🗑️
            </button>
          </div>
          <div class="coordinates">
            <div class="coord">
              <span class="label">X:</span>
              <span class="value">{location.x}</span>
            </div>
            <div class="coord">
              <span class="label">Y:</span>
              <span class="value">{location.y}</span>
            </div>
          </div>
          <div class="location-footer">
            <small>Создана: {new Date(location.created_at).toLocaleString('ru-RU')}</small>
          </div>
        </div>
      {/each}
    </div>
    
    <div class="map-container">
      <h3>🗺️ Карта маршрута</h3>
      <div class="map-wrapper">
        <img src={mapImage} alt="Карта" class="map-background" />
        <svg class="map-overlay" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
          <!-- Плавная кривая между точками -->
          {#if filteredLocations.length > 1}
            <path
              d={createSmoothPath(filteredLocations.map(loc => ({
                x: 50 + loc.x / 2,
                y: 50 - loc.y / 2
              })))}
              stroke="#e74c3c"
              stroke-width="0.5"
              fill="none"
              stroke-dasharray="2,1"
              opacity="0.7"
            />
            
            <!-- Стрелки направления -->
            {#each filteredLocations.slice(0, -1) as location, i}
              {@const nextLoc = filteredLocations[i + 1]}
              {@const x1 = 50 + location.x / 2}
              {@const y1 = 50 - location.y / 2}
              {@const x2 = 50 + nextLoc.x / 2}
              {@const y2 = 50 - nextLoc.y / 2}
              {@const midX = (x1 + x2) / 2}
              {@const midY = (y1 + y2) / 2}
              {@const angle = getArrowAngle({x: x1, y: y1}, {x: x2, y: y2})}
              
              <g transform="translate({midX}, {midY}) rotate({angle})">
                <polygon
                  points="0,-1 2,0 0,1"
                  fill="#e74c3c"
                  opacity="0.8"
                />
              </g>
            {/each}
          {/if}
          
          <!-- Красные точки локаций -->
          {#each filteredLocations as location, i}
            <g>
              <circle 
                cx={50 + location.x / 2}
                cy={50 - location.y / 2}
                r="1.5"
                fill="#e74c3c"
                stroke="white"
                stroke-width="0.3"
                opacity="0.9"
              />
              <!-- Пульсирующий эффект для первой и последней точки -->
              {#if i === 0 || i === filteredLocations.length - 1}
                <circle 
                  cx={50 + location.x / 2}
                  cy={50 - location.y / 2}
                  r="1.5"
                  fill="none"
                  stroke="#e74c3c"
                  stroke-width="0.3"
                  opacity="0.6"
                >
                  <animate
                    attributeName="r"
                    from="1.5"
                    to="3"
                    dur="1.5s"
                    repeatCount="indefinite"
                  />
                  <animate
                    attributeName="opacity"
                    from="0.6"
                    to="0"
                    dur="1.5s"
                    repeatCount="indefinite"
                  />
                </circle>
              {/if}
            </g>
          {/each}
          
          <!-- Метки начала и конца -->
          {#if filteredLocations.length > 0}
            <text 
              x={50 + filteredLocations[0].x / 2 + 2}
              y={50 - filteredLocations[0].y / 2 - 2}
              font-size="3"
              fill="#27ae60"
              font-weight="bold"
            >
              START
            </text>
            {#if filteredLocations.length > 1}
              <text 
                x={50 + filteredLocations[filteredLocations.length - 1].x / 2 + 2}
                y={50 - filteredLocations[filteredLocations.length - 1].y / 2 - 2}
                font-size="3"
                fill="#e74c3c"
                font-weight="bold"
              >
                END
              </text>
            {/if}
          {/if}
        </svg>
      </div>
      <div class="map-legend">
        <div class="legend-item">
          <span class="legend-dot start"></span>
          <span>Начало маршрута</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot end"></span>
          <span>Конец маршрута</span>
        </div>
        <div class="legend-item">
          <span class="legend-line"></span>
          <span>Путь следования</span>
        </div>
      </div>
    </div>
  {/if}
</div>

{#if showModal}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="modal-overlay" onclick={closeModal}>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="modal" onclick={(e) => e.stopPropagation()}>
      <h3>Новая локация</h3>
      <form onsubmit={(e) => { e.preventDefault(); createLocation(); }}>
        <div class="form-group">
          <label for="x">Координата X</label>
          <input 
            id="x"
            type="number" 
            bind:value={formData.x}
            required
            step="0.1"
            min="-100"
            max="100"
            placeholder="От -100 до 100"
          />
        </div>
        <div class="form-group">
          <label for="y">Координата Y</label>
          <input 
            id="y"
            type="number" 
            bind:value={formData.y}
            required
            step="0.1"
            min="-100"
            max="100"
            placeholder="От -100 до 100"
          />
        </div>
        <div class="modal-actions">
          <button type="button" class="btn-secondary" onclick={closeModal}>
            Отмена
          </button>
          <button type="submit" class="btn-primary">
            Создать
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}

<ConfirmModal 
  show={showConfirmDelete}
  title="Удаление локации"
  message={locationToDelete ? `Вы уверены, что хотите удалить локацию с координатами X: ${locationToDelete.x}, Y: ${locationToDelete.y}? Это действие необратимо.` : ''}
  confirmText="Удалить"
  cancelText="Отмена"
  danger={true}
  onConfirm={deleteLocation}
  onCancel={cancelDelete}
/>

<style>
  .locations-container {
    padding: 1rem;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2rem;
  }

  .btn-back {
    background: none;
    border: none;
    color: #667eea;
    cursor: pointer;
    font-size: 1rem;
    padding: 0.5rem 0;
    margin-bottom: 1rem;
    font-weight: 600;
    display: block;
  }

  .btn-back:hover {
    text-decoration: underline;
  }

  h2 {
    margin: 0 0 0.5rem 0;
    color: #333;
  }

  .character-description {
    color: #666;
    margin: 0;
  }

  .date-filters {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 2rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    flex-wrap: wrap;
  }

  .filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .filter-group label {
    font-weight: 600;
    color: #666;
    font-size: 0.9rem;
  }

  .date-input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 0.9rem;
    font-family: inherit;
  }

  .date-input:focus {
    outline: none;
    border-color: #667eea;
  }

  .btn-clear {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.3s;
  }

  .btn-clear:hover {
    background: #c0392b;
  }

  .filter-info {
    margin-left: auto;
    color: #666;
    font-size: 0.9rem;
  }

  .filter-info strong {
    color: #667eea;
  }

  .loading, .error, .empty {
    text-align: center;
    padding: 3rem;
    font-size: 1.1rem;
  }

  .error {
    color: #e74c3c;
  }

  .empty {
    color: #666;
  }

  .locations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .location-card {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .location-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .location-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .location-header h3 {
    margin: 0;
    color: #667eea;
    font-size: 1.1rem;
  }

  .coordinates {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .coord {
    flex: 1;
    background: white;
    padding: 0.7rem;
    border-radius: 6px;
    display: flex;
    justify-content: space-between;
  }

  .coord .label {
    color: #999;
    font-weight: 600;
  }

  .coord .value {
    color: #333;
    font-weight: 700;
    font-size: 1.1rem;
  }

  .location-footer {
    padding-top: 1rem;
    border-top: 1px solid #e0e0e0;
  }

  .location-footer small {
    color: #999;
  }

  .map-container {
    margin-top: 3rem;
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 8px;
  }

  .map-container h3 {
    margin: 0 0 1rem 0;
    color: #333;
  }

  .map-wrapper {
    position: relative;
    width: 100%;
    padding-top: 100%; /* Квадратное соотношение сторон */
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .map-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .map-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .map-legend {
    display: flex;
    gap: 2rem;
    margin-top: 1rem;
    padding: 1rem;
    background: white;
    border-radius: 8px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #666;
  }

  .legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
  }

  .legend-dot.start {
    background: #27ae60;
    box-shadow: 0 0 8px rgba(39, 174, 96, 0.5);
  }

  .legend-dot.end {
    background: #e74c3c;
    box-shadow: 0 0 8px rgba(231, 76, 60, 0.5);
  }

  .legend-line {
    width: 30px;
    height: 2px;
    background: #e74c3c;
    display: inline-block;
    position: relative;
  }

  .legend-line::after {
    content: '→';
    position: absolute;
    right: -10px;
    top: -8px;
    color: #e74c3c;
  }

  .btn-primary {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.7rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.3s;
  }

  .btn-primary:hover {
    background: #5568d3;
  }

  .btn-secondary {
    background: #e0e0e0;
    color: #333;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.3s;
  }

  .btn-secondary:hover {
    background: #d0d0d0;
  }

  .btn-icon {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0.3rem;
    transition: transform 0.2s;
  }

  .btn-icon:hover {
    transform: scale(1.2);
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    width: 90%;
    max-width: 400px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }

  .modal h3 {
    margin: 0 0 1.5rem 0;
    color: #333;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #666;
    font-weight: 600;
  }

  .form-group input {
    width: 100%;
    padding: 0.7rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    box-sizing: border-box;
  }

  .form-group input:focus {
    outline: none;
    border-color: #667eea;
  }

  .modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
  }
</style>
