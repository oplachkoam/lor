<script>
  import { onMount } from 'svelte';
  import ConfirmModal from './ConfirmModal.svelte';
  import { API_URL } from '../config.js';
  
  export let onSelectCharacter;
  
  let characters = [];
  let loading = true;
  let error = null;
  let showModal = false;
  let editingCharacter = null;
  let showConfirmDelete = false;
  let characterToDelete = null;
  
  let formData = {
    name: '',
    description: ''
  };

  async function fetchCharacters() {
    try {
      loading = true;
      error = null;
      const response = await fetch(`${API_URL}/api/characters`);
      if (!response.ok) throw new Error('Ошибка загрузки персонажей');
      const data = await response.json();
      characters = data.characters;
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function saveCharacter() {
    try {
      const url = editingCharacter 
        ? `${API_URL}/api/characters/${editingCharacter.id}`
        : `${API_URL}/api/characters`;
      
      const method = editingCharacter ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка сохранения');
      }
      
      closeModal();
      await fetchCharacters();
    } catch (e) {
      alert(e.message);
    }
  }

  function confirmDeleteCharacter(character) {
    characterToDelete = character;
    showConfirmDelete = true;
  }

  async function deleteCharacter() {
    if (!characterToDelete) return;
    
    try {
      const response = await fetch(`${API_URL}/api/characters/${characterToDelete.id}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) throw new Error('Ошибка удаления');
      
      await fetchCharacters();
      showConfirmDelete = false;
      characterToDelete = null;
    } catch (e) {
      alert(e.message);
      showConfirmDelete = false;
      characterToDelete = null;
    }
  }

  function cancelDelete() {
    showConfirmDelete = false;
    characterToDelete = null;
  }

  function openCreateModal() {
    editingCharacter = null;
    formData = { name: '', description: '' };
    showModal = true;
  }

  function openEditModal(character) {
    editingCharacter = character;
    formData = {
      name: character.name,
      description: character.description
    };
    showModal = true;
  }

  function closeModal() {
    showModal = false;
    editingCharacter = null;
    formData = { name: '', description: '' };
  }

  onMount(fetchCharacters);
</script>

<div class="characters-container">
  <div class="header">
    <h2>Персонажи</h2>
    <button class="btn-primary" onclick={openCreateModal}>
      ➕ Добавить персонажа
    </button>
  </div>

  {#if loading}
    <div class="loading">Загрузка...</div>
  {:else if error}
    <div class="error">{error}</div>
  {:else if characters.length === 0}
    <div class="empty">
      <p>Пока нет персонажей</p>
      <button class="btn-primary" onclick={openCreateModal}>
        Создать первого персонажа
      </button>
    </div>
  {:else}
    <div class="characters-grid">
      {#each characters as character}
        <div class="character-card">
          <div class="character-header">
            <h3>{character.name}</h3>
            <div class="actions">
              <button 
                class="btn-icon" 
                onclick={() => openEditModal(character)}
                title="Редактировать"
              >
                ✏️
              </button>
              <button 
                class="btn-icon" 
                onclick={() => confirmDeleteCharacter(character)}
                title="Удалить"
              >
                🗑️
              </button>
            </div>
          </div>
          <p class="description">{character.description}</p>
          <div class="character-footer">
            <small>Создан: {new Date(character.created_at).toLocaleString('ru-RU')}</small>
            <button 
              class="btn-secondary"
              onclick={() => onSelectCharacter(character.id)}
            >
              📍 Локации
            </button>
          </div>
        </div>
      {/each}
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
      <h3>{editingCharacter ? 'Редактировать персонажа' : 'Новый персонаж'}</h3>
      <form onsubmit={(e) => { e.preventDefault(); saveCharacter(); }}>
        <div class="form-group">
          <label for="name">Имя</label>
          <input 
            id="name"
            type="text" 
            bind:value={formData.name}
            required
            placeholder="Введите имя персонажа"
          />
        </div>
        <div class="form-group">
          <label for="description">Описание</label>
          <textarea 
            id="description"
            bind:value={formData.description}
            required
            placeholder="Введите описание персонажа"
            rows="4"
          ></textarea>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn-secondary" onclick={closeModal}>
            Отмена
          </button>
          <button type="submit" class="btn-primary">
            {editingCharacter ? 'Сохранить' : 'Создать'}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}

<ConfirmModal 
  show={showConfirmDelete}
  title="Удаление персонажа"
  message={characterToDelete ? `Вы уверены, что хотите удалить персонажа "${characterToDelete.name}"? Это действие необратимо.` : ''}
  confirmText="Удалить"
  cancelText="Отмена"
  danger={true}
  onConfirm={deleteCharacter}
  onCancel={cancelDelete}
/>

<style>
  .characters-container {
    padding: 1rem;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  h2 {
    margin: 0;
    color: #333;
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

  .characters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .character-card {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .character-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .character-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }

  .character-header h3 {
    margin: 0;
    color: #667eea;
    font-size: 1.3rem;
  }

  .actions {
    display: flex;
    gap: 0.5rem;
  }

  .description {
    color: #666;
    margin: 0 0 1rem 0;
    line-height: 1.5;
  }

  .character-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e0e0e0;
  }

  .character-footer small {
    color: #999;
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
    font-size: 0.9rem;
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
    max-width: 500px;
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

  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: 0.7rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    box-sizing: border-box;
  }

  .form-group input:focus,
  .form-group textarea:focus {
    outline: none;
    border-color: #667eea;
  }

  .modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
  }
</style>

