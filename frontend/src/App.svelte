<script>
  import Characters from './lib/Characters.svelte';
  import Locations from './lib/Locations.svelte';
  
  let activeTab = 'characters';
  let selectedCharacterId = null;
  
  function selectCharacter(id) {
    selectedCharacterId = id;
    activeTab = 'locations';
  }
  
  function backToCharacters() {
    activeTab = 'characters';
    selectedCharacterId = null;
  }
</script>

<main>
  <header>
    <h1>Властелин колец</h1>
    <p>Управление персонажами и их локациями</p>
  </header>

  <div class="tabs">
    <button 
      class:active={activeTab === 'characters'}
      onclick={() => { activeTab = 'characters'; selectedCharacterId = null; }}
    >
      👥 Персонажи
    </button>
    <button 
      class:active={activeTab === 'locations'}
      onclick={() => activeTab = 'locations'}
      disabled={!selectedCharacterId}
    >
      📍 Локации
    </button>
  </div>

  <div class="content">
    <div class="page-container">
      {#if activeTab === 'characters'}
        <div class="page" style="animation: slideIn 0.4s ease-out;">
          <Characters onSelectCharacter={selectCharacter} />
        </div>
      {:else if activeTab === 'locations'}
        <div class="page" style="animation: slideIn 0.4s ease-out;">
          <Locations characterId={selectedCharacterId} onBack={backToCharacters} />
        </div>
      {/if}
    </div>
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
  }

  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  header {
    text-align: center;
    color: white;
    margin-bottom: 2rem;
  }

  header h1 {
    margin: 0;
    font-size: 3rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
  }

  header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
  }

  .tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    justify-content: center;
  }

  .tabs button {
    padding: 0.8rem 1.5rem;
    border: none;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
  }

  .tabs button:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }

  .tabs button.active {
    background: white;
    color: #667eea;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .tabs button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .content {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    min-height: 500px;
    overflow: hidden;
  }

  .page-container {
    position: relative;
  }

  .page {
    width: 100%;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(20px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
</style>
